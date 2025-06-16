
-- First, let's check if the tables exist and create them if they don't
-- This is a safe operation that won't affect existing data

-- Create game_sessions table if it doesn't exist
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

-- Create progress_updates table if it doesn't exist
CREATE TABLE IF NOT EXISTS public.progress_updates (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  session_id UUID NOT NULL,
  message TEXT NOT NULL,
  phase TEXT NOT NULL,
  step TEXT NOT NULL,
  progress NUMERIC NOT NULL DEFAULT 0,
  timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  file_content TEXT,
  file_created TEXT
);

-- Add foreign key constraint if it doesn't exist
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

-- Enable RLS if not already enabled
ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.progress_updates ENABLE ROW LEVEL SECURITY;

-- Create RLS policies if they don't exist
DO $$ 
BEGIN
  -- Policies for game_sessions
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'game_sessions' AND policyname = 'Users can view their own game sessions') THEN
    CREATE POLICY "Users can view their own game sessions" 
      ON public.game_sessions 
      FOR SELECT 
      USING (auth.uid() = user_id);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'game_sessions' AND policyname = 'Users can create their own game sessions') THEN
    CREATE POLICY "Users can create their own game sessions" 
      ON public.game_sessions 
      FOR INSERT 
      WITH CHECK (auth.uid() = user_id);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'game_sessions' AND policyname = 'Users can update their own game sessions') THEN
    CREATE POLICY "Users can update their own game sessions" 
      ON public.game_sessions 
      FOR UPDATE 
      USING (auth.uid() = user_id);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'game_sessions' AND policyname = 'Users can delete their own game sessions') THEN
    CREATE POLICY "Users can delete their own game sessions" 
      ON public.game_sessions 
      FOR DELETE 
      USING (auth.uid() = user_id);
  END IF;

  -- Policies for progress_updates
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'progress_updates' AND policyname = 'Users can view progress updates for their sessions') THEN
    CREATE POLICY "Users can view progress updates for their sessions" 
      ON public.progress_updates 
      FOR SELECT 
      USING (
        EXISTS (
          SELECT 1 FROM public.game_sessions 
          WHERE game_sessions.id = progress_updates.session_id 
          AND game_sessions.user_id = auth.uid()
        )
      );
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = 'progress_updates' AND policyname = 'Users can create progress updates for their sessions') THEN
    CREATE POLICY "Users can create progress updates for their sessions" 
      ON public.progress_updates 
      FOR INSERT 
      WITH CHECK (
        EXISTS (
          SELECT 1 FROM public.game_sessions 
          WHERE game_sessions.id = progress_updates.session_id 
          AND game_sessions.user_id = auth.uid()
        )
      );
  END IF;
END $$;
