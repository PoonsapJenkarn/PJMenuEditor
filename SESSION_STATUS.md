# SESSION STATUS - OE Isan Menu Editor

ปรับปรุงล่าสุด: 2026-10-24 13:54 (+07)

## เสร็จรอบนี้ (ยังไม่ commit) - เส้นคั่นใต้ส่วนหัว: สีตามตีม + ซ่อนได้
### สีตามตีม
- .rule เดิมสีทองฝังตาย #c9a227 -> ใช้ var(--line-dot) (token สีเส้นของแต่ละตีม เส้นจุด .ln ใช้อยู่แล้ว) -> เปลี่ยนตามตีมครบ 13 ตีม + custom อัตโนมัติ ไม่ต้องเพิ่มค่าทีละตีม
- ผลข้างเคียง: ตีมครีมเส้นเปลี่ยนจากทอง -> เบจอ่อน #cdbfa8 (เข้าชุดตีม) · ตีมเข้ม/เย็น (ขาว-ดำ/น้ำเงิน/เขียวทะเล) เส้นเข้าโทนแล้ว ไม่ลอย
### ซ่อนได้ (จอ + พิมพ์ + ติดไปกับไฟล์)
- โมเดล data-rulehide บน <html> (เลียน data-theme) -> CSS html[data-rulehide] .rule{display:none !important} ไม่มี @media = มีผลทั้งจอและพิมพ์
- save ทั้ง 2 แบบ (buildEditorHtml/buildMenuHtml) clone documentElement -> attribute ติดไปกับไฟล์ที่เซฟ -> เมนูที่เซฟก็ซ่อนเส้นตอนพิมพ์
- ไม่ใช้ localStorage (ต่างจาก pgcontenthide) - สถานะเป็นของเอกสาร เก็บไปกับไฟล์ ไม่ใช่ global
- ปุ่ม btnRuleHide แท็บ หน้า กลุ่มใหม่ 'เส้นคั่น' (ต่อจากกลุ่มธีม) · toggle ซ่อน<->แสดง สลับ label (btn.ruleHide/ruleShow) · active = เขียว #217346 (เพิ่มเข้า list 3 selector ตามข้อ 11)
- toggleRuleHide() + _ruleHideSync() · เรียก _ruleHideSync() ตอนเปิดแอป (ต่อจาก _themeLoad) sync ปุ่มกับสถานะไฟล์ · markDirty เมื่อ toggle
- i18n ครบ TH+EN (btn.ruleHide/ruleShow/grp.rule/ttl.ruleHide)
- lint #110 ล็อก: var(--line-dot) + ห้าม #c9a227 + html[data-rulehide] + 2 ฟังก์ชัน + ปุ่ม + active เขียว + startup call + i18n ครบ
- lint PASS (rc=0), เขียนดิสก์ (html 8,138,790 bytes)

## รอผู้ใช้ทดสอบ (F5)
1. แท็บ หน้า > เลื่อนธีม (dropdown) -> เส้นคั่นเปลี่ยนสีตามตีมทุกตีม (ไม่ใช่ทองตายตัวแล้ว)
2. แท็บ หน้า > กลุ่ม 'เส้นคั่น' > ปุ่ม 'ซ่อนเส้นคั่น' -> เส้นหาย ปุ่มเขียว label เป็น 'แสดงเส้นคั่น'
3. ลองพิมพ์ (Ctrl+P) ตอนซ่อน -> เส้นต้องหายในตัวอย่างพิมพ์ด้วย
4. Save Menu ตอนซ่อน -> เปิดไฟล์เมนูที่เซฟ เส้นต้องยังซ่อน (ติดไปกับไฟล์)

## ค้างถัดไป
- contrast .ep-preview #6b7280 = 4.42 ยังตก WCAG 4.5
- ปุ่มยืนยัน ปรับราคา แยกโซนด้วยเส้นคั่น? · ตัวคั่น สี · รูป รอเลือกแบบ · popup เล็ก

## commit ที่จะใช้ (ผู้ใช้รันเองที่ C:\OE)
git add -A
git commit -m "feat: เส้นคั่นใต้ส่วนหัวสีตามตีม (var --line-dot) + ปุ่มซ่อนเส้น จอ+พิมพ์+ติดไฟล์ (btnRuleHide แท็บหน้า) + lint #110"
git push

HEAD ก่อนหน้า: c387b4b
