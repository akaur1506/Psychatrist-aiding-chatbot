What I added

- `sql/add_last_seen_and_index.sql` — ALTER TABLE to add `last_seen` timestamp and an index.
- `sql/cleanup_stale_sessions.sql` — SQL to mark sessions `ended_at = now()` when `last_seen` is older than a threshold.

How to apply

1. Open your Supabase project → SQL Editor.
2. Run `sql/add_last_seen_and_index.sql` to add the column and index.
3. Option A — Manual run: Run `sql/cleanup_stale_sessions.sql` whenever you want to clean up stale sessions.

3. Option B — Scheduled automatic cleanup (recommended):
   - In Supabase, go to "SQL Editor" → "Scheduled" (or use pg_cron if enabled).
   - Create a new scheduled job that runs the `cleanup_stale_sessions.sql` query every 5 minutes (or your chosen cadence).

Notes

- The client code already updates `last_seen` on start/ping/end.
- Tune the interval `'10 minutes'` in the cleanup SQL to your desired inactivity timeout.
- If you prefer a server-side scheduled job and your Supabase plan supports it, use Supabase's scheduler or `pg_cron`.
