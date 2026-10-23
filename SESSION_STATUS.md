# OE Isan Menu Editor — Session Status

## งานใหญ่: ย้ายธีมเป็นพาเนลจัดระเบียบ (ตาม mockup อนุมัติ) — แบ่ง 2 checkpoint
พาเนลธีมก่อน → แล้วค่อย local override ต่อ element (กล่องกลุ่ม/โน้ต/หัวกลุ่ม)

## ✅ Checkpoint 1 — โครงพาเนลใหม่ (เสร็จ · 23 ต.ค. 2026 · รอทดสอบ)
- preset: segment 5 ปุ่ม → **dropdown** (.ep-sel .ep-theme-sel · onchange=_themePick(this.value)) · mk() สร้าง <option> แทน <button>
- 9 โซน flat → **3 กลุ่มมีป้าย**: กล่องโน้ต (พื้น/ขอบ) · กลุ่มเมนู (พื้นหัว/พื้นเนื้อ/ขอบ) · ตัวอักษร (ชื่อ/ราคา/หมายเหตุ/เส้นจุด) · เส้นคั่น .thcp-sep ระหว่างกลุ่ม
- _thcp ทั้ง 9 ยังเหมือนเดิม (split swatch A4) แค่ห่อใน .thcp-cat/.thcp-cat-z มีหัว .thcp-cat-h
- _themeSwatchActiveSeg: toggle .theme-opt.on → set dropdown .ep-theme-sel = 'custom'
- ลบ CSS .ep-seg .theme-opt (เลิกใช้) · เพิ่ม CSS .thcp-cat/.thcp-cat-h/.thcp-cat-z/.thcp-sep/.ep-theme-sel
- i18n เพิ่ม th.grpNote/th.grpGroup/th.grpText (TH+EN)
- lint #94: เลิกเช็ค .ep-seg .theme-opt/.ep-mini.on → เช็ค .ep-theme-sel + onchange ผูก _themePick · lint #95: เพิ่ม grp keys
- **ยังเป็นสีล้วน** — ความหนาขอบยังไม่ใส่ (checkpoint 2)
- in-memory + disk lint PASS (rc=0) · token 18/18

## ⏳ รอผู้ใช้ทดสอบ Checkpoint 1 (Ctrl+Shift+R)
1. หน้า → ธีม → preset เป็น dropdown (เลือกครีม/ขาว-เขียว/เข้ม-ทอง/กระดาษ-แดงอิฐ/กำหนดเอง)
2. เลือกธีม preset จาก dropdown → สีเมนูเปลี่ยนตาม
3. เลือก 'กำหนดเอง' → 9 โซนโผล่เป็น 3 กลุ่มมีป้าย (กล่องโน้ต/กลุ่มเมนู/ตัวอักษร) เห็นครบ
4. แต่ละโซนกดเปิดถาดสี preview+ตกลง/ยกเลิก ได้เหมือนเดิม
5. สลับ TH/EN → ชื่อกลุ่ม + ชื่อ preset เปลี่ยนภาษา

## ⏳ Checkpoint 2 (ถัดไป — ยังไม่เริ่ม)
เพิ่มความหนาขอบ 3 โซน: --note-bw/--grp-bw/--line-bw ใน :root ทุกธีม + rewire .crab/.sec/.ln + ตัวปรับความหนาในแถวโซนขอบ (preview/commit) · .sec-h border-bottom ใช้ --grp-bd ร่วม → ความหนาขอบกลุ่มคุมด้วย

## ⏳ งานใหญ่ถัดจากพาเนลธีม: local override ต่อ element
คลิกกล่องกลุ่มเมนู/กล่องโน้ต/หัวกลุ่ม → แก้ขอบ/พื้น/gradient เฉพาะชิ้น (ไม่กระทบธีม) · ตาม idiom data-* เดิม (data-ol-c/data-acc0) · Canva-style local + theme อยู่ด้วยกัน

## ⏳ ยังไม่ commit (ให้ผู้ใช้รันเอง)
cd C:\OE
git add -A
git commit -m "feat: พาเนลธีม preset dropdown + 9 โซน 3 กลุ่มมีป้าย (checkpoint 1) + lint #94/#95"
git push
