-- 001 — raw layer + ETL state (analytics project ONLY; never run on live envs)

create schema if not exists raw;
create schema if not exists etl;

-- Watermark bookkeeping per (source env, table)
create table if not exists etl.state (
  env         text        not null,
  table_name  text        not null,
  watermark   timestamptz,
  last_run_at timestamptz,
  rows_copied bigint      not null default 0,
  primary key (env, table_name)
);

-- Mirrored ai_runs. Design: full source row preserved in `row` jsonb
-- (robust to per-env schema drift); hot columns promoted for SQL ergonomics.
-- ETL fills promoted columns best-effort from the row; adjust the list after
-- inspecting real data (TODO P2).
create table if not exists raw.ai_runs (
  env               text        not null,
  id                uuid        not null,
  created_at        timestamptz,
  updated_at        timestamptz,
  user_id           uuid,
  workspace_id      uuid,
  studio_project_id uuid,
  source            text,
  kind              text,
  status            text,
  provider          text,
  provider_model    text,
  prompt            text,
  params            jsonb,
  credit_cost       numeric,
  row               jsonb       not null,
  copied_at         timestamptz not null default now(),
  primary key (env, id)
);

create index if not exists ai_runs_env_created_idx
  on raw.ai_runs (env, created_at);
create index if not exists ai_runs_kind_model_idx
  on raw.ai_runs (kind, provider, provider_model);
create index if not exists ai_runs_user_idx
  on raw.ai_runs (env, user_id);
create index if not exists ai_runs_project_idx
  on raw.ai_runs (env, studio_project_id);

-- Outcome tables (P3): additional raw.* mirrors follow the same pattern —
-- (env, id) PK + promoted columns + full `row` jsonb. Added when the outcome
-- table list is decided; ETL creates nothing implicitly.
