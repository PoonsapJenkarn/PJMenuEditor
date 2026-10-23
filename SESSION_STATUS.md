# OE Isan Menu Editor — Session Status

## ✅ cursor หมายเหตุชิดซ้าย + caret หนาขึ้นทั้งแอป (เสร็จ · 23 ต.ค. 2026 · รอทดสอบ)

### 1. cursor หมายเหตุไปติดกากบาทแดง
- สาเหตุ: .secnote text-align:right (ดีไซน์ตั้งใจ) → cursor ไปขวาชนกากบาท ×
- แก้: body.editmode .secnote[contenteditable] += text-align:left (เฉพาะตอนแก้) → พิมพ์ชิดซ้าย cursor อยู่หน้า
- base .secnote ยัง right — บนเมนูจริง/ตอนพิมพ์คงชิดขวาตามดีไซน์เดิม

### 2. caret ทั้งแอป (ทุกช่องที่พิมพ์ได้)
- selector: [contenteditable="true"] + input ใน edbar/edpanel/typobar/edtabs/calModal
- caret-shape:block = หนาขึ้นจริง (Chrome/Edge ใหม่รองรับ · ไม่รองรับ = เส้นปกติ ไม่ error)
- **สำคัญ: caret-color:currentColor ไม่ใช่ #171a1e ตายตัว** — เพราะสีดำตายจะหายในธีมเข้ม-ทอง (ตัวอักษรสว่างบนพื้นเข้ม) · currentColor = ตามตัวอักษร = พื้นสว่างได้เข้ม (=ดำตามที่ขอ) · ธีมเข้มได้สว่างไม่หาย
- lint #100 ล็อก: caret-shape:block + caret-color:currentColor + secnote edit text-align:left

- in-memory + disk lint PASS (rc=0) · token 4/4

## ⏳ รอผู้ใช้ทดสอบ — Ctrl+Shift+R
1. แก้ไขข้อความ → กด "+ หมายเหตุ" → cursor อยู่ซ้าย ไม่ชน × แดง
2. cursor ทุกช่องพิมพ์ (ชื่อเมนู/ราคา/ช่อง HEX/ซูม) → หนาขึ้นเป็นบล็อก (ถ้าใช้ Chrome/Edge)
3. ลองธีมเข้ม-ทอง → แก้ข้อความ → caret ยังเห็น (สว่าง) — ไม่หาย

## ⏳ ยังไม่ commit
cd C:\OE
git add -A
git commit -m "feat: cursor หมายเหตุชิดซ้าย(ตอนแก้) + caret หนาขึ้น block + สีตามตัวอักษร + lint #100"
git push

## ค้าง (ตามลำดับ)
- ธีม: Checkpoint 2 ความหนาขอบ 3 โซน (--note-bw/--grp-bw/--line-bw) + local override element
