---
name: siamshort-video-music-video
description: >-
  Complete music-video production, one skill end-to-end: song + artist in → visual story/treatment → section-synced shot list → generate EVERY performance and narrative clip in a loop (including footage-swap passes) until the full MV is finished → assembly manifest. Use for "MV", "music video", "มิวสิควิดีโอ", performance videos, footage-swap MV work.
---

# Music Video — song in, finished MV out

Hard-won laws from the platform's largest workload: every prompt ≤2,000 chars, ONE delta per pass, montage between clips, never within.

## PHASE A — Story & pre-production

1. **Intake:** song (file, length, structure: intro/verse/chorus/bridge/outro) · artist identity refs · direction (performance / narrative / hybrid) · ratio (21:9 or 9:16) · existing footage to swap? · **gate mode**. Confirm.
2. **Write the visual story (treatment):** even a performance MV tells a story — emotional arc mapped to song structure (verse = intimate, chorus = explosive, bridge = the turn), ONE style sentence + palette, 3–5 recurring visual motifs that evolve across sections. **Approval gate on the treatment.**
3. **Shot list synced to the song:** every shot = song section + time range + beat description + type (performance / narrative / b-roll / swap-pass). Time-blocks are ENCOURAGED here — music sync is where they lift. Performance/narrative alternation plans the identity pressure (full shots ↔ body-part close-ups).
4. **Assets:** artist canonical portraits (+ model sheet for swaps) · location plates per motif.
5. **Cost gate** → explicit confirmation. Phase B runs to completion.

## PHASE B — Production loop (gen-loop engine over the shot list)

Per shot by type:
- **performance (new gen):** style sentence FIRST + `@[cast]` + body-part focus alternation + locked camera on identity-critical shots · continuous take within the clip
- **narrative:** start-frame continuity from prior accepted shot + named anchors + ONE beat
- **swap pass (existing footage):** `KEEP THE ORIGINAL AUDIO TRACK` header · source spec facts one line · positional targeting ("the man on SCREEN-LEFT") · character ref scoped "person only — backdrop does not enter frame" · ONE delta (swap OR relight OR environment); chain passes; technical plates when compositing needs them
- generate → verify → inspect (identity, sync feel, motif consistency) → repair by deviation table → accept → next shot
- loop until every section of the song has its accepted clips — the MV is not done until the board covers the full song timeline

## PHASE C — Assembly manifest
Clips mapped to the song timeline · grade/color notes · motif continuity notes · blocked-shot report.

## Non-negotiable
Treatment + shot-list approval before generation · cost confirmation before Phase B · gen-loop discipline · never montage within a performance clip · placeholder lint on every prompt · platform rules override.
