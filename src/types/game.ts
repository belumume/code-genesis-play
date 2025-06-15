

export interface GeneratedFile {
  name: string;
  path: string;
  content: string;
  type: 'html' | 'markdown' | 'other' | 'python';
}

export interface GameGenerationResult {
  success: boolean;
  projectName?: string;
  projectPath?: string;
  sessionId?: string;
  gameFile?: string;
  debugCycles?: number;
  error?: string;
  files?: GeneratedFile[];
}

export interface ProgressUpdate {
  type: 'log' | 'result' | 'error';
  level?: string;
  message: string;
  timestamp: string;
  data?: any;
}

