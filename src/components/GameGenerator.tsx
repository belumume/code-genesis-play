import React, { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Play, Download, AlertCircle, CheckCircle, FileText, Code, Eye, Bot, TestTube, Wrench, Lightbulb } from 'lucide-react';
import { toast } from 'sonner';
import { useApiConfig } from '@/hooks/useApiConfig';
import { useAuth } from '@/hooks/useAuth';
import { supabase } from '@/integrations/supabase/client';
import type { Tables } from '@/integrations/supabase/types';
import { FileViewer } from './FileViewer';

interface ProgressUpdate {
  session_id: string;
  phase: string;
  step: string;
  progress: number;
  message: string;
  timestamp: string;
  file_created?: string;
  file_content?: string;
}

interface GenerationSession {
  session_id: string;
  status: 'started' | 'generating' | 'completed' | 'failed';
  prompt: string;
  created_at: string;
  progress_updates: ProgressUpdate[];
  error?: string;
  game_path?: string;
}

interface GeneratedFile {
  name: string;
  path: string;
  content: string;
  type: 'python' | 'markdown' | 'other';
}

// Production Configuration:
// In Lovable, set these environment variables:
// VITE_API_BASE_URL = https://your-app.onrender.com
// VITE_WS_BASE_URL = wss://your-app.onrender.com
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000';

// Detect if running on Lovable platform
const isLovablePlatform = window.location.hostname.includes('lovable.app');
const DEMO_MODE = false; // Disabled for production

export function GameGenerator() {
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentSession, setCurrentSession] = useState<GenerationSession | null>(null);
  const [progress, setProgress] = useState(0);
  const [currentPhase, setCurrentPhase] = useState('');
  const [currentMessage, setCurrentMessage] = useState('');
  const [progressUpdates, setProgressUpdates] = useState<ProgressUpdate[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [generatedFiles, setGeneratedFiles] = useState<GeneratedFile[]>([]);
  const [selectedFile, setSelectedFile] = useState<GeneratedFile | null>(null);
  const [showFileViewer, setShowFileViewer] = useState(false);

  const websocketRef = useRef<WebSocket | null>(null);
  const { apiBaseUrl, wsBaseUrl, isLoading: configLoading } = useApiConfig();

  // Redirect to auth if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated && !window.location.pathname.includes('/auth')) {
      window.location.href = '/auth';
    }
  }, [authLoading, isAuthenticated]);

  const connectWebSocket = (sessionId: string) => {
    const ws = new WebSocket(`${wsBaseUrl}/ws/generate`);
    websocketRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket connected');
      // Send the generation request after connection
      ws.send(JSON.stringify({
        prompt: prompt.trim(),
        session_id: sessionId
      }));
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.error) {
          setError(data.error);
          setIsGenerating(false);
          return;
        }

        const update: ProgressUpdate = data;
        
        setProgressUpdates(prev => [...prev, update]);
        setProgress(update.progress * 100);
        setCurrentPhase(update.phase);
        setCurrentMessage(update.message);

        // Handle file creation updates
        if (update.file_created && update.file_content) {
          const fileType = update.file_created.endsWith('.py') ? 'python' : 
                          update.file_created.endsWith('.md') ? 'markdown' : 'other';
          
          const newFile: GeneratedFile = {
            name: update.file_created.split('/').pop() || update.file_created,
            path: update.file_created,
            content: update.file_content,
            type: fileType
          };
          
          setGeneratedFiles(prev => [...prev, newFile]);
          toast.success(`File created: ${newFile.name}`);
        }

        // Handle completion
        if (update.phase === 'COMPLETED') {
          setIsGenerating(false);
          toast.success('Game generated successfully!');
          fetchGeneratedFiles(sessionId);
        } else if (update.phase === 'FAILED' || update.phase === 'ERROR') {
          setIsGenerating(false);
          setError(update.message);
          toast.error('Game generation failed');
        }
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setError('Connection error occurred');
      setIsGenerating(false);
    };
  };

  const fetchGeneratedFiles = async (sessionId: string) => {
    try {
      const response = await fetch(`${apiBaseUrl}/api/games/${sessionId}/files`);
      if (response.ok) {
        const files = await response.json();
        setGeneratedFiles(files);
      }
    } catch (err) {
      console.error('Failed to fetch generated files:', err);
    }
  };

  const startGeneration = async () => {
    if (!user) {
      toast.error('Please log in to generate games');
      return;
    }

    if (!prompt.trim()) {
      toast.error('Please enter a game concept');
      return;
    }

    setIsGenerating(true);
    setError(null);
    setProgress(0);
    setCurrentPhase('');
    setCurrentMessage('');
    setProgressUpdates([]);
    setGeneratedFiles([]);

    // Demo mode for Lovable platform
    if (DEMO_MODE) {
      simulateDemoGeneration();
      return;
    }

    try {
      // Create session in database first with proper typing
      const { data: sessionData, error: sessionError } = await supabase
        .from('game_sessions')
        .insert({
          user_id: user.id,
          prompt: prompt.trim(),
          status: 'started'
        })
        .select()
        .single();

      if (sessionError) {
        console.error('Session creation error:', sessionError);
        throw new Error(`Failed to create session: ${sessionError.message}`);
      }
      
      if (!sessionData) {
        throw new Error('Failed to create session - no data returned');
      }

      console.log('Starting generation with API URL:', apiBaseUrl);
      const response = await fetch(`${apiBaseUrl}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt.trim(),
          user_id: user.id,
          session_id: sessionData.id,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setCurrentSession({
        session_id: result.session_id || sessionData.id,
        status: 'started',
        prompt: prompt.trim(),
        created_at: new Date().toISOString(),
        progress_updates: [],
      });

      connectWebSocket(result.session_id || sessionData.id);
      toast.success('Game generation started!');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to start generation';
      setError(errorMessage);
      setIsGenerating(false);
      toast.error(errorMessage);
    }
  };

  const simulateDemoGeneration = async () => {
    const sessionId = `demo-${Date.now()}`;
    setCurrentSession({
      session_id: sessionId,
      status: 'started',
      prompt: prompt.trim(),
      created_at: new Date().toISOString(),
      progress_updates: [],
    });

    toast.success('Demo generation started!');

    // Simulate phases
    const phases = [
      { phase: 'DESIGN', message: 'Conceptualizing game design...', progress: 0.1 },
      { phase: 'PLANNING', message: 'Creating technical specifications...', progress: 0.3 },
      { phase: 'CODING', message: 'Generating game code...', progress: 0.6 },
      { phase: 'VERIFICATION', message: 'Verifying generated game...', progress: 0.9 },
    ];

    for (const [index, phase] of phases.entries()) {
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setCurrentPhase(phase.phase);
      setCurrentMessage(phase.message);
      setProgress(phase.progress * 100);
      
      setProgressUpdates(prev => [...prev, {
        session_id: sessionId,
        phase: phase.phase,
        step: 'processing',
        progress: phase.progress,
        message: phase.message,
        timestamp: new Date().toISOString(),
      }]);

      // Simulate file creation
      if (phase.phase === 'CODING') {
        const demoFiles = [
          { name: 'main.py', content: generateDemoMainPy() },
          { name: 'GDD.md', content: generateDemoGDD() },
          { name: 'TECH_PLAN.md', content: generateDemoTechPlan() },
        ];
        setGeneratedFiles(demoFiles.map(f => ({ ...f, type: f.name.endsWith('.py') ? 'python' : 'markdown', path: f.name })));
      }
    }

    setIsGenerating(false);
    setCurrentPhase('COMPLETED');
    setProgress(100);
    toast.success('Demo generation completed!');
  };

  const generateDemoMainPy = () => `import pygame
import sys

# Initialize Pygame
pygame.init()

# Game window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("${prompt}")

# Colors
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear screen
    screen.fill(WHITE)
    
    # Draw demo content
    pygame.draw.circle(screen, BLUE, (400, 300), 50)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()`;

  const generateDemoGDD = () => `# Game Design Document
## ${prompt}

### Overview
This game was generated by AI Genesis Engine based on your prompt.

### Core Mechanics
- Movement controls
- Collision detection
- Score system

### Visual Style
- Minimalist design with geometric shapes
- Vibrant color palette
`;

  const generateDemoTechPlan = () => `# Technical Plan

## Architecture
- main.py: Entry point and game loop
- player.py: Player character logic
- world.py: Game world and level management

## Technologies
- Python 3.8+
- Pygame library
`;

  const stopGeneration = () => {
    if (websocketRef.current) {
      websocketRef.current.close();
    }
    setIsGenerating(false);
    setCurrentSession(null);
    setProgress(0);
    setCurrentPhase('');
    setCurrentMessage('');
  };

  const downloadFile = (file: GeneratedFile) => {
    const blob = new Blob([file.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = file.name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const downloadAllFiles = async () => {
    if (!currentSession) return;
    
    // Demo mode: Create zip in browser
    if (DEMO_MODE) {
      const zip = generatedFiles.map(file => 
        `--- ${file.name} ---\n${file.content}\n\n`
      ).join('');
      
      const blob = new Blob([zip], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `game_${currentSession.session_id}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      toast.success('Demo files downloaded!');
      return;
    }
    
    try {
      const response = await fetch(`${apiBaseUrl}/api/games/${currentSession.session_id}/download`);
      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `game_${currentSession.session_id}.zip`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        toast.success('Game files downloaded!');
      }
    } catch (err) {
      toast.error('Failed to download game files');
    }
  };

  const viewFile = (file: GeneratedFile) => {
    setSelectedFile(file);
    setShowFileViewer(true);
  };

  const playGame = (file: GeneratedFile) => {
    if (file.name.endsWith('.html')) {
      // Create a blob URL for the HTML content and open in new tab
      const blob = new Blob([file.content], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      const newWindow = window.open(url, '_blank');
      
      // Clean up the blob URL after a delay
      setTimeout(() => {
        URL.revokeObjectURL(url);
      }, 1000);
      
      toast.success('Game opened in new tab!');
    }
  };

  const closeFileViewer = () => {
    setShowFileViewer(false);
    setSelectedFile(null);
  };

  // Cleanup WebSocket on unmount
  useEffect(() => {
    return () => {
      if (websocketRef.current) {
        websocketRef.current.close();
      }
    };
  }, []);

  const getPhaseIcon = (phase: string) => {
    switch (phase) {
      case 'COMPLETED':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'FAILED':
      case 'ERROR':
        return <AlertCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Loader2 className="h-4 w-4 animate-spin text-blue-500" />;
    }
  };

  const getPhaseColor = (phase: string) => {
    switch (phase) {
      case 'DESIGN': return 'bg-purple-500';
      case 'PLANNING': return 'bg-blue-500';
      case 'CODING': return 'bg-green-500';
      case 'VERIFICATION': return 'bg-yellow-500';
      case 'COMPLETED': return 'bg-emerald-500';
      case 'FAILED':
      case 'ERROR': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'python': return <Code className="h-4 w-4 text-blue-500" />;
      case 'markdown': return <FileText className="h-4 w-4 text-green-500" />;
      default: return <FileText className="h-4 w-4 text-gray-500" />;
    }
  };

  if (authLoading || configLoading) {
    return (
      <div className="max-w-6xl mx-auto space-y-6">
        <Card>
          <CardContent className="flex items-center justify-center py-8">
            <div className="flex items-center gap-2">
              <Loader2 className="h-5 w-5 animate-spin" />
              <span>Loading...</span>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect to auth
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Connection Status */}
      <Card>
        <CardContent className="py-4">
          <div className="flex items-center gap-2 text-sm">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>Connected to: {apiBaseUrl}</span>
            <div className="ml-auto flex items-center gap-2 text-muted-foreground">
              <span>Logged in as: {user?.email}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Left Column - Input and Progress */}
      <div className="space-y-6">
        {/* Input Section */}
        <Card>
          <CardHeader>
            <CardTitle>Game Concept</CardTitle>
            <CardDescription>
              Describe your game idea in a single sentence. The AI will create a complete, playable game from your concept.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Textarea
              placeholder="e.g., A space platformer where you collect crystals while avoiding alien enemies"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="min-h-[100px]"
              disabled={isGenerating}
            />
            <div className="flex gap-2">
              <Button 
                onClick={startGeneration} 
                disabled={isGenerating || !prompt.trim()}
                className="flex-1"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Game...
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-4 w-4" />
                    Generate Game
                  </>
                )}
              </Button>
              {isGenerating && (
                <Button variant="outline" onClick={stopGeneration}>
                  Cancel
                </Button>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Error Display */}
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Progress Section */}
        {isGenerating && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Loader2 className="h-5 w-5 animate-spin" />
                Generating Your Game
              </CardTitle>
              <CardDescription>
                AI is creating a complete game from your prompt...
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>{currentPhase && `Phase: ${currentPhase}`}</span>
                  <span>{Math.round(progress)}%</span>
                </div>
                <Progress value={progress} className="h-2" />
              </div>
              
              {currentMessage && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  {getPhaseIcon(currentPhase)}
                  <span>{currentMessage}</span>
                </div>
              )}

              {currentPhase && (
                <Badge 
                  variant="secondary" 
                  className={`${getPhaseColor(currentPhase)} text-white`}
                >
                  {currentPhase}
                </Badge>
              )}
            </CardContent>
          </Card>
        )}
      </div>

      {/* Right Column - Files and Progress Log */}
      <div className="space-y-6">
        {/* Generated Files */}
        {generatedFiles.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Generated Files</span>
                <Button 
                  size="sm" 
                  variant="outline" 
                  onClick={downloadAllFiles}
                  className="flex items-center gap-2"
                >
                  <Download className="h-4 w-4" />
                  Download All
                </Button>
              </CardTitle>
              <CardDescription>
                Files created during game generation
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {generatedFiles.map((file, index) => (
                  <div key={index} className="flex items-center justify-between p-2 rounded-lg bg-muted hover:bg-muted/80 transition-colors cursor-pointer">
                    <div className="flex items-center gap-2" onClick={() => viewFile(file)}>
                      {getFileIcon(file.type)}
                      <span className="text-sm font-medium">{file.name}</span>
                      <Badge variant="secondary" className="text-xs">
                        {file.content.split('\n').length} lines
                      </Badge>
                      {file.name.endsWith('.html') && (
                        <Badge variant="default" className="text-xs bg-green-500">
                          Playable
                        </Badge>
                      )}
                    </div>
                    <div className="flex gap-1">
                      {file.name.endsWith('.html') && (
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => playGame(file)}
                          className="h-6 w-6 p-0 text-green-600 hover:text-green-700"
                          title="Play Game"
                        >
                          <Play className="h-3 w-3" />
                        </Button>
                      )}
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => viewFile(file)}
                        className="h-6 w-6 p-0"
                      >
                        <Eye className="h-3 w-3" />
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => downloadFile(file)}
                        className="h-6 w-6 p-0"
                      >
                        <Download className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Progress Updates Log */}
        {progressUpdates.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Generation Log</CardTitle>
              <CardDescription>
                Real-time updates from the AI generation process
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {progressUpdates.map((update, index) => (
                  <div key={index} className="flex items-center gap-2 text-sm p-2 rounded-lg bg-muted">
                    {getPhaseIcon(update.phase)}
                    <Badge variant="outline" className="text-xs">
                      {update.phase}
                    </Badge>
                    <span className="flex-1">{update.message}</span>
                    <span className="text-xs text-muted-foreground">
                      {new Date(update.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* File Viewer Dialog */}
      <FileViewer
        file={selectedFile}
        isOpen={showFileViewer}
        onClose={closeFileViewer}
        onDownload={downloadFile}
      />
    </div>
  );
}
