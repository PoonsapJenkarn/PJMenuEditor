# SESSION STATUS - OE Isan Menu Editor

ปรับปรุงล่าสุด: 2026-10-25 18:05 (+07)

## เสร็จรอบนี้ (ยังไม่ commit) - แก้บั๊กพิมพ์ไม่เต็มหน้า (ROOT CAUSE เจอแล้ว)
- ปัญหา: print/PDF หน้าถูกย่อ ~74-80 เปอร์เซ็นต์ ชิดมุมซ้ายบน แม้ Margins=None (เป็นมาหลายรอบ ผู้ใช้ยืนยัน reproduce ได้)
- ROOT CAUSE: body{min-width:960px} อยู่ใน CSS หลัก (เพิ่มตอนแก้บั๊กจอแคบ) แต่ @media print ไม่ได้ reset -> ตอนพิมพ์ body ถูกบังคับ 960px = 254mm เกิน A4 210mm -> Chrome ย่อทั้งหน้าลงชิดมุมซ้ายบน
- ทำไมหลงทางนาน: ไม่เกี่ยว Margins/เครื่องพิมพ์/Borderless เลย · เทสต์กรอบแดงเต็ม A4 เพราะไฟล์เทสต์ไม่มี min-width · screenshot วัดไม่แม่น (ดู anti-pattern memory)
- FIX: @media print{body{...min-width:0 !important;width:auto !important;}} (reset ตอนพิมพ์ให้ body กลับมาพอดี A4)
- lint #111 ล็อก: @media print body ต้องมี min-width:0
- lint PASS (rc=0), เขียนดิสก์ (html 8,138,835 bytes)

## รอผู้ใช้ทดสอบ (F5 + print preview)
- รีเฟรช (F5) แล้วเปิด print preview (Ctrl+P) / Save as PDF Margins=None
- คาดผล: พื้นครีมเต็มความกว้าง A4 ไม่ย่อ ไม่ชิดมุมซ้ายบนแล้ว (เนื้อหายังเว้น padding 8/12mm ตามดีไซน์ = ปกติ)
- ถ้าเต็มแล้ว = จบบั๊กพิมพ์

## ค้างถัดไป (ถ้าผู้ใช้ต้องการ)
- ลด padding .page ถ้าอยากให้เนื้อหาชิดขอบกระดาษกว่านี้
- contrast .ep-preview #6b7280 = 4.42 ยังตก WCAG 4.5
- ปุ่มยืนยัน ปรับราคา แยกโซนด้วยเส้นคั่น? · ตัวคั่น สี · รูป รอเลือกแบบ · popup เล็ก

## commit ที่จะใช้ (ผู้ใช้รันเองที่ C:\OE)
git add -A
git commit -m "fix: พิมพ์ไม่เต็มหน้า - reset body min-width ตอนพิมพ์ (body 960px เกิน A4 ทำ Chrome ย่อหน้า) + lint #111"
git push

HEAD ก่อนหน้า: c387b4b
