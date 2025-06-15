
import React, { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, Play, Download, AlertCircle, CheckCircle } from 'lucide-react';
import { toast } from 'sonner';

interface ProgressUpdate {
  session_id: string;
  phase: string;
  step: string;
  progress: number;
  message: string;
  timestamp: string;
}

interface GenerationSession {
  session_id: string;
  status: 'started' | 'generating' | 'completed' | 'failed';
  prompt: string;
  created_at: string;
  progress_updates: ProgressUpdate[];
  error?: string;
}

const API_BASE_URL = 'http://localhost:8000';
const WS_BASE_URL = 'ws://localhost:8000';

export function GameGenerator() {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentSession, setCurrentSession] = useState<GenerationSession | null>(null);
  const [progress, setProgress] = useState(0);
  const [currentPhase, setCurrentPhase] = useState('');
  const [currentMessage, setCurrentMessage] = useState('');
  const [progressUpdates, setProgressUpdates] = useState<ProgressUpdate[]>([]);
  const [error, setError] = useState<string | null>(null);

  const websocketRef = useRef<WebSocket | null>(null);

  const connectWebSocket = (sessionId: string) => {
    const ws = new WebSocket(`${WS_BASE_URL}/ws/${sessionId}`);
    websocketRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket connected');
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

        // Handle completion
        if (update.phase === 'COMPLETED') {
          setIsGenerating(false);
          toast.success('Game generated successfully!');
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

  const startGeneration = async () => {
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

    try {
      const response = await fetch(`${API_BASE_URL}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setCurrentSession({
        session_id: result.session_id,
        status: 'started',
        prompt: prompt.trim(),
        created_at: new Date().toISOString(),
        progress_updates: [],
      });

      // Connect WebSocket for real-time updates
      connectWebSocket(result.session_id);

      toast.success('Game generation started!');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to start generation';
      setError(errorMessage);
      setIsGenerating(false);
      toast.error(errorMessage);
    }
  };

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

  return (
    <div className="max-w-4xl mx-auto space-y-6">
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

      {/* Success Section */}
      {currentSession?.status === 'completed' && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-600">
              <CheckCircle className="h-5 w-5" />
              Game Generated Successfully!
            </CardTitle>
            <CardDescription>
              Your game has been created and is ready to play.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-2">
              <Button className="flex-1">
                <Download className="mr-2 h-4 w-4" />
                Download Game
              </Button>
              <Button variant="outline">
                <Play className="mr-2 h-4 w-4" />
                View Code
              </Button>
            </div>
            
            <div className="p-4 bg-muted rounded-lg">
              <h4 className="font-medium mb-2">Game Details:</h4>
              <p className="text-sm text-muted-foreground mb-2">
                <strong>Prompt:</strong> {currentSession.prompt}
              </p>
              <p className="text-sm text-muted-foreground">
                <strong>Generated:</strong> {new Date(currentSession.created_at).toLocaleString()}
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
