# OE Isan Menu — SESSION STATUS

อัปเดตล่าสุด: Thu 22 Oct 2026, 12:02 +07

## งานล่าสุด: ความจางกลุ่มเมนู (semi-transparent panel) — เห็นพื้นหลังลอดกลุ่มเมนูได้
ผู้ใช้เลือก: แนว A (แผงกึ่งโปร่งใส ปรับระดับได้) + ขอบเขต A (ต่อหน้า เข้าชุดกับพาเนลพื้นหลัง)
เหตุผล: Professional/Enterprise ใช้ semi-transparent tinted panel เพราะคุม contrast ได้ + พิมพ์ออกแน่นอน (frosted glass/blur พิมพ์ไม่ออก ไม่เหมาะเมนูที่ปริ้นต์)

## สถานะ: ✅ เขียนลงดิสก์แล้ว · lint จริงจากดิสก์ PASS (rc=0) — รอผู้ใช้ทดสอบใน browser
- เขียน OEIsanHotpotMenuEditor.html + lint_oe.py (assert-gated: anchor 0 + lint rc=0 ก่อนเขียน)
- re-run lint จากดิสก์: rc=0 · braces 3325:3325 สมดุล
- token ครบ: --secalpha, _pageBgSetSecAlpha, _bgSecDimCommit, bg.menuDim, rgba(255,255,255,var(--secalpha,1)), rgba(245,239,228,var(--secalpha,1))
- **ยังไม่ commit**

## สิ่งที่เปลี่ยน
- CSS: .sec พื้น rgba(255,255,255,var(--secalpha,1)) · .sec-h พื้น rgba(245,239,228,var(--secalpha,1)) !important · เพิ่ม print-color-adjust:exact ทั้งคู่
- ตัวหนังสือ/เส้นจุด/ราคา อยู่คนละชั้น ไม่โดน alpha → ทึบ 100% เสมอ (contrast ไม่เสีย)
- var ต่อหน้า --secalpha ตั้งบน .page (inherit ลง .sec/.sec-h) · ใช้ _pageBgTargets(scope) เดียวกับพื้นหลัง
- JS ใหม่: _pageBgSetSecAlpha / _bgSecDimLive / _bgSecDimCommit · var _pageBgSecFade
- _bgCur เก็บ secfade เพิ่ม · hydrate อ่าน --secalpha จาก .page · _bgReapply พา secfade ไป scope ใหม่
- slider ใหม่ "ความจางกลุ่มเมนู" (default 0 = ทึบเต็ม ไม่กระทบเอกสารเดิม · max 80 กัน contrast พัง) ต่อจาก "ความจางสี"
- i18n bg.menuDim (TH ความจางกลุ่มเมนู / EN Menu panel fade)
- lint ข้อ 85 ล็อกฟีเจอร์ (--secalpha + _pageBgSetSecAlpha + slider + i18n)
- boardmode .sec/.sec-h ใช้ !important override → ไม่กระทบ (โหมด monochrome ทึบเสมอ ถูกต้อง)

## รอทดสอบ (browser · refresh F5 ก่อน)
1. หน้าที่มีพื้นหลัง (เช่นหน้า 2) → เปิดพาเนลพื้นหลัง → เลื่อน "ความจางกลุ่มเมนู": กล่องเมนูโปร่งขึ้น เห็นพื้นหลังลอด · ตัวหนังสือยังชัด 100%
2. ขอบเขต "เฉพาะหน้านี้/ทุกหน้า/คี่/คู่/ช่วง" ใช้ได้เหมือนพื้นหลัง
3. ปริ้นต์/preview: สีกึ่งโปร่งพิมพ์ออก
4. default (ไม่แตะ slider) = กล่องทึบเหมือนเดิม ไม่เพี้ยน

## ขั้นถัดไป (หลังผู้ใช้ยืนยันผ่าน)
commit งานทั้งหมดรอบนี้ (พื้นหลัง layer ซ้อน + ความจางสี + ความจางกลุ่มเมนู) → push (ฐาน 547a397)

## ค้างสะสม (ยังไม่ commit ทั้งหมด)
- พื้นหลัง layer ซ้อน (สี+รูป ไม่ลบกัน) + ความจางสีแยกความจางรูป
- ความจางกลุ่มเมนู (semi-transparent panel ต่อหน้า)
