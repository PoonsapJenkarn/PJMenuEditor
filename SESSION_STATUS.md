# OE Isan Menu — Session Status

**อัปเดตล่าสุด:** 27 ก.ย. 2026, 16:14 — v74: align selection subsystem กับ mockup (แก้ไฮไลท์ไม่ activate + สีไม่ติด)

## 2 ต.ค. 2026 (18:55) — ยังไม่ commit (ต่อจาก b2603e9)
- แถบปรับราคาเรียง เพิ่ม|ลด · [10] · บาท|% (ผู้ใช้ทดสอบผ่านแล้ว)
- เลือกค่าให้: เฉพาะหน้า = หน้าที่เห็นบนจอมากที่สุดตอนเปิด panel (_priceVisiblePage) · เฉพาะกลุ่ม = กลุ่มของช่องราคาที่ focus ล่าสุดในโหมดปรับราคา ถ้ายังไม่ได้เลือก (_priceFocusGroup) · เลือกแล้วไม่เปลี่ยนเอง · ปุ่มขอบเขตยังไม่ preselect
- ช่องใส่ราคา: เพิ่ม label "ราคา" (.ep-setwrap, pr.priceLbl) ลบ placeholder + key pr.pricePh
- panel ลบหน้า: ลบ placeholder "เช่น 1,3,5-7" → ตัวอย่างอยู่ใน preview (pnl.totalPages → pnl.delPageHint) · ลบ key pnl.delPagePlaceholder · openPanel prompt ไม่รองรับ placeholder แล้ว
- lint_oe.py ข้อ 9: FAIL ถ้าเจอ placeholder= / placeholder: (ทดสอบแล้ว: เวอร์ชันก่อนเจอ 3 จุด, ตอนนี้ 0)
- UI_STANDARD ข้อ 4 (preselect เฉพาะเมื่อระบุได้แน่นอน) + ข้อ 6 (ห้าม placeholder)
- ทดสอบตรรกะ 12 กรณีผ่าน (ยังไม่ทดสอบในเบราว์เซอร์)

## 2 ต.ค. 2026 (18:26) — commit b2603e9 แล้ว
- ตัดสินใจ (18:28): (1) แถบปรับราคาเรียง เพิ่ม|ลด · [10] · บาท|% — แก้แล้ว ยังไม่ commit (2) ใช้ทั้งประเภท ช่องราคาคงจับคู่สีจากข้อความ (เช่น 30-40 → ช่อง 30 ได้สีของ "30" เท่านั้น) — ไม่แก้

## 2 ต.ค. 2026 (18:00) — ✅ commit แล้วใน b2603e9
- ✅ ผู้ใช้ทดสอบแล้ว (18:14): Ctrl+Z ขณะ panel เปิดอยู่ ทำงานปกติ — ปิดรายการค้างนี้
- โหมดปรับราคา (body.pricemode) แยกจาก editmode: ระหว่าง panel ปรับราคาเปิด แก้ได้เฉพาะ .pr · ชื่อเมนู/กลุ่ม/ส่วนหัว/หมายเหตุ/ติดต่อ แก้ไม่ได้ · ไม่มีปุ่มเพิ่ม/ลบ/ทำซ้ำ/ลาก · แถบฟอนต์ไม่ทำงาน · แถบล่าง st.priceMode
- ฟังก์ชันใหม่ _priceModeOn/_priceModeOff/_priceModeExit/_priceModeMark · ลบ _enteredEdit (เดิม openPricePanel เรียก toggleEdit)
- mutual exclusion: toggleEdit/toggleImgMode/editHeader/switchTab → _priceModeExit
- openPanel: เปิดทับ panel เดิม → เรียก onClose ของ panel เดิม (เดิมไม่เรียก → โหมดค้าง) — consumer onClose มีแค่ panel ปรับราคา
- openPanel option ใหม่ noDocEnter: Enter ในช่องเอกสารไม่ยืนยัน panel (เดิมพิมพ์ราคาในช่องแล้ว Enter = ยืนยัน panel)
- _prCell / markDirty / _reapplyEditable (undo) / observer (หน้าใหม่) / save clones รองรับ pricemode · CSS กรอบ+ช่องว่างใช้กับ pricemode
- ทดสอบตรรกะ 11 กรณีผ่าน (ยังไม่ทดสอบในเบราว์เซอร์)

## 2 ต.ค. 2026 (16:25) — ✅ commit แล้วใน b2603e9
- panel ปรับราคา เพิ่มงาน "ใส่ราคา" (bpTask: ปรับราคา default / ใส่ราคา) · ใส่ในช่อง (bpFill: เฉพาะช่องว่าง / แทนที่ทุกช่อง) ไม่เลือกไว้ล่วงหน้า · ช่องราคา .ep-price กรองด้วย _prCleanChars + ตรวจรูปแบบ _PR_VALID (35 หรือ 35-45)
- preview: "ใส่ใหม่ N ช่อง · เขียนทับ M ช่อง (เดิม→ใหม่)" ส่วนเขียนทับสีแดง · ราคาเท่ากันอยู่แล้วไม่นับ · 0 ช่อง = ปุ่มกดไม่ได้ + แจ้งสาเหตุ (pr.setNoEmpty / pr.setNoChange)
- ปุ่มยืนยันเปลี่ยนชื่อตามงาน (ปรับราคา / ใส่ราคา) · ใส่แล้วเปลี่ยนเฉพาะตัวเลข รูปแบบช่องคงเดิม · undo ได้
- ฟังก์ชันใหม่ _bulkSetPlan / _bulkPriceCleanInput · ช่องจำนวนปรับราคาเปลี่ยน selector เป็น .ep-amt
- ทดสอบตรรกะ 12 กรณีผ่าน (ยังไม่ทดสอบในเบราว์เซอร์)

## 2 ต.ค. 2026 (15:40) — ✅ commit แล้วใน b2603e9
- ใช้ทั้งประเภท: ไฮไลท์ทั้งข้อความแล้วจัดรูปแบบ = รูปแบบทั้งช่อง (_typoPromoteFullRun) → คัดลอกไปช่องที่ข้อความต่างกันได้ (เดิม ราคา 35-45 ทาแดงทั้งหมด แล้วช่องอื่นไม่เปลี่ยน)
- ข้อความเมื่อไม่มีช่องเปลี่ยน แจ้งสาเหตุจริง: fl.applyAllNoFmt (ต้นทางไม่มีรูปแบบ) / fl.applyAllNoMatch (รูปแบบบางตัวอักษร ข้อความไม่ตรง) / fl.applyAllNone (เหมือนกันอยู่แล้ว)

## 2 ต.ค. 2026 (14:40) — commit 70e8e9e
- panel ปรับราคา ตรง UI_STANDARD: ขอบเขต เฉพาะกลุ่ม > เฉพาะหน้า (ใหม่ + dropdown หน้า) > ทุกหน้า · ไม่เลือกไว้ล่วงหน้า · dropdown กลุ่มใช้ _typoGroupOptsHtml (ชื่อ · หน้า N, เรียงหน้า>ชื่อ) + "— เลือกกลุ่ม —"
- ปุ่ม "ปรับราคา" กดไม่ได้จนกว่าจะเลือกครบ หรือเมื่อ preview = 0 · validate (_bulkPriceCheck) กัน Enter · ไม่มีอะไรเปลี่ยน = เตือน fl.bulkPriceNone ไม่บันทึก undo
- ฟังก์ชันใหม่ _bulkPriceRead / _bulkPriceCheck ใช้ร่วม preview + readValues + validate
- ช่องราคา รับเฉพาะตัวเลข: 0-9 + '-' 1 ตัว (ช่วงราคา, พิมพ์เป็นตัวแรกไม่ได้) · เลขไทย→อารบิก · Enter ไม่ขึ้นบรรทัด · ตัวอื่นไม่แสดง + เตือน fl.prNumOnly · beforeinput (พิมพ์/วาง/ลาก) + input (กันหลุด) · ทดสอบตรรกะ 12 กรณีผ่าน
- ช่องราคาว่างของแถวใหม่ (newRow) ในโหมดแก้: CSS :empty / :has(> br:only-child) → inline-block min-width 3em ให้เห็นกรอบและคลิกกรอกได้ (เดิมกว้าง 0) · ไม่ใส่ placeholder ตามที่ผู้ใช้ต้องการ
- แก้: dropdown หน้าไม่มีหน้าที่เพิ่มระหว่าง panel เปิดค้าง (สร้างตัวเลือกครั้งเดียวตอนเปิด) → _bulkPriceSync + MutationObserver (_bulkPriceObsStart/Stop) อัปเดตตัวเลือกเมื่อเอกสารเปลี่ยน, จำตัวที่เลือกด้วย element, readValues sync ก่อนปรับราคา
- ไม่ได้ทำ "เลือกกลุ่มของช่องที่คลิกไว้ก่อน" ใน panel นี้: กดแท็บ หน้า = ออกจากโหมดแก้ = ล้างการเลือกเสมอ (switchTab → toggleEdit → typoClear) จึงไม่มีช่องที่เลือกค้าง

## 2 ต.ค. 2026 (13:40) — commit b39417e
- แก้: panel เปิดอยู่ → คลิกข้อความอื่น → toolbar ค้าง disabled. สาเหตุ: _panelOutside ปิด panel ตอน mousedown → #edbar หด → body padding-top ลด → เนื้อหาเลื่อนขึ้น → click ตก element อื่น → typoClear()
  แก้ที่ openPanel กลาง: _panelCloseAfterRelease(seq) ปิดหลัง mouseup/dragend + _panelSeq กันปิด panel ที่เปิดใหม่ + ถอด listener เก่าตอนเปิดทับ — ครอบทุก panel: ใช้ทั้งประเภท, คืนค่า, ลบกลุ่ม, ลบหน้า, ลบหลายหน้า, panel บรรทัด 2221 (ปรับราคาไม่ปิดเมื่อคลิกนอกอยู่แล้ว)
- lint_oe.py ข้อ 8 + UI_STANDARD.md ข้อ 2

## 2 ต.ค. 2026 (13:10) — ยังไม่ commit (ต่อจาก 5cc35c1)
- แก้ปุ่ม typobar สถานะ .on พื้นไม่เขียว/ตัวอักษรขาว: กฎ .on เดิม (#typobar .tbtn.on) แพ้ .applyall/.reset/.clearsel/.clearfield/:hover → เปลี่ยนเป็น #typobar button.tbtn.on (+ :hover + svg) วางหลังสุด, ลบกฎเก่า
- lint_oe.py ข้อ 7: ตรวจกฎ .on ถูก CSS อื่นทับพื้นหลัง → FAIL (ทดสอบแล้ว จับบั๊กเดิมได้ 5 จุด)
- UI_STANDARD.md: เพิ่มกฎ CSS ของ .on

## 2 ต.ค. 2026 (13:00) — ยังไม่ commit (ต่อจาก 5cc35c1)
- เพิ่ม UI_STANDARD.md = มาตรฐาน UI ของทั้งโปรเจกต์ (ใช้ทุกครั้งที่สร้าง element ใหม่)
- openPanel รองรับ activeBtn: ปุ่มที่เปิด panel = .on (เขียว) จนปิด · ใช้กับ ใช้ทั้งประเภท / คืนค่า / ปรับราคา (ย้ายจากโค้ดเฉพาะมาใช้กลไกกลาง) · กดซ้ำ = ปิด
- ขอบเขต: ไม่เลือกค่าเริ่มต้น · ปุ่มยืนยัน disabled จนเลือก · validate กัน Enter (pnl.needScope)
- dropdown กลุ่ม เรียงตามหน้า > ชื่อ (localeCompare numeric) — ผู้ใช้เลือก A
รอผู้ใช้ตัดสินใจ: panel ปรับราคายังเลือก "ทั้งเพจ" ไว้ล่วงหน้า (ต่างจากมาตรฐานข้อ 4)

## 2 ต.ค. 2026 (12:30) — ยังไม่ commit (ต่อจาก 5cc35c1)
- panel คืนค่า: สีเขียวเหมือน panel หลัก (ลบ tone:'warn')
- ลำดับขอบเขต เล็กไปใหญ่ทั้ง 2 panel · ใช้ทั้งประเภท ค่าเริ่มต้น = เฉพาะหน้านี้
- dropdown กลุ่ม: "ชื่อ · หน้า N" + (k) ถ้าชื่อซ้ำในหน้าเดียวกัน · เลือกกลุ่มที่คลิกไว้ก่อน · ซ่อน "เฉพาะกลุ่ม" สำหรับหมายเหตุ/ติดต่อ (_typoGroupOptsHtml)
- กลุ่มใหม่ชื่อ "หมวดใหม่ (N)" · N = เลขสูงสุดในเอกสาร + 1 · ทำสำเนากลุ่มชื่อ หมวดใหม่ (N) ได้เลขใหม่ (_nextNewGroupNo / _renumberDupGroup)
ค้าง: EN ของ "เฉพาะอันนี้"/"เฉพาะหน้านี้" · verify_oe.py · Export log · QR Code · ลบ .bak · ปุ่ม "ล้างรูปแบบ" ซ้ำกับ "คืนค่า"

## 2 ต.ค. 2026 (11:00) — commit ต่อจาก 4daaa53
- panel "คืนค่า": อ่านขอบเขตก่อนปิด panel (readValues) · ล้างสีเฉพาะตัวอักษร + ขีดเส้นใต้/ขีดฆ่า · แจ้งจำนวนช่องที่คืนค่าจริง (fl.resetN / fl.resetNone)
- เพิ่ม typo_partial_mockup.html เข้า git (testbed อ้างอิง)
ค้าง: รัน python verify_oe.py บนเครื่อง → ถ้าผ่านใส่ใน pre-commit hook · Export log (มีแค่ CSS .al-export*) · QR Code (รอ URL) · ลบ .bak 38 ไฟล์ ~212MB · ปุ่ม "ล้างรูปแบบ" ซ้ำกับ "คืนค่า"

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
