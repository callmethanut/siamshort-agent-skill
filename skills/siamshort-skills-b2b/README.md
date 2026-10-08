# 🎬 SiamShort B2B Skills Pack (สำหรับแพลตฟอร์มเรา — siamshort MCP)

Skill pack สำหรับทำหนังบน **Siamshort/GEE ผ่าน siamshort MCP** — พอร์ต/คัดจาก
siamshort-skills (Fable). ติดตั้ง: คัดลอกโฟลเดอร์สกิลไป `~/.claude/skills/` แล้วเรียก `/<ชื่อ>`.
Prerequisite: ต่อ siamshort MCP แล้ว (ดู siamshort-mcp/README.md).

อัปเดต 2026-07-14: agent ตั้ง image output ที่มีอยู่เป็นหน้าปกโปรเจกต์ได้ด้วย
`set_project_cover(project_id, run_id)` โดยไม่ gen ซ้ำและไม่เสียแต้ม.

## สกิลในแพ็ก (8)

| สกิล | ที่มา | ใช้ทำอะไร |
|---|---|---|
| **siamshort-b2b-auto-movie** | พอร์ตจาก siamshort_auto_loop | GEE Loop เต็มรูป: บท → project+world → assets → shots (plot+tag+prompt) → gen วิดีโอทีละช็อต human-in-the-loop. มี VOCABULARY MAP (character=Cast, chapter=Sequence, storybox=Shot) + reference/gee-platform-map.md |
| **siamshort-b2b-shot-continuity** | พอร์ตจาก seedance-shot-continuity | กลไก Phase B: ทีละช็อต + scene/position/CAM-BG lock + วิเคราะห์ทั้งคลิป + PASS/FAIL + regen ≤4 (เครื่องมือ GEE ทั้งหมด) |
| **siamshort-b2b-auto-director** | พอร์ตจาก fable-auto-director | ไอเดีย 1 บรรทัด → โปรเจกต์ครบชุด auto-decision (confirm ครั้งเดียว + OK-gate ต่อวิดีโอ) |
| **siamshort-b2b-idea-board** | เขียนใหม่จาก idea-board docs | คู่มือ canvas: node ทุกกลุ่ม (Input/Gen/Output/Helper/Tools) + workflow recipes (text→image→video, manhwa→`add_shot_asset` — ห้าม auto-แนบเป็น gen ref) + กฎเหล็กบนบอร์ด |
| **siamshort-b2b-board-movie** | เขียนใหม่ (จาก feedback ทดสอบจริง) | Pipeline ทำหนังบนบอร์ดแบบคุม consistency: story → entity identity → storyboard image ต่อช็อต (ref entity) → manhwa position frame → วิดีโอต่อช็อต + layout กันทับ |
| **siamshort-b2b-script-from-novel** | คัดลอกตรง (ไม่แตะ MCP) | นิยาย/เรื่องยาว → บทถ่ายทำ △-format ละเอียดยิบ |
| **siamshort-b2b-anti-plastic** | คัดลอกตรง (craft ล้วน) | ชั้น realism/texture กันหน้าพลาสติก/ลุค AI |
| **siamshort-b2b-physics-guide** | คัดลอก + patch ชื่อ tool | ลูกโซ่ฟิสิกส์ 5 ชั้นสำหรับช็อตมีแรงตั้งต้น (ของตก/แตก/สาด/ชน) |

## ไม่พอร์ต (เหตุผล)

- **storyboard** — สร้าง storyboard-sheet/manhwa ซึ่ง Loop ตัดออกแล้ว ; ของ GEE ใช้
  `generate_shot_image` (draft still ต่อช็อต) แทน.
- `siamshort_auto_loop` / `fable-auto-director` ต้นฉบับ — ผูก tool ของ Fable ;
  ใช้เวอร์ชันพอร์ตในแพ็กนี้แทนเมื่ออยู่บน GEE.

⚠️ อย่าติดตั้งสกิล Fable ต้นฉบับปนกับแพ็กนี้ใน `~/.claude/skills/` ถ้าทำงานบน GEE —
ชื่อ tool คนละชุด agent อาจสับสน.

## 📦 Ready-to-install packages (`dist/`)

- `dist/<skill>.skill` — ติดตั้งใน **Claude Desktop**: Settings → Capabilities → Skills →
  upload ไฟล์ `.skill` ทีละตัว.
- `dist/<skill>.zip` — เนื้อหาเดียวกัน สำหรับที่ที่รับ `.zip` (เช่น claude.ai custom skills).
- `dist/siamshort-b2b-skills-pack.zip` — ทั้งแพ็กก้อนเดียว สำหรับ **Claude Code**:
  แตกลง `~/.claude/skills/` (Windows: `%USERPROFILE%\.claude\skills\`) แล้วเปิด session ใหม่.

หลังแก้ SKILL.md ใดๆ ให้ re-run การ pack (zip โฟลเดอร์ → เปลี่ยนนามสกุล) เพื่อให้ dist ตรงกับซอร์ส.
