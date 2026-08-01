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
- [x] `call_llm()` implemented (gemini/anthropic, retries, JSON-robust, graceful skip)
- [x] Outcome labels SQL — `compute_outcomes.py` rebuilds `tags.run_outcomes` nightly (kept 118 / superseded 7,879 / single_success 1,222 / final 1,805 / failed 1,728 / untracked 4,194)
- [ ] DEFERRED (owner): API-key tagging of backlog — analysis proceeding in-chat instead
- [ ] Consider copying minimal `canvas_nodes` for canvas keeper signals (66% of runs are canvas)

## P5 — Metrics + first report — DONE 2026-08-01
- [x] `metrics.*` views rebuilt on real columns (006)
- [x] Deep analysis report → `vault/Reports/2026-08-01-deep-analysis-01.md` (6 findings + 5 skill recommendations)
- [x] `render_reports.py` nightly summary → `vault/Reports/auto/`, wired into workflow with `compute_outcomes.py`

## P6 — Prompt best-practice mining (owner requirement 2026-08-01, supersedes old P6)
Goal 1: best way to write prompts per SUBJECT TYPE (character / scene / prop / …), image + video,
incl. lighting, camera, anti-slop → separate note per type in `vault/Best-Practices/`.
Goal 2: best-practice profile per VIDEO GENRE (vlog/vox, advertise, movie, short-drama, MV …)
+ strategy for continuous self-improvement as prompt data grows.

### A — Corpus preparation (small steps)
- [x] A1. Heuristic subject-type classifier (migration 007, `metrics.prompt_corpus`, 12 types) (SQL regex + entity links): character / scene-location / prop-object / storyboard-sheet / vfx-edit / performance-swap / other → `metrics.prompt_corpus` view
- [x] A2. Spot-checked 60+ samples over 2 iterations (storyboard→image-only, dialogue-performance + shot-with-refs + world-concept added, story-ring/prop fix) (in-chat), fix rules until ~90% right
- [x] A3. Quality cohorts (`metrics.prompt_corpus_good`, 3,069 accepted prompts): kept + converged-final + single_success = "good" vs superseded-early = "draft"
- [x] A4. Hierarchical taxonomy (migration 008): main_cat (generate/edit/transfer/dialogue) → sub_cat + `ops[]` multi-operation flags

### B — Image best-practice notes (one small task each)
- [x] B1. `image-character.md` — DONE 2026-08-01: 3 proven templates (canonical ref portrait / structured fields / angle sheet), 6 rules, anti-warp negatives
- [x] B2. `image-scene.md` — DONE 2026-08-01: DEPOPULATED template (escalating negations + reference-plate purpose), ref-scoped relight recipe, stills-then-animate rule
- [x] B3. `image-prop.md` — DONE 2026-08-01: studio-isolation template v2 (NO hands), material+wear specificity, jewelry warning, b-roll video recipe (camera-first + tactile)
- [ ] B4. `image-storyboard-sheet.md` — panel sheets (the kept-prompt winner shape)
- [ ] B5. `image-techniques.md` — cross-cutting: lighting grammar, camera/lens, composition, anti-slop negatives

### C — Video best-practice notes
- [ ] C1. `video-character-performance.md` — character shots, performance/face swap, identity locks
- [ ] C2. `video-action-vfx.md` — action beats, physics causality, destruction/energy
- [ ] C3. `video-continuity-extend.md` — extend/next-shot, position locks, start-frame refs
- [ ] C4. `video-techniques.md` — timing blocks, camera movement, lighting, audio cues, anti-slop
- [ ] C5. Per-model syntax appendix (seedance `[image N]` vs xskill `@image_file_N`, ratio/duration quirks)

### D — Video genre profiling
- [ ] D1. Genre classifier heuristics (vlog/vox-pop, advertise/commercial, movie/cinematic, short-drama, MV, other) + spot-check
- [ ] D2. Per-genre profile notes → `vault/Best-Practices/genre-*.md` (ratio, duration, pacing, prompt shape, model choice)

### E — Self-improvement strategy & knowledge management
- [ ] E1. `vault/Best-Practices/_strategy.md` — how the loop stays alive: nightly data growth → re-mine triggers (every N new chains / monthly), evidence-linked notes (every claim cites chain/query), versioned updates (append changelog per note, never silent rewrite)
- [ ] E2. Vault management conventions: folder layout, naming, note template with Evidence/Changelog sections
- [ ] E3. Re-mining runbook: repeatable scripts (chain extraction + cohort queries) saved under `vault/Queries/`
- [ ] E4. (later) validation results from P8 feed back into the notes (what worked in practice)

### F — (LATER) Full automation: one prompt → complete video
- [ ] F1. Loop spec per shot: composer (v1 in converged shape) → inspect output → classify deviation → apply ONE playbook move → regen → converged → burst variations (from report 02)
- [ ] F2. Pipeline spec end-to-end: one user prompt → genre profile (D) → story/shot breakdown → per-shot prompts from best-practice notes (B/C) → shot loop (F1) with continuity locks → assemble
- [ ] F3. Prototype as an agent flow on DEV via SiamShort MCP (human gate per shot first, then unattended)
- [ ] F4. Benchmark: attempts/shot + points/shot vs human baseline (4.94 attempts, seedance) — iterate until it wins
- [ ] F5. Handoff package → owner ports to n8n/production

## P7 — Suggestion skill drafts
- [ ] Draft enhance-prompt skill(s) → `vault/Skill-Drafts/` (profile + model-spec constraints; Thai→English handling)
- [ ] Review against existing platform prompt conventions (pass-2 EXTEND, anti-plastic, continuity) — read-only reference

## P8 — Validation loop
- [ ] Protocol: raw vs enhanced prompt → real gen on DEV via SiamShort MCP; human verdict
- [ ] Log verdicts back to analytics DB (`tags.experiment_verdicts`)
- [ ] Iterate skills until win-rate target; write evidence report → `vault/Experiments/`
- [ ] Handoff package for owner's n8n/production port (out of scope here)
