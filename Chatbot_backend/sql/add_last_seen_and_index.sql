-- Add a last_seen column to sessions and index it
ALTER TABLE public.sessions
ADD COLUMN IF NOT EXISTS last_seen timestamptz;

-- Create an index to efficiently find stale sessions
CREATE INDEX IF NOT EXISTS idx_sessions_last_seen ON public.sessions (last_seen);

-- Optional: ensure ended_at is timestamptz if not already
ALTER TABLE public.sessions
ALTER COLUMN ended_at TYPE timestamptz USING ended_at::timestamptz;
