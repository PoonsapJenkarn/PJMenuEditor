# OE Isan Menu — SESSION STATUS

อัปเดตล่าสุด: Thu 22 Oct 2026, 21:45 +07

## งานล่าสุด: panel เพิ่มหลายหน้า เปลี่ยน label เป็น "เพิ่ม [ ] หน้า" (หน่วยต่อท้ายช่อง)
ผู้ใช้สั่ง: เปลี่ยน "เพิ่มหน้า [box]" → "เพิ่ม [box] หน้า" (label นำหน้าช่อง "เพิ่ม" + หน่วย "หน้า" ต่อท้ายช่อง)
อ้างอิง: แบบ "กริยา [เลข] หน่วย" = แนวมาตรฐาน insert N rows/pages (Excel/Sheets)

## สถานะ: ✅ เขียนลงดิสก์แล้ว · lint จริงจากดิสก์ PASS (rc=0) — รอผู้ใช้ทดสอบใน browser
- เขียน OEIsanHotpotMenuEditor.html + lint_oe.py (assert-gated)
- re-run lint จากดิสก์: rc=0 · braces 3383:3383 สมดุล
- token ครบ: _sufT, ep-suffix, suffixKey:'pnl.addPageSuf', pnl.addPageSuf (หน้า/pages), pnl.addPageLabel='เพิ่ม'
- **ยังไม่ commit**

## สิ่งที่เปลี่ยน
- openPanel โหมด prompt: เพิ่ม slot suffix (opts.suffixKey/opts.suffix) → render .ep-suffix ต่อท้าย input (เดิมมีแต่ label หน้า input)
- _sufT() helper (คู่กับ _lblT) + _panelRelang อัปเดต suffix ตอนเปลี่ยนภาษา
- CSS .ep-suffix (mirror .ep-label) — #edpanel เป็น flex row อยู่แล้ว label·input·suffix·preview เรียงบรรทัดเดียว
- openAddPagesPanel: + suffixKey:'pnl.addPageSuf'
- i18n: pnl.addPageLabel 'เพิ่มหน้า'→'เพิ่ม' (TH), 'Add pages'→'Add' (EN) · ใหม่ pnl.addPageSuf 'หน้า'/'pages'
- ปุ่ม ribbon หลัก "เพิ่มหน้า" (btn.addPage) ไม่เปลี่ยน — เปลี่ยนเฉพาะ label ใน panel
- lint ข้อ 89: + เช็ค pnl.addPageSuf + ep-suffix + suffixKey (ล็อกรูปแบบ "เพิ่ม [N] หน้า")
- suffix slot เป็น generic — panel prompt อื่นในอนาคตใช้ได้ด้วย

## รอทดสอบ (browser · refresh F5 ก่อน)
1. กด caret ▾ ข้างปุ่มเพิ่มหน้า → panel ขึ้นเป็น "เพิ่ม [2] หน้า" (label เพิ่ม + ช่อง + หน่วยหน้า บรรทัดเดียว)
2. สลับ EN → "Add [2] pages"
3. พิมพ์เลข → preview + เพิ่มหน้าทำงานปกติเหมือนเดิม
4. ปุ่ม ribbon หลักยังเขียน "เพิ่มหน้า" เหมือนเดิม

## ขั้นถัดไป (หลังผู้ใช้ยืนยันผ่าน)
commit ทั้งชุด → push (ฐานล่าสุด 0b2f92c)

## ค้างสะสม (ยังไม่ commit)
1. บั๊กปุ่มซ่อนเนื้อหา sync ตอนคลิกเปลี่ยนหน้า — ทดสอบผ่านแล้ว
2. ปุ่มเพิ่มหน้า split button (ปุ่มหลัก +1 + caret) — ทดสอบผ่านแล้ว
3. panel เพิ่มหลายหน้า label "เพิ่ม [ ] หน้า" — รอทดสอบ

## ค้างตัดสิน
- GF_Knowledge_Notes.md จะเก็บใน repo หรือถอด (git rm --cached)
- slider ความจาง จะให้ sync ตามหน้าที่เลือกด้วยไหม (ค่าเป็น global)
