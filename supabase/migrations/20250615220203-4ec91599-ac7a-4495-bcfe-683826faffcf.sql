
-- Create the game_sessions table if it doesn't exist
CREATE TABLE IF NOT EXISTS public.game_sessions (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  prompt TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'started',
  error TEXT,
  game_path TEXT
);

-- Create the progress_updates table if it doesn't exist
CREATE TABLE IF NOT EXISTS public.progress_updates (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  session_id UUID NOT NULL,
  phase TEXT NOT NULL,
  step TEXT NOT NULL,
  progress NUMERIC NOT NULL DEFAULT 0,
  message TEXT NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  file_created TEXT,
  file_content TEXT
);

-- Add foreign key constraint for progress_updates (only if it doesn't exist)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.table_constraints 
    WHERE constraint_name = 'progress_updates_session_id_fkey'
  ) THEN
    ALTER TABLE public.progress_updates 
    ADD CONSTRAINT progress_updates_session_id_fkey 
    FOREIGN KEY (session_id) REFERENCES public.game_sessions(id) ON DELETE CASCADE;
  END IF;
END $$;

-- Enable Row Level Security on both tables
ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.progress_updates ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for game_sessions
DROP POLICY IF EXISTS "Users can view their own game sessions" ON public.game_sessions;
CREATE POLICY "Users can view their own game sessions" 
  ON public.game_sessions 
  FOR SELECT 
  USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can create their own game sessions" ON public.game_sessions;
CREATE POLICY "Users can create their own game sessions" 
  ON public.game_sessions 
  FOR INSERT 
  WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update their own game sessions" ON public.game_sessions;
CREATE POLICY "Users can update their own game sessions" 
  ON public.game_sessions 
  FOR UPDATE 
  USING (auth.uid() = user_id);

-- Create RLS policies for progress_updates
DROP POLICY IF EXISTS "Users can view progress for their sessions" ON public.progress_updates;
CREATE POLICY "Users can view progress for their sessions" 
  ON public.progress_updates 
  FOR SELECT 
  USING (
    EXISTS (
      SELECT 1 FROM public.game_sessions 
      WHERE id = progress_updates.session_id 
      AND user_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "System can create progress updates" ON public.progress_updates;
CREATE POLICY "System can create progress updates" 
  ON public.progress_updates 
  FOR INSERT 
  WITH CHECK (true);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_game_sessions_user_id ON public.game_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_game_sessions_created_at ON public.game_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_progress_updates_session_id ON public.progress_updates(session_id);
CREATE INDEX IF NOT EXISTS idx_progress_updates_timestamp ON public.progress_updates(timestamp);
