# OE Isan Menu — Session Status

**อัปเดตล่าสุด:** 27 ก.ย. 2026, 16:14 — v74: align selection subsystem กับ mockup (แก้ไฮไลท์ไม่ activate + สีไม่ติด)

## 2 ต.ค. 2026 (10:20) — กำลัง commit
- ปุ่มสี: แสดงสีของตัวอักษรที่คลิกจริง (_typoPtr) — ผู้ใช้ทดสอบผ่าน
- คลิกโดยไม่ไฮไลท์ = ล้างช่วงไฮไลท์เก่า (saveSelection) — สี/ฟอนต์ลงทั้งช่องที่คลิก
- เพิ่ม verify_oe.py (ตรวจ static ผ่าน / ส่วน headless browser ยังไม่เคยรันบนเครื่อง) — ยังไม่ใส่ใน pre-commit hook
ค้างหลัง commit: panel "คืนค่า" ปิด panel ก่อนอ่านค่า (เลือกขอบเขตแล้วไม่มีผล) · รัน python verify_oe.py บนเครื่อง · backlog: Export log (มีแค่ CSS .al-export*), QR Code (รอ URL), ลบ .bak 38 ไฟล์ ~212MB

## 1 ต.ค. 2026 (20:30) — ยังไม่ commit
- ใช้ทั้งประเภท: คัดลอกรูปแบบช่องต้นทางแบบละเอียด (style ทั้งช่อง + สีเฉพาะตัวอักษร เช่น "นู" แดง) ไปช่องอื่น — ช่องต้นทางไม่เปลี่ยน
  - ข้อความเหมือนต้นทาง = ตำแหน่งเดียวกัน · ข้อความต่าง = ทุกจุดที่มีคำเดียวกัน (ไม่มีคำนั้น = ไม่ทาเฉพาะตัวอักษร)
  - ฟังก์ชัน: _typoCaptureFormat / _typoWrapRange / _typoApplyFormat (แทน _typoStyleAtCursor ที่ลบแล้ว)
- ใช้ทั้งประเภท: แก้ panel ปิดก่อนอ่านค่า (readValues) · ปุ่ม "นำไปใช้" · "ทั้งเพจ"→"ทุกหน้า" · แจ้งจำนวนช่องที่เปลี่ยนจริง
- toolbar ตอนลากไฮไลท์: selectionchange เรียก typoSelect + click ไม่ typoClear ถ้ายังมีไฮไลท์ (รอผู้ใช้ยืนยัน)
ค้าง: panel "คืนค่า" ยังมีบั๊กปิด panel ก่อนอ่านค่า · ปุ่มสีไม่แสดงสีของข้อความที่ไฮไลท์ · ผลรัน verify_oe.py บนเครื่อง

## 28 ก.ย. 2026 (21:xx) — ยังไม่ commit
แก้แล้วบนดิสก์ (รอผู้ใช้ทดสอบ):
- ตั้งค่าเริ่มต้น แยกตามประเภท element (`_defaultStyles[key]`) ใช้กับ row ใหม่เท่านั้น ของเดิมไม่แตะ
- ปุ่มตั้งค่าเริ่มต้น: disabled เมื่อไม่ได้เลือก element / เขียวเมื่อประเภทนั้น set แล้ว
- ทาสี: ไม่ไฮไลท์ = ทั้ง element, ไฮไลท์ = เฉพาะช่วง
- คลิก element → ปุ่มสีเปลี่ยนตามสี element (`window._setCurrent`)
- คืนปุ่ม "คืนค่า" (typoResetBtn) ที่โดนลบโดยไม่ตั้งใจ
ค้าง: Export log (มีแค่ CSS `.al-export*` ยังไม่มีปุ่ม/โค้ด), QR Code (รอ URL), ลบ .bak (38 ไฟล์ ~212MB — ยังไม่ลบ)

### เครื่องมือตรวจใหม่: `verify_oe.py`
รันหลังแก้ทุกครั้ง: `python verify_oe.py` → PASS(0) / FAIL(1) / INCOMPLETE(2)
ตรวจ: lint_oe.py + JS structure + ฟังก์ชันหลักครบ + id ที่อ้างถึงมีจริง + id/ฟังก์ชันหายเทียบ HEAD + diff + เปิด Chrome headless ทดสอบแท็บ/โหมดแก้/ปุ่มตั้งค่าเริ่มต้น/ปุ่มสี
ตั้งใจลบ id: `set OE_ALLOW_REMOVE_IDS=id1,id2`

## v74 (27 ก.ย. 2026) — แก้ selection subsystem ให้ตรง mockup
รากปัญหา (พบจากเทียบ mockup ที่ทำงานได้ vs ไฟล์จริง) — 3 handler v73 ตีกันเอง:
1. **selectionchange** เดิม `if(r.collapsed){_typoSelRange=null}` → พอ focus ย้ายเข้า HEX, range หาย → แก้: เก็บเฉพาะ non-collapsed, ไม่ null เมื่อ collapse (align mockup L163)
2. **mousedown** เดิม return เฉยๆ → แก้: snapshot range ก่อน focus ย้าย (align mockup L212) + เพิ่ม typoHex ใน guard
3. **click handler** เดิมคลิกที่ว่าง `typoClear()` เสมอ → click-after-drag ล้าง selection ที่เพิ่งไฮไลท์ → แก้: deselect เฉพาะเมื่อไม่มี live highlight ใน field
verify: depth 0, brace 988:988, paren 2441:2441 — **รอเทสต์**

## ไฟล์หลัก
`C:\OE\OEIsanHotpotMenuWithImageEditor.html` (~5.7MB) บน TH-JH3W034

## Git commits (user รันเอง)
- `29ecda3` — v63–v66 (bulk price + undo 1000 + POOL GC + log panel)
- `12cb2a9` — v67–v69 (flash ละเอียด + panel i18n + status reset)
- **v70 บนดิสก์ ยังไม่ commit** (partial formatting engine Step 1)

## กำลังทำ: PORT typography mockup → ไฟล์จริง (v71)

### สถานะไฟล์จริง v70 (มีอยู่แล้ว)
- `_typoWrap(prop,val)` — Range API span-wrap ✅
- `_typoSelRange` + selectionchange tracking ✅
- typoColorLive/typoColorApply/typoFontApply/typoSizeStep ✅
- typoClearSel/typoClearField (มี `_snapNow()` → undo ได้) ✅
- sizebox +/− ✅ · typoColor input + typoPaint button (ยังไม่ใช่ split) 
- applyall/reset ✅

### ต้อง PORT เพิ่มจาก mockup (v14)
1. **U (underline) + S (strikethrough)** — markup ใน seg B/I + handlers ผ่าน `_typoWrap('text-decoration',...)`
2. **Color dropdown palette + split-button** — แทน typoColor+typoPaint ด้วย colorpick component:
   - split-button: โซนสี=ทาทันที · caret▾=เปิด palette
   - popup: Swatch grid 40 สี + สีล่าสุด(auto-track localStorage) + HEX input + เพิ่มเติม(native picker) + ปุ่มทาสี
3. **focus-safe mousedown snapshot** — snapshot selection ตอน mousedown ก่อน focus ย้าย (สำหรับ HEX/color controls)
4. **Rename:** "ล้างรูปแบบ"→"ล้างจุดที่เลือก" (title: ล้างรูปแบบเฉพาะจุดที่ไฮไลท์)
5. **ล้างทั้งช่อง = ไม่ confirm** (พึ่ง undo — มี `_snapNow` แล้ว) — ตัดสินแล้ว ไม่ต้องแก้ logic

### การตัดสินใจที่ล็อกแล้ว (user)
- ปุ่มทาสีใน popup: **เก็บไว้** (commit point ของ path พิมพ์ HEX)
- Swatch: **grid เต็ม 40 สี** ชื่อหมวด "Swatch"
- ชื่อปุ่มล้าง: **"ล้างจุดที่เลือก"** + "ล้างทั้งช่อง"
- ล้างทั้งช่อง: **ไม่ confirm** ใช้ undo
- split-button สี: โซนสีคลิกทาทันที + caret เปิด palette (แบบ Excel)

## บทเรียนเทคนิค (session นี้)
1. execCommand เชื่อไม่ได้ข้ามเบราว์เซอร์ → ใช้ Range API (`_typoWrap`)
2. ช่อง text (HEX) แย่ง focus → snapshot ตอน mousedown ก่อน focus ย้าย, ทำงานบน savedRange
3. ปุ่ม/swatch focus-safe ผ่าน mousedown+preventDefault — text input ทำไม่ได้
4. agent มองผล render ไม่ได้ → mockup ทดสอบ runtime แล้ว user เทสต์

## วิธีทำงาน (user กำหนด)
- ไม่เกริ่น "งานใหญ่/ยาก/เสี่ยง" — พูดแล้วทำเลย
- ประกอบใน workspace → verify (depth/unterminated/brace/paren) → copy ขึ้นดิสก์ทีเดียว
- ทุก edit ยึด anchor เต็ม
- ไฟล์ใหญ่: บอกสเต็ป+เวลาตอนเริ่ม · จบด้วย status line

## Backlog (หลัง port เสร็จ)
- Step 2: "ล้างทั้งหน้า" ใน Page tab (panel + confirm + reuse _parsePages)
- ปุ่ม "สีเริ่มต้น (Auto)" — คืนสีดีไซน์เดิม
- A: lint warning `function 'p'` (false positive — nested scope, ไม่ต้องแก้ก็ได้)
- C: ปุ่ม Export log · D: QR Code · E: ลบไฟล์ .bak สะสม

## mockup reference
`C:\OE\typo_partial_mockup.html` (v14) = testbed มาตรฐานใหม่ที่ user เทสต์ผ่านแล้ว — ใช้เป็นแหล่ง port
