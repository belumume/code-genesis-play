
import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Download, X, Play } from 'lucide-react';

interface GeneratedFile {
  name: string;
  path: string;
  content: string;
  type: 'python' | 'markdown' | 'other';
}

interface FileViewerProps {
  file: GeneratedFile | null;
  isOpen: boolean;
  onClose: () => void;
  onDownload: (file: GeneratedFile) => void;
}

export function FileViewer({ file, isOpen, onClose, onDownload }: FileViewerProps) {
  if (!file) return null;

  const isGameFile = file.name === 'game.html' || file.name.endsWith('.html');

  const handlePlayGame = () => {
    const blob = new Blob([file.content], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank');
  };

  const getLanguageFromType = (type: string, fileName: string) => {
    if (fileName.endsWith('.html')) return 'html';
    if (fileName.endsWith('.js')) return 'javascript';
    if (fileName.endsWith('.py')) return 'python';
    if (fileName.endsWith('.md')) return 'markdown';
    if (type === 'python') return 'python';
    if (type === 'markdown') return 'markdown';
    return 'text';
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[80vh] flex flex-col">
        <DialogHeader className="flex-shrink-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <DialogTitle>{file.name}</DialogTitle>
              <Badge variant="secondary">
                {getLanguageFromType(file.type, file.name)}
              </Badge>
              <Badge variant="outline">
                {file.content.split('\n').length} lines
              </Badge>
            </div>
            <div className="flex items-center gap-2">
              {isGameFile && (
                <Button
                  size="sm"
                  onClick={handlePlayGame}
                  className="flex items-center gap-2"
                >
                  <Play className="h-4 w-4" />
                  Play Game
                </Button>
              )}
              <Button
                size="sm"
                variant="outline"
                onClick={() => onDownload(file)}
                className="flex items-center gap-2"
              >
                <Download className="h-4 w-4" />
                Download
              </Button>
              <Button
                size="sm"
                variant="ghost"
                onClick={onClose}
                className="h-6 w-6 p-0"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </DialogHeader>
        
        <div className="flex-1 min-h-0">
          <ScrollArea className="h-full w-full rounded-md border">
            <div className="p-4">
              <pre className="text-sm font-mono whitespace-pre-wrap break-words">
                <code>{file.content}</code>
              </pre>
            </div>
          </ScrollArea>
        </div>
        
        {isGameFile && (
          <div className="flex-shrink-0 p-4 bg-muted rounded-md">
            <p className="text-sm text-muted-foreground">
              💡 This is a playable HTML5 game! Click "Play Game" to open it in a new tab and start playing.
            </p>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
