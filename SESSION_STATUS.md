# SESSION STATUS - OE Isan Menu Editor

ปรับปรุงล่าสุด: 2026-10-26 18:20 (+07)

## เสร็จรอบนี้ (ยังไม่ commit) - เปลี่ยนคำ "ป้ายหน้า" เป็น "เลขหน้า"
- ปุ่ม: ซ่อนป้ายหน้า -> ซ่อนเลขหน้า · สถานะ: แสดงป้ายหน้า -> แสดงเลขหน้า
- tooltip: ซ่อนป้ายเลขหน้า (...) -> ซ่อนเลขหน้า (...)
- EN: Hide/Show page label -> Hide/Show page number (ปุ่ม + tooltip)
- แก้ markup default (title + span) + i18n TH + EN + คอมเมนต์ CSS · ไม่แตะ key/logic (btn.plabelHide ฯลฯ คงเดิม)
- ตรวจแล้วไม่เหลือคำ "ป้ายหน้า" / "page label" ในไฟล์
- lint PASS (rc=0), เขียนดิสก์แล้ว

## รอผู้ใช้ทดสอบ (F5)
- แท็บ เท็มเพลต: ปุ่มเป็น "ซ่อนเลขหน้า" · กดแล้วเปลี่ยนเป็น "แสดงเลขหน้า"
- สลับ EN: Hide page number / Show page number

## commit ที่จะใช้ (ผู้ใช้รันเองที่ C:\OE)
git add -A
git commit -m "ui: เปลี่ยนคำ 'ป้ายหน้า' เป็น 'เลขหน้า' (Hide page number)"
git push

HEAD ก่อนหน้า: 5124d60
