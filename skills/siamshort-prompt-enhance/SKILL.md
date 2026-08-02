---
name: siamshort-prompt-enhance
description: >-
  Rewrite any image or video generation prompt into the platform's proven best-practice shape — without generating anything. Use when the user asks to "improve / rewrite / fix my prompt", "ช่วยแก้ prompt", "เขียน prompt ให้หน่อย", "ทำไม gen ไม่ตรง", pastes a draft prompt for review, or shows a bad output and asks what to change. Costs zero points; output is a ready-to-paste prompt plus a short why.
---

# Prompt Enhance — rewrite to best practice (no generation)

This skill NEVER generates media unless the user explicitly asks to run the result. Its product is the rewritten prompt.

## Workflow

1. **Understand the intent** — from the draft prompt (any language) and anything attached: target kind (image/video) · what they're doing (create new / edit existing media / swap identity / dialogue clip) · subject type (character, scene, prop, storyboard sheet, multi-ref shot, action beat, continuity shot…) · refs available · model if known. Ask at most ONE clarifying question, only if the rewrite would differ materially.
2. **Pick the matching recipe** from the recipe modules and pour the user's intent into that shape — preserve their creative content exactly; restructure, don't reinterpret.
3. **Apply the laws** (prompt-laws module):
   - refs down to ≤2, each scoped both ways ("use ONLY for X — must NOT control camera/background")
   - strip banned tokens (lens numbers, 4K/8K, octane, masterpiece, grain-as-token, prose duration/fps)
   - one committed lighting sentence with a named physical source
   - purpose statement · field structure · locks/preserve-lists where the shape requires
   - LAW violations the user asked for get flagged, not silently obeyed: 9-panel sheet → propose two sheets; 4-ref composition → propose staged passes; 3.5k-char swap → cut to one delta
4. **Deliver:**
   - the rewritten prompt in a copy-ready block (keep the user's language mix — Thai/EN both fine)
   - 3–5 bullets: what changed and WHICH law/recipe drove it
   - if params matter (ratio, duration, model routing), state them separately — they belong in settings, not prose
5. **Repair mode** — if the user shows a bad OUTPUT: classify the deviation (gen-loop table) → change exactly ONE thing → return the minimally-edited prompt and say which move was applied and why only one.

## Boundaries
- Zero-point operation: no generation, no runs, unless the user says run it.
- Never fabricate refs the user doesn't have; if a recipe needs a ref (start-frame, character sheet), say what to attach and how to make it.
- Respect the user's style/genre choices — laws constrain structure, not creativity.
- If the ask is a full production (whole story/video), route to the matching end-to-end video skill instead.
