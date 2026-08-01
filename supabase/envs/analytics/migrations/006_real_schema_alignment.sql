-- 006 — align raw mirrors with the REAL live schema (verified against dev
-- PostgREST OpenAPI on 2026-08-01). Guessed names from 001/005 corrected:
--   ai_runs:        user_id → owner_id, params → model_options (+ charge_points, source FKs)
--   studio_projects: name → title (+ genre, status)
--   profiles:       display_name → full_name (+ email, tier_key, language)
--   shots           → studio_shots (real name; project link goes via studio_chapters)
-- New mirrors: studio_shot_assets (keeper signal!), studio_chapters.
-- usage_pricing keys on `key` (ETL maps it into `id`).
-- Safe now: only dev partially copied; the full clone re-runs with --full.

-- metrics views depend on the dropped columns — rebuilt at the end.
drop view if exists metrics.style_tag_lift;
drop view if exists metrics.keeper_rate_by_model;
drop view if exists metrics.reroll_candidates;
drop view if exists metrics.runs_enriched;

-- ai_runs
alter table raw.ai_runs drop column if exists user_id;
alter table raw.ai_runs drop column if exists params;
alter table raw.ai_runs
  add column if not exists owner_id uuid,
  add column if not exists model_options jsonb,
  add column if not exists charge_points numeric,
  add column if not exists studio_shot_id uuid,
  add column if not exists canvas_node_id uuid,
  add column if not exists studio_entity_id uuid;
create index if not exists ai_runs_owner_idx on raw.ai_runs (env, owner_id);

-- studio_projects
alter table raw.studio_projects drop column if exists name;
alter table raw.studio_projects
  add column if not exists title text,
  add column if not exists genre text,
  add column if not exists status text;

-- profiles
alter table raw.profiles drop column if exists display_name;
alter table raw.profiles
  add column if not exists full_name text,
  add column if not exists email text,
  add column if not exists tier_key text,
  add column if not exists language text;

-- shots → studio_shots
drop table if exists raw.shots;
create table if not exists raw.studio_shots (
  env                     text        not null,
  id                      text        not null,
  created_at              timestamptz,
  updated_at              timestamptz,
  chapter_id              text,
  number                  numeric,
  status                  text,
  duration_seconds        numeric,
  aspect_ratio            text,
  selected_video_asset_id text,
  created_by              text,
  row                     jsonb       not null,
  copied_at               timestamptz not null default now(),
  primary key (env, id)
);
create index if not exists studio_shots_chapter_idx
  on raw.studio_shots (env, chapter_id);

-- studio_shot_assets — per-output row incl. `selected` (keeper signal) and
-- ai_run_id (joins outcomes straight onto runs)
create table if not exists raw.studio_shot_assets (
  env          text        not null,
  id           text        not null,
  created_at   timestamptz,
  shot_id      text,
  type         text,
  media_kind   text,
  asset_id     text,
  ai_run_id    text,
  storage_path text,
  selected     boolean,
  removed_at   timestamptz,
  created_by   text,
  row          jsonb       not null,
  copied_at    timestamptz not null default now(),
  primary key (env, id)
);
create index if not exists shot_assets_run_idx
  on raw.studio_shot_assets (env, ai_run_id);
create index if not exists shot_assets_shot_idx
  on raw.studio_shot_assets (env, shot_id);

-- studio_chapters — the shot → project link
create table if not exists raw.studio_chapters (
  env        text        not null,
  id         text        not null,
  created_at timestamptz,
  updated_at timestamptz,
  project_id text,
  number     numeric,
  status     text,
  row        jsonb       not null,
  copied_at  timestamptz not null default now(),
  primary key (env, id)
);
create index if not exists chapters_project_idx
  on raw.studio_chapters (env, project_id);

-- usage_pricing extras
alter table raw.usage_pricing
  add column if not exists created_at timestamptz,
  add column if not exists updated_at timestamptz,
  add column if not exists enabled boolean,
  add column if not exists source text;

-- Rebuild metrics views on the real columns
create or replace view metrics.runs_enriched as
select
  r.env, r.id, r.created_at, r.owner_id, r.studio_project_id,
  r.studio_shot_id, r.canvas_node_id, r.source, r.kind, r.status,
  r.provider, r.provider_model, r.prompt, r.model_options,
  r.credit_cost, r.charge_points,
  t.subject, t.medium, t.style, t.lighting, t.camera, t.language,
  o.outcome, o.signals
from raw.ai_runs r
left join tags.run_tags t using (env, id)
left join tags.run_outcomes o using (env, id);

create or replace view metrics.keeper_rate_by_model as
select
  env, kind, provider, provider_model,
  count(*)                                             as runs,
  count(*) filter (where outcome = 'kept')             as kept,
  round(100.0 * count(*) filter (where outcome = 'kept') / nullif(count(*), 0), 1)
                                                       as keeper_pct,
  sum(charge_points)                                   as points_charged,
  round(sum(charge_points) / nullif(count(*) filter (where outcome = 'kept'), 0), 2)
                                                       as points_per_keeper
from metrics.runs_enriched
group by env, kind, provider, provider_model;

create or replace view metrics.style_tag_lift as
select
  env, provider_model,
  s.tag                                                as style_tag,
  count(*)                                             as runs_with_tag,
  round(100.0 * count(*) filter (where outcome = 'kept') / nullif(count(*), 0), 1)
                                                       as keeper_pct_with_tag
from metrics.runs_enriched
cross join lateral unnest(style) as s(tag)
group by env, provider_model, s.tag;

create or replace view metrics.reroll_candidates as
select
  env, owner_id, studio_project_id, kind,
  count(*)          as runs_in_hour,
  min(created_at)   as first_run,
  max(created_at)   as last_run
from raw.ai_runs
group by env, owner_id, studio_project_id, kind, date_trunc('hour', created_at)
having count(*) >= 3;

do $$
begin
  if exists (select from pg_roles where rolname = 'analyst') then
    grant select on all tables in schema raw to analyst;
    grant select on all tables in schema metrics to analyst;
  end if;
end $$;
