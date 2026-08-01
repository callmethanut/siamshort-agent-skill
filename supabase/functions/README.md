# functions/ — analytics-project Edge Functions

None yet. When one is needed (e.g. a scheduled tagging trigger):

1. Create `functions/<slug>/index.ts` — **self-contained single file**
   (this project's deployer intentionally has no `_shared/` inliner).
2. Optional `functions/<slug>/config.json` → `{"verify_jwt": false}`.
3. Deploy: `SUPABASE_ENV=analytics python3 scripts/deploy_function.py <slug>`
4. Boot-test after deploy (anon POST → expect 401/405, not BOOT_ERROR).
