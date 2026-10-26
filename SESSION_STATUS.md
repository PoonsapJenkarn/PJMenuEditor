# SESSION STATUS - OE Isan Menu Editor

ปรับปรุงล่าสุด: 2026-10-26 09:15 (+07)

## เสร็จรอบนี้ (ยังไม่ commit) - เฟส 1 ระบบเลย์เอาต์ (เท็มเพลต): ฐาน + A + B
- แท็บใหม่ "เท็มเพลต" (data-tab="template") แทรกหลังแท็บ "หน้า" · rpane ใหม่ data-pane="template"
- ระบบ layout แนวเดียวกับ data-theme: attribute data-layout บน <html> · default (ไม่มี attr) = 2col(A) · data-layout="1col" = B
- CSS: :root[data-layout="1col"] .grid{flex-direction:column} + .col{flex:0 0 auto;width:100%}
  - CRITICAL: :root[data-layout="1col"] body.measuring .grid{flex-direction:column !important} = override ตัวแบ่งหน้า (body.measuring บังคับ row) ให้ 1col วัด overflow เป็น column ถูกต้อง (specificity สูงกว่า)
- JS: _LAYOUTS + _layoutCur/_layoutSyncBtns/_layoutApply(id,persist)/_layoutPick/_layoutLoad (mirror pattern ของ theme) · เก็บ localStorage(oe_layout) + attribute ติดไฟล์ · _layoutApply เรียก checkOverflow({quiet:true})
- ปุ่มใน rpane: btnLayout_2col / btnLayout_1col (b-lg + svg + span) · active = เขียว #217346 (เพิ่มใน 3 selector list)
- startup: _layoutLoad() หลัง _themeLoad();_ruleHideSync();
- i18n ครบ TH+EN: tab.template, lay.2col, lay.1col, grp.layout, fl.layoutSet
- lint #114 ล็อกครบ: CSS 1col + measuring override + 5 ฟังก์ชัน + 2 ปุ่ม + tab + rpane + active เขียว + startup + i18n
- lint PASS (rc=0), เขียนดิสก์ (html 8,147,830 bytes)

## ⚠️ ข้อจำกัดที่ต้องบอกผู้ใช้ (Layout B)
- Layout B stack เป็น 1 คอลัมน์ด้วย CSS · หน้าที่เต็มพอดีในแบบ 2 คอลัมน์ พอ stack เนื้อหาสูงขึ้น ~2 เท่า = อาจล้นหน้า (ต้องเพิ่มหน้า/ย้ายกลุ่มเอง)
- การ reflow กลุ่มข้ามหน้าอัตโนมัติ = งานเฟสหลัง (ยังไม่ทำ) · ตอนนี้ B เหมาะกับเมนูที่แต่ละหน้ารายการไม่แน่นมาก

## รอผู้ใช้ทดสอบ (F5)
1. แถบแท็บ: ข้อความ · รูป · หน้า · เท็มเพลต · หน้าจอ · ไฟล์ (เท็มเพลตหลังหน้า)
2. แท็บ เท็มเพลต: ปุ่ม 2 คอลัมน์ / 1 คอลัมน์ · ปุ่มที่เลือกอยู่ = เขียว
3. กด 1 คอลัมน์ -> เมนูทั้ง 2 หน้า stack เป็นคอลัมน์เดียว (กลุ่มซ้ายก่อน กลุ่มขวาตาม)
4. กด 2 คอลัมน์ -> กลับเป็นปัจจุบัน
5. พิมพ์/Save ตอนเลือก 1col -> layout ติดไปกับไฟล์ (data-layout บน html)
6. (ข้อจำกัด) 1col หน้าที่แน่นจะล้น = ปกติของเฟสนี้ ยังไม่ reflow

## เฟสถัดไป
- เฟส 2: Layout C (3 คอลัมน์) = ต้อง JS redistribute กลุ่มลง 3 คอลัมน์ + ทดสอบแบ่งหน้าหนัก (เสี่ยงสูง แยกก้อน)
- (ถ้าผู้ใช้ต้องการ) auto-reflow กลุ่มข้ามหน้าสำหรับ 1col

## ค้างอื่นๆ
- กล่องโน้ต หดกว้างตามข้อความ? · contrast .ep-preview 4.42 · ปุ่มยืนยันปรับราคาแยกโซน? · ตัวคั่น สี·รูป · popup เล็ก · local override ต่อ element

## commit ที่จะใช้ (ผู้ใช้รันเองที่ C:\OE)
git add -A
git commit -m "feat: เฟส 1 ระบบเลย์เอาต์ (เท็มเพลต) - แท็บเท็มเพลต + Layout A(2col)/B(1col) + lint #114"
git push

HEAD ก่อนหน้า: 58b5a2d (+ Blue Ocean, ย้ายแท็บไฟล์ ถ้ายังไม่ push ตามลำดับ)
