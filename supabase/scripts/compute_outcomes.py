#!/usr/bin/env python3
"""Compute outcome labels for every run → tags.run_outcomes (full rebuild).

Pure SQL over platform signals — no LLM. Taxonomy (first match wins):
  failed          status='failed'
  kept            a selected, non-removed studio_shot_asset points at the run
  discarded       the run's shot asset was explicitly removed
  superseded      an earlier run on a target (shot/node/entity) that was
                  re-rolled — i.e. not the latest run on that target
  final           latest completed run on a multi-attempt target (survived
                  iteration, though no explicit selection signal)
  single_success  the only run on its target, completed (accepted first try)
  untracked       completed but no target link (nothing to infer from)

`signals` records the evidence: target attempts + this run's position.

Usage:
    SUPABASE_ENV=analytics python3 scripts/compute_outcomes.py
"""

from __future__ import annotations

from _client import analytics_conn

SQL = """
begin;
delete from tags.run_outcomes;

insert into tags.run_outcomes (env, id, outcome, signals)
with base as (
  select
    r.env, r.id, r.status, r.created_at,
    coalesce(r.studio_shot_id::text, r.canvas_node_id::text,
             r.studio_entity_id::text) as target,
    exists (select 1 from raw.studio_shot_assets sa
            where sa.env = r.env and sa.ai_run_id = r.id::text
              and sa.selected and sa.removed_at is null)  as kept,
    exists (select 1 from raw.studio_shot_assets sa
            where sa.env = r.env and sa.ai_run_id = r.id::text
              and sa.removed_at is not null)              as discarded
  from raw.ai_runs r
),
ranked as (
  select b.*,
    count(*)     over (partition by env, target)                          as tgt_runs,
    row_number() over (partition by env, target order by created_at desc) as rn_desc
  from base b
  where target is not null
)
select env, id,
  case
    when status = 'failed' then 'failed'
    when kept then 'kept'
    when discarded then 'discarded'
    when rn_desc > 1 then 'superseded'
    when tgt_runs = 1 and status = 'completed' then 'single_success'
    when status = 'completed' then 'final'
    else 'unknown'
  end,
  jsonb_build_object('target_runs', tgt_runs, 'position_from_last', rn_desc)
from ranked
union all
select env, id,
  case when status = 'failed' then 'failed'
       when kept then 'kept'
       when status = 'completed' then 'untracked'
       else 'unknown' end,
  jsonb_build_object('target_runs', 0)
from base where target is null;

commit;
"""


def main() -> None:
    conn = analytics_conn()
    cur = conn.cursor()
    cur.execute(SQL)
    cur.execute(
        "select outcome, count(*) from tags.run_outcomes group by 1 order by 2 desc"
    )
    for outcome, n in cur.fetchall():
        print(f"  {outcome:16} {n}")
    conn.commit()
    print("done.")


if __name__ == "__main__":
    main()
