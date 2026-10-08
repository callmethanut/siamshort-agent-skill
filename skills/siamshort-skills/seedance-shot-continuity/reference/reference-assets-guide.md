# MCP Reference Assets Guide — Capture Frame & Trim Video

## Overview

Reference Assets คือ image/video ที่เก็บ **ระดับ Chapter** — ใช้เป็น `%reference` ใน prompt ของ StoryBox (shot) ไหนก็ได้ภายใน Chapter เดียวกัน

**3 เครื่องมือหลัก:**

| Tool | ทำอะไร | ได้อะไร |
|------|--------|---------|
| `capture_video_frame` | จับเฟรมจากวิดีโอ (เฟรมไหนก็ได้ / last frame) | image ref |
| `trim_reference_video` | ตัดบางช่วงจากวิดีโอ (1-15 วินาที) | video ref |
| `add_ref_asset_to_shot` | แนบ ref asset เข้า shot เพื่อใช้ `%name` ใน prompt | — |

---

## 1. capture_video_frame

จับ **เฟรมเดียว** จากวิดีโอ ณ เวลาที่ระบุ → ได้ภาพ JPEG เก็บเป็น Reference Asset

### Input

```json
{
  "projectUid": "IZdhOv0kfK4fi_R1",
  "chapterUid": "pubWeymO6q8RzUut",
  "videoUrl": "https://d2xsxph8kpxj0f.cloudfront.net/.../video.mp4",
  "timeSec": 6,
  "name": "sb21_rose_study"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectUid` | string | **Yes** | UID ของ project |
| `chapterUid` | string | **Yes** | UID ของ chapter ที่จะเก็บ asset |
| `videoUrl` | string | **Yes** | URL ของวิดีโอ (ใช้ URL จาก video gen result โดยตรง) |
| `timeSec` | number | No | วินาทีที่ต้องการจับ; **ไม่ใช่แค่ last frame** — ใส่เลขวินาทีไหนก็ได้ (0, 3, 6, 12...) ใส่ `-1` = เฟรมสุดท้าย (default: -1) |
| `name` | string | No | ชื่อ asset (ถ้าไม่ใส่ = "Frame @{time}s") |
| `sourceAssetUid` | string | No | UID ของ video asset ต้นทาง (สำหรับ tracking) |

### Output

```json
{
  "uid": "abc123xyz",
  "name": "sb21_rose_study",
  "url": "https://d2xsxph8kpxj0f.cloudfront.net/.../ref-assets/1/abc123xyz-frame.jpg",
  "captureTimeSec": 6
}
```

### ตัวอย่างการใช้

```
// จับเฟรมที่ 6 วินาที
capture_video_frame({ ..., timeSec: 6, name: "rose_closeup" })

// จับเฟรมแรก (0 วินาที)
capture_video_frame({ ..., timeSec: 0, name: "opening_frame" })

// จับเฟรมสุดท้าย
capture_video_frame({ ..., timeSec: -1, name: "ending_frame" })

// จับเฟรมกลางวิดีโอ (ถ้าวิดีโอ 15 วินาที)
capture_video_frame({ ..., timeSec: 7.5, name: "mid_action" })
```

---

## 2. trim_reference_video

ตัด **บางช่วง** จากวิดีโอ (1-15 วินาที) → ได้วิดีโอสั้นเก็บเป็น Reference Asset

### Input

```json
{
  "projectUid": "IZdhOv0kfK4fi_R1",
  "chapterUid": "pubWeymO6q8RzUut",
  "sourceVideoUrl": "https://d2xsxph8kpxj0f.cloudfront.net/.../video.mp4",
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
| `name` | string | No | ชื่อ asset |
| `sourceAssetUid` | string | No | UID ของ video asset ต้นทาง |

**ข้อจำกัด:** `endSec - startSec` ต้องอยู่ระหว่าง **1-15 วินาที**

### Output

```json
{
  "uid": "def456xyz",
  "name": "sb21_action_sequence",
  "url": "https://d2xsxph8kpxj0f.cloudfront.net/.../ref-assets/1/def456xyz-trim.mp4",
  "durationSec": 5
}
```

---

## 3. รูปและวิดีโอไปอยู่ที่ไหน

### Storage Location

| ประเภท | S3 Key Pattern | URL Pattern |
|--------|---------------|-------------|
| Captured Frame | `ref-assets/{userId}/{uid}-frame.jpg` | `https://d2xsxph8kpxj0f.cloudfront.net/{appId}/{projectKey}/ref-assets/{userId}/{uid}-frame.jpg` |
| Trimmed Video | `ref-assets/{userId}/{uid}-trim.mp4` | `https://d2xsxph8kpxj0f.cloudfront.net/{appId}/{projectKey}/ref-assets/{userId}/{uid}-trim.mp4` |

### Database Record (ตาราง `reference_assets`)

ทุก asset ถูกบันทึกใน DB พร้อมข้อมูล:

| Field | Capture Frame | Trim Video |
|-------|--------------|------------|
| `uid` | unique ID | unique ID |
| `mediaType` | `"image"` | `"video"` |
| `sourceType` | `"capture_frame"` หรือ `"last_frame"` | `"trim"` |
| `url` | S3 URL ของ JPEG | S3 URL ของ MP4 |
| `sourceVideoUrl` | URL วิดีโอต้นทาง | URL วิดีโอต้นทาง |
| `captureTimeSec` | เวลาที่จับ (วินาที) | null |
| `trimStartSec` | null | จุดเริ่มตัด |
| `trimEndSec` | null | จุดจบตัด |
| `durationSec` | null | ความยาว (วินาที) |
| `chapterId` | chapter ที่ asset อยู่ | chapter ที่ asset อยู่ |

---

## 4. ขึ้นใน Reference Assets — ใช้ได้ทุก StoryBox ใน Chapter

เมื่อ capture/trim สำเร็จ → asset จะ **ขึ้นใน Reference Assets ของ Chapter นั้นทันที** → สามารถดึงมาใช้กับ StoryBox (shot) ไหนก็ได้ภายใน Chapter เดียวกัน

### ดูรายการ Reference Assets

**Tool:** `list_reference_assets`

```json
{
  "chapterUid": "pubWeymO6q8RzUut",
  "mediaType": "all"
}
```

Output จะรวมทั้ง:
- Manual uploads
- Captured frames
- Trimmed videos
- Auto-generated storyboards & last frames

---

## 5. ดึงมาเป็น %ref สำหรับ Prompt ใน StoryBox

### วิธีที่ 1: add_ref_asset_to_shot (แนะนำ)

**Tool:** `add_ref_asset_to_shot`

```json
{
  "shotUid": "box_abc123",
  "assetUid": "abc123xyz",
  "assetUrl": "https://d2xsxph8kpxj0f.cloudfront.net/.../abc123xyz-frame.jpg",
  "assetName": "rose_closeup",
  "mediaType": "image"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `shotUid` | string | **Yes** | UID ของ StoryBox (shot) ที่จะแนบ ref |
| `assetUid` | string | No | UID ของ reference asset |
| `assetUrl` | string | **Yes** | URL ของ asset (จาก capture/trim output) |
| `assetName` | string | **Yes** | ชื่อที่จะใช้อ้างอิงใน prompt ด้วย `%name` |
| `mediaType` | string | **Yes** | `"image"` หรือ `"video"` หรือ `"audio"` |

**ผลลัพธ์:** Asset ถูกเพิ่มเข้า `box.referenceImages` → ใช้ `%rose_closeup` ใน prompt ของ shot นั้นได้

### วิธีที่ 2: อ้างอิงตรงใน prompt ด้วย %uid

ใน prompt field ของ StoryBox พิมพ์:
```
%abc123xyz
```

ระบบจะ resolve เป็น image/video URL ให้อัตโนมัติตอน generate

---

## 6. Full Workflow ตัวอย่าง

### Scenario: สร้าง Shot 22 ที่ต่อเนื่องจาก Shot 21

```
┌─────────────────────────────────────────────────────┐
│ Step 1: ดึง video URL ของ shot 21 ที่ gen สำเร็จแล้ว │
└─────────────────────────────────────────────────────┘
    ↓ videoUrl = "https://...shot21.mp4"

┌─────────────────────────────────────────────────────┐
│ Step 2: Capture frame ที่ต้องการ                      │
└─────────────────────────────────────────────────────┘
    capture_video_frame({
      projectUid: "...",
      chapterUid: "...",
      videoUrl: "https://...shot21.mp4",
      timeSec: 12,          ← จับเฟรมที่ 12 วินาที (ไม่ใช่แค่ last frame!)
      name: "sb21_rose_turn"
    })
    ↓ ได้ { uid: "ref001", url: "https://...ref001-frame.jpg" }

┌─────────────────────────────────────────────────────┐
│ Step 3: แนบ ref เข้า shot 22                          │
└─────────────────────────────────────────────────────┘
    add_ref_asset_to_shot({
      shotUid: "box_shot22",
      assetUrl: "https://...ref001-frame.jpg",
      assetName: "sb21_rose_turn",
      mediaType: "image"
    })

┌─────────────────────────────────────────────────────┐
│ Step 4: เขียน prompt สำหรับ shot 22                    │
└─────────────────────────────────────────────────────┘
    prompt: "Rose continues turning from %sb21_rose_turn, 
             camera dollies forward to medium close-up, 
             soft golden hour lighting"

┌─────────────────────────────────────────────────────┐
│ Step 5: Generate video shot 22                        │
│         → Seedance ใช้ captured frame เป็น reference  │
│         → ได้ visual continuity จาก shot 21           │
└─────────────────────────────────────────────────────┘
```

### Scenario: ใช้ Trim Video เป็น Motion Reference

```
┌─────────────────────────────────────────────────────┐
│ Step 1: Trim ช่วงที่ต้องการจากวิดีโอเดิม              │
└─────────────────────────────────────────────────────┘
    trim_reference_video({
      projectUid: "...",
      chapterUid: "...",
      sourceVideoUrl: "https://...shot15.mp4",
      startSec: 5,
      endSec: 10,
      name: "sb15_walk_motion"
    })
    ↓ ได้ { uid: "ref002", url: "https://...ref002-trim.mp4", durationSec: 5 }

┌─────────────────────────────────────────────────────┐
│ Step 2: แนบ video ref เข้า shot ใหม่                  │
└─────────────────────────────────────────────────────┘
    add_ref_asset_to_shot({
      shotUid: "box_shot16",
      assetUrl: "https://...ref002-trim.mp4",
      assetName: "walk_motion_ref",
      mediaType: "video"
    })

┌─────────────────────────────────────────────────────┐
│ Step 3: เขียน prompt ที่อ้างอิง video ref              │
└─────────────────────────────────────────────────────┘
    prompt: "Same walking motion as %walk_motion_ref, 
             but from a wider angle, tracking shot"
    
    → Seedance ใช้ trimmed video เป็น motion reference
```

---

## 7. สรุป Flow ทั้งหมด

```
Video Gen Result
    │
    ├── capture_video_frame (timeSec = 0~15 หรือ -1)
    │       ↓
    │   Image (.jpg) → S3 → reference_assets DB
    │       ↓
    │   add_ref_asset_to_shot → %name ใน prompt
    │
    └── trim_reference_video (startSec → endSec, 1-15s)
            ↓
        Video (.mp4) → S3 → reference_assets DB
            ↓
        add_ref_asset_to_shot → %name ใน prompt
```

**Key Point:** ทุก Reference Asset เป็น **per-Chapter** — สร้างครั้งเดียว ใช้ได้กับทุก StoryBox (shot) ใน Chapter นั้น

---

## 8. Error Handling

| Error | สาเหตุ | แก้ไข |
|-------|--------|-------|
| "Failed to download video" | URL expired หรือ 404 | ใช้ URL สดจาก video gen result |
| "Failed to capture frame" | timeSec เกิน duration ของวิดีโอ | ลดค่า timeSec หรือใช้ -1 |
| "Duration must be 1-15 seconds" | endSec - startSec ไม่อยู่ในช่วง | ปรับ startSec/endSec |
| "Video trim failed" | codec ไม่รองรับ | ระบบจะ retry ด้วย re-encode อัตโนมัติ |
| "Reference already exists in shot" | ชื่อหรือ URL ซ้ำ | ใช้ชื่ออื่น หรือข้ามไป |
| "Shot not found" | shotUid ไม่ถูกต้อง | ตรวจสอบ UID |

---

## 9. Important Notes

1. **`timeSec` ไม่ได้จำกัดแค่ last frame** — ใส่เลขวินาทีไหนก็ได้ (0, 1, 2.5, 6, 12, 14.9...)
2. **URL ที่ได้จาก output เป็น permanent URL** — ไม่ expire, ใช้ได้ตลอด
3. **Asset ขึ้นใน chapter ทันที** — ไม่ต้อง refresh หรือรอ
4. **ใช้ `list_reference_assets` ดูรายการทั้งหมด** — ก่อนจะ add ซ้ำ
5. **`add_ref_asset_to_shot` สร้าง Virtual Asset อัตโนมัติ** — สำหรับ Ark/BytePlus provider
6. **Video ref ใช้เป็น motion reference** — Seedance จะเลียนแบบการเคลื่อนไหว
7. **Image ref ใช้เป็น composition/style reference** — Seedance จะเลียนแบบ framing/look
