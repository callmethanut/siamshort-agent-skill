---
name: storyboard
description: Storyboard prompt generator — renders a form widget, then turns the answers into GPT Images 2.0 prompts for storyboard sheets used as Seedance 2.0 video references. Use when the user types "/storyboard", asks for a storyboard / 絵コンテ / story board prompt, or wants reference boards for video generation. Do NOT trigger for plain image generation (use /gpt-image) or video shot prompts (use /seedance2-0).
---

# Storyboard prompt generator

Turns creator-friendly form answers into one or more GPT Images 2.0 prompts that render a
professional storyboard sheet. The sheet (and optional character sheet) is used as a
reference image set for Seedance 2.0 video generation, so panel artwork must stay clean
and croppable.

## Step 1 — render the form

1. Silently call `mcp__visualize__read_me` with modules `["elicitation"]`.
2. Read `assets/widget.html` (next to this file) and pass its contents verbatim to
   `mcp__visualize__show_widget` (title: `storyboard_prompt_generator_form`).
3. Wait for the submitted payload, which arrives as a message starting with
   `Storyboard details — Title: … · Video format: …`.

## Step 2 — defaults and validation

- `Title` and `Video format` are required. If either is missing from the payload, ask one
  short question before generating. Everything else gets defaults silently.
- Summary blank → invent a story from title + format + mood. Summary present but no
  handling choice → polish and expand it. "Use it exactly as written" → keep wording,
  only split into beats.
- Panel count: default 8; clamp to 4–20.
- Panel shape: default Landscape 16:9. Color: full color unless "B&W sketch look" picked.
- Sheet options: default to panel numbers only if the group was skipped.
- Sheet text language: default English. ("No text" → no captions, no numbers, no title.)
- Characters blank → invent 1–3 named characters and lock their look in the prompt.

## Step 3 — grid math

- panel h/w: landscape 0.5625 · square 1 · portrait 1.778
- `cols = max(2, round(sqrt(N × 4/3 × h/w)))`, `rows = ceil(N / cols)`
- If a col count within ±1 divides N exactly, prefer it (avoid >2 empty cells).
- Examples: 8 landscape → 3×3 · 12 landscape → 3 cols × 4 rows · 9 square → 3×3 ·
  12 portrait → 6 cols × 2 rows.
- Sheet aspect = (cols × panel w) : (rows × panel h). Recommend the /gpt-image (/img)
  size closest to it, largest available (4K-class): landscape-ish → landscape size,
  portrait-ish → portrait, near-square → square.
- N ≥ 13 → split into two sheets ("Sheet 1 of 2 — panels 1–8" / "Sheet 2 of 2 — panels
  9–16"), repeating the style and character blocks verbatim on both so they match.

## Step 4 — write the GPT Images 2.0 prompt (always in English)

Template (one paragraph per block, plain text):

```
Professional {full-color | black-and-white pencil} storyboard sheet{ with a slim title
bar at the top reading "TITLE"}: {N} panels arranged in a {rows}×{cols} grid on a clean
light-gray background, each panel {16:9 | 9:16 | 1:1} with thin dark borders and
generous white margins between panels.{ Small panel numbers (1–N) printed in the margin
at the top-left of each panel, outside the artwork.}{ Beneath each panel a thin caption
strip in small clean {language} text with three short lines: ACTION, CAMERA, DIALOGUE.}

ART STYLE: {style line}. Consistent character designs, color palette and lighting logic
in every panel.

CHARACTERS (identical design in every panel): {Name — age, look, outfit; …}

PANELS:
1. (WIDE establishing) {beat}
2. (MEDIUM) {beat}
…

No watermark, no logo, clean margins, legible text.
```

Style lines:
- Anime — Japanese: `high-quality Japanese TV anime, crisp clean lineart, rich cinematic lighting and color`
- Anime — Pixar-style 3D: `Pixar-style 3D animation look, soft global illumination, expressive stylized faces`
- Live action: `photorealistic live-action film stills, 35mm cinema look, natural lighting`
- Other: expand the user's words into one concrete sentence.

Beat structure by video format (map across N panels, one beat per panel, ≤2 lines each,
concrete visual verbs only):
- Story: hook → setup → development → turn → climax → resolution
- CM / advertising: relatable problem → product reveal → demo/benefit → emotional payoff → product/logo end frame
- Educational / explainer: question → context → steps 1…k → recap
- Information: headline image → key facts → detail → takeaway frame
- Entertainment: setup → escalation → peak gag/moment → button
- Art / expression: motif intro → variations → transformation → final image

Shot grammar: open on a wide establishing shot, vary wide/medium/close/over-the-shoulder/
insert, never the same framing twice in a row, end on the format's closing frame.

Hard rules for video-reference safety:
- All numbers, captions and the title live in the white margins, never inside panel
  artwork — panels must crop clean for Seedance and text must not leak into video.
- Mood and time-of-day continuity must be stated once and respected across beats.

Character sheet selected → output a second, separate prompt:

```
Character reference sheet, {style line}: {for each character} full-body front view and
side view plus a face close-up with two expressions, standing on a neutral light-gray
background, name labels in small clean text. Identical design across all views. No
watermark.
```

## Step 5 — deliver

1. Story beats list (one line per panel) so the user can tweak before generating.
2. The final prompt(s), each in its own copy-ready code block.
3. Recommended /img size + the ready-to-run `/img` command(s).
4. Offer to run /img now. Remind: 1 panel ≈ 1 Seedance shot (~15 s per the Seedance
   continuity skills, so 8 panels ≈ 2 min of footage), and the character sheet feeds
   Seedance directly as a character reference.

Related: /gpt-image (/img) generates the sheets; /seedance2-0 and the ~/.codex Seedance
continuity skills turn panels into shot prompts.
