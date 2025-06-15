import React from 'react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Clock, CheckCircle, AlertCircle, XCircle } from 'lucide-react';
import type { ProgressUpdate } from '@/types/game';

interface GameProgressProps {
  logs: ProgressUpdate[];
  isGenerating: boolean;
}

export function GameProgress({ logs, isGenerating }: GameProgressProps) {
  const getIcon = (update: ProgressUpdate) => {
    if (update.type === 'error' || update.level === 'error') {
      return <XCircle className="h-4 w-4 text-red-500" />;
    }
    if (update.level === 'success') {
      return <CheckCircle className="h-4 w-4 text-green-500" />;
    }
    if (update.level === 'warning') {
      return <AlertCircle className="h-4 w-4 text-yellow-500" />;
    }
    return <Clock className="h-4 w-4 text-blue-500" />;
  };

  const getBadgeVariant = (update: ProgressUpdate) => {
    if (update.type === 'error' || update.level === 'error') return 'destructive';
    if (update.level === 'success') return 'default';
    if (update.level === 'warning') return 'secondary';
    return 'outline';
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  if (logs.length === 0 && !isGenerating) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5" />
            Multi-Agent Progress
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Enter a game prompt to see the autonomous AI agents at work!
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="h-5 w-5" />
          Multi-Agent Progress
          {isGenerating && (
            <Badge variant="secondary" className="animate-pulse">
              Generating...
            </Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-96 w-full">
          <div className="space-y-3">
            {logs.map((update, index) => (
              <div
                key={index}
                className="flex items-start gap-3 p-3 rounded-lg border bg-card/50"
              >
                {getIcon(update)}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <Badge variant={getBadgeVariant(update)} className="text-xs">
                      {update.level || update.type}
                    </Badge>
                    <span className="text-xs text-muted-foreground">
                      {formatTime(update.timestamp)}
                    </span>
                  </div>
                  <p className="text-sm leading-relaxed break-words">
                    {update.message}
                  </p>
                  {update.data && (
                    <pre className="mt-2 text-xs bg-muted p-2 rounded overflow-x-auto">
                      {JSON.stringify(update.data, null, 2)}
                    </pre>
                  )}
                </div>
              </div>
            ))}
            {isGenerating && (
              <div className="flex items-start gap-3 p-3 rounded-lg border bg-card/50 animate-pulse">
                <div className="h-4 w-4 bg-blue-500 rounded-full animate-ping" />
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <Badge variant="outline" className="text-xs">
                      AI Working...
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Multi-agent system is processing your request...
                  </p>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
