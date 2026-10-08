---
name: siamshort-b2b-idea-board
description: >-
  คู่มือใช้ Idea Board (canvas) ของ Siamshort/GEE ผ่าน siamshort MCP — รู้จัก node
  ทุกกลุ่ม (Input / Gen / Output / Helper / Tools), การต่อ edge เป็น workflow,
  การ gen image/video บนบอร์ด, และการส่งผลลัพธ์เข้า movie pipeline (Mix Stage).
  ใช้เมื่อผู้ใช้อยากทำงานบน idea board / canvas: "สร้าง node", "ต่อ workflow บนบอร์ด",
  "gen รูปบน canvas", "ทำ mood board", "brainstorm บนบอร์ด", "/siamshort-b2b-idea-board".
  Do NOT trigger สำหรับงานหนังเต็มรูป (ใช้ /siamshort-b2b-auto-movie) หรือ gen วิดีโอ
  ทีละช็อตใน sequence (ใช้ /siamshort-b2b-shot-continuity).
---

# 🎨 Siamshort Idea Board — คู่มือ agent (siamshort MCP)

Idea Board = **realtime node canvas** ของโปรเจกต์: ผู้ใช้ (และ agent) วาง node ต่อสายเป็น
workflow แล้ว AI output ตกลงบนบอร์ด. คนที่เปิดบอร์ดอยู่ **เห็น node ที่ agent สร้างแบบสด**
(realtime) — ทำงานเป็น "เพื่อนร่วมบอร์ด" ได้เลย.

> โครงสร้าง: `canvas_boards` → `canvas_nodes` (type + data jsonb) → `canvas_edges`
> (ทิศ **output → input**; ลูกศรชี้เข้า node ผู้บริโภค). พารามิเตอร์แพลตฟอร์ม/ราคา:
> `siamshort-b2b-auto-movie/reference/gee-platform-map.md`.

> 🚧 **SURFACE SPLIT (2026-07-16):** สกิลนี้ = โลก canvas — สำหรับแชท/agent ของ
> idea board (ปัจจุบันใช้ผ่าน Claude desktop/cowork ; อนาคตมี canvas chat agent
> เฉพาะบนเว็บ). **แชทหนัง (auto-movie family) ถูกบล็อกไม่ให้ใช้ canvas** —
> อย่าดึงสกิลนี้เข้าไปทำงานใน movie Loop.

---

## 🔧 AGENT SCRATCH MODE — ใช้บอร์ดเป็น "เครื่องมือ" ไม่ใช่ปลายทาง

เมื่อ pipeline อื่น (เช่นงานหนังบน Claude desktop ที่ user สั่งให้ใช้บอร์ดช่วย gen)
ใช้ canvas เป็นแค่ engine:
1. ใช้บอร์ดชื่อ **`__agent_scratch__<project_id>`** — สร้างครั้งเดียว ใช้ซ้ำตลอด
   (อย่าสร้างบอร์ดใหม่ทุกงาน — บอร์ดผู้ใช้จะรก).
2. ผลลัพธ์ทุกชิ้น **ต้อง register กลับ project surface ทันที**:
   entity → `set_entity_image(entity_id, run_id)` · mix stage →
   `save_to_mix_stage(project_id, name, run_id)` · ช็อต →
   `add_shot_asset(shot_id, type, run_id)`.
3. **รายงานผลเป็นของบน project surface เสมอ** ("อัปเดตรูป cast แล้ว" / "เพิ่มเข้า
   Mix Stage แล้ว") — ❌ ห้ามจบงานด้วย "ไปดูบนบอร์ด".
4. อย่าลืม: identity ref ของ cast/set/prop ไม่ต้องใช้บอร์ดแล้ว —
   `set_entity_gen_references` → `generate_entity_image` ตรงๆ เร็วกว่าและลง entity เอง.

---

## 1) NODE GROUPS — node ทุกชนิดบนบอร์ด (และ MCP สร้างอะไรได้)

### 🟦 Input group — วัตถุดิบป้อน gen
| type | data สำคัญ | MCP สร้าง? |
|---|---|---|
| `prompt_text` | `text` (ข้อความ prompt) | ✅ `canvas_add_node(type:"prompt_text", text)` |
| `image` | `src` (https) + `storage_path` | ✅ (src ต้องเป็น URL — ❌ base64 ; ไฟล์แนบจาก user → `upload_reference(file_path, workspace_id:<project.workspace_id>)` ก่อน) |
| `video` | `src` + `poster` | ✅ (คลิปแนบจาก user → `upload_reference` ก่อน ; เป็น **motion ref** ของ gen_video ได้) |
| `audio` | `src` + `storage_path` | ✅ `canvas_add_node(type:"audio", src)` (ไฟล์แนบ → `upload_reference` ก่อน) |
| `asset_ref` | snapshot ของ entity ในโปรเจกต์ (Cast/Set/Prop/Mix Stage) | ✅ **`canvas_add_asset_ref(board_id, entity_id)`** — มาตรฐานเดียวกับ Insert → Asset reference บนเว็บ (การ์ดผูก entity + ระบบ re-sign URL ให้) ; ใช้เป็น ref_node_ids ได้เลย |
| `canvas_ref` | snapshot ของ node จากบอร์ดอื่น | ✅ `canvas_add_canvas_ref(board_id, source_board_id, source_node_id)` |
| `likeness_ref` | BytePlus virtual-asset (คนจริง) | ❌ (เว็บเท่านั้น + moderation) |

### 🟩 Gen group — node ประมวลผล (มีปุ่ม Generate)

⭐ **นโยบายเลือก node: งานที่มี ref/ตัวละคร/ฉาก = ใช้ ADVANCED เป็นหลัก**
(`canvas_add_advanced_gen` — mention ผูก ref ระบุตัว + วาง idle รอ confirm ได้) ;
simple เหมาะเฉพาะ gen ลอยๆ ไม่มี ref. **"gen storyboard" บนบอร์ด = advanced + template
เต็มจาก `siamshort-b2b-board-movie/reference/storyboard-sheet-template.md` เสมอ
(1 ซีน = 1 sheet) ⛔ ห้ามเขียน prompt คีย์เฟรมเดี่ยวเอง — เคยพังมาแล้ว.**

⭐ **นโยบายลำดับงาน (งานหลายช็อต/หลาย gen node):**
1. ✍️ **เขียน prompt ทีละช็อต/ซีน ห้าม batch** — เขียนตัว i ให้จบลึกครบ → วาง node
   ทันที → ค่อยขึ้นตัว i+1. เขียนขนานหลายตัวพร้อมกัน = prompt สั้นตื้นทุกตัว (พังมาแล้ว)
   — โดยเฉพาะ video prompt ที่ของจริงยาวมาก ต้อง analyze ทีละช็อต.
2. 🚦 **วาง idle ให้ครบชุด → คน confirm → ค่อย run**: advanced gen สร้าง node idle (ฟรี)
   — วางครบทุกช็อตแล้ว**หยุดรอ user confirm** ก่อนเรียก `run_gen_node` แม้แต่ตัวเดียว.
   ใช้ทั้งชุดรูป storyboard และชุดวิดีโอ ; pipeline เต็มรูปเดินตาม gate ของ
   `/siamshort-b2b-board-movie`.
| type | ตั้งค่าใน data | MCP |
|---|---|---|
| `gen_image` | model, ratio, resolution (1K/2K/4K), quality (Low/Med/High) | ✅ ผ่าน `canvas_generate_image` (สร้าง+ยิงให้ครบ) |
| `gen_video` | model, ratio, resolution, duration | ✅ ผ่าน `canvas_generate_video` |
| `gen_idea_text` | textPreset, variants | ⚠️ วางได้ แต่บนเว็บเป็น demo — run จริงผ่าน MCP ไม่ได้ |
| `gen_audio` | model seed-audio-1, voice, format | ✅ วางด้วย `canvas_add_node(type:"gen_audio")` + ต่อ prompt_text + `run_gen_node` → output_audio (TTS/เสียง) |
| `gen_image_advanced` / `gen_video_advanced` | `text` = marker string `@[label](node:id)` — editor ในตัว, ไม่อ่าน prompt_text ต้นทาง | ✅ `canvas_add_advanced_gen(kind, prompt)` — mention entity ด้วย token จาก get_project ได้เลย (tool สร้าง ref node + rewrite ให้) ; **สร้างแบบ idle ไม่ยิง** → คน confirm → `run_gen_node` |
| `video_upscale` | Topaz upscale (target 1080p/4K) | ❌ (เว็บเท่านั้น) |

- **Simple gen** อ่าน prompt จาก `prompt_text` ที่ต่อสายเข้า + อ่าน ref จาก media node
  ทุกตัวที่ต่อเข้า. **Advanced gen** อ่านจาก `data.text` ของตัวเอง (mention `node:` id).
- ⛔ กฎระบบ: gen node ต้องถูก persist **ก่อน** ยิง start-workflow (RLS) — MCP orchestrator
  จัดการให้แล้ว อย่าทำมือ.

### 🟨 Output group — ผลลัพธ์ AI (ระบบสร้าง ไม่สร้างมือ)
`output_image` / `output_video` / `output_text` — เกิดจาก gen พร้อม edge เส้นประ
(`kind:"generated"` — **ลบไม่ได้ โดยดีไซน์**). data: `runId`, `producedBy` (gen node id),
`variantIndex`, `src`, `status (running|done|error)`, `promotedTo[]`.
❌ **ห้าม agent สร้าง/แก้ output node เอง** นอก orchestrator — `canvas_generate_*` +
`wait_for_run` เติมผลให้อัตโนมัติ.

### ⬜ Helper group — จัดบอร์ด ไม่เกี่ยว gen
| type | ใช้ทำอะไร | MCP |
|---|---|---|
| `sticky_note` | โน้ตสีเหลือง (`text`, `color`) | ✅ |
| `note_text` | ข้อความยาว | ✅ |
| `frame` | กรอบจัดกลุ่ม — ลาก frame = ลากทั้งกลุ่ม (คิดจาก overlap) | ✅ |
| `drawing` / `reroute` | วาดเส้น / จุด pass-through สาย | ❌ |

### 🛠 Tools group (เว็บเท่านั้น)
| อะไร | ทำอะไร | ทางแทนบน MCP |
|---|---|---|
| `tool` node (`data.op`) เช่น extract-frame / extract-storyboard | ตัดเฟรมจากวิดีโอ ฯลฯ | ❌ — แจ้ง user ทำในเว็บ |
| Promote (เมนูบน output node) | ส่ง output → Cast/Set/Prop / Mix Stage / cover / shot | ✅ cover: `set_project_cover(project_id, run_id)` (reuse รูปเดิม, 0 แต้ม) · shot: `add_shot_asset(shot_id, type:"storyboard"/"manhwa"/"insert", run_id)` (pointer 0 แต้ม — dev) · Mix Stage: `save_to_mix_stage` ผ่าน authenticated app bridge · entity = เว็บ |

---

## 2) WORKFLOW RECIPES (ผ่าน MCP)

**A. Text → Image (พื้นฐานสุด):**
```
canvas_generate_image(board_id, prompt, ratio, resolution, quality)
→ ได้ prompt_text → gen_image → output_image ครบ + run_id
→ wait_for_run(run_id) จน completed → output node เติมรูปเอง
```

**B. Image → Video (ต่อยอดผลลัพธ์):**
```
1. gen รูปด้วย A → ได้ output_node_id
2. canvas_generate_video(board_id, prompt, ref_node_ids:[<output_node_id>], duration, ratio)
   → รูปนั้นกลายเป็น ref (image_files) ของวิดีโอ + เกิดสาย ref → gen ให้เห็นบนบอร์ด
```
ref_node_ids รับ node ที่มี URL ใช้ได้: `image` / `output_image` / `video` / `output_video`
(asset_ref/canvas_ref อ่านได้ถ้ามีอยู่แล้วบนบอร์ด). URL ในตัว node เก่าอาจหมดอายุ (~1 ชม.) —
ถ้า resolver ฟ้อง "no usable http URL" ให้เอา `storage_path`/`runId` ไปขอใหม่
(`get_asset_url` / `get_run_status`) แล้วอัปเดต node หรือใช้ node ใหม่.

**C. ตั้ง output image เป็นหน้าปกโปรเจกต์ (ไม่ gen ซ้ำ):**
```
1. wait_for_run(run_id) จน image completed
2. set_project_cover(project_id, run_id)
   → เขียน cover_asset_id + world_settings.coverPath/coverUrl
   → reuse asset เดิม, 0 แต้ม, หน้าเว็บอ่าน URL ใหม่ได้ทันที
```
ถ้ามี `storage_path` อยู่แล้ว ใช้ `update_world(project_id, cover_path)` ได้;
ถ้าจะเอาปกออก ใช้ `set_project_cover(project_id, clear:true)`.

**C. ใช้ entity ของโปรเจกต์เป็น ref บนบอร์ด (มาตรฐาน):**
```
get_project → canvas_add_asset_ref(board_id, entity_id) → ใส่เป็น ref_node_ids ของ gen
```
(= Insert → Asset reference ของเว็บเป๊ะ: การ์ด entity + URL รีเฟรชเอง ; ⛔ เลิกใช้ท่า
image node + get_asset_url แล้ว — ใช้เฉพาะ media ที่ไม่ใช่ entity เช่นไฟล์แนบ user.)

**D. Manhwa ของช็อต → ลงทะเบียนเป็น shot asset (ท่าใหม่ — 0 แต้ม):**
```
canvas_generate_image(prompt สไตล์ manhwa) → wait_for_run
→ add_shot_asset(shot_id, type:"manhwa", run_id, select:true)  ← pointer เข้า studio_shot_assets
                                                                  (ไม่ก๊อปไฟล์ ไม่เสียแต้ม ; select = ตัวโชว์)
→ ดู/สลับตัวโชว์: list_shot_assets(shot_id, type:"manhwa") / select_shot_asset(...)
→ ซ่อนตัวที่ไม่ใช้: เลือกตัวแทนก่อนถ้าจำเป็น → remove_shot_asset(...)
  (soft-hide pointer เท่านั้น; output/run/storage/แต้มยังอยู่, ไม่ refund; audit ด้วย include_removed:true)
```
⛔ **manhwa = display/mention เท่านั้น — ห้าม auto-แนบเป็น video-gen ref** (Rev 3 #1).
จะใช้ manhwa เป็น ref ของ `generate_shot_video` ต่อเมื่อ **user ตัดสินใจสั่งเอง** เท่านั้น
ค่อยทำแยก: `list_promotable_references` (ถ้าเป็น shot asset) → `save_to_mix_stage`
พร้อม source type/role → `attach_shot_mix_stage_refs(...)` (additive ไม่ล้าง ref เดิม).
ใช้ `set_shot_mix_stage_refs` เฉพาะตอน user สั่ง replace/clear ทั้งชุดเท่านั้น.
❌ เลิกท่าเก่า (save_to_mix_stage ชื่อ `manhwa_*` เป็น convention) สำหรับ manhwa แล้ว —
Mix Stage เหลือไว้สำหรับ reference media ที่ใช้ซ้ำจริงๆ. **ภาพสไตล์พิเศษอื่นที่ไม่ผูกช็อต**
(สไตล์บอร์ด/ทดลอง) ยังเก็บเข้า Mix Stage ได้ตามเดิม.

**E. Mood board / brainstorm:** `canvas_create_board` → `frame` ตั้งชื่อโซน →
`sticky_note`/`note_text` ไอเดีย → recipe A ต่อโซน → `canvas_connect_nodes` โยงความสัมพันธ์.
จัดวางด้วย x,y เอง (โซนละคอลัมน์ ห่างกัน ~400px) กันกองทับ.

**F. STORY STRIP — เล่าเรื่องทั้งเรื่องบนบอร์ด จนได้วิดีโอครบทุก beat ⭐**
เมื่อ user สั่ง "gen เรื่อง/นิทานบน idea board":
```
1. แตกเรื่องเป็น beats (3–8 beat) → สรุปแผน + ประมาณแต้ม (get_balance) → ให้ user confirm 1 ครั้ง
2. canvas_create_board("<ชื่อเรื่อง>") → frame ต่อ beat (เรียงคอลัมน์ x = 80, 1200, 2320, …)
3. ตัวละคร/ฉากหลัก: gen "character sheet" ด้วย recipe A 1 รูป/ตัว → ใช้เป็น ref ทุก beat
   (identity consistency — เท่ากับ portrait ของ movie pipeline). 🎯 prompt sheet ต้อง
   **CLEAN REF**: ตัวละคร = "single character, neutral pose, clean plain studio background,
   no scenery, no other people" · prop = "single isolated object on plain white background,
   no hands, no scene" · ฉาก = "empty location, no people" — ref สะอาด = ทุก beat ไม่ drift
4. ต่อ beat i:
   a. canvas_generate_image(prompt ของ beat, ref_node_ids: [character sheets, output ของ beat ก่อน])
      → wait_for_run → ได้ภาพ beat
   b. canvas_generate_video(prompt การเคลื่อนไหวของ beat,
      ref_node_ids: [ภาพ beat นี้ (+ วิดีโอ/ภาพ beat ก่อน ถ้าต้องการ motion ต่อเนื่อง)],
      duration ตาม beat) → wait_for_run → วิดีโอ beat ตกบนบอร์ด
   c. แจ้งผล beat ให้ user (ผ่าน/แก้) ก่อนไป beat ถัดไป — วิดีโอ = เงินจริง อย่ายิงรัวข้าม feedback
5. ครบทุก beat → สรุป: บอร์ดมีวิดีโอเรียงตาม frame ; อยากตัดต่อ/เก็บเข้า movie → promote:
   save_to_mix_stage ต่อคลิป หรือแนะนำ user ย้ายไป movie pipeline (/siamshort-b2b-auto-movie)
```
⚠️ continuity บน canvas อ่อนกว่า movie pipeline (ไม่มี tag/mention entity/extend) — เรื่องยาว
หรือซีเรียส แนะนำ user ใช้ /siamshort-b2b-auto-movie แทน ; story strip เหมาะกับเรื่องสั้น/ทดลองไว.
⭐ ต้องการ consistency เต็มรูปบนบอร์ด (identity → storyboard → manhwa position → video) →
ใช้ **/siamshort-b2b-board-movie** (pipeline production ครบ 7 ขั้น + layout มาตรฐานกันทับ).

**Layout tip:** ทุก `canvas_add_node` / `canvas_generate_*` รับ `x`,`y` (กลุ่ม gen วางที่
x, x+360, x+720) ; **ไม่ใส่ = ระบบวางต่อท้ายล่างสุดของบอร์ดให้อัตโนมัติ ไม่ทับของเดิม**.
งานหลายกลุ่มให้คุม layout เอง: คอลัมน์ละ ≥1200px แนวนอน, แถวละ ≥1300px แนวตั้ง.

**G. ไฟล์แนบจาก user → ใช้เป็น ref ⭐**
user แนบรูป/วิดีโอ/เสียงมาในแชท (หน้าคน / สไตล์ / โลโก้ / สถานที่จริง / voice / sound) → **ต้องเคารพและใช้เสมอ**:
```
1. หา path ไฟล์ในเครื่อง (แนบใน Claude Code = มี path ; ไม่รู้ path → ถาม user)
2. upload_reference(file_path, workspace_id:<project.workspace_id>) → {asset_id, signed_url, storage_path}
3. ใช้เป็น ref ได้ 2 ทาง (รองรับ **รูป วิดีโอ และเสียง**):
   a. บนบอร์ด: canvas_add_node(type:"image"/"video"/"audio", src:signed_url, label:"user ref: ...")
      → ใส่ใน ref_node_ids ของ gen — ระบบแยกให้เอง: รูป → image_files (identity/composition)
      · วิดีโอ → video_files (motion/จังหวะ) · เสียง → audio_files (voice/music/sound)
   b. เข้า movie: ค้นของเดิมด้วย list_mix_stage_refs; ถ้ายังไม่มีจึง
      save_to_mix_stage(project_id, name, storage_path, source_type, reference_role)
      → attach_shot_mix_stage_refs → ใส่ mention_token ที่คืนมาใน prompt เมื่ออ้าง ref
      → generate_shot_video (รูป→image_files, คลิป→video_files, เสียง→audio_files)
```
📌 semantics ของ ref: **image = ลุค/องค์ประกอบ/identity · video = การเคลื่อนไหว/จังหวะ ·
audio = voice/music/sound**
— กำกับใน prompt เสมอว่าจะเอาอะไรจาก ref ("copy the MOTION from the reference clip;
do NOT copy its look/lighting" หรือกลับกัน) ไม่งั้นโมเดลลอกทั้งหมด.
⛔ ห้าม auto-promote/auto-attach; ถ้าค้นเจอหลายตัวต้องถาม user และใช้
`set_shot_mix_stage_refs` เฉพาะ user สั่ง replace/clear ทั้งชุด. video/audio/multi-panel
image ห้ามใช้เป็น Start/End Frame.
✅ VA parity กับเว็บ: BytePlus register รูป+วิดีโอ; xskill register VA เฉพาะรูปและส่ง
วิดีโอเป็น signed `video_files`; เสียงส่ง `audio_files` ไม่ใช่ VA. เจอ "still being
registered" = รอ ~30 วิ เรียกซ้ำ.

---

## 3) กฎเหล็กบนบอร์ด (ระบบจริง — ละเมิดแล้วพังเงียบ)

1. ⛔ **ห้าม base64 / data: URL ใน node data** — realtime ตัดทิ้งเงียบทั้งบอร์ด (>256KB).
   media = URL + storage_path เสมอ (MCP validate ให้แล้ว).
2. **edge เส้นประ (generated) ลบไม่ได้** — เป็นโครงสร้าง gen→output ; หายเองเมื่อ output ถูกลบ.
3. **URL บน node มีอายุ ~1 ชม.** — เว็บ re-sign ตอนโหลดเอง ; MCP อย่า cache URL เก่าข้ามชั่วโมง.
4. **ลบ node ได้แล้ว (`canvas_delete_nodes`) และเป็น soft remove** — ไฟล์ gen ไม่หาย
   อยู่ใน project library เสมอ (จ่ายแต้มแล้วระบบเก็บให้) ; ลบเพื่อจัดบอร์ดได้สบายใจ
   แล้วค่อยเอากลับมา insert ใหม่จาก library/รัน list_runs ได้.
5. **บอร์ดใหญ่ (>1000 nodes)** — `canvas_get_board` เพจให้แล้ว ; แต่คิดก่อนเพิ่ม node รัวๆ.
6. ✅ **Virtual assets อัตโนมัติแล้ว**: BytePlus register ref รูป+คลิป; xskill register VA
เฉพาะรูป ส่วนคลิปส่ง signed `video_files`; เสียงส่ง `audio_files` ไม่ใช่ VA. MCP ใช้ flow
เดียวกับปุ่ม Run บนเว็บ (Active → asset token /
Failed(faceless) → raw fallback) ; ถ้าได้ error "still being registered" = ระบบกำลัง
register อยู่ รอ ~30 วิแล้วเรียก tool เดิมซ้ำ (dedup ทำให้ retry ถูก). ref ratio นอกช่วง 0.4–2.5 = MCP
letterbox (แถบเทาเข้ม ไม่ crop) ให้อัตโนมัติก่อน register — เหมือนเว็บทุกอย่าง.
7. **QC ทุก gen:** `wait_for_run` แล้วเช็ค `status` เสมอ — `failed` มาพร้อม `error_kind` +
   `suggested_action` (moderation = ห้าม retry เดิม / timeout = ลองซ้ำได้ 1 / invalid_input =
   แก้พารามิเตอร์ก่อน). ของที่ fail **ห้ามใช้เป็น ref ขั้นถัดไป** — dependency rules เต็มดู
   /siamshort-b2b-board-movie §GEN QC GATE.
8. gen ตัดแต้มตอนเริ่ม (`get_balance` ก่อนชุดใหญ่ ; fail คืนเอง). รูป ~4.5pt · วิดีโอ ~20-40pt.

---

## 4) MCP CHEAT-SHEET (canvas)

| งาน | tool |
|---|---|
| สร้าง/ดูบอร์ด | `canvas_create_board(project_id,title)` · `canvas_list_boards` · `canvas_get_board(board_id)` |
| Asset reference (มาตรฐาน) | `canvas_add_asset_ref(board_id, entity_id, x?, y?)` — การ์ด entity ตาม Insert ของเว็บ |
| Insert from output | `canvas_add_output_ref(board_id, run_id, variant_index?)` — วาง output เก่า (รูป/คลิป/เสียง) เป็น media node มาตรฐาน |
| Canvas reference | `canvas_add_canvas_ref(board_id, source_board_id, source_node_id)` — การ์ด snapshot ข้ามบอร์ด |
| เพิ่ม node | `canvas_add_node(board_id, type, text?(=content)/src?/label?, x?, y?)` — type: prompt_text·note_text·sticky_note·image·video·frame·gen_image·gen_video·gen_idea_text ; ข้อความใส่ผ่าน `text` (หรือ `content` ก็ได้) |
| ลบ node (บอร์ดสะอาด) | `canvas_delete_nodes(board_id, node_ids ≤50)` — soft remove: เอา tile ออกจากบอร์ด + สายที่เกี่ยว ; **ไฟล์ gen อยู่ใน library ต่อ เอากลับมา insert ใหม่ได้** (ai_runs ไม่ถูกแตะ) ; node ที่กำลัง running จะถูก skip |
| เอา output เก่ากลับมาใช้ | `list_runs` → `get_run_status(run_id)` (signed URL) → `canvas_add_node(type:"image"/"video", src)` — หรือใช้ output picker ในเว็บ |
| แก้ node | `canvas_update_node(node_id, text?/label?/src?/model?/ratio?/resolution?/quality?/duration?)` — แก้ note เปล่า, แก้ prompt ของ advanced node ก่อน run_gen_node, เปลี่ยน settings ; ห้ามแก้ตอน running |
| ต่อสาย | `canvas_connect_nodes(board_id, source_node_id, target_node_id)` |
| จัดบอร์ด/ย้าย node | `canvas_move_nodes(board_id, moves:[{node_id,x,y}])` — ย้ายทีเดียวถึง 200 node ; flow: `canvas_get_board` → คำนวณ layout ใหม่จาก type/label/ขนาด → ย้ายทั้งชุด (คนดูบอร์ดเห็น node เลื่อนสด) |
| gen บนบอร์ด | `canvas_generate_image(board_id, prompt, model?, ratio?, resolution?, quality?, ref_node_ids?)` · `canvas_generate_video(..., duration?, ref_node_ids?)` |
| advanced gen (mention) | `canvas_add_advanced_gen(board_id, kind, prompt มี mention @[ชื่อ](cast:id)/(node:id), model?, ...)` — สร้าง idle เสมอ ; แล้ว `run_gen_node(node_id)` เมื่อ confirm |
| ยิง node ที่มีอยู่ | `run_gen_node(node_id)` — simple (อ่าน prompt/ref จากสาย) และ advanced (อ่าน text+mention) ; ⛔ advanced มี **integrity guard 2 ทิศ**: mention ที่ไม่มีสายต่อ = reject · ref ที่ต่อสายแต่ไม่ mention = reject (ยังไม่เสียแต้ม — error บอกวิธีแก้: connect/แก้ text/ถอดสาย) ; รองรับ mention เสียง (audio → audio_files) แล้ว |
| รอผล + เติม output | `wait_for_run(run_id)` / `get_run_status(run_id)` (เติม output node ให้เอง) |
| ส่งเข้า movie (ref ใช้ซ้ำ) | `save_to_mix_stage(project_id, name, run_id, source_type, reference_role)` → `attach_shot_mix_stage_refs(...)`; ใช้ `list_mix_stage_refs` ค้นของเดิมก่อนและถาม user ถ้ามีหลายตัว |
| ลงทะเบียน output เป็นของช็อต | `add_shot_asset(shot_id, type:"storyboard"/"manhwa"/"insert", run_id, select?)` (0 แต้ม) → `list_shot_assets` / `select_shot_asset` / `remove_shot_asset` (soft-hide unselected pointer; ไม่ลบไฟล์/run, ไม่ refund; `include_removed:true` ใช้ audit) ; ⛔ manhwa ห้าม auto-แนบเป็น gen ref — user สั่งเองเท่านั้น |
| URL หมดอายุ | `get_asset_url(storage_path)` |
