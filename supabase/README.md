# _agent-skill/supabase — analytics-project tooling

Own tool folder for the **analytics Supabase project**, mirroring the
conventions of the main `supabase-tools/` (env selector, per-env migrations,
confirm gate) while staying fully independent — these tools mutate ONLY the
analytics project; live envs are read-only ETL sources.

## Layout (mirrors supabase-tools)

```
supabase/
  scripts/    _client.py  migrate.py  deploy_function.py  etl_copy.py  tag_runs.py
  functions/  ← analytics-project edge functions (none yet; self-contained single files)
  envs/
    analytics/  migrations/  .env  ← the one real target (copy .env.example → .env)
  requirements.txt
```

## Rules

1. **`SUPABASE_ENV` is REQUIRED** — no default: `SUPABASE_ENV=analytics python3 scripts/...`
2. `analytics` is the internal sandbox (no `--confirm`). Any env added later
   is a real target and needs `--confirm <env>`.
3. Applied migrations are immutable (tracked in `etl.migrations`) —
   corrections are new forward migrations.
4. **These tools never point at a live platform env.** Live envs appear only
   as `SRC_*` read-only credentials for `etl_copy.py`.
5. Analysis sessions (Supabase MCP) use the read-only `analyst` role from
   migration 004 — never the service key. Only ETL/tagging scripts write.

## Everyday commands

```bash
cd _agent-skill/supabase
pip install -r requirements.txt
cp envs/analytics/.env.example envs/analytics/.env   # fill (owner)

SUPABASE_ENV=analytics python3 scripts/migrate.py --status
SUPABASE_ENV=analytics python3 scripts/migrate.py            # apply schema

SUPABASE_ENV=analytics python3 scripts/etl_copy.py --env dev # first copy
SUPABASE_ENV=analytics python3 scripts/etl_copy.py           # all sources
SUPABASE_ENV=analytics python3 scripts/tag_runs.py --limit 50

SUPABASE_ENV=analytics python3 scripts/deploy_function.py <slug>  # when EFs exist
```

Nightly: `etl_copy.py` then `tag_runs.py` — incremental and idempotent, safe
to re-run or overlap.
