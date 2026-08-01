#!/usr/bin/env python3
"""Apply numbered migrations from envs/<env>/migrations/ via the Management API.

Mirrors supabase-tools/migrate.py conventions: SUPABASE_ENV required, applied
files tracked in etl.migrations (immutable — corrections are new forward
migrations), `analytics` is the no-confirm sandbox.

Usage:
    SUPABASE_ENV=analytics python3 scripts/migrate.py --status
    SUPABASE_ENV=analytics python3 scripts/migrate.py
"""

from __future__ import annotations

import sys

from _client import ENV, MIGRATIONS_DIR, require_confirm, run_sql


def ensure_tracking() -> None:
    run_sql("create schema if not exists etl")
    run_sql(
        """create table if not exists etl.migrations (
               filename text primary key,
               applied_at timestamptz not null default now()
           )"""
    )


def applied_set() -> set[str]:
    rows = run_sql("select filename from etl.migrations")
    return {row["filename"] for row in rows}


def main() -> None:
    if not MIGRATIONS_DIR.exists():
        sys.exit(f"No migrations dir: {MIGRATIONS_DIR}")
    files = sorted(p.name for p in MIGRATIONS_DIR.glob("*.sql"))

    ensure_tracking()
    applied = applied_set()

    if "--status" in sys.argv:
        for name in files:
            print(f"{'applied' if name in applied else 'PENDING':>8}  {name}")
        return

    require_confirm(sys.argv)

    analyst_password = ENV.get("ANALYST_PASSWORD", "")
    for name in files:
        if name in applied:
            continue
        sql = (MIGRATIONS_DIR / name).read_text(encoding="utf-8")
        if "__ANALYST_PASSWORD__" in sql:
            if not analyst_password:
                print(f"skip {name}: ANALYST_PASSWORD not set in .env")
                continue
            sql = sql.replace("__ANALYST_PASSWORD__", analyst_password)
        print(f"applying {name} ...")
        try:
            run_sql(sql)
            run_sql(
                "insert into etl.migrations (filename) values "
                f"('{name}') on conflict do nothing"
            )
        except RuntimeError as exc:
            sys.exit(f"FAILED {name}: {exc}")

    print("done.")


if __name__ == "__main__":
    main()
