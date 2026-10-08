---
name: siamshort-b2b-auto-movie
description: >-
  "GEE Loop" — กระบวนการมาตรฐาน end-to-end ทำหนังบนแพลตฟอร์ม Siamshort/GEE ผ่าน
  siamshort MCP: จากบท/ไอเดีย → โปรเจกต์+world → cast/sets/props (+รูป) →
  sequences → shots (plot+tag+prompt) → gen วิดีโอทีละช็อต (human-in-the-loop)
  โดยสมมุติบทบาทเป็นทีมกำกับหนังระดับโลก. ใช้เมื่อผู้ใช้พิมพ์
  "/siamshort-b2b-auto-movie", "ทำหนังบน GEE/Siamshort", "เริ่ม Loop บน siamshort",
  "สร้างหนัง end to end", "auto movie", หรืออ้างถึง GEE Loop — และเมื่อ user ขอ
  งานชิ้นส่วนของ Loop ในโปรเจกต์: "gen/ทำ storyboard" (ช็อตเดียวหรือทุกช็อต —
  default = SHEET multi-panel ดูข้อ 10b), "เขียน prompt ช็อต", "gen รูป/วิดีโอช็อต",
  "ตั้ง cover", "เช็คสถานะโปรเจกต์แล้วทำต่อ".
  คุม 2 เฟส: PHASE A pre-production (บท → ถาม pacing → สร้าง project+world →
  cast/sets/props + gen รูป → sequences + shots ครบ plot/duration/transition →
  TAG entity ทุกช็อต → prompt ทุกช็อต → สรุปให้ user confirm) และ PHASE B
  video-gen loop (gen 1 ช็อต → วิเคราะห์คลิป → รอ user OK → ช็อตถัดไป ห้ามข้าม
  gate). Do NOT trigger เมื่อ: ใช้แพลตฟอร์ม Fable เดิม (ใช้ /siamshort_auto_loop),
  แค่แปลงนิยาย→บท (ใช้ /siamshort-b2b-script-from-novel), หรือเล่นบน idea-board
  canvas อย่างเดียว (ใช้ canvas_* tools ตรงๆ).
---

# 🎬 Siamshort Auto-Movie — GEE Loop (end-to-end ผ่าน siamshort MCP)

กระบวนการเดียวกับ "Loop" ของ p'ton แต่ **ปรับให้ตรงกับแพลตฟอร์ม Siamshort/GEE ของเราเอง**
(siamshort MCP server) — จาก **บท → project+world → assets → sequences/shots → gen วิดีโอ
ทีละช็อต (human-in-the-loop)**.

> **สมมุติบทบาท = ทีมกำกับหนังระดับโลก** ตลอดกระบวนการ (Director / Story / Visual /
> Motion / Sound — spawn subagent ช่วยได้ แต่ห้ามข้าม OK-gate).
> ⭐ **คลังเทคนิค anti-slop เต็ม (ฉบับ GEE) = `reference/master-prompt-techniques.md` ของสกิลนี้
> — อ่านก่อนเขียน prompt storyboard/วิดีโอทุกครั้ง** (scene anchor อสมมาตร · CAM/BG+POSITION LOCK ·
> ข้อจำกัด Seedance §6 · continuity §9). ใช้คู่ `siamshort-b2b-anti-plastic` ·
> `siamshort-b2b-physics-guide` · `/siamshort-b2b-shot-continuity`.

---

## 📖 VOCABULARY MAP — เทียบศัพท์ Fable (สกิลเก่า) ↔ GEE (แพลตฟอร์มเรา)

| Fable (สกิลเก่า) | GEE / siamshort MCP | หมายเหตุ |
|---|---|---|
| character | **Cast** = entity_type `character` | `create_entity(entity_type:"character")` |
| scene (สถานที่) | **Set** = entity_type `scene` | `create_entity(entity_type:"scene")` |
| item | **Prop** = entity_type `item` | `create_entity(entity_type:"item")` |
| chapter | **Sequence** = `create_chapter` | 1 sequence มี `content` (เนื้อเรื่องท่อนนั้น) |
| **storybox** | **Shot** = `create_shot` | 1 shot = 1 beat = `plot` + `prompt` + `duration_seconds` + วิดีโอ 1 ตัว. Sequence 1 อัน มีหลาย shot |
| seedancePrompt | `studio_shots.prompt` | เขียนผ่าน `update_shot(prompt:...)` หรือ AI เขียนด้วย `generate_shot_prompt` |
| `update_shot(characterIds/sceneIds/itemIds)` | `character_ids` / `scene_id` / `item_ids` | ⭐ ของเรา **`create_shot` รับ tag ได้เลย** (update_shot ก็ได้) — scene ผูกได้ **1 ตัว** ต่อช็อต |
| mention `@char #scene $item` ในข้อความ | **mention_token** จาก `get_project` เช่น `@[โรส](cast:uuid)` `#[คลับ](set:uuid)` `$[มีด](prop:uuid)` | เซิร์ฟเวอร์แปลงเป็น syntax ของแต่ละโมเดลเอง — ❌ ห้ามเขียน `@image_file_N`/`【@图片N】` เอง |
| `regen_shot_video` + `poll_video_byteplus` | `generate_shot_video` + `wait_for_run` / `get_run_status` | ผลลัพธ์ = mp4 + signed URL (หมดอายุ ~1 ชม. → ต่ออายุด้วย `get_asset_url`) |
| `%ref` / `capture_video_frame` / `trim_reference_video` | ❌ **ยังไม่มีใน GEE MCP** | ใช้แทนด้วย: draft image (`generate_shot_image`) เป็น visual anchor + `transition_to_next:"extend"` + mention/tag ; frame-ref จะตามมาเฟสหน้า |
| storyboard-sheet | ✅ **ทำได้ใน Loop แล้ว** (2026-07-17) | `generate_shot_storyboard_sheet` — รูปเดียว multi-panel ต่อช็อต, ดูข้อ A10b |
| manhwa | ❌ ไม่ gen ใน Loop นี้ | เป็นของ canvas family ; register ผ่าน `add_shot_asset(type:"manhwa")` เมื่อ user ทำมาจากฝั่งบอร์ด |

**ฟิลด์ภายใน 1 storybox ↔ 1 shot (GEE `studio_shots`):**

| ฟิลด์ Fable storybox | ฟิลด์ GEE | เขียน/สร้างด้วย |
|---|---|---|
| ข้อความ storybox / `presetText` (action+timing+กล้อง) | `plot` | `create_shot` / `update_shot` |
| `seedancePrompt` | `prompt` | `update_shot` / `generate_shot_prompt` |
| **selected single-frame shot image/keyframe** (legacy `image_path`; **ไม่ใช่ storyboard sheet**) | `image_path` = **draft still ที่เลือกอยู่** + ประวัติใน `studio_shot_assets` ✅ | ใช้เฉพาะเมื่อ user ขอเฟรมเดียว/keyframe/draft still: `generate_shot_image(shot_id, user_explicitly_requested_single_frame:true)` → `wait_for_run` → **`add_shot_asset(shot_id, type:"storyboard", run_id, select:true)`** (pointer 0 แต้ม; เก็บ variant และ sync `image_path`). คำว่า “storyboard” เฉย ๆ ต้องใช้ `generate_shot_storyboard_sheet` ตามข้อ 10b |
| **manhwa image** | **`studio_shot_assets`** (type `manhwa`) ✅ | gen สไตล์การ์ตูนด้วย `canvas_generate_image` → `wait_for_run` → **`add_shot_asset(shot_id, type:"manhwa", run_id)`** (0 แต้ม — pointer ไม่ก๊อปไฟล์ ; `select:true` = ตั้งเป็นตัวโชว์ของช็อต) → ดู/สลับด้วย `list_shot_assets` / `select_shot_asset`. ซ่อนตัวที่ไม่ใช้ด้วย `remove_shot_asset` หลังเลือกตัวแทนแล้ว — ซ่อนเฉพาะ pointer, ไม่ลบ output/run/storage และไม่ refund. ⛔ **ห้าม auto-แนบเป็น video-gen ref** (Rev 3 #1 — manhwa = display/mention เท่านั้น): จะใช้เป็น ref จริงต่อเมื่อ **user สั่งเอง** ค่อย `list_promotable_references` → `save_to_mix_stage` → `attach_shot_mix_stage_refs` (additive) แยกต่างหาก. ใช้ `set_shot_mix_stage_refs` เฉพาะ user สั่ง replace/clear. ❌ เลิกเขียน manhwa ผ่าน naming-convention `manhwa_*` บน Mix Stage แล้ว |
| วิดีโอ / takes | `video_path` + ประวัติทุก take ใน ai_runs (`list_runs(studio_shot_id)`) ; **เลือก take = เว็บ UI เท่านั้น** | `generate_shot_video` |
| **insert clip** (patch เฉพาะช่วงของช็อต) | `studio_shot_assets` (type `insert` — วิดีโอเท่านั้น) | gen ปกติ ≥4s → **`add_shot_asset(shot_id, type:"insert", run_id, metadata:{note, insert_at_seconds, duration_seconds, replaces_asset_id?})`** — ⛔ ไม่ใช่ full take: ห้าม select/ห้ามแตะ `selected_video_asset_id` |
| duration | `duration_seconds` | `create_shot` / `update_shot` |
| — (Fable ไม่มี) | `transition_to_next` (`extend`/`jump`) — hint ต่อเนื่องเฟรมข้ามช็อต | `create_shot` / `update_shot` |

> 📌 **อ่านสถานะช็อตให้ถูก (อย่าทำให้ user สับสน):** storyboard ทุกแบบ (draft still
> และ sheet) compose จาก **`plot`** — ช็อตที่มี plot = **gen storyboard ได้ทันที**.
> ฟิลด์ `prompt` ว่าง = ขาดเฉพาะ **วิดีโอ** เท่านั้น. เวลารายงานสถานะให้แยกเสมอ:
> "plot ครบ → storyboard พร้อม gen · prompt ยังว่าง → ต้องเขียนก่อน gen วิดีโอ"
> — ❌ ห้ามพูดรวมว่า "no prompts, no storyboards" ราวกับ storyboard ถูกบล็อกไปด้วย.

---

## 0) กฎเปิดสกิล (ทำก่อนเสมอ)

1. **สวมบททีมกำกับระดับโลก** — ทุก decision (มุมกล้อง / blocking / แสง / จังหวะ) คิดแบบมืออาชีพ.
2. **อ่าน `reference/gee-platform-map.md` ของสกิลนี้** — พารามิเตอร์จริง + ข้อจำกัด + gotchas
   ของแพลตฟอร์มเรา (ratio ที่ระบบรับ, โมเดลที่พิสูจน์แล้ว, กติกา points).
   เทคนิค prompt เชิง craft → `reference/master-prompt-techniques.md` (ฉบับ GEE ในสกิลนี้).
3. ⛔ **กฎเหล็ก — ทุกการ gen (รูป/prompt/วิดีโอ) ผ่าน siamshort MCP เท่านั้น**
   (`generate_entity_image` · `generate_shot_image` · `generate_shot_prompt` ·
   `generate_shot_video` · `start_video_prompt_chain`). ❌ ห้ามยิง provider ตรง /
   ห้ามใช้สกิล gen รูปภายนอก — รูปนอก MCP ไม่ลงทะเบียนในโปรเจกต์ = mention/tag/continuity พัง.
4. ⛔⛔ **กฎเหล็ก TAG — ทุก shot ต้องผูก entity จริง ไม่ใช่แค่พิมพ์ชื่อ:**
   ตอน `create_shot`/`create_shots_batch` ใส่ `character_ids:[...]`, `scene_id:"..."`,
   `item_ids:[...]` ให้ครบทุกช็อต (หรือ `update_shot` ตามหลัง). Tag = ref รูป ambient
   ตอน gen วิดีโอ ; mention_token ใน prompt = ref แบบระบุตัวชัด. **ใช้ทั้งคู่**:
   tag ทุกตัวที่อยู่ในช็อต + mention เฉพาะตัวที่ต้องการให้ model bind ชัดๆ.
5. **เช็ค `get_balance` ก่อนเริ่ม PHASE ใหญ่** — gen ตัดแต้มตอนเริ่ม (fail คืนอัตโนมัติ).
   บอก user คร่าวๆ ว่าแผนนี้กินประมาณกี่แต้ม (ดูราคา `list_models` + ตารางใน reference).
6. **ทุก id สำคัญ (project/chapter/shot/entity/run) จดไว้ในบทสนทนา** — tool อื่นต้องใช้ต่อ.
7. ⛔⛔ **SURFACE LOCK — Loop นี้ทำงานบน project surface เท่านั้น** (entities / chapters /
   shots / mix stage). ❌ **ห้ามใช้ idea board / `canvas_*` ในแชทนี้ทุกกรณี** — งาน canvas
   เป็นของแชท/agent เฉพาะของ idea board (คนละส่วนกัน). user ขอทำงานบนบอร์ด → แจ้งว่า
   เป็นคนละพื้นที่ ให้ใช้แชท/หน้า idea board แทน. ผลงานทุกชิ้นของ Loop ต้องลงจบบน
   project surface (`generate_entity_image` / `set_entity_image` / `save_to_mix_stage` /
   `add_shot_asset`) — ❌ ห้ามส่งงานจบด้วย "ไปดูบนบอร์ด".

---

## PHASE A — PRE-PRODUCTION (บท → project → assets → shots ครบ prompt+tag)

1. **รับบท/ไอเดีย → บทถ่ายทำละเอียด** — ถ้ามีนิยาย/บทยาว ใช้ `/siamshort-b2b-script-from-novel`
   ก่อน (ได้ △-format = source of truth). ไอเดียสั้น → ทีมกำกับ (subagent 5 role) ขยายเอง
   แล้วให้ user เห็นก่อน.
2. **ถาม PACING 3 ระดับ (รวดเร็ว/ปานกลาง/ยาว)** — เหมือน Loop เดิม: บทเท่ากัน ต่างที่วิธีแตก
   เป็น shot (⚡ น้อยสุด/ตัดฉับ · ▶ 1 shot = 1 beat · 🎬 แตก 1 action หลายมุม). เสนอ default
   ตามแนวเรื่อง แต่ **ให้ user ตัดสิน**.
3. **เสนอ graphic style 5 แบบ** จากบท → user เลือก → ยึดทั้งเรื่อง (ปรับแค่ฉาก/เวลา/แสง).
4. **สร้างโปรเจกต์:** `create_project(title, logline, genre, ratio, synopsis, visual_rules,
   era, atmosphere, film_style, ...)` — ⭐ **`synopsis` ต้องแน่น** (หลาย AI action ฝั่งเซิร์ฟเวอร์
   gate ด้วย world synopsis) ; `visual_rules` = graphic style + บล็อกข้อห้ามที่เลือก ;
   `ratio` ของโปรเจกต์ = ratio หลักของหนัง (แนวตั้ง = `9:16`).
5. **สร้าง Cast / Sets / Props:** `create_entity` ทีละตัว — `description` = **visual DNA
   ละเอียด ของ subject ล้วนๆ** (ภาษาอังกฤษ) เพราะเป็น prompt ตรงของรูป. 🎯 **CLEAN REF:**
   Cast = ตัวละครอย่างเดียว ❌ห้ามใส่ฉากหลัง/คนอื่นใน description · Prop = วัตถุเดี่ยว
   ❌ไม่มีมือ/โต๊ะ/ฉาก · Set = สถานที่ไม่มีคน — ระบบ gen พื้นหลัง clean reference /
   พื้นขาว studio / depopulated ให้เองอยู่แล้ว การใส่ฉากใน description จะตีกับ directive
   ของระบบ. ตอน QC: cast มีฉาก/คนแทรก · prop มีมือ/ฉาก · set มีคน = FAIL → regen.
   - Set = **eye-level WIDE establishing เฟรมเดียว** เห็นทุกโซน + anchor อสมมาตรชัด
     (ใส่ใน description) — ❌ ไม่ใช่ turnaround grid.
   - จากนั้น **gen รูปทุกตัว**: `generate_entity_image(entity_id)` → `wait_for_run` จนครบ.
     ยิงพร้อมกันได้ (ระบบมี queue ให้เอง — สถานะ `queued` = ปกติ รอต่อ). รูปไม่ผ่าน → แก้
     `update_entity(description)` แล้ว gen ใหม่ (≤3 ครั้ง/ตัว แล้วเอาตัวดีสุด).
   - 🖼 **regen ด้วยรูปอ้างอิง (identity ref):**
     `set_entity_gen_references(entity_id, [{imageUrl:"<storage path>", label:"..."}])`
     ก่อน แล้วค่อย `generate_entity_image(entity_id)` — ระบบใช้ ref เป็น identity anchor
     แรงสุดให้เองอัตโนมัติ ผลลง `image_path` ของ entity ตรงๆ (ref ติดถาวรจนกว่าจะ
     replace/clear ด้วย `references:[]`). ⭐ ทางนี้ทางเดียวสำหรับ ref หน้าตา/ลุค.
   - ♻️ **adopt รูป/วิดีโอที่มีอยู่แล้วเป็นตัว entity** (เช่น run เก่าที่สวยอยู่แล้ว):
     `set_entity_image(entity_id, run_id|asset_id|storage_path, target:"image"|"video")`
     — pointer 0 แต้ม ไม่ gen ใหม่ (`target:"video"` = `video_path` ของ Mix Stage).
   - 👁 **การ QC รูปด้วยตัวเอง — รู้ขีดจำกัดของสภาพแวดล้อม:**
     ❌ **ห้ามใช้ Read กับ URL เด็ดขาด** (Read = ไฟล์ local เท่านั้น — URL จะ fail เปล่าๆ).
     **`view_asset(run_id|asset_id|storage_path)` = ทางดูรูปอย่างเป็นทางการ** (0 แต้ม,
     ย่อรูปให้เอง): บน **Claude desktop** ใช้แล้วเห็นรูปจริง → QC เองได้เลย.
     บน **เว็บแชท (GLM)**: เรียก view_asset ได้แต่โมเดลอาจมองรูปไม่เห็น (ยืนยันแล้ว
     2026-07-16) — ถ้ามองไม่เห็น **ถาม user ให้ช่วย QC** ("รูปชุดนี้ผ่านไหม?" — รูปแสดง
     ในแชทให้ user อยู่แล้ว) ก่อนไปขั้นถัดไป. ❌ ห้ามหาทางอ้อมด้วย WebFetch/Bash/URL.
5b. 📎 **user แนบไฟล์ ref = ต้องใช้ — เลือกทางตาม "ref นี้ใช้ทำอะไร"** (ทุกทางเริ่มด้วย
   `upload_reference(file_path, workspace_id:<project.workspace_id>)`):
   - **ref หน้าตา/ลุคของ cast/set/prop** →
     `set_entity_gen_references(entity_id, [{imageUrl:"<storage path>"}])` →
     `generate_entity_image(entity_id)` — ผลลง entity ตรงๆ.
     ⭐ ทางนี้ทางเดียว — ❌ ห้ามอ้อมไป gen บน canvas (ผลจะไม่ลง entity + ผิด SURFACE LOCK ข้อ 7).
   - **ref composition/motion/sound ระดับช็อต** → ถ้าเป็นของเดิมให้ค้น exact match ด้วย
     `list_mix_stage_refs`; ถ้ายังไม่อยู่จึง `save_to_mix_stage(storage_path, source_type,
     reference_role)` → `attach_shot_mix_stage_refs` แบบ additive → ใส่ `mention_token`
     ที่คืนมาใน video prompt เมื่อเรียกชื่อ ref. ตอน gen ช็อต: **รูป → image_files
     (identity/composition/style) · คลิป → video_files (motion/จังหวะ) · เสียง →
     audio_files (voice/music/sound)** อัตโนมัติ. เลือกโมเดลที่รองรับ media นั้นและกำกับ
     ใน prompt ว่าต้องเอาคุณสมบัติใดจาก ref.
     VA parity กับ IdeaBoard: BytePlus register ทั้งรูป+วิดีโอ; xskill register VA เฉพาะรูป
     (วิดีโอส่ง signed `video_files` ตาม provider contract); เสียงส่ง `audio_files` ไม่ใช่ VA ;
     "still being registered" → รอ ~30 วิ เรียกซ้ำ.
     ⛔ ห้าม auto-promote/auto-attach; ถ้าค้นเจอหลายตัวต้องถาม user. ใช้
     `set_shot_mix_stage_refs` เฉพาะ user สั่ง replace/clear ทั้งชุด. storyboard/manhwa/
     Bible/Lookbook แบบหลาย panel เป็น general ref เท่านั้น; video/audio และ multi-panel
     image ห้ามเป็น Start/End Frame.
   - ❌ **อย่าเอารูป anchor ของ entity ไปซ้ำใน Mix Stage** — tag + mention entity
     ก็แนบรูปให้ตอน gen storyboard/วิดีโออยู่แล้ว (อย่าเสนอ user ด้วย). Mix Stage
     มีไว้สำหรับ ref ที่ **ไม่ใช่ตัว entity** เท่านั้น (composition/motion/สไตล์เฉพาะช็อต).

6. **สร้าง Sequences:** `create_chapter(project_id, title, summary, content,
   duration_seconds)` — `content` = เนื้อเรื่องท่อนนั้นเต็มๆ (เป็น context ให้ AI เขียน prompt).
7. **ลง Shots (= storybox เดิม):** `create_shots_batch(chapter_id, shots:[...])` ตามลำดับบท —
   ต่อช็อต: `title` · `plot` (action+มุมกล้อง+position ละเอียด — **ยังไม่ใส่ graphic style** ;
   ปริมาณ action พอดีวินาที: 5 วิ = 1 จังหวะ, 10–15 วิ = 2–3 จังหวะ) ·
   `duration_seconds` (**4–15 วิ/ช็อต เท่านั้น — ผลรวมทุกช็อต ≈ target ของหนัง**;
   target 60 วิ → 6–10 ช็อต) · `transition_to_next` (`extend` = เฟรมท้ายต่อเนื่องไปช็อตถัดไป /
   `jump` = ตัดฉาก) · ⭐ **tag `character_ids` / `scene_id` / `item_ids` ให้ครบตั้งแต่ตอนสร้าง**.
   - **เปิดทุก location ใหม่ด้วย ESTABLISHING SHOT** (ไม่มีคน บอกที่+เวลา).
   - ⚠️ **ลำดับช็อตถูกกำหนดตอนสร้าง** — MCP ยังไม่มี tool แทรก/สลับลำดับ → **วางแผนให้จบ
     ก่อนค่อย create**. ตกช็อต = เพิ่มท้าย sequence ได้อย่างเดียว (แล้วเล่าตามบทตอน gen แทน).
   - ช็อตมีแรงตั้งต้น (ของตก/แตก/สาด/ล้ม/ชน) → ขยายด้วย `siamshort-b2b-physics-guide` ก่อนเขียน plot.
8. **เขียน prompt ทุกช็อต — 2 ทาง (เลือก/ผสม):**
   - **ทาง AI (แนะนำเริ่มต้น):** `start_video_prompt_chain(project_id)` — ระบบไล่เขียน
     prompt ให้ทุกช็อตที่มี plot แบบ **ต่อเนื่องช็อตต่อช็อต** ฝั่งเซิร์ฟเวอร์ (ปิดจอได้) →
     poll `get_chain_job_status(project_id)` จน completed แล้ว review ทีละช็อต.
     ⚠️ chain มีได้ 1 ตัว/โปรเจกต์ ; ต้องรอ n8n cron หยิบ (~5 นาที).
   - **ทางมือ (คุมเองเต็มที่):** `update_shot(shot_id, prompt:"...")` — ใส่
     **mention_token** จาก `get_project` (`@[ชื่อ](cast:id)` ฯลฯ) ตรงตำแหน่งที่ตัวละคร/
     ฉาก/พร็อพปรากฏ + scene-lock + position-lock + anti-slop ตาม MASTER.
     เซิร์ฟเวอร์แปลง token → ref รูป + syntax ต่อโมเดลเองทั้งหมด.
     ✍️ **เขียนทีละช็อตตามลำดับเรื่องเสมอ ห้าม batch** — video prompt ของจริงยาวมาก:
     อ่าน plot + เฟรมท้ายช็อต i-1 → เขียนช็อต i จบลึก → `update_shot` ทันที → ค่อยช็อต
     i+1. เขียนขนานหลายช็อต = prompt ตื้น continuity หลุด (chain ฝั่งเซิร์ฟเวอร์ก็ไล่
     ทีละช็อตด้วยเหตุผลเดียวกัน).
9. **DOUBLE-CHECK กับบท** — `get_project` ดึงทั้งหมดมาตรวจ: ครบทุก beat? tag ครบทุกช็อต?
   prompt ตรง plot? → **สรุปภาพรวมให้ user** (กี่ sequence · กี่ shot · กี่ตัวละคร · เรื่องย่อ
   ต่อช็อต · แต้มที่จะใช้ต่อวิดีโอ) → **รอ user confirm**. user ขอแก้ → ตรวจกับบททุกครั้ง ;
   ถ้าแก้แล้วไม่ตรงบท → เตือนก่อน.
10. **(optional แต่ช่วยมาก) gen storyboard ช็อตสำคัญ ให้ user เห็นทิศทางก่อนเผาแต้มวิดีโอ.
    จบ PHASE A.**
    - ⭐ **"storyboard" ใน Loop นี้ default = SHEET multi-panel ตามข้อ 10b** (user ruling
      2026-07-17) — user พูดว่า "gen storyboard" เฉยๆ ก็หมายถึง sheet.
      draft still เฟรมเดียว (`generate_shot_image(shot_id)` — plot compose ฝั่งเซิร์ฟเวอร์
      + portrait จาก tag) ใช้เมื่อ user ระบุ "เฟรมเดียว/draft still" หรือ agent ต้องการ
      anchor เร็วราคาถูกก่อน gen วิดีโอ (บอก user ว่าเป็น draft ไม่ใช่ sheet).
    - ⚠️ **ช็อตที่มี storyboard อยู่แล้ว (image_path ไม่ว่าง / `list_shot_assets` มี
      type storyboard) → ถาม user ก่อน gen ใหม่เสมอ** (บนเว็บใช้ ask_user ; บน
      desktop ถามในแชท) — 3 ตัวเลือก:
      ① **เพิ่มเป็น variant** → gen แล้ว `add_shot_asset(shot_id, type:"storyboard",
      run_id)` (ไม่ select — ตัวเดิมยังโชว์ สลับได้ใน UI) ·
      ② **แทนตัวที่เลือกอยู่** → gen แล้ว `add_shot_asset(..., select:true)`
      (sync `image_path`) · ③ **เก็บของเดิม ไม่ gen** (0 แต้ม).
      ห้ามตัดสินแทน user แม้เหตุผลดี (เช่น ref ตัวละครเพิ่งอัปเดต) — บอกเหตุผล
      แล้วให้ user เลือก.
10b. 🎞 **Storyboard SHEET ต่อช็อต (รูปเดียว multi-panel — user ruling 2026-07-16):**
    เมื่อ user ขอ "storyboard ของช็อตนี้" แบบแผ่นโปรดักชัน:
    1. เติมเทมเพลต **per-shot mode** จาก
       `../siamshort-b2b-board-movie/reference/storyboard-sheet-template.md`
       — `{STORY_ACTION}` = storybox ของช็อตทั้งก้อน · `{N}` = 4–8 ตาม duration ·
       `{SCENE_NO}` = `SEQ.SHOT` (เช่น `2.3`) · `{LANGUAGE}` ตามภาษาบทของโปรเจกต์ ·
       refs = entity ที่ tag บนช็อต (cast/set/prop ที่มีรูปแล้ว) **เรียงลำดับให้ตรง
       REF MAPPING** (`@image1` = ref ตัวแรกใน array).
    2. **Preflight ก่อนเสียแต้ม:** refs ทุกตัวต้องอยู่ในโปรเจกต์ปัจจุบันและมี
       `image_path` ที่ใช้ได้. ถ้า cast/set/prop ที่จำเป็นยังไม่มีรูป ให้หยุดและบอก
       prerequisite นั้นก่อน — ห้ามยิง call ที่รู้ว่าจะ `invalid_input` และห้ามข้าม
       identity ref แบบเงียบๆ.
    3. ⚠️ ช็อตมี storyboard อยู่แล้ว → ผ่าน **gate ข้อ 10** ก่อนเสมอ (variant / แทน / เก็บเดิม).
    4. `generate_shot_storyboard_sheet(shot_id, prompt:<เทมเพลตเต็ม>, refs:[...ordered],
       panel_count:4|6|8,
       image_size:"1:1"` (4 แถว) / `"3:4"` (5+ แถว)`)` → `wait_for_run` →
       `add_shot_asset(shot_id, type:"storyboard", run_id, select ตามที่ user เลือกใน gate)`.
    5. โชว์ผลให้ user (รูปขึ้นในแชทเอง) แล้วถาม QC ตามข้อ 👁 — ❌ ห้ามใช้ Read กับ URL.
    - หลายช็อตต้องทำ **ครบ lifecycle ทีละช็อตเท่านั้น**: generate → wait terminal →
      แก้ error/QC/gate → add asset → จึงเริ่มช็อตถัดไป. ห้ามยิง sheet แบบ parallel;
      error แรกให้หยุด batch ที่เหลือ แก้ตาม `error_kind`/`suggested_action` ก่อน.
    - ❌ ห้ามใช้ `generate_shot_image` ทำ sheet (draft still เฟรมเดียว แต่ง prompt เองไม่ได้)
      และ ❌ ห้ามอ้อม canvas (SURFACE LOCK ข้อ 0.7 ยังบังคับเต็ม).
10c. 🖼 **Cover / Poster ของโปรเจกต์ (2026-07-17 — มี tool ตรงแล้ว ห้ามอ้อม canvas):**
    เมื่อ user ขอ cover/poster:
    1. เขียน poster prompt เอง (key-art composition + สไตล์จาก `visual_rules`/world +
       **ใส่ text ชื่อเรื่องบนภาพได้ — ตั้งใจให้มีตรงนี้ที่เดียว**) ; refs = cast หลัก
       (เรียงลำดับตรงกับที่อ้างในพรอมป์ต — `@image1` = refs[0]).
    2. `generate_project_cover(project_id, prompt, refs, image_size ตาม ratio โปรเจกต์)`
       → `wait_for_run` → **โชว์ user ก่อนเสมอ** (tool ไม่ตั้ง cover เอง).
    3. user ชอบ → `set_project_cover(project_id, run_id)` (0 แต้ม) ; ไม่ชอบ →
       ปรับ prompt regen (≤3) หรือเก็บไว้เฉยๆ (รูปอยู่ใน library ไม่หาย).

---

## PHASE B — VIDEO-GEN LOOP (ทีละช็อต · human-in-the-loop · ห้ามข้าม gate)

> ⛔ **กฎเหล็ก: gen 1 ช็อต → STOP รอ user OK → ค่อยช็อตถัดไป. ห้าม batch.**

วนต่อช็อต N:

1. **วิเคราะห์ช็อตก่อนหน้า (N−1) ก่อนเสมอ** — เอา signed URL วิดีโอช็อตก่อน (จาก
   `get_run_status` / `list_runs` ; URL เก่าหมดอายุ → `get_asset_url(storage_path)`)
   → ดาวน์โหลด → **วิเคราะห์ทั้งคลิป** (ffmpeg grid 16 เฟรม `fps=1, tile=4x4` + เฟรมเต็ม
   จุดสำคัญ — อย่าเชื่อเฟรมท้ายอย่างเดียว) → อ่าน **position นักแสดงทุกคน + แสง + CONTINUITY
   NOTE** (เศษ/คราบ/ของล้ม ต้องอยู่ต่อช็อตถัดไป). *(ช็อตแรกของซีน → ใช้ draft image + Set ref แทน)*
2. **ล็อก prompt ช็อต N:** `update_shot(shot_id, prompt:...)` ตามผลวิเคราะห์ —
   scene-lock + position-lock + anti-slop + mention_token ครบ. เลี่ยงเปิด 0s ด้วย
   ตัวละคร/มุมเดียวกับ last frame ช็อตก่อน (กัน model ก๊อปเฟรมแปะ).
3. **gen วิดีโอ:** `generate_shot_video(shot_id, model, ratio, resolution, duration)` —
   ⭐ **ส่ง `ratio` + `resolution` + `duration` ครบทุกครั้ง ห้าม omit** (omit resolution =
   error `video_variant_not_priced` ที่หลอกว่าราคาขาด — จริงๆ คือพารามิเตอร์หาย).
   ค่าแนะนำอยู่ใน `reference/gee-platform-map.md` (โมเดล/ratio/แต้ม). ระบบใช้ prompt
   ที่เซฟไว้ + tag + mention อัตโนมัติ.
4. **poll:** `wait_for_run(run_id, timeout_s:55)` วนจน terminal (วิดีโอ = หลายนาที ;
   `queued` = รอคิว ปกติ). ได้ mp4 signed URL.
5. **วิเคราะห์คลิปเต็ม (เหมือนข้อ 1)** เช็ค: position ถูก · ไม่เพี้ยน/ไม่โคลน/ไม่แบ่งจอ ·
   ฉากตรง ref · ratio ถูก · ความยาวครบ.
6. **STOP → ส่งวิดีโอ + ผลวิเคราะห์ให้ user "โอเคไหม / แก้ไหม?"**
   - ❌ ไม่ผ่าน → หาสาเหตุ → แก้ prompt เฉพาะจุด → `generate_shot_video` ใหม่ (**≤4 ครั้ง/ช็อต**
     ครบแล้วเอาตัวดีสุด ให้ user เลือก) → ถามใหม่. **ห้ามไปช็อตถัดไปจนกว่า user OK.**
   - 🔧 **เสียแค่บางช่วง** ("ช่วง 4 วิตรงนี้ทำใหม่เป็น insert") → ใช้ insert flow แทน regen ทั้ง take:
     gen วิดีโอปกติเฉพาะ action นั้น (**ขั้นต่ำ 4s — platform clamp** ; ผ่าน ask_user gate ก่อน
     เหมือน gen วิดีโอทุกครั้ง) → `add_shot_asset(shot_id, type:"insert", run_id,
     metadata:{note, insert_at_seconds, duration_seconds, replaces_asset_id?})`.
     ⛔ insert ไม่ใช่ full take — **ห้าม select / ห้ามแตะ `selected_video_asset_id`** ของช็อต.
     (ขั้นตอนเต็ม: /siamshort-b2b-shot-continuity ข้อ 6.5)
7. **user OK → ช็อต N+1** (กลับข้อ 1). วนจนจบเรื่อง — ทุกช็อตมี OK-gate เสมอ.

---

## ✅ QUICK CHECKLIST ก่อน gen ทุกช็อต (ย่อ — เต็มดู MASTER + reference)

- [ ] shot นี้ **tag** `character_ids`/`scene_id`/`item_ids` ครบ (ดูจาก `get_project`)
- [ ] prompt มี **mention_token** ของตัวที่ต้อง bind ชัด (❌ ไม่เขียน syntax provider เอง)
- [ ] SCENE อ้าง **ABSOLUTE landmark** ของ Set ref (❌ ซ้าย/ขวาตามกล้อง ❌ มโนเฟอร์นิเจอร์)
- [ ] **CAM/BG + POSITION LOCK** ต่อเนื่องจากผลวิเคราะห์ช็อตก่อน ; ❌ สลับฝั่ง A↔B
- [ ] MEDIUM/MCU เป็นหลัก · กล้อง eye-level · ❌ overhead/CCTV
- [ ] [ANTI-CLONE] นับตัว "EXACTLY N" · [ANTI-SPLIT] ❌ แบ่งจอ/grid
- [ ] ตัวหนังสือบนภาพ = อังกฤษเท่านั้น · กันขาตั้งกล้อง/rig โผล่ (cameraOverride)
- [ ] แรงตั้งต้น → ลูกโซ่ฟิสิกส์ครบ + CONTINUITY NOTE ช็อตก่อนยังอยู่
- [ ] `transition_to_next` ตั้งถูก (extend/jump) · duration/ratio อยู่ในสเปกโมเดล
- [ ] แต้มพอ (`get_balance`) — วิดีโอ ~20-40 pt/ช็อต ตาม duration/resolution

---

## เครื่องมือ GEE MCP ที่สกิลนี้ใช้ (ครบชุด)

`list_projects` · `get_project` (มี mention_token) · `get_balance` · `list_models` ·
`list_runs` · `get_asset_url` · `create_project` · `update_world` · `set_project_cover` · `create_chapter` ·
`create_shot` / `create_shots_batch` · `update_shot` · `create_entity` / `update_entity` ·
`set_entity_gen_references` (identity refs ถาวรของ entity — 0 แต้ม) ·
`set_entity_image` (adopt asset ที่มีอยู่เป็นรูป/วิดีโอ entity — 0 แต้ม) ·
`add_shot_asset` / `select_shot_asset` / `remove_shot_asset` / `list_shot_assets` (shot-asset pointers 0 แต้ม — dev; remove = soft-hide, no delete/refund) ·
`generate_entity_image` · `generate_shot_image` · `generate_shot_prompt` ·
`generate_shot_storyboard_sheet` (sheet multi-panel ต่อช็อต — prompt เต็ม + refs เรียงลำดับ, ดูข้อ 10b) ·
`generate_project_cover` (poster/cover key art — prompt เต็ม + refs, โชว์ user แล้วค่อย `set_project_cover` — ดูข้อ 10c) ·
`generate_shot_video` · `get_run_status` · `wait_for_run` · `start_video_prompt_chain` ·
`get_chain_job_status` (⛔ `canvas_*` = บล็อกใน Loop นี้ — เป็นของแชท idea board, ดูข้อ 7)

> ยังไม่มีใน MCP (อย่าเรียก): capture_video_frame · trim_reference_video · %ref ·
> delete/reorder shot · upscale. ต้องใช้ = แจ้ง user ให้ทำในเว็บ UI แทน.
