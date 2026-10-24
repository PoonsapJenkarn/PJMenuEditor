# SESSION STATUS - OE Isan Menu Editor

ปรับปรุงล่าสุด: 2026-10-24 12:03 (+07)

## เสร็จรอบนี้ (ยังไม่ commit) - vertical alignment ปุ่ม action ใน panel
- ผู้ใช้เลือก: align ปุ่ม action กับแถว control (ไม่ใช่กลางความสูงรวม panel)
- แก้: #edpanel .ep-btns เพิ่ม align-self:flex-start -> ปุ่ม (ปรับราคา/ยืนยัน) ขอบบนตรงแถว control ไม่ลอยต่ำ
- เหตุ: panel 2 ชั้น (control บน + label ล่าง) · align-items:center เดิมจัดปุ่มกลางความสูงรวม ปุ่มที่ไม่มี label เลยลอยต่ำกว่าแถว control
- lint #106 ล็อก: .ep-btns ต้อง align-self:flex-start
- lint PASS (rc=0), เขียนดิสก์ (html 8,132,169 bytes)

## รอผู้ใช้ทดสอบ (F5)
- แท็บ ข้อความ > ปรับราคา: ปุ่ม ปรับราคา ขวาสุด ขอบบนตรงแถว control (ปุ่ม tool/textbox) ไม่ลอยต่ำ
- panel อื่นที่มีปุ่มยืนยัน (ยกเลิก/คืนค่า) ก็อยู่ระดับแถว control เหมือนกัน

## ค้างถัดไป
- ปุ่มยืนยัน ปรับราคา แยกโซนด้วยเส้นคั่น? (ถามไว้ก่อนหน้า ยังไม่เคาะ)
- ตัวคั่น สี · รูป รอเลือกแบบ (dot เว้นวรรค / และ / + / พริก SVG)
- popup เล็ก = ฟิลด์เดียว

## commit ที่จะใช้ (ผู้ใช้รันเองที่ C:\OE)
git add -A
git commit -m "ui: ปุ่ม action ใน panel align แถว control (align-self:flex-start) + lint #106"
git push

HEAD ก่อนหน้า: a7f6959
