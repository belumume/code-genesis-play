
import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import { Download, FileText } from 'lucide-react';
import type { GeneratedFile } from '@/types/game';

interface FileViewerProps {
  file: GeneratedFile | null;
  isOpen: boolean;
  onClose: () => void;
  onDownload: (file: GeneratedFile) => void;
}

export function FileViewer({ file, isOpen, onClose, onDownload }: FileViewerProps) {
  if (!file) return null;

  const getLanguageFromType = (type: string) => {
    switch (type) {
      case 'html':
        return 'html';
      case 'markdown':
        return 'markdown';
      case 'python':
        return 'python';
      default:
        return 'text';
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[80vh]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            {file.name}
            <Badge variant="outline" className="text-xs">
              {file.type}
            </Badge>
          </DialogTitle>
        </DialogHeader>
        
        <div className="flex-1 overflow-hidden">
          <ScrollArea className="h-[60vh] w-full rounded-md border p-4">
            <pre className="text-sm">
              <code className={`language-${getLanguageFromType(file.type)}`}>
                {file.content}
              </code>
            </pre>
          </ScrollArea>
        </div>
        
        <div className="flex justify-between items-center pt-4">
          <div className="text-sm text-muted-foreground">
            {file.content.length} characters
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={() => onDownload(file)}
              className="flex items-center gap-2"
            >
              <Download className="h-4 w-4" />
              Download
            </Button>
            <Button variant="outline" onClick={onClose}>
              Close
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
