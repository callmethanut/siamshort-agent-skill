# 🎬 Siamshort Skills Pack (อัปเดต 2026-07-06)
7 skills ทำหนัง Siamshort/Fable. ติดตั้ง: คัดลอกโฟลเดอร์ไป ~/.claude/skills/ แล้วเรียก /<ชื่อ>

⭐ อัปเดตล่าสุด (2 เรื่อง):
1) กฎเหล็ก TAG entity ลง storybox — พอได้ storybox ต้อง update_shot ผูก characterIds/sceneIds/itemIds ทุกช็อต (ไม่ใช่แค่ @/#/$ mention)
2) เอา storyboard + manhwa ออกจาก Loop — PHASE A จบที่ storybox+tag+assets, PHASE B เน้น gen video ทีละ shot มี human-in-the-loop

หลัก: siamshort_auto_loop · siamshort_script_from_novel · anti-plastic · seedance-shot-continuity · physics-guide
ขับ MCP ตรง: fable-auto-director · storyboard (สกิลแยก ถ้าอยากทำ storyboard-sheet เดี่ยว)
ไม่ใส่: gpt-image (มี API key), artifact-design (built-in). การต่อ MCP = connector/claude mcp ไม่ใช่ skill.
