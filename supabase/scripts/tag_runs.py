#!/usr/bin/env python3
"""LLM tagging batch (P4): tag untagged raw.ai_runs rows with structured axes.

Idempotent: selects rows with no tags.run_tags entry, tags them once, writes
tags.run_tags. Outcome labels are NOT produced here (they are SQL over
platform signals).

Providers (set in envs/analytics/.env):
  TAGGING_PROVIDER=gemini     TAGGING_MODEL=gemini-2.5-flash
  TAGGING_PROVIDER=anthropic  TAGGING_MODEL=claude-haiku-4-5-20251001
Plus TAGGING_API_KEY. When unconfigured the script exits 0 with a notice so
the nightly workflow stays green.

Usage:
    SUPABASE_ENV=analytics python3 scripts/tag_runs.py --limit 50
    SUPABASE_ENV=analytics python3 scripts/tag_runs.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time

import requests
from psycopg2.extras import Json

from _client import ENV, analytics_conn

TAG_PROMPT = """Analyze this AI image/video generation prompt and return JSON only (no markdown, no explanation):
{
  "subject": "<main subject category: person|animal|landscape|object|scene|abstract|text|other>",
  "medium": "<photorealistic|cinematic|anime|illustration|3d|documentary|other>",
  "style": ["<up to 6 short style/technique tags present in the prompt>"],
  "lighting": "<dominant lighting descriptor or null>",
  "camera": "<camera/lens/framing descriptor or null>",
  "language": "<en|th|mixed>"
}

Prompt:
---
__PROMPT__
---"""

MAX_PROMPT_CHARS = 6000
RETRIES = 4


def _extract_json(text: str) -> dict:
    """Parse the model's reply; tolerate code fences / stray prose."""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fence:
        text = fence.group(1)
    else:
        brace = re.search(r"\{.*\}", text, re.S)
        if brace:
            text = brace.group(0)
    return json.loads(text)


def call_llm(prompt_text: str) -> dict:
    provider = ENV.get("TAGGING_PROVIDER", "").lower()
    api_key = ENV.get("TAGGING_API_KEY", "")
    model = ENV.get("TAGGING_MODEL", "")

    for attempt in range(RETRIES):
        try:
            if provider == "gemini":
                resp = requests.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                    params={"key": api_key},
                    json={
                        "contents": [{"parts": [{"text": prompt_text}]}],
                        "generationConfig": {
                            "temperature": 0,
                            "responseMimeType": "application/json",
                        },
                    },
                    timeout=60,
                )
                resp.raise_for_status()
                text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            elif provider == "anthropic":
                resp = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                    },
                    json={
                        "model": model,
                        "max_tokens": 400,
                        "temperature": 0,
                        "messages": [{"role": "user", "content": prompt_text}],
                    },
                    timeout=60,
                )
                resp.raise_for_status()
                text = resp.json()["content"][0]["text"]
            else:
                sys.exit(f"Unknown TAGGING_PROVIDER: {provider!r} (use gemini|anthropic)")
            return _extract_json(text)
        except (requests.RequestException, KeyError, IndexError,
                json.JSONDecodeError) as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            if attempt == RETRIES - 1:
                raise
            # back off harder on rate limits
            time.sleep((2 ** attempt) * (3 if status == 429 else 1))
    raise RuntimeError("unreachable")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not (ENV.get("TAGGING_PROVIDER") and ENV.get("TAGGING_API_KEY")
            and ENV.get("TAGGING_MODEL")):
        print("tagging not configured (TAGGING_* empty in .env) — skipping.")
        return  # exit 0: keeps the nightly workflow green until P4 is wired

    conn = analytics_conn()
    cur = conn.cursor()

    cur.execute(
        """select r.env, r.id, r.prompt
           from raw.ai_runs r
           left join tags.run_tags t using (env, id)
           where t.id is null
             and r.prompt is not null
             and length(r.prompt) > 0
           order by r.created_at desc
           limit %s""",
        (args.limit,),
    )
    rows = cur.fetchall()
    print(f"untagged rows selected: {len(rows)}")
    if args.dry_run:
        for env_name, run_id, prompt in rows[:10]:
            print(f"  {env_name} {run_id}: {prompt[:80]!r}")
        return

    tag_model = ENV.get("TAGGING_MODEL", "")
    tagged = failed = 0
    for env_name, run_id, prompt in rows:
        try:
            result = call_llm(
                TAG_PROMPT.replace("__PROMPT__", prompt[:MAX_PROMPT_CHARS])
            )
        except Exception as exc:  # noqa: BLE001 — log and keep batch moving
            failed += 1
            print(f"  FAIL {env_name} {run_id}: {type(exc).__name__}: "
                  f"{str(exc).splitlines()[0][:120]}")
            if failed >= 20:
                print("too many failures — aborting batch (will retry next run)")
                break
            continue
        style = result.get("style") or []
        if not isinstance(style, list):
            style = [str(style)]
        cur.execute(
            """insert into tags.run_tags
                 (env, id, subject, medium, style, lighting, camera, language,
                  tag_model, raw_llm)
               values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               on conflict (env, id) do nothing""",
            (
                env_name, run_id,
                result.get("subject"), result.get("medium"),
                [str(s) for s in style][:6],
                result.get("lighting"), result.get("camera"),
                result.get("language"),
                tag_model, Json(result),
            ),
        )
        conn.commit()
        tagged += 1
        if tagged % 50 == 0:
            print(f"  tagged {tagged}/{len(rows)}", flush=True)
    print(f"tagged: {tagged}, failed: {failed}")


if __name__ == "__main__":
    main()
