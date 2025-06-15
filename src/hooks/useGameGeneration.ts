
import { useState, useCallback } from 'react';
import { useApiConfig } from './useApiConfig';
import { supabase } from '@/integrations/supabase/client';
import { toast } from 'sonner';
import type { GeneratedFile, GameGenerationResult, ProgressUpdate } from '@/types/game';

export function useGameGeneration() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [progressLogs, setProgressLogs] = useState<ProgressUpdate[]>([]);
  const [result, setResult] = useState<GameGenerationResult | null>(null);
  const { apiBaseUrl, wsBaseUrl, isLoading: configLoading } = useApiConfig();

  const addProgressLog = useCallback((update: ProgressUpdate) => {
    setProgressLogs(prev => [...prev, update]);
  }, []);

  const clearLogs = useCallback(() => {
    setProgressLogs([]);
    setResult(null);
  }, []);

  const generateGame = useCallback(async (prompt: string) => {
    if (!prompt.trim()) {
      toast.error('Please enter a game prompt');
      return;
    }

    if (configLoading) {
      toast.error('Still loading configuration, please wait...');
      return;
    }

    try {
      setIsGenerating(true);
      clearLogs();
      
      // Create game session in database
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        toast.error('Please sign in to generate games');
        return;
      }

      console.log('Creating game session for user:', user.id);

      // First check if the table exists by trying a simple select
      const { data: testData, error: testError } = await supabase
        .from('game_sessions')
        .select('id')
        .limit(1);
      
      if (testError) {
        console.error('Table access test failed:', testError);
        addProgressLog({
          type: 'error',
          level: 'error',
          message: `❌ Database access error: ${testError.message}. Please check if the database tables are properly set up.`,
          timestamp: new Date().toISOString()
        });
        
        // Fall back to direct API call without database session
        addProgressLog({
          type: 'log',
          level: 'info',
          message: '🔄 Proceeding without database session tracking...',
          timestamp: new Date().toISOString()
        });
        
        await generateGameDirectly(prompt);
        return;
      }

      console.log('Table access test successful');

      const { data: session, error: sessionError } = await supabase
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
        addProgressLog({
          type: 'error',
          level: 'error',
          message: `❌ Failed to create game session: ${sessionError.message}`,
          timestamp: new Date().toISOString()
        });
        
        // Fall back to direct API call
        addProgressLog({
          type: 'log',
          level: 'info',
          message: '🔄 Proceeding without database session tracking...',
          timestamp: new Date().toISOString()
        });
        
        await generateGameDirectly(prompt);
        return;
      }

      console.log('Game session created:', session);

      addProgressLog({
        type: 'log',
        level: 'info',
        message: `🚀 Starting AI Genesis Engine for: "${prompt}"`,
        timestamp: new Date().toISOString()
      });

      addProgressLog({
        type: 'log',
        level: 'info',
        message: '🤖 Initializing multi-agent system (Architect, Engineer, Sentry, Debugger)...',
        timestamp: new Date().toISOString()
      });

      // Connect to WebSocket for real-time updates
      const wsUrl = wsBaseUrl.replace('https://', 'wss://').replace('http://', 'ws://');
      const ws = new WebSocket(`${wsUrl}/ws/generate`);

      ws.onopen = () => {
        console.log('WebSocket connected');
        // Send generation request
        ws.send(JSON.stringify({
          prompt: prompt.trim(),
          session_id: session.id
        }));
      };

      ws.onmessage = (event) => {
        try {
          const update = JSON.parse(event.data);
          
          if (update.type === 'result') {
            // Final result received
            const gameResult: GameGenerationResult = {
              success: update.success,
              projectName: update.project_name,
              projectPath: update.project_path,
              sessionId: update.session_id,
              gameFile: update.game_file,
              debugCycles: update.debug_cycles,
              error: update.error
            };
            
            setResult(gameResult);
            
            if (update.success) {
              addProgressLog({
                type: 'log',
                level: 'success',
                message: '✅ Game generation completed successfully!',
                timestamp: new Date().toISOString()
              });
              
              // Fetch generated files
              fetchGeneratedFiles(update.project_name);
              
              toast.success('Game generated successfully!');
            } else {
              addProgressLog({
                type: 'error',
                level: 'error',
                message: `❌ Generation failed: ${update.error}`,
                timestamp: new Date().toISOString()
              });
              toast.error(`Generation failed: ${update.error}`);
            }
            
            setIsGenerating(false);
            ws.close();
            
          } else if (update.type === 'log') {
            // Progress update
            addProgressLog(update);
          } else if (update.type === 'error') {
            addProgressLog({
              type: 'error',
              level: 'error',
              message: `❌ Error: ${update.message}`,
              timestamp: new Date().toISOString()
            });
            toast.error(`Error: ${update.message}`);
            setIsGenerating(false);
            ws.close();
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        addProgressLog({
          type: 'error',
          level: 'error',
          message: '❌ WebSocket connection error. Falling back to HTTP generation...',
          timestamp: new Date().toISOString()
        });
        
        // Fallback to HTTP API
        fallbackToHttpGeneration(prompt, session.id);
      };

      ws.onclose = () => {
        console.log('WebSocket connection closed');
      };

    } catch (error) {
      console.error('Generation error:', error);
      toast.error(`Generation error: ${error}`);
      setIsGenerating(false);
    }
  }, [apiBaseUrl, wsBaseUrl, configLoading, addProgressLog, clearLogs]);

  const generateGameDirectly = async (prompt: string) => {
    try {
      addProgressLog({
        type: 'log',
        level: 'info',
        message: `🚀 Starting AI Genesis Engine for: "${prompt}"`,
        timestamp: new Date().toISOString()
      });

      addProgressLog({
        type: 'log',
        level: 'info',
        message: '🤖 Initializing multi-agent system (Architect, Engineer, Sentry, Debugger)...',
        timestamp: new Date().toISOString()
      });

      // Connect to WebSocket for real-time updates
      const wsUrl = wsBaseUrl.replace('https://', 'wss://').replace('http://', 'ws://');
      const ws = new WebSocket(`${wsUrl}/ws/generate`);

      ws.onopen = () => {
        console.log('WebSocket connected (direct mode)');
        // Send generation request without session ID
        ws.send(JSON.stringify({
          prompt: prompt.trim()
        }));
      };

      ws.onmessage = (event) => {
        try {
          const update = JSON.parse(event.data);
          
          if (update.type === 'result') {
            // Final result received
            const gameResult: GameGenerationResult = {
              success: update.success,
              projectName: update.project_name,
              projectPath: update.project_path,
              sessionId: update.session_id,
              gameFile: update.game_file,
              debugCycles: update.debug_cycles,
              error: update.error
            };
            
            setResult(gameResult);
            
            if (update.success) {
              addProgressLog({
                type: 'log',
                level: 'success',
                message: '✅ Game generation completed successfully!',
                timestamp: new Date().toISOString()
              });
              
              // Fetch generated files
              fetchGeneratedFiles(update.project_name);
              
              toast.success('Game generated successfully!');
            } else {
              addProgressLog({
                type: 'error',
                level: 'error',
                message: `❌ Generation failed: ${update.error}`,
                timestamp: new Date().toISOString()
              });
              toast.error(`Generation failed: ${update.error}`);
            }
            
            setIsGenerating(false);
            ws.close();
            
          } else if (update.type === 'log') {
            // Progress update
            addProgressLog(update);
          } else if (update.type === 'error') {
            addProgressLog({
              type: 'error',
              level: 'error',
              message: `❌ Error: ${update.message}`,
              timestamp: new Date().toISOString()
            });
            toast.error(`Error: ${update.message}`);
            setIsGenerating(false);
            ws.close();
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        addProgressLog({
          type: 'error',
          level: 'error',
          message: '❌ WebSocket connection error. Falling back to HTTP generation...',
          timestamp: new Date().toISOString()
        });
        
        // Fallback to HTTP API
        fallbackToHttpGeneration(prompt, 'direct');
      };

      ws.onclose = () => {
        console.log('WebSocket connection closed (direct mode)');
      };

    } catch (error) {
      console.error('Direct generation error:', error);
      addProgressLog({
        type: 'error',
        level: 'error',
        message: `❌ Direct generation failed: ${error}`,
        timestamp: new Date().toISOString()
      });
      setIsGenerating(false);
    }
  };

  const fallbackToHttpGeneration = async (prompt: string, sessionId: string) => {
    try {
      addProgressLog({
        type: 'log',
        level: 'info',
        message: '🔄 Using HTTP fallback for generation...',
        timestamp: new Date().toISOString()
      });

      const requestBody: any = {
        prompt: prompt.trim()
      };

      if (sessionId !== 'direct') {
        requestBody.session_id = sessionId;
      }

      const response = await fetch(`${apiBaseUrl}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      
      setResult(result);
      
      if (result.success) {
        addProgressLog({
          type: 'log',
          level: 'success',
          message: '✅ Game generation completed via HTTP!',
          timestamp: new Date().toISOString()
        });
        
        fetchGeneratedFiles(result.project_name);
        toast.success('Game generated successfully!');
      } else {
        addProgressLog({
          type: 'error',
          level: 'error',
          message: `❌ HTTP generation failed: ${result.error}`,
          timestamp: new Date().toISOString()
        });
        toast.error(`Generation failed: ${result.error}`);
      }
      
    } catch (error) {
      console.error('HTTP fallback error:', error);
      addProgressLog({
        type: 'error',
        level: 'error',
        message: `❌ HTTP fallback failed: ${error}`,
        timestamp: new Date().toISOString()
      });
      toast.error(`HTTP generation failed: ${error}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const fetchGeneratedFiles = async (projectName: string) => {
    if (!projectName) return;
    
    try {
      const response = await fetch(`${apiBaseUrl}/api/games/${projectName}/files`);
      if (response.ok) {
        const filesData = await response.json();
        const files: GeneratedFile[] = [];
        
        for (const fileInfo of filesData.files) {
          try {
            const fileResponse = await fetch(`${apiBaseUrl}/api/games/${projectName}/files/${fileInfo.name}`);
            if (fileResponse.ok) {
              const content = await fileResponse.text();
              files.push({
                name: fileInfo.name,
                path: `${projectName}/${fileInfo.name}`,
                content,
                type: fileInfo.name.endsWith('.html') ? 'html' : 
                      fileInfo.name.endsWith('.md') ? 'markdown' : 
                      fileInfo.name.endsWith('.py') ? 'python' : 'other'
              });
            }
          } catch (error) {
            console.error(`Error fetching file ${fileInfo.name}:`, error);
          }
        }
        
        setResult(prev => prev ? { ...prev, files } : null);
      }
    } catch (error) {
      console.error('Error fetching generated files:', error);
    }
  };

  const downloadFile = useCallback((file: GeneratedFile) => {
    const blob = new Blob([file.content], { 
      type: file.type === 'html' ? 'text/html' : 'text/plain' 
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = file.name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    toast.success(`Downloaded ${file.name}`);
  }, []);

  return {
    isGenerating,
    progressLogs,
    result,
    generateGame,
    clearLogs,
    downloadFile,
    addProgressLog
  };
}
