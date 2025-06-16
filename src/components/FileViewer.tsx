import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { X, Download, Play, ExternalLink } from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { toast } from 'sonner';

interface FileViewerProps {
  file: {
    name: string;
    content: string;
    type: string;
  };
  onClose: () => void;
}

export function FileViewer({ file, onClose }: FileViewerProps) {
  const [showGamePreview, setShowGamePreview] = useState(false);

  const getLanguage = (fileName: string, fileType: string): string => {
    if (fileName.endsWith('.py')) return 'python';
    if (fileName.endsWith('.js')) return 'javascript';
    if (fileName.endsWith('.ts') || fileName.endsWith('.tsx')) return 'typescript';
    if (fileName.endsWith('.html')) return 'html';
    if (fileName.endsWith('.css')) return 'css';
    if (fileName.endsWith('.md')) return 'markdown';
    if (fileName.endsWith('.json')) return 'json';
    return fileType === 'python' ? 'python' : 'text';
  };

  const handleDownload = () => {
    const blob = new Blob([file.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = file.name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success(`Downloaded ${file.name}`);
  };

  const handlePlayGame = () => {
    if (file.name.endsWith('.html')) {
      setShowGamePreview(true);
    }
  };

  const handleOpenInNewTab = () => {
    const blob = new Blob([file.content], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const newWindow = window.open(url, '_blank');
    
    // Clean up the blob URL after a delay
    setTimeout(() => {
      URL.revokeObjectURL(url);
    }, 1000);
    
    toast.success('Game opened in new tab!');
  };

  const isHtmlGame = file.name.endsWith('.html') || file.name === 'game.html';

  return (
    <>
      <Dialog open={true} onOpenChange={onClose}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-hidden flex flex-col">
          <DialogHeader className="flex flex-row items-center justify-between">
            <DialogTitle className="text-xl font-semibold">{file.name}</DialogTitle>
            <div className="flex items-center gap-2">
              {isHtmlGame && (
                <>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handlePlayGame}
                    className="flex items-center gap-2"
                  >
                    <Play className="h-4 w-4" />
                    Preview
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleOpenInNewTab}
                    className="flex items-center gap-2"
                  >
                    <ExternalLink className="h-4 w-4" />
                    New Tab
                  </Button>
                </>
              )}
              <Button
                variant="outline"
                size="sm"
                onClick={handleDownload}
                className="flex items-center gap-2"
              >
                <Download className="h-4 w-4" />
                Download
              </Button>
              <Button
                variant="ghost"
                size="icon"
                onClick={onClose}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </DialogHeader>
          
          <div className="flex-1 overflow-auto">
            <SyntaxHighlighter
              language={getLanguage(file.name, file.type)}
              style={vscDarkPlus}
              showLineNumbers={true}
              wrapLines={true}
              customStyle={{
                margin: 0,
                borderRadius: '0.375rem',
                fontSize: '0.875rem',
              }}
            >
              {file.content}
            </SyntaxHighlighter>
          </div>
        </DialogContent>
      </Dialog>

      {/* Game Preview Modal */}
      {showGamePreview && isHtmlGame && (
        <Dialog open={showGamePreview} onOpenChange={setShowGamePreview}>
          <DialogContent className="max-w-6xl max-h-[90vh] overflow-hidden flex flex-col p-0">
            <DialogHeader className="p-4 border-b">
              <div className="flex items-center justify-between">
                <DialogTitle>Game Preview: {file.name}</DialogTitle>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleOpenInNewTab}
                  >
                    <ExternalLink className="h-4 w-4 mr-2" />
                    Open in New Tab
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setShowGamePreview(false)}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </DialogHeader>
            
            <div className="flex-1 relative bg-gray-100">
              <iframe
                srcDoc={file.content}
                className="w-full h-full border-0"
                title="Game Preview"
                sandbox="allow-scripts allow-same-origin"
                style={{ minHeight: '600px' }}
              />
            </div>
          </DialogContent>
        </Dialog>
      )}
    </>
  );
}
