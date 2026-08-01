-- 005 — raw mirrors for context tables (projects, owners, shots, pricing)
-- so the first clone captures enough to join runs → project → owner → outcome
-- without ever re-reading live. Same pattern as raw.ai_runs: (env, id) PK,
-- best-effort promoted columns, FULL source row in `row` jsonb (nothing is
-- ever lost even if promoted names don't match a source env's schema).
-- Ids are text (source PK types vary across tables).

create table if not exists raw.studio_projects (
  env          text        not null,
  id           text        not null,
  created_at   timestamptz,
  updated_at   timestamptz,
  name         text,
  owner_id     text,
  workspace_id text,
  row          jsonb       not null,
  copied_at    timestamptz not null default now(),
  primary key (env, id)
);
create index if not exists studio_projects_owner_idx
  on raw.studio_projects (env, owner_id);

create table if not exists raw.profiles (
  env          text        not null,
  id           text        not null,
  created_at   timestamptz,
  updated_at   timestamptz,
  display_name text,
  row          jsonb       not null,
  copied_at    timestamptz not null default now(),
  primary key (env, id)
);

create table if not exists raw.shots (
  env               text        not null,
  id                text        not null,
  created_at        timestamptz,
  updated_at        timestamptz,
  studio_project_id text,
  chapter_id        text,
  selected_asset_id text,
  row               jsonb       not null,
  copied_at         timestamptz not null default now(),
  primary key (env, id)
);
create index if not exists shots_project_idx
  on raw.shots (env, studio_project_id);

create table if not exists raw.usage_pricing (
  env            text        not null,
  id             text        not null,
  provider       text,
  provider_model text,
  kind           text,
  credit_cost    numeric,
  audience       text,
  row            jsonb       not null,
  copied_at      timestamptz not null default now(),
  primary key (env, id)
);

-- Grant only if the analyst role already exists (004 may still be pending —
-- its default privileges cover these tables once it runs).
do $$
begin
  if exists (select from pg_roles where rolname = 'analyst') then
    grant usage on schema raw to analyst;
    grant select on all tables in schema raw to analyst;
  end if;
end $$;
