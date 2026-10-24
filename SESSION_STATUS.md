# SESSION STATUS - OE Isan Menu Editor

ปรับปรุงล่าสุด: 2026-10-24 13:00 (+07)

## เสร็จรอบนี้ (ยังไม่ commit) - custom dropdown ธีม + live preview
- เปลี่ยนตัวเลือกธีมจาก native <select> เป็น custom dropdown (listbox เอง) เพราะ native select เลื่อน/ชี้ในลิสต์ที่เปิดอยู่ไม่ยิง event = preview ตอนเลื่อนไม่ได้ (ข้อจำกัดเบราว์เซอร์)
- พฤติกรรม: ชี้/เลื่อน(ลูกศร)=ดูธีมจริงบนหน้าทันที (ไม่ persist) · คลิก/Enter=ยืนยัน(commit+บันทึก) · Esc/คลิกนอก/ปิด panel=คืนธีมเดิม
- JS ใหม่: _themePreviewVisual (ภาพอย่างเดียว ไม่แตะ _theme) + _themeDdHtml/Toggle/Open/Close/Detach/Preview/Commit/Key/SetHl · _THEME_ORDER (custom แรกเสมอ) + _THEME_KEYS
- preview รองรับทั้ง preset (ถอด inline vars) และ custom (ใส่ inline vars จาก localStorage กลับ) · revert = _themePreviewVisual(committed)
- keyboard: ArrowUp/Down เลื่อน+preview, Enter=commit, Esc/Tab=ปิด+คืนเดิม · a11y role=listbox/option
- เก็บ document listener (mousedown/keydown capture) ตอนเปิด ถอดตอนปิด (กัน leak) · commit ตั้ง _themeDd=null ก่อนเรียก _themePick เพื่อไม่ให้ onClose ของ panel revert ธีมที่เพิ่ง commit
- แก้ _themeSwatchActiveSeg: เดิม set select.value='custom' -> เปลี่ยนเป็นอัปเดต trigger label (#themeDdCur) + mark option custom (เพราะ select ไม่มีแล้ว)
- panel theme เพิ่ม onRelang:_themeRenderPanel (เปลี่ยนภาษา = rebuild ทั้ง dropdown) + onClose เพิ่ม _themeDdClose(true)
- CSS: .ep-ddwrap/.ep-dd-trigger/.ep-dd-pop/.ep-dd-opt (แทน .ep-theme-sel ที่ถอดออก) · hover/hl เขียว #217346
- ลบ dead: .ep-theme-sel CSS rule + ฟังก์ชัน mk() + native select markup + query .ep-theme-sel (เหลือ ep-theme-sel 1 ตัวใน comment เก่าเท่านั้น ไม่ใช่โค้ดทำงาน)
- lint: อัปเดต #94 (3 จุดที่ผูกกับ select -> ตรวจ _themeDdHtml/_themeDdPreview/_themeDdCommit + _THEME_ORDER custom-first) + เพิ่ม #109 (ล็อกฟังก์ชัน dropdown+preview+revert+CSS)
- lint PASS (rc=0), เขียนดิสก์ (html 8,137,370 bytes)

## รอผู้ใช้ทดสอบ (F5 ก่อน)
1. แท็บ หน้า > ธีม > คลิก dropdown -> ชี้/เลื่อนเมาส์แต่ละธีม = หน้าเมนูเปลี่ยนตามทันที (preview)
2. คลิกธีม = ยืนยัน (ค้างธีมนั้น) · กด Esc หรือคลิกนอก = เด้งกลับธีมเดิม (ไม่ค้างธีมที่แค่ชี้)
3. ลูกศรขึ้น-ลง = เลื่อน+preview, Enter = ยืนยัน
4. เลือก กำหนดเอง = เข้าโหมดแก้ 9 โซน (เหมือนเดิม) · แก้สีโซน -> trigger โชว์ "กำหนดเอง"
5. custom อยู่บนสุดของลิสต์เสมอ

## ค้างถัดไป
- comment เก่าใน CSS ยังมีคำ .ep-theme-sel (cosmetic เท่านั้น) - เก็บกวาดได้ถ้าต้องการ
- contrast .ep-preview #6b7280 = 4.42 ยังตก WCAG 4.5
- ปุ่มยืนยัน ปรับราคา แยกโซนด้วยเส้นคั่น? · ตัวคั่น สี · รูป รอเลือกแบบ · popup เล็ก

## commit ที่จะใช้ (ผู้ใช้รันเองที่ C:\OE)
git add -A
git commit -m "feat: custom dropdown ธีม + live preview (ชี้=ดูจริง คลิก=ยืนยัน Esc/นอก=คืนเดิม) + lint #94/#109"
git push

HEAD ก่อนหน้า: a9ddd6f
