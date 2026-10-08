# 🎬 MASTER — เทคนิค Prompt กันตำแหน่งเพี้ยน/slop (GEE edition)

> Port จาก `siamshort_auto_loop/reference/00_MASTER_prompt-techniques.md` (ตกผลึกจากงานจริง:
> กุหลาบเผาใจ ฯลฯ) — **craft ทุกข้อคงเดิม เปลี่ยนเฉพาะเครื่องมือเป็นของ GEE/siamshort MCP.**
> อ่านก่อนเขียน prompt storyboard/วิดีโอทุกครั้ง. อัปเดต 2026-07-10.

⛔ กฎเหล็ก: ทุก gen ผ่าน siamshort MCP เท่านั้น · ทุก shot ต้อง TAG entity
(`character_ids`/`scene_id`/`item_ids` — ตอน `create_shot` หรือ `update_shot`) ไม่ใช่แค่พิมพ์ชื่อ.

---

## ⭐ 1) SCENE DESIGN = มุมกว้าง eye-level เห็นทุกโซนเฟรมเดียว + ANCHOR อสมมาตร (เทคนิคหลัก)

**ปัญหา:** ฉากหรู/สมมาตร (บันไดสองข้างเหมือนกัน) → AI ไม่รู้ว่าตัวละครโซนไหน → ตำแหน่งพลิก/slop.

1. **วางผัง geography ของห้อง** (อะไรอยู่โซนไหน — ร่างในหัวพอ ❌ ไม่ต้อง top-down เพราะวิดีโอถ่าย
   eye-level, scene ref ต้อง match มุมที่กล้องเห็นจริง).
2. **ทำลายความสมมาตร — ทุกโซนมี landmark เด่นไม่ซ้ำ**: บันไดซ้าย = พรมแดง + นาฬิกาตั้งพื้น +
   รูปพ่อกรอบทอง · บันไดขวา = ไม้เปลือย + ปาล์มกระถางน้ำเงิน + รูปปั้นหินอ่อน · มุมขวา = เปียโนดำ ·
   กลาง = โซฟายู + แจกันกุหลาบ.
3. **ระบุตำแหน่งแบบ ABSOLUTE อ้าง landmark** — ❌ "ซ้าย/ขวา" (พลิกตามกล้อง) ✅ "ข้างนาฬิกาโบราณ /
   ฝั่งเปียโน / ตีนบันไดขวา" ; ของซ้ำหลายตัว (โซฟา 3 ตัว) → เรียก "โซฟาฝั่งนาฬิกา/ฝั่งเปียโน".
   > ตัวอย่างที่ไม่มีวันสับสน: "โรสนั่งโซฟา**ฝั่งเปียโน** หันหาป้าที่ยืน**ข้างนาฬิกาตีนบันไดซ้าย**"
4. **อ้างเฉพาะของจริงที่มีในรูป Set ref + ล็อกห้ามมโน** — อ้างของที่ไม่มีจริง → AI มโนเฟอร์นิเจอร์ใหม่.
   ใส่: `❗ใช้เฉพาะเฟอร์นิเจอร์ที่มีในรูปฉากอ้างอิง ❌ห้ามเพิ่มโต๊ะ/เก้าอี้/โซฟา/แจกันที่ไม่มีในรูป`.
5. ⚠️ **ช็อตวิดีโอ WIDE เห็นผนังหลังเต็มห้อง = ตัวกระตุ้น mirror/ของงอก** (เคสจริง: Seedance mirror
   เปียโนเป็น 2 ตัว + งอกโคมไฟ + แถบกระจกห้องซ้อน) → เลี่ยง wide แบบนั้น ใช้ medium/MCU ปักตัวกับ
   landmark ฝั่งเดียว + ใส่ `⛔ LAYOUT LOCK (อสมมาตร): เปียโนตัวเดียวฝั่งขวา ; ❌ห้าม mirror ❌ห้ามของ
   ตัวที่สอง ❌ห้ามกระจกสะท้อน/ห้องซ้อน`.
   📌 อย่าสับสน: *Set ref มุมกว้าง (รูปนิ่งไม่มีคน เห็นทุกโซน)* = สิ่งที่ต้องการ ; *ช็อตวิดีโอ wide
   คนยืนกลางเห็นผนังสองฝั่ง* = สิ่งที่ต้องเลี่ยง.
6. **Set entity ของ GEE**: `description` ต้องสั่ง `single eye-level WIDE establishing, ONE
   continuous frame, all zones visible with DISTINCT asymmetric landmarks per zone (list them),
   no people, ❌NOT grid/turnaround/contact sheet ❌NOT top-down` + แสง/เวลา → `generate_entity_image`.
   (ระบบ gen ฉาก depopulated ให้อยู่แล้ว — หน้าที่เราคือลิสต์ anchor รายโซนให้ครบ.)

**ลำดับ:** ผัง geography → gen Set ref (anchor ครบ อสมมาตร) → blocking ตัวละครตามพิกัด landmark จริง.

---

## 2) CAM/BG LOCK — ปัก "ทิศกล้อง + ฉากหลังรายตัว" ทุกคัท

ทุกคัทระบุ: (1) กล้องหันทางไหน (2) **หลังตัวละครแต่ละคนเห็น landmark อะไร** เช่น
`@วิน หลัง=เปียโน`, `@โรส หลัง=บันไดซ้าย+นาฬิกา`.
- ไม่ปัก BG → Seedance ดูดตัวละครไปหา anchor เด่นสุด → ย้ายจุด/กลับด้าน (เคสจริงหลายครั้ง).
- ⛔ **POSITION LOCK ข้ามทั้งฉาก**: ปัก "ฝั่ง + BG anchor ตายตัว" ต่อคน แล้วใช้ซ้ำทุกช็อต บนเส้น 180°
  เดิม + `❌ห้ามสลับ A ไปฝั่งของ B`. prompt ที่ AI ร่างล่วงหน้ามักให้ทุกคน "กลางโถง" เหมือนกันหมด —
  **ไล่แก้ให้ตรง anchor ก่อน gen ทุกช็อต**.

## 3) SCENE REF ในวิดีโอ = mention Set + TEXT สั้น (ห้ามบรรยายฉากยาว)

- GEE: **tag `scene_id` บน shot + mention `#[ชื่อSet](set:uuid)`** (token จาก `get_project`) —
  ระบบแนบรูป Set + แปลง syntax ต่อโมเดลเอง.
- ❌ ห้ามบรรยายฉากยาว (เพดาน/เสา/ของแต่ง) — AI จะ "มโนฉากใหม่ตามคำ" ; ✅ สูตร:
  `Location: ใช้ฉากเดิมตามรูป #[Set] เป๊ะ (เวลา/แสง) — ❗ห้ามเปลี่ยน/สร้างใหม่/แต่งเพิ่ม.`
- ใส่ได้แค่ เวลา/แสง/มู้ด (golden hour, แสงเทียน) = บรรยากาศ ไม่ใช่สร้างสถานที่.
- Set ต้องมีรูปแล้ว (`image_path`) ไม่งั้นระบบข้าม ref เงียบๆ.

## 4) MEDIUM SHOT = SIGNATURE LOOK

MEDIUM / MCU เป็นหลัก (เห็นตัว+ไหล่+ฉากรอบ) ❌ ไม่ extreme face close-up ทั่วไป ; CU เก็บไว้
ไคลแม็กซ์/บีตอารมณ์.

## 5) SHOT CONSTRUCTION + ANTI-SLOP GUARDS (ใส่ทุก prompt)

- ⭐ **เปิดทุก location ใหม่ด้วย ESTABLISHING SHOT** (EXT/WIDE ไม่มีคน ไม่มีบท กล้องนิ่ง บอกที่+เวลา)
  แล้วค่อยเข้าเหตุการณ์ ; ตึก/บ้านเดียวกันหลายซีน establish ครั้งเดียว + ใช้ช็อตเดินเข้าห้องเป็น transition.
  (GEE: วางแผน establishing ไว้ใน shot list ตั้งแต่ต้น — แทรกทีหลังไม่ได้.)
- เปิด 0s ใกล้ๆ → hard cut สลับ MEDIUM ↔ MCU ↔ OTS (ไม่แพนเวียน).
- **eye-level เท่านั้น** ❌ มุมสูง/overhead/crane/CCTV (Seedance เพี้ยน) ; มุมเท่เก็บไว้ reveal/ไคลแม็กซ์.
- **[ANTI-CLONE]** `EXACTLY N named characters, each appears EXACTLY once` + มีตัวยืนเด่นเดียว →
  ย้ำ "ยืนคนเดียว=X ที่เหลือนั่ง".
- **[ANTI-SPLIT]** `ONE single continuous frame, ONE camera ❌ห้ามแบ่งจอ/two-panel/grid แม้ wide`.
- ระยะไกลสองฝั่ง → **OTS deep-focus เฟรมเดียว** ❌ wide โชว์สองปลาย (จะแตกสองท่อน).
- คุมสีหน้าตัวหลักตามคาแรกเตอร์ (พระเอกนิ่งสง่า ไม่ใช่หน้าคับแค้น).

## 6) ข้อจำกัด SEEDANCE ที่ต้องจำ

- **ตัวหนังสือไทยบนภาพเรนเดอร์ไม่ได้** → SFX/overlay อังกฤษเท่านั้น ; บทพูดไทยได้ (เสียง/lip-sync).
- มุมสูง/crane → เพี้ยน ; ฝูงคน → ชอบโคลน (นับเป๊ะ).
- ⚠️ **คำว่า "DV cam / tripod / ขาตั้งกล้อง" เป็นวัตถุใน prompt → Seedance วาดกล้อง+ขาตั้งจริงกลางเฟรม**
  (เคสจริง 2 ช็อต). แก้: ใส่ `cameraOverride` ทุก gen ที่เห็นพื้น:
  `"this is the FINAL FILM not behind-the-scenes; floor/foreground completely CLEAR;
  ❌ absolutely NO camera/tripod/DSLR/film rig/monitor/mic/film crew anywhere in frame;
  camera = viewer's invisible eye; eye-level"` ; ถาวร = เขียน style เป็น "lo-fi found-footage
  film grade" ไม่ใช่อุปกรณ์.

## 7) VIDEO WORKFLOW (GEE MCP)

1. ล็อก prompt (scene-lock §3 + position/CAM-BG lock §2 + anti-slop §5 + STYLE LOCK §8).
2. gen: `generate_shot_video(shot_id, model:"seedance-fast"/"seedance" (GROUP — LB เลือก provider),
   ratio, resolution:"720p", duration 4–15, generate_audio?)` หรือบน canvas =
   `run_gen_node(<gen_video node>)`.
3. `wait_for_run(run_id)` วนจน terminal (`error_kind`+`suggested_action` มากับ fail).
4. **วิเคราะห์ทั้งคลิป** — grid 16 เฟรม `ffmpeg -vf "fps=1,scale=240:-1,tile=4x4"` + เฟรมเต็มจุดสำคัญ ;
   ❌ อย่าเชื่อเฟรมท้าย `-sseof` เดี่ยว (จับรอยตัดหลอกตา) ❌ อย่า hstack หน้าคนติดกัน (เบลนดูเหมือนจูบ).
5. เช็ค: ตำแหน่งถูก/นิ่ง · เพี้ยน · โคลน · แตกจอ · ฉากตรง ref · ratio · ช่วงท้ายคลิป.
6. FAIL → แก้ prompt เฉพาะจุด → regen (≤4/ช็อต ; ครบเอาตัวดีสุด) ; PASS → อ่านตำแหน่งจริง →
   ล็อกช็อตถัดไป ; ยิงทีละช็อตเสมอ.

## 8) GRAPHIC STYLE STRING (มาตรฐาน — ❌ ไม่มีคำว่า "shaky" / ❌ ไม่มีชื่ออุปกรณ์กล้อง)

```
lo-fi found footage film grade, voyeuristic, heavy grain, motion blur, digital noise,
underexposed shadows, lo-fi color bleed, realistic live-action, NOT anime, NOT cartoon.
THRILLER เงียบกดดัน ไม่มีดนตรี. ไม่มีตัวหนังสือบนภาพ.
```
(ตัวอย่างสาย found-footage — เรื่องอื่นตั้ง STYLE LOCK ของตัวเองแล้วแปะทุก prompt คำต่อคำ ;
ใส่ lighting/time เพิ่มได้ = บรรยากาศ.)

## 9) CONTINUITY & ADVANCED BLOCKING (บทเรียนจริง)

### 9.1 เปิดช็อตด้วย CLOSE-UP "ต่อเนื่องอารมณ์"
ช็อตใหม่ = บท/อารมณ์ต่อเนื่องของตัวเดิม → เปิด CU หน้าตัวนั้น (ตรึงจุดเดิม+ขยี้อารมณ์) แล้วขยาย
MCU/insert ; ก่อนเขียน **วิเคราะห์เฟรมช็อตก่อน** (ชุด/ผม/ฝั่ง/bg) ระบุซ้ำใน prompt + `🔗 ต่อเนื่องจาก SBx`.

### 9.2 ใช้เฟรม/ภาพช็อตก่อนเป็น ref มุมกล้อง
GEE: ใช้ **storyboard/keyframe ของช็อต** เป็น ref (`ref_node_ids` บน canvas / Mix Stage +
`set_shot_mix_stage_refs` บน movie pipeline ; `transition_to_next:"extend"` สำหรับต่อเฟรมท้าย).
⚠️ ref แบบนี้ condition "ใกล้เคียง" ไม่ pin pixel → กำกับเสมอ: `ใช้ ref เป็น "มุมกล้อง/องค์ประกอบ
เท่านั้น" ❌ห้ามลอก graphic style/แสงของรูป ❌ห้ามเพิ่ม action ของรูป` + ล็อกกรอบ (medium, กล้องไม่ถอย).
(จับเฟรมกลางคลิป/ตัดคลิป = ทำในเว็บ Mix Stage — MCP ยังไม่มี.)
สั่ง action "ธรรมชาติ เร็ว ไม่อืด" ("โผเข้ากอดทันที") — Seedance ชอบทำช้าถ้าไม่กำชับ.

### 9.3 ตัวเดิน + ล็อกตัวนิ่ง (motivated follow)
ตัวนำเดิน → กล้องตามนุ่ม eye-level ¾ ; ⛔ ตัวอยู่กับที่ล็อก `ยืนนิ่งจุดเดิม ❌ไม่เดินตาม ❌ไม่ย้าย`
(ไม่งั้นโดนดูดเดินตาม/วาร์ป) ; จบช็อตเดินที่ landmark เพื่อส่งต่อ ; eyeline ช็อตถัดไปอ้าง landmark ตัวนิ่ง.

### 9.4 ANTI-ARTIFACT (god-ray/โคมระย้า)
`❌ห้ามวัตถุ/จานลอยกลางอากาศหลังศีรษะ ❌ห้ามโคมระย้าเพี้ยนเป็นจานบิน ❌ห้ามผนัง/เพดานเหลวบิด ;
ฉากหลังคมชัดเป็นสถาปัตยกรรมจริง`.

### 9.5 INSERT/PROP — ของในกรอบ + กัน morph
รูปในกรอบ → ย้ำ "เป็นรูปถ่ายในกรอบเท่านั้น ไม่ใช่คนจริงในฉาก" ; ของที่ถือ+ขยับ เสี่ยง morph
(กรอบรูปถือเอียง → กลายเป็นแท่งเงิน) → `ถือตั้งตรง หันด้านรูปเข้ากล้อง เห็นชัดตลอด ❌ห้าม morph
❌ห้ามถือเอียงจนเห็นแค่ขอบ`.

### 9.6 OTS sliver ≠ clone
ไหล่/หลังอีกตัวเบลอ foreground ใน reverse shot = OTS ปกติ ไม่ใช่โคลน — อย่า flag ผิดตอน QC.

### 9.7 จบช็อตที่ตัวนิ่ง = HARD CUT ไปตัวนั้น SOLO
อยากจบด้วยตัวที่ยืนนิ่ง → คัทท้ายเป็น "ตัวนั้นคนเดียวในเฟรม ที่ landmark เดิม + ❌ห้าม two-shot
❌ห้ามเดินเข้าหาตัวนำ" — ปล่อยอยู่เฟรมเดียวกับตัวนำ = Seedance ดูดให้เดินมายืนข้าง (ดริฟต์).

---

**ใช้คู่กับ:** `/siamshort-b2b-shot-continuity` (กลไก loop) · `siamshort-b2b-anti-plastic`
(realism/texture) · `siamshort-b2b-physics-guide` (ลูกโซ่แรง) · `gee-platform-map.md` (พารามิเตอร์).
