---
name: siamshort-b2b-auto-director
description: >-
  Auto-Director Mode บน Siamshort/GEE — เปลี่ยนไอเดียเรื่อง 1 บรรทัด ให้เป็นโปรเจกต์หนัง
  ครบชุดผ่าน siamshort MCP: project+world → cast/sets/props (+รูป) → sequence →
  shots+prompt → gen วิดีโอทีละช็อต. ผู้ใช้ให้แค่ไอเดีย สกิลตัดสินใจกำกับเองทั้งหมด
  (ถามได้ ≤3 คำถามเฉพาะที่เปลี่ยนงานจริง). ใช้เมื่อ user บอก "เอาเรื่อง... มาทำเป็นหนัง
  บน GEE/Siamshort", "auto-director", "ทำหนังให้หน่อยจากไอเดียนี้", "/siamshort-b2b-auto-director".
  Do NOT trigger เมื่อ: user มีบท/นิยายเต็มและอยากคุมทุกขั้น (ใช้ /siamshort-b2b-auto-movie ที่มี
  confirm-gate ละเอียดกว่า), แพลตฟอร์ม Fable เดิม (ใช้ /fable-auto-director),
  หรือ gen รูปเดี่ยว.
---

# 🎬 Siamshort Auto-Director (GEE) — ไอเดีย 1 บรรทัด → หนังทั้งเรื่อง

พอร์ตจาก `fable-auto-director` มาใช้ **siamshort MCP**. ต่างจาก `/siamshort-b2b-auto-movie` ตรงที่
**auto-decision สูงสุด**: user ให้ไอเดีย → สกิลตัดสินใจกำกับ (โครง/สไตล์/ตัวละคร/ช็อต) เอง
โดยถาม **≤3 คำถาม** แล้วลุย. ยังคง **OK-gate ตอน gen วิดีโอทีละช็อต** (เงินจริง) + one-shot
confirm ก่อนเริ่มเผาแต้ม.

> เครื่องมือ/พารามิเตอร์/ข้อจำกัด GEE ทั้งหมด = ตาม
> `siamshort-b2b-auto-movie/reference/gee-platform-map.md` (อ่านก่อนเสมอ) ; craft ระดับ prompt =
> `/siamshort-b2b-shot-continuity` + `siamshort-b2b-anti-plastic` + `siamshort-b2b-physics-guide`. ⛔ ทุกการ gen ผ่าน
> siamshort MCP เท่านั้น.

---

## 0) Defaults (ถามเฉพาะที่เปลี่ยนงานจริง ≤3 ข้อ)

| Decision | Default | ถามเมื่อ |
|---|---|---|
| Ratio | **9:16** (viral แนวตั้ง) | เรื่องดู cinematic → เสนอ 16:9 |
| ขนาด | 1 sequence · **5 shots** · 10–15s/ช็อต | user บอก "ซีรีส์/ยาว" |
| Base look | เลือกให้ตามโทนเรื่อง (found-footage = default สายไวรัล) | โทนกำกวม |
| โมเดลวิดีโอ | GROUP `seedance-fast` 720p (LB เลือก provider เอง) | คุณภาพสูง → GROUP `seedance` ; อยากมีเสียง → `generate_audio:true` |
| งบ | เช็ค `get_balance` แล้วแจ้งประมาณการ (รูป ~4.5pt/ตัว · วิดีโอ ~20–40pt/ช็อต) | แต้มไม่พอแผน |

## 1) BUILD PIPELINE (auto — ทำรวดเดียว แล้ว confirm ครั้งเดียว)

1. **ขยายไอเดีย → โครงเรื่อง 3 องก์ + beat ต่อช็อต** (สวมบททีมกำกับระดับโลก ; แนวคอเมดี้ →
   เสนอ Comic-SFX layer: onomatopoeia อังกฤษ + speed-lines).
2. `create_project(title, logline, genre, ratio, synopsis แน่นๆ, visual_rules = base look +
   บล็อกข้อห้ามทั้งเรื่อง)`.
3. `create_entity` ครบ Cast/Sets/Props (description = visual DNA อังกฤษละเอียด ; Set =
   eye-level wide establishing) → `generate_entity_image` ทุกตัว → `wait_for_run` จนครบ.
   (user ให้รูป ref → `upload_reference` → `set_entity_gen_references(entity_id, [...])`
   ก่อน gen — ❌ ห้ามอ้อม canvas: SURFACE LOCK ตาม `/siamshort-b2b-auto-movie` ข้อ 0.7
   บังคับสกิลนี้ด้วย — canvas เป็นของแชท idea board แยกต่างหาก.)
4. `create_chapter(content = เนื้อเรื่องเต็ม)` → `create_shots_batch` ครบทุกช็อต:
   plot ละเอียด (action+มุมกล้อง+position) · duration · `transition_to_next` ·
   ⭐ **tag `character_ids`/`scene_id`/`item_ids` ครบตั้งแต่สร้าง**.
5. เขียน prompt ทุกช็อตเอง (`update_shot`) ตาม `/siamshort-b2b-shot-continuity` §1–5 + mention_token
   จาก `get_project` — หรือใช้ `start_video_prompt_chain` แล้ว review.
6. **สรุปทั้งหมดให้ user 1 ครั้ง** (โครง · ตัวละคร+รูป · ช็อตต่อช็อต · ประมาณการแต้ม) →
   **รอ confirm ครั้งเดียว** → เข้าข้อ 2 ของ PHASE วิดีโอ.

## 2) VIDEO LOOP — ทีละช็อต (OK-gate คงเดิม ห้ามข้าม)

ใช้ `/siamshort-b2b-shot-continuity` เป็นกลไกเต็ม: วิเคราะห์ช็อตก่อน → ล็อก prompt →
`generate_shot_video` → `wait_for_run` → วิเคราะห์ทั้งคลิป → **STOP รอ user OK** →
ช็อตถัดไป (regen ≤4/ช็อต).

## 3) สิ่งที่ Fable ทำแต่ GEE Auto-Director ไม่ทำ (แจ้ง user แทน)

- ✅ **cover gen ทำได้แล้ว** (2026-07-17): `generate_project_cover` → โชว์ user →
  `set_project_cover(run_id)` — ดู `/siamshort-b2b-auto-movie` ข้อ 10c.
- ❌ manhwa / comic-SFX **overlay หลัง gen** — SFX ใส่เป็นคำสั่งใน prompt ได้
  (ตัวหนังสือบนภาพ = อังกฤษเท่านั้น) แต่ post-overlay ทำในเว็บ/ตัดต่อ.
- 📎 upload รูป ref ผ่าน MCP ทำได้แล้ว (`upload_reference` → `set_entity_gen_references` /
  `save_to_mix_stage`) — แต่รูป **หน้าคนจริง** อาจติด moderation ฝั่ง provider ;
  ref วิดีโอของคนจริง = virtual asset auto-register.
- ❌ แทรก/ลบ/สลับช็อตหลังสร้าง — วางแผนให้จบใน build ข้อ 4.
