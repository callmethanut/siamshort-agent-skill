# GitHub Actions — nightly sync setup & usage guide

The nightly pipeline runs entirely on GitHub Actions ("Variant A"): one
scheduled workflow executes the same Python scripts used locally —
ETL sync → LLM tagging → (later) report rendering → commit reports to git.
Local Obsidian just pulls.

```
03:30 BKK  GitHub Actions (.github/workflows/nightly.yml)
             ├─ etl_copy.py      live envs → analytics Supabase (incremental)
             ├─ tag_runs.py      tag new rows (skipped until P4 wired)
             ├─ render_reports.py  → vault/Reports/auto/*.md   (P5)
             └─ git commit+push  reports only, append-only
your PC    git pull  → Obsidian sees new reports
```

## One-time setup

### 1. Create the private repo and push

```bash
cd _agent-skill
git init -b main
git add .
git commit -m "agent-skill-enhancement scaffold"
gh repo create <org>/agent-skill --private --source . --push
```

Must be **private** — the vault and reports contain internal analytics.
Check before the first push: `git status` must NOT list
`supabase/envs/analytics/.env` (it is gitignored; only `.env.example` goes in).

### 2. Add the single secret

All credentials travel as ONE repo secret, `ANALYTICS_ENV_FILE`, whose value
is the entire content of your filled `.env`:

```bash
gh secret set ANALYTICS_ENV_FILE < supabase/envs/analytics/.env
```

The workflow writes it back to `supabase/envs/analytics/.env` at runtime, so
the scripts behave exactly as they do locally (including `SRC_*`
auto-discovery — adding an env later = update local `.env`, re-run the
`gh secret set` command above; no workflow change).

### 3. First full clone — do it LOCALLY, not in Actions

The initial full-history copy can run long; do it from your machine where you
can watch progress (see `supabase/README.md`). The Action then only ever does
small incremental catch-ups. Order:

```bash
SUPABASE_ENV=analytics python3 scripts/etl_copy.py --env dev   # verify counts first
SUPABASE_ENV=analytics python3 scripts/etl_copy.py             # then all envs
```

### 4. Test the workflow manually

GitHub → repo → **Actions** tab → `nightly-sync` → **Run workflow** (the
`workflow_dispatch` button). Watch the logs; a correct run after the first
clone shows small `+N` page counts and "no new reports".

Note: the schedule only activates after the workflow file exists on the
default branch, and GitHub may skip schedules on repos with no activity for
60+ days — a manual run or any push re-enables it.

## Operations

- **Schedule** — `cron: "30 20 * * *"` is UTC (= 03:30 Bangkok). GitHub cron
  has no timezone setting; convert BKK−7 when changing it.
- **Missed nights are harmless** — the watermark in `etl.state` means the next
  run just catches up. Re-runs and overlaps are idempotent; `concurrency`
  in the workflow prevents parallel syncs.
- **Logs / failures** — Actions tab keeps full logs per run; GitHub emails the
  repo owner on workflow failure by default.
- **Tagging step** is `continue-on-error` until P4 wires the LLM key — it
  "fails" quietly and nothing else is affected.
- **Reports** are append-only files in `vault/Reports/auto/` — the bot never
  edits existing notes, so `git pull` on your machine can't conflict with
  hand-written vault notes. Pull before writing new notes locally.
- **Backfills** (new table added, or `--full` re-copy) — run locally, not in
  Actions; the workflow is sized for nightly increments.

## Security notes

- The secret contains **live service keys for all source envs**. Keep repo
  access to owners only; rotate keys if a collaborator leaves or exposure is
  suspected (`gh secret set` again after rotating).
- Analysis via Supabase MCP must keep using the read-only `analyst` role —
  the Actions secret is for the pipeline only.
- The workflow's `GITHUB_TOKEN` has `contents: write` only (report commits);
  it cannot touch other repos.
