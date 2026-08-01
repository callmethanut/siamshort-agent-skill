# skills/ — one skill per end-to-end video type

Generated from the mined Best-Practices vault (`../vault/Best-Practices/`, 2026-08-01 corpus baseline). Format matches the agent-service skill registry (`SKILL.md` + `skill.json`, primary skills + module dependencies).

| skill | video type | key data behind it |
|---|---|---|
| `siamshort-module-prompt-laws` | (shared module, loaded by all) | the LAW tier: ref-count, panel-count, length, technique lifts, anti-slop verdicts |
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
`siamshort-module-prompt-laws` must ship together with any of the primary skills (always-load dependency). The referenced platform modules (`siamshort-module-studio-platform`, `-anti-plastic`, `-shot-continuity`, `-storyboard-sheet`, `-physics-guide`) already exist in that registry.

## Maintenance

These skills encode the vault's LAW/RECIPE tier as of 2026-08-01. When a re-mine (per `vault/Best-Practices/E-strategy.md`) changes a law, update `siamshort-module-prompt-laws` FIRST — the per-genre skills only carry workflow + genre recipes, so most data updates touch one file.
