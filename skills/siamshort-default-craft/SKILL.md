---
name: siamshort-default-craft
description: >-
  Ambient baseline craft for Studio/Canvas chats when NO primary skill is active: whenever the agent writes or edits any image/video generation prompt in normal conversation, apply the mined prompt laws and recipes silently. Not user-invocable; intended to be loaded by default per surface (requires runtime "default skill" support — see skill.json note).
---

# Default Craft (ambient — active when no primary skill is)

When the conversation involves writing, editing, or repairing ANY generation prompt and no primary skill is running:

1. Apply the prompt-laws module silently (refs ≤2 scoped ±, banned tokens stripped, lighting with a named source, one subject, panel/length laws, targeted negatives only).
2. Pour the request into the matching recipe shape (image-recipes / video-recipes) — restructure, never reinterpret the user's creative intent.
3. Fill missing required slots (framing, lighting, camera policy, style anchor) with concrete inferred choices; mention inferred additions in one short line.
4. If the user's ask violates a LAW (9-panel sheet, 4-ref composition, 3.5k swap prompt), say so in one sentence and offer the compliant alternative.
5. Stay lightweight: no lectures, no restructuring of non-generation conversation, zero extra ceremony. If the user wants the full treatment, suggest `siamshort-prompt-enhance`; a whole production → the matching video skill.

Boundaries: never generate without an explicit ask; platform rules, points confirmation, and moderation always override.
