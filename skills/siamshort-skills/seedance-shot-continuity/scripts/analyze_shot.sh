#!/usr/bin/env bash
# analyze_shot.sh — โหลดวิดีโอ Seedance + วิเคราะห์ทั้งคลิปในคำสั่งเดียว
# ใช้: analyze_shot.sh <video_url> <name> [outdir]
#   <video_url>  signed URL จาก poll_video_byteplus
#   <name>       ชื่อช็อต เช่น sb8  (ไฟล์จะเป็น <name>.mp4 / <name>_grid.png / <name>_tT.jpg)
#   [outdir]     โฟลเดอร์ปลายทาง (default: โฟลเดอร์ปัจจุบัน)
# ผลลัพธ์: <name>.mp4, ratio (ควร 720x1280 = 9:16), <name>_grid.png (16 เฟรม 0-15s),
#          และเฟรมเต็มที่ t=1,5,8,11,14 สำหรับเช็คตำแหน่ง/ฉาก/โคลน/แตกจอ
set -euo pipefail

URL="${1:?ต้องใส่ video_url}"
NAME="${2:?ต้องใส่ name เช่น sb8}"
OUT="${3:-.}"
mkdir -p "$OUT"
MP4="$OUT/$NAME.mp4"

echo "→ download $NAME ..."
curl -sL -A "Mozilla/5.0" "$URL" -o "$MP4"
file "$MP4" | grep -qi 'media\|MP4' || { echo "❌ ไฟล์ไม่ใช่วิดีโอ (URL หมดอายุ?)"; exit 1; }

echo -n "→ ratio: "
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$MP4"
echo -n "→ duration: "
ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$MP4"

echo "→ grid 16 เฟรม (0-15s) ..."
ffmpeg -y -i "$MP4" -vf "fps=1,scale=240:-1,tile=4x4" -frames:v 1 "$OUT/${NAME}_grid.png" 2>/dev/null

echo "→ เฟรมเต็มจุดสำคัญ t=1,5,8,11,14 ..."
for t in 1 5 8 11 14; do
  ffmpeg -y -ss "$t" -i "$MP4" -frames:v 1 -q:v 2 "$OUT/${NAME}_t${t}.jpg" 2>/dev/null || true
done

echo "✅ เสร็จ — เปิดดู $OUT/${NAME}_grid.png ก่อน แล้วเจาะ ${NAME}_tT.jpg จุดที่สงสัย"
echo "   เช็ค: ตำแหน่งนิ่ง? เพี้ยน? โคลน? แตกจอ? ฉากตรง ref? 9:16? 14-15s โอเค?"
