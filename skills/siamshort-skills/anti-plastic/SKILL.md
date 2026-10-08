---
name: anti-plastic
description: >-
  Anti-Plastic / Hyperreal Detail Writing — วิธีเขียน prompt ภาพ/วิดีโอให้ "ละเอียดถูกจุด"
  จนผลลัพธ์ไม่พลาสติก ไม่มีกลิ่น AI ใช้ได้ทุก genre (portrait, found-footage, action, wuxia,
  horror, drama, ads, anime). Use when the user types "/anti-plastic", says "กันพลาสติก",
  "ผิวพลาสติก / หน้าตุ๊กตา / ดูเป็น AI / ไม่เนียน", "เขียน prompt ละเอียดแบบ hyperreal",
  or asks to rewrite a prompt so the output stops looking fake/CGI/airbrushed.
  Output = diagnose → medium-first → 5-axis evidence (M·T·P·I·L) → full prompt
  (7-block video / 8-dimension image) → self-audit pass → negative arsenal.
  Do NOT trigger for position/continuity locking (use seedance-shot-continuity) or the full
  production pipeline (use siamshort_auto_loop) — this skill is the "realism/texture layer"
  those pipelines call whenever a prompt gets written.
---

# Anti-Plastic / Hyperreal Detail

> Master source: `Desktop/Fable/Siamshort auto technique/05_ANTI-PLASTIC-HYPERREAL.md`
> ตัวอย่าง prompt ต้นทาง (verbatim): `Prompt-Library/06_hyperreal-sports-speed.md` [SPD-002..004]
> Golden examples ต่อ genre: `reference/genre-recipes.md`

## หลักคิดแกนกลาง

**ภาพจริงไม่ได้จริงเพราะคำว่า "realistic, 8K" — มันจริงเพราะมี "ร่องรอยของโลกจริง" (reality evidence).**
ละเอียดถูกจุด ≠ ละเอียดเยอะ. ทุก prompt ต้องฉีดหลักฐาน 5 แกน + negative เชิงรุก:

| แกน | คำถามที่ต้องตอบ | ตัวอย่างหลักฐาน |
|-----|----------------|----------------|
| **M — MEDIUM** | ใครถ่าย? กล้องอะไร? ฟุตนี้มีอยู่จริงได้ยังไง? | consumer DV 2000s เพื่อนถ่าย / HD broadcast / 35mm หนัง HK 90s |
| **T — TEXTURE** | แสงตกกระทบ "พื้นผิว" อะไรบ้าง? | pores, peach fuzz catching sunlight, ไหมชุ่มเหงื่อ, สนิมดาบ |
| **P — PHYSICS** | น้ำหนัก/แรง/ผลกระทบอยู่ตรงไหน? | เข่ายุบตอนลงพื้น, fabric lag, แรงปะทะดันถอย, ลมพัดปีกหมวก |
| **I — IMPERFECTION** | อะไร "พลาด" แบบมนุษย์/อุปกรณ์? | AF hunt, whip pan เลยเป้า, rolling shutter, จับ moment ช้าไปนิด |
| **L — LIFE** | โลกรอบ subject ยังหมุนต่อยังไง? | คนข้างๆ เชียร์เบลอๆ, ใบไผ่ร่วงต่อเนื่อง, เสียงเก้าอี้เอี๊ยด |
| **+N — NEGATIVE** | แบนอะไรเชิงรุก? | plastic skin, poreless, airbrushed, doll face, CGI, posing |

> **กฎเหล็ก: เปลี่ยน genre = เปลี่ยน "ชุดหลักฐาน" — ไม่ใช่เปลี่ยนโครง.**

## รากเหง้าความพลาสติก 5 ข้อ (สิ่งที่ต้องสั่งทับ default ของโมเดล)

1. **Perfection default** — ผิวเรียบ แสงแฟลต เฟรมกลางเป๊ะ → สั่งความไม่สมบูรณ์อย่างเจาะจง
2. **ไม่มี medium** — ภาพลอยในสุญญากาศ → ประกาศ medium แล้ว flaw ทั้งตระกูลตามมาอัตโนมัติ
3. **Subject รู้ตัวว่าถูกถ่าย** — pose = ตุ๊กตา → caught mid-moment, unaware of camera, micro-behavior
4. **แสงเป็น "สี" ไม่ใช่ "ฟิสิกส์"** → เขียนแสงแบบ "ตกกระทบอะไร" (เงาปีกหมวกเคลื่อนบนหน้า, เมฆเคลื่อน→แสงเปลี่ยน)
5. **โลกหยุดรอ subject** — ฉากหลังเป็นวอลเปเปอร์ → โลกมีชีวิตต่อเนื่องทั้งช็อต + เสียง ambient ลิสต์เป็นข้อๆ

## วิธีเขียนแต่ละแกน

### M — MEDIUM (ตัวคูณใหญ่สุด — เลือกก่อนเสมอ)
ประกาศ 3 ชั้น: **อุปกรณ์ + คนถือ + เหตุผลการมีอยู่ของฟุตเทจ** แล้วลิสต์ flaw ประจำตระกูล 4–6 ข้อ
ปิดด้วยสิ่งที่ medium นั้น "ไม่มี" (*no stabilization, no cinematic moves, no modern color grade*).
ตัวอย่าง: "กล้อง DV ยุค 2000s เพื่อนถ่ายเล่น" → AF hunt + lens breathing + rolling shutter + สีซีด + noise มาฟรีทั้งชุด

### T — TEXTURE
ผิว: pores → peach fuzz **catching the sunlight** → *not airbrushed* (ผูก texture กับแสงเสมอ).
ผ้า: ชนิด + น้ำหนัก + สภาพ (ยับ/ลุ่ย/รอยชุน). ของ/ฉาก: ทุกชิ้นมีอายุ (สนิม รอยบิ่น คราบ).

### P — PHYSICS
ร่างกายมีน้ำหนัก (weight shifted forward, เข่ายุบ), ผ้า/ผมตามหลังการเคลื่อนไหวครึ่งจังหวะ,
ทุกแรงมีผลลัพธ์ (โดนฟัน→เซถอยจริง), action = **ท่าจริงของศาสตร์นั้น** (กฎ DAN)
⚙️ **แรงตั้งต้นใหญ่ (ของตก/แตก/สาด/หก/ล้ม/ชน) → ขยายเป็นลูกโซ่เต็ม 5 ชั้นด้วยสกิล `physics-guide`**
(เทคนิค 06 — object audit → primary → cascade → reflex-ก่อน-อารมณ์ → continuity ของเศษ/คราบ)

### I — IMPERFECTION (3 ระดับ ใส่ให้ครบ)
อุปกรณ์พลาด (AF วืด, noise) + คนถ่ายพลาด (เฟรมเบี้ยว, whip pan เลยเป้า, **จับ moment ช้าไปนิด**)
+ โลกพลาด (ธง/ไหล่คนตัดหน้าเลนส์, ฝุ่นแตะเลนส์)

### L — LIFE
คนรอบข้างมีกิจกรรมของตัวเอง, ธรรมชาติขยับต่อเนื่อง (ใบไม้ร่วง เมฆเคลื่อน),
เสียงลิสต์เฉพาะที่มีจริงในฉาก + ปิดท้าย "ไม่มีดนตรี/บรรยาย"

### +N — NEGATIVE ARSENAL (3 กลุ่ม)
กันพลาสติก (plastic skin, poreless, airbrushed, doll face, waxy, CGI) ·
กันพฤติกรรม AI (posing, looking at lens, slow-motion ไม่ได้สั่ง, frozen expression) ·
กันหลุดโลก+ปลอดภัย (deformed hands, garbled text, extra people, real logos/public figures)

## โครงวิดีโอ 7 บล็อก (มาตรฐาน pton time-code + ชั้น anti-plastic)

1. **ตัวละครหลัก** — identity lock + T (ผิว texture + สภาพเสื้อผ้า)
2. **สถานที่** — anchor รายโซน + L (สิ่งที่ขยับต่อเนื่อง + พฤติกรรมแสง)
3. **สไตล์ภาพ** — genre look + *สารคดีเหนือจริง, spontaneous, unaware of camera*
4. **สไตล์กล้อง** — M+I: medium 3 ชั้น + flaw list + สิ่งที่ medium ไม่มี
5. **Time-code beats** — P: ทุก beat มี micro-behavior ที่มีน้ำหนัก (มือจับขอบหมวก, ไหล่กระตุก, ส้นเท้าครูด)
6. **เสียง** — L: เสียงจริงในฉากเป็นข้อๆ + "ไม่มีดนตรี/บรรยาย"
7. **⛔/เป้าหมาย** — N 3 กลุ่ม + ประโยคเป้าหมายอารมณ์ 1 ประโยค (*"เหมือนคลิปครอบครัวยุค 2000s ที่ถูกลืม"*)

## โครงภาพนิ่ง 8 มิติ

ตัวละคร(ผิวผูกแสง) → เนื้อผ้า+การตัดเย็บ(แทนบรรยายร่างกาย) → โมเมนต์สีหน้า(caught mid-reaction)
→ เลนส์(telephoto compression, DOF, foreground occlusion) → แสง×ผิว(ฟิสิกส์) → พื้นหลังมีชีวิต+bokeh
→ medium/คุณภาพ(ประกาศเสมอ + diegetic details เช่นแถบ broadcast สมมุติ **อังกฤษเท่านั้น**) → negative arsenal

## META-LOOP (ให้โมเดลเขียนเอง — ดีกว่า one-shot ~20%)

1. ตั้งบทบาทผู้เชี่ยวชาญระดับท็อปก่อนเสมอ
2. บังคับวิเคราะห์รากเหง้า "ทำไมพลาสติก" ก่อนเขียน
3. จบด้วย **self-audit**: หาจุดเสี่ยงกลิ่น AI ≥3 จุด แล้วแก้เป็น final
4. คาถา refine: *"ปรับปรุงอีกครั้ง ให้แต่ละมิติลงพื้นดินมากขึ้น"*

## WORKFLOW เมื่อถูกเรียก

1. รับโจทย์ (genre, subject, ratio, engine, เดี่ยว/ใน chapter)
2. DIAGNOSE ผลงานเดิม (ถ้ามี) → ชี้รากเหง้าที่โดน
3. เลือก MEDIUM ก่อน (3 ชั้น)
4. เติม T/P/I/L ตาม genre recipe → `reference/genre-recipes.md`
5. เขียนเต็มโครง 7 บล็อก / 8 มิติ
6. SELF-AUDIT ≥3 จุด → แก้เป็น final
7. ปิดด้วย negative arsenal

## ข้อควรระวังกับ pipeline เดิม

- ใน shot-continuity loop: imperfection ระดับ "เบา–กลาง" เท่านั้น — เฟรมโยนแรงเกิน anchor/side-lock อ่านไม่ออก
- medium ประกาศระดับ chapter (system prompt) ให้เหมือนกันทุกช็อต กัน grain/สีเพี้ยนข้ามช็อต
- text บนจอ = อังกฤษเท่านั้น ; กฎเดิมครบ: 15s/ช็อต, ⛔POSITION, 音效, &scene VA, OK-gate, **pton กด gen เอง**
