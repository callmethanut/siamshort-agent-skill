---
name: fable-auto-director
description: >
  Auto-Director Mode — turn ONE line of story idea into a COMPLETE Siamshort/Fable
  StoryBox film project via the Fable MCP, fully directed. Use whenever the user wants you
  to build / gen / "ทำหนัง / ทำซีรีส์ / สร้างโปรเจกต์" in Fable or Siamshort from an idea,
  or says things like "เอาเรื่อง... มาทำเป็นหนัง", "gen project ใน siamshort", "auto-director",
  "ทำหนังให้หน่อย". The skill handles EVERYTHING: project → characters → scenes → items →
  cover → chapter → continuity-directed 15-second shots → comic-SFX overlay → manhwa.
  The user only supplies the story idea; this skill does the directing and the MCP calls.
  Do NOT trigger for plain image gen (use gpt-image) or pure storyboard-sheet prompts (use storyboard).
---

# 🎬 Fable Auto-Director Mode (โหมดผู้กำกับอัตโนมัติ)

**What it's called / แนวหนัง-โหมดนี้คืออะไร**

This is **"Auto-Director Mode"** — a one-line-idea → full-film pipeline on the Fable / Siamshort
StoryBox engine (Seedance 2.0). It is NOT a story generator; it is a **film director + MCP
operator**. The user says *what kind of story they want*; you do the directing decisions and
fire the MCP calls to build the whole project.

The **signature house style** is:

> **Found-Footage × Comic-SFX Hyper-Comedy** —
> a lo-fi, voyeuristic, hand-held "real footage" BASE, played wildly over-the-top, with
> **Scott Pilgrim / Kick-Ass style English onomatopoeia SFX + manga speed-lines** layered on top.

The same engine also runs other base looks on request (all share the continuity + SFX core):
- `found-footage` (default for viral Thai shorts — CCTV, hidden-cam, helmet-cam, vlog)
- `glossy rom-com / sports-comedy` (bright, lens-flare, slow-mo hero — e.g. the "ลุงหล่อ HYROX" build)
- `cinematic drama`, `mockumentary`, `horror found-footage`, etc.

The craft rules below are distilled from the `seedance-camera-grammar-continuity` and
`seedance-continuity-drama-pipeline` skills, plus hard-won fixes from real builds.

---

## 0) What you need from the user (and what you decide)

The user gives a **story idea** (one line is enough). You may ask 1–3 quick questions ONLY if
they materially change the build, then proceed. Sensible defaults:

| Decision | Default | When to ask |
|---|---|---|
| Aspect ratio | **9:16** (viral vertical) | ask if it might be cinematic 16:9 |
| Episodes (ตอน) / shots | 1 chapter; **5 StoryBox** per ตอน | ask if they want a series vs one-shot |
| Base look | found-footage (or match the idea's tone) | ask if ambiguous |
| Comic-SFX layer | ON for action/comedy, by request | offer it |
| A real face? | if user sends a photo → use as character ref | — |

If the idea is action/comedy, **pitch the SFX layer** — it's the magic.

---

## 1) The MCP toolset

All build calls go to the **Fable / Siamshort MCP server**
(in this user's setup the id is `30cd8ff5-560a-4540-b9bc-9b7e55af7173`; discover via ToolSearch
if it differs). Load with ToolSearch in two batches:

- **Build:** `create_project, create_character, create_scene, create_item, create_chapter,
  create_shot, update_shot, regen_character_image, regen_scene_image, regen_item_image`
- **Media:** `generate_cover, gen_manhwa_storyboard, poll_image_task, list_assets, list_shots,
  get_shot, get_full_project_context`

For a real-photo character or a title-card logo, also use the **`gpt-image`** skill (GPT Image 2)
and Fable's `upload_image` (base64 → S3 URL).

**Async note:** every image gen may return a final `imageUrl` OR a `jobId`. If a `jobId`,
`poll_image_task` every ~8s up to ~10 tries. On `500/502/524/"fetch failed"`: wait ~10s and
continue — it usually started. Manhwa returns `status:"generating"` (fire-and-forget; the URL is
NOT exposed via `get_shot`, it renders server-side and shows in the studio).

---

## 2) THE BUILD PIPELINE (fire these in order)

### Step 1 — create_project  ⚠️ LEAN ONLY
The `projects` table currently **rejects extra fields** (worldDescription/worldFilmStyle/genre/
cameraType crash the INSERT, and `update_project` errors too). So:

> Call `create_project` **exactly once** with **only** `{ name, aspectRatio:"9:16" }`.
> If it returns a `projectUid`, USE IT (even though `genre/artStyle` come back null — that's fine,
> the **chapter** carries the real style). NEVER call it twice (creates orphan duplicates).
> NEVER call `update_project`.

### Step 2 — characters (+ images)
- `create_character(projectUid, name, description)` then `regen_character_image(uid, prompt, ratio:"9:16")`.
- **Assign every named character a FIXED screen side** in the description and keep it for the whole
  chapter: e.g. *"RECURRING MAIN, locked frame-RIGHT in all shots"*, opponent *"frame-LEFT"*.
  For anthology episodes, add a **recurring anchor character** (a witness/host/reporter) who appears
  every ตอน — that single fixed person is what makes separate episodes feel like one series.
- **Character look-variants** (transformations): make a SECOND character for a changed look (e.g.
  `@ลุงหล่อ` suit → `@ลุงหล่อบึก` shirtless-buff). Generate the variant's image with
  `regen_character_image(newUid, referenceUrls:[<original's imageUrl>], prompt:"SAME face, but …")`
  so the **face stays identical** (face-lock).
- **Real photo → character:** if the user sends a photo and you can reach the file, `upload_image`
  (base64) → S3 URL → `create_character(..., imageUrl:<S3 url>)`. If you can't reach the file,
  build a faithful look-alike from a detailed description and TELL the user they can drop the photo
  in a reachable folder to swap the exact face.

### Step 3 — scenes (+ images)  ⚠️ EMPTY PLATES
- `create_scene(projectUid, name, description, category, timeOfDay, graphicStyleGenre, graphicStyleSubGenre)`
  then `regen_scene_image(uid, prompt, ratio:"9:16")`.
- **Scenes are LOCATION PLATES — NO people.** Prompt them as empty environments
  ("ABSOLUTELY NO people, no humans, no crowd, no silhouettes — background plate only"). Characters
  are added in the shots, not baked into the scene.
- Every scene description names **3–6 fixed ANCHORS** (stable objects/architecture: door, table,
  pole, fridge, podium, stands…). Anchors are how position-lock works.

### Step 4 — items (+ images)
- `create_item` + `regen_item_image(ratio:"9:16")`. Signature props/weapons (ป้าศรี's ไม้กวาด,
  race bib, medal). A **logo/title-card** can be an item too (see §6).

### Step 5 — cover
- `generate_cover(projectUid, title, prompt, ratio:"2:3")`. The cover endpoint is **flaky (500s)** —
  try once, retry once; if it still fails, mark `cover_pending` and move on (it often actually
  rendered; check `get_project.coverImageUrl` later).

### Step 6 — chapter (carries the real style)
`create_chapter(projectUid, title, mode:"story", aspectRatio:"9:16", genre, subGenre,
graphicStyle:<full style string>, seedanceSystemPrompt:<SYSTEM PROMPT below>)`.
The **seedanceSystemPrompt** is auto-appended to every video gen — bake the contract into it:

```
สไตล์ <base look> กล้องตัวเดียวต่อเนื่อง. ทุก StoryBox = 1 ช็อต 15 วิ.
รักษา wardrobe/prop/แสง/เวลา/อารมณ์ต่อเนื่อง ช็อตถัดไปรับสภาพจบจากช็อตก่อน เปลี่ยนตอน/สถานที่ต้องมี establishing.
ล็อกตำแหน่ง: <ตัวหลัก> ฝั่ง<ขวา/กลาง> เสมอ, <คู่ปรับ> ฝั่ง<ซ้าย>. ปิดท้ายทุกช็อต 14-15s มุมสูงกว้างค้างท้ายบอกตำแหน่งเทียบ anchor.
เน้น close-up บทสนทนา. บทพูดเป็นภาษาไทย(เสียง). ตัวหนังสือบนจอ = อังกฤษเท่านั้น.
ห้ามแบ่งจอ/กริด/หลายช่อง/split screen/ตัวละครซ้ำ-โคลน. single continuous shot, no text overlay except English SFX.
```

### Step 7 — shots (the directing)
For each beat: `create_shot(chapterUid, presetText, seedancePrompt, sortOrder)` →
`update_shot(shotUid, characterIds, sceneIds, itemIds, status:"prompt_ready")`.
- **`presetText`** = a short THAI story summary (1–2 lines), prefix `[ตอนN] `. Not the full prompt.
- **`seedancePrompt`** = the director prompt (template in §3). Tag chars/scenes/items with
  `@name #name $name` — **always a space after the tag** (Thai has no spaces; glued tags break).
- **Link the entity IDs** via `update_shot` — text mentions alone do NOT link. Re-pass
  `characterIds/sceneIds/itemIds` to be safe.
- To **insert** a shot at the front (intro card, new opening), use `sortOrder:0` (sorts before 1).

### Step 8 — manhwa
For every shot: `gen_manhwa_storyboard(shotUid, manhwaStyle)` —
`cinematic-panels` (default) / `action-dynamic` (action/comedy) / `noir-thriller` (horror) /
`emotional-drama`. This is the photoreal comic preview. Skip the *regular* storyboard
(`regen_shot_image`) unless asked.

### 🚫 NEVER gen video
Do not call `generate_video*`, `regen_shot_video`, `story_gen_video_next` unless the user
explicitly asks. You set up prompts; they press render.

---

## 3) DIRECTING GRAMMAR (the continuity contract)

**One shot = one continuous 15-second beat**, single moving camera. Build coverage so emotion reads.

**Shot template (`seedancePrompt`):**
```
Location: #scene <time/light>
<ตัวหลัก> ฝั่ง<ขวา/กลาง> เสมอ, <คู่ปรับ> ฝั่ง<ซ้าย>
0-4s  <shot size + angle> <action/emotion, name 2–3 anchors> ; บทพูด @char: "ไทย..."
4-8s  <DIFFERENT size/angle> <reaction — cover both speakers>
8-12s <DIFFERENT> <counter-reaction / decision>
12-14s <handoff emotion to next shot>
14-15s มุมสูงกว้างค้างท้าย เห็นทั้งฉาก: <ใครอยู่ตรงไหนเทียบ anchor>
<STYLE/SFX tail + guard>
```

**Position-lock (the #1 rule the user cares about):** assign each character a fixed screen side and
**never swap it** — A stays left, B stays right, the whole chapter. State the side every shot and in
the 14-15s high-wide **position-lock tail** (the tail re-establishes exact placement vs anchors so
the next shot can inherit it).

**Continuity:** each shot inherits the previous shot's ending position/action/emotion; within a ตอน
the 5 shots are ONE continuous scene (only size/angle change); keep **action continuous** across cuts;
**establishing beat** at every new ตอน/location; vary shot size & angle each adjacent shot; give
**close-up reaction coverage** to everyone affected, including silent witnesses.

**Shot-size by frame fill:** extreme-CU (~100%) / CU (~80%) / medium (~50%) / wide (~20%) / extreme-wide.
**Angle by emotion:** eye-level/OTS for talk, high for weak/ashamed, low for power/threat, top for
documents, slight dutch for rupture, POV for subjectivity. A high/overhead angle is a CAMERA **MOVE**
(crane/orbit) — never a held map.

**No-grid guard** (append to every video prompt; certain words make Seedance render a 3×3 contact
sheet instead of a moving shot — avoid map/CCTV-grid/floor-plan/clock-position/compass/multi-view):
```
ภาพเดียวต่อเนื่อง กล้องตัวเดียว ห้ามแบ่งจอ ห้ามกริด ห้ามหลายช่อง ห้ามคอลลาจ ห้าม split screen ห้ามตัวละครซ้ำ/โคลน.
single continuous cinematic shot, one moving camera, no split screen, no grid, no panels, no multi-view, no duplicate/clone character.
```

---

## 4) COMIC-SFX LAYER (the signature "เท่ๆ")

Layer Scott-Pilgrim / Kick-Ass comic energy ON TOP of the live-action base — pop-out SFX words +
manga speed-lines + halftone/ink bursts + white impact flashes, animated at the impact beats.

- **🟥 ON-SCREEN TEXT MUST BE ENGLISH.** Seedance cannot render Thai text on the image (it comes out
  garbled). SFX words are ENGLISH only: `SNATCH!` `VROOM!` `KYAAAA!` `FWOOM!` `RRRIP!` `CHA-CHING! $$$`.
  **Spoken dialogue stays THAI** — that's audio/lip-sync, not on-screen text, and Seedance handles it.
- It stays **one continuous shot** — the comic FX are overlays, NOT a multi-panel comic page. Keep the
  no-grid guard; just swap "no on-screen text" for "English SFX overlays allowed, no Thai text".
- **The 14-15s tail clears SFX** so positions read clean.

**SFX tail to append (English-SFX variant):**
```
<base look> photoreal live-action BASE, with animated comic-book ENGLISH onomatopoeia SFX text
(English words ONLY, no Thai on screen) + manga speed-line impact bursts + halftone/ink-burst overlays
(Scott Pilgrim / Kick-Ass style). ภาพช็อตเดียวต่อเนื่อง กล้องตัวเดียว ไม่ใช่หน้าการ์ตูนหลายช่อง — ตัวหนังสือ SFX อังกฤษเท่านั้น
ห้ามตัวหนังสือไทยบนภาพ ห้ามแบ่งจอ/พาเนล/กริด/split screen/ตัวละครซ้ำ-โคลน.
```

**SFX vocab by beat:** impact `BOOM! SLAM! THWACK! CRASH!` · speed `DASH! VROOM! SKRRT! WHOOSH!` ·
grab `SNATCH! GRAB! GOTCHA!` · shock `HUH?! GASP?! WHOA?!` · swoon `KYAAAA! BA-DUMP! 💗` ·
money `CHA-CHING! $$$` · power-up `FWOOM! 💢 DEMON AURA!!` · cute `DING ✨ SMIRK~ WINK 😉` ·
ending `FINISH! 🏁 TO BE CONTINUED?!`

---

## 5) HARD RULES (learned the hard way — don't repeat these)

1. **On-screen text = English; dialogue = Thai.** (Seedance can't render Thai text on image.)
2. **Scenes = empty plates, no people.**
3. **create_project lean only; never update_project** (DB rejects extra fields).
4. **Cover endpoint is flaky** — try/retry once, else `cover_pending` and continue.
5. **Position-lock + 14-15s tail on every shot.** Never let A and B swap sides between clips.
6. **Recurring anchor character** glues anthology episodes into a series.
7. **Face-lock variants** via `regen_character_image(referenceUrls:[orig.imageUrl])` for transformations.
8. **Tag hygiene:** a space after every `@ # $` tag.
9. **Back up before overwriting** when revising (see §7).
10. **Never gen video** unless asked. Manhwa is the preview.

---

## 6) INTRO TITLE-CARD recipe (optional, very "เท่")

1. Generate 2–3 logo title-card options with the **`gpt-image`** skill (GPT Image 2) — for a TITLE/LOGO,
   Thai or English text is fine because it's a still image (NOT through Seedance). Let the user pick.
2. Save the chosen logo as an **`$item`** (`create_item(..., imageUrl:<cdn url>)`).
3. Insert a **`sortOrder:0`** StoryBox: a 5-second single continuous title card — hero stands beside the
   logo, signature move, looks at camera; allow only the logo text; keep the no-grid guard.

---

## 7) REVISION workflow (when the user tweaks a shot)

1. `get_shot` (or `list_shots`) to read the CURRENT prompt + entity links.
2. **Back up the old prompt(s) to a local `.md` file FIRST** (e.g. `<project>-BACKUP.md`) so the user can
   revert ("revert shot N" → put the backed-up prompt back).
3. `update_shot` with the new `seedancePrompt`, re-passing `characterIds/sceneIds/itemIds`.
4. If the change alters the visible content, `gen_manhwa_storyboard` again for that shot.
- Studio display numbering shifts by +1 when an intro card sits at sortOrder 0 (display #N = sortOrder N-1).

---

## 8) QUALITY GATE (before saying "done")

- [ ] Project lean-created; chapter carries the full style + seedanceSystemPrompt.
- [ ] Every character has a fixed screen side; recurring anchor present for series.
- [ ] Scenes are empty plates with 3–6 named anchors; all asset images generated.
- [ ] Every shot: `presetText` (Thai) + `seedancePrompt` + linked `characterIds/sceneIds/itemIds`.
- [ ] Each shot opens with position-lock line, ends with 14-15s high-wide tail; action continuous;
      establishing on each new location.
- [ ] On-screen SFX English only; dialogue Thai; no-grid guard on every prompt.
- [ ] Manhwa fired for every shot. No video generated.
- [ ] Cover present or `cover_pending` noted.

---

## 9) CREDITS / COST notes

- Cost ≈ number of **image generations**: characters + scenes + items + cover + (1 manhwa per shot).
  Shot text (create_shot/update_shot) is ~free. No video = no video credits.
- GPT Image 2 (gpt-image skill) high/1K ≈ **64 credits/image**; use `--quality low` for drafts.
- Tally at the end: list image-gen counts per category and the total.

---

## 10) WORKED EXAMPLE (one line → full build)

> User: *"ลุงคนนี้แข่ง HYROX ถอดเสื้อโชว์กล้าม สาวกรี๊ด แนวรักตลก 5 ช็อต ใส่ SFX"*

1. `create_project{ name:"ลุงหล่อพิชิต HYROX", aspectRatio:"9:16" }` → projectUid.
2. Characters: `@ลุงหล่อ` (suit, CENTER hero) + face-locked variant `@ลุงหล่อบึก` (ripped) +
   `@แนน` (LEFT) + `@จอย` (RIGHT, distinct face). regen all.
3. Scenes (empty plates): `#สนามHYROX`, `#เส้นชัยHYROX` + anchors. Items: `$ป้ายเบอร์074`, `$เหรียญแชมป์`.
4. Cover (2:3). Chapter with glossy-rom-com style + SFX system prompt.
5. 5 shots: ① arrive in suit → `RRRIP!!` rip → buff reveal `✨BOOM✓ WHOA?!`  ② race surge `DASH! BOOM!`
   ③ flex + fans `KYAAAA! 💗`  ④ 2 women chase `DASH! WAIT~!`  ⑤ finish `FINISH! 🏁 GLOMP! WINK 😉`.
   Each: ลุง CENTER / แนน LEFT / จอย RIGHT, Thai dialogue, English SFX, 14-15s tail.
6. Link IDs, `gen_manhwa_storyboard(action-dynamic)` ×5. No video.

That's the whole mode. **User brings the idea; you direct the film and command the MCP.**
