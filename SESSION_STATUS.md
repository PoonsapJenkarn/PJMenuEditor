# OE Isan Menu Editor — Session Status

## ✅ เสร็จแล้ว (รอบ 2 — เพิ่ม 4 ธีม + ปุ่มเลือกธีม · 23 ต.ค. 2026)
- CSS: :root[data-theme] 3 ธีม (white-green / dark-gold / paper-brick) · cream = base :root (default)
- ธีมเข้ม-ทอง: override .sec-h เป็นทอง #d4af37 ทุกกลุ่ม (ทับ --accent รายหมวดเฉพาะธีมนี้ · ธีมสว่างยังได้สีรายหมวด)
- ปุ่ม btnTheme แท็บ "หน้า" กลุ่มใหม่ "ธีม" · เปิด panel เลือก 4 ธีม (openPanel tone:info — ไม่มี icon) · active เขียว (ข้อ 11)
- JS: _THEMES / _themeApply / _themeLoad / _themePick / openThemePanel · ธีมเก็บใน data-theme บน <html> → ติดไฟล์อัตโนมัติ (cloneNode) + จำ localStorage oe_theme
- _themeLoad(): เคารพ data-theme ในไฟล์ก่อน localStorage (ไฟล์ที่เซฟไว้เปิดมาได้สีถูก)
- i18n TH/EN ครบ (btn.theme/grp.theme/th.pick/th.cream/th.whiteGreen/th.darkGold/th.paperBrick/fl.themeSet/ttl.theme)
- lint #94 ล็อกทั้งฟีเจอร์
- in-memory lint PASS (rc=0) → เขียนดิสก์ → disk lint PASS (rc=0) → token 16/16 ครบ

## ⏳ รอผู้ใช้ทดสอบ (รีเฟรช Ctrl+Shift+R)
1. แท็บ "หน้า" → มีกลุ่ม "ธีม" ปุ่มรูปจานสี
2. กด "ธีม" → panel เด้ง 4 ธีม · ปุ่มธีมที่เลือกอยู่เขียว
3. กดทีละธีม → สีเมนูเปลี่ยนทันที (ป้ายโน้ต/กลุ่มเมนู/ชื่อ/ราคา/เส้นจุด)
4. ธีมเข้ม-ทอง → หัวกลุ่มทุกกลุ่มเป็นทอง อ่านออกทุกกลุ่ม (ไม่มืดบนมืด)
5. กด TH/EN → ชื่อธีมใน panel เปลี่ยนภาษา
6. เซฟ + เปิดไฟล์ใหม่ → ธีมติดมาด้วย

## ⏳ ยังไม่ commit (ให้ผู้ใช้รันเอง)
cd C:\OE
git add -A
git commit -m "feat: ธีมสี 4 ธีม + ปุ่มเลือกธีม (รอบ2) + lint #94"
git push

## หมายเหตุ
- เปลี่ยนธีม = markDirty (นับเป็นการแก้เอกสาร ต้อง save) · ยังไม่มีจุด Undo (ถ้าต้องการค่อยเพิ่ม)
- สีเส้นขอบ+สีหมายเหตุของแต่ละธีม derive ให้กลมกลืน (ไม่ได้อยู่ในตาราง 6 โซนที่ approve) — ปรับได้
