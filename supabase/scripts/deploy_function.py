#!/usr/bin/env python3
"""Deploy an Edge Function to the ANALYTICS project via the Management API.

Mirrors supabase-tools/deploy_function.py conventions, simplified:
  • functions/<slug>/index.ts must be SELF-CONTAINED (no `_shared/` imports —
    the platform's inliner and its BOOT_ERROR pitfalls are deliberately not
    replicated here; keep analytics EFs single-file).
  • functions/<slug>/config.json may set {"verify_jwt": false}.
  • Known Management-API quirk: the JSON body endpoint strips the first 4
    characters of the deployed body — 4 newlines are prepended to survive it.

Usage:
    SUPABASE_ENV=analytics python3 scripts/deploy_function.py <function-slug>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from _client import PROJECT_REF, mgmt_get, mgmt_send, require_confirm

ROOT = Path(__file__).resolve().parent.parent
FUNCTIONS_DIR = ROOT / "functions"

_SHARED_IMPORT_RE = re.compile(r'from\s+["\'][^"\']*_shared/[^"\']+["\']')


def read_verify_jwt(fn_dir: Path) -> bool:
    config = fn_dir / "config.json"
    if config.exists():
        try:
            return bool(json.loads(config.read_text(encoding="utf-8")).get("verify_jwt", True))
        except ValueError:
            sys.exit(f"Invalid JSON in {config}")
    return True


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print("Usage: SUPABASE_ENV=analytics python3 scripts/deploy_function.py <slug>")
        return 1
    slug = args[0]
    fn_dir = FUNCTIONS_DIR / slug
    entry = fn_dir / "index.ts"
    if not entry.exists():
        print(f"No index.ts at {entry}", file=sys.stderr)
        return 1

    require_confirm(sys.argv)

    src = entry.read_text(encoding="utf-8")
    if _SHARED_IMPORT_RE.search(src):
        sys.exit(
            f"{slug}/index.ts imports from _shared/ — analytics EFs must be "
            "self-contained (single file). Fold the helper in."
        )

    body = "\n\n\n\n" + src  # survive the 4-char strip quirk
    verify_jwt = read_verify_jwt(fn_dir)

    existing = mgmt_get(f"/projects/{PROJECT_REF}/functions/{slug}")
    if existing.status_code == 200:
        resp = mgmt_send(
            "PATCH",
            f"/projects/{PROJECT_REF}/functions/{slug}",
            {"body": body, "verify_jwt": verify_jwt},
        )
        action = "updated"
    elif existing.status_code == 404:
        resp = mgmt_send(
            "POST",
            f"/projects/{PROJECT_REF}/functions",
            {"slug": slug, "name": slug, "body": body, "verify_jwt": verify_jwt},
        )
        action = "created"
    else:
        print(
            f"Refusing deploy: pre-read for '{slug}' returned HTTP "
            f"{existing.status_code}, expected 200 or 404.",
            file=sys.stderr,
        )
        return 1

    if resp.status_code >= 400:
        print(f"Error {resp.status_code}: {resp.text}", file=sys.stderr)
        return 1
    print(f"Function '{slug}' {action}. (verify_jwt={verify_jwt})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
