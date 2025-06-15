
-- Create game_sessions table to store game generation sessions
CREATE TABLE public.game_sessions (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  prompt TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'started',
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  error TEXT,
  game_path TEXT
);

-- Add Row Level Security (RLS) to ensure users can only see their own sessions
ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;

-- Create policy that allows users to SELECT their own sessions
CREATE POLICY "Users can view their own game sessions" 
  ON public.game_sessions 
  FOR SELECT 
  USING (auth.uid() = user_id);

-- Create policy that allows users to INSERT their own sessions
CREATE POLICY "Users can create their own game sessions" 
  ON public.game_sessions 
  FOR INSERT 
  WITH CHECK (auth.uid() = user_id);

-- Create policy that allows users to UPDATE their own sessions
CREATE POLICY "Users can update their own game sessions" 
  ON public.game_sessions 
  FOR UPDATE 
  USING (auth.uid() = user_id);

-- Create policy that allows users to DELETE their own sessions
CREATE POLICY "Users can delete their own game sessions" 
  ON public.game_sessions 
  FOR DELETE 
  USING (auth.uid() = user_id);

-- Create progress_updates table to store real-time progress updates
CREATE TABLE public.progress_updates (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  session_id UUID REFERENCES public.game_sessions(id) ON DELETE CASCADE NOT NULL,
  phase TEXT NOT NULL,
  step TEXT NOT NULL,
  progress DECIMAL NOT NULL DEFAULT 0,
  message TEXT NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  file_created TEXT,
  file_content TEXT
);

-- Add RLS for progress_updates
ALTER TABLE public.progress_updates ENABLE ROW LEVEL SECURITY;

-- Create policy for progress_updates (users can only see updates for their own sessions)
CREATE POLICY "Users can view progress updates for their own sessions" 
  ON public.progress_updates 
  FOR SELECT 
  USING (
    session_id IN (
      SELECT id FROM public.game_sessions WHERE user_id = auth.uid()
    )
  );

-- Create policy for inserting progress updates (system use)
CREATE POLICY "Allow insert progress updates" 
  ON public.progress_updates 
  FOR INSERT 
  WITH CHECK (true);
