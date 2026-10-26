# SESSION STATUS - OE Isan Menu Editor

ปรับปรุงล่าสุด: 2026-10-26 14:25 (+07)

## เสร็จรอบนี้ (ยังไม่ commit) - เฟส 2 Layout C (3 คอลัมน์) ด้วย CSS columns
- data-layout="3col": .grid{display:block;column-count:3;column-gap:14px} + .col{display:contents}
- เทคนิค: .col{display:contents} ยก .sec ขึ้นเป็น flow items ให้ multicol จัดเอง · .sec{break-inside:avoid} (มีอยู่แล้ว) กันกลุ่มแตกข้ามคอลัมน์
- กฎนอก @media = มีผลพิมพ์ด้วย · ไม่ต้อง override measuring (block+columns ไม่ใช่ flex, measuring row ไม่กระทบ)
- _LAYOUTS = ['2col','1col','3col'] · ปุ่ม btnLayout_3col (3 แท่งตั้ง svg) · active เขียว (3 selector list)
- i18n ครบ TH(3 คอลัมน์)+EN(3 columns)
- lint #114 ขยาย: 3col CSS (column-count:3 + .col display:contents) + .sec break-inside + ปุ่ม + _LAYOUTS + i18n
- lint PASS (rc=0), เขียนดิสก์ (html 8,148,587 bytes)

## ⚠️ ข้อจำกัดที่บอกผู้ใช้แล้ว (3 คอลัมน์)
- A4 กว้าง 186mm (หัก padding) / 3 คอลัมน์ ≈ 51mm/คอลัมน์ = แคบ
- เหมาะกับเมนูชื่อสั้น+ราคาหลักเดียว-สองหลัก (เครื่องดื่ม/ของหวาน/ท็อปปิ้ง) · ชื่อเมนูอีสานยาวจะตัด 2 บรรทัด/เส้นจุดสั้น
- ไม่เหมาะแทน 2 คอลัมน์ทั้งหมด = เป็นตัวเลือกสำหรับบางหน้า/บางเมนู

## รอผู้ใช้ทดสอบ (F5)
1. แท็บ เท็มเพลต: มีปุ่ม 2 คอลัมน์ / 1 คอลัมน์ / 3 คอลัมน์
2. กด 3 คอลัมน์ -> กลุ่มเมนูไหลลง 3 คอลัมน์ (แต่ละกลุ่มไม่แตกข้ามคอลัมน์)
3. ดูชื่อเมนูยาว (แจ่วฮ้อนหมู/ต้มแซบกระดูกอ่อน) ว่าแคบไปไหม — ตามข้อจำกัดด้านบน
4. พิมพ์/Save ตอน 3col -> layout ติดไฟล์
5. สลับ 2col/1col/3col ไปมา -> ปุ่มเขียวตามที่เลือก

## เฟส/งานถัดไป
- (ถ้า 3col แคบไป) อาจทำ auto-reflow หรือจำกัด 3col เฉพาะบางกลุ่ม
- กล่องโน้ต หดกว้างตามข้อความ? · contrast .ep-preview 4.42 · ปุ่มยืนยันปรับราคาแยกโซน? · ตัวคั่น สี·รูป · popup เล็ก · local override ต่อ element

## commit ที่จะใช้ (ผู้ใช้รันเองที่ C:\OE)
git add -A
git commit -m "feat: เฟส 2 Layout C (3 คอลัมน์) ด้วย CSS columns + lint #114"
git push

HEAD ก่อนหน้า: d853401
