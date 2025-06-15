
import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { GameProgress } from './GameProgress';
import { GameResult } from './GameResult';
import { useGameGeneration } from '@/hooks/useGameGeneration';
import { useApiConfig } from '@/hooks/useApiConfig';
import { Sparkles, Zap, Brain, Shield, Wrench } from 'lucide-react';

export function GameGenerator() {
  const [prompt, setPrompt] = useState('');
  const { apiBaseUrl, isLoading: configLoading } = useApiConfig();
  const {
    isGenerating,
    progressLogs,
    result,
    generateGame,
    clearLogs,
    downloadFile
  } = useGameGeneration();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    generateGame(prompt);
  };

  const handleClear = () => {
    clearLogs();
    setPrompt('');
  };

  const examplePrompts = [
    "A space shooter where you dodge asteroids and shoot aliens",
    "A simple platformer where you jump on moving platforms to reach the top",
    "A puzzle game where you match colored blocks to clear them",
    "A racing game where you steer a car to avoid obstacles",
    "A snake game where you eat food and grow longer"
  ];

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold gradient-text mb-2">
          AI Genesis Engine v2.1
        </h1>
        <p className="text-lg text-muted-foreground mb-4">
          Transform single-sentence prompts into complete, playable JavaScript/HTML5 games
        </p>
        
        {/* Multi-Agent System Badges */}
        <div className="flex justify-center items-center gap-2 mb-4">
          <Badge variant="outline" className="flex items-center gap-1">
            <Brain className="h-3 w-3" />
            Architect
          </Badge>
          <Badge variant="outline" className="flex items-center gap-1">
            <Wrench className="h-3 w-3" />
            Engineer
          </Badge>
          <Badge variant="outline" className="flex items-center gap-1">
            <Shield className="h-3 w-3" />
            Sentry
          </Badge>
          <Badge variant="outline" className="flex items-center gap-1">
            <Zap className="h-3 w-3" />
            Debugger
          </Badge>
        </div>

        <div className="flex justify-center items-center gap-4 text-sm text-muted-foreground">
          <span>🤖 Autonomous Multi-Agent System</span>
          <span>•</span>
          <span>🔧 Self-Correcting Architecture</span>
          <span>•</span>
          <span>🎮 Instant Browser Games</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Section */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="h-5 w-5" />
                Game Prompt
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Textarea
                    placeholder="Describe your game idea in a single sentence..."
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    className="min-h-[100px] resize-none"
                    disabled={isGenerating || configLoading}
                  />
                </div>

                <div className="flex gap-2">
                  <Button
                    type="submit"
                    disabled={!prompt.trim() || isGenerating || configLoading}
                    className="flex-1"
                  >
                    {isGenerating ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                        Generating...
                      </>
                    ) : (
                      <>
                        <Sparkles className="h-4 w-4 mr-2" />
                        Generate Game
                      </>
                    )}
                  </Button>
                  
                  {(progressLogs.length > 0 || result) && (
                    <Button
                      type="button"
                      variant="outline"
                      onClick={handleClear}
                      disabled={isGenerating}
                    >
                      Clear
                    </Button>
                  )}
                </div>
              </form>

              {configLoading && (
                <div className="text-center py-4">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary mx-auto mb-2" />
                  <p className="text-sm text-muted-foreground">Loading configuration...</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Example Prompts */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Example Prompts</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {examplePrompts.map((example, index) => (
                  <button
                    key={index}
                    className="w-full text-left p-2 rounded border border-dashed border-muted-foreground/20 hover:border-primary/50 hover:bg-muted/50 transition-colors text-sm"
                    onClick={() => setPrompt(example)}
                    disabled={isGenerating}
                  >
                    {example}
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* API Status */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">System Status</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Backend API</span>
                  <Badge variant={apiBaseUrl ? "default" : "destructive"}>
                    {apiBaseUrl ? "Connected" : "Offline"}
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Multi-Agent System</span>
                  <Badge variant="default">Ready</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Output Format</span>
                  <Badge variant="secondary">JavaScript/HTML5</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Progress and Results Section */}
        <div className="space-y-6">
          <GameProgress logs={progressLogs} isGenerating={isGenerating} />
          
          {result && (
            <GameResult result={result} onDownloadFile={downloadFile} />
          )}
        </div>
      </div>

      <Separator className="my-8" />

      {/* Footer Info */}
      <div className="text-center text-sm text-muted-foreground">
        <p className="mb-2">
          🏆 Built for the $40K AI Showdown • Powered by Claude 4 Opus
        </p>
        <p>
          Autonomous multi-agent system with self-correction and enterprise security
        </p>
      </div>
    </div>
  );
}
