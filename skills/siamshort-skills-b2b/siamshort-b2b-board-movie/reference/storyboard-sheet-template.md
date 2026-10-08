# Storyboard Sheet Template (production style — ONE image, multi-panel)

Template พิสูจน์แล้วจากงานจริง (Speechless). ผลลัพธ์ = **รูปเดียว** ที่มี N panel
เรียง 2 คอลัมน์ (❌ ไม่ใช่หลายรูป). ใช้ได้ 2 โหมด:
- **1 ซีน = 1 sheet** (board-movie เดิม): panel = ช็อตทั้งหมดของซีน.
- **1 shot-storybox = 1 sheet** (movie pipeline, user ruling 2026-07-16):
  panel = การแตก action ของ storybox เดียวเป็นมุมกล้อง 4–8 มุม —
  ผลลัพธ์ register เป็น storyboard ของ shot นั้น
  (`add_shot_asset(shot_id, type:"storyboard", run_id)` — ผ่าน gate
  variant/replace ตาม auto-movie §A10 เสมอ).
แทนที่ `{...}` ทุกจุดก่อนใช้ ; โครง/ถ้อยคำนอกนั้น **ห้ามตัดทิ้ง**
(แต่ละบล็อกคือบทเรียนที่จ่ายมาแล้ว).

## วิธีเติม

| Placeholder | ใส่อะไร |
|---|---|
| `{PROJECT_TITLE}` | ชื่อเรื่อง |
| `{SCENE_NO}` | โหมดซีน: เลขซีน · โหมด per-shot: เลข sequence (หรือ `SEQ.SHOT` เช่น `2.3` ให้ชัดต่อแผ่น) — ย้ำใน rule กัน model เขียน Scene 1 ทุกแผ่น |
| `{N}` / `{ROWS}` | โหมดซีน: จำนวนช็อตของซีน · โหมด per-shot: จำนวน beat/มุมกล้องที่แตกจาก storybox (**4–8**: ~5วิ→4 · 10–15วิ→6–8) / `ceil(N/2)` (2 คอลัมน์เสมอ) ; N>10 → แตก 2 sheet แล้วคัดลอกบล็อก style+ref ซ้ำเป๊ะ |
| `{LANGUAGE}` | ภาษาของ action/dialogue บนแผ่น (default `Thai`) — คำอธิบายมุมกล้องใน CAMERA ANGLE VOCABULARY แปลตามภาษานี้ด้วย (ตัวอย่างในเทมเพลตเป็นไทย) |
| `{PANEL_RATIO}` | ratio ของหนัง (จาก project.ratio) |
| `{PANEL_ORIENTATION}` | 16:9 → `HORIZONTAL (landscape orientation) — wider than tall` / 9:16 → `VERTICAL (portrait orientation) — taller than wide` |
| `{CAMERA_LENS}` | สเปกกล้อง/เลนส์ตามลุคของเรื่อง เช่น `ARRI ALEXA Mini LF, anamorphic 50mm, T2.8, shallow depth of field, cinematic film grain` ; ไม่มีธีมเฉพาะ → `Eye-level framing, cinematic anamorphic composition, shallow depth of field` (ประโยค anti-rig หลัง placeholder = ส่วนคงที่ ห้ามตัด) |
| `{REF_MAPPING}` | บรรทัดต่อ ref ตามลำดับ `ref_node_ids` ที่แนบ: `Image k (@imagek): Character/Scene "ชื่อ" — use this exact ...` (cast = face/hair/body/clothing · set = environment/lighting/atmosphere) |
| `{STYLE_LOCK}` | สไตล์ที่ล็อกทั้งเรื่อง (แทนบรรทัด MANDATORY STYLE) |
| `{STORY_ACTION}` | โหมด per-shot: **วาง storybox ของ shot ทั้งก้อน** (plot+POSITION LOCK+TIMING+บทพูด ครบตาม format เดิม — มันคือ golden sample อยู่แล้ว). โหมดซีน: **บล็อกที่ตัดสินคุณภาพ — เขียนครบตาม golden sample:** (1) บรรทัด style ของเรื่อง (2) สถานที่ `@imageK(ฉาก)` + เวลา/แสง (3) `เริ่มต่อเนื่องจากช็อตก่อน: ...` ถ้ามี (4) **⛔ POSITION LOCK เข้มงวด**: ทุกตัวละคร = ลุคเต็ม (ผม/ชุด/สีหน้า) + โซน foreground/background + หันทางไหน + ข้อห้าม (`❌ห้ามเดินเข้าหากัน ❌ห้ามรวม two-shot ❌ห้ามดริฟต์`) (5) **beat ไล่เวลา** `0-3s:/3-7s:/7-11s:` (6) `กล้อง:` มุม+ข้อห้าม (7) `บทพูด:` (8) `เสียง:` (9) `Negative:` no text/subtitles/logo/split (10) ประโยครักษา identity ปิดท้าย — อ้าง `@imageN(ชื่อ)` ทุกครั้งที่เอ่ยตัวละคร/ฉาก |
| sheet ratio ตอน gen | 2 คอลัมน์ 16:9 ≈ ใกล้จัตุรัส → `image_size:"1:1"` (4 แถว) หรือ `"3:4"` (5+ แถว) ; panel 9:16 → `"9:16"` |

## TEMPLATE (ส่งทั้งก้อนเป็น prompt เดียว)

```
You are a professional storyboard artist and film production designer.
Create a professional storyboard image in the style of a real film production storyboard.
=== PROJECT TITLE ===
Add a header bar at the top of the storyboard with the project title: "{PROJECT_TITLE}"
The header should be clean and professional (dark background, white text, centered).
=== STORYBOARD PANEL LAYOUT ===
Create a storyboard image with 2 COLUMNS and multiple ROWS ({ROWS} rows = {N} panels total).
Each ROW contains 2 panels side by side.
Each PANEL consists of:
- LEFT HALF: A cinematic illustration/frame showing the action
- RIGHT HALF: A text information block with white/light background containing:
  * "SCENE {SCENE_NO}" (boxed) and "SHOT" number (1-{N})
  * "ACTION / DIALOGUE" section with the action description in {LANGUAGE}
  * "NOTE / CAMERA" section with camera angle/movement info
IMPORTANT: The SCENE number for ALL panels in this storyboard is {SCENE_NO}. Do NOT use Scene 1 unless this IS scene 1.
The text info block uses clean typography:
- "SCENE {SCENE_NO}" label in small caps with the number in a bordered box, and "SHOT" number (1-{N})
- "ACTION / DIALOGUE" as a section header in bold
- Action text in regular weight, {LANGUAGE} language
- "NOTE / CAMERA" as a section header
- Camera info in format: "CAMERA TYPE / {LANGUAGE} description" (e.g., "WIDE SHOT / มุมกว้าง", "CLOSE UP / มุมใกล้", "MEDIUM SHOT / มุมระดับสายตา")
Use thin black borders/lines to separate panels and sections.
The overall image should look like a professional film production document.
=== LANGUAGE RULE ===
Action/Dialogue text: {LANGUAGE} language
Camera labels: English camera type + {LANGUAGE} description
Scene/Shot labels: English
No watermarks, no logos.
=== PANEL ASPECT RATIO (CRITICAL) ===
This video is {PANEL_RATIO} format. Each panel illustration MUST use {PANEL_RATIO} aspect ratio.
Panels are {PANEL_ORIENTATION}.
Do NOT draw square panels. The panel shape must clearly reflect the {PANEL_RATIO} video frame.
=== REFERENCE IMAGE MAPPING ({K} images attached) ===
{REF_MAPPING}
CRITICAL: Faithfully reproduce each character's appearance from their reference image. Face, hair style, skin tone, and outfit MUST match the reference exactly in every shot.
=== VISUAL STYLE (APPLY TO ALL ILLUSTRATION FRAMES) ===
MANDATORY STYLE: {STYLE_LOCK}
Camera/Lens: {CAMERA_LENS}. Floor/ground clear — NO camera, tripod, DSLR, rig, boom or crew anywhere in frame. The camera is an invisible eye. NO on-screen UI, NO subtitles, NO captions, NO burned-in text inside the illustration frames.
=== CONTINUITY RULES ===
Before drawing, plan the physical staging:
1. Identify the main location and spatial anchor.
2. Place all characters in consistent positions.
3. Maintain character positions across all panels unless movement is described.
4. Only the camera angle changes between panels — characters stay in place.
Do not restage the scene for each panel.
Do not swap character positions.
Do not change foreground/background order unless the story describes movement.
Scene: {SCENE_NAME}
=== STORY ACTION (Divide into {N} shots) ===
{STORY_ACTION}
=== SHOT PROGRESSION ===
Divide the user's action into {N} logical shots with varied camera angles:
- Mix of WIDE SHOT, MEDIUM SHOT, CLOSE UP, INSERT SHOT, MEDIUM CLOSE UP as appropriate
- Each shot should advance the story
- Vary camera angles for visual interest while maintaining spatial consistency
- Include establishing shots, reaction shots, and detail shots as needed
=== CAMERA TRANSITION RULES (CRITICAL) ===
- NEVER use the same camera angle for 2 consecutive shots (e.g., Shot 3 = WIDE SHOT → Shot 4 MUST NOT be WIDE SHOT)
- Shot {N} (LAST SHOT) MUST use a DIFFERENT camera angle from Shot 1 — this ensures a clear visual transition when cutting to the next sequence
- Shot 1 typically opens with WIDE SHOT or establishing angle; Shot {N} must close with a contrasting angle (CLOSE UP, MEDIUM CLOSE UP, INSERT SHOT, or OVER THE SHOULDER)
- If Shot 1 is WIDE SHOT, Shot {N} should be CLOSE UP or MEDIUM CLOSE UP (and vice versa)
- This prevents the "last shot looks identical to next video's first shot" problem
- Think of Shot {N} as the TRANSITION POINT — it must create visual contrast that makes the cut to the next sequence feel intentional and dynamic
=== CHARACTER IDENTITY PRESERVATION ===
Every character must keep the exact same appearance across all panels:
- Same face, hair, clothing, body proportions
- Do not redesign or beautify characters between panels
- When @imageN(CharacterName) is mentioned, draw EXACTLY as shown in reference
- Throughout the entire storyboard, do not duplicate the same character in the same panel; avoid multiple characters sharing the same face
=== CAMERA ANGLE VOCABULARY ===
Use these camera types in the NOTE/CAMERA section:
- WIDE SHOT / มุมกว้าง
- MEDIUM SHOT / มุมระดับสายตา
- CLOSE UP / มุมใกล้
- MEDIUM CLOSE UP / มุมใกล้
- INSERT SHOT / มุมใกล้สิ่งของ
- LOW ANGLE / มุมต่ำ
- HIGH ANGLE / มุมสูง
- OVER THE SHOULDER / มุมข้ามไหล่
- POV / มุมมองตัวละคร
=== FINAL QUALITY TARGET ===
The final image must look like a professional {LANGUAGE} film production storyboard document.
Clean, readable, with cinematic illustrations and organized text information.
All panels must feel like one continuous scene with consistent character blocking.
```

## หมายเหตุการใช้กับ GEE

- ยิงผ่าน `canvas_add_advanced_gen(board_id, kind:"image", prompt:<template ทั้งก้อน>,
  resolution:"2K" ขึ้นไป (ตัวหนังสือใน panel ต้องอ่านออก), ratio ตามตาราง)` →
  node วางแบบ idle ให้ review → `run_gen_node`.
- **วิธี map mention (สำคัญสุด):** ยิงผ่าน `canvas_add_advanced_gen(kind:"image", prompt:<template>)`
  — บล็อก REF MAPPING แต่ละบรรทัดปิดท้ายด้วย **mention token จริง**:
  `Image 1 (@image1): Character "โรส" — use this exact face... @[โรส](cast:<uuid>)`
  (tool สร้าง Asset reference node + ต่อสายตามลำดับ mention → `@image1` = mention แรกเสมอ) ;
  ในเนื้อ STORY ACTION ใช้ `@image1(โรส)` เป็นคำธรรมดา.
  ⛔ **ห้ามใช้ simple node / prompt คีย์เฟรมเดี่ยวแทน storyboard sheet เด็ดขาด.**
- sheet ที่ผ่าน Gate 2 แล้ว → `save_to_mix_stage` เก็บเป็นคลังถาวรของซีน.
