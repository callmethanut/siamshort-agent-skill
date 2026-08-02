---
name: siamshort-module-video-recipes
description: >-
  Full video prompt recipes mined from the accepted-generation corpus (C1–C6 Best-Practices): verbatim winning templates for character/performance shots, swaps, action/physics, continuity series, edits on existing footage, and the technique matrix. Load whenever writing ANY video generation or video-edit prompt.
---

# Video Recipes (full templates — C1–C6)

## C1 — Character shots & performance/identity swap

**Length law:** swap/transfer prompts under ~2,000 chars; 3.5k+ templates perform worst. Template systems must emit short prompts.

**The one-delta V2V template** (identity kept, one thing changed — the corpus's cleanest winner):
```
source: Original "<file>" uploaded as <ref> — <duration>s MP4, <resolution>, ~<fps>fps.
Preserve the real subject(s), face(s), identity, wardrobe, body timing,
performance, framing, lens, camera movement, source speed, and any source
edits EXACTLY.
Change ONLY <the one delta: environment | performer | grade>.
SOURCE LOCK — build on <ref>. KEEP 1:1: subject, …
```
Swap + relight + cleanup = three separate passes, never one prompt.

**Character-swap spec header:**
```
Duration <n>s, ratio <r>. <fps>fps. Format: MP4.
Smart Cuts: OFF — one continuous take, single shot, no cuts, no reverse
angles, no inserts.
[REFERENCES]
Image = CHARACTER LOCK, <WHO — by screen position for multi-person footage:
"THE MAN ON SCREEN-LEFT"> (model sheet; person only, the studio backdrop
does not enter frame): <full identity description>
```
- **Positional targeting** for two-person footage — address performers by screen side.
- **Ref bleed guard** — "person only, backdrop does not enter frame".
- **`KEEP THE ORIGINAL AUDIO TRACK`** as its own loud header for any audio-preserving swap.

**Lip-sync presenter/avatar:** simple scene + identity ref + "smiles warmly, looks directly into the camera, speaks naturally with synchronized lip movements. She says (<lang>): «exact spoken line verbatim»." Locked camera.

**Stylized character shots:** style sentence FIRST ("Vertical anime-cyberpunk fusion, bold ink-line accents…") + `@[cast]` + **body-part focus alternation** (full shot → trembling hands ECU → forearm) — the identity-pressure release valve; stylized worlds hold identity far better than photoreal.

## C2 — Action / physics / destruction (generating from scratch)

**Write the reflex** (+12.5, the top action lift): initial force → material response → debris/dust → **character reaction (recoil / stagger / brace / สะดุ้ง / เซ)** → settle. Weight/momentum words help (+7.9). Energy must come FROM something and DO something — never decorative aura.

**Montage matrix:** single-beat → one-take OK · multi-beat action → ALLOW montage ("montage, multi-shot, don't use one camera angle") — forcing one-take on complex action fails · swap/dialogue → continuous performance, never montage · MV → montage freely.

**Creature/armor anti-slop block:** "Reference image overrides text. Do not redesign anything. No morphing. No extra limbs."

**Witness camera:** position the camera relative to scene elements ("ultra low-angle witness camera behind scattered soldiers") + ONE named move ("slow push forward with slight clockwise orbit").

**Depopulated destruction:** "focuses strictly on the physical damage and mechanical tearing of the empty <thing>… completely vacant, absolutely no people" + a **damage/material detail sheet as ref**.

**Thai camera asides work:** action prose with parenthetical directions "(มุมกล้องหมุนรอบตัว… ค่อยๆซูมไปที่ดวงตา)".

**Composite starter:**
```
[REFS ≤2, scoped ±] identity ref (overrides text; no morphing/extra limbs)
                    + damage sheet OR location plate
[FORMAT]  duration/ratio via params · single-beat? one-take : allow montage
[CAMERA]  witness position + one move · slow-motion on the hero beat
[ACTION]  force → response → debris → REFLEX → settle
[FORBID]  no morphing, no extra limbs (+ no people, if a plate)
```

## C3 — Continuity / extend / series

**Artifacts over adjectives:** attach an extracted last-frame as start-frame, or the prev clip as ref — prose like "same position, same camera" measures NEGATIVE. Use the platform's extract-frame / Mix Stage flow.

**Start-frame shape:** `<frame> = starting frame. Preserve <short list: layout, color tone, lens perspective, key objects> and <NAMED continuity anchors — "Lohit's red shirt continuity", "right-hand bandage">. Generate a <n>-second clip: <ONE beat>.` Anchors = 2–4 named specifics, never "keep everything consistent".

**Series recipe** (chains indefinitely, no refs needed):
```
Continue inside the same <setting>. <this shot's process/story beat with
tactile material words>. <CONSTANTS restated verbatim every shot: framing
rule / wardrobe line / camera style line>
```
- "**Only hands and forearms are visible**" — faceless series are drift-proof.

**Shot-card format block** (per clip): `// SHOT_ID — <intent> (<camera move → beat → emotion>)` + `[format] single-shot · ~<n>s / <ratio> / Smart Cuts: OFF / One continuous take` — add the no-overlay barrage (no subtitle, no text overlay, no logo, no watermark) **when a model bakes in text** (targeted fix, not blanket).

**Technical-pass trick:** "Use <clip> as the ONLY input. Create an occlusion plate / clean matte-style motion guide. This is not a beauty render. This is not a final VFX shot. This is only a technical source plate for the next pass. Preserve exactly: camera movement, frame timing, positions…"

## C6 — Edits on existing footage (background / relight / remove / style)

**Role-blocks beat lock-walls** — never one giant preserve paragraph; named blocks with per-block verbs, ≤3 blocks:
```
SOURCE — Lock the source video exactly. Preserve <performance list>.
  Never redraw or change him.
<DELTA_REF> — Replace ONLY <the one thing> with this <new element>.
  Keep <list of what stays consistent WITHIN the new element>.
<DESIGN_REF> — Use ONLY for the design of <specific element>.
```
- **The delta gets its own keep-list** — preserve within the change, not just around it.
- **Sync added elements to source motion**: "animate the moon so it grows larger IN SYNC WITH the camera zoom" — no independent motion for new elements.
- **Timed element persistence**: "vultures present from 0.01s and remain through the shot" (prevents pop-in/out).
- **Negative-POV constraints**: "no eye POV, no visibility into the driver-side" — ban camera information, not just objects.
- State target lighting concretely; "match the lighting" alone measures negative.

## C4 — Technique matrix (cross-cutting)
- **Slow-motion generously** on hero beats (+16.5 — video's easiest win; slower = fewer physics errors).
- **Locked/static camera whenever identity matters** (+7.1 on swaps). ONE named camera move max in generation; NO camera moves in edits.
- **Time-blocks (0-3s / 3-7s…)** when pacing or music-sync IS the task (+6.1 singing, +6.7 staged edits); elsewhere use as a repair move after a pacing miss.
- **Duration / resolution / fps → parameters, not prose.** In-prose format facts are mega-template bloat (exception: the swap spec header states source-file facts).
- Strip: numeric lens specs (negative in 5/6 video types), audio/SFX descriptions (sound is post), "no music" declarations, 4K/8K tags, handheld tags (documentary genre only).
- Film grain: OK inside a committed style sentence for cinematic dialogue/shots; never as a lone token.
- Lint every prompt: `[INSERT`, `paste …here`, `TODO`, unfilled `{x}` → reject before submit.


## Seedance conventions (adopted 2026-08-02, DRAFT until corpus-validated)

- **Wrappers**: music `(...)` · SFX `<...>` · dialogue `{exact line}` (mark language if foreign: `Says in Japanese: {…}`) · on-screen title `【...】`.
- **Dual-ref subjects**: per subject, head + full-body refs, both labeled: "Subject 1 — facial features reference <<<image_1>>> (head); hair/makeup/costume reference <<<image_2>>> (full-body)".
- **Section order**: Camera → Subject → Space → Audio.
- **Ordered beats, not clock time**: exact second ranges are unreliable — write beats in order; label "Shot 1 / Shot 2" inside one gen when needed. Time-blocks only when music-sync FEEL is the intent.
- **Action degree**: body part + amplitude/speed/intensity ("snaps head left", "pushes hard off the ground"); beats major → minor in story order.
- **Assembly negatives**: when audio/subs are assembled in post (all end-to-end skills): every video prompt includes `no music` + `no subtitles`; never write narration text into the video prompt when a separate narration track exists.
- **Keyframe stills** (start/end/highlight): locate the beat (or mentally simulate subject+camera+environment) and describe ONLY that static moment — pre-loading posture and gaze (start) · finishing pose + aftermath (end) · peak-impact composition (highlight).

## Model reference syntax
| provider/surface | grammar |
|---|---|
| byteplus-seedance-2 (Ark direct) | `[image 1]` `[video 1]` `[audio 1]` by attachment order |
| xskill routes | `@image_file_N` (legacy `【@图片N】`) |
| platform mention layer (idea-board/studio) | `@[name](node:…)` · `@[cast]` · `#[set]` · `$[prop]` — resolved before dispatch |
Techniques are provider-agnostic; only mention style changes. Params source of truth: the Studio platform module / model specs.
