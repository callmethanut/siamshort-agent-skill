-- 003 — metrics layer: starter views (DRAFT — refine in P5 once real data
-- confirms promoted columns and outcome coverage)

create schema if not exists metrics;

-- Runs joined with tags + outcomes: the main analysis surface.
create or replace view metrics.runs_enriched as
select
  r.env,
  r.id,
  r.created_at,
  r.user_id,
  r.studio_project_id,
  r.source,
  r.kind,
  r.status,
  r.provider,
  r.provider_model,
  r.prompt,
  r.params,
  r.credit_cost,
  t.subject,
  t.medium,
  t.style,
  t.lighting,
  t.camera,
  t.language,
  o.outcome,
  o.signals
from raw.ai_runs r
left join tags.run_tags t using (env, id)
left join tags.run_outcomes o using (env, id);

-- Keeper-rate by model (per env). "Keeper" = outcome 'kept'.
create or replace view metrics.keeper_rate_by_model as
select
  env,
  kind,
  provider,
  provider_model,
  count(*)                                             as runs,
  count(*) filter (where outcome = 'kept')             as kept,
  round(100.0 * count(*) filter (where outcome = 'kept') / nullif(count(*), 0), 1)
                                                       as keeper_pct,
  sum(credit_cost)                                     as credits_spent,
  round(sum(credit_cost) / nullif(count(*) filter (where outcome = 'kept'), 0), 2)
                                                       as credits_per_keeper
from metrics.runs_enriched
group by env, kind, provider, provider_model;

-- Style-tag lift: keeper-rate with vs without a given style tag, per model.
create or replace view metrics.style_tag_lift as
select
  env,
  provider_model,
  s.tag                                                as style_tag,
  count(*)                                             as runs_with_tag,
  round(100.0 * count(*) filter (where outcome = 'kept') / nullif(count(*), 0), 1)
                                                       as keeper_pct_with_tag
from metrics.runs_enriched
cross join lateral unnest(style) as s(tag)
group by env, provider_model, s.tag;

-- Re-roll chains: same user, same source context, rapid successive runs.
-- DRAFT heuristic — refine with real source/context columns in P5.
create or replace view metrics.reroll_candidates as
select
  env,
  user_id,
  studio_project_id,
  kind,
  count(*)          as runs_in_hour,
  min(created_at)   as first_run,
  max(created_at)   as last_run
from raw.ai_runs
group by env, user_id, studio_project_id, kind, date_trunc('hour', created_at)
having count(*) >= 3;
