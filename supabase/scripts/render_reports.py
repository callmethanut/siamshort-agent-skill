#!/usr/bin/env python3
"""Render the mechanical nightly report → vault/Reports/auto/YYYY-MM-DD-nightly.md

Append-only: one dated file per day; existing files are never edited. Deep
qualitative analysis lives in hand-written vault/Reports/ notes — this is the
dashboard summary only.

Usage:
    SUPABASE_ENV=analytics python3 scripts/render_reports.py
"""

from __future__ import annotations

from pathlib import Path

from _client import ROOT, analytics_conn


def rows(cur, sql):
    cur.execute(sql)
    return cur.fetchall()


def table(headers, data):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in data:
        out.append("| " + " | ".join("" if v is None else str(v) for v in r) + " |")
    return "\n".join(out) if data else "_no data_"


def main() -> None:
    conn = analytics_conn()
    cur = conn.cursor()

    # Bangkok date from the DB clock so local/CI runs agree
    cur.execute("select (now() at time zone 'Asia/Bangkok')::date")
    today = cur.fetchone()[0].isoformat()

    out_dir = ROOT.parent / "vault" / "Reports" / "auto"
    out_path = out_dir / f"{today}-nightly.md"
    if out_path.exists():
        print(f"{out_path.name} already exists — skipping (append-only)")
        return
    out_dir.mkdir(parents=True, exist_ok=True)

    last24 = rows(cur, """
        select env, count(*),
               count(*) filter (where status='failed'),
               coalesce(round(sum(charge_points)::numeric,0),0)
        from raw.ai_runs
        where created_at > now() - interval '24 hours'
        group by env order by 2 desc""")

    outcomes = rows(cur, """
        select o.outcome, count(*) from tags.run_outcomes o group by 1 order by 2 desc""")

    models7 = rows(cur, """
        with t as (
          select provider_model, kind,
                 coalesce(studio_shot_id::text, canvas_node_id::text,
                          studio_entity_id::text) target,
                 count(*) attempts,
                 count(*) filter (where status='failed') fails,
                 sum(charge_points) pts
          from raw.ai_runs
          where created_at > now() - interval '7 days'
          group by 1,2,3)
        select provider_model, kind, sum(attempts) runs,
               round(100.0*sum(fails)/nullif(sum(attempts),0),1) fail_pct,
               round(avg(attempts) filter (where target is not null),2) att_per_target,
               coalesce(round(sum(pts)::numeric,0),0) points
        from t group by 1,2 having sum(attempts) >= 10
        order by points desc nulls last limit 12""")

    points7 = rows(cur, """
        select env, coalesce(round(sum(charge_points)::numeric,0),0)
        from raw.ai_runs
        where created_at > now() - interval '7 days' and charge_points > 0
        group by env order by 2 desc""")

    md = f"""# Nightly summary — {today}

Auto-generated from the analytics DB. Deep analysis: see hand-written notes in `Reports/`.

## Last 24h — new runs per env

{table(["env", "runs", "failed", "points"], last24) if last24 else "_no new runs in the last 24h_"}

## Outcome distribution (all-time)

{table(["outcome", "runs"], outcomes)}

## Last 7 days — models

{table(["model", "kind", "runs", "fail %", "attempts/target", "points"], models7)}

## Last 7 days — points by env

{table(["env", "points"], points7)}
"""
    out_path.write_text(md, encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
