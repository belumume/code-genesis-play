import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { FileViewer } from './FileViewer';
import { Play, Download, FileText, Trophy, Zap } from 'lucide-react';
import { toast } from 'sonner';
import type { GeneratedFile, GameGenerationResult } from '@/types/game';

interface GameResultProps {
  result: GameGenerationResult;
  onDownloadFile: (file: GeneratedFile) => void;
}

export function GameResult({ result, onDownloadFile }: GameResultProps) {
  const [selectedFile, setSelectedFile] = useState<GeneratedFile | null>(null);
  const [fileViewerOpen, setFileViewerOpen] = useState(false);

  const openFileViewer = (file: GeneratedFile) => {
    setSelectedFile(file);
    setFileViewerOpen(true);
  };

  const closeFileViewer = () => {
    setSelectedFile(null);
    setFileViewerOpen(false);
  };

  const playGame = () => {
    // Check if we have a cloud URL first
    if (result.cloudUrl) {
      window.open(result.cloudUrl, '_blank');
      toast.success('Game opened in new tab!');
      return;
    }
    
    // Fallback to local file if available
    const gameFile = result.files?.find(f => f.name === 'game.html' || f.name.endsWith('.html'));
    if (gameFile) {
      const blob = new Blob([gameFile.content], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank');
      toast.success('Game opened in new tab!');
    } else {
      toast.error('Game file not found');
    }
  };

  if (!result.success) {
    return (
      <Card className="border-red-200 bg-red-50/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-red-700">
            <FileText className="h-5 w-5" />
            Generation Failed
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-red-600 mb-4">{result.error}</p>
          <div className="flex items-center gap-2 text-sm text-red-500">
            <Badge variant="destructive">Failed</Badge>
            {result.debugCycles && (
              <span>Debug cycles: {result.debugCycles}</span>
            )}
          </div>
        </CardContent>
      </Card>
    );
  }

  const gameFile = result.files?.find(f => f.name === 'game.html' || f.name.endsWith('.html'));
  const hasPlayableGame = !!result.cloudUrl || !!gameFile;

  return (
    <>
      <Card className="border-green-200 bg-green-50/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-green-700">
            <Trophy className="h-5 w-5" />
            Game Generated Successfully!
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-2 text-sm">
            <Badge variant="default" className="bg-green-600">
              Success
            </Badge>
            {result.debugCycles !== undefined && (
              <Badge variant="outline">
                <Zap className="h-3 w-3 mr-1" />
                {result.debugCycles} debug cycles
              </Badge>
            )}
            <Badge variant="secondary">
              Project: {result.projectName}
            </Badge>
            {result.cloudUrl && (
              <Badge variant="secondary" className="bg-blue-100">
                ☁️ Cloud Hosted
              </Badge>
            )}
          </div>

          {hasPlayableGame && (
            <div className="flex items-center gap-2">
              <Button onClick={playGame} className="flex items-center gap-2">
                <Play className="h-4 w-4" />
                Play Game
              </Button>
              <p className="text-sm text-muted-foreground">
                {result.cloudUrl 
                  ? '🌐 Your game is hosted in the cloud!'
                  : '🎮 Your game is ready to play!'}
              </p>
            </div>
          )}

          {result.cloudUrl && (
            <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm font-medium text-blue-800 mb-1">Permanent Game URL:</p>
              <a 
                href={result.cloudUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-xs font-mono text-blue-600 hover:underline break-all"
              >
                {result.cloudUrl}
              </a>
            </div>
          )}

          {result.files && result.files.length > 0 && (
            <div>
              <h4 className="font-medium mb-2">Generated Files:</h4>
              <div className="grid grid-cols-1 gap-2">
                {result.files.map((file, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-3 border rounded-lg bg-background"
                  >
                    <div className="flex items-center gap-2">
                      <FileText className="h-4 w-4 text-muted-foreground" />
                      <span className="font-mono text-sm">{file.name}</span>
                      <Badge variant="outline" className="text-xs">
                        {file.type}
                      </Badge>
                      {file.name.endsWith('.html') && (
                        <Badge variant="default" className="text-xs bg-blue-600">
                          Playable
                        </Badge>
                      )}
                    </div>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => openFileViewer(file)}
                      >
                        View
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onDownloadFile(file)}
                      >
                        <Download className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      <FileViewer
        file={selectedFile}
        isOpen={fileViewerOpen}
        onClose={closeFileViewer}
        onDownload={onDownloadFile}
      />
    </>
  );
}
