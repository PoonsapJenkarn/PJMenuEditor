# OE Isan Menu — SESSION STATUS

อัปเดตล่าสุด: Fri 23 Oct 2026, 00:42 +07

## งานล่าสุด: A4+caret ปรับเทียบจอ เป็น split button จริง (แก้ให้ตรง pattern ปุ่มเพิ่มหน้า)
ผู้ใช้ติง: caret ปรับเทียบจอรอบก่อนทำเป็น pill เดี่ยวลอยห่าง A4 2px — ไม่ตรง pattern split button ของปุ่มเพิ่มหน้า
ยอมรับ: ไม่มีเหตุผลที่ดีพอ ผมทำไม่ consistent เอง (เป็นแบบที่ 3 ที่ไม่ควรมี) · split button ดีกว่าเพราะสื่อความสัมพันธ์ A4(ซูม)+caret(ตั้งค่า)=primary+secondary เหมือนเพิ่มหน้า

## สถานะ: ✅ เขียนลงดิสก์แล้ว · lint จริงจากดิสก์ PASS (rc=0) — รอผู้ใช้ทดสอบใน browser
- re-run lint จากดิสก์: rc=0 · braces 3402:3402 สมดุล
- checks: a4split markup+css · A4 ตัดขอบขวา · caret มุมโค้งขวา · btnCal คง 1 · lint#69 btnCal.on ยังอยู่
- **ยังไม่ commit**

## สิ่งที่เปลี่ยน (HTML อย่างเดียว · lint ไม่แตะ)
- markup: wrap A4 + caret ใน <span class="a4split"> (กัน gap:2px ของ zoomctl แยก 2 ปุ่ม → ชิดเป็นหน่วยเดียว)
- CSS: .a4split{inline-flex} · A4 (#zoomA4) border-right:none + มุมขวาตัด (border-radius ซ้ายอย่างเดียว) · caret (#btnCal.a4caret) border-radius:0 6px 6px 0 (มุมขวา) + เส้นคั่นกลาง = border ซ้ายของ caret ประชิด A4 · margin-left:0 (เดิม 2px)
- ผลลัพธ์: A4+caret = 1 pill เชื่อมกัน มีเส้นคั่นกลาง เหมือน .addpage-split เป๊ะ
- คง id=btnCal → openCal/closeCal/lint #69 (ปุ่มเปิด modal active เขียว) ไม่ต้องแตะ
- A4 กดหลัก=ซูมทันที · caret=เปิด modal ปรับเทียบจอ (เหมือนเดิม)

## รอทดสอบ (browser · refresh F5 ก่อน)
1. A4 กับ caret ▾ ชิดกันเป็นปุ่มเดียว มีเส้นคั่นบางๆ กลาง (ไม่ใช่ 2 ปุ่มลอยห่างกัน) — หน้าตาเหมือนปุ่มเพิ่มหน้า
2. กด A4 = ซูมทันที · กด caret = เปิด modal ปรับเทียบจอ
3. caret เขียว active ตอนเปิด modal · ปิดแล้วเลิกเขียว
4. มุมโค้ง: ซ้าย(A4) โค้ง · ขวา(caret) โค้ง · กลางเป็นเส้นตรงชิดกัน

## ขั้นถัดไป (หลังผู้ใช้ยืนยันผ่าน)
commit รวมงานจัดแถบบน 2 โซน + A4 split button → push (ฐานล่าสุด 3b5c33e)

## ค้างสะสม (ยังไม่ commit)
1. จัดแถบบน 2 โซน + เส้นคั่น + ปรับเทียบจอเป็น caret (รอบก่อน) — ทดสอบผ่านบางส่วน
2. A4+caret เป็น split button จริง (รอบนี้) — รอทดสอบ

## ค้างตัดสิน / งานถัดไป
- icon identity (glyph generic) — งานใหญ่แยก · ยังไม่ตัดสิน (A รื้อ system / B เปลี่ยนชุด / C ทีละจุด)
- GF_Knowledge_Notes.md จะเก็บใน repo หรือถอด
- slider ความจาง จะให้ sync ตามหน้าที่เลือกด้วยไหม (ค่าเป็น global)
