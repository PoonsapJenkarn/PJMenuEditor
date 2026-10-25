# SESSION STATUS - OE Isan Menu Editor

ปรับปรุงล่าสุด: 2026-10-25 18:45 (+07)

## เสร็จรอบนี้ (ยังไม่ commit) - เส้นกรอบปรับความหนา+แบบเส้นได้ (Theme Checkpoint 2)
- .crab (กล่องโน้ต): border -> var(--note-bw,1.5px) var(--note-bs,solid) var(--note-bd) · คงสีตีมเดิม
- .sec (กล่องกลุ่มเมนู): border -> var(--grp-bw,1px) var(--grp-bs,solid) var(--grp-bd)
- .sec-h (เส้นใต้หัวกลุ่ม): border-bottom -> var(--grp-bw,1px) var(--grp-bs,solid) var(--grp-bd) = คุมด้วย grp-bw/bs ร่วมกับกล่องกลุ่ม (เข้าชุดกัน)
- กลุ่มใหม่ "ขอบกล่อง" ในพาเนลธีม โผล่เสมอ (ไม่เฉพาะตีม custom): body += _themeBorderGroupHtml() หลัง dropdown head
  - กล่องโน้ต: หนา (dropdown 0.5-3px) + แบบ (ทึบ/ประ/จุด/ไม่มี)
  - กล่องกลุ่ม: หนา + แบบ
- เก็บเป็น inline CSS var บน <html> (--note-bw/bs, --grp-bw/bs) อิสระจากตีม: _themeApply ลบแค่ _THEME_VARS (9 สี) ไม่แตะ border vars -> สลับตีมไม่รีเซ็ต · clone documentElement จับ inline style -> ติดไฟล์+พิมพ์
  - ไม่ใช้ localStorage (เป็น document setting แบบ data-rulehide) · default ผ่าน var() fallback · markDirty เมื่อเปลี่ยน
- native select onchange = apply ทันที (live) · อ่านค่าปัจจุบันจาก documentElement.style ตอน render panel = sync เสมอ
- i18n ครบ TH+EN (th.bw/bs/grpNoteEdge/grpGrpEdge/bsSolid/bsDashed/bsDotted/bsNone)
- lint #112 ล็อก: .crab/.sec/.sec-h ใช้ var(bw/bs) + ฟังก์ชัน + panel insert + i18n ครบ
- lint PASS (rc=0), เขียนดิสก์ (html 8,141,552 bytes)

## รอผู้ใช้ทดสอบ (F5)
1. แท็บ หน้า > ธีม: มีกลุ่ม "ขอบกล่อง" โผล่เสมอ (ทั้งตีมสำเร็จรูปและ custom)
2. เปลี่ยน หนา/แบบ ของกล่องโน้ต -> กรอบกล่อง * ทางร้านไม่มีเมนูปู เปลี่ยนทันที
3. เปลี่ยน หนา/แบบ ของกล่องกลุ่ม -> กรอบกล่องเมนูหมู/เนื้อ + เส้นใต้หัวกลุ่ม เปลี่ยนพร้อมกัน
4. สลับตีม (dropdown) -> ความหนา/แบบ ไม่รีเซ็ต (คงค่าที่ตั้ง) · สีกรอบเปลี่ยนตามตีม
5. เลือกแบบ "ไม่มี" -> กรอบหาย

## ค้างถัดไป
- contrast .ep-preview #6b7280 = 4.42 ยังตก WCAG 4.5
- ปุ่มยืนยัน ปรับราคา แยกโซนด้วยเส้นคั่น? · ตัวคั่น สี · รูป รอเลือกแบบ · popup เล็ก
- local override ต่อ element (คลิกกล่องแต่ละอันปรับเฉพาะอัน) - ยังไม่ทำ (รอบนี้ทำ global)

## commit ที่จะใช้ (ผู้ใช้รันเองที่ C:\OE)
git add -A
git commit -m "feat: เส้นกรอบกล่องโน้ต/กลุ่มเมนู ปรับความหนา+แบบเส้นได้ (global อิสระจากตีม ติดไฟล์+พิมพ์) + lint #112"
git push

HEAD ก่อนหน้า: 0a6add4
