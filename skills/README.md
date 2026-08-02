# skills/ — one skill = one complete video production, end to end

Two tiers: **`siamshort-default-craft`** = the overall-knowledge skill (write/enhance/repair prompts, invocable now, default-loadout when runtime supports it) · **`siamshort-video-*`** = one automation skill per video style profile. Each video PRIMARY runs the full pipeline: **PHASE A** write the story → storyboard → assets → cost gate · **PHASE B** the gen-loop engine generates EVERY shot (compose → generate → inspect → one-move repair → accept → carry continuity → next) until the whole story's board is DONE · **PHASE C** assembly manifest. Gate mode `review-each` or `auto-run` chosen at intake.

Generated from the mined Best-Practices vault (`../vault/Best-Practices/`, 2026-08-01 corpus baseline). Format matches the agent-service skill registry (`SKILL.md` + `skill.json`, primary skills + module dependencies).

| skill | video type | key data behind it |
|---|---|---|
| `siamshort-module-prompt-laws` | shared module (always) | the LAW tier: ref-count, panel-count, length, technique lifts, anti-slop verdicts |
| `siamshort-module-image-recipes` | shared module (conditional) | FULL image templates from B1–B6: portraits, sheets, plates, props, multi-ref staging, model routing |
| `siamshort-module-video-recipes` | shared module (always) | FULL video templates from C1–C6: one-delta V2V, swap headers, action composite, series recipe, role-blocks, technique matrix, ref-syntax |
| `siamshort-module-gen-loop` | shared module (always) | the Phase-B loop engine: deviation→repair-move table (from 905 mined chains), failure branch, gate policy, progress board, resume rules |
| `siamshort-default-craft` | **tier 0/1: write · enhance · repair any prompt** (no automation, zero points); designed to also load as the per-surface DEFAULT when no skill is active | all laws + recipes via modules; repair mode = gen-loop deviation table |
| `siamshort-video-vox-explainer` | topic → narrated explainer (vox style) | stills-first (scene stills 4× video success), faceless framing, script gate |
| `siamshort-video-advertise` | product/brand commercial | best-genre recipes (26.7%): studio isolation, b-roll eruption beat, lip-sync presenter |
| `siamshort-video-documentary` | process/industrial series | best series recipe (29.7%): restated constants, hands-only, handheld |
| `siamshort-video-comedy-short` | gag shorts | best genre (43.9%): SHOT cards, 12s punchline holds, storyboard-driven |
| `siamshort-video-music-video` | song → MV | hardest workload's laws: ≤2k prompts, ONE delta/pass, positional targeting, KEEP AUDIO |

Not duplicated here: **short-drama/movie** — already covered by the existing `siamshort-b2b-auto-movie`; the `prompt-laws` module is designed so that skill can add it as a dependency and inherit the same laws.

## Deploy

Copy the folders into the agent-service workspace registry:
```
agent-service-vercel/workspace/.claude/skills/<name>/
```
All four shared modules (`prompt-laws`, `image-recipes`, `video-recipes`, `gen-loop`) must ship together with any primary skill. The referenced platform modules (`siamshort-module-studio-platform`, `-anti-plastic`, `-shot-continuity`, `-storyboard-sheet`, `-physics-guide`) already exist in that registry.

## Maintenance

These skills encode the vault's LAW/RECIPE tier as of 2026-08-01. When a re-mine (per `vault/Best-Practices/E-strategy.md`) changes a law, update `siamshort-module-prompt-laws` FIRST — the per-genre skills only carry workflow + genre recipes, so most data updates touch one file.
