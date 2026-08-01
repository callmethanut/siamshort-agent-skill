---
name: siamshort-module-prompt-laws
description: >-
  Data-mined prompt laws from 16,946 real SiamShort generations (2026-08 corpus). Loaded by every video-type skill before writing any prompt. Encodes the panel-count law, ref-count law, length law, technique lifts, and anti-slop verdicts with their evidence tiers.
---

# Prompt Laws (mined 2026-08-01, re-mined per E-strategy triggers)

Apply these BEFORE style or creativity. LAW = hard rule; SIGNAL = prefer unless conflict.

## Structure laws
- **Ref-count (LAW):** max 2 references per generation; a 3rd halves success. Complex frames = staged passes of 2 refs (plate → char A → char B → polish), each pass a lockable checkpoint.
- **Storyboard panel-count (LAW):** 4–6 panels, grid stated explicitly (2×2 / 3×2); NEVER 9 (4% success over 292 tries), never 5/7. ≈1 panel per 1.5–3s of intended clip.
- **Transfer/swap length (LAW):** keep swap prompts under ~2,000 chars; 3.5k+ templates perform worst. ONE delta per pass: preserve everything, change exactly one thing; the delta gets its own keep-list.
- **One subject per generation (LAW):** never multi-character lineups or multi-view grids in one image.
- **Ref scoping (SIGNAL, strong):** every ref declares role positively AND negatively — "use ONLY for X; must NOT control Y (camera/background)".

## Technique laws
- **Lighting:** name a physical in-scene source (practical lamp, neon, candle, window) — the single best lift. One committed lighting sentence; dramatic contrast for portraits, never for environments.
- **Camera:** shot-size + angle words freely; slow-motion generously on hero beats (+16.5); locked camera whenever identity matters; ONE named camera move max. NO numeric lens/f-stop specs (negative in every cohort, image and video).
- **Action:** write the reflex — bodies recoil/stagger/brace on impact (+12.5, the top action lift). Energy must come FROM something and DO something. Multi-beat action → allow montage; one-take only for single beats. Never montage on swaps/dialogue.
- **Continuity:** artifacts over adjectives — attach an extracted start-frame or prev clip; name 2–4 specific continuity anchors (red shirt, bandage); re-state series constants one line each; keep faces out of frame when story allows.
- **Timing:** duration/resolution/fps go in parameters, not prose. Time-blocks (0-3s / 3-7s) when pacing or music-sync IS the task, or as a repair move.

## Anti-slop verdicts
- BANNED tokens: 4K/8K/ultra-res, octane/unreal/render-engine, masterpiece/ultra-detailed, numeric lens specs.
- Targeted negatives only, on observed failure: NO hands (props) · NO people/silhouettes/shadows (plates) · no warping/distortion (wardrobe) · no morphing/no extra limbs (creatures) · no subtitle/text/logo/watermark (when overlays appear).
- Realism = concrete physical evidence in the description (materials, wear state, pores, flyaways) — never bolted-on "natural skin texture" tokens.
- State the artifact's PURPOSE ("canonical reference…", "clean reference plate to be populated…", "technical source plate for the next pass") — appears in accepted prompts of every type.

## Genre quick-routes (from D-genre-profiles)
documentary/process → series recipe, hands-only, handheld OK · advertise → product b-roll or presenter lip-sync, 16:9, short prompts · comedy → SHOT cards + 12s holds, fast model · MV → swap laws above, montage OK, KEEP ORIGINAL AUDIO header · horror → stills-first, darkness via edit passes.
