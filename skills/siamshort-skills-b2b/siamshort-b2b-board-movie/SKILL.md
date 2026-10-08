---
name: siamshort-b2b-board-movie
description: >-
  Board-Movie Pipeline — สร้างวิดีโอเรื่องยาวบน Idea Board ของ Siamshort/GEE แบบ
  "คุมความต่อเนื่อง" ครบวงจร: story → gen cast/sets/props → วาง storybox + gen
  storyboard image ต่อช็อต (ref entity) → manhwa position frame (ถ้าต้องการ) →
  gen วิดีโอต่อช็อตโดย ref storyboard + ช็อตก่อนหน้า — มี 4 CONFIRM GATE (elements →
  storyboard prompts → รูปทั้งหมด → video prompts): ก่อน gen ทุกขั้น วาง node idle พร้อม prompt
  ให้คน confirm ก่อนยิงเสมอ + เขียน prompt ทีละช็อตห้าม batch. ใช้เมื่อ user อยากได้ "หนัง/
  เรื่องราวบน idea board ที่ภาพนิ่ง-วิดีโอต่อเนื่องกัน", "ทำหนังบน canvas ให้เป็นระบบ",
  "/siamshort-b2b-board-movie". สกิลนี้ = วิธีการผลิต ; วิธีใช้ node/เครื่องมือ =
  /siamshort-b2b-idea-board (อ่านคู่กัน). Do NOT trigger สำหรับ mood board เล่นๆ
  (idea-board recipe ธรรมดาพอ) หรืองาน sequence/shot จริงจัง (/siamshort-b2b-auto-movie).
---

# 🎞 SiamShort Board-Movie Pipeline (GEE) — story → วิดีโอครบเรื่อง บนบอร์ดเดียว

จุดต่างจาก recipe "Story Strip" ธรรมดา: pipeline นี้ **บังคับขั้น identity + storyboard +
position ก่อนถึงวิดีโอ** — แก้ปัญหา "วิดีโอแต่ละช็อตหน้าตา/ฉาก/ตำแหน่งไม่ต่อเนื่อง".
เครื่องมือทั้งหมด = siamshort MCP (`/siamshort-b2b-idea-board` cheat-sheet) ;
craft ระดับ prompt = `/siamshort-b2b-shot-continuity` + anti-plastic + physics-guide.

---

## LAYOUT มาตรฐานของบอร์ด (กันทับ + อ่านง่าย) ⭐

ใช้ **x,y ชัดเจนทุก node** (MCP รองรับแล้ว ; ไม่ใส่ = ระบบวางต่อท้ายล่างสุดให้เอง ไม่ทับ):

```
แถว STYLE/STORY   y=80     : note_text เรื่องย่อ · sticky_note style lock
แถว CAST/SET/PROP y=500    : รูป entity เรียงแนวนอน (คอลัมน์ละ 400px)
แถว SHOT i       y=1000 + (i-1)*1300 : frame ครอบ 1 ช็อต —
   x=80 prompt/storyboard gen group · x=1300 manhwa group (ถ้ามี) · x=2500 video group
```
- 1 ช็อต = 1 แถว (สูง ~1300) ; ภายในช็อตวางกลุ่ม gen ห่างกันแนวนอน ≥1200.
- ตั้ง `label` ทุก node สำคัญ (`SB01 storyboard`, `SB01 video`) — คนเปิดบอร์ดอ่านรู้เรื่อง.

---

## PIPELINE 11 ขั้น · 4 CONFIRM GATE 🚦 — "วาง node idle ให้ครบ → คน confirm → ค่อยยิง"

หลักคิด 2 ข้อ (ห้ามละเมิดทั้งคู่):
- 🚦 **CONFIRM-BEFORE-RUN ทุกขั้นที่เสียแต้ม**: `canvas_add_advanced_gen` สร้าง node
  **idle** (ฟรี ยังไม่ยิง) — วาง node พร้อม prompt เต็มให้ครบทั้งชุดก่อน → หยุดรอ user
  confirm → ค่อย `run_gen_node`. ทุก gate = สรุปให้ user ดู แล้ว**หยุดรอ** ห้ามข้าม.
- ✍️ **ONE-AT-A-TIME RULE**: storybox text · storyboard sheet prompt · video prompt —
  **เขียนทีละช็อต/ซีนเสมอ ห้ามเขียน batch หลายช็อตรวดเดียว**. เขียนช็อต i ให้จบลึกครบ
  ทุกส่วน (อ่าน storybox/ผลช็อต i-1 ก่อนเสมอ) → วาง node ลงบอร์ดทันที → ค่อยขึ้นช็อต i+1.
  เหตุผล: เขียนขนานกัน = prompt สั้น ตื้น รายละเอียดหาย ทุกตัว (พังมาแล้ว) — โดยเฉพาะ
  video prompt ที่ของจริงยาวมาก ต้อง analyze ทีละช็อต.

### 1) STORY
- รับเรื่อง/ไอเดีย → ถาม **pacing** + **ratio** ถ้าไม่ชัด → เลือก **STYLE LOCK**
  (เสนอ 3–5 จากโทนเรื่อง; เขียนเป็น `sticky_note "STYLE LOCK: ..."` — แปะท้าย prompt
  รูป/วิดีโอทุกตัวทั้งเรื่อง คำต่อคำ).
- ⏱ **DURATION BUDGET (ทำตั้งแต่ตรงนี้):** 1 วิดีโอ = **4–15 วิเท่านั้น** →
  ความยาวหนัง T วินาที = ผลรวมของช็อต 4–15 วิ. สูตรเร็ว: จำนวนช็อต ≈ T ÷ 6–10 วิ
  (30 วิ → 3–6 ช็อต · 60 วิ → 6–10 ช็อต · 3 นาที → 15–25 ช็อต). กำหนด duration
  รายช็อตตามจังหวะ: beat เร็ว/ตัดฉับ = 4–6 วิ · beat ปกติ = 6–10 วิ · beat อารมณ์/ยืด
  = 10–15 วิ ; **รวมแล้วต้อง ≈ T** (คลาดได้ ±10%). แสดงตารางช็อต+วินาทีให้ user เห็น.
- เขียนเรื่องย่อ + โครง beat → `note_text` ลงแถว STORY. `get_balance` + ประมาณการแต้ม
  ทั้งเรื่อง (รูป ~4.5pt · วิดีโอ ~20-40pt/ช็อต — วิดีโอคิดตาม duration) แจ้ง user.

### 2) GEN ELEMENTS — cast / sets / props
- สกัดรายชื่อจากเรื่อง → `create_entity` → `generate_entity_image` ทุกตัว → QC gate (regen ≤3).
- 🎯 **CLEAN REF RULE — description = ตัว subject ล้วนๆ เท่านั้น:**
  - **Cast**: DNA ของตัวละครอย่างเดียว (หน้า/วัย/ผม/ชุด/ของติดตัว) — ❌ ห้ามใส่ฉากหลัง/
    สถานที่/คนอื่นใน description (ระบบจะ gen เป็น clean reference background ให้เอง;
    ใส่ฉากไป = ตีกับ directive ของระบบ → ภาพ drift)
  - **Prop**: วัตถุเดี่ยวล้วน (แก้ว = แก้วใบเดียว, ปืน = ปืนกระบอกเดียว) — ❌ ไม่มีมือถือ/
    โต๊ะ/ฉาก (ระบบ gen เป็น isolated object บนพื้นขาว studio ให้เอง)
  - **Set**: สถานที่ล้วน ไม่มีคน — eye-level wide establishing, anchor อสมมาตรชัด
  - ตรวจตอน QC: cast มี bg/คนอื่นแทรก · prop มีฉาก/มือ · set มีคน = **FAIL → regen**
- ดึงขึ้นบอร์ดด้วย **`canvas_add_asset_ref(board_id, entity_id)`** (การ์ด Asset reference
  มาตรฐานเว็บ) เรียงแถว CAST/SET/PROP → **ref กลางของทุกช็อต**.

- 📎 **user แนบไฟล์ ref มา = ต้องใช้เสมอ**:
  `upload_reference(file_path, workspace_id:<project.workspace_id>)` →
  - หน้าคน/ลุคตัวละคร → ref ตอน gen รูป cast บน canvas (หรือใช้ตรงเป็น ref วิดีโอได้เลย —
    MCP register virtual asset ให้อัตโนมัติแล้ว)
  - ภาพสถานที่/สไตล์ → ref ของ Set/storyboard gen · โลโก้/ของจริง → ref ของ Prop
  - **คลิปวิดีโอแนบ** → video node → ref ของ canvas_generate_video (**motion ref** —
    Seedance เลียนแบบการเคลื่อนไหว/จังหวะ ; กำกับ "copy MOTION only, not look/lighting")
    หรือ save_to_mix_stage → แนบช็อต (คลิป → video_files อัตโนมัติ)
  - **ไฟล์เสียงแนบ** → audio node → sound/voice/music ref ของ video gen (audio_files;
    เลือก Seedance model ที่รองรับ audio ref) หรือ save_to_mix_stage → แนบช็อต
  - ทุกตัวขึ้นบอร์ดเป็น image/video/audio node label "user ref: ..." ให้เห็นว่าอะไรมาจาก user

### 🚦 3) GATE 1 — CONFIRM ELEMENTS
- โชว์รูปทุกตัว + เรื่องย่อ → user ชี้ตัวไหนไม่ใช่ → แก้ DNA + regen เฉพาะตัว → confirm.
- **identity ผิดตรงนี้ = ผิดทั้งเรื่อง** — gate นี้ห้ามรีบ.

### 4) STORYBOX TEXT — ทุก sequence ทุก shot (text ล้วน ฟรี) — ✍️ ทีละช็อต
- แตกเรื่องเต็มเป็น shot list ละเอียดทุกช็อต: action + มุมกล้อง + position + **duration
  (4–15 วิ ตาม DURATION BUDGET ข้อ 1 — ผลรวม = ความยาวหนัง)** + transition +
  **entity ที่อยู่ในช็อต** (ทีมกำกับ 5 role; แรงตั้งต้น → physics-guide).
- ✍️ **เขียนทีละช็อตตามลำดับเรื่อง**: เขียน SB01 จบลึก → `canvas_add_node(note_text,
  label:"SB01")` ลงแถวช็อตทันที → อ่าน SB01 อีกรอบเพื่อ continuity → ค่อยเขียน SB02.
  ❌ ห้ามร่างทุกช็อตพร้อมกันแล้วเทลงบอร์ดทีเดียว — ได้ storybox ตื้นทุกตัว.
- ⏱ **ปริมาณ action ต้องพอดีวินาที**: ช็อต 5 วิ = 1 การกระทำ + 1 reaction ; ช็อต 10–15 วิ
  = 2–3 จังหวะ. action เกินเวลา = โมเดลเร่ง/ตัดเอง = slop — แตกเป็น 2 ช็อตแทน.

### 5) SETUP STORYBOARD NODES พร้อม PROMPT — ทุกซีน (idle ยังไม่ยิง = ฟรี) ⭐ ✍️ ทีละซีน
- **1 ซีน = 1 storyboard sheet เดียว** (ไม่ใช่ 1 รูปต่อช็อต!) — professional film document:
  header ชื่อเรื่อง · 2 คอลัมน์ × ceil(N/2) แถว · แต่ละ panel = ภาพ + กล่องข้อความ
  (SCENE/SHOT · ACTION ไทย · CAMERA EN/ไทย) · กฎ transition (ห้ามมุมซ้ำติดกัน, ช็อตท้าย
  ≠ ช็อตแรก) · identity preservation ครบ.
- ⛔ **ใช้ template เต็มจาก `reference/storyboard-sheet-template.md` เท่านั้น** — เติม
  placeholder (title/scene no/N/ratio/STYLE LOCK/ref mapping/story action + POSITION LOCK)
  ห้ามเขียน prompt storyboard เอง. ⛔ ห้ามใช้ simple node / prompt คีย์เฟรมเดี่ยวแทน sheet.
- ✍️ เขียน template ของซีน i ให้จบเต็มก้อน (STORY_ACTION ครบ 10 องค์ประกอบทุก panel) →
  **`canvas_add_advanced_gen(kind:"image", prompt:<template เต็มก้อน — REF MAPPING ปิดท้าย
  บรรทัดด้วย mention token @[ชื่อ](cast:/set:id) ตามลำดับ @imageN>, resolution:"2K",
  ratio:"1:1"/"3:4", x:80, y:<แถวซีน>, label:"SCENE x storyboard")`** → ค่อยเขียนซีน i+1.
  **ยังไม่เรียก run_gen_node** — node idle รอ gate.

### 🚦 6) GATE 2 — CONFIRM STORYBOARD PROMPTS (ก่อนเสียแต้มรูปแม้แต่แต้มเดียว)
- สรุปทุก sheet ให้ user: ซีนไหน กี่ panel, ref ตัวไหนบ้าง, ประมาณแต้มรวม → user เปิดบอร์ด
  อ่าน prompt บน node ได้ตรงตัว (แก้บนเว็บหรือสั่ง agent แก้ — ฟรี) → **confirm แล้วค่อยยิง**.

### 7) RUN STORYBOARD + MIX STAGE — ทีละ sheet
- `run_gen_node(<sheet i>)` → `wait_for_run` → QC: identity ตรง ref · ครบ N panel ·
  เลข SCENE ถูก · panel ratio ถูก (regen ≤3) → ลง `add_shot_asset` เมื่อผูกกับช็อตจริง.
  ⛔ ห้าม auto-promote/auto-attach. เมื่อ user สั่งใช้ sheet เป็น video ref จึง
  `list_promotable_references` → `save_to_mix_stage` → `attach_shot_mix_stage_refs`
  แบบ additive และใส่ mention_token ใน video prompt; ถ้ามีหลาย candidate ต้องถามก่อน.
- ช็อตไหนต้องการ ref เฟรมเดี่ยวสะอาดๆ เพิ่ม (ไม่มีกล่องข้อความ) → gen keyframe เฉพาะช็อตนั้น
  เสริมได้ (composition ตาม panel ใน sheet).
- **GEN MANHWA (ถ้าต้องการ — ช็อต blocking ซับซ้อน)**: `canvas_generate_image("manhwa
  staging panel of <ช็อต>, arrows showing movement, positions labeled in English",
  ref_node_ids:[storyboard ช็อตนั้น], x:1300, y:<แถวช็อต>)` — รูปถูก + prompt เชิงกลไก
  ยิงได้เลยแล้วรีวิวรวมใน Gate 3.
  ⛔ **manhwa = display/position-planning เท่านั้น — ห้ามต่อสายเข้า video node อัตโนมัติ**
  (decision Rev 3 #1): แค่**เสนอ** user ที่ Gate 3/4 ว่ามี manhwa ใช้เป็น position guide ได้
  → **user สั่งเองเท่านั้น** ค่อย `canvas_connect_nodes` + mention `@[label](node:id)`
  (พร้อมกำกับ "positions only — ❌ห้ามลอกสไตล์ manhwa ลงวิดีโอ").
  📌 โปรเจกต์ที่ทำงานบน `studio_shots` จริง (movie pipeline) → ลงทะเบียน manhwa ด้วย
  `add_shot_asset(shot_id, type:"manhwa", run_id)` แทน — เลิกท่า naming-convention
  `manhwa_*` บน Mix Stage แล้ว. ถ้ารูปใดไม่ใช้ ให้เลือกตัวที่ดีด้วย `select_shot_asset`
  ก่อน แล้วค่อย `remove_shot_asset` เพื่อซ่อน pointer จากช็อตเท่านั้น — output/run/storage
  และประวัติแต้มยังอยู่ครบ, ไม่มี refund.

### 🚦 8) GATE 3 — CONFIRM ALL VISUALS ⭐ ด่านกันเงินหลัก
- โชว์ **storyboard sheet ทุกซีน + manhwa เรียงตามซีน/ช็อต** (สรุป: ช็อตไหนผ่าน/regen กี่ครั้ง/ตัวไหน
  ยังน่าห่วง) → user ไล่ดูทั้งเรื่อง สั่งแก้เป็นรายช็อต → แก้จน user **confirm ทั้งชุด**.
- ❌ **ห้ามแตะวิดีโอแม้แต่ช็อตเดียวจนกว่า gate นี้ผ่าน** — regen รูป 4.5pt vs วิดีโอ 20-40pt.

### 9) SETUP VIDEO NODES พร้อม PROMPT — ทุกช็อต (idle ยังไม่ยิง = ฟรี) ⭐ ✍️ ทีละช็อต
- ✍️ **video prompt ของจริงยาวมาก — วิเคราะห์+เขียนทีละช็อตเท่านั้น**: อ่าน storybox +
  storyboard panel + ตำแหน่งท้ายช็อต i-1 → เขียน prompt ช็อต i เต็ม → วาง node → ช็อต i+1.
- ต่อช็อต: `canvas_add_advanced_gen(board_id, kind:"video", prompt, model, ratio, duration
  ตาม shot list, x:2500, y:<แถวช็อต>, label:"SBxx video")` — **สร้าง node แบบ idle เสมอ
  ไม่ยิง**. prompt = motion + dialog + camera + `[POSITION LOCK]` + STYLE LOCK + anti-slop
  + **mention ตัวละคร/ฉากด้วย mention_token** (`@[ชื่อ](cast:id)` `#[ฉาก](set:id)`) —
  tool จะสร้าง ref node + ต่อสายให้เอง ; ref เพิ่มเติม (storyboard sheet / keyframe)
  ต่อสายด้วย `canvas_connect_nodes` + mention เป็น `@[label](node:id)` —
  **manhwa ต่อสายเฉพาะเมื่อ user สั่งใช้เป็น position guide เท่านั้น (ดูข้อ 7 / Rev 3 #1)**.
- ⏱ **prompt ต้อง align กับ duration ของช็อต**: เขียนเผื่อ timeline (0s → กลาง → เฟรมท้าย) ;
  บทพูดพูดจบทันวินาทีที่มี (ไทย ~7 พยางค์/วิ) ; action เกินเวลา = แตกช็อต.
- ผลลัพธ์: ทุกช็อตมี **video node พร้อม prompt เต็มอยู่บนบอร์ด** — user เปิดบอร์ด
  อ่าน/แก้ในเว็บได้ตรงตัว node เลย (นี่คือ artifact ของ Gate 4).

### 🚦 10) GATE 4 — CONFIRM VIDEO NODES
- user ไล่ดู video node ทุกตัวบนบอร์ด (prompt แก้ได้ฟรี — บนเว็บหรือสั่ง agent แก้) →
  confirm → ถามโหมด: **ทีละช็อต OK-gate** (default) หรือ **ต่อเนื่อง** (หยุดเฉพาะ QC fail).

### 11) GEN VIDEOS — ทีละช็อตเสมอ (ยิง node ที่ confirm แล้ว)
- ต่อช็อต: วิเคราะห์วิดีโอช็อตก่อนทั้งคลิป (ffmpeg grid) → ตำแหน่งจริงต่างจากแผน →
  แก้ POSITION LOCK ใน text ของ node ก่อน → **`run_gen_node(<SBxx video node>)`** →
  `wait_for_run` → QC gate (error_kind + วิเคราะห์ทั้งคลิป) → PASS: โหมดทีละช็อต = รอ OK /
  โหมดต่อเนื่อง = ไปต่อ ; FAIL: regen (run_gen_node ซ้ำ, ≤4) → ครบเพดานรายงาน user.
- 📌 โปรเจกต์ที่ทำงานบน `studio_shots` จริง + user ขอแก้แค่ "ช่วง" ของช็อต ("ช่วง 4 วิ
  ทำใหม่เป็น insert") → gen วิดีโอปกติเฉพาะ action นั้น (≥4s — platform clamp; ผ่าน ask_user
  gate ก่อน) → `add_shot_asset(shot_id, type:"insert", run_id, metadata:{note,
  insert_at_seconds, duration_seconds, replaces_asset_id?})` — ⛔ ไม่ใช่ full take:
  ห้าม select/ห้ามแตะ `selected_video_asset_id`. (ขั้นตอนเต็ม: /siamshort-b2b-shot-continuity ข้อ 6.5)
- จบเรื่อง: สรุปวิดีโอเรียงตาม frame + เสนอ `save_to_mix_stage` / ย้ายเข้า movie pipeline
  (`/siamshort-b2b-auto-movie`) / ตัดต่อภายนอก.

---

## ⛔ GEN QC GATE — เช็คทุก gen ก่อนไปขั้นถัดไป (pipeline หยุดเมื่อ dependency พัง)

ทุกครั้งหลัง `wait_for_run` ให้อ่านผลก่อนทำอะไรต่อ:

1. **`status:"completed"` + มี outputs** → ผ่าน gate → ใช้ต่อได้.
2. **`status:"failed"/"cancelled"`** → อ่าน `error_kind` + `suggested_action` ที่ MCP
   แนบมาให้ แล้วทำตาม:
   | error_kind | ทำอะไร |
   |---|---|
   | `moderation` | ❌ ห้าม regen เดิมๆ — เอา ref คนจริงออก / ลดคำรุนแรง แล้วค่อย regen ; แจ้ง user |
   | `timeout` | regen เดิมได้ 1 ครั้ง ; ซ้ำอีก → ใช้ GROUP id (LB หา provider ว่างเอง) หรือลด duration/res |
   | `invalid_input` | แก้ ratio/resolution/duration ให้ตรงสเปกก่อน regen (ห้าม retry เดิม) |
   | `provider_error` / `unknown` | regen 1 ครั้ง ; ซ้ำ → เปลี่ยนโมเดล + แจ้ง user |
   แต้มคืนอัตโนมัติทุกกรณี — ความเสียหายคือเวลา ไม่ใช่เงิน.
3. **`completed` แต่ outputs ว่าง** → MCP จะติด `suggested_action` เตือน — ถือว่า fail, regen.
4. ⛔ **DEPENDENCY RULE — ของพังห้ามไหลลงท่อ:**
   - entity image fail → **หยุด** storyboard ทุกช็อตที่มีตัวนั้น จนกว่า entity ผ่าน
   - storyboard ช็อต i fail → **ห้าม gen วิดีโอช็อต i** (และห้ามใช้เป็น ref ช็อต i+1)
   - วิดีโอช็อต i fail เกินเพดาน regen → ใช้ตัวดีสุดที่มี + แจ้ง user ; ช็อต i+1 อ้าง
     position จาก "ตัวที่เลือกใช้จริง" ไม่ใช่ตัวที่ตั้งใจ
   - ref node ที่ URL ตาย/หมดอายุ = dependency fail เหมือนกัน — ต่ออายุก่อน ห้ามยิงทั้งที่รู้ว่า ref เสีย
5. เพดาน regen: รูป ≤3 · วิดีโอ ≤4 ต่อชิ้น — ครบแล้วรายงาน user พร้อม error ล่าสุด อย่าวนเงียบๆ.

## กติกาความต่อเนื่อง (สรุปสั้น — เต็มดู /siamshort-b2b-shot-continuity)

- **STYLE LOCK แปะทุก prompt คำต่อคำ** — เปลี่ยนได้แค่ ฉาก/เวลา/แสง.
- **identity จาก entity รูปเดียวกันเสมอ** — ref รูป entity ทุกช็อตที่ตัวนั้นปรากฏ ห้ามให้
  โมเดล "จำเอง".
- **1 ช็อต = 1 gen** ; ทีละช็อต ; OK-gate ทุกวิดีโอ ; regen ≤4 แล้วเอาตัวดีสุด.
- **วิเคราะห์ทั้งคลิปก่อนล็อกช็อตถัดไป** — ตำแหน่ง/แสงจริง ไม่ใช่ที่ตั้งใจ.
- ✅ **Virtual assets อัตโนมัติแล้ว**: BytePlus register ref รูป+คลิป; xskill register VA
เฉพาะรูป ส่วนคลิปส่ง signed `video_files`; เสียงส่ง `audio_files` ไม่ใช่ VA. MCP ใช้ flow
เดียวกับปุ่ม Run บนเว็บ (Active → asset token /
  Failed(faceless) → raw fallback) ; ถ้าได้ error "still being registered" = ระบบกำลัง
  register อยู่ รอ ~30 วิแล้วเรียก tool เดิมซ้ำ (dedup ทำให้ retry ถูก). ref ratio นอกช่วง 0.4–2.5 = MCP
  letterbox (แถบเทาเข้ม ไม่ crop) ให้อัตโนมัติก่อน register — เหมือนเว็บทุกอย่าง.
- ref URL บน node เก่าหมดอายุ ~1 ชม. → resolver ฟ้อง = ขอใหม่ (`get_asset_url` /
  `get_run_status`) ก่อนใช้.
