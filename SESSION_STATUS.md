# OE Isan Menu — Session Status

**อัปเดตล่าสุด:** 27 ก.ย. 2026, 16:14 — v74: align selection subsystem กับ mockup (แก้ไฮไลท์ไม่ activate + สีไม่ติด)

## 6 ต.ค. 2026 (11:50) — ยังไม่ commit (ต่อจาก bdba991)
- ผู้ใช้พบ: ช่องเลขหน้าพิมพ์ตัวเลขยาวไม่จำกัด (555… → error 5.55e+98) · สั่ง: ช่องกรอกอื่นทำด้วย → work instruction ขยาย: ทุกช่องต้องมีความยาวสูงสุด (UI_STANDARD ข้อ 6, lint ข้อ 17)
- เลขหน้า: _pgCleanChars(v,{maxDig=หลักของจำนวนหน้า,maxLen:50}) · _parsePages ตรวจหน้ามีจริงก่อนวนนับช่วง (1-99999999 เคยทำแท็บค้าง) + แสดงตามที่พิมพ์ · เตือน fl.pagesTooLong / fl.pagesFull
- ราคา: _PR_MAXDIG=5 ต่อเลข (_prCleanChars st.run/after/max) ทั้งช่องในเมนูและ panel · จำนวน: บาท 5 / % 3 (fl.amtTooLong) · เตือน fl.prTooLong
- HEX: _hexClean (# ตัวแรก, 0-9 A-F, 6 หลัก, ตัวใหญ่) · fl.hexOnly / fl.hexOnlyTh
- ข้อความ: _TXT_LIMITS (ชื่อเมนู 60 · ชื่อกลุ่ม 30 · หัวข้อติดต่อ 40 · ชื่อ/เบอร์ 4 บรรทัด×30 · หมายเหตุ 120) · Enter ไม่ได้ยกเว้นชื่อ/เบอร์ (ขึ้นเป็น <br>) · beforeinput + input สำรอง · fl.txtTooLong / txtNoEnter / txtLines
- วาง Ctrl+V ในช่องเมนู = ข้อความล้วน (เดิมสี/ฟอนต์จาก Word ติดมา) · ลากวางที่ยาวเกิน = ไม่รับ
- เตรียมแก้บนสำเนาระหว่างเครื่องออฟไลน์ (5 ต.ค.) แล้วตรวจว่าไฟล์บนเครื่องตรงกับสำเนา (sha256) ก่อนใช้ · ทดสอบตรรกะ 28 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
- ข้อจำกัดที่รู้: วางข้อความหลายบรรทัดในช่องชื่อ/เบอร์ จะต่อเป็นบรรทัดเดียว (ต้องกด Enter เอง)

## 5 ต.ค. 2026 (10:35) — ยังไม่ commit (ต่อจาก bdba991)
- ผู้ใช้ถามทำไมไม่ทำเป็น Word → ตอบแล้ว · ผู้ใช้ยืนยัน: ทำ HTML ต่อ ไม่เปลี่ยน
- บั๊ก: ลบหลายหน้า (deletePagesByRange) ไม่มี _snapNow → Ctrl+Z ย้อนผิดจุด + ไม่ dirty (ปิดแท็บไม่เตือน) · แก้: เติม _snapNow() หลังลบ
- ข้อความยืนยันลบ 3 จุด (pnl.delGroupMsg / delPageMsg / confirmDelMsg) "กู้คืนไม่ได้"/"cannot undo" → "กด Ctrl+Z เพื่อย้อนได้ (ก่อนปิดหรือรีเฟรชหน้า)" / "press Ctrl+Z to undo (before closing or reloading)" · panel ยังสีแดง
- แถบล่างหลังลบ fl.delGroup / delPage / deletedPages เติม " · กด Ctrl+Z เพื่อย้อน" / " · Press Ctrl+Z to undo"
- .gitignore: แก้คำอธิบายที่ผิด ("ไม่เกี่ยวกับโปรเจกต์") → "เก็บนอก git ตามที่ผู้ใช้สั่ง · มีไฟล์เมนู .docx ของร้านอยู่ด้วย" · กฎไม่เปลี่ยน
- ทดสอบตรรกะ 4 กรณีผ่าน (ใช้ _takeSnapshot/_snapNow/undo ตัวจริง) · ยังไม่ทดสอบในเบราว์เซอร์
- (11:00) ผู้ใช้พบ: ปุ่ม ลบหน้า (btnDelPage) ไม่เป็นสีเขียวระหว่าง panel เปิด — ผิด UI_STANDARD ข้อ 2 (ผมตกปุ่มนี้ไป)
  - แก้: activeBtn/toggleBtn ทั้งขั้นกรอกเลขหน้าและขั้นยืนยัน · กดซ้ำ = ปิด panel · CSS #edbar #btnDelPage.on ต่อท้ายกฎเดียวกับ btnBulkPrice (พื้นเขียว/svg ขาว/ตัวอักษรขาว)
  - ตรวจแล้ว: ปุ่มบน ribbon ที่เปิด panel ทั้ง 4 ตัว (ลบหน้า, ปรับราคา, ใช้ทั้งประเภท, คืนค่า) ส่ง activeBtn ครบ · ทดสอบตรรกะ 5 กรณีผ่าน
- (11:15) ผู้ใช้ทดสอบ: ปุ่ม ลบหน้า เขียวระหว่าง panel เปิด ✓ · พบ: ช่องเลขหน้าพิมพ์ภาษาไทยได้ ("ถำไพกฟหด")
  - ผู้ใช้สั่ง work instruction: ช่องกรอกทุกช่องรับได้เฉพาะตัวอักษรของข้อมูลนั้น → UI_STANDARD ข้อ 6 + lint ข้อ 16
  - แก้: openPanel option filter/onFiltered (กรองก่อน onInput, คง cursor) · _pgCleanChars (0-9 , - เว้นวรรค · ๐-๙→0-9) · เตือน fl.pagesOnly / fl.pagesOnlyTh (แป้นพิมพ์ภาษาไทย) TH/EN
  - lint ข้อ 16: prompt ต้องมี filter (เวอร์ชันก่อนจับได้ 1) · text input ที่ไม่มีตัวกรอง = warning → ตอนนี้เหลือ typoHex (ช่องรหัสสี) รับตัวอักษรอะไรก็ได้ แค่ขอบแดง — ยังไม่แก้ รอผู้ใช้
  - ทดสอบตรรกะ 9 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์

## 5 ต.ค. 2026 (10:00) — ✅ commit แล้วใน bdba991 (10:12) · ผู้ใช้ทดสอบ Ctrl+P ระหว่างแก้รูป: ไม่มีเส้นประรอบรูป/โลโก้ ✓ · 2 sheets ✓ · ยังไม่แจ้ง: Ctrl+P ระหว่างแก้ข้อความ
- ผู้ใช้ทดสอบ (ก่อนแก้): Ctrl+P ระหว่างแก้รูป มีเส้นประรอบรูป+โลโก้ ✗ · Save Menu ไม่มีเส้นประ ✓
- Save Menu ปลอดภัยอยู่แล้ว: ปุ่มอยู่แท็บ ไฟล์ และ switchTab ออกจากทุกโหมดก่อน → ไม่แก้ buildMenuHtml
- แก้พิมพ์: ครอบกฎหน้าตาโหมดแก้ 13 กฎ (imgmode/editmode/headermode/pricemode: เส้นประ พื้นสีฟ้า padding กรอบเลือก) ด้วย @media screen{} — ตรวจแล้ว: เอาตัวครอบออก = ไฟล์เดิมทุกตัวอักษร, JS ไม่เปลี่ยน, ลำดับ cascade เดิม
- lint ข้อ 15 + UI_STANDARD ข้อ 7 · ยังไม่ทดสอบในเบราว์เซอร์

## 5 ต.ค. 2026 (09:30) — ✅ commit แล้วใน a3ef302 (09:48)
- พิมพ์: แถบขาวด้านบน + 4 แผ่นแทน 2 · สาเหตุยืนยันจากโค้ด: syncBarHeight ใส่ body.style.paddingTop/Bottom แบบ inline ชนะ @media print{body{padding-top:0}} ที่ไม่มี !important (ประมาณ 41mm บน + แถบล่าง → หน้า 1 ล้นไปแผ่น 2, หน้า 2 ล้นไปแผ่น 4)
  - แก้: เติม !important (CSS บรรทัด 263) · ไม่แตะ JS · lint ข้อ 14 (เวอร์ชันก่อน FAIL ตอนนี้ OK) · UI_STANDARD ข้อ 7
  - ผู้ใช้เลือกไม่แก้ .page:last-child (ไม่ทำงานเพราะมี <script> ต่อท้าย แต่ไม่ใช่สาเหตุ 4 แผ่น)
- ข้อความแถบล่าง: fl.imgHidden "✓ ซ่อนรูป {n} รูปแล้ว (…)" / "✓ {n} images hidden (…)" · fl.imgShown "✓ แสดงรูป {n} รูปแล้ว" / "✓ {n} images shown"
- (09:43) ผู้ใช้ทดสอบพิมพ์: Ctrl+P ขึ้น "2 sheets of paper" ✓ (เดิม 4) · หน้า 1 และ 2 โลโก้ชิดบน ไม่มีแถบขาว ✓ · ยกเลิกแล้วแถบเครื่องมือบนจอไม่ทับเมนู ✓ · ยังไม่เห็น: ข้อความซ่อน/แสดงรูปแบบใหม่
- ผู้ใช้บอกว่าขั้นตอนทดสอบที่ให้ไปเข้าใจยาก → ต่อไปเขียนขั้นตอนทดสอบให้สั้น เป็นการกดทีละปุ่ม + สิ่งที่ต้องเห็น

## 5 ต.ค. 2026 (08:55) — .gitignore ครอบคลุมไฟล์ MS Office ทุกชนิด ✅ commit 655d119
- (08:52) ผู้ใช้เลือก ignore *.pdf + OEIsanHotpotMenu_items.txt (ไฟล์อยู่บนดิสก์เหมือนเดิม) · ยังไม่ commit
- ตรวจแล้ว: ใน git ไม่มีไฟล์ Office ถูก track อยู่ (index 15 ไฟล์ ไม่มี .doc/.xls/.ppt ฯลฯ) · บนดิสก์มี .docx 11 ไฟล์ + ไฟล์ล็อก ~$ 2 ไฟล์ — ถูก ignore อยู่แล้ว ไม่เคยเข้า commit
- ขยาย .gitignore จาก Word/Excel 5 แบบ → Word/Excel/PowerPoint/Visio/Access/Publisher/OneNote/Outlook (ไฟล์ HTML/MD/PY/PNG/SVG ที่ track อยู่ไม่โดนกฎใหม่)

## 5 ต.ค. 2026 (08:45) — ✅ commit แล้วใน d6e92b2 (08:48) · ผู้ใช้ทดสอบในเบราว์เซอร์ผ่าน: แก้รูป→ซ่อนรูป ออกจากแก้รูป รูปหาย เขียวปุ่มเดียว · ซ่อนรูป→แก้รูป รูปกลับ เขียวปุ่มเดียว · ทั้ง TH และ EN · ยังไม่แจ้ง: ซ่อนรูปแล้วแก้ข้อความ
- บั๊กที่ผู้ใช้พบ: แก้รูป → ซ่อนรูป = รูปหายระหว่างแก้รูป + ปุ่มเขียวทั้งคู่ (ซ่อนรูป → แก้รูป ถูกอยู่แล้ว) · ผม (agent) ตกกรณีนี้ทั้งสเปกและชุดทดสอบ
- ผู้ใช้เลือก A "กดปุ่มไหนหลังสุด ใช้ปุ่มนั้น": toggleImgHide ซ่อนตอน imgmode → toggleImgMode() ออกก่อน แล้วซ่อน · แถบล่างหลังสุด = ผลซ่อนรูป
- ทดสอบตรรกะ 5 กรณีผ่าน (ใช้ toggleImgMode จริง) · UI_STANDARD ข้อ 7 เพิ่มกฎกลับกัน
- ผู้ใช้ทดสอบเปลี่ยนภาษาปุ่มซ่อนรูป TH/EN ผ่าน
- รอตัดสินใจ: ข้อความแถบล่าง fl.imgHidden/fl.imgShown ให้เป็น "✓ …แล้ว" / "✓ 12 images hidden/shown" เหมือนข้อความผลอื่น (ยังไม่แก้)

## 5 ต.ค. 2026 (08:30) — commit f3d8c3c แล้ว
- ผู้ใช้ทดสอบซ่อนรูป: ปุ่มอยู่กลุ่ม มุมมอง ✓ · ซ่อนแล้วโลโก้อยู่ ข้อความไม่ขยับ ✓ · Ctrl+P มีรูปครบ ✓ · ยังไม่แจ้ง: แก้รูปแล้วรูปกลับ / ซ่อนแล้วแก้ข้อความ / EN
- ตอน commit git รัน gc อัตโนมัติ (pack objects + cruft) — ปกติ ไม่มีข้อมูลหาย
- รอตัดสินใจ: Ctrl+P หน้าแรกมีแถบขาวด้านบน + ขึ้น 4 sheets (เมนู 2 หน้า) — สงสัย body.style.paddingTop (inline) ชนะ @media print{body{padding-top:0}} ที่ไม่มี !important · ยังไม่ยืนยัน

## 4 ต.ค. 2026 (21:05) — ✅ commit แล้วใน f3d8c3c (5 ต.ค. 08:26)
- ปุ่ม "ซ่อนรูป" (id=btnImgHide) แท็บ รูป กลุ่มใหม่ "มุมมอง" ต่อจาก จัดการรูป (นอก #imgbar → กดได้โดยไม่ต้องเข้าแก้รูป) · ลำดับปุ่ม จัดการรูป เดิมไม่เปลี่ยน
  - ซ่อนเฉพาะ .page .fimg (12 รูป รวมรูปหัวเมนู hdr) · โลโก้ .logo ไม่ซ่อน · ผู้ใช้เลือก: เฉพาะจอ / เฉพาะรูปอาหาร / ในแท็บรูป
  - body.imghidden + @media screen visibility:hidden · ไม่ markDirty ไม่มี undo · buildEditorHtml/buildMenuHtml เอา class ออก + รีเซ็ตปุ่ม
  - .on เขียวตอนซ่อน · tooltip สลับ ttl.imgHide/ttl.imgShow · แถบล่าง fl.imgHidden/fl.imgShown (tk) · ไม่มีรูป+ไม่ซ่อน = ปุ่มปิด · ซ่อนอยู่ = กดได้เสมอ
  - toggleImgMode เข้าโหมด → _imgHideOff · _imgHideSync ใน toggleImgMode/switchTab/_restorePages/โหลดหน้า
  - ทดสอบตรรกะ 8 กรณีผ่าน · (21:13) ผู้ใช้ทดสอบในเบราว์เซอร์: ปุ่มอยู่กลุ่ม มุมมอง ✓ · กดแล้วรูปอาหาร+รูปหม้อหัวเมนูหาย โลโก้อยู่ ข้อความไม่ขยับ ปุ่มเขียว ✓ · รอทดสอบ: Ctrl+P มีรูป / แก้รูปแล้วรูปกลับ / ซ่อนแล้วแก้ข้อความ / EN
- พบ (ยังไม่แก้): buildMenuHtml (ดาวน์โหลดเมนู) ไม่เอา imgmode/headermode ออกจาก body → ดาวน์โหลดตอนอยู่ในโหมดแก้รูป อาจติดเส้นประรอบรูปในไฟล์เมนู — ต้องตรวจ CSS ก่อน

## 4 ต.ค. 2026 (19:20) — commit 0873482 แล้ว
- ผู้ใช้ทดสอบ (5 รูป): แถบล่าง Price mode EN ✓ · ผลปรับราคา TH→EN "✓ Increased +6 Baht · 7 items" ✓ · preview "7 items · 16→22" ✓ · ตำแหน่งรูป รูป 12 → Image 12 ✓ · ปุ่ม Adjust / Choose a scope first ✓
- พบจากรูป (ยังไม่แก้): dropdown กลุ่ม/หน้าใน panel ยังเป็น "· หน้า 1" ตอน EN — ตัวเลือก (sc.grpOpt / sc.pageOpt) สร้างตอนเปิด panel ไม่ถูกสร้างใหม่ตอนเปลี่ยนภาษา (ชื่อกลุ่มเป็นเนื้อหาเมนู ไม่แปล)
- (19:25) แก้ dropdown เปลี่ยนภาษา: openPanel option ใหม่ onRelang (เรียกใน _panelRelang ก่อน onCustom) · ใช้ทั้งประเภท/คืนค่า = _typoGroupSelRelang (สร้างตัวเลือกใหม่ คง value = index .sec) · ปรับราคา = _bulkPriceSync (คงค่าตาม element) · UI_STANDARD ข้อ 6 · ทดสอบตรรกะ 7 กรณีผ่าน (รอบแรก fail 4 เพราะตัวจำลอง select ไม่ถอด &amp; — ไม่ใช่โค้ด) · ไม่มี lint ตรวจข้อนี้ · ✅ commit 57b0f02 (20:24)
  - (19:26) ผู้ใช้ทดสอบในเบราว์เซอร์: ปรับราคา EN → dropdown "ข้าว & เส้น · Page 1" ✓ · แถบล่าง "Price mode · Only price cells can be edited" ✓ · preview "Enter amount to adjust" ✓ · ยังไม่เห็นผล One page / ใช้ทั้งประเภท / คืนค่า
  - (19:43) ตัดสินใจ: แถบล่าง = โหมด/ผลการทำงานเท่านั้น · เลือกกลุ่ม/หน้าใน dropdown อัปเดตเฉพาะ preview ใน panel ไม่เขียนแถบล่าง (กันทับผลลัพธ์ + ไม่ซ้ำ preview)

## 3 ต.ค. 2026 (10:35) — ✅ commit แล้วใน bf88ba2 (i18n 42 key + panel แปลใหม่ตอนเปลี่ยนภาษา) · ส่วน (22:40) แถบล่างเปลี่ยนภาษา ✅ commit แล้วใน 0873482
- ป้าย "รวมช่องว่าง" ถูกตัดตอนหน้าต่างแคบ: .ep-adjwrap เพิ่ม flex-wrap:wrap
- label panel ลบหน้า: "ลบหน้า:" → "ลบหน้า" / "Delete pages:" → "Delete pages"
- i18n sweep: เพิ่ม 42 key (TH/EN ครบ 214/214, ตัวแปร {x} ตรงกันทุก key)
  - HTML: tooltip/ข้อความ ตัวเลือกสี, ปุ่มขนาด, ขีดล่าง/ขีดกลาง, แบบเส้น จุด/ขีด/ทึบ, ตั้งค่าเริ่มต้น, ล้างรูปแบบจุดที่เลือก, ล้างรูปแบบ, คำแนะนำเลือกไอคอน
  - JS: ปุ่ม เพิ่มรายการ/เพิ่มกลุ่ม/ลบหน้านี้ (data-i18n → เปลี่ยนตามภาษาทันที), คำเตือนล้นหน้า, ข้อความแถบล่างเครื่องมือฟอนต์/สี 12 จุด, ใส่รูปทุกหน้า, ชื่อกลุ่มสำรอง, เฉพาะหน้านี้/เฉพาะอันนี้, ตั้งค่าเริ่มต้น (ใช้ _typoLabel แทน .label ภาษาไทย)
  - _statusMode เริ่มที่ msg:null → clearStatus ใช้ t('st.ready')
  - ไทยที่เหลือ 21 จุด ตั้งใจไม่แปล: เนื้อหาเมนู, branch ที่ไม่ทำงาน (btnEditLabel/btnImgLabel มีอยู่), ค่าสำรอง TYPO_TYPES.label และ t()||..., เลขไทย, สถานะเริ่มต้นในไฟล์ที่บันทึก
- UI_STANDARD ข้อ 6: ทุกข้อความ UI ต้องผ่าน t()/data-i18n
- ทดสอบ: แทนค่าตัวแปร TH/EN 16 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
- (10:50) ผู้ใช้รายงาน: เปิด panel ปรับราคาตอน TH แล้วกด EN → preview "เลือกขอบเขตก่อน" + ปุ่ม "ปรับราคา" ยังเป็นไทย (key EN มีครบ — ข้อความที่ JS ใส่ไม่ถูกแปลใหม่)
  - openPanel รับ okKey/cancelKey/msgKey+msgArgs/labelKey · _panelRelang (ตั้งตอนเปิด ล้างตอนปิด) แปลปุ่ม/label/msg + เรียก onInput/onCustom + แปล error จาก validate · applyLang เรียก _panelRelang
  - แปลง caller 8 จุด (ลบกลุ่ม, ลบหน้า, ใช้ทั้งประเภท, คืนค่า, ปรับราคา, ลบหลายหน้า + ยืนยัน) เป็น key · okText/msg สำเร็จรูปยังรองรับ
  - lint ข้อ 12: ห้าม okText/cancelText/msg/label : t(  (เวอร์ชันก่อนจับได้ 18 จุด ตอนนี้ 0) · ทดสอบตรรกะ 11 กรณีผ่าน
- (22:40) แถบล่างเปลี่ยนภาษาตาม: tk(key,args)/tkj(parts)/tt(m) (String object จำ key) · _renderStatus จำ _statusShown + แสดง _ttStr(msg) · applyLang แปลข้อความที่แสดงอยู่ใหม่ · clearStatus ใช้ tk('st.ready')
  - แปลงทุกจุดที่เขียนแถบล่าง: t( → tk( 60 จุดใน 54 call · ต่อข้อความ (hdr.mode, img.mode, ตำแหน่งรูป) → tkj · _typoLabel / t_needSel / _bulkAdjReason คืน tk · หน่วย "บาท" ใน args เป็น tk
  - lint ข้อ 13: ห้าม t( ในอาร์กิวเมนต์ของ setStatus/flashStatus/_renderStatus (เวอร์ชันก่อนจับได้ 55 · ตอนนี้ 0) · UI_STANDARD ข้อ 6 · ทดสอบตรรกะ 8 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
  - ข้อจำกัด: บันทึกกิจกรรมเก็บข้อความภาษาตอนที่เกิด (ประวัติ — ไม่แปลย้อนหลัง) · คำ "Width/Height/mm" ในตำแหน่งรูปเป็นภาษาอังกฤษตายตัวอยู่เดิม
  - ค้าง: ข้อความยืนยันลบกลุ่ม/ลบหน้าบอก "กู้คืนไม่ได้" แต่กด Ctrl+Z ย้อนได้ — ต้องตรวจก่อน

## 3 ต.ค. 2026 (09:36) — commit 2a8efb1 แล้ว
- ผู้ใช้ทดสอบหน้าต่างแคบ (รูป 3 รูป): ribbon แท็บ ข้อความ กลุ่ม จัดรูปแบบ ลงบรรทัด 2 ในแถบ หน้าเมนูถูกดันลง ✓ · panel ปรับราคา/ใส่ราคา ลงบรรทัด 2 ทั้งชุด ป้ายอยู่กับตัวเลือก ✓ · หน้า 3 ถูกเลือกให้ ✓ · ข้อความเหตุผล "ทุกช่องเป็นราคานี้อยู่แล้ว" + ปุ่มปิด ✓
- ค้าง (ผู้ใช้ให้เก็บทีหลัง): C2 cursor ไม่ไปช่องราคาหลังกด [ใส่ราคา] — แก้ครั้งที่ 1 (mousedown preventDefault + setTimeout focus) ไม่ได้ผล · ต้องได้ document.activeElement จากผู้ใช้ก่อนแก้ต่อ
- (09:50) แก้แถบล่างโดนทับตอน resize: checkOverflow(opts) · resize listener เรียก checkOverflow({quiet:true}) = ไม่แตะแถบล่าง เว้นแต่ล้น/หายล้นเปลี่ยน · ผู้เรียกอื่น 28 จุด (แก้เอกสาร) ไม่เปลี่ยน — ยังคืนข้อความโหมด เพื่อไม่ให้ผลเก่าค้างหลังแก้ใหม่ · ทดสอบตรรกะ 7 กรณีผ่าน · UI_STANDARD ข้อ 7 · ✅ commit e670b84
  - (09:51) รูปผู้ใช้: หลังย่อหน้าต่าง แถบล่างกลายเป็นข้อความโหมด — โค้ดใหม่ทำแบบนี้ไม่ได้ที่ความกว้าง >720px (.page 210mm ตายตัว ไม่ล้น/หายล้น) · รอผู้ใช้ตรวจ checkOverflow.length ใน Console (1=โค้ดใหม่, 0=โค้ดเก่า) ก่อนหาสาเหตุต่อ
  - (10:05) ผู้ใช้ตรวจ checkOverflow.length = 1 (โค้ดใหม่) → สาเหตุ: @media (max-width:720px) ทำหน้าเมนู 1 คอลัมน์ → checkOverflow เตือนล้นปลอม → ขยายกลับ หายล้น → clearStatus ทับผลลัพธ์
  - แก้: CSS body.measuring .page{width:210mm;padding:12mm 12mm 8mm} + body.measuring .grid{flex-direction:row} (!important) = วัดแบบ A4 เสมอ · ไม่แตะ JS · หน้าจอแคบยังแสดง 1 คอลัมน์ · พิมพ์/บันทึกไม่กระทบ
  - lint_oe.py ข้อ 11: selector ใน @media width ต้องมีคู่ body.measuring (เวอร์ชันก่อนจับได้ .page .grid · ตอนนี้ 0) · UI_STANDARD ข้อ 7 · ✅ commit 3a861d0
  - (10:13) ผู้ใช้ทดสอบผ่านครบ 5 ข้อ: ผลลัพธ์แถบล่างอยู่รอดทั้งตอนย่อจน 1 คอลัมน์และขยายกลับ · ล้นจริงยังเตือน (กรอบส้ม + แถบเหลือง) · Ctrl+Z แล้วคำเตือนหาย
  - พบจากรูปหน้าต่าง ~500px: ป้าย "รวมช่องว่าง (นับเป็น 0)" ถูกตัดที่ขอบขวา panel (.ep-adjwrap inline-flex ไม่มี flex-wrap + .ep-chk nowrap) — ยังไม่แก้ รอผู้ใช้ตัดสิน

## 3 ต.ค. 2026 (03:10) — ✅ commit แล้วใน 2a8efb1
- ผู้ใช้รายงาน: ปรับราคาในกลุ่มที่ช่องราคาว่างทั้งหมด → ปุ่มกดไม่ได้ แต่ขึ้นแค่ "0 รายการ" ไม่บอกเหตุผล
- ตัดสินใจ: ช่องว่างไม่นับเป็น 0 (ข้าม) + บอกเหตุผลจริง · ว่างทั้งหมด = ปุ่ม "ใส่ราคา" ใน preview สลับเป็นงานใส่ราคา + เฉพาะช่องว่าง คงขอบเขต + focus ช่องราคา
- ฟังก์ชันใหม่ _bulkAdjPlan (เปลี่ยน/ว่าง/ไม่ใช่ตัวเลข/ได้ราคาเดิม) ใช้ทั้ง preview และ exec · _bulkAdjReason · _bulkPriceGoSet · CSS .ep-goset
- preview: "N รายการ · 30→36 · ข้ามช่องว่าง 2 ช่อง" · ไม่มีรายการ / ว่างทั้งหมด / ได้ราคาเดิม / ไม่ใช่ตัวเลข มีข้อความเฉพาะ · งานใส่ราคาขอบเขตว่าง = "ไม่มีรายการในขอบเขตนี้"
- ลบ key fl.bulkPriceNone (แทนด้วยเหตุผลจริง) · เพิ่ม 7 key TH/EN
- UI_STANDARD ข้อ 6: ปุ่มกดไม่ได้ต้องบอกเหตุผลก่อนกด + ช่องว่างไม่ใช่ 0
- ทดสอบตรรกะ 9 กรณีผ่าน (ยังไม่ทดสอบในเบราว์เซอร์)
- (03:20) ผู้ใช้เห็นแถบล่าง "3 รายการ" ค้างจากครั้งก่อน ขณะ preview บอก 2 → แถบล่างเป็นผลครั้งก่อน ไม่ใช่ bug ของ preview
  - fl.bulkPriceUp/Down เป็น "✓ เพิ่มราคา +6 บาทแล้ว · N รายการ" (ให้เหมือน fl.setPrice)
  - _priceEditResetStatus: โหมดปรับราคา แก้ .pr เอง → แถบล่างกลับเป็น st.priceMode (window capture = ก่อนตัวกรองราคา เพื่อให้คำเตือน prNumOnly ยังขึ้นได้)
  - ทดสอบตรรกะ 4 กรณีผ่าน
- (03:35) ตัวเลือก "รวมช่องว่าง (นับเป็น 0)" (checkbox bpIncl) ในงานปรับราคา · ไม่ติ๊กไว้ก่อน · ใช้ได้เฉพาะ เพิ่ม+บาท (ลด/% = ปิด + เอาติ๊กออก + tooltip pr.inclEmptyNA)
  - _bulkAdjPlan แยก adj / filled / empty · preview "2 รายการ · 30→36 · ช่องว่าง 1 ช่อง → 6" (ส่วนช่องว่างตัวหนาแดง)
  - ว่างทั้งหมด + เพิ่มบาท ไม่ติ๊ก → pr.allEmptyTick (บอกให้ติ๊กหรือใส่ราคา) + ปุ่ม [ใส่ราคา] ยังอยู่
  - แถบล่าง: fl.bulkPriceUpFill / เติมอย่างเดียวใช้ fl.setPrice
  - UI_STANDARD ข้อ 6 เพิ่มกฎตัวเลือกรวมช่องว่าง · ทดสอบตรรกะ 12 กรณีผ่าน
- (08:50) ผลทดสอบผู้ใช้: A1–A4, B1–B4, C1, C3, C4, D1, D2 ผ่าน · C2 ไม่ผ่าน (cursor ไม่อยู่ในช่องราคา)
  - แก้ C2: ปุ่ม .ep-goset mousedown preventDefault (ไม่รับ focus ก่อนถูกลบ) + focus ช่องราคาใน setTimeout 0 · ไม่พบโค้ดอื่นที่แย่ง focus — สาเหตุยังไม่ยืนยันในเบราว์เซอร์
- พบจากรูป (ยังไม่แก้ รอผู้ใช้ตัดสิน):
  - ribbon: #edribbon height:82px ตายตัว + .rpane flex-wrap:wrap → กลุ่มที่ตกบรรทัดล้นออกนอกแถบ ทับหน้าเมนู (syncBarHeight วัดได้แค่ 82px)
  - Ctrl+Z ระหว่าง panel ปรับราคาเปิด → dropdown กลุ่มกลับเป็น "— เลือกกลุ่ม —" (_restorePages แทนที่ .page ทั้งหมด → _ref หาย → _bulkPriceSync ถือว่ากลุ่มถูกลบ)
  - resize หน้าต่าง → checkOverflow → clearStatus ทับข้อความผลลัพธ์ในแถบล่าง (อาจเป็นเหตุที่รูป A3 แถบล่างเป็นข้อความโหมด)
- (09:30) ผู้ใช้เลือก A (แถบสูงตามปุ่ม) + แก้ dropdown หลัง Ctrl+Z · ไม่เลือกแก้ "แถบล่างโดนทับตอน resize" (ยังค้าง)
  - CSS: #edribbon height:82px → min-height:82px · .rpane gap:6px 0 · #edpanel flex-wrap:wrap gap:8px 11px · .ep-preview nowrap → normal + flex:1 1 180px · .ep-msg flex:1 1 220px
  - _bpSecKey/_bpSecFromKey: เก็บ ตำแหน่ง+ชื่อ+หน้า ของกลุ่มที่เลือก หาคืนหลัง undo · หน้า: ps._pidx เลขหน้าเดิม · ไม่ตรง = ไม่เลือก
  - lint_oe.py ข้อ 10 (ribbon height ตายตัว / ep-preview,ep-msg nowrap) — ทดสอบแล้ว: เวอร์ชันก่อนจับได้ 2 จุด ตอนนี้ 0
  - UI_STANDARD ข้อ 7 (layout) · ทดสอบตรรกะ dropdown 6 กรณีผ่าน · CSS ยังไม่ได้ดูในเบราว์เซอร์

## 2 ต.ค. 2026 (19:30–21:05) — ✅ commit แล้วใน 40f1419
- ผู้ใช้ทดสอบ 5efc89e ผ่านทั้ง 5 ข้อ
- ช่องจำนวนปรับราคา (.ep-amt): type=number → type=text inputmode=numeric · กรองใน _bulkPriceCleanInput ให้รับเฉพาะจำนวนเต็ม (เลขไทยแปลงให้, ไม่รับ - และ .) · เตือน fl.amtNumOnly · อ่านค่าด้วย parseInt
- เหตุผลจำนวนเต็ม: โหมดบาทเดิมพิมพ์ 2.5 ได้ → ราคา 32.5 ซึ่งช่องราคาเองรับไม่ได้
- ทดสอบตรรกะ 12 กรณีผ่าน (ยังไม่ทดสอบในเบราว์เซอร์)
- (21:05) ช่องจำนวนว่างตอนเปิด panel (เดิม 10) + label "จำนวน" (pr.amtLbl TH/EN) หน้า เพิ่ม|ลด · ว่าง = ปุ่มกดไม่ได้ + "ใส่จำนวนที่ต้องการปรับ" · เพิ่ม/บาท ยัง preselect (เป็นวิธี ไม่ใช่ค่า และ preview แสดงผลก่อนกด)
- ลบ CSS ค้าง #typobar input[type=number] 2 จุด (ไม่มี element ใช้ — ตรวจแล้ว typobar มีแค่ color/text/file)
- ทดสอบตรรกะ 5 กรณีผ่าน (ยังไม่ทดสอบในเบราว์เซอร์)

## 2 ต.ค. 2026 (18:55) — ✅ commit แล้วใน 5efc89e
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
