---
name: siamshort-default-craft
description: >-
  The baseline craft skill: write, enhance, and repair image/video generation prompts using the platform's mined best practices — no automation, no point spend. Use when the user asks to "improve / rewrite / fix my prompt", "ช่วยแก้ prompt", "เขียน prompt ให้หน่อย", "ทำไม gen ไม่ตรง", pastes a draft prompt, or shows a bad output. Also designed to load by DEFAULT when no other skill is active, so ordinary gen conversations silently apply the same craft.
---

# Default Craft — write & enhance prompts (the overall-knowledge skill)

Two modes, same knowledge. Never generates media unless the user explicitly asks to run the result.

## Mode 1 — Ambient (active as the default, no skill invoked)

Whenever the conversation requires writing or editing ANY generation prompt:
- apply the prompt-laws silently (refs ≤2 scoped ±, banned tokens stripped, one named-source lighting sentence, one subject, panel/length laws, targeted negatives only)
- pour the request into the matching recipe shape; fill missing slots (framing, lighting, camera policy, style anchor) with concrete inferred choices and mention inferred additions in one short line
- if the ask violates a LAW (9-panel sheet, 4-ref composition, 3.5k swap prompt), say so in one sentence and offer the compliant alternative
- stay lightweight: no lectures, no ceremony, don't touch non-generation conversation

## Mode 2 — Invoked ("improve my prompt" / draft pasted / bad output shown)

1. **Understand the intent** — kind (image/video) · doing what (create / edit existing / swap / dialogue) · subject type · refs available · model if known. At most ONE clarifying question, only if the rewrite would differ materially.
2. **Pick the matching recipe** and pour the user's content into that shape — preserve creative intent exactly; restructure, don't reinterpret.
3. **Apply the laws** — scoping, stripping, locks/preserve-lists, purpose statement, field structure; flag LAW violations with the compliant alternative.
4. **Completeness pass** — every required slot filled; missing ones inferred from intent/genre and marked as inferred so the user can veto:
   - image: ONE subject · framing (shot size + angle in words) · lighting (one sentence, named physical source, matched to type) · style anchor · purpose statement · scoped refs · targeted negatives for the type's known failure
   - video: all of the above + ONE action beat (reflex if force) · ONE named camera move or locked camera for identity · slow-motion decision · continuity anchors when following a shot · montage/one-take per the matrix
   - fill with concrete choices ("lit by the flickering fluorescent tube above the workbench"), never generic quality words
5. **Deliver** — copy-ready prompt (keep the user's Thai/EN mix) + 3–5 bullets (what changed, which law) + params stated separately (ratio/duration/model belong in settings, not prose).
6. **Repair mode** — bad output shown: classify the deviation (gen-loop table) → change exactly ONE thing → return the minimal edit and name the move.

## Boundaries
- Zero-point: no generation or runs unless the user says run it (then platform confirmation rules apply).
- Never fabricate refs; if the recipe needs one (start-frame, character sheet), say what to attach and how to create it.
- Laws constrain structure, never the user's creative/style choices.
- A whole-story production ask → route to the matching end-to-end video skill (vox-explainer, advertise, documentary, comedy-short, music-video).
