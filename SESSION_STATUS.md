# OE Isan Menu Editor — Session Status

## ✅ Checkpoint 2 — ตรึงหน้าใน toggleEdit (เสร็จ · 23 ต.ค. 2026 · รอทดสอบ)

### ต้นเหตุ (คนละกลไกกับ #98)
รอบ #98 แก้ measuring clamp ใน checkOverflow ไปแล้ว — แต่เข้าโหมดแก้ยังเด้งเพราะอีกกลไก: ตอนเข้า editmode ทุกหน้า **สูงขึ้น** (.page height:auto + padding/ปุ่มโหมดแก้) → หน้าใหม่ (หน้า 3) ถูกดันลง → viewport ไปจบที่ท้ายหน้า 2

### วิธีแก้ (pixel-perfect ไม่กระโดด)
- ต้น toggleEdit: จับ _veIdx99=_priceVisiblePage() + _veTop99=rect.top ของหน้านั้น **ก่อน** toggle editmode
- ท้ายฟังก์ชัน (หลัง checkOverflow): ถ้า on → scrollTop += (rect.topใหม่ - _veTop99) = ชดเชยส่วนที่สูงขึ้นด้านบน → หน้าที่ดูอยู่คงตำแหน่งเดิมเป๊ะ
- reuse _priceVisiblePage (generic — หาหน้าที่เห็นมากสุดระหว่าง bar/status)
- ไม่ใช้ scrollIntoView (จะกระโดดไปหัวหน้า) — ใช้ scrollTop += delta แทน
- lint #99 ล็อก: toggleEdit ต้องมี _veIdx99 + _priceVisiblePage + scrollTop
- in-memory + disk lint PASS (rc=0) · token 9/9 · capture ก่อน toggle / restore หลัง checkOverflow ยืนยันแล้ว

## ⏳ รอผู้ใช้ทดสอบ — Ctrl+Shift+R
เพิ่มหน้าใหม่ → (อยู่หน้าใหม่) → คลิก "แก้ไขข้อความ" → ควรอยู่หน้าใหม่ที่เดิม (ตำแหน่งเดิม) ไม่เด้งไปท้ายหน้า 2
รวมกับ #98: เพิ่ม/ลบรายการก็ไม่เด้ง → ครบทั้ง 2 เคสแล้ว

## ⏳ ยังไม่ commit (รวม #98 + #99 — ค้างทั้งคู่)
cd C:\OE
git add -A
git commit -m "fix: ตรึงหน้าตอนเข้าโหมดแก้ (scrollTopชดเชยความสูง toggleEdit) + lint #99"
git push

## ค้าง (ตามลำดับ)
- ธีม: Checkpoint 2 ความหนาขอบ 3 โซน (--note-bw/--grp-bw/--line-bw) + local override element
