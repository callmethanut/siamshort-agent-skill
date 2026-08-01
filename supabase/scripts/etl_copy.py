#!/usr/bin/env python3
"""Nightly ETL: copy generation history from live envs → analytics project.

READ-ONLY against sources (PostgREST GET with service key). Writes only to
the analytics DB. Incremental via per-(env, table) watermark in etl.state;
paginated in pages of 1000 (PostgREST default hard cap — never rely on a
single request returning everything). Idempotent: upsert on (env, id).

Table modes:
  • watermark_col set  → incremental by that timestamp column
  • watermark_col None → small catalog table, fully re-copied every run

Every copied row is stored WHOLE in the `row` jsonb column — promoted columns
are best-effort conveniences; a wrong/missing source column can never lose
data, and re-promoting later is a SQL backfill from `row`, not a re-clone.

Usage:
    SUPABASE_ENV=analytics python3 scripts/etl_copy.py               # all sources, all tables
    SUPABASE_ENV=analytics python3 scripts/etl_copy.py --env dev     # one source env
    SUPABASE_ENV=analytics python3 scripts/etl_copy.py --table ai_runs
    SUPABASE_ENV=analytics python3 scripts/etl_copy.py --full        # ignore watermark
"""

from __future__ import annotations

import argparse
import sys
import time

import requests
from psycopg2.extras import Json, execute_values

from _client import analytics_conn, source_envs

PAGE_SIZE = 1000

# Tables to mirror. Each needs a matching raw.<name> table (see migrations).
# Column names verified against the dev PostgREST OpenAPI (2026-08-01);
# per-env drift is harmless — absent columns land as NULL, `row` keeps all.
# "id_col": source PK column mapped into the mirror's `id` (default "id").
TABLES: dict[str, dict] = {
    "ai_runs": {
        "watermark_col": "created_at",
        "promoted": [
            "id", "created_at", "updated_at", "owner_id", "workspace_id",
            "studio_project_id", "studio_shot_id", "canvas_node_id",
            "studio_entity_id", "source", "kind", "status", "provider",
            "provider_model", "prompt", "model_options", "credit_cost",
            "charge_points",
        ],
        "jsonb_cols": {"model_options"},
    },
    # Context tables — so runs join to project / owner / outcome without
    # ever touching live again.
    "studio_projects": {
        "watermark_col": "created_at",
        "promoted": ["id", "created_at", "updated_at", "title", "owner_id",
                     "workspace_id", "genre", "status"],
        "jsonb_cols": set(),
    },
    "profiles": {
        "watermark_col": "created_at",
        "promoted": ["id", "created_at", "updated_at", "full_name", "email",
                     "tier_key", "language"],
        "jsonb_cols": set(),
    },
    "studio_chapters": {
        "watermark_col": "created_at",
        "promoted": ["id", "created_at", "updated_at", "project_id",
                     "status"],
        "jsonb_cols": set(),
    },
    "studio_shots": {
        "watermark_col": "created_at",
        "promoted": ["id", "created_at", "updated_at", "chapter_id",
                     "status", "aspect_ratio",
                     "selected_video_asset_id", "created_by"],
        "jsonb_cols": set(),
    },
    # Keeper signal: one row per shot output, `selected` + ai_run_id.
    "studio_shot_assets": {
        "watermark_col": "created_at",
        "promoted": ["id", "created_at", "shot_id", "type", "media_kind",
                     "asset_id", "ai_run_id", "storage_path", "selected",
                     "removed_at", "created_by"],
        "jsonb_cols": set(),
    },
    # Small catalog — full refresh each run (no watermark), so cost joins
    # always reflect current per-env pricing. PK is `key`.
    "usage_pricing": {
        "watermark_col": None,
        "id_col": "key",
        "promoted": ["id", "created_at", "updated_at", "provider",
                     "provider_model", "kind", "credit_cost", "audience",
                     "enabled", "source"],
        "jsonb_cols": set(),
    },
}


def fetch_page(src: dict, table: str, order_col: str, id_col: str,
               watermark: str | None, watermark_col: str | None,
               offset: int) -> list[dict]:
    params = {
        "select": "*",
        "order": f"{order_col}.asc,{id_col}.asc" if order_col != id_col
        else f"{id_col}.asc",
        "limit": str(PAGE_SIZE),
        "offset": str(offset),
    }
    if watermark and watermark_col:
        params[watermark_col] = f"gte.{watermark}"
    resp = requests.get(
        f"{src['url']}/rest/v1/{table}",
        params=params,
        headers={
            "apikey": src["key"],
            "Authorization": f"Bearer {src['key']}",
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def upsert_rows(cur, env_name: str, table: str, cfg: dict, rows: list[dict]) -> None:
    promoted = cfg["promoted"]
    jsonb_cols = cfg["jsonb_cols"]
    cols = ["env", *promoted, "row"]
    values = []
    id_col = cfg.get("id_col", "id")
    for row in rows:
        rec = [env_name]
        for col in promoted:
            source_col = id_col if col == "id" else col
            value = row.get(source_col)
            if col == "id" and value is not None:
                value = str(value)  # raw mirrors use text ids (mixed PK types)
            elif col in jsonb_cols and value is not None:
                value = Json(value)
            rec.append(value)
        rec.append(Json(row))
        values.append(tuple(rec))
    updates = ", ".join(
        f"{c} = excluded.{c}" for c in cols if c not in ("env", "id")
    )
    execute_values(
        cur,
        f"insert into raw.{table} ({', '.join(cols)}) values %s "
        f"on conflict (env, id) do update set {updates}, copied_at = now()",
        values,
    )


def copy_table(conn, env_name: str, src: dict, table: str, cfg: dict,
               full: bool) -> int:
    cur = conn.cursor()
    watermark_col = cfg["watermark_col"]
    id_col = cfg.get("id_col", "id")
    order_col = watermark_col or id_col

    watermark = None
    if watermark_col and not full:
        cur.execute(
            "select watermark from etl.state where env=%s and table_name=%s",
            (env_name, table),
        )
        found = cur.fetchone()
        watermark = found[0].isoformat() if found and found[0] else None

    total = 0
    max_seen = watermark
    offset = 0
    while True:
        page = fetch_page(src, table, order_col, id_col, watermark,
                          watermark_col, offset)
        if not page:
            break
        upsert_rows(cur, env_name, table, cfg, page)
        total += len(page)
        if watermark_col:
            last = page[-1].get(watermark_col)
            if last and (max_seen is None or last > max_seen):
                max_seen = last
        conn.commit()
        print(f"  {env_name}/{table}: +{len(page)} (total {total})", flush=True)
        if len(page) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        time.sleep(0.2)  # be gentle with live PostgREST between pages

    cur.execute(
        """insert into etl.state (env, table_name, watermark, last_run_at, rows_copied)
           values (%s, %s, %s, now(), %s)
           on conflict (env, table_name) do update set
             watermark = excluded.watermark,
             last_run_at = now(),
             rows_copied = etl.state.rows_copied + excluded.rows_copied""",
        (env_name, table, max_seen, total),
    )
    conn.commit()
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", help="single source env name (e.g. dev)")
    parser.add_argument("--table", help="single table (default: all)")
    parser.add_argument("--full", action="store_true", help="ignore watermarks")
    args = parser.parse_args()

    sources = source_envs()
    if not sources:
        sys.exit("No SRC_* source credentials filled in envs/analytics/.env")
    if args.env:
        if args.env not in sources:
            sys.exit(f"env '{args.env}' not configured; have: {', '.join(sources)}")
        sources = {args.env: sources[args.env]}

    tables = TABLES
    if args.table:
        if args.table not in TABLES:
            sys.exit(f"table '{args.table}' not configured; have: {', '.join(TABLES)}")
        tables = {args.table: TABLES[args.table]}

    conn = analytics_conn()
    grand_total = 0
    for env_name, src in sources.items():
        for table, cfg in tables.items():
            try:
                grand_total += copy_table(conn, env_name, src, table, cfg, args.full)
            except requests.HTTPError as exc:
                print(f"  {env_name}/{table}: HTTP error {exc} — skipping env/table")
            except Exception as exc:  # noqa: BLE001 — skip table, keep the run alive
                conn.rollback()
                print(f"  {env_name}/{table}: ERROR {type(exc).__name__}: "
                      f"{str(exc).splitlines()[0]} — skipping env/table")
    print(f"done. rows upserted: {grand_total}")


if __name__ == "__main__":
    main()
