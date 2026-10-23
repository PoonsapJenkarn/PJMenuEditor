# OE Isan Menu Editor — Session Status

## ✅ เสร็จแล้ว (รอบ 1 — วางฐานธีมสี · 23 ต.ค. 2026)
- แทรก `:root` ตัวแปรสีกลาง 9 ตัว (5 โซน + สีตัวอักษร/เส้น) ที่ต้น <style> ก้อนแรก
  - โซน: --note-bd/--note-bg (ป้ายโน้ต .crab) · --grp-bd/--grp-head-bg/--grp-body-bg (กลุ่มเมนู .sec/.sec-h) · --txt-name/--txt-note/--txt-price/--line-dot (ตัวอักษร+เส้นจุด)
  - โซนพื้นกลุ่ม 4-5 เก็บเป็น RGB triple เพราะซ้อน var(--secalpha) ของฟีเจอร์ความจาง
- rewire 10 จุด: .crab, .sec border, .sec bg, .sec-h bg, .sec-h border-bottom, .nm, .nm .note, .ln, .pr, .secnote
- **default = สีเดิมเป๊ะ → ภาพต้องไม่เปลี่ยน (pure refactor)**
- เพิ่ม lint #93: ล็อก :root + 9 ตัวแปร + 5 โซนต้องใช้ var() + ห้าม hardcode สีเดิมกลับ
- in-memory lint PASS (rc=0) → เขียนดิสก์ → disk lint PASS (rc=0) → token 11/11 ครบ

## ⏳ รอผู้ใช้ทดสอบ
- รีเฟรช (F5/Ctrl+Shift+R) แล้วดูว่า **ภาพเหมือนเดิมทุกจุด** (ป้ายโน้ต/กรอบกลุ่ม/หัวกลุ่ม/ชื่อเมนู/ราคา/เส้นจุด/หมายเหตุ)
- ถ้าภาพเปลี่ยน = refactor พลาด แจ้งได้เลย

## ⏳ ยังไม่ commit (ให้ผู้ใช้รันเอง)
cd C:\OE
git add -A
git commit -m "refactor: วางฐาน :root ตัวแปรสีกลาง 5 โซน + สีตัวอักษร (รอบ1 ธีม) + lint #93"
git push

## 📋 รอบ 2 (ถัดไป — ยังไม่เริ่ม)
- เพิ่ม 4 ธีม (ครีม default / ขาว-เขียว / เข้ม-ทอง / กระดาษ-แดงอิฐ) สลับชุดตัวแปร + ปุ่มเลือกธีม
- **งานซ่อนรอบ 2:** สีตัวอักษรหัวกลุ่ม .sec-h = var(--accent) ตั้งแยกรายหมวด (ไม่อยู่ใน :root นี้) — ธีมเข้ม-ทองต้องจัดการหัวข้อเข้มบนพื้นเข้มเพิ่ม
