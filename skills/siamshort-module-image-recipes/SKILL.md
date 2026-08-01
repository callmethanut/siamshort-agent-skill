---
name: siamshort-module-image-recipes
description: >-
  Full image prompt recipes mined from the accepted-generation corpus (B1–B6 Best-Practices): verbatim winning templates for character portraits, angle sheets, scene plates, props, storyboard sheets, and multi-ref composition, plus the staging doctrine. Load whenever writing ANY image generation prompt.
---

# Image Recipes (full templates — B1–B6)

## B1 — Character

**Canonical reference portrait** (the identity anchor; use before any shots exist):
```
Reference-style character portrait. A SINGLE subject — the character — centred
in frame on a CLEAN neutral or soft studio background. NEUTRAL pose,
FORWARD-FACING, well-lit with defined facial features. Frame from head to
mid-thigh so the face, build, and wardrobe all read clearly. This image is the
canonical reference that downstream shot/video gens will use to keep identity
stable — clarity matters more than drama.
Character name: <NAME>
Description: <personality + backstory 2-3 sentences — drives expression/posture>
Role: <main/supporting>
Visual rules: <palette / era / material constraints>
```

**Face-only ref scoping** (when re-using an approved face): `@[ref] Controls ONLY: approved face identity, age read, gaze, eye color, brow shape, nose-lip relationship, smile character, cheek and jaw softness, skin tone range, hair color and part.` — feature-by-feature list; nothing else.

**Wardrobe anti-warp block**: `costume fits perfectly on body, well-fitted clothing, proper proportions, no warping, no distortion, fabric drapes naturally on figure, outfit scaled correctly to body size.`

**Multi-angle sheet**: exact grid + numeric angles — `CU 5 angles {left 90, 45}{front 0}{right -45, -90} + FULL-BODY same 5 angles, white background` + `{use attached image as strong reference, 1:1 similarity, photorealistic, live-action}`.

**Identity-drift reset**: `REFERENCE INPUTS: None. Do not attach any image reference. Rebuild the character from written traits only.`

Rules: ONE subject per gen (multi-character lineups fail hard). Thai-mixed prompts = no penalty.

## B2 — Scene / location plate

```
Cinematic environment / establishing shot. DEPOPULATED location — NO people,
NO characters, NO humans, NO figures, NO silhouettes, NO shadows of people in
the frame. Focus only on architecture, props, lighting, weather, and
atmosphere. The shot reads as a clean reference plate that downstream gens
will populate with characters.
Scene name: <NAME>
Description: <location type: interior/exterior — subtype>
             <architecture / materials / props>
             <ONE committed lighting sentence with a named physical source>
```
- Story text with character names is SAFE inside Description — the header wins.
- Relight recipe (existing location): exactly two scoped refs — `@[geo-ref] composition + design` + `@[light-ref] the <grade> + <light quality>` + "The same wide scene relit from X to Y".
- Never: multi-view grids of one location; lettered map keys ("gate (F)") — describe spatial relations in words ("hut right / river left, temple pushed deep into far background").

## B3 — Prop / product

```
Studio product photo of a SINGLE object isolated on a PURE WHITE SEAMLESS
background. Soft, even studio lighting, no harsh shadows. NO people, NO hands,
NO characters in the frame. Clean composition, the object is the only subject
— this is a reference image, not an in-scene capture.
Item name: <NAME>
Description: <material + construction + wear state + function>
Visual rules: <palette / style>
```
- Material + wear words carry realism ("structured indigo-wash denim, visible contrast stitching", "partially crumbled, dusty").
- Fine jewelry: macro framing, expect iteration, lock the winner as an asset immediately.
- Catalog/multi-product: each object cutout-isolated first ("transparent object edges, no floor"), then composed — layout task, not scene.

## B4 — Storyboard sheet

```
PRODUCTION STORYBOARD SHEET — <4|6> panels total, <ratio> film.
Layout: <2x2 | 3x2> grid, thin white borders, small caption under each panel.
Title block top: "SHOT n — <SLUGLINE> (<BEAT NAME>)"  · Subtitle: <Thai title>
STYLE: <one committed sentence: palette + surface + grain>
CHARACTERS: <2-3 line identity block each: age, build, hair, wardrobe, emotion>
  keep designs 100% consistent across all panels, match the reference images
  EXACTLY — same people in every panel.
Panel 1: <one concrete visual beat + camera hint>
Panel 2: … (one beat per panel)
@[cast refs]
```
- LAW: 4–6 panels only (6 in 3×2 = best; 9 = 4% success; 5/7 never). >6 beats → two sheets.
- Photoreal sheets add: "Photorealistic live-action cinematic frames, natural non-plastic skin, subtle film grain, no cartoon no anime" — and still expect iteration (real faces drift).
- Single-panel variant for quick boards: "Cinematic film storyboard frame — a single panel, clean composition: <beat>".
- Never persona-frame ("You are a storyboard artist") — state the artifact.
- **Format beats panel count**: identity TEXT blocks + simple cast mentions succeed (same 4-panel count: 89.5% vs 8.1%); heavy ref-algebra (`@[x] = {y}` role tables) FAILS on sheets. Thai captions/titles mix freely with EN structure.

## B6 — Multi-ref composition (chars + scene + props in one frame)

- LAW: ≤2 refs per pass. Staging doctrine for complex frames:
  `pass 1` scene plate (B2) → `pass 2` char A into plate (char ref + plate, both scoped ±) → `pass 3` char B / prop → `pass 4` edit-polish (lighting match, one delta). Lock each pass output.
- Scoping grammar (both directions): "@[x] อ้างอิงเฉพาะ <role> — ห้ามใช้<what it must not control (มุมกล้อง/ฉากหลัง)>".
- Identity at composition time: reuse the B1 face-scope list + "Preserve her identity with extremely high fidelity. Keep the same face, proportions, hairstyle, skin tone, age, body proportions, posture."
- Two-character emotional scenes: emotion per character replaces pose choreography ("A calm, compassionate; B defensive, wounded; soft morning window light").
- Simple compositions deserve one-line direct verbs ("เอาหัว @[head] มาแปะบน @[body]").
- Text position words are weak — use a composition ref (sheet panel/sketch) when layout is critical.
- Disciplined role-table shape (works at ≤2 refs, ≤6 words per role): `PURPOSE: <one-line goal>. REFERENCE INPUTS @[a] = <role>. @[b] = <role>.`
- Asset transform: "@[a] = target image to transform. Use as the locked subject, <lock-list>…" + exactly ONE delta (e.g. nighttime + sirens on).
- Lint before submit: reject prompts containing `[INSERT`, `paste …here`, `TODO`, unfilled `{placeholders}`.

## Cross-cutting (B5)
- Lighting: name a physical source (best lift: char +23, scene +46); dramatic contrast portraits-only (kills environments); soft/even studio for reference images (wrong on cinematic sheets); golden/warm = safe default.
- Camera: shot-size + angle vocabulary freely; describe lens EFFECTS ("extreme close-up, strong background blur") — NO numeric lens/f-stop specs, NO 4K/8K/octane/masterpiece tokens, no grain-as-token (grain only inside a committed style sentence).
- Anti-plastic = concrete physical evidence in the description (pores, flyaways, fabric wear, asymmetry) — never bolted-on "natural skin" tokens.
- Purpose statement on every artifact. Field structure over prose. One subject per gen.

## Model routing (image)
- `gpt-image-2` — the workhorse for everything incl. sheets and Thai-mixed prompts.
- `byteplus-seedream-5-pro` — strongest on character portraits; WEAK on environments — don't route scene plates to it.
- `gpt-image-2-vip` — measurably worse on sheets than base; no evidence it earns its cost.
