# MCP Reference Assets Guide — Capture, Edit & Trim

## สำคัญมาก: %name ไม่ใช่ %uid

ระบบใช้ **`%name`** ในการอ้างอิง reference ใน prompt — **ไม่ใช่ `%uid`**

```
✅ ถูก:  %sb21_rose_study       (ใช้ name ที่ตั้งตอน capture/trim/edit)
❌ ผิด:  %uw2vlgznmqs7k550     (นี่คือ uid — ห้ามใช้!)
```

---

## Overview

Reference Assets เก็บ **ระดับ Chapter** — สร้างครั้งเดียว ใช้ได้กับทุก StoryBox (shot) ใน Chapter นั้น

**เครื่องมือหลัก:**

| Tool | ทำอะไร | Output สำคัญ |
|------|--------|-------------|
| `capture_video_frame` | จับเฟรมจากวิดีโอ (เวลาไหนก็ได้) | `{uid, name, url}` |
| `edit_reference_asset` | Edit รูปด้วย GPT-Image-2-Edit (XSkill) | `{uid, name, url}` |
| `trim_reference_video` | ตัดบางช่วง 1-15 วินาที | `{uid, name, url}` |
| `add_ref_asset_to_shot` | แนบ ref เข้า shot → ใช้ `%name` ใน prompt | — |
| `list_reference_assets` | ดูรายการ ref ทั้งหมดใน chapter | array of assets |

---

## Workflow 2 แบบ

### A) ใช้ตรง (ไม่ edit)

```
1. capture_video_frame / trim_reference_video  → ได้ {name, url}
2. add_ref_asset_to_shot                       → assetName = name
3. เขียน prompt: %sb21_rose
```

### B) Capture → Edit → Ref (แนะนำ!)

```
1. capture_video_frame     → ได้ {name, url} ของเฟรม
2. edit_reference_asset    → ส่ง url + editPrompt → GPT-Image-2 Edit → ได้รูปใหม่ {name, url}
3. add_ref_asset_to_shot   → assetName = edited name
4. เขียน prompt: %sb21_rose_edited
```

---

## 1. capture_video_frame

จับ **เฟรมเดียว** จากวิดีโอ ณ เวลาที่ระบุ → ได้ภาพ JPEG

**ไม่ได้จำกัดแค่ last frame!** — ใส่ `timeSec` เป็นเลขวินาทีไหนก็ได้

### Input

```json
{
  "projectUid": "IZdhOv0kfK4fi_R1",
  "chapterUid": "pubWeymO6q8RzUut",
  "videoUrl": "https://...mp4",
  "timeSec": 6,
  "name": "sb21_rose_study"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectUid` | string | **Yes** | UID ของ project |
| `chapterUid` | string | **Yes** | UID ของ chapter |
| `videoUrl` | string | **Yes** | URL ของวิดีโอ (ใช้ URL จาก video gen result) |
| `timeSec` | number | No | **เวลาที่ต้องการจับ (วินาที)** — ใส่ 0, 3, 6.5, 12... ได้หมด; `-1` = เฟรมสุดท้าย (default: -1) |
| `name` | string | No | **ชื่อ asset — นี่คือสิ่งที่ใช้กับ % ใน prompt!** เช่น `sb21_rose_study` → ใช้ `%sb21_rose_study` |

### Output

```json
{
  "uid": "uw2vlgznmqs7k550",
  "name": "sb21_rose_study",
  "url": "https://d2xsxph8kpxj0f.cloudfront.net/.../ref-assets/1/uw2vlgznmqs7k550-frame.jpg",
  "captureTimeSec": 6,
  "usage": "To use in prompts: 1) call add_ref_asset_to_shot with assetName='sb21_rose_study'..., 2) then write %sb21_rose_study in the shot prompt. Do NOT use %uw2vlgznmqs7k550."
}
```

---

## 2. edit_reference_asset (ใหม่!)

Edit รูปด้วย **XSkill GPT-Image-2-Edit** → สร้าง reference asset ใหม่

ใช้สำหรับ:
- ลบ/เปลี่ยน background
- แก้ไข lighting, สี, mood
- เพิ่ม/ลบ elements
- ปรับ composition

### Input

```json
{
  "projectUid": "IZdhOv0kfK4fi_R1",
  "chapterUid": "pubWeymO6q8RzUut",
  "sourceImageUrl": "https://...frame.jpg",
  "sourceAssetUid": "uw2vlgznmqs7k550",
  "editPrompt": "Remove background, add dramatic rain and neon lighting",
  "name": "sb21_rose_rain",
  "ratio": "16:9"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectUid` | string | **Yes** | UID ของ project |
| `chapterUid` | string | **Yes** | UID ของ chapter |
| `sourceImageUrl` | string | **Yes** | URL ของรูปต้นทาง (จาก capture_video_frame result `url`, หรือ URL รูปใดๆ) |
| `sourceAssetUid` | string | No | UID ของ asset ต้นทาง (จาก capture result `uid`, สำหรับ tracking) |
| `editPrompt` | string | **Yes** | **คำอธิบายการ edit** (ภาษาอังกฤษแนะนำ) |
| `name` | string | No | **ชื่อ asset ใหม่ — ใช้กับ % ใน prompt!** เช่น `sb21_rose_rain` → `%sb21_rose_rain` |
| `ratio` | string | No | Aspect ratio: `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `3:2`, `2:3` (default: `16:9`) |

### Output

```json
{
  "uid": "abc123xyz",
  "name": "sb21_rose_rain",
  "url": "https://d2xsxph8kpxj0f.cloudfront.net/.../ref-assets/1/edit-1719...-abc.png",
  "editPrompt": "Remove background, add dramatic rain and neon lighting",
  "ratio": "16:9",
  "usage": "To use this edited image in prompts: 1) Call add_ref_asset_to_shot with assetName=\"sb21_rose_rain\", assetUrl=\"https://...\", mediaType=\"image\". 2) Then write %sb21_rose_rain in your shot prompt. Do NOT use %abc123xyz."
}
```

### ตัวอย่าง editPrompt

| ต้องการ | editPrompt |
|---------|-----------|
| ลบ background | `"Remove background and replace with cyberpunk cityscape at night"` |
| เปลี่ยนแสง | `"Add dramatic golden hour lighting from the left side"` |
| เปลี่ยนสีผม | `"Change hair color to blue with purple highlights"` |
| เพิ่มฝน | `"Add heavy rain with reflections on the ground"` |
| ลบตัวละครอื่น | `"Remove all other characters, keep only the main character"` |
| เปลี่ยน mood | `"Make it look like a horror scene with dark shadows and fog"` |

---

## 3. trim_reference_video

ตัด **บางช่วง** จากวิดีโอ (1-15 วินาที) → ได้วิดีโอสั้น

### Input

```json
{
  "projectUid": "IZdhOv0kfK4fi_R1",
  "chapterUid": "pubWeymO6q8RzUut",
  "sourceVideoUrl": "https://...mp4",
  "startSec": 3,
  "endSec": 8,
  "name": "sb21_action_sequence"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectUid` | string | **Yes** | UID ของ project |
| `chapterUid` | string | **Yes** | UID ของ chapter |
| `sourceVideoUrl` | string | **Yes** | URL ของวิดีโอต้นทาง |
| `startSec` | number | **Yes** | จุดเริ่มตัด (วินาที, integer >= 0) |
| `endSec` | number | **Yes** | จุดจบตัด (วินาที, integer >= 1) |
| `name` | string | No | **ชื่อ asset — ใช้กับ % ใน prompt!** เช่น `sb21_action` → `%sb21_action` |

**ข้อจำกัด:** `endSec - startSec` ต้องอยู่ระหว่าง **1-15 วินาที**

### Output

```json
{
  "uid": "def456xyz",
  "name": "sb21_action_sequence",
  "url": "https://d2xsxph8kpxj0f.cloudfront.net/.../ref-assets/1/def456xyz-trim.mp4",
  "durationSec": 5,
  "usage": "To use in prompts: 1) call add_ref_asset_to_shot with assetName='sb21_action_sequence'..., 2) then write %sb21_action_sequence in the shot prompt."
}
```

---

## 4. add_ref_asset_to_shot (แนบ ref เข้า shot)

**ต้องเรียก tool นี้ก่อน** ถึงจะใช้ `%name` ใน prompt ของ shot นั้นได้

### Input

```json
{
  "shotUid": "box_abc123",
  "assetUid": "uw2vlgznmqs7k550",
  "assetUrl": "https://...frame.jpg",
  "assetName": "sb21_rose_study",
  "mediaType": "image"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `shotUid` | string | **Yes** | UID ของ StoryBox (shot) ที่จะแนบ ref |
| `assetUid` | string | No | `uid` จาก output ของ capture/edit/trim (สำหรับ tracking) |
| `assetUrl` | string | **Yes** | `url` จาก output ของ capture/edit/trim |
| `assetName` | string | **Yes** | **`name` จาก output — นี่คือ %name ที่ใช้ใน prompt!** |
| `mediaType` | string | **Yes** | `"image"` (capture/edit) หรือ `"video"` (trim) |

---

## 5. รูปและวิดีโอไปอยู่ที่ไหน

### Storage (S3 → CloudFront CDN)

| ประเภท | URL Pattern | Permanent? |
|--------|-------------|-----------|
| Captured Frame | `.../ref-assets/{userId}/{uid}-frame.jpg` | **Yes** ไม่ expire |
| Edited Image | `.../ref-assets/{userId}/edit-{timestamp}-{random}.png` | **Yes** ไม่ expire |
| Trimmed Video | `.../ref-assets/{userId}/{uid}-trim.mp4` | **Yes** ไม่ expire |

### Database (ตาราง `reference_assets`)

ทุก asset ถูกบันทึกพร้อมข้อมูล:
- `uid` — unique identifier
- `name` — **ชื่อที่ใช้กับ % ใน prompt**
- `url` — permanent CDN URL
- `mediaType` — "image" หรือ "video"
- `sourceType` — "capture_frame", "last_frame", "edit", หรือ "trim"
- `chapterId` — ผูกกับ chapter (ใช้ได้ทุก shot ใน chapter)

---

## 6. Full Workflow Examples

### Example A: Capture → ใช้ตรง

```
Step 1: capture_video_frame({ timeSec: 6, name: "sb21_rose_study" })
        → { name: "sb21_rose_study", url: "https://...frame.jpg" }

Step 2: add_ref_asset_to_shot({
          shotUid: "box_shot22",
          assetName: "sb21_rose_study",
          assetUrl: "https://...frame.jpg",
          mediaType: "image"
        })

Step 3: prompt → "Rose continues from %sb21_rose_study, camera dollies forward..."
```

### Example B: Capture → Edit → ใช้ (แนะนำ!)

```
Step 1: capture_video_frame({ timeSec: 6, name: "sb21_rose_raw" })
        → { name: "sb21_rose_raw", url: "https://...frame.jpg" }

Step 2: edit_reference_asset({
          sourceImageUrl: "https://...frame.jpg",
          editPrompt: "Remove background, add soft bokeh with warm golden light",
          name: "sb21_rose_golden",
          ratio: "16:9"
        })
        → { name: "sb21_rose_golden", url: "https://...edited.png" }

Step 3: add_ref_asset_to_shot({
          shotUid: "box_shot22",
          assetName: "sb21_rose_golden",
          assetUrl: "https://...edited.png",
          mediaType: "image"
        })

Step 4: prompt → "Rose in %sb21_rose_golden, camera pushes in to close-up,
         she turns to face the window with a gentle smile"
```

### Example C: Trim → ใช้เป็น motion ref

```
Step 1: trim_reference_video({ startSec: 5, endSec: 10, name: "sb15_walk" })
        → { name: "sb15_walk", url: "https://...trim.mp4" }

Step 2: add_ref_asset_to_shot({
          shotUid: "box_shot16",
          assetName: "sb15_walk",
          assetUrl: "https://...trim.mp4",
          mediaType: "video"
        })

Step 3: prompt → "Same walking motion as %sb15_walk, wider angle"
```

---

## 7. สรุป: อะไรใช้ตรงไหน

| จาก output | ใช้ทำอะไร | ตัวอย่าง |
|-----------|-----------|---------|
| `uid` | ใส่ใน `assetUid` (optional tracking) | `"uw2vlgznmqs7k550"` |
| **`name`** | **ใส่ใน `assetName` + ใช้เป็น `%name` ใน prompt** | `"sb21_rose_golden"` → `%sb21_rose_golden` |
| `url` | ใส่ใน `assetUrl` + ใส่ใน `sourceImageUrl` (สำหรับ edit) | `"https://...frame.jpg"` |

---

## 8. Naming Best Practices

| แบบ | ตัวอย่าง | ดี/ไม่ดี |
|-----|---------|---------|
| สื่อความหมาย + shot number | `sb21_rose_closeup` | ✅ ดี |
| บอก action | `sb15_walk_motion` | ✅ ดี |
| บอกว่า edited | `sb21_rose_golden` | ✅ ดี |
| ใช้ uid | `uw2vlgznmqs7k550` | ❌ ห้าม! |
| มี space | `sb21 rose study` | ❌ ใช้ underscore แทน |

---

## 9. Error Handling

| Error | สาเหตุ | แก้ไข |
|-------|--------|-------|
| "Failed to download video" | URL expired/404 | ใช้ URL สดจาก video gen result |
| "Failed to capture frame" | timeSec เกิน duration | ลดค่า timeSec หรือใช้ -1 |
| "Duration must be 1-15 seconds" | endSec - startSec ผิด | ปรับให้อยู่ในช่วง 1-15 |
| "XSkill GPT-Image-2-Edit returned no images" | Edit ล้มเหลว | ลอง editPrompt ใหม่ หรือเปลี่ยน ratio |
| "Shot not found" | shotUid ผิด | ตรวจสอบ UID |

---

## 10. Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│  CAPTURE FRAME                                               │
│  capture_video_frame({ timeSec: 6, name: "xxx" })           │
│  → ได้ { name, url }                                        │
│                                                              │
│  EDIT IMAGE (optional but recommended)                       │
│  edit_reference_asset({ sourceImageUrl: url,                │
│    editPrompt: "...", name: "xxx_edited", ratio: "16:9" })  │
│  → ได้ { name, url } (รูปใหม่ที่ edit แล้ว)                 │
│                                                              │
│  TRIM VIDEO                                                  │
│  trim_reference_video({ startSec, endSec, name: "xxx" })    │
│  → ได้ { name, url }                                        │
│                                                              │
│  ATTACH TO SHOT                                              │
│  add_ref_asset_to_shot({ shotUid,                           │
│    assetName: name, assetUrl: url, mediaType })             │
│                                                              │
│  USE IN PROMPT                                               │
│  "Camera pushes in on %xxx, soft lighting..."               │
│                                                              │
│  ⚠️  %name = ชื่อที่ตั้ง (เช่น %sb21_rose_golden)            │
│  ❌  %uid = random string (ห้ามใช้!)                         │
└─────────────────────────────────────────────────────────────┘
```
