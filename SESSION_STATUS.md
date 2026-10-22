# OE Isan Menu — SESSION STATUS

อัปเดตล่าสุด: Thu 22 Oct 2026, 23:32 +07

## งานล่าสุด: ให้ panel ประวัติ (#actlog) ขยายตาม UI scale ด้วย
ผู้ใช้พบ: ปรับ A+/A− แล้ว toolbar/แถบล่างขยาย แต่ panel ประวัติไม่ขยาย
สาเหตุ: #actlog เป็น position:fixed แยกเดี่ยว (ไม่อยู่ใน #edbar/#edstatus) — รอบก่อน scope uiscale แค่ 2 element เลยตกหล่น (เป็นช่องโหว่ ไม่ใช่ตั้งใจ · ประวัติเป็น chrome ควรขยายตาม)

## สถานะ: ✅ เขียนลงดิสก์แล้ว · lint จริงจากดิสก์ PASS (rc=0) — รอผู้ใช้ทดสอบใน browser
- CSS: เพิ่ม #actlog{zoom:var(--uiscale,1);} (ต่อจาก #edbar/#edstatus) → chrome ครบ 3 ตัว
- lint ข้อ 91 แก้: guard "ห้าม zoom element อื่น" ครอบ #actlog ด้วย + บังคับต้องมี #actlog{zoom} (ทั้ง 3 chrome)
- re-run lint จากดิสก์: rc=0 · braces 3400:3400 สมดุล
- **ยังไม่ commit**

## chrome ที่ขยายตาม --uiscale (ครบแล้ว)
#edbar (tabs/ribbon/typobar/imgbar/edpanel) · #edstatus (แถบล่าง) · #actlog (ประวัติ) — .page (เมนู) ไม่โดน แยกด้วย --pagezoom

## รอทดสอบ (browser · refresh F5 ก่อน)
1. เปิดประวัติ (คลิกไอคอนซ้ายแถบล่าง) → กด A+ : panel ประวัติใหญ่ขึ้นตาม toolbar
2. กด A− : ประวัติเล็กลงตาม
3. ประวัติ align กับแถบล่าง ไม่มีช่องว่าง/ซ้อนกันตอน zoom (actlog bottom:32px scale ตาม)
4. เมนู A4 ยังไม่เปลี่ยนขนาด (ซูมเพจแยก)

## ขั้นถัดไป (หลังผู้ใช้ยืนยันผ่าน)
commit ทั้งชุด UI scale (toolbar+แถบล่าง+ประวัติ) → push (ฐานล่าสุด b622065)

## ค้างสะสม (ยังไม่ commit)
1. ตัวปรับขนาด UI chrome A−/A+ (toolbar+แถบล่าง) — ทดสอบผ่านแล้ว
2. #actlog ขยายตาม UI scale — รอทดสอบ

## ค้างตัดสิน
- GF_Knowledge_Notes.md จะเก็บใน repo หรือถอด (git rm --cached)
- slider ความจาง จะให้ sync ตามหน้าที่เลือกด้วยไหม (ค่าเป็น global)
