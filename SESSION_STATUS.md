# SESSION STATUS - OE Isan Menu Editor

ปรับปรุงล่าสุด: 2026-10-25 21:15 (+07)

## เสร็จรอบนี้ (ยังไม่ commit) - รวม tool เส้น/ขอบ เป็นพาเนลเดียว + แก้บั๊ก key ชน
### แก้บั๊ก key ชน (สำคัญ)
- th.bw/th.bs (ที่ใช้เป็น หนา/แบบ ของขอบกล่อง) ไปชนกับ th.bw ชื่อตีม "ขาว-ดำ" -> ป้ายขึ้น "ขาว-ดำ" แทน "หนา"
- แก้: เปลี่ยน key ขอบเป็น th.edgeW (หนา/Width) + th.edgeS (แบบ/Style) · th.bw คงเป็นชื่อตีมอย่างเดียว
- (lint #112 เดิมจับไม่เจอเพราะนับ key ที่ชนกันเอง - แก้ check แล้ว)

### รวมเป็นพาเนลเดียว "เส้น·ขอบ" ในแท็บหน้า
- ถอดกลุ่ม "ขอบกล่อง" ออกจากพาเนลธีม (ลบ _themeBorderGroupHtml + body += ...) เพราะเป็น global ไม่ผูกตีม อยู่ในธีมแล้วสับสน
- ถอดปุ่ม "ซ่อนเส้นคั่น" (btnRuleHide) ออกจากริบบอน
- สร้างปุ่มใหม่ btnLineEdge "เส้น·ขอบ" ในแท็บหน้า (แทนตำแหน่ง btnRuleHide เดิม) เปิดพาเนลรวม
- _lineEdgeRenderPanel + openLineEdgePanel: พาเนลรวม 3 กลุ่มใน thcp-row เดียว
  - เส้นคั่น: toggle ซ่อน/แสดง (btnRuleHide ย้ายมาอยู่ในพาเนล เป็น ep-mini.on เขียว)
  - ขอบกล่องโน้ต: หนา (th.edgeW) + แบบ (th.edgeS)
  - ขอบกล่องกลุ่ม: หนา + แบบ
- active-green สลับ btnRuleHide -> btnLineEdge (3 selector ใน #edbar)
- _ruleHideSync เพิ่ม else b.textContent (ปุ่มในพาเนลไม่มี span)
- i18n ใหม่ TH+EN: btn.lineEdge/grp.lineEdge/ttl.lineEdge · เปลี่ยน th.bw/bs -> th.edgeW/edgeS
- lint #110 ปรับ: ตรวจ btnLineEdge active เขียว + openLineEdgePanel + btnLineEdge exist
- lint #112 ปรับ: _lineEdgeRenderPanel + note-bw/grp-bw ในพาเนล + toggleRuleHide ในพาเนล + i18n th.edgeW/edgeS
- lint PASS (rc=0), เขียนดิสก์ (html 8,142,810 bytes)

## รอผู้ใช้ทดสอบ (F5)
1. แท็บ หน้า: ปุ่ม "เส้น·ขอบ" (แทน "ซ่อนเส้นคั่น" เดิม) · พาเนลธีมไม่มีกลุ่มขอบกล่องแล้ว
2. กดปุ่ม "เส้น·ขอบ" -> พาเนลรวม: toggle ซ่อนเส้นคั่น + ขอบกล่องโน้ต(หนา/แบบ) + ขอบกล่องกลุ่ม(หนา/แบบ)
3. ป้าย dropdown ความหนาต้องขึ้น "หนา" (ไม่ใช่ "ขาว-ดำ" แล้ว)
4. toggle ซ่อนเส้นคั่น -> เส้นคั่นใต้ส่วนหัวหาย ปุ่มเขียว label เป็น "แสดงเส้นคั่น"
5. ปุ่ม "เส้น·ขอบ" เขียวตอนเปิดพาเนล
6. สลับภาษา TH/EN ขณะเปิดพาเนล -> ป้ายแปลถูก

## ค้างถัดไป
- contrast .ep-preview #6b7280 = 4.42 ยังตก WCAG 4.5
- ปุ่มยืนยัน ปรับราคา แยกโซนด้วยเส้นคั่น? · ตัวคั่น สี · รูป รอเลือกแบบ · popup เล็ก
- local override ต่อ element (คลิกกล่องปรับเฉพาะอัน) - ยังไม่ทำ

## commit ที่จะใช้ (ผู้ใช้รันเองที่ C:\OE)
git add -A
git commit -m "feat: รวม tool เส้น/ขอบ เป็นพาเนลเดียว 'เส้น·ขอบ' แท็บหน้า (ซ่อนเส้นคั่น+ขอบกล่องโน้ต/กลุ่ม) + แก้บั๊ก key ชน th.bw + lint #110/#112"
git push

HEAD ก่อนหน้า: 0a6add4
