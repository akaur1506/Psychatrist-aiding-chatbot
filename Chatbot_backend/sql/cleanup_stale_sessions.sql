-- Mark sessions as ended when last_seen is older than the threshold
-- Adjust the interval below to your desired inactivity timeout (e.g. '10 minutes')

UPDATE public.sessions
SET ended_at = now()
WHERE ended_at IS NULL
  AND last_seen < now() - interval '10 minutes';

-- You can run this SQL manually or schedule it to run periodically.
