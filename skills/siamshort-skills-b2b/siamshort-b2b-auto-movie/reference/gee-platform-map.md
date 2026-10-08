# GEE platform map — พารามิเตอร์จริง + gotchas (คู่มือประกอบ /siamshort-b2b-auto-movie)

อัปเดต 2026-07-08 (ตรวจกับโค้ดจริง + ทดสอบ live บน dev แล้วทุกข้อ).

## 1. Entity types + enum ที่ DB บังคับ

| UI | entity_type | คอลัมน์เฉพาะ (ค่าอื่น = DB reject) |
|---|---|---|
| Cast | `character` | `character_category`: `lead` \| `supporting` \| `antagonist` \| `cameo` · `character_gender`: `female` \| `male` \| `non_binary` \| `unspecified` |
| Set | `scene` | `location_type` / `time_of_day` / `mood` (ข้อความอิสระ) |
| Prop | `item` | ไม่มีคอลัมน์เฉพาะ |

- `description` = prompt ตรงของ `generate_entity_image` — เขียนอังกฤษ ละเอียด **เฉพาะตัว
  subject**. เซิร์ฟเวอร์มี directive บังคับอยู่แล้ว (ตรวจจาก build-entity-image-prompt.ts):
  character = clean reference background ท่า neutral · prop = isolated object พื้นขาว studio
  · set = depopulated (ไม่มีคน) + negative rules หัว-ท้าย prompt → ❌ อย่าใส่ฉากหลัง/คนอื่น/
  บริบทลงใน description ของ cast/prop เด็ดขาด (จะตีกับ directive แล้วภาพ drift).
- Set description แนะนำ: `eye-level wide establishing shot, single frame, all zones
  visible, distinct asymmetric landmarks: <list>, no people, <time of day>, <mood>`.

## 2. Mention tokens (ระบบ reference ของ GEE)

- ดึงจาก `get_project` → ทุก entity มี `mention_token` พร้อมใช้:
  - Cast → `@[ชื่อ](cast:<uuid>)` · Set → `#[ชื่อ](set:<uuid>)` · Prop → `$[ชื่อ](prop:<uuid>)`
- แปะใน `prompt` ของ shot ตรงตำแหน่งที่ตัวนั้นปรากฏ. ตอน gen เซิร์ฟเวอร์:
  เซ็นรูป entity (24 ชม.) → เลือก adapter ต่อโมเดล → แปลง token เป็น syntax ของโมเดลนั้น
  (`@image_file_N` / `【@图片N】` / APT legend / `[image N]`) → ใส่ ref ลง slot ที่ถูก.
- ⛔ ห้ามเขียน syntax พวกนั้นเองเด็ดขาด — เขียน token กลางอย่างเดียว.
- entity ที่ **tag** ไว้บน shot (`character_ids`/`scene_id`/`item_ids`) จะถูกแนบเป็น
  ambient ref ให้อัตโนมัติแม้ไม่ mention (ระบบ dedupe ให้ ไม่ซ้ำ).
- entity ที่ยังไม่มีรูป (`image_path` ว่าง) → ระบบข้าม ref ตัวนั้นเงียบๆ (ไม่ fail) —
  เพราะงั้น **gen รูป entity ให้เสร็จก่อนถึง PHASE B เสมอ**.

## 3. โมเดลวิดีโอ + ราคา — ⭐ ใช้ GROUP id เป็นหลัก (ตรวจ 2026-07-10)

**GROUP = load-balanced server-side**: ส่ง id กลุ่ม → start-workflow เลือก provider ที่ว่าง
ให้เอง (byteplus↔xskill) + คิดราคา flat ของกลุ่ม — เหมือนที่เว็บใช้. พิสูจน์ live ผ่าน MCP แล้ว.

| id (ใช้ตัวนี้) | ชนิด | base | audio | สมาชิก |
|---|---|---|---|---|
| ⭐ `seedance-fast` | GROUP | 38 | ✅ | byteplus-seedance-2-fast / seedance-2-ark-fast |
| ⭐ `seedance` | GROUP | 60 | ✅ | byteplus-seedance-2 / seedance-2-ark |
| `byteplus-seedance-2(-fast)` | ตรงตัว | 60/38 | ✅ | ใช้เมื่อต้องบังคับ provider เท่านั้น |
| `seedance-2-ark(-fast)` / `apt-seedance-2(-fast)` | ตรงตัว | 60/38 | ✅ | ทางเลือก |
| `seedance-2` / `seedance-fast-2` (xskill st-ai เก่า) | ตรงตัว | 60/38 | ❌ ไม่มี audio | เลี่ยง |
| `topaz-upscale` | — | 108 | — | upscale, ยังไม่มี MCP tool |

- 🔊 **`generate_audio: true`** ใส่ได้กับตระกูล Seedance (ดูคอลัมน์ audio / `list_models`
  ฟิลด์ `supports_generated_audio`) — เสียงประกอบ/บรรยากาศมากับวิดีโอเลย.
- image ก็มี GROUP: `gpt-image-2` (27) · `nanobanana-2` (15) · `nanobanana-2-pro` (27).

- ราคาโดนคิด **ตอนเริ่ม** (`consume_credits_v2`) — fail = คืนแต้มอัตโนมัติ.
- วิดีโอ = dynamic points: `base × (duration ÷ ref) × resolution multiplier`.
- รูป entity/draft ≈ 4.5 pt (1K/low) — คูณตาม resolution/quality.
- text prompt ≈ 1–2 pt/ช็อต.

## 4. พารามิเตอร์ generate_shot_video

- `model`: จาก `list_models(kind:"video")` ใช้ค่า `provider_model` ตรงๆ.
- `ratio`: ⚠️ ต้องเป็นค่าที่ระบบมีในตาราง pricing — ปลอดภัยสุด `16:9` / `9:16` / `1:1`.
  ค่าแปลก (`21:9` เคยทำ gen fail ทั้งระบบมาแล้ว) — อย่าเดา.
- `resolution`: `720p` (fast รับสูงสุด 720p) / `1080p` (เฉพาะตัวเต็ม).
- `duration`: **4–15 วินาที ต่อ 1 วิดีโอ** (MCP clamp ให้ ; ไม่ส่ง = ใช้ `duration_seconds`
  ของ shot). ความยาวหนังรวม = ผลรวมช็อต → วางแผนจำนวนช็อต ≈ ความยาว ÷ 6–10 วิ
  ตั้งแต่ขั้น shot list เสมอ (30 วิ → 3–6 ช็อต · 60 วิ → 6–10 ช็อต).
- ไม่ส่ง `prompt` → ใช้ prompt ที่เซฟบน shot (แนะนำ: เซฟก่อนด้วย `update_shot` เสมอ
  เพื่อให้ Retry/Recreate ในเว็บเห็นตัวเดียวกัน).

## 4b. Reference ต่อ gen — image + video

- โมเดลวิดีโอรองรับ **ทั้ง image ref และ video ref** ; slot แยกตามชนิดอัตโนมัติ:
  image → `image_files` (identity/composition) · video → `video_files` (motion —
  Seedance เลียนแบบการเคลื่อนไหว). syntax การ bind ต่อ provider เซิร์ฟเวอร์/n8n จัดการเอง.
- แหล่ง ref: mention/tag entity (รูป) · Mix Stage (รูป+คลิป ผ่าน gen_refs) · canvas
  ref_node_ids (รูป+คลิป) · ไฟล์แนบ user ผ่าน `upload_reference`.
- กำกับใน prompt เสมอ: เอา "ลุค" หรือ "การเคลื่อนไหว" จาก ref — ไม่กำกับ = โมเดลลอกทั้งคู่.

## 5. Async pattern (ทุก gen)

```
generate_* → { run_id, status: queued|running }
loop: wait_for_run(run_id, timeout_s:55) → timed_out:true = ยังไม่เสร็จ เรียกซ้ำ
terminal: completed → outputs[{storage_path, signed_url}] / failed → error_message + คืนแต้ม
```
- `queued` = ติด concurrency cap ของระบบ (ปกติ — cron ระบายคิวเอง) รอต่อได้เลย.
- วิดีโอ = คาดหวัง 3–10 นาที ; เกิน ~30 นาที = ระบบตัด fail + คืนแต้มเอง.
- **signed URL อายุ ~1 ชม.** — เก็บ `storage_path` คู่กันเสมอ ; หมดอายุ →
  `get_asset_url(storage_path)`.

## 6. วิเคราะห์คลิป (client-side — ทำเองในเครื่อง)

```bash
curl -sL "<signed_url>" -o shotN.mp4
ffmpeg -i shotN.mp4 -vf "fps=1,scale=320:-1,tile=4x4" -frames:v 1 shotN_grid.png
# + เฟรมเต็มจุดสำคัญ: ffmpeg -ss <sec> -i shotN.mp4 -frames:v 1 shotN_t<sec>.png
```
เปิดรูปดู (Read) → อ่าน position/แสง/continuity ทั้งคลิป — อย่าตัดสินจากเฟรมท้ายเฟรมเดียว.

## 7. Chain job (AI เขียน prompt ทุกช็อต)

- `start_video_prompt_chain(project_id)` → คิวเฉพาะช็อตที่ **มี plot แต่ยังไม่มี prompt**.
- เงื่อนไข: 1 chain active ต่อโปรเจกต์ · role ต้องมี `shots.ai_gen` · n8n cron หยิบทุก ~5 นาที
  (ถ้าค้าง pending นาน = cron ฝั่งแพลตฟอร์มยังไม่เปิด — แจ้ง user).
- ตามผลด้วย `get_chain_job_status(project_id)` → `completed_count/total_count` + สถานะต่อช็อต.
- prompt ที่ chain เขียนจะมี mention marker มาให้เอง — review แล้วแก้เฉพาะจุดด้วย `update_shot`.

## 8. ข้อจำกัด MCP ปัจจุบัน (แจ้ง user แทนที่จะฝืน)

- ❌ แทรก/สลับลำดับ shot · ลบ shot/entity/sequence — วางแผนก่อนสร้าง ; ลบ = ทำในเว็บ.
- ❌ capture frame / trim clip เป็น ref (`%ref` ของ Fable) — ใช้ draft image +
  `transition_to_next:"extend"` + position-lock ใน prompt แทน ; ฟีเจอร์ Mix Stage มีในเว็บ.
- ❌ เลือก take (selected video) / upscale / panels (Bible/Lookbook) — ทำในเว็บ.
- ✅ **Virtual assets อัตโนมัติแล้ว**: gen วิดีโอ byteplus/xskill ที่มี ref รูป/คลิป — MCP
  register เป็น virtual asset ให้เอง (เหมือนปุ่ม Run บนเว็บ: Active → asset token /
  Failed(faceless) → raw fallback) ; ถ้าได้ error "still being registered" = ระบบกำลัง
  register อยู่ รอ ~30 วิแล้วเรียก tool เดิมซ้ำ (dedup ทำให้ retry ถูก). ref ratio นอกช่วง 0.4–2.5 = MCP
  letterbox (แถบเทาเข้ม ไม่ crop) ให้อัตโนมัติก่อน register — เหมือนเว็บทุกอย่าง.

## 9. Billing / workspace

- แต้มตัดจาก workspace ของ user ที่ MCP ล็อกอิน (org = pool กลาง + budget cap ต่อคน).
- `get_balance` โชว์ balance + cap ; `insufficient_funds` / `budget_cap_exceeded` =
  หยุดถาม user ก่อน (อย่าลดสเปกเองเงียบๆ).
