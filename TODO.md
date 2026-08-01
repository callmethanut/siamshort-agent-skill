# TODO — agent-skill-enhancement

Completed items move to `siamshort-kms/Archive/todos/YYYY-MM.md` per workspace rules.

## P0 — Scaffold (2026-08-01)
- [x] KMS project doc (`Projects/agent-skill-enhancement/README.md`)
- [x] Root folder `_agent-skill/` with supabase/ + vault/ + TODO
- [x] Schema drafts (raw / tags / metrics / etl state / analyst role)
- [x] ETL + tagging script skeletons, `.env.example`

## P1 — Analytics Supabase project (owner + agent)
- [x] Owner: create dedicated Supabase project (ref `uueojkdhkkfgstcfsjuf`, ap-southeast-2)
- [x] Fill `.env`: project ref + access token + service key (owner); ANALYST_PASSWORD generated; pooler DB URL set — **owner still to paste DB password** into ANALYTICS_DB_URL
- [ ] Owner: fill SRC_* source env URLs + service keys (7 envs)
- [x] Apply migrations 001–005 (2026-08-01, via Management API)
- [x] `analyst` role verified: SELECT ok, INSERT blocked ("read-only transaction") via pooler `aws-0-ap-southeast-2.pooler.supabase.com`
- [ ] Connect Supabase MCP using the `analyst` role

## P2 — ETL: dev env end-to-end (first clone, LOCAL python) — DONE 2026-08-01
- [x] Verified real schema via dev OpenAPI → migration 006: `studio_shots`/`studio_shot_assets`/`studio_chapters` (not `shots`), ai_runs `owner_id`/`model_options`/`charge_points`, projects `title`, profiles `full_name`, usage_pricing PK `key`; metrics views rebuilt
- [x] Dev cloned; watermark resume + crash-skip resilience proven (main `studio_chapters.number="test"` drift → fragile numeric promotions dropped, values safe in jsonb)

## P3 — First clone all envs + nightly GitHub Actions (Variant A — locked)
- [x] FIRST CLONE COMPLETE all 7 envs (2026-08-01): 16,946 ai_runs (16,419 with prompt) · 204 projects · 164 profiles · 368 shots · 156 shot_assets (118 selected=keeper signals) · usage_pricing 29/env
- [ ] Decide any EXTRA outcome tables (mix-stage refs, canvas node presence, exports) — add to `TABLES` + migration; per-table backfill only
- [x] Two private repos live: `callmethanut/siamshort-agent-skill` (tooling+Actions) + `callmethanut/siamshort-agent-skill-vault` (vault, own repo for Obsidian sync); secrets `ANALYTICS_ENV_FILE` + `VAULT_PUSH_TOKEN` set
- [x] `nightly-sync` manual run GREEN end-to-end (2026-08-01): dual checkout ✓, ETL all 7 envs ✓, tagging graceful-skip ✓, report step ✓; scheduled 03:30 BKK nightly
- [ ] Confirm first *scheduled* run tomorrow morning (Actions tab should show a run ~03:30 BKK)
- [ ] Data-handling note: customer prompts = internal only; no media copied (storage paths only)
- [ ] (dropped: sync-sources Edge Function — superseded by Actions Variant A; n8n explicitly excluded)

## P4 — LLM tagging batch
- [ ] Choose tagging LLM + wire key into `.env` (`TAGGING_*`)
- [ ] Implement `call_llm()` in `tag_runs.py`; tag axes: subject / medium / style[] / lighting / camera / language
- [ ] Outcome labels from platform signals (kept / re-rolled / abandoned) — SQL, not LLM
- [ ] Idempotency check: re-run tags 0 already-tagged rows; spot-check 30 tags by hand

## P5 — Metrics + first report
- [ ] Finalize `metrics.*` views (keeper-rate, cost-per-keeper, re-roll chains) against real columns
- [ ] First analysis report → `vault/Reports/` (per model × ratio × env)
- [ ] Save reusable SQL → `vault/Queries/`

## P6 — Style profiles
- [ ] Extract per-user / per-project / per-model style profiles → `vault/Style-Profiles/` + `tags.style_profiles` table
- [ ] Guard against over-fit: profiles keyed by subject/medium category

## P7 — Suggestion skill drafts
- [ ] Draft enhance-prompt skill(s) → `vault/Skill-Drafts/` (profile + model-spec constraints; Thai→English handling)
- [ ] Review against existing platform prompt conventions (pass-2 EXTEND, anti-plastic, continuity) — read-only reference

## P8 — Validation loop
- [ ] Protocol: raw vs enhanced prompt → real gen on DEV via SiamShort MCP; human verdict
- [ ] Log verdicts back to analytics DB (`tags.experiment_verdicts`)
- [ ] Iterate skills until win-rate target; write evidence report → `vault/Experiments/`
- [ ] Handoff package for owner's n8n/production port (out of scope here)
