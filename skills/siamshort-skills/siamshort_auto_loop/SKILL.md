---
name: siamshort_auto_loop
description: >-
  "Loop" — กระบวนการมาตรฐาน end-to-end ในการทำหนัง Siamshort/Fable จากบท →
  storybox → gen วิดีโอทีละช็อต (human-in-the-loop) โดยสมมุติบทบาทเป็นทีมกำกับหนังระดับโลก
  และคุมคุณภาพด้วยคลังเทคนิค anti-slop ที่ p'ton คอนเฟิมจากงานจริง.
  ใช้เมื่อผู้ใช้พิมพ์ "/siamshort_auto_loop", พูดว่า "ทำตาม Loop", "เริ่ม Loop",
  "ลูป", "เข้า production", "ทำหนัง/ซีรีส์ตามกระบวนการ", "เริ่ม pre-production →
  gen วิดีโอ", หรืออ้างถึง "Siamshort auto technique / MASTER prompt-techniques".
  คุม 2 เฟส: PHASE A pre-production (รับบท → /siamshort_script_from_novel "เท่านั้น" ให้ละเอียดยิบ →
  ถาม pacing 3 ระดับ (รวดเร็ว/ปานกลาง/ยาว) → เลือก graphic style → ลง storybox มีวินาที/มุมกล้อง/position
  ด้วย subagent 5 role (Director/Story/Visual/Motion/Sound) → double-check กับ novel → สรุปให้ user confirm
  (แก้ทุกครั้งตรวจกับบท) → tag entity ลง storybox → gen character/scene/item = จบ PHASE A ❌ไม่ทำ storyboard/manhwa)
  และ PHASE B video-gen loop (storybox ครบแล้ว → เน้น gen video ทีละ shot มี human-in-the-loop ไม่ใช่ทีละ 10: วิเคราะห์ช็อตก่อนหน้า →
  lock ตำแหน่ง+แสง → gen 1 วิดีโอ → รอ user กดโอเคว่าวิดีโอดีแล้ว ค่อยไปช็อตถัดไป ;
  ยังไม่โอเค=แก้+regen แล้วถามใหม่ ห้ามข้าม gate). อ้างคลังเทคนิคเต็มที่
  reference/00_MASTER_prompt-techniques.md ทุกครั้งก่อนเขียน prompt.
  Do NOT trigger เมื่อ: แค่แปลงนิยาย→บท (ใช้ /siamshort_script_from_novel),
  one-line idea → ทั้งโปรเจกต์อัตโนมัติแนวคอเมดี้ (ใช้ /fable-auto-director),
  gen รูปเดี่ยว (ใช้ /gpt-image), หรือทำ storyboard-sheet อย่างเดียว (ใช้ /storyboard).
---

# 🔁 Siamshort Auto-Loop — กระบวนการผลิตหนัง Fable/Siamshort

กระบวนการมาตรฐานที่ p'ton เรียกว่า **"Loop"** — ใช้ทำหนัง Fable/Siamshort จาก
**บท → storybox → gen วิดีโอทีละช็อต (human-in-the-loop)** ให้ตัวละครอยู่ตำแหน่งเดิมต่อเนื่อง
ไม่ slop/ไม่เพี้ยน มากที่สุด.

> **สมมุติบทบาท = ทีมกำกับหนังระดับโลก** ตลอดทั้งกระบวนการ.
> สรุปจากงานจริง (กุหลาบเผาใจ ฯลฯ). คลังหลักการ prompt/anti-slop เต็มอยู่ที่
> **`reference/00_MASTER_prompt-techniques.md`** — **อ่านก่อนเขียน prompt ทุกครั้ง**.

---

## 0) กฎเปิดสกิล (ทำก่อนเสมอ)

1. **สวมบททีมผู้กำกับระดับโลก** — ทุก decision (มุมกล้อง, blocking, แสง, จังหวะตัด) คิดแบบมืออาชีพ.
2. **อ่าน `reference/00_MASTER_prompt-techniques.md` ให้ครบก่อนลงมือเขียน prompt** — เป็นคลังบทเรียน
   anti-slop ที่ขาดไม่ได้ (scene-anchor map, CAM/BG lock, position lock, anti-clone/split,
   ข้อจำกัด Seedance, cameraOverride กันขาตั้งกล้อง ฯลฯ). Quick-checklist อยู่ท้ายไฟล์นี้ แต่
   **รายละเอียด + เคสจริง อยู่ใน MASTER**.
3. **ยึด graphic style + บล็อกข้อห้ามชุดเดียวกันทั้ง chapter** — ปรับแค่ฉาก/วัน/เวลา/แสงตามบท.
4. ⛔ **กฎเหล็ก — ทุกการสร้าง/เรนเดอร์/แก้รูปใน Loop = ผ่าน Fable/Siamshort MCP เท่านั้น.** ใช้ MCP tools:
   `generate_image` · `regen_character_image` · `regen_scene_image` · `regen_item_image` ·
   `story_gen_images_batch` (gen รูป asset) · และแก้ ref ด้วย `edit_reference_asset`.
   **❌ ห้ามสร้างรูปผ่านสกิล `/gpt-image` (`/img`) หรือยิง xskill.ai เองโดยตรงในขั้นตอนใดๆ ของ Loop เด็ดขาด** — รูปที่ gen นอก
   MCP จะ **ไม่ถูกลงทะเบียนในโปรเจกต์** (ไม่มี VA/byteplus sync, mention `#scene`/`&VA`/`%ref` ไม่ได้, หน้า/ฉากหลุด continuity).
   📌 หมายเหตุ: `edit_reference_asset` ใช้ GPT-Image-2 ก็จริง แต่เป็น **ฝั่งเซิร์ฟเวอร์ผ่าน MCP** (ลงทะเบียน ref ให้อัตโนมัติ) =
   คนละทางกับสกิล `/gpt-image` ที่ยิง xskill ตรง → ใช้ `edit_reference_asset` ได้ ✅ / ใช้ `/gpt-image` ไม่ได้ ❌.
5. ⛔⛔ **กฎเหล็ก (พลาดบ่อยสุด!) — พอได้ storybox ต้อง "TAG / เลือก entity ลง storybox" เสมอ ไม่ใช่แค่ mention ในข้อความ:**
   ทุก StoryBox หลัง `create_shot` + เขียน `seedancePrompt` เสร็จ → **ต้องเรียก `update_shot(shotUid,
   characterIds:[...], sceneIds:[...], itemIds:[...])` เลือก @character / #scene / $item ที่อยู่ในช็อตนั้นให้ครบ
   — เป็น "ขั้นสุดท้าย" ของทุกช็อต**. แค่พิมพ์ `@char / #scene / $item` ใน *ข้อความ prompt* **ไม่พอ** เพราะ:
   - (ก) **UI ต้องเห็น tag** character/scene/item ที่เลือกใน storybox (ไม่งั้นช็องว่าง เหมือน "ลืม tag")
   - (ข) **ตอน gen วิดีโอ ดึง ref จาก tag ที่ผูกไว้** ไม่ใช่จากตัวอักษร → ไม่ผูก = หน้า/ฉากหลุด
   - (ค) `create_shot` / การเซฟ prompt ชอบ **auto-link ตามชื่อ** → ผูกผิด/ทับ tag ที่ตั้งใจ (ชื่อชนกัน เช่น
         `@โรสริน` vs `@โรสรินลุคคลับ`) → จึงต้อง `update_shot` set `characterIds/sceneIds/itemIds` **ทับเป็น step สุดท้าย** ทุกครั้ง
   - ⚙️ `create_shot` **ไม่รับ** characterIds/sceneIds/itemIds (มีแค่ presetText/seedancePrompt/sortOrder)
     → ต้อง `update_shot` เท่านั้น ; อย่าลืม **ทุกช็อต** (loop ครบ ไม่ใช่แค่ช็อตแรก).

---

## PHASE A — PRE-PRODUCTION (บท → storybox + assets · ❌ไม่ทำ storyboard/manhwa)

1. **รับบท → บทถ่ายทำ "ละเอียดยิบ" — ⚠️ บังคับใช้ `/siamshort_script_from_novel` เท่านั้น** (ห้ามวิเคราะห์/
   แปลงบทด้วยวิธีอื่นเด็ดขาด). ได้ **บทถ่ายทำ △-format ที่ละเอียดยิบทุก action** — เก็บ **ทุกความปรารถนาของ
   นักเขียน novel ครบ** (△ action / บทพูด / V.O. / 音效), ทำโดย **agent ระดับโลก** ตามสกิล. บทนี้ =
   **source of truth** ของทั้ง Loop (ทุกขั้นต่อจากนี้ต้องตรงกับบทนี้).

2. **ถาม user: PACING — "ความยืดของหนัง" 3 ระดับ (มาตรฐาน) ⭐** — บท △-format เหมือนเดิม เปลี่ยนแค่
   "วิธีแตกเป็นช็อต / ความยืด":

   | ระดับ | การเล่า | บทพูด / อารมณ์ | จำนวน storybox (บทเท่ากัน) | เหมาะกับ |
   |------|--------|----------------|---------------------------|---------|
   | ⚡ **รวดเร็ว** | action ครบตาม novel แต่ **บีบกระชับ** เล่าไวสุด ตัดฉับ ไม่มีน้ำ | คำพูดตัดเหลือแก่น ยัดไวๆ ; reaction น้อย | **น้อยสุด** | คลิปไวรัล/สั้น hook เร็ว retention สูง |
   | ▶ **ปานกลาง** | สมดุล action↔อารมณ์ จังหวะหนัง/ซีรีส์ปกติ ; **1 storybox = 1 beat หลัก** | บทพูดครบ + reaction/หายใจพอดี | **ปานกลาง** | ดราม่า/ซีรีส์ทั่วไป เล่าครบ ดูเพลิน |
   | 🎬 **ยาว (หนังโรง)** | ยืดๆ slow-burn อารมณ์เยอะ ; **แตก 1 action เป็นหลายมุม/หลายช็อต** ; 1 storybox อาจแค่สลับอารมณ์ไปมา (CU สีหน้า/สายตา/มือสั่น/ความเงียบ) | บทพูดเต็ม + pause + subtext ยาว | **มากสุด** | หนังอารมณ์เข้มข้น ; **ให้คนตัดมีของเล่นเยอะ** เลือกช็อต/จังหวะได้อิสระ |

   > เสนอ default ตามแนวเรื่อง (ดราม่าอารมณ์/แค้น = ยาว · สายไวรัล = รวดเร็ว) แต่ **ให้ user ตัดสิน** ก่อนไปต่อ.

3. **แนะนำ graphic style 5 แบบให้ user เลือก** (ระบบมี default) — อ่านบทแล้ววิเคราะห์ว่าหนังเรื่องนี้ควรเป็นสไตล์ไหน.

4. **PRE-PRODUCTION → ลง storybox ของ siamshort (timed shot-plan) ⭐** — แปลงบท △-format → **storybox** ที่มี
   **วินาที (timing) + มุมกล้อง + action + position เบื้องต้น** ครบทุกช็อต ตาม pacing ที่เลือก (ข้อ 2).
   **prompt ขั้นนี้ยังไม่ใส่ graphic style ใดๆ** (โฟกัส action/timing/กล้อง — ใส่ style ทีหลังตอน gen).
   **เปิดทุกซีน/สถานที่ใหม่ด้วย ESTABLISHING SHOT** (MASTER §5).
   ⚙️ **storybox ไหนมี "แรงตั้งต้น" (ของตก/แตก/สาด/เท/หก/ล้ม/สะดุด/ชน/ผลัก/ตบ/ไฟ/ฝน/ลม) →
   ขยายด้วยสกิล `physics-guide` (ลูกโซ่ฟิสิกส์ 5 ชั้น: object audit → เหตุการณ์หลัก → ลูกโซ่ →
   reflex-ก่อน-อารมณ์ → world echo + CONTINUITY NOTE)** — user เขียน action สั้นได้
   ระบบเติมความธรรมชาติให้เอง (เทคนิค 06_PHYSICS-GUIDE).

   **spawn subagent 5 ตัว (role ชัด — ทีมกำกับระดับโลก) ช่วยกันคิดจากบท action → storybox:**
   - 🎯 **Director / Showrunner — "Vision & Taste"** : คุมโทน/ธีม/จังหวะใหญ่/เอกภาพน้ำเสียง, ถือ **final-cut authority**, แตก brief → ทิศทางให้อีก 4 ตัว, ตัดสินข้อขัดแย้ง, การันตีทุกช็อต "พูดภาษาเดียวกัน".
   - ✍️ **Story Architect — "Soul & Emotion"** : concept/world-building/โครง 3 องก์-beat sheet/character arc/บทพูด/subtext + วิศวกรรมอารมณ์ (setup–payoff, จุดพลิก, จังหวะให้หายใจ).
   - 🎨 **Visual Director (Cinematography + Production Design) — "Look & Continuity"** : ออกแบบตัวละคร/asset + **ล็อก reference ให้ consistent ข้ามช็อต** (จุดเป็นจุดตายของ AI video), color script, lighting, ภาษาเลนส์/องค์ประกอบ, ออกแบบโลก/ฉาก.
   - 🎥 **Motion & Performance Director — "AI Generation Craft"** : shot design → prompt จริง (Seedance), shot type/camera movement/กำกับการแสดงในเฟรม, multi-shot temporal continuity, regen/QC loop, รู้จุดแข็ง-ข้อจำกัด engine (= bottleneck ตัวจริง).
   - 🎵 **Sound, Music & Edit Director — "Rhythm & Feel"** : assembly/pacing/ตัดบนอารมณ์/continuity QC/color finishing + score/SFX/dialogue/mix (เสียง ≈ 50% ของหนัง).

   **ลำดับส่งต่อ:** Director เซ็ตวิสัยทัศน์ → Story เขียนลง storybox+beat → Visual ออกแบบ look+lock asset →
   Motion วาง prompt+continuity → Sound/Edit วางจังหวะ+เสียง → กลับให้ Director ตรวจ **final cut** →
   **วน loop แก้จุดที่ยังไม่ผ่าน**. (ใช้ CAM/BG lock MASTER §2 + POSITION LOCK + skill `seedance-shot-continuity`.)

   ⭐⛔ **ทุกช็อตที่ลง (`create_shot`) → ต้อง `update_shot` TAG `characterIds/sceneIds/itemIds` ให้ครบทันที**
   (ดู §0 ข้อ 5 — เลือก character/scene/item ลง storybox จริง ไม่ใช่แค่ mention ในข้อความ ; ทำเป็นขั้นสุดท้ายของแต่ละช็อต).

5. **DOUBLE-CHECK: storybox ↔ บท novel** — เอา storybox ที่ได้ตรวจทานกับบท △-format/novel อีกรอบว่า
   **รายละเอียดครบถ้วน ไม่ slop ไม่มีอะไรหาย** ก่อนเสนอ user.

6. **แจ้ง user ภาพรวมก่อนลงมือ:** กี่ storybox · กี่ scene · กี่ตัวละคร · ลุคใหม่ต้องสร้างไหม/อย่างไร ·
   **เล่าเรื่องย่อแต่ละ storybox คร่าวๆ** (เช่น 12 storybox → เล่าทั้ง 12) → **รอ user confirm หรือแก้ไข**.
   - ⚠️ **ทุกครั้งที่ user ขอแก้ → ต้องตรวจทานกับบทละเอียดทุกครั้ง** (กัน slop / ไม่ตรง novel / ของหาย).
     ถ้าการแก้ **ทำให้ไม่ตรงบท → เตือน user "อันนี้ไม่ตรงกับบทนะ"** ; user ok แล้วค่อยลุยต่อ.

7. **(confirm แล้ว) gen character + scene + item** ทั้งหมดที่เกี่ยวกับบท.
   - ⚠️ scene ref = **มุมกว้างระดับสายตา เฟรมเดียว (eye-level WIDE establishing)** เห็นทุกโซน + anchor อสมมาตรชัดในภาพเดียว — ❌ ไม่ใช่ 3×3 turnaround/grid, ❌ ไม่ต้อง top-down
     (ต้องส่ง `prompt` custom เองทุกครั้ง — ดู MASTER §1 ข้อ 6). ของเด่น/พร็อพสำคัญ → `create_virtual_asset` ด้วย.

8. **finalize prompt (ใส่ graphic style + anti-slop locks ตาม MASTER) ให้ครบทุก storybox → จบ PHASE A.**
   ❌ **ไม่ต้อง gen storyboard / manhwa** (ตัดออกจาก Loop แล้ว) — พอ storybox + prompt + tag + assets ครบ ก็ข้ามไป PHASE B (gen video) ได้เลย.
   - ⛔ **ก่อนข้าม PHASE B เช็กว่า *ทุก* storybox tag `characterIds/sceneIds/itemIds` ครบแล้ว** (§0 ข้อ 5) —
     ไม่ผูก tag = ตอน gen video ดึงหน้า/ฉาก/พร็อพผิดหรือหลุด. verify ด้วย `list_shots` / `get_shot`.

---

## PHASE B — VIDEO-GEN LOOP (storybox ครบ → เน้น gen video ทีละ shot · human-in-the-loop)

> 🎯 **storybox + prompt + tag + assets ครบจาก PHASE A แล้ว → หัวใจ PHASE B = gen video ทีละ shot โดยมี human-in-the-loop (OK-gate ทุกช็อต).** ❌ ไม่มี storyboard/manhwa มาคั่น — ได้ storybox ครบก็ยิงวิดีโอทีละช็อตเลย.
>
> ⛔ **กฎเหล็กของ Loop: ทำทีละวิดีโอ — ไม่ใช่ทีละ 10.** gen ได้ **1 ช็อต** → **STOP รอ user
> กดโอเคว่า "วิดีโอดีแล้ว"** → ค่อยขยับไปช็อตถัดไป. **ห้าม gen ช็อตถัดไปจนกว่า user จะ OK ช็อตปัจจุบัน.**

วนต่อช็อต N แบบนี้ทุกครั้ง:

1. **วิเคราะห์ช็อตก่อนหน้า (N−1) ก่อนเสมอ** — อ่าน+วิเคราะห์วิดีโอช็อตก่อน **ทั้งคลิป** → อ่าน
   **position นักแสดงทุกคนว่าอยู่ตรงไหนของ scene** (lock ให้ต่อเนื่อง) + อ่าน **แสง** (lock ไม่ให้เพี้ยน).
   *(ช็อตแรกสุดของซีน/ไม่มีช็อตก่อน → ข้ามขั้นนี้ ใช้ scene ref + storybox แทน)*
2. **เขียน/ล็อก prompt ช็อต N** ตามผลวิเคราะห์ + MASTER (scene-lock + position-lock + anti-slop).
   - เลี่ยงขึ้นต้น 0s ด้วยตัวละครเดิมจาก last frame ของช็อตก่อน (ถ้า last frame = A → 0s ไม่เริ่มด้วย A).
     **ยกเว้น** user สั่งเอา last frame มาเป็น ref ตำแหน่ง → 0s ห้ามเริ่มด้วยมุมกล้องเดียวกับ last frame นั้น.
   - 📌 **user อยากเอารูป/คลิปจาก storybox ไหนมาเป็น ref ให้ช็อตนี้ → ทำตาม `§REF-ASSETS`**
     (`capture_video_frame` / `trim_reference_video` → `add_ref_asset_to_shot` → `%name`).
   - ⚙️ **ช็อตมีแรงตั้งต้น (ของตก/แตก/สาด/ล้ม/ชน ฯลฯ) → เรียกสกิล `physics-guide` ขยายลูกโซ่ก่อน gen** ;
     และ **ดึง CONTINUITY NOTE ของช็อตก่อนหน้า** (เศษ/คราบ/เก้าอี้ล้ม/เสื้อเปียก/ไอที่จางหมด)
     มาใส่ใน scene/position lock ของช็อตนี้เสมอ — เศษแก้วช็อต 5 ต้องยังอยู่บนพื้นช็อต 6.
3. **gen วิดีโอ 1 ช็อต** (`regen_shot_video` 9:16 — ดู §VIDEO / MASTER §7) → poll จนได้ videoUrl.
4. **STOP → ถาม user "วิดีโอโอเคไหม / แก้ไหม?" แล้วรอ user กดโอเค.**
   - ❌ ยังไม่โอเค/ให้แก้ → เช็คว่าเกิดอะไรขึ้น → ปรับ prompt เฉพาะจุด → **regen ช็อตเดิม** (≤4 ครั้ง)
     → ถาม user ใหม่. **ห้ามไปช็อตถัดไป** จนกว่าจะได้ OK.
5. **user กดโอเคว่าวิดีโอดีแล้ว → ค่อยไปช็อต N+1** (กลับขึ้นข้อ 1: วิเคราะห์ช็อต N ที่เพิ่งผ่าน → ทำต่อ).
6. **วนทีละช็อตจนจบ** — ทุกช็อตมี OK-gate ของ user คั่นเสมอ (ไม่มีการ batch หลายช็อตรวด).
7. **ขั้นตอนไหน subagent ทำให้ไว/ดีขึ้น → ใช้ได้เลย** (แต่ห้ามข้าม OK-gate).

> รายละเอียด loop ต่อช็อต (gen → poll → วิเคราะห์ทั้งคลิป → PASS/FAIL → regen ≤4) ใช้สกิล
> **`seedance-shot-continuity`** เป็นกลไกหลักของ Phase B.

---

## กฎทั่วไปของ Loop

- ⭐ **แทรก scene/establishing เมื่อไหร่ → renumber storybox ใหม่ให้ต่อเนื่อง (1..N) เสมอ.**
  - ⚠️ บทเรียนระบบ: `update_shot` **ไม่มี sortOrder → แก้ลำดับหลังสร้างไม่ได้** ; และ `create_shot`
    **ปัดเศษเป็นจำนวนเต็ม** (0.5→1, 7.5→8) → ชนกับช็อตเดิม.
  - ⭐ **วิธีที่ถูก: วางแผน sortOrder ตอน `create_shot` ให้มี GAP แต่แรก (10, 20, 30, …)** เพื่อแทรก
    establishing/insert ทีหลังได้ (เช่น 15, 25) โดยไม่ชน ; หรือ **สร้าง establishing shot ก่อน** ช็อตอื่น
    ในซีนนั้น. เผลอสร้างเลขติดกันแล้วอยากแทรก = ต้อง delete+recreate (เสีย prompt/tag ที่ทำไว้).
    ระหว่าง gen วิดีโอ Phase B ลำดับจริงให้ยึดตามบท (ไม่ต้องพึ่ง sortOrder ในเว็บ).
- ทุก prompt ยึด **graphic style + บล็อกข้อห้ามเดียวกันทั้ง chapter** (ปรับแค่ฉาก/วัน/เวลา/แสง).
- สกิลที่ใช้ร่วม: **`seedance-shot-continuity`** (ลูปทีละช็อต + position lock — กลไกหลัก Phase B) ·
  prompt format/style/บล็อกข้อห้าม = **`reference/00_MASTER_prompt-techniques.md`** ·
  ชั้น realism/texture = **`anti-plastic`** · ชั้นฟิสิกส์ลูกโซ่ (action มีแรง/กระแทก) = **`physics-guide`** ·
  "idea เดียว → ทั้งโปรเจกต์อัตโนมัติ" = **`fable-auto-director`** · แปลงนิยาย→บท =
  **`siamshort_script_from_novel`** · storyboard-sheet prompt = **`storyboard`**.

---

## §VIDEO — พารามิเตอร์ generate วิดีโอ (Fable MCP)

1. ล็อก prompt (scene-lock + position/anchor-lock + anti-slop) ก่อนเสมอ.
2. **gen 9:16:** `regen_shot_video(shotUid, ratio "9:16", resolution "720p", model "seedance_2.0", duration 15)`
   — ❌ อย่าใช้ `story_gen_video_next` (ล็อก 16:9).
3. `poll_video_byteplus(taskId)` → success + videoUrl.
4. **โหลด + วิเคราะห์ "ทั้งคลิป"** (grid 16 เฟรม `fps=1,tile=4x4` + เฟรมเต็มจุดสำคัญ ; อย่าเชื่อเฟรมท้าย
   `-sseof` อย่างเดียว ; อย่า hstack หน้าคนติดกัน).
5. เช็ค: ตำแหน่งถูก/นิ่ง · เพี้ยนไหม · โคลนไหม · แตกจอไหม · ฉากตรง ref · 9:16 · ช่วง 14–15s.
6. **FAIL → ปรับ prompt เฉพาะจุด → regen** (≤4 ครั้ง/ช็อต ; ครบ 4 ไม่ได้ก็รับตัวดีสุด ไปต่อ).
7. **PASS → อ่านตำแหน่งจริง → ล็อกช็อตถัดไป**.
8. ยิงทีละช็อต (อย่ายิงพร้อมกันหลายตัวจนข้ามขั้น "เห็นผลก่อนล็อกตัวถัดไป").
- credits ~45–55 / คลิป 15s 720p ; image-gen connector บางวัน flaky → retry.
- ใส่ `cameraOverride` กันขาตั้งกล้อง/DSLR โผล่ทุก gen ที่เห็นพื้น (ดู MASTER §6).

---

## §REF-ASSETS — ดึงรูป/คลิปจาก storybox มาเป็น %reference (เมื่อ user ขอ) ⭐

เมื่อ user อยากให้ **"เอารูป/วิดีโอจาก storybox ไหน มาเป็น reference ให้การ gen ช็อตนั้นๆ"** — เพื่อ lock
มุมกล้อง/องค์ประกอบ/การเคลื่อนไหว ให้ต่อเนื่อง — ใช้ flow นี้. **รายละเอียดเต็ม (ทุก param + error handling
+ ตัวอย่าง) อยู่ที่ `reference/02_REFERENCE-ASSETS_capture-edit-trim.md` — อ่านก่อนใช้.**

> Reference Asset เก็บ **ระดับ Chapter** → สร้างครั้งเดียว ใช้ได้กับทุก storybox (shot) ใน chapter เดียวกัน.
> เช็คก่อนสร้างซ้ำด้วย `list_reference_assets(chapterUid, mediaType "all")`.

> ⚠️ **กฎสำคัญสุด — ใน prompt ใช้ `%name` เท่านั้น ❌ ห้าม `%uid`.** ต้อง `add_ref_asset_to_shot` ก่อนเสมอ
> ถึงจะอ้าง `%name` ได้ (**ไม่มี shortcut อ้าง uid ตรงๆ ใน prompt**). ตั้ง `name` สื่อความหมาย+เลขช็อต ไม่มี
> เว้นวรรค (ใช้ `_`) เช่น `sb21_rose_closeup`, `sb15_walk_motion` — ❌ ห้ามตั้งเป็น uid / มี space / ยาวเกินไป.

**4 เครื่องมือ:**
- `capture_video_frame(projectUid, chapterUid, videoUrl, timeSec, name)` → จับ **เฟรมเดียว** ที่วินาทีไหนก็ได้
  (`timeSec` 0~15 ; **ไม่ใช่แค่ last frame** ; `-1` = เฟรมสุดท้าย) → **image ref** (composition/มุมกล้อง/style).
- ⭐ `edit_reference_asset(projectUid, chapterUid, sourceImageUrl, editPrompt, name, ratio)` → **เอารูป (จาก
  capture หรือ url ใดๆ) ไป edit ด้วย XSkill GPT-Image-2-Edit (ฝั่งเซิร์ฟเวอร์ผ่าน MCP — ❌ ไม่ใช่สกิล /gpt-image) ก่อน แล้วค่อยเอามาเป็น ref**: ลบ/เปลี่ยน bg ·
  แก้ lighting/สี/mood · เพิ่ม-ลบ element · ปรับ composition → ได้รูปใหม่ permanent `{name, url}`. `ratio` =
  `1:1`/`4:3`/`3:4`/`16:9`/`9:16`/`3:2`/`2:3` (default `16:9` — **วิดีโอ Loop 9:16 ให้ใส่ `ratio:"9:16"`**) ;
  `editPrompt` เป็นภาษาอังกฤษ.
- `trim_reference_video(projectUid, chapterUid, sourceVideoUrl, startSec, endSec, name)` → ตัดคลิป **1–15s**
  → **video ref** = **motion reference** (Seedance เลียนแบบการเคลื่อนไหว).
- `add_ref_asset_to_shot(shotUid, assetUrl, assetName, mediaType "image"/"video")` → แนบ ref เข้า shot ปลายทาง
  **(บังคับ — ต้องเรียกก่อน ถึงจะใช้ `%assetName` ได้)** → อ้าง `%assetName` ใน prompt (auto-สร้าง VA ให้ BytePlus).
  *(จาก output ของ capture/edit/trim: `name`→`assetName`, `url`→`assetUrl`, `uid`→`assetUid` optional tracking)*

**Flow A — ใช้ตรง (เอาเฟรมจาก sbX → ref ให้ sbY):**
1. ดึง `videoUrl` ของ sbX ที่ gen ผ่านแล้ว (ใช้ URL สดจาก gen result).
2. `capture_video_frame(... videoUrl=<sbX>, timeSec=<วินาทีที่ชอบ>, name="sbX_xxx")` → ได้ `url` + `uid`.
   *(อยากได้ motion แทนภาพนิ่ง → `trim_reference_video(... startSec,endSec ≤15s)`)*
3. `add_ref_asset_to_shot(shotUid=<sbY>, assetUrl=<จากข้อ2>, assetName="sbX_xxx", mediaType="image")`.
4. เขียน prompt sbY อ้าง `%sbX_xxx`.
5. `regen_shot_video(<sbY> …)` → Seedance ใช้ ref นั้นต่อเนื่อง.

**Flow B — capture → EDIT → ref (⭐ แนะนำ เมื่ออยากแต่งรูปก่อนเอามาอ้าง):**
1. `capture_video_frame(... name="sbX_raw")` → ได้ `url` เฟรมดิบ.
2. `edit_reference_asset(sourceImageUrl=<เฟรมดิบ>, editPrompt="<สั่งแก้ EN>", name="sbX_edited", ratio="9:16")`
   → ได้รูป edit แล้ว `{name, url}` (permanent).
3. `add_ref_asset_to_shot(shotUid=<sbY>, assetUrl=<edited url>, assetName="sbX_edited", mediaType="image")`.
4. prompt sbY อ้าง `%sbX_edited` → `regen_shot_video`.
   *(ใช้แต่งฉาก/แสง/ลบของรก/เปลี่ยน mood ให้ ref ตรงใจ ก่อนป้อนเข้า gen — ดู editPrompt ตัวอย่างใน reference 02)*

⚠️ **คุม ref ไม่ให้ลากของไม่พึงประสงค์มา** (MASTER §9.2): regen condition บน ref เป็นแบบ "ใกล้เคียง" **ไม่ pin
pixel เป๊ะ** → คันโยกคือ prompt: สั่ง `%ref` = **"มุมกล้อง/องค์ประกอบเท่านั้น ❌ห้ามลอก graphic style/แสง/
ห้ามเพิ่ม action ของรูปนั้น"** + ล็อกกรอบ (medium/ครึ่งตัว กล้องไม่ถอย) ไม่งั้นมันถอยเป็น full-body / เปลี่ยน
detail เอง.
⚠️ ถ้า `capture_video_frame` พลาด (timeSec เกิน duration) → ลดเลข/ใช้ `-1` ; **fallback** = `lastFrameUrl` +
`upload_image` (URL ถาวร).
🔗 ผูกกับ **Phase B ข้อ 2/4**: ถ้าใช้ last frame ของช็อตก่อนเป็น ref ตำแหน่ง → 0s **ห้ามเริ่มด้วยมุมกล้องเดียว
กับ last frame** นั้น (กัน Seedance ก๊อปเฟรมแปะ).

---

## ✅ QUICK ANTI-SLOP CHECKLIST (ย่อ — รายละเอียดเต็ม + เคสจริงอยู่ใน reference/00_MASTER)

ก่อน gen ทุกช็อต ไล่เช็ก:

- [ ] **SCENE = มุมกว้างระดับสายตา เห็นทุกโซนในเฟรมเดียว + anchor ทุกโซนไม่ซ้ำ** (ไม่ต้อง top-down) ; อ้างตำแหน่งแบบ **ABSOLUTE landmark** (ข้างนาฬิกา/
      ฝั่งเปียโน) ❌ ไม่ใช่ ซ้าย/ขวาตามกล้อง. อ้างเฉพาะ **ของจริงในรูป ref** + ล็อก "ห้ามมโนเฟอร์นิเจอร์".
- [ ] **CAM/BG LOCK** ทุกคัท: กล้องหันทางไหน + หลังตัวละครแต่ละคนเห็น landmark อะไร.
- [ ] **POSITION LOCK ข้ามทั้งฉาก**: ใครอยู่ฝั่งไหน + หันหน้าทางไหน + ❌ห้ามสลับฝั่ง A↔B (ใช้ซ้ำทุกช็อต).
- [ ] **scene ref ในวิดีโอ = mention `#ชื่อScene` หรือ `&VA` + TEXT สั้น** — ❌ ห้ามบรรยายฉากยาว (AI มโนฉากใหม่).
- [ ] **MEDIUM / MCU เป็นหลัก** (signature look) ; CU เฉพาะไคลแม็กซ์.
- [ ] **เปิดทุก location ใหม่ด้วย ESTABLISHING SHOT** (EXT/wide ไม่มีคน บอกที่+เวลา) ก่อนเข้าเหตุการณ์.
- [ ] **กล้อง eye-level** ❌ ห้ามมุมสูง/overhead/crane/CCTV ในวิดีโอ (Seedance เพี้ยน).
- [ ] **[ANTI-CLONE]** นับตัวเป๊ะ "EXACTLY N" + "ยืนคนเดียว=X ที่เหลือนั่ง".
- [ ] **[ANTI-SPLIT]** ภาพเดียวต่อเนื่อง ❌ ห้ามแบ่งจอ/two-panel/grid แม้ wide ; ระยะไกลสองฝั่ง→ OTS deep-focus.
- [ ] **กันขาตั้งกล้อง:** ❌ เลี่ยงคำว่า DV cam/tripod/ขาตั้ง เป็น "วัตถุ" ; ใส่ `cameraOverride`
      "FINAL FILM, floor clear, NO camera/tripod/DSLR/rig in frame, camera = invisible eye".
- [ ] **ตัวหนังสือบนภาพ = อังกฤษเท่านั้น** (Seedance เรนเดอร์ไทยบนภาพไม่ได้ ; บทพูดไทยได้=เสียง).
- [ ] **ANTI-ARTIFACT** (god-ray/โคมระย้า): ❌ห้ามจาน/วัตถุลอยหลังหัว ❌ห้ามผนัง/เพดานเหลวบิด.
- [ ] **WIDE เห็นผนังหลัง = กระตุ้น mirror/ของซ้ำ** → เลี่ยง ใช้ medium/MCU ปักตัวกับ landmark ฝั่งเดียว +
      บล็อก `⛔ LAYOUT LOCK (ห้าม mirror)`.
- [ ] **จบช็อตที่ตัวยืนนิ่ง = hard cut ไปตัวนั้น SOLO** (ไม่งั้น Seedance ดูดให้เดินมา two-shot ดริฟต์).
- [ ] **PHYSICS CHAIN (`physics-guide`)**: ช็อตมีแรงตั้งต้น → ลูกโซ่ครบ 5 ชั้น + real-time ห้าม slow-mo
      ห้ามรีเพลย์ ; **เศษ/คราบ/สภาพจาก CONTINUITY NOTE ช็อตก่อน = ต้องอยู่ต่อ** จนกว่าบทให้เก็บ.
- [ ] **วิเคราะห์ทั้งคลิป** ไม่ใช่เฟรมท้าย ; อ่าน position จริง + แสง ก่อนล็อกช็อตถัดไป.

---

## เครื่องมือ/ของที่เกี่ยวข้อง

- **คลังเทคนิคเต็ม:** `reference/00_MASTER_prompt-techniques.md` (9 หมวด + เคสจริงทุกบทเรียน) ·
  `reference/02_REFERENCE-ASSETS_capture-edit-trim.md` (capture / **edit (GPT-Image-2)** / trim → `%ref` — ดู §REF-ASSETS).
- **สกิลร่วม:** `seedance-shot-continuity` · `fable-auto-director` · `siamshort_script_from_novel` · `storyboard`.
  ⛔ `gpt-image`/`img` = **ใช้นอก Loop เท่านั้น** ; ใน Loop สร้างรูปผ่าน Fable MCP เสมอ (ดูกฎ §0 ข้อ 4).
- **MCP server:** Fable (`30cd8ff5-…`) — VA enforcement, `regen_shot_video`, `poll_video_byteplus`,
  `capture_video_frame`/`edit_reference_asset`/`trim_reference_video`/`upload_image`, `add_ref_asset_to_shot`, `list_reference_assets`.
- **memory:** `fable-mcp-video-gen-workflow`, `kuhlaab-phao-jai-project`,
  `seedance-onscreen-text-english-only`, `seedance-multichar-clone-guard`, `fable-item-vs-virtual-asset`.
- **โปรเจกต์อ้างอิงที่ใช้ Loop นี้:** กุหลาบเผาใจ (uid IZdhOv0kfK4fi_R1) — Interlude, กลับมาเพื่อทวงคืน,
  นางฟ้าที่ตายไปแล้ว.

> 📌 โฟลเดอร์ต้นทาง `Desktop/Fable/Siamshort auto technique/` ยังเป็น **master source** ที่ p'ton อัปเดต
> เทคนิคใหม่ลงไป — ถ้าแก้ที่นั่น ให้ re-sync มาที่ `reference/` ของสกิลนี้.
