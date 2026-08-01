---
name: siamshort-video-vox-explainer
description: >-
  End-to-end vox-style narrated explainer video from a single topic: research → script with per-scene VO lines → scene stills (reference plates) → animate per scene → captions/assembly plan, with a cost gate before any point-spending batch. Use for "vox", "explainer", "คลิปอธิบาย", "ทำวิดีโอสรุปเรื่อง", faceless narrated content, newsroom/mixed-media style topic videos.
---

# Vox Explainer (topic → narrated video)

Faceless, narration-driven. The narration script is the spine; every visual serves a VO line.

## Workflow

1. **Intake:** topic + target length (default 60s), ratio (9:16 vertical default, 16:9 optional), language (TH/EN), style key (newsroom / mixed-media / diorama-like collage). Confirm before research.
2. **Research & script:** outline 5–8 beats; write VO narration per beat (one breath-length sentence each, spoken-Thai natural if TH). Show the full script for approval — the script gate is the cheapest edit point.
3. **Scene plan:** one scene per beat: VO line · visual concept · still-vs-motion decision. Prefer stills-first — generate each scene as an image plate, then animate only the scenes that need motion (data: establishing/scene stills succeed 4× more than direct scene video).
4. **Cost gate:** show scene count × image/video points estimate; require explicit confirmation before generating.
5. **Scene plates (images):** DEPOPULATED plate template per scene — no people unless the beat requires a figure; then faceless framing (hands/silhouette/back view — drift-proof). One committed lighting sentence with a named physical source. ≤2 refs per plate.
6. **Animate:** per scene, plate as start-frame + ONE motion beat + one named camera move; slow-motion on emphasis beats. Duration per scene from the script's VO length. No text overlays (captions burn in at assembly).
7. **Review loop:** one scene at a time, verify the run, attach, stop at human gate before next.
8. **Assembly plan:** ordered scene list + VO text + caption text + music note — hand to the user's editor/export flow.

## Craft rules (from prompt-laws)
- Consistent style: repeat the SAME style sentence in every scene prompt (the series-constants rule).
- No lens numbers, no 4K/octane tokens; purpose statement on every plate.
- Numbers/diagrams in-scene beat text overlays — models fail at rendered text; leave data callouts to captions.

## Non-negotiable behavior
- Script approval before any generation; cost confirmation before any batch.
- One video generation at a time; never claim success on unverified runs.
- Platform security, permissions, and point rules override this workflow.
