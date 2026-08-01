# _agent-skill — Agent Skill Enhancement (internal analytics)

Learn from historical image/video generation data to build prompt-suggestion /
self-improve skills. Analysis and validation happen HERE, internally, before
anything ships to the platform.

**Independence rule (hard):** this project never writes to any live Supabase,
never edits app repos, never edits shared n8n. Read-only copies come IN;
reports and validated skills go OUT. Everything lives under this folder plus
one dedicated analytics Supabase project.

Project overview + locked decisions: `siamshort-kms/Projects/agent-skill-enhancement/README.md`

## Layout

```
_agent-skill/
├── README.md            ← this file
├── TODO.md              ← working task breakdown (keep current)
├── .github/workflows/   ← nightly-sync (Actions runs ETL + tagging + reports)
├── docs/                ← github-actions-setup.md (setup & usage guide)
├── supabase/            ← own tool folder for the analytics project
│   │                      (mirrors supabase-tools conventions — see supabase/README.md)
│   ├── scripts/         ← _client.py · migrate.py · deploy_function.py · etl_copy.py · tag_runs.py
│   ├── functions/       ← analytics-project edge functions (none yet)
│   └── envs/analytics/  ← migrations/ + .env (copy .env.example, owner fills)
└── vault/               ← dedicated Obsidian vault (open this folder in Obsidian)
    ├── Home.md
    ├── Reports/         ← analysis write-ups
    ├── Style-Profiles/  ← extracted user/project/model profiles
    ├── Skill-Drafts/    ← draft suggestion/enhance skills under test
    ├── Experiments/     ← validation runs (enhanced vs raw) + verdicts
    └── Queries/         ← reusable SQL saved as notes
```

## Quickstart (after owner creates the analytics Supabase project)

```bash
cd supabase
pip install -r requirements.txt
cp envs/analytics/.env.example envs/analytics/.env      # owner fills credentials

SUPABASE_ENV=analytics python3 scripts/migrate.py       # apply schema (001–004)
SUPABASE_ENV=analytics python3 scripts/etl_copy.py --env dev   # first copy, verify counts
SUPABASE_ENV=analytics python3 scripts/etl_copy.py             # all configured envs
SUPABASE_ENV=analytics python3 scripts/tag_runs.py --limit 50  # tagging (needs LLM key)
```

Nightly schedule: GitHub Actions runs the same scripts (`.github/workflows/
nightly.yml`, 03:30 BKK) — setup guide in `docs/github-actions-setup.md`.
First full clone is always LOCAL; the Action only does small incremental
catch-ups + commits auto-reports to `vault/Reports/auto/` for Obsidian to pull.

## Analysis access

Connect Claude to the analytics project via the Supabase MCP using the
READ-ONLY `analyst` role created by migration `004_analyst_role.sql`
(never the service key). Only ETL/tagging scripts write.
