# OE Isan Menu Editor — Session Status

## ✅ Checkpoint 2 — ปุ่มขอบตัวอักษร "A" = split A4 (เสร็จ · 23 ต.ค. 2026 · รอทดสอบ)
- ทำ .olpick เป็น frame เดียว (border #d2d0ce, radius 6px, height 30px) — A เป็นเซลล์หลัก (คง toggle เปิด/ปิดขอบ) + caret 22px เข้าชุด A4
- **scope เฉพาะ .olpick** — B/I/U/S (ตัวหนา/เอียง/ขีดล่าง/ขีดฆ่า) ใช้ .ttoggle เดิม ไม่โดน (verify: base .ttoggle untouched)
- ไม่ใช้ overflow:hidden (เพราะ .ol-pop อยู่ข้างใน .olpick — จะโดนตัด) → ใช้มุมโค้งที่เซลล์ในแทน
- inner: .olpick .ttoggle{border:none;radius:0} · #typoOutline radius ซ้าย · .on เขียวยังทำงาน (ไม่ set background ใน override → .ttoggle.on ยังชนะ)
- lint #97 ขยาย: ตรวจ .olpick frame #d2d0ce + olcaret 22px
- in-memory + disk lint PASS (rc=0) · token ครบ (ยกเว้น typo ข้อความ error ใน lint 'ไม่ใช้'→ควรเป็น 'ไม่ใช่' — ไม่กระทบการทำงาน)

## ✅ มาตรฐานปุ่มถาดสีครบทุกจุดแล้ว (checkpoint 1+2)
- ตัวอักษร(font) · พื้นหลัง · ธีม×9 · ขอบตัวอักษร A = split A4 เหมือนกันหมด
- มาตรฐานอยู่ UI_STANDARD.md §14 + lint #97

## ⏳ รอผู้ใช้ทดสอบ (Ctrl+Shift+R)
- แท็บข้อความ → คลิกข้อความ → ปุ่ม A (ขอบตัวอักษร): A + caret เป็นกรอบเดียว เหมือน A4 · กด A = เปิด/ปิดขอบได้ปกติ · caret hover เขียว
- เช็ค B/I/U/S ยังเป็นปุ่มเดี่ยวเหมือนเดิม (ไม่โดนแก้)
- เทียบกับปุ่ม A4 — ควรหน้าตาเหมือนกันทั้งกลุ่ม

## ⏳ ยังไม่ commit (รวม checkpoint 1+2 ได้)
cd C:\OE
git add -A
git commit -m "feat: ปุ่มขอบ A = split A4 (checkpoint 2 · scope .olpick ไม่โดน B/I/U/S) + lint #97"
git push

## ✅ มาตรฐานถาดสีครบวงจร (preview+ตกลง/ยกเลิก + split A4 button)
ทุกถาดสี (font/ขอบ/พื้นหลัง/ธีม): กดสี=preview · ตกลง=ติด · ยกเลิก/นอก=คืน · ปุ่มเปิด = split frame A4
(ถาดพื้นหลัง bg ยังเป็น instant-model เดิมตาม decision 21 ต.ค. — ถ้าจะทำ preview+OK/Cancel ด้วย ค่อยสั่ง)
