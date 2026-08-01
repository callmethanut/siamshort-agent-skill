-- 002 — tag layer: LLM tagging + outcome labels + experiment verdicts

create schema if not exists tags;

-- One row per tagged run. Written only by tag_runs.py (idempotent).
create table if not exists tags.run_tags (
  env         text        not null,
  id          uuid        not null,
  subject     text,                 -- e.g. "person", "animal", "landscape"
  medium      text,                 -- e.g. "photorealistic", "anime", "3d"
  style       text[]      not null default '{}',  -- e.g. {"cinematic lighting","film grain"}
  lighting    text,
  camera      text,
  language    text,                 -- prompt language: "en" | "th" | "mixed"
  tagged_at   timestamptz not null default now(),
  tag_model   text,                 -- LLM used, for auditability
  raw_llm     jsonb,                -- full LLM response for debugging
  primary key (env, id)
);

-- Outcome labels derived from platform signals via SQL (NOT the LLM).
-- Recomputed by ETL/post-process as outcome tables land in P3.
create table if not exists tags.run_outcomes (
  env          text        not null,
  id           uuid        not null,
  outcome      text,                -- "kept" | "rerolled" | "abandoned" | "failed" | "unknown"
  signals      jsonb,               -- which evidence fired (selected_asset, mix_stage, ...)
  computed_at  timestamptz not null default now(),
  primary key (env, id)
);

-- P6: extracted style profiles (also mirrored as notes in vault/Style-Profiles/)
create table if not exists tags.style_profiles (
  scope       text        not null, -- "user" | "project" | "model" | "workspace"
  scope_key   text        not null, -- e.g. "dev:user:<uuid>", "byteplus-seedance-2"
  category    text        not null, -- subject/medium bucket the profile applies to
  profile     jsonb       not null, -- extracted tags/preferences
  updated_at  timestamptz not null default now(),
  primary key (scope, scope_key, category)
);

-- P8: validation verdicts (enhanced vs raw prompt experiments)
create table if not exists tags.experiment_verdicts (
  experiment_id text        not null,
  variant       text        not null, -- "raw" | "enhanced"
  env           text        not null default 'dev',
  run_ref       text,                -- ai_runs id on DEV (live) for traceability
  prompt        text,
  verdict       text,                -- "win" | "loss" | "tie"
  notes         text,
  created_at    timestamptz not null default now(),
  primary key (experiment_id, variant)
);
