# OE Isan Menu Editor — Session Status

## ✅ เสร็จ (ถาดข้อความ D + ถาดขอบตัวอักษร B · 23 ต.ค. 2026 · รอทดสอบ)
มาตรฐานถาดสีใหม่ (previewสด + ตกลง/ยกเลิก) — ทำครบ 4 ถาด: ธีม(A) + ข้อความ(D) + ขอบ(B) · เหลือพื้นหลัง(C) กับ ความหนาขอบ 3 โซน(A2)

### ถาดข้อความ (D)
- ตัดปุ่ม "ทาสี" (typoCpPaint) ออก · ใส่ ตกลง/ยกเลิก แทน
- preview: คลิกทั้งช่อง/เส้นจุด = สดบนเมนู · ไฮไลต์บางคำ = preview ที่ปุ่มสี (ไม่แตะข้อความจนกดตกลง = คืนเป๊ะเสมอ) — ผู้ใช้เลือกเอง (safe)
- commit = applyColorRange (markDirty+undo 1 จุด) · cancel/คลิกนอก/Esc = คืนสีเดิม (_closePop auto-restore)
- typoCpApply กลายเป็นปุ่มเปิดถาด (เพิ่มใน _NOEDIT21 แล้ว)

### ถาดขอบตัวอักษร (B)
- คง อัตโนมัติ + ความหนาเส้น · เพิ่ม ตกลง/ยกเลิก ท้าย ol-pop
- preview = ตั้ง textShadow สด (ไม่ markDirty) · commit = _olApply+markDirty 1 จุด · cancel/ปิด = คืน textShadow เดิม (_olPopClose auto-restore ทุกเส้นทางปิด)
- delegation เปลี่ยนจาก typoOutlineSetColor/SetWidth ตรง → _olPvColor/_olPvWidth/_olPvAuto (preview) · .ol-add = HSV ชั้นรองคงเดิม

- CSS: เพิ่ม #typobar .cp-ok/.cp-cancel/.cp-actions (mirror #edpanel)
- lint #96 ล็อก: ห้ามมี typoCpPaint + ต้องมี _tcp*/_ol* commit/cancel + ปุ่มตกลงทั้ง 2 ถาด
- lint #21: typoCpApply → _NOEDIT21 (เปิดถาด ไม่แก้เมนูเอง)
- in-memory + disk lint PASS (rc=0) · token 18/18 · ไม่มี warning

## ⏳ รอผู้ใช้ทดสอบ (Ctrl+Shift+R) — แก้ข้อความที่แจ้งว่าไม่เปลี่ยน
- แก้ข้อความ → คลิกช่องข้อความ → กดถาดสี (▾) → กดสี = เมนูเปลี่ยนสด → ตกลง=ติด / ยกเลิก=คืน
- สีขอบตัวหนังสือ (ปุ่ม A ▾) → กดสี/ความหนา = preview → ตกลง/ยกเลิก
- ไฮไลต์บางคำแล้วเปลี่ยนสี → เมนูยังไม่เปลี่ยนจนกดตกลง (preview ที่ปุ่ม)

## ⏳ ยังไม่ commit
cd C:\OE
git add -A
git commit -m "feat: ถาดข้อความ+ขอบ preview+ตกลง/ยกเลิก ตัดทาสี (รอบ B+D) + lint #21/#96"
git push

## ⏳ รอบถัดไป
- A2: ความหนาขอบ 3 โซนธีม (note-bd/grp-bd/line-dot → --note-bw/--grp-bw/--line-bw) · .sec-h border-bottom ใช้ grp-bd ร่วม
- C: ถาดพื้นหลัง (bg) — ⚠ เคย instant (21 ต.ค.) ต้องเคาะก่อนเปลี่ยนเป็น ตกลง/ยกเลิก
