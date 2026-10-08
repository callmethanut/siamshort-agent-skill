---
name: seedance-shot-continuity
description: >-
  Build a Seedance/Fable video drama ONE SHOT AT A TIME with locked character
  positioning and shot-to-shot continuity. Use when the user wants to gen video
  shot-by-shot via the Fable MCP, says "ทำวิดีโอทีละช็อต", "gen video ต่อเนื่อง",
  "position lock / ล็อกตำแหน่ง", "วิเคราะห์วิดีโอก่อนหน้าแล้วทำอันต่อไป", "ไม่ให้ slop /
  ไม่ให้เพี้ยน", or "/seedance-shot-continuity". The loop: lock prompt → gen 9:16 →
  analyze the WHOLE clip → fix slop / read true positions → lock next shot.
  Do NOT trigger for one-off image gen (gpt-image) or storyboard sheets (storyboard).
---

# Seedance Shot Continuity Loop

วิธีปั้นหนัง Seedance/Fable แบบ **ทีละช็อต** ให้ตัวละคร **อยู่ตำแหน่งเดิมต่อเนื่อง** และ
**ไม่ slop/ไม่เพี้ยน** มากที่สุด — gen ช็อต → วิเคราะห์ทั้งคลิป → ปรับช็อตถัดไป → ล็อกตำแหน่ง → ทำต่อ.

> สรุปบทเรียนจริงจากโปรเจกต์ กุหลาบเผาใจ (Fable MCP + BytePlus Seedance 2.0). ใช้คู่กับ
> memory `fable-mcp-video-gen-workflow`, `seedance-multichar-clone-guard`,
> `seedance-onscreen-text-english-only`, และ skill `seedance-continuity-director`.

---

## THE LOOP — ต่อช็อต N

1. **ล็อก prompt SB(N)** — scene-lock + position-lock + anti-slop guards (ดูด้านล่าง).
2. **Gen 9:16:** `regen_shot_video(shotUid, ratio "9:16", resolution "720p", model "seedance_2.0", duration 15)`.
   ❌ อย่าใช้ `story_gen_video_next` — มันล็อก **16:9 เสมอ** (ไม่มี param ratio).
3. **Poll:** `poll_video_byteplus(taskId)` จน `status: success` (~4–7 นาที). เก็บ `videoUrl`.
4. **โหลด + วิเคราะห์ "ทั้งคลิป"** (grid 16 เฟรม + เฟรมเต็มจุดสำคัญ — ดู ANALYSIS).
5. **ตัดสิน PASS / FAIL:**
   - ❌ FAIL ถ้า: ตำแหน่งผิด/teleport/morph, เพี้ยน (หน้าเบี้ยว/อนาโตมีพัง), **โคลน/ตัวซ้ำ**,
     **แตกจอ/สองท่อน/split**, ฉากผิด (ไม่ตรง ref), ratio ผิด, ช่วง 14–15s พัง.
6. **FAIL → ปรับ prompt เฉพาะจุด → regen.** เพดาน **4 ครั้ง/ช็อต**, ปรับทุกครั้ง; ครบ 4 ยังไม่ได้
   ก็ **รับตัวที่ดีสุด แล้วไปช็อตต่อไป**.
7. **PASS → อ่านตำแหน่งจริงตอนจบ → ล็อกเข้า prompt SB(N+1)** ให้ต่อเนื่องเป๊ะ.
8. **ประหยัดเวลา:** ระหว่าง SB(N) เรนเดอร์ ให้ **เขียน prompt SB(N+1) ดักไว้** (pipeline).

> ⚠️ แม้ช็อตจะ FAIL และต้องข้าม ก็ **ต้องอ่านตำแหน่งจริงให้ถูก** เพื่อไม่ให้ช็อตถัดไปเพี้ยนตาม.

> 🔗 **(Optional — เมื่อ user ต้องการ "ต่อภาพ/ต่อ motion" เป๊ะจากช็อตก่อน):** แทรกก่อนข้อ 1 ของ SB(N) —
> `capture_video_frame` (ภาพนิ่ง = มุม/องค์ประกอบ) หรือ `trim_reference_video` (วิดีโอ = การเคลื่อนไหว) จากช็อตก่อน
> → `add_ref_asset_to_shot` → อ้าง `%ref` ใน prompt SB(N). คุม **"เอามุม/มูฟเมนต์ ไม่เอาลุค/แสง"** ตาม **§3**.
> ปกติ continuity ใช้แค่ scene-VA + position-lock ก็พอ — งัด ref asset มาเมื่อ user ขอความต่อเนื่องของภาพ/การเคลื่อนไหวจริงๆ.

---

## 1) SCENE LOCK — ให้ "รูป ref" คุมฉาก ไม่ใช่ตัวอักษร  ⭐ บทเรียนใหญ่สุด

- `regen_shot_video` **ไม่แนบรูป scene อัตโนมัติ** (ใช้แค่ VA ตัวละคร) → ถ้าไม่ทำอะไร ฉากจะ drift เป็น
  ห้องหรู/ฝรั่ง/มั่ว.
- **แต่ถ้าบรรยายฉากยาวเป็นตัวอักษร** (เพดานคานขื่อ/แท่นบูชาทอง/ฯลฯ) → Seedance **"มโนฉากใหม่ตามคำ"**
  กลายเป็นที่ที่ไม่ใช่รูป ref เลย.
- ✅ **สูตรที่ถูก:** `&ชื่อSceneVA` (mention) + **ข้อความฉากสั้นที่สุด**:
  ```
  Location: ใช้ฉากเดิมตามรูปอ้างอิง &ชื่อScene เป๊ะทุกอย่าง (สถานที่เดิม + เวลา/แสง) —
  ❗ห้ามเปลี่ยนฉาก ห้ามสร้างสถานที่ใหม่ ห้ามแต่ง/เพิ่มของในฉาก.
  Use the SAME EXACT location as reference image &ชื่อScene; do NOT reinvent or alter the set.
  ```
- Scene VA ต้อง `byteplusSyncStatus: "ready"` (เช็ค `list_virtual_assets`; ถ้ายังไม่ ready →
  `sync_virtual_asset_byteplus`). รูป ref แบบ 2 พาเนล (front+back) ใช้เป็น mention ได้ ไม่ทำให้วิดีโอแตก
  (ถ้าคุม anti-split).
- ใส่เฉพาะ **เวลา/แสง/มู้ด** เป็นคำได้ (ค่ำ/แสงเทียน/golden hour) — นั่นคือ "บรรยากาศ" ไม่ใช่ "สร้างสถานที่".

---

## 2) POSITION LOCK — ล็อกตำแหน่งตัวละคร

- วาง **แผนผังตำแหน่งคงที่ทั้งซีน** (ใครยืนโซนไหน) แล้วยึดทุกช็อต. ตัวอย่าง (กุหลาบ ฉากงานศพ):
  *โรส = โซนหน้า ใกล้หีบศพ · แม่ = ปลายทางเข้า/ท้ายศาลา · ทศ เข้าจากท้าย→ขึ้นหน้า · วิน เข้าหาโรสหน้า.*
- ทุก prompt ใส่ **โซน + anchor** ของแต่ละตัวชัด: `@X ยืนหน้าสุดใกล้ $หีบศพ; @Y ยืนปลายทางเข้า (ไกล)`.
- **อ่านตำแหน่งจาก "วิดีโอจริง"** ไม่ใช่เดา — โมเดล drift ได้ ต้องดูทั้งคลิปแล้วจับว่าจริงๆ ใครอยู่ไหน
  แล้วค่อยล็อกช็อตถัดไปตามนั้น.
- เปิด SB(N+1) ด้วยประโยค `[POSITION LOCK ต่อจาก SB(N): ...]` ที่ตรงกับ **ตอนจบจริง** ของ SB(N).
- ระยะห่างไกลสองฝั่ง ใช้ **OTS deep-focus เฟรมเดียว** (ไหล่คนหน้า → อีกคนเล็กๆ ท้าย) อย่าใช้ wide
  ที่พยายามโชว์ "สองปลายสุดพร้อมกัน" — มันจะ **แตกเป็นสองท่อน**.
- ⭐ **[CAM/BG LOCK] ปัก "ทิศกล้อง + ฉากหลังรายตัว" ทุก cut** — กันเพี้ยน/กลับด้านได้ดีที่สุด.
  ระบุทุกช็อต/ทุกคัท: (1) กล้องหันทางไหน (เข้าแท่นบูชา/หน้า หรือ ทางเข้า/ท้าย) (2) หลังตัวละครแต่ละคนเห็นอะไร เช่น
  `@วิน หลัง=แท่นบูชาทอง+หีบศพ` / `@โรส หลัง=ทางเข้า+แขก`. **เหตุผล:** ถ้าไม่ปัก BG, Seedance จะดูดตัวละคร
  ไปหา anchor ที่เด่นสุด (แท่นบูชาทอง) → ย้ายจุด/กลับด้าน (เคสจริง: SB13 แม่เด้งไปหน้าหีบศพ, SB17↔18 วินคนละจุด).
  ช็อตคู่เดิมต่อเนื่อง → สั่ง `ฉากหลังเหมือน SB(N) เป๊ะ` เพื่อล็อกมุมให้ตรงกัน.

---

## 3) REFERENCE ASSETS — ดึงภาพ/วิดีโอจาก StoryBox ก่อนหน้ามาเป็น `%ref`  ⭐

Reference Asset = image/video เก็บ **ระดับ Chapter** → ใช้ `%name` ใน prompt ของ StoryBox (shot) ไหนก็ได้
ใน chapter เดียวกัน. ใช้ตอนอยากให้ช็อตใหม่ **ต่อเนื่องจากช็อตก่อนหน้า** — เอา **มุม/องค์ประกอบ** (จากภาพนิ่ง)
หรือ **การเคลื่อนไหว** (จากวิดีโอ) มาอ้างอิง โดยไม่ต้องบรรยายเป็นคำยาวๆ. ทุก tool มีครบใน Fable MCP แล้ว.
📄 รายละเอียดเต็ม + error table: `reference/reference-assets-guide.md`.

| tool | ทำอะไร | ได้ → คุมอะไร |
|---|---|---|
| `capture_video_frame` | จับ 1 เฟรม (วินาทีไหนก็ได้ / `-1`=last) | **image ref** → composition / มุมกล้อง / ลุค |
| `trim_reference_video` | ตัดช่วง **1–15 วิ** จากวิดีโอ | **video ref** → **motion** (Seedance ลอกการเคลื่อนไหว) |
| `add_ref_asset_to_shot` | แนบ ref เข้า shot → ใช้ `%name` | — (สร้าง VA ให้อัตโนมัติ Ark/BytePlus) |
| `list_reference_assets` | ดู ref ทั้ง chapter (กันแนบซ้ำ) | — |

**Flow:**
1. **ภาพ:** `capture_video_frame(projectUid, chapterUid, videoUrl, timeSec, name)` → `{uid,name,url}`
   **มูฟเมนต์:** `trim_reference_video(projectUid, chapterUid, sourceVideoUrl, startSec, endSec, name)` → `{uid,name,url}`
2. `add_ref_asset_to_shot(shotUid, assetUrl, assetName, mediaType, assetUid?)` — `mediaType` = `"image"` (เฟรม) / `"video"` (trim).
3. `update_shot(shotUid, seedancePrompt)` → เขียน prompt ที่อ้าง `%name`.

**จำไว้:**
- **per-Chapter:** สร้างครั้งเดียวใช้ได้ทุก shot ใน chapter; URL ที่ได้ **permanent ไม่ expire**.
- `timeSec` ใส่วินาทีไหนก็ได้ (0, 2.5, 6, 14.9…) ไม่ใช่แค่ last frame; trim ต้อง `endSec − startSec = 1–15s`.
- อ้างได้ 2 ทาง: `add_ref_asset_to_shot` (แนะนำ — ตั้งชื่อ `%name` เอง) หรือพิมพ์ `%uid` ตรงใน prompt.
- **image ref = composition/style · video ref = motion** — เลือก `mediaType` ให้ตรงงาน.
- ก่อนแนบ → `list_reference_assets(chapterUid)` เช็คก่อน (ชื่อ/URL ซ้ำ → error "already exists").
- URL ต้นทางต้องสด (จาก video-gen result) ไม่งั้น "Failed to download"; `timeSec` เกิน duration → ลด/ใช้ `-1`.

```json
// A) ภาพนิ่ง: capture เฟรมวินาที 14 ของ SB15 → %sb15_angle
{ "tool": "capture_video_frame",
  "arguments": { "projectUid": "...", "chapterUid": "...",
    "videoUrl": "https://cdn/.../sb15.mp4", "timeSec": 14, "name": "sb15_angle" } }
// → { uid: "abc", name: "sb15_angle", url: "https://cdn/.../frame.jpg" }

// B) มูฟเมนต์: trim 5 วิจาก SB15 → %sb15_motion
{ "tool": "trim_reference_video",
  "arguments": { "projectUid": "...", "chapterUid": "...",
    "sourceVideoUrl": "https://cdn/.../sb15.mp4", "startSec": 5, "endSec": 10, "name": "sb15_motion" } }

// C) แปะเข้าช็อตปลายทาง (เลือก mediaType ให้ตรง)
{ "tool": "add_ref_asset_to_shot",
  "arguments": { "shotUid": "<target>", "assetUrl": "https://cdn/.../frame.jpg",
    "assetName": "sb15_angle", "mediaType": "image" } }
```

### ⚠️ กฎเหล็ก (image ref) — เอา "มุมกล้องอย่างเดียว" ห้ามลอกลุค
เฟรมที่ตัดมา Seedance จะ **ลอกทั้งมุม + graphic style + แสง/สี** ถ้าไม่สั่งห้าม → ต้องกำกับชัดใน prompt:
- ✅ ใช้ `%name` เป็น **"ตัวอย่างมุมกล้อง (camera-angle reference) เท่านั้น"** — ลอกเฉพาะ **ANGLE + FRAMING +
  ตำแหน่งตัวละคร**, และใช้ **เฉพาะเฟรมเปิด (0s) เท่านั้น**.
- ❌ **ห้ามลอก graphic style + แสง/สีของรูป** — ให้ใช้ลุคที่กำหนดในช็อตแทน (เช่น **found-footage แดดทอง**).
- ประโยคกำกับ (วางในช็อตปลายทาง):
  ```
  ใช้ %sb15_angle เป็น "ตัวอย่างมุมกล้องเท่านั้น (camera-angle reference ONLY)" สำหรับเฟรมเปิด 0s —
  ลอกเฉพาะ angle + framing + ตำแหน่งตัวละคร.
  ❗ห้ามลอกสไตล์ภาพ/แสง/สีจากรูปนี้ — ใช้ลุค found-footage แดดทอง (golden hour, แสงแดดธรรมชาติ,
  มือถือถ่ายสั่นเล็กน้อย) ตามที่กำหนดในช็อตนี้แทน.
  Use %sb15_angle as a CAMERA-ANGLE reference ONLY (opening frame): copy framing & character positions;
  do NOT copy its graphic style / lighting / color — keep the found-footage golden-sun look defined here.
  ```
> **video ref (motion):** ใช้หลักเดียวกัน — สั่ง "ลอก **การเคลื่อนไหว** จาก `%ref` แต่ **มุม/ลุค/แสง** ตามที่กำหนดในช็อตนี้".
> ใช้คู่กับ **[CAM/BG LOCK] (§2)**: frame ล็อก "มุม" จากภาพจริง · CAM/BG ล็อก "ทิศกล้อง + ฉากหลังรายตัว" เป็นคำ — เสริมกัน.

---

## 4) ANTI-SLOP GUARDS — ใส่ทุก prompt

- **Anti-clone (นับคนเป๊ะ):**
  ```
  [ANTI-CLONE] ตัวละครหลัก N คนเท่านั้น: @A , @B — อย่างละ 1 ห้ามโคลน/ทำซ้ำ/มิเรอร์.
  แขกฉากหลังเป็น extras นั่ง หน้าทั่วไปหลากหลาย ห้ามซ้ำหน้าตัวละครหลัก.
  EXACTLY N named characters, each appears EXACTLY once.
  ```
  ถ้ามีคน "ยืนเด่น" คนเดียวท่ามกลางคนนั่ง → ย้ำ **"มีคนยืนคนเดียว = X ที่เหลือนั่งหมด"** (กันโคลนตัวยืน).
- **Anti-split:** `ONE single continuous frame, ONE camera; ❌ห้ามแบ่งจอ/สองท่อน/two-panel/stack/grid
  แม้ในช็อต wide.` (Seedance ชอบลอก layout 2 พาเนลจากรูป ref มาเป็น split.)
- **กล้อง:** `ระดับสายตา ตัดฉับ hard cut; ❌ห้ามมุมสูง/overhead/crane/CCTV` — มุมก้ม/เครนทำ Seedance **เพี้ยน**.
  มุมเท่ (low-angle reveal / eye-duel) เก็บไว้เฉพาะ **ช็อตเปิดตัว + ไคลแม็กซ์** และคุมให้ไม่สุดขั้ว.
- **ตัวหนังสือ:** Seedance เรนเดอร์ไทยบนภาพไม่ได้ → SFX/overlay เป็นอังกฤษเท่านั้น; **บทพูดไทยได้** (เป็นเสียง).

---

## 5) SHOT CONSTRUCTION

- เปิด 0s ด้วย **close-up** เสมอ → ตัดฉับสลับ CU ↔ medium ↔ OTS (ไม่แพนเวียน = ไม่เวียนหัว).
- เติม 15 วิ ด้วย **emotion close-up ของตัวละครที่อยู่ในช็อต** (เก็บ footage ไว้ตัดต่อ).
- จบด้วย **เฟรมเดียวที่อ่านตำแหน่งได้** (OTS deep-focus / CU อารมณ์) — ไม่บังคับ wide เสมอไป.
- บทพูด/VO เขียนเป็น `บทพูด @X : "..."` และ `VOICE OVER (เสียง @X ไทย): "..."`.
- **แทรกช็อตเสริมเล่าเรื่อง** ได้: flashback / reveal — สร้างด้วย `create_shot(sortOrder = 10.5)` คั่นกลาง.
  Flashback ให้ **ลุคต่างชัด** (warm 8mm memory vs ปัจจุบันเย็นๆ) + ฉาก flashback บรรยายเป็นคำได้
  (เพราะไม่มี ref ต้อง match) + เลี่ยงผูก VA ผู้ใหญ่ถ้าต้องการเวอร์ชันเด็ก.

---

## 6) ANALYSIS PROTOCOL — ดูทั้งคลิป ไม่ใช่แค่เฟรมท้าย

```bash
# ratio (9:16 = 720x1280)
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 in.mp4
# grid 16 เฟรมคลุม 0-15s
ffmpeg -y -i in.mp4 -vf "fps=1,scale=240:-1,tile=4x4" -frames:v 1 grid.png
# เฟรมเต็มจุดสำคัญ (เปลี่ยน T)
ffmpeg -y -ss T -i in.mp4 -frames:v 1 -q:v 2 fT.jpg
```
- ❗**อย่าเชื่อเฟรมสุดท้ายจาก `-sseof` อย่างเดียว** — บางทีจับรอยตัดพอดี เห็นเป็น "สองท่อน" หลอกตา.
- ❗**อย่า hstack เฟรมหน้าคนติดกันหลายเฟรม** — ภาพเบลนกันจะดูเหมือน "จูบ/ตัวซ้อน" หลอกตา. ดูเฟรมเดี่ยว full-res.
- เทียบฉากกับ **รูป ref จริง** (เทียบพาเนลที่มุมเดียวกัน) ก่อนตัดสินว่าฉากตรงไหม.
- เช็คลิสต์ทุกช็อต: ตำแหน่งถูก/นิ่ง · ไม่เพี้ยน · ไม่โคลน · ไม่แตกจอ · ฉากตรง ref · 9:16 · 14–15s โอเค.
- มี `scripts/analyze_shot.sh <url> <name>` ช่วยโหลด+grid+ratio+เฟรมสำคัญในคำสั่งเดียว.

---

## 7) MCP CHEAT-SHEET (Fable server)

| งาน | tool |
|---|---|
| ดูช็อตทั้ง chapter + uid + prompt | `list_shots(chapterUid)` |
| แก้ prompt/positions/links | `update_shot(shotUid, seedancePrompt, characterIds, sceneIds, itemIds, presetText)` |
| แทรกช็อตใหม่คั่นกลาง | `create_shot(chapterUid, sortOrder=10.5, presetText, seedancePrompt)` |
| **gen วิดีโอ 9:16** | `regen_shot_video(shotUid, ratio "9:16", resolution "720p", model "seedance_2.0", duration 15)` |
| poll | `poll_video_byteplus(taskId)` → success + videoUrl + lastFrameUrl |
| เช็ค VA ฉากพร้อมยัง | `list_virtual_assets` → `byteplusSyncStatus: ready`; ไม่พร้อม → `sync_virtual_asset_byteplus` |
| **(§3)** ตัดเฟรมวิดีโอ → image ref (มุม/ลุค) | `capture_video_frame(projectUid, chapterUid, videoUrl, timeSec, name)` → `{uid,name,url}` |
| **(§3)** ตัดช่วงวิดีโอ 1–15s → video ref (motion) | `trim_reference_video(projectUid, chapterUid, sourceVideoUrl, startSec, endSec, name)` → `{uid,name,url}` |
| **(§3)** แปะ ref เข้าช็อตปลายทาง (ใช้ `%name`) | `add_ref_asset_to_shot(shotUid, assetUrl, assetName, mediaType, assetUid?)` |
| **(§3)** ดู ref ทั้ง chapter (กันซ้ำ) | `list_reference_assets(chapterUid, mediaType "all")` |

- ค่าใช้จ่าย ~**45–55 credits / คลิป 15s 720p**.
- ใช้ background sleep ~270–290s ระหว่างรอ poll (กันยิงถี่เกิน) แล้วค่อย poll.

---

## QUICK CHECKLIST ต่อช็อต
- [ ] `&SceneVA` + scene-text สั้น (ห้ามบรรยายฉากยาว)
- [ ] `[POSITION LOCK ต่อจาก SB(N-1)]` ตรงกับตอนจบจริง
- [ ] เปิด close-up, ตัดฉับ, eye-level (ไม่มุมสูง)
- [ ] (ถ้า user ขอต่อภาพ/motion จากช็อตก่อน, §3) capture/trim → `add_ref_asset_to_shot` → `%ref` ; เอามุม/มูฟเมนต์ ❌ห้ามลอกลุค/แสง
- [ ] `[ANTI-CLONE]` นับคนเป๊ะ + "ยืนคนเดียว=X ถ้ามี"
- [ ] `[ANTI-SPLIT]` เฟรมเดียว ห้ามสองท่อน
- [ ] บทพูดไทย / SFX อังกฤษ / ไม่มีตัวหนังสือไทยบนภาพ
- [ ] gen 9:16 → poll → วิเคราะห์ทั้งคลิป → PASS หรือ regen (≤4)
- [ ] อ่านตำแหน่งจริง → ล็อกช็อตถัดไป
