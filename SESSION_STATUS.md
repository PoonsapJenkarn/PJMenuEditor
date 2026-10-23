# OE Isan Menu Editor — Session Status

## ✅ ปุ่มคืนค่า = กลุ่ม "ตั้งค่า" มีเส้นคั่น+ป้าย (เสร็จ · 23 ต.ค. 2026 · รอทดสอบ)
- ปัญหา: ปุ่มคืนค่าลอยโดดเดี่ยว ไม่มีป้ายกลุ่มใต้เหมือนกลุ่มอื่น → อยู่คนละระดับ
- แก้: ใส่เส้นคั่น .thcp-sep ก่อนปุ่ม + ห่อใน .thcp-cat (ปุ่มใน .thcp-cat-z บน, ป้าย .thcp-cat-h ล่าง) — โครงเดียวกับ 3 กลุ่มสี
- ชื่อกลุ่ม = "ตั้งค่า" (th.grpSet · TH ตั้งค่า / EN Settings)
- ผล: ปุ่มคืนค่าลอยระดับเดียวกับถาดสี/dropdown (ป้ายอยู่ล่างเสมอกัน)
- lint #95 ขยาย: เพิ่ม th.grpSet ใน group-key list
- in-memory + disk lint PASS (rc=0) · token 7/7

## ⏳ รอผู้ใช้ทดสอบ — Ctrl+Shift+R (hard refresh)
หน้า → ธีม → กำหนดเอง → ปุ่มคืนค่ามีเส้นคั่นกั้น + ป้าย "ตั้งค่า" ใต้ปุ่ม → ลอยระดับเดียวกับ element อื่น

## ⏳ ยังไม่ commit (รวมงานพาเนลธีมทั้งชุดของรอบนี้)
ค้างตั้งแต่ checkpoint 1 — ยังไม่ commit หลายรอบ: (1) baseline flex-end (2) ภาษาดี ribbon 13px (3) ย้ายชื่อกลุ่มลงล่าง flex-start (4) กลุ่มตั้งค่า
cd C:\OE
git add -A
git commit -m "feat: พาเนลธีมโครง ribbon + กลุ่มคืนค่า(ตั้งค่า)มีป้าย+เส้นคั่น + lint #95"
git push

## ⏳ Checkpoint 2 + local override element (ค้าง)
- Checkpoint 2: ความหนาขอบ 3 โซน (--note-bw/--grp-bw/--line-bw)
- local override: คลิกกล่อง/โน้ต/หัวกลุ่ม → ขอบ/พื้น/gradient เฉพาะชิ้น
