---
name: siamshort-video-music-video
description: >-
  End-to-end music video: song/audio + artist refs → visual treatment → shot list synced to song sections → performance clips and swap passes with strict audio preservation → assembly plan. Use for "MV", "music video", "มิวสิควิดีโอ", performance videos, singer content, footage-swap MV work. Encodes the hard-won laws from the platform's largest and most difficult workload (3,837 prompts).
---

# Music Video (song → MV)

The MV corpus's #1 lesson: mega-template prompts fail. Every prompt this skill emits stays under ~2,000 chars and changes exactly ONE thing per pass.

## Workflow

1. **Intake:** song (file/length/structure: intro-verse-chorus-bridge), artist identity refs, treatment direction (performance / narrative / hybrid), ratio (21:9 cinematic or 9:16 social). Confirm.
2. **Treatment:** one style sentence + palette + 3–5 recurring visual motifs. Approval gate.
3. **Shot list synced to song sections:** each shot = section, beat description, performance vs b-roll, duration. Time-blocks are ENCOURAGED here (music sync is the one place they lift: 0-3s intro riff / 3-7s first line…). Approval + cost gate.
4. **Performance clips (new generation):** style sentence + `@[cast]` ref + body-part focus alternation (full shot → hands on strings → close-up) — the identity-pressure release valve. Locked camera on identity-critical shots; montage between shots is fine (MV is the montage-friendly genre).
5. **Swap passes (existing footage):** per pass —
   - `KEEP THE ORIGINAL AUDIO TRACK` as the loud header
   - source spec facts (duration, resolution, fps) one line
   - positional targeting for multi-performer footage ("the man on SCREEN-LEFT…")
   - character ref scoped "person only — backdrop does not enter frame"
   - ONE delta: swap OR relight OR environment — never combined; chain passes
   - technical plates (occlusion/matte guides) when compositing needs them
6. **Review loop:** one clip at a time, verify, attach, human gate.
7. **Assembly plan:** clips mapped to song timeline; color/grade notes for post.

## Craft rules (from prompt-laws)
- Never montage WITHIN a swap/performance clip (continuous take), montage freely BETWEEN clips.
- Placeholder lint before submit: reject any prompt containing "paste", "[INSERT", "TODO".
- Lens numbers, fps-in-prose, no-music declarations: strip them — parameter fields carry format.

## Non-negotiable behavior
- Treatment + shot-list approval before generation; cost confirmation per batch; one generation at a time; never claim success on unverified runs; platform rules override.
