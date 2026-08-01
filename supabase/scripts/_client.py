"""Env selector + Supabase Management API client for the analytics project.

Mirrors the conventions of the main `supabase-tools/` (SUPABASE_ENV required,
per-env envs/<env>/.env + migrations, confirm gate) but is fully independent —
this tooling knows ONLY about the analytics project and read-only sources.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
ENVS_ROOT = ROOT / "envs"

# Env target selector — REQUIRED, no default (mirrors supabase-tools rule).
ENV_NAME = os.getenv("SUPABASE_ENV", "").strip()
if not ENV_NAME:
    available = (
        ", ".join(sorted(p.name for p in ENVS_ROOT.iterdir() if p.is_dir()))
        if ENVS_ROOT.exists()
        else "(none)"
    )
    sys.exit(
        "SUPABASE_ENV is required — no default, on purpose.\n"
        "  e.g.  SUPABASE_ENV=analytics python3 scripts/migrate.py --status\n"
        f"  available envs: {available}"
    )

ENV_DIR = ENVS_ROOT / ENV_NAME
MIGRATIONS_DIR = ENV_DIR / "migrations"
_ENV_FILE = ENV_DIR / ".env"
if not _ENV_FILE.exists():
    sys.exit(f"Env file not found: {_ENV_FILE}  (SUPABASE_ENV={ENV_NAME!r})")


def _load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip()
    return values


ENV = _load_env_file(_ENV_FILE)

PROJECT_REF = ENV.get("SUPABASE_PROJECT_REF", "")
ACCESS_TOKEN = ENV.get("SUPABASE_ACCESS_TOKEN", "")
SUPABASE_URL = ENV.get("SUPABASE_URL", "")
ANALYTICS_DB_URL = ENV.get("ANALYTICS_DB_URL", "")

# Printed on every tool run so the target is never a surprise.
print(
    f"\n  ┌─ Analytics target: {ENV_NAME.upper()}\n"
    f"  └─ project_ref={PROJECT_REF or '?'}  url={SUPABASE_URL or '?'}\n",
    file=sys.stderr,
)

# `analytics` is the internal sandbox (no confirm). Any OTHER env added later
# requires an explicit `--confirm <env>` matching SUPABASE_ENV.
_SAFE_ENVS = {"analytics"}

MGMT_BASE = "https://api.supabase.com/v1"


def require_confirm(argv: list[str]) -> None:
    if ENV_NAME in _SAFE_ENVS:
        return
    if "--confirm" in argv:
        idx = argv.index("--confirm")
        if idx + 1 < len(argv) and argv[idx + 1] == ENV_NAME:
            return
    sys.exit(
        f"Env '{ENV_NAME}' is not a sandbox — re-run with:  --confirm {ENV_NAME}"
    )


def _require(name: str, value: str) -> str:
    if not value:
        sys.exit(f"Missing required env var: {name}. Fill in {_ENV_FILE}.")
    return value


def _mgmt_headers() -> dict[str, str]:
    _require("SUPABASE_PROJECT_REF", PROJECT_REF)
    _require("SUPABASE_ACCESS_TOKEN", ACCESS_TOKEN)
    return {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }


def run_sql(query: str) -> list[dict]:
    """Execute SQL on the analytics DB via the Management API.
    Retries on 429 with backoff (Management-API throttle)."""
    for attempt in range(7):
        resp = requests.post(
            f"{MGMT_BASE}/projects/{PROJECT_REF}/database/query",
            headers=_mgmt_headers(),
            json={"query": query},
            timeout=60,
        )
        if resp.status_code == 429:
            time.sleep(min(2**attempt, 30))
            continue
        if resp.status_code >= 400:
            raise RuntimeError(
                f"SQL error {resp.status_code}: {resp.text}\nQuery: {query[:500]}"
            )
        try:
            return resp.json()
        except ValueError:
            return []
    raise RuntimeError("SQL error 429: throttled after retries")


def mgmt_get(path: str) -> requests.Response:
    return requests.get(f"{MGMT_BASE}{path}", headers=_mgmt_headers(), timeout=60)


def mgmt_send(method: str, path: str, payload: dict) -> requests.Response:
    return requests.request(
        method, f"{MGMT_BASE}{path}", headers=_mgmt_headers(), json=payload, timeout=120
    )


def analytics_conn():
    """Direct Postgres connection for bulk writes (ETL / tagging)."""
    import psycopg2

    url = ANALYTICS_DB_URL
    if not url or "XXXX" in url or "PASSWORD" in url:
        sys.exit(f"ANALYTICS_DB_URL is not filled in {_ENV_FILE}")
    return psycopg2.connect(url)


def source_envs() -> dict[str, dict[str, str]]:
    """Discover SRC_<NAME>_URL / SRC_<NAME>_SERVICE_KEY pairs. name → config."""
    sources: dict[str, dict[str, str]] = {}
    for key, value in ENV.items():
        if key.startswith("SRC_") and key.endswith("_URL") and value:
            name = key[len("SRC_"):-len("_URL")]
            service_key = ENV.get(f"SRC_{name}_SERVICE_KEY", "")
            if service_key:
                sources[name.lower()] = {"url": value.rstrip("/"), "key": service_key}
    return sources
