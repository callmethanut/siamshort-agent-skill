---
name: siamshort-b2b-shot-continuity
description: >-
  Build a Seedance video drama on Siamshort/GEE ONE SHOT AT A TIME with locked
  character positioning and shot-to-shot continuity — the core Phase-B engine
  of /siamshort-b2b-auto-movie, usable standalone. Use when the user wants to gen
  video shot-by-shot via the siamshort MCP, says "ทำวิดีโอทีละช็อตบน GEE",
  "gen video ต่อเนื่อง", "position lock / ล็อกตำแหน่ง", "วิเคราะห์วิดีโอก่อนหน้าแล้ว
  ทำอันต่อไป", "ไม่ให้ slop", or "/siamshort-b2b-shot-continuity". The loop:
  lock prompt → generate_shot_video → wait_for_run → analyze the WHOLE clip →
  fix slop / read true positions → lock next shot. Do NOT trigger on the Fable
  platform (use /seedance-shot-continuity) or for one-off image gen.
---

# Siamshort Shot-Continuity Loop (GEE / siamshort MCP)

พอร์ตจาก `seedance-shot-continuity` (Fable) — **craft เหมือนเดิมทุกข้อ เปลี่ยนเฉพาะเครื่องมือ
ให้เป็นของ GEE**. ปั้นวิดีโอ **ทีละช็อต** ให้ตัวละคร **อยู่ตำแหน่งเดิมต่อเนื่อง** ไม่ slop/ไม่เพี้ยน.

> ศัพท์: Fable storybox = GEE **Shot** · chapter = **Sequence** · character/scene/item =
> **Cast/Set/Prop** (`entity_type: character|scene|item`). ดู VOCABULARY MAP ใน
> `/siamshort-b2b-auto-movie` + พารามิเตอร์จริงใน `siamshort-b2b-auto-movie/reference/gee-platform-map.md`.

---

## THE LOOP — ต่อช็อต N

1. **ล็อก prompt SB(N):** `update_shot(shot_id, prompt:...)` — scene-lock + position-lock +
   anti-slop guards (ด้านล่าง).
2. **Gen:** `generate_shot_video(shot_id, model:"seedance-fast" (GROUP — LB เลือก provider เอง), ratio:"9:16",
   resolution:"720p", duration:<ตาม shot ≤15>)` → ได้ `run_id`.
3. **Poll:** `wait_for_run(run_id, timeout_s:55)` วนจน terminal (~3–10 นาที ; `queued` = รอคิว
   ปกติ). ได้ mp4 signed URL (+ เก็บ `storage_path` — URL หมดอายุ ~1 ชม. → `get_asset_url`).
4. **โหลด + วิเคราะห์ "ทั้งคลิป"** (grid 16 เฟรม + เฟรมเต็มจุดสำคัญ — ดู ANALYSIS).
4b. **run-level fail ก่อนถึงเนื้อหา:** `status:"failed"` → อ่าน `error_kind`/`suggested_action`
   จาก MCP (moderation = แก้ ref/คำก่อน ห้าม retry เดิม · timeout = ซ้ำได้ 1 แล้วเปลี่ยนโมเดล ·
   invalid_input = แก้พารามิเตอร์ ·
   **`variant_not_priced` = พารามิเตอร์ขาด/ค่าไม่อยู่ใน catalog — ❌ อย่าเพิ่งเปลี่ยนโมเดล:**
   เช็คว่าส่ง `resolution` (480p/720p/1080p) + `ratio` (เช่น 9:16) **ครบทั้งคู่** แล้ว retry
   โมเดลเดิม — ส่วนใหญ่คือลืม resolution) ; แต้มคืนอัตโนมัติ. ผ่านแล้วค่อยตัดสินเนื้อหาข้อ 5.
   **`JWT expired` (ทุก tool ล้มพร้อมกัน) = token ของ turn นี้หมดอายุ (turn ยาวเกิน ~1 ชม.
   — เกิดกับ batch ยาวๆ):** ❌ **หยุดเรียก tool ทันที ห้าม retry รัวๆ** — งาน gen ที่สั่งไปแล้ว
   ยังรันต่อฝั่งแพลตฟอร์มปกติ. แจ้ง user สั้นๆ: "token หมดอายุ ส่งข้อความใหม่ 1 ครั้ง
   (เช่น 'ทำต่อ') แล้วผมจะเช็ค run ที่ค้างแล้วไปต่อจากเดิม".
   **กฎ retry ทั่วไป:** error เดิมซ้ำ 2 ครั้ง = เปลี่ยนวิธี ห้ามยิงซ้ำท่าเดิม ;
   (ระบบมี circuit breaker — fail ติดกันถึงเพดาน (~5) ทุก tool จะถูกบล็อกทั้ง turn
   → สรุปสถานการณ์ให้ user แล้วบอกวิธีไปต่อ).
5. **ตัดสิน PASS / FAIL:** ❌ FAIL ถ้า ตำแหน่งผิด/teleport/morph · เพี้ยน (หน้าเบี้ยว/อนาโตมีพัง) ·
   โคลน/ตัวซ้ำ · แตกจอ/split · ฉากผิด (ไม่ตรง Set ref) · ratio ผิด · ช่วงท้ายพัง.
6. **FAIL → ปรับ prompt เฉพาะจุด → gen ใหม่** (เพดาน **4 ครั้ง/ช็อต** ; ครบแล้วรับตัวดีสุด ไปต่อ).
7. **PASS → อ่านตำแหน่งจริงตอนจบ → ล็อกเข้า prompt SB(N+1)**.
8. **ประหยัดเวลา:** ระหว่าง SB(N) เรนเดอร์ เขียน prompt SB(N+1) ดักไว้ (แต่ **อย่า gen** จนกว่า
   จะวิเคราะห์ SB(N) จบ + user OK).

> ⚠️ แม้ช็อต FAIL และต้องยอมรับ ก็ **ต้องอ่านตำแหน่งจริง** เพื่อไม่ให้ช็อตถัดไปเพี้ยนตาม.

---

## 1) SCENE LOCK — ให้ "รูป ref" คุมฉาก ไม่ใช่ตัวอักษร ⭐ บทเรียนใหญ่สุด

- บน GEE: ฉาก = **Set entity** (`entity_type:"scene"`) ที่ **gen รูปแล้ว** (`image_path` มีค่า).
  วิธีให้รูปฉากไปถึงโมเดล: (1) **tag** `scene_id` บน shot (ambient ref อัตโนมัติ) และ/หรือ
  (2) **mention** `#[ชื่อSet](set:uuid)` (token จาก `get_project`) ใน prompt = bind ชัดกว่า.
- **ห้ามบรรยายฉากยาวเป็นตัวอักษร** — Seedance จะ "มโนฉากใหม่ตามคำ". ✅ สูตร:
  ```
  Location: ใช้ฉากเดิมตามรูปอ้างอิง #[ชื่อSet](set:uuid) เป๊ะทุกอย่าง —
  ❗ห้ามเปลี่ยนฉาก ห้ามสร้างสถานที่ใหม่ ห้ามแต่ง/เพิ่มของในฉาก.
  Use the SAME EXACT location as the referenced set image; do NOT reinvent or alter the set.
  ```
- ใส่เฉพาะ **เวลา/แสง/มู้ด** เป็นคำได้ (ค่ำ/แสงเทียน/golden hour) — บรรยากาศ ไม่ใช่สร้างสถานที่.
- ⚠️ Set ที่ยังไม่มีรูป → ระบบ **ข้าม ref เงียบๆ** (ไม่ fail) → เช็คก่อนเสมอด้วย `get_project`
  ว่า `image_path` ไม่ว่าง ; ว่าง → `generate_entity_image(set_id)` ให้เสร็จก่อน.

## 2) POSITION LOCK — ล็อกตำแหน่งตัวละคร (craft เดิมทุกข้อ)

- วาง **แผนผังตำแหน่งคงที่ทั้งซีน** แล้วยึดทุกช็อต ; ทุก prompt ใส่ **โซน + anchor** รายตัว.
- **อ่านตำแหน่งจาก "วิดีโอจริง"** ไม่ใช่เดา → เปิด SB(N+1) ด้วย `[POSITION LOCK ต่อจาก SB(N): ...]`
  ที่ตรงกับตอนจบจริง.
- ระยะไกลสองฝั่ง → **OTS deep-focus เฟรมเดียว** ❌ อย่า wide โชว์สองปลาย (แตกสองท่อน).
- ⭐ **[CAM/BG LOCK]** ทุกคัท: (1) กล้องหันทางไหน (2) หลังตัวละครแต่ละคนเห็น landmark อะไร —
  ไม่ปัก BG = Seedance ดูดตัวละครไปหา anchor เด่นสุด → ย้ายจุด/กลับด้าน.

## 3) REFERENCE จากช็อตก่อนหน้า — ทางเลือกบน GEE (⚠️ ต่างจาก Fable)

GEE MCP **ยังไม่มี** `capture_video_frame` / `trim_reference_video` / `%ref` — ใช้แทนด้วย:

| ต้องการ | วิธีบน GEE |
|---|---|
| ภาพต่อเนื่อง (เฟรมท้าย → เฟรมเปิดช็อตถัดไป) | ตั้ง `transition_to_next:"extend"` บนช็อตก่อน (`update_shot`) — pipeline ฝั่งแพลตฟอร์มดูแล + เขียน position/CAM-BG lock ใน prompt ให้ตรงผลวิเคราะห์ |
| มุมกล้อง/องค์ประกอบอ้างอิง | `generate_shot_image(shot_id)` = draft still ของช็อตนั้น (compose จาก plot + tag) เป็น visual anchor |
| identity ตัวละคร/ฉาก/พร็อพ | tag + mention_token (ระบบแนบ portrait ให้เอง) — แข็งแรงสุดบน GEE |
| ตัดเฟรม/ตัดคลิปเป็น ref แบบ Fable | ❌ ทำในเว็บ UI (Mix Stage) แล้วแจ้ง user ; หรือรอ MCP เฟสหน้า |

## 4) ANTI-SLOP GUARDS — ใส่ทุก prompt (เหมือน Fable เป๊ะ)

- **[ANTI-CLONE]** นับคนเป๊ะ: `EXACTLY N named characters, each appears EXACTLY once` +
  "ยืนคนเดียว = X ที่เหลือนั่ง" เมื่อมีตัวยืนเด่น.
- **[ANTI-SPLIT]** `ONE single continuous frame, ONE camera; ❌ห้ามแบ่งจอ/two-panel/grid แม้ wide.`
- **กล้อง eye-level ตัดฉับ** ❌ มุมสูง/overhead/crane/CCTV (Seedance เพี้ยน) ; มุมเท่เก็บไว้
  ช็อตเปิดตัว+ไคลแม็กซ์.
- **ตัวหนังสือบนภาพ = อังกฤษเท่านั้น** ; บทพูดไทยได้ (เป็นเสียง).
- กันขาตั้งกล้อง/rig โผล่: `FINAL FILM, floor clear, NO camera/tripod/DSLR/rig in frame`.

## 5) SHOT CONSTRUCTION (craft เดิม)

- เปิด 0s ด้วย **close-up** → ตัดฉับสลับ CU ↔ medium ↔ OTS ; เติมวินาทีด้วย emotion CU ;
  จบด้วยเฟรมที่อ่านตำแหน่งได้.
- ถ้าใช้ extend จากช็อตก่อน → 0s **ห้ามเริ่มมุมเดียวกับ last frame** (กันก๊อปเฟรมแปะ).
- บทพูด/VO: `บทพูด @X : "..."` / `VOICE OVER (เสียง @X ไทย): "..."`.
- ⚠️ GEE **แทรกช็อตคั่นกลางไม่ได้ผ่าน MCP** (ไม่มี sortOrder ทศนิยมแบบ Fable) — flashback/insert
  ต้องวางแผนตอนสร้าง shots ; ตกหล่น = ต่อท้าย sequence แล้วเล่าตามบทตอน gen.

## 6) ANALYSIS PROTOCOL — ดูทั้งคลิป ไม่ใช่แค่เฟรมท้าย (เหมือนเดิม)

```bash
curl -sL "<signed_url>" -o sbN.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 sbN.mp4  # 9:16 = 720x1280
ffmpeg -y -i sbN.mp4 -vf "fps=1,scale=240:-1,tile=4x4" -frames:v 1 sbN_grid.png
ffmpeg -y -ss <T> -i sbN.mp4 -frames:v 1 -q:v 2 sbN_t<T>.jpg   # เฟรมเต็มจุดสำคัญ
```
- ❗อย่าเชื่อเฟรมท้ายจาก `-sseof` เฟรมเดียว ; ❗อย่า hstack หน้าคนติดกัน (ภาพเบลนหลอกตา).
- เทียบฉากกับ **รูป Set จริง** (`get_project` → image_path → `get_asset_url`) ก่อนตัดสิน.
- เช็คลิสต์: ตำแหน่งถูก/นิ่ง · ไม่เพี้ยน · ไม่โคลน · ไม่แตกจอ · ฉากตรง ref · ratio ถูก · ช่วงท้ายโอเค.
- ⚠️ **โปรโตคอลนี้ (curl/ffmpeg) ใช้ได้เฉพาะที่มี Bash (Claude desktop).**
  บนเว็บแชท: agent เปิดคลิป/รูปเองไม่ได้ (❌ ห้ามใช้ Read กับ URL — fail เปล่าๆ) —
  วิดีโอแสดงในแชทให้ user เห็นแล้ว → **ให้ user ช่วยดูคลิปแล้วบอกผล** ตามเช็คลิสต์ข้างบน
  (ถามเจาะ: ตำแหน่งใคร-อยู่ไหนตอนจบ · มีโคลน/แตกจอไหม · ฉากตรง ref ไหม).
- 🖼 **รูปนิ่ง (storyboard/entity): `view_asset(run_id|asset_id|storage_path)` มีแล้ว**
  (0 แต้ม) — desktop เห็นรูปจริง QC เองได้ ; เว็บ (GLM) โมเดลอาจมองไม่เห็น →
  ถาม user แทน. **วิดีโอ**: view_asset ยังไม่รองรับ — desktop ใช้ curl/ffmpeg ตามบน,
  เว็บให้ user ดู.

## 6.5) INSERT — regen เฉพาะ "ช่วง" ของช็อต (ไม่ใช่ทั้ง take)

เมื่อ user บอกว่าเสียแค่บางช่วง ("ช่วง 4 วิตรงนี้ไม่ดี ทำใหม่เป็น insert") — **อย่า regen ทั้งช็อต**:
1. เขียน prompt ใหม่เฉพาะ action ของช่วงนั้น (scene/position/anti-slop lock เดิมใช้ครบ) →
   gen วิดีโอปกติ `generate_shot_video(...)` ความยาว = action นั้น **ขั้นต่ำ 4s (platform clamp)**.
   เป็นการ gen ที่เสียแต้ม → ต้องผ่าน **ask_user gate** ก่อนเหมือน gen วิดีโอทุกครั้ง.
2. `wait_for_run` → วิเคราะห์คลิปเต็มตามข้อ 6 ตามปกติ.
3. ลงทะเบียน: `add_shot_asset(shot_id, type:"insert", run_id, metadata:{note:"แก้อะไร",
   insert_at_seconds:<จุดเริ่มในช็อต>, duration_seconds:<ความยาวช่วง>, replaces_asset_id:<ตัวเดิม ถ้ามี>})`
   (pointer 0 แต้ม ; insert รับเฉพาะ**วิดีโอ**).
4. ⛔ **insert ไม่ใช่ full take — ห้าม select ให้มัน / ห้ามแตะ take หลักของช็อต
   (`selected_video_asset_id`)** ; UI โชว์เป็น chip แยก การตัดต่อจริงทำในเว็บ.
- ดู/ซ่อน: `list_shot_assets(shot_id, type:"insert")` / `remove_shot_asset` (soft-hide, ไม่ refund).
- ⚠️ คนละเรื่องกับ "แทรกช็อตคั่นกลาง sequence" (ข้อ 5) — อันนั้นคือลำดับช็อต,
  อันนี้คือ patch ช่วงเวลาภายในช็อตเดียว.

## 7) MCP CHEAT-SHEET (GEE / siamshort server)

| งาน | tool |
|---|---|
| ดู shots + prompt + tag ทั้งโปรเจกต์ (+mention_token) | `get_project(project_id)` |
| แก้ prompt/tag | `update_shot(shot_id, prompt, character_ids, scene_id, item_ids)` |
| gen วิดีโอ | `generate_shot_video(shot_id, model:"seedance-fast"/"seedance" (GROUP), ratio:"9:16", resolution:"720p", duration, generate_audio?)` |
| poll | `wait_for_run(run_id, timeout_s:55)` → completed + outputs[{signed_url, storage_path}] |
| ต่ออายุ URL | `get_asset_url(storage_path)` |
| ประวัติ run ของช็อต | `list_runs(studio_shot_id)` |
| ลงทะเบียน insert clip (patch เฉพาะช่วง — ดูข้อ 6.5) | `add_shot_asset(shot_id, type:"insert", run_id, metadata:{note, insert_at_seconds, duration_seconds, replaces_asset_id?})` — ⛔ ห้ามแตะ take หลัก |
| draft still เป็น anchor | `generate_shot_image(shot_id)` |
| เช็คแต้ม | `get_balance` (วิดีโอ ~20–40 pt ตาม duration/res ; fail คืนแต้มเอง) |

## QUICK CHECKLIST ต่อช็อต
- [ ] Set มีรูปแล้ว + tag `scene_id` + (ถ้าต้อง bind ชัด) mention `#[Set](set:id)` + scene-text สั้น
- [ ] `[POSITION LOCK ต่อจาก SB(N-1)]` ตรงตอนจบจริง + [CAM/BG LOCK] รายตัว
- [ ] เปิด close-up · ตัดฉับ · eye-level · [ANTI-CLONE] · [ANTI-SPLIT]
- [ ] บทพูดไทย / ตัวหนังสือบนภาพ EN / กัน tripod
- [ ] `transition_to_next` ตั้งถูก (extend/jump)
- [ ] gen → poll → วิเคราะห์ทั้งคลิป → PASS หรือ regen (≤4) → อ่านตำแหน่งจริง → ล็อกช็อตถัดไป
