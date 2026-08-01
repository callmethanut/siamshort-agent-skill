#!/usr/bin/env python3
"""LLM tagging batch (P4): tag untagged raw.ai_runs rows with structured axes.

Idempotent: selects rows with no tags.run_tags entry, tags them once, writes
tags.run_tags. Outcome labels are NOT produced here (they are SQL over
platform signals — see TODO P4).

The LLM call is a stub until P4 wires TAGGING_* credentials in .env.

Usage:
    SUPABASE_ENV=analytics python3 scripts/tag_runs.py --limit 50
    SUPABASE_ENV=analytics python3 scripts/tag_runs.py --dry-run
"""

from __future__ import annotations

import argparse
import sys

from psycopg2.extras import Json

from _client import ENV, analytics_conn

TAG_PROMPT = """Analyze this AI image/video generation prompt and return JSON only:
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
{prompt}
---"""


def call_llm(prompt_text: str) -> dict:
    """P4 TODO: implement against the provider in TAGGING_PROVIDER/.env.
    Must return the parsed JSON dict from TAG_PROMPT."""
    raise NotImplementedError(
        "Wire TAGGING_PROVIDER/TAGGING_API_KEY/TAGGING_MODEL in envs/analytics/.env "
        "and implement call_llm() (P4 in TODO.md)."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

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
    tagged = 0
    for env_name, run_id, prompt in rows:
        try:
            result = call_llm(TAG_PROMPT.replace("{prompt}", prompt))
        except NotImplementedError as exc:
            sys.exit(str(exc))
        cur.execute(
            """insert into tags.run_tags
                 (env, id, subject, medium, style, lighting, camera, language,
                  tag_model, raw_llm)
               values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               on conflict (env, id) do nothing""",
            (
                env_name, run_id,
                result.get("subject"), result.get("medium"),
                result.get("style") or [],
                result.get("lighting"), result.get("camera"),
                result.get("language"),
                tag_model, Json(result),
            ),
        )
        conn.commit()
        tagged += 1
    print(f"tagged: {tagged}")


if __name__ == "__main__":
    main()
