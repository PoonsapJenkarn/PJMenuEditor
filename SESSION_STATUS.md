# OE Isan Menu — Session Status

**อัปเดตล่าสุด:** 27 ก.ย. 2026, 16:14 — v74: align selection subsystem กับ mockup (แก้ไฮไลท์ไม่ activate + สีไม่ติด)

## ▶ เริ่ม session ใหม่ที่นี่ (ปิด session 9 ต.ค. 2026 11:40)
- งานล่าสุด: ช่อง HEX สีขอบ + หน้าต่างสีขึ้นใต้ปุ่มที่เปิด + "สีมาตรฐาน" + lint #35 — ผู้ใช้ทดสอบผ่าน (11:37) · ✅ commit แล้วใน 4a7174f (11:44) · git สะอาด (ตรวจ 9 ต.ค. 11:51)
- ไฟล์: C:\OE\OEIsanHotpotMenuEditor.html · ไม่ล้น A4 · พิมพ์ 2 แผ่น · ขอบหน้า 8/12/8 mm · เครื่องพิมพ์พิมพ์ไม่ได้ ~2.5 mm ทุกด้าน (เผื่อ 3 mm, lint #34)
- ค้าง (เลือกทำ): กลุ่มใหม่ยังใช้สีเดิม #4a8579 · ออกจากโหมดแก้รูปแล้วข้อความแถบล่างค้าง · ลบรูปอาหารไม่มีผล · เพิ่มรูปไม่ย่อ · หลัง Ctrl+Z แถบรูปแบบอาจชี้ช่องที่ถูกลบ · ไอคอน ⚠ ซ้ำในแถบล่าง · ประวัติถี่เกิน · สีเส้นจุดไม่ทำงาน · typoFont ผูก 2 ครั้ง · B/I/U/S ไม่มีผล · ปุ่ม [ใส่ราคา] ไม่ focus · QR code (รอ URL) · ชื่อเมนูกลับ 17px? (ท้ายหน้า 1 มีที่ว่าง) · จำสีขอบล่าสุดข้าม reload? · ไฟล์ mockup ที่ไม่ได้ track 3 ไฟล์ (ลบหรือเก็บ?)
- verify_oe.py รันผ่านแล้ว 61/61 บนเครื่อง (11 ต.ค. 2026) · ยังไม่อยู่ใน pre-commit hook (ยังไม่ตัดสินใจเอาเข้า)

## 13 ต.ค. 2026 (10:00) — ✅ ปุ่มขยาย/ย่อรูป (imgScale) สร้างจุด Undo · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha 99f3f3d051d56d99 → ad70758f3c77f762
- ผู้ใช้เลือกจาก backlog (decision 09:58): แก้ imgScale ไม่มี Undo (ช่องว่างที่รู้อยู่นานแล้ว)
- บั๊กเดิม: imgScale ไม่เรียก markDirty → กดขยาย/ย่อแล้ว Ctrl+Z ไม่คืน · ลากมุมรีไซส์คืนได้ (mouseup → markDirty บรรทัด 2344)
- แก้ html 1 จุด (imgScale บรรทัด 2220): เพิ่ม cw=parseInt(cs.width) · guard if(nw===cw){_imgReadout;return;} (ชนขอบ 30px ย่อไม่ลง = ไม่สร้าง undo กฎ #6) · ท้ายฟังก์ชันเรียก markDirty() (debounced เหมือน resize-drag · กดรัวรวมเป็น 1 undo)
- เลือก markDirty (debounced) ไม่ใช่ _snapNow (ทันที) เพื่อให้สอดคล้องกับ resize-drag + กดรัวๆ ไม่สร้าง undo หลายจุดเกินจำเป็น
- lint #55 ใหม่ (imgScale ต้องมี markDirty + guard nw===cw) · V0 ผ่าน · ทดสอบบั๊ก 2 แบบจับครบ
- git: layer ต่อจาก commit f330421 (lint #54) · เปลี่ยน 4 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS
- วิธี: workspace menu_work.html + lint_oe_cur.py · copy กลับ sha ตรง ad70758f3c77f762 · device python/sandbox ไม่เสถียร (ใช้ workspace + file_copy)

## 12 ต.ค. 2026 (22:40) — ✅ lint #54 ล็อก pattern กัน XSS (defense-in-depth) · ไม่แก้ HTML · lint ผ่าน · ยังไม่ commit · html คงที่ 99f3f3d (commit 5cbfb2c)
- ผู้ใช้ถาม security assessment ของ app เมนู (ไม่ใช่งาน AEON) → agent ไล่ตรวจ XSS: innerHTML 27 จุด + sink อื่นทั้งหมด → ไม่พบช่องโหว่ใช้โจมตีได้จริง (โค้ด pattern ถูกต้องอยู่แล้ว)
- ผลตรวจ: (1) ข้อความแถบล่าง _renderStatus ใช้ textContent (บรรทัด 1125) (2) ชื่อกลุ่มใน dropdown _typoGroupOptsHtml ผ่าน epEsc (บรรทัด 2861) (3) dialog ลบกลุ่ม pre-escape epEsc(nm) (บรรทัด 1054) (4) อัปโหลดรูปเช็ก f.type=image/* + data: URL (5) save ใช้ cloneNode→outerHTML · ไม่มี eval/new Function/document.write/javascript:/on*=
- จุดเปราะ (ไม่ใช่บั๊ก): openPanel→_msgT() ลง innerHTML ไม่ escape ในตัว — ปลอดภัยเพราะ caller เดียวที่ส่ง user content (ลบกลุ่ม) pre-escape ไว้ · ถ้ามี caller ใหม่ส่งชื่อเมนู/ไฟล์ดิบ = ช่องโหว่ → lint ล็อกไว้
- แก้ lint_oe.py: เพิ่ม #54 (5 ข้อย่อย ก-จ: epEsc ครบ 4 · _renderStatus textContent · _typoGroupOptsHtml epEsc · delGroup pre-escape · ไม่มี sink อันตราย) · V0 ผ่าน · ทดสอบบั๊ก 6 แบบจับครบ
- แก้ UI_STANDARD.md: เพิ่มหัวข้อ 'ความปลอดภัย (client-side XSS)' อธิบาย pattern + จุดเปราะ _msgT
- git: ไม่แตะ html (คงที่ 99f3f3d = commit 5cbfb2c) · เปลี่ยน 3 ไฟล์: lint_oe.py + UI_STANDARD + SESSION_STATUS · commit แยกเป็นงาน lint/docs ล้วน
- วิธี: workspace lint_oe_cur.py · copy กลับ · ไม่ต้อง copy html (ไม่เปลี่ยน)

## 12 ต.ค. 2026 (19:50) — ✅ แก้บั๊กรูป add ใหม่หายตอนออกโหมด/เปิดไฟล์ (วางกลางหน้า A4 + clamp) · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha d77638f659c74751 → 99f3f3d051d56d99
- ผู้ใช้แจ้งบั๊ก (19:25): add รูปใหม่ → ออก edit mode บางทีรูปหาย (กด edit ยังอยู่) · save ไฟล์ editor .html → เปิดใหม่รูปหาย
- ไล่ตรวจ root cause: imgAdd วาง top=Math.round(prc.height/2-h/2) · prc.height = ความสูง render จริง ซึ่งในโหมดแก้ .page เป็น height:auto;min-height:297mm;overflow:visible (ยืดได้) → prc.height เกิน 297mm → รูปวางใต้เส้น 297mm · ออกโหมด/เปิดไฟล์ .page กลับเป็น height:297mm;overflow:hidden → ส่วนเลย 297mm ถูกตัดหาย
- ยืนยัน NOT ไฟล์เสีย/src หาย: _readImageFile ใช้ readAsDataURL = base64 ฝังในไฟล์ (createObjectURL ใช้แค่ตอน logo swap บรรทัด 1230 ไม่เกี่ยว) · ไม่มี CSS ซ่อน .fimg ทั้งรูปตามโหมด · box-sizing:border-box ทั้งเอกสาร
- แก้ html 1 จุด (บรรทัด top ใน imgAdd): อ้าง A4 คงที่ `_A4px=297*96/25.4` + `_padPx=8*96/25.4` → `_topPx=Math.round(Math.max(_padPx, Math.min(_A4px/2-h/2, _A4px-_padPx-h)))` · clamp กันรูปสูงล้นขอบพิมพ์ · วางกลางหน้าเสมอ (decision ผู้ใช้ 19:46) · left เดิมใช้ prc.width=210mm คงที่ ไม่แตะ
- lint #53 ใหม่ (ห้าม top จาก prc.height · ต้องมี 297*96/25.4 · ต้อง clamp Math.max/Math.min) · V0 ผ่าน · ทดสอบบั๊ก 3 แบบจับครบ · (เงื่อนไข clamp เขียนผิดรอบแรก ternary precedence + split _topPx ตัวท้าย → V0 fail → แก้เป็น Math.max/min in _b53 ตรงๆ)
- git: layer ต่อจาก commit 9bb73d3 (cap+ป้าย+relang) · เปลี่ยน 4 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS
- วิธี: workspace menu_work.html + lint_oe_cur.py · copy กลับ sha ตรง 99f3f3d051d56d99 · device python/sandbox ไม่เสถียร (ใช้ workspace + file_copy)

## 12 ต.ค. 2026 (19:05) — ✅ ป้ายใต้รูปเปลี่ยนภาษาตาม TH/EN · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha f05dc184fc7984b1 → d77638f659c74751
- ผู้ใช้สั่ง (19:04 + ภาพยืนยันป้าย 3 แถวทำงาน): "เอาให้เปลี่ยนภาษาด้วยได้ไหม" — คำ ขนาดต้นฉบับ/ขนาดปัจจุบัน ค้างภาษาเดิมตอนสลับ TH/EN (ป้าย render เฉพาะตอน _imgReadout)
- วิเคราะห์: applyLang ไม่ได้ re-render ป้ายรูปของรูปที่เลือก (แถบล่าง re-render อยู่แล้วที่บรรทัด _statusShown key/parts · ป้าย sizetag คือช่องโหว่)
- แก้ html 1 จุด: applyLang +บรรทัด `if(typeof _imgReadout==='function' && typeof _imgSel!=='undefined' && _imgSel && document.contains(_imgSel)) _imgReadout(_imgSel);` ท้ายฟังก์ชัน · guard: typeof (โหลดแรก var ยังไม่ assign — function hoisted ปลอดภัย) + document.contains (รูปถูกลบหลัง Undo) · imgmode/editmode แยกกัน ไม่ชนเส้นจุด (บรรทัด _typoType.line)
- lint #52 ใหม่ (applyLang ต้องมี _imgReadout(_imgSel) + guard document.contains) · V0 ผ่าน · ทดสอบบั๊ก 2 แบบจับครบ
- git: layer ต่อจากงาน 18:40 (cap 100mm + ป้าย 3 แถว + bake) ที่ยังไม่ commit · เปลี่ยน 3 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS · ⚠ งานนี้รวมกับ 18:40 ควร commit เป็นชุดเดียว (ป้าย 3 แถว + เปลี่ยนภาษา = ฟีเจอร์เดียวกัน)
- วิธี: workspace menu_work.html + lint_oe_cur.py · copy กลับ sha ตรง d77638f659c74751 · device python timeout/sandbox ไม่เสถียร (ใช้ workspace + file_copy)

## 12 ต.ค. 2026 (18:40) — ✅ รูป add ใหม่ cap 100mm + ป้ายใต้รูป 3 แถว (ต้นฉบับ px / ปัจจุบัน mm) + bake baseline ตอน save · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha f05dc184fc7984b1
- ผู้ใช้สั่ง (18:34, 3 ข้อ + decision 18:39): (1) รูป add ใหม่ cap W/H ไม่เกิน 100mm (ผู้ใช้วัดเองว่าเหมาะกับ A4) (2) ป้ายใต้รูปแสดง Original (px) + Current (mm) (3) ปุ่มคืนขนาด = คืนค่าจากที่ save ไฟล์ไปแล้ว
- agent ท้วง 2 จุด (ผู้ใช้เห็นด้วย ทั้ง 2): Current คง mm ไม่ใช่ px (Original=ความละเอียด px / Current=ขนาดพิมพ์ mm คนละมิติ แบบ InDesign Link / Photoshop Image Size — ห้ามรวมหน่วย) · ข้อ 3 เดิมคืนขนาดออกแบบ ไม่ตรงคำ "ที่ save ไปแล้ว" → bake-on-save
- แก้ html 4 จุด: (1) imgAdd: `var w=im.width,h=im.height` +`_CAPpx=100*96/25.4` +`_sc=Math.min(_CAPpx/w,_CAPpx/h,1)` + `w/h=Math.round(*_sc)` (2) sizetag 2→3 แถว (ชื่อ / Original naturalW×H px / Current wmm×hmm mm) (3) buildEditorHtml bake `data-w0/h0=el.style.width/height` ทุก .fimg ตอน save (4) i18n `img.origSize`/`img.curSize` TH+EN
- lint: rewrite #50 (fit-box 120×200 → cap 100mm: ห้าม _HMAX/_WMAX/120*r · ต้องมี 100*96/25.4 · Math.min(...,1) · w/h=Math.round(*_sc) · baseline) + เพิ่ม #51 (sizetag 3 แถว: naturalWidth/Height + t('img.origSize')+t('img.curSize') + px + mm · buildEditorHtml bake · i18n origSize/curSize th+en) · V0 ผ่าน · ทดสอบบั๊ก 8 แบบจับครบ · ไฟล์ 5.37MB
- git: base = งาน add-ขนาดจริง (ไม่มี cap) ที่แก้ตรงเครื่อง 17:02 (ยังไม่ commit) · รอบนี้ layer ทับเป็น cap 100mm · เปลี่ยน 4 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS · ⚠ ตรวจ git log/status ก่อน commit (สถานะ fit-cap 39d855 เดิมยังไม่ยืนยัน)
- วิธี: workspace menu_work.html + lint_oe_cur.py · copy กลับ sha ตรง f05dc184fc7984b1 · device python timeout 65s (ใช้ workspace + file_copy)

## 12 ต.ค. 2026 (15:10) — ✅ ขนาดเริ่มรูปใหม่ = fit ขนาดจริงเข้ากรอบเพดาน คงสัดส่วน · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha d9e622b311a441b2 → 39d855317166b59d (ต่อจาก actual-size commit 1e816ee)
- ผู้ใช้สั่ง (decision 15:05): default ตอนเพิ่มรูป = "ขนาดจริง + cap พอดีเมนู" (ถาม pro/enterprise ใช้เท่าไหร่ → agent ตอบ Word/PPT แทรกขนาดจริงแล้ว fit · ผู้ใช้เลือกแนวนี้)
- แก้ imgAdd: เดิม fixed สูง 120px (w=120*r) → _sc=Math.min(Hmax/im.height, Wmax/im.width, 1) · w=im.width*_sc h=im.height*_sc · Hmax=120px(≈36mm) Wmax=200px(≈60mm) · top ใช้ h/2 (เดิม 60 คงที่) · baseline data-w0/h0 = ขนาดที่ fit
- ผล: รูป ratio≤~1.67 สูง 36mm เท่าเดิมเป๊ะ (ไฟล์ H500 → _sc=0.24) · ratio>1.67 ชนเพดานกว้าง 60mm (เดิมบานเกิน) · รูปเล็กกว่าเพดาน=ขนาดจริง (min 1) · เฉพาะ add ใหม่ · รูปเดิม 6 จุด baseline ไม่กระทบ
- lint ข้อ 50 ใหม่ (ห้าม 120*r · ต้อง im.width/height+Math.min · cap มี 1 ท้าย · baseline=w/h) ทดสอบบั๊ก 4 แบบจับครบ · braces 2473:2473 · ไฟล์ 5.37MB
- git: disk สะอาดที่ 1e816ee ก่อนเริ่ม · งานนี้เป็น commit แยก · เปลี่ยน 3 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS
- วิธี: workspace menu_out12→out13 · lint_oe10→oe11 · copy กลับ sha ตรง 39d855317166b59d · device python ยัง timeout 65s (ใช้ workspace)

## 12 ต.ค. 2026 (14:50) — ✅ ปุ่ม "ขนาดจริง" (ปุ่มที่ 2 คืนขนาด pixel จริงไฟล์) + honest-dim ทั้ง 2 ปุ่ม · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha 0484d6c233181bd4 → d9e622b311a441b2 (ต่อจาก image-refresh commit c09813a)
- ผู้ใช้สั่ง (14:35): ทำ 2 ปุ่ม · ปุ่ม 1 คืนขนาดที่ออกแบบ (มีอยู่แล้ว) · ปุ่ม 2 คืนขนาด original pixel ของไฟล์ · "เตรียมเครื่องมือให้ครบ อย่าบังคับผู้ใช้ว่าต้องขนาดไหน" (agent เคยค้านปุ่ม 2 ว่ารูปล้นหน้า — ผู้ใช้ท้วงว่าเป็นสิทธิ์ผู้ใช้เลือก · agent ยอมรับ)
- แก้: (1) ปุ่ม btnImgActual ต่อจาก btnImgReset ในกลุ่มจัดการรูป (2) imgActualSize: w/h = img.naturalWidth/naturalHeight + markDirty (undo) + guard อ่านไม่ได้ (3) _imgResetSync เขียนใหม่คุม 2 ปุ่ม honest-dim: คืนขนาดจางเมื่อ style===w0/h0 · ขนาดจริงจางเมื่อ style===naturalW/H px (4) i18n: btn.actualSize/ttl.imgActual/ttl.imgActualAt/ttl.imgActualNeed/fl.imgSizeActual/fl.imgSizeAtActual/fl.imgNoNatural TH+EN · ttl.imgReset/imgResetAt ปรับคำ "ขนาดที่ออกแบบไว้"
- lint ข้อ 49 ใหม่ (btnImgActual+imgActualSize naturalWidth+markDirty · _imgResetSync คุม 2 ปุ่ม + honest compare) ทดสอบบั๊ก 4 แบบจับครบ · braces 2473:2473 · ไฟล์ 5.37MB
- git: image-refresh commit แล้ว c09813a (ผู้ใช้ 14:50) · งานปุ่มนี้ลงเครื่องเป็น commit ที่ 2 แยก · เปลี่ยน 3 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS
- วิธี: workspace menu_out11→out12 · lint_oe9→oe10 · copy กลับ sha ตรง d9e622b311a441b2 · device python ยัง timeout 65s (ใช้ workspace)

## 12 ต.ค. 2026 (13:40) — ✅ refresh ไฟล์รูปใหม่ 6 จุด (5 ไฟล์ต้นทาง) ใช้ตำแหน่งเดิม · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha 320e3e26af51356f → 0484d6c233181bd4
- ผู้ใช้สั่ง (13:26–13:36): เปลี่ยน base64 รูปใหม่จาก C:\AmazonQuickTempFiles\OE_ISAN_Image\ImageEdit\ImageSelected\ · header p1+p2 ← HotpotHeader1-H500.png (ผู้ใช้แก้คำสั่งล่าสุด: HotpotHeader2.png ไม่มีในโฟลเดอร์ → ใช้ HotpotHeader1-H500.png) · PlaPaoPaiFai2-H500.png (p1) · Plapao17-H500.png (p1) · Mortar1-H500.png (p2) · Beverage17→Beverage19-Soda-H500.png (p2)
- เหตุผลผู้ใช้: รูปเดิมคืนขนาด (Reset Size) ไม่ได้ → ตั้ง baseline ใหม่สะอาดจากขนาดจริงรูปใหม่
- สัดส่วนรูปใหม่ตรงกรอบเดิมเกือบเป๊ะทุกจุด (ครอป ~0% วัดด้วย PIL) → คงตำแหน่ง+กรอบเดิม (top/left/width/height) · อัปเดต data-ratio (header 2.154, plapaopaifai 3.754, plapao17 2.006, beverage 1.816, mortar 0.856) · data-w0/h0 = กรอบเดิม · data-fname + alt อัปเดตตรงไฟล์จริง (HotpotHeader2→HotpotHeader1-H500, Beverage17→Beverage19-Soda-H500)
- ไฟล์โต 4.35MB→5.37MB (รูปใหม่ base64 ใหญ่กว่า) · ยังเปิด/พิมพ์ออฟไลน์ได้ · braces 2463:2463 · lint PASS 0 warning · ไม่แตะ lint (งาน content) · เปลี่ยน 2 ไฟล์: html + SESSION_STATUS
- วิธี: copy 5 PNG เครื่อง→workspace · PIL วัด ratio · ฝัง base64 ทั้ง 6 .fimg (reverse-index splice) · copy กลับ sha ตรง 0484d6c233181bd4 · device python ยัง timeout 65s (ใช้ workspace)

## 12 ต.ค. 2026 (12:00) — ✅ ปุ่ม "คืนขนาด" รูป (คืนขนาดฐาน) · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha 6b42d031e2d12505 → 320e3e26af51356f (ต่อจากปุ่มเพิ่มรูป commit 02cbe5a)
- ผู้ใช้สั่ง (decision 12:00): รูปที่ยืด/หดไปมา คืนขนาดเดิมได้ · เลือก "ทำปุ่มคืนขนาดเดิม (ถาวร)"
- การวิเคราะห์: รูปไม่เคยเพี้ยนสัดส่วน (imgScale + ลากมุม ล็อก height=width/ratio) · แต่ไม่มี baseline เก็บไว้ → ต้องสร้าง · imgScale (ขยาย/ย่อ) ไม่ได้ markDirty = ช่องว่างเดิม ไม่ใช่งานนี้ (ไม่แตะ)
- แก้: (1) ฝัง data-w0/data-h0 ลงทุก .fimg (6 รูป = ขนาด commit ล่าสุด) (2) ปุ่ม btnImgReset ในกลุ่มจัดการรูปต่อจาก ย่อ (3) imgResetSize: set w/h=dataset.w0/h0 + markDirty (undo กฎ #6) · เท่าเดิม=ไม่นับแก้ · ไม่มี baseline=แจ้งเตือน (4) _imgResetSync wire ใน _imgReadout (enable/disable+tooltip) (5) imgAdd เก็บ baseline รูปใหม่ (w px/120px) (6) i18n btn.resetSize/ttl.imgReset/ttl.imgResetNeed/fl.imgSizeReset/fl.imgSizeSame/fl.imgNoBaseline TH+EN
- data-w0/h0 เก็บทั้ง build* เหมือน data-ratio (ไม่ตัด) · gate ปกติ (ไม่ใช่ imgalways — ทำงานกับรูปที่เลือก) · lint ข้อ 48 ใหม่ (จับใน _imgReadout scope กันชนชื่อ fn) ทดสอบบั๊ก 6 แบบจับครบ
- วิธี: workspace menu_out9→out10 · lint_oe8→oe9 · copy กลับ · device python ยัง timeout 65s

## 12 ต.ค. 2026 (11:18) — ✅ ปุ่ม "เพิ่มรูป" กดได้ตลอด + เข้าโหมดแก้รูปอัตโนมัติ · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha d6b833b6691645b8 → 6b42d031e2d12505 (ต่อจาก A4 commit 31405d3)
- ผู้ใช้สั่ง (ภาพ 12 ต.ค.): "เพิ่มรูป" ควร enabled ตลอดไม่ต้องเข้าโหมดแก้รูปก่อน + เพิ่มรูป+เข้าโหมดพร้อมกัน เหมือน "ซ่อนรูป" · ปุ่มอยู่ที่เดิม (กลุ่มจัดการรูป) แค่เปลี่ยน behavior
- แก้ 3 จุด: (1) ปุ่มเพิ่มรูป +class imgalways (2) gate #imgbar แยกจาก #typobar: dim รายปุ่ม .rgl + .rgb>*:not(.imgalways) ไม่ dim .rgb ทั้งกล่อง + .rgroup pointer-events:none + .imgalways pointer-events:auto (ปุ่มสว่าง+กดได้จริง ไม่หลอกตา) (3) imgAdd: ถ้าไม่ใช่ imgmode → toggleImgMode() หลังอ่านไฟล์สำเร็จ (ยกเลิก/ไฟล์ผิด = ไม่เข้าโหมด)
- #typobar คงเดิมเป๊ะ (gate .rgroup/.rgroup>*) · opacity ไม่แตะ .rgroup (lint ข้อ 25 self-check ผ่าน) · lint ข้อ 47 ใหม่ + ทดสอบบั๊ก 5 แบบจับครบ
- git: A4 commit แล้ว 31405d3 (ผู้ใช้ 11:18) · งานปุ่มนี้ลงเครื่องเป็น commit ที่ 2 แยก
- วิธี: workspace menu_out8→out9 · lint_oe7→oe8 · copy กลับ · device python ยัง timeout 65s

## 11 ต.ค. 2026 (23:55) — ✅ เอาเส้นประ "สิ้นสุด A4" + ข้อความออกจากโหมดแก้ (เหลือลายเฉียง) · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha 90ac96e84d27c666 → d6b833b6691645b8
- ผู้ใช้สั่ง (ภาพที่ 3, 23:55): เส้นประ + ป้าย "สิ้นสุด A4 ส่วนล่างไม่พิมพ์" บัง element แถวล่าง (ทับ "น้ำแข็งใหญ่ 20" + ปุ่มทำซ้ำ/ลบ) แก้ลำบาก · ลายเฉียงโปร่งใสแยกจาก A4 ขาวชัดพอแล้ว
- agent เห็นด้วย (เหตุผล): pasteboard metaphor (InDesign/Word/PPT) ใช้สีพื้นที่ต่างบอกขอบหน้า ไม่มีป้าย — เอาเส้น+ข้อความออกเหลือลายเฉียง = ตรงมาตรฐานขึ้น + ไม่บังงาน
- ลบ: .page::after (เส้นประ+ข้อความ ทุกโหมด editmode/headermode/pricemode/imgmode) · --a4lbl (setProperty applyLang + removeProperty build*×2) · pg.a4end (ตารางภาษา th+en) · คอมเมนต์ CSS อัปเดต
- เก็บ: .page background (ขาว 297mm + ลายเฉียง repeating-linear-gradient 135deg) ไม่แตะ · เป็น screen-only ไม่กระทบพิมพ์
- lint ข้อ 37 เขียนใหม่: ลายเฉียงต้องอยู่ · ห้ามเหลือ ::after boundary/--a4lbl · ทดสอบไฟล์ใส่บั๊ก
- วิธี: workspace menu_out7→out8 · lint + copy กลับ · device python ยัง timeout 65s

## 11 ต.ค. 2026 (23:45) — ✅ กันโน้ต (ราคาตามไซส์) ถูกรื้อตอน "ใช้ทั้งประเภท" · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha 24a09fbf40f6907b → 90ac96e84d27c666
- บั๊กจริง (ผู้ใช้จับได้ภาพ 23:35): _typoClearInner รื้อแท็ก `<i>` เปล่า (เงื่อนไข `if(isType || d.className) return;` + /^(B|I|EM|...)$/ && !attributes.length → unwrap) → โน้ตหลุดกฎ .nm i (สี+ขนาด+เอียง) แล้วรับ format ต้นทางเต็ม (ฟอนต์+ขนาด+สี+style)
- agent ยอมรับ: เคยบอกผิดว่า "เก็บ <i> ไว้ style ไม่หาย" เพราะอ่าน _typoClearInner มาไม่ครบ (output truncated ตรง `if(isType |`) แล้วเดาส่วนที่เหลือ — ผิดหลักห้ามเดา
- โจทย์ผู้ใช้ (3 ข้อ): (1) เปลี่ยนเฉพาะ font → โน้ตเปลี่ยน font ตาม style เดิม (2) ใช้ทั้งประเภท inherit → เปลี่ยน font ตาม style เดิม (3) ไฮไลท์โน้ตตรงๆ → เปลี่ยนตามแก้
- แก้: ใส่ class="note" ให้แท็กโน้ต (className truthy → _typoClearInner ข้าม ไม่รื้อ) · ย้าย .nm i → .nm .note (สี+ขนาด+เอียง ไม่มี font-family → font ยัง inherit จาก cell) · โน้ตกลุ่มเช่นกัน · lint ใหม่กันหลุด
- หมายเหตุ: เอียงใน Prompt ยังต้องโหลด ital axis แยก (คนละเรื่อง ค้างไว้) · ตัว strip ครบ build* ต้องเช็ก class="note" ไม่หลุดลงไฟล์เมนู (ปกติ textContent คงอยู่)
- วิธี: workspace menu_out6→out7 · lint + copy กลับ · device python ยัง timeout 65s

## 11 ต.ค. 2026 (21:30) — ✅ ยุบ function p ซ้ำ 2 ตัว → pad2 กลางตัวเดียว (warning function 'p' หายแล้ว) · lint ผ่านสะอาด 0 warning · ยังไม่ commit · html sha 3a4115cea9ca8618 → 24a09fbf40f6907b
- ผู้ใช้เลือก (decision 21:29): ทาง ก — ยุบเป็น pad2 (แก้ที่ต้นเหตุ ไม่ทิ้งขยะ) · warning เป็น false positive (p nested คนละ scope ใน tsStamp/_fmtTs โค้ดเหมือนกันเป๊ะ)
- ทำ: เพิ่ม function pad2(n){return (n<10?'0':'')+n;} กลาง 1 ตัวก่อน tsStamp · ลบ function p ใน tsStamp + _fmtTs · เปลี่ยน p(→pad2( เฉพาะใน 2 ฟังก์ชันนั้น (replace ทั้งก้อน ไม่ global)
- วิธี: workspace menu_out5→out6 · lint ยืนยัน warning หาย · copy กลับ · device python ยัง timeout 65s

## 11 ต.ค. 2026 (14:16) — ✅ ลบ dead CSS 7 ตัว + แก้ verify ไม่ให้เตือน al-* · lint ผ่าน · ยังไม่ commit · html sha 5f0dc3b39dc95280 → 3a4115cea9ca8618
- ผู้ใช้เลือก (decision 14:16): ลบ dead CSS 7 (footer, imgstatus, jaew, pmeta, tinfo, tlabel, who) + แก้ verify section 7 allowlist al- (al-error/al-warning สร้างแบบ 'al-'+e.type ใน log — false positive ลบไม่ได้)
- ก่อนลบ: ตรวจทุก occurrence ของ 7 class ใน <style> ว่าเป็น standalone rule ไม่ใช่ selector-list ร่วมกับ class ที่ใช้งาน (footer เจอ selector 3×, imgstatus 2× — ต้องดูทุกจุด)
- วิธี: ทำบน workspace (menu_out4→out5 · verify) แล้ว copy กลับ · lint + verify static ยืนยัน · device python ยัง timeout 65s
- ผล: ลบ 10 rule (footer×3, imgstatus×2, jaew, pmeta, tinfo, tlabel, who) −964 ไบต์ · al- ครบ (al-row, 'al-'+e.type, .al-error/.al-warning) · braces 2453:2453 · lint PASS · verify section 7 เพิ่ม _DYN_CLS=("al-",) ทดสอบ 3 เคสผ่าน (ไม่เตือน CSS ใหม่ · ยังจับ dead จริง · al-ghost ไม่เตือน)

## 11 ต.ค. 2026 (13:06) — ✅ เก็บงานบ้าน B ชุดปลอดภัย (ซ่อม verify_oe.py + ลบ _wtest.txt + gitignore mockup) · ยังไม่ commit
- ออดิตพบ (จากไฟล์จริง commit 07469bd): verify_oe.py REQUIRED_FUNCS ยังมี typoColorApply ที่ถูกลบไปแล้ว (lint #40 ย้ายไป applyColorRange) → verify จะ FAIL ทันทีถ้ารัน · เช็กครบ 34 ตัว ขาดแค่ตัวนี้ตัวเดียว
- ทำ: (1) verify_oe.py เปลี่ยน "typoColorApply" → "applyColorRange" ในลิสต์ (applyColorRange มีจริง def 1 ครั้ง) (2) ลบ _wtest.txt (ไฟล์ขยะ "ok3" จากทดสอบ write channel · untracked) (3) .gitignore เพิ่ม *_mockup.html (4 ไฟล์ mockup)
- ยังไม่ตัดสินใจเอา verify เข้า pre-commit hook — รอผู้ใช้รัน verify เองก่อน (ต้องมี Chrome + subprocess ที่ agent รันไม่ได้) · hook ปัจจุบันเป็น lint อย่างเดียว คงไว้
- mockup อาจ track อยู่แล้ว → .gitignore ไม่ถอด ต้อง git rm --cached (ยืนยันด้วย git status)

## 11 ต.ค. 2026 (11:56) — ✅ focus ช่องกรอกเมื่อ selector ครบ (ทั้ง 2 โหมด) · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha 7026d28c3edd1a73 → 5f0dc3b39dc95280
- ผู้ใช้สั่ง (11:38/11:56): เข้าโหมดปรับราคา → เช็ก 5 กลุ่ม (งาน·ขอบเขต·dropdown·เพิ่ม/ลด·บาท/%) ครบแล้ว/เลือกใหม่ครบแล้ว → focus ช่องกรอก
- ตีความ (ยืนยันกับผู้ใช้ 11:51): "ช่องใส่ราคา" = ช่องของโหมดนั้น · ปรับราคา→.ep-amt (จำนวน) · ใส่ราคา→.ep-price (ราคา) · กลุ่ม 4,5 มี default (เพิ่ม/บาท) = ครบเสมอ → ในทางปฏิบัติ "ครบ" = ขอบเขต + dropdown(ถ้ากลุ่ม/หน้า)
- แก้: _bulkPricePreview เปลี่ยนจาก _wasSet/_wasFill (เฉพาะ set mode) → _selDone (scope+gidx/pidx ครบ) แล้ว focus ช่องของโหมด (isSet?.ep-price:.ep-amt) ทุก preview ที่ครบ · setTimeout 0 + document.contains · ลบ _wasSet/_wasFill ทิ้ง (ไม่ทิ้งขยะ)
- เหตุผลเกณฑ์ "ครบ": เฉพาะกลุ่มยังไม่เลือกกลุ่ม = ไม่ครบ → ไม่ focus → ไม่แย่ง dropdown · เลือกกลุ่มเสร็จ = ครบ → focus · set mode ไม่บังคับ fill (คงพฤติกรรมที่ผู้ใช้ทดสอบผ่าน 9:23)
- lint ข้อ 45 เขียนใหม่ (selector-complete) + ทดสอบไฟล์ใส่บั๊ก · ทำบน workspace แล้ว copy กลับ (device python ยัง timeout 65s · on-device write ยังล่ม)

## 11 ต.ค. 2026 (00:30) — ✅ โฟกัสช่องราคาอัตโนมัติเมื่อกดแท็บ "ใส่ราคา" + เลือก "ใส่ในช่อง" · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha 2d71ebe8b43ea919 → 7026d28c3edd1a73
- ผู้ใช้ยืนยัน (ภาพ 2 รูป 00:17): ทางที่ใช้จริง = กดแท็บ "ใส่ราคา" → เลือก "เฉพาะช่องว่าง/แทนที่ทุกช่อง" → ช่องราคาโผล่ แต่ไม่มีเคอร์เซอร์
- สาเหตุ: .focus() มีจุดเดียวในปุ่ม preview (_bulkPriceGoSet) ซึ่งเป็นมุมหายาก · แท็บ "ใส่ราคา" (ทางหลัก) ไม่มีโฟกัส · และการคลิก "ใส่ในช่อง" ยังแย่งโฟกัสไป radio
- แก้: _bulkPricePreview โฟกัส .ep-price เมื่อ "เพิ่งสลับมาใส่ราคา" (p._wasSet) หรือ "เพิ่งเปลี่ยนใส่ในช่อง" (p._wasFill) เท่านั้น — ไม่แย่งโฟกัสตอนพิมพ์ · setTimeout 0 + document.contains guard
- lint ข้อ 45 ใหม่ + ทดสอบไฟล์ใส่บั๊ก · ทำบน workspace แล้ว copy กลับ (device python sandbox ยัง timeout 65s · on-device write ยังล่ม)

## 10 ต.ค. 2026 (22:10) — ✅ ย้ายเมนู "ยำหมูยอ + กุ้งลวก" ต่อท้าย "ยำหมูยอ" + migration ข้อความเส้นจุดเข้าตารางภาษา · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha ก่อนแก้ 2f0e7cb14c7a554f → หลัง 2d71ebe8b43ea919
- (A) ย้ายแถว: ผู้ใช้สั่ง (decision 21:50) ตามข้อความ = ยำหมูยอ(70) → ยำหมูยอ+กุ้งลวก(100) → ยำปลาหมึก(80) · ลำดับเดิมหลังยำทะเลรวมหายเรียบร้อย · string replace (ตัด ROW แทรกหลัง ANCHOR) ขนาดไฟล์เท่าเดิม
- (B) migration ln.hint: ไฟล์บนดิสก์ (2f0e7cb1) ไม่ตรง commit 7f6e661 — งานค้าง: ตารางภาษาเพิ่ม key ln.hint แล้ว แต่ --lnhint เก่า (setProperty applyLang + removeProperty build*×2) กลายเป็น dead (::after ที่เคยใช้ถูกลบไปแล้ว) · ผู้ใช้เลือก (decision 22:06) "ทำ migration ให้จบ"
- ทำ: _lnSelMsg อ่าน t('ln.hint') (แหล่งเดียว) · ลบ --lnhint 3 จุด · อัปเดตคำในตารางให้ตรงที่อนุมัติ: TH 'เปลี่ยนสีและแบบเส้นได้เท่านั้น' / EN 'Change color and line style only' (ตารางค้างคำเก่าไม่มี "เท่านั้น")
- lint ข้อ 44 เขียนใหม่ (ตารางภาษา): _lnSelMsg ต้องใช้ t('ln.hint') · ตารางต้องมี ln.hint TH+EN · typoSelect/applyLang คงเดิม · ห้ามเหลือ ::after/--lnhint · ทดสอบไฟล์ใส่บั๊ก 7 แบบ จับได้ครบ
- วิธี: เนื้อเมนู+i18n บรรทัดเดียว 4MB (file_edit แก้ไม่ได้) · on-device write+python sandbox ยังล่ม (error 500 / timeout 65s แม้อ่านเบา) → ทำบน workspace ทั้งหมด (HTML+lint) รัน lint ที่เครื่องกลาง แล้ว copy กลับ 2 ไฟล์ · file_copy/file_edit/file_read (SNCS) ยังปกติ

## 10 ต.ค. 2026 (17:30) — ✅ ย้ายข้อความเส้นจุดจากในช่อง → แถบล่าง · lint ผ่าน · ยังไม่ทดสอบในเบราว์เซอร์ · ยังไม่ commit (ต่อจาก 633908e)
- ผู้ใช้พบ (ภาพ): วางในช่องแล้วข้อความขาด (ช่องเส้นจุดแคบ อยู่ระหว่างชื่อ-ราคา) · decision 17:27 เลือก "แถบล่าง" (เต็มเสมอ ไม่ตัด ไม่ทับ)
- ลบ: .ln.typosel::after (ในช่อง) + position:relative + --lnhint (setProperty ใน applyLang + removeProperty ใน build* 2 จุด)
- เพิ่ม: _lnSelMsg(type)=tkj([_typoLabel, ' — '+(_lang EN/TH)]) · typoSelect: setStatus isLine?_lnSelMsg(type):_typoLabel(type) · applyLang: ถ้าเลือกเส้นจุดอยู่ → setStatus(_lnSelMsg(_typoType)) สร้างใหม่ตอนสลับภาษา
- ข้อความ: "เปลี่ยนสีและแบบเส้นได้เท่านั้น" / "Change color and line style only" (ยัง inline ใน _lnSelMsg + applyLang ไม่ได้อยู่ I18N table เพราะ on-device write ยังล่ม)
- lint ข้อ 44 เขียนใหม่ (status-bar): _lnSelMsg มี TH+EN · typoSelect ใช้ isLine?_lnSelMsg · applyLang re-render · ห้ามเหลือ ::after/--lnhint · ทดสอบไฟล์ที่ใส่บั๊ก 4 แบบ จับได้ครบ · html sha 76ef4a36f4680ee0
- ⚠ on-device write (run_python_on_device_with_write) ยังล่ม error 500 ต่อเนื่อง (~11:19 ถึง 17:30+) — ทำผ่าน file_edit ทั้งหมด · read ปกติ

## 10 ต.ค. 2026 (16:50) — ✅ ข้อความเส้นจุด: "เปลี่ยนสีและแบบเส้นได้เท่านั้น" + ย้ายมากลางช่อง · lint ผ่าน · ยังไม่ทดสอบในเบราว์เซอร์ · ยังไม่ commit (
- ผู้ใช้เลือก (decision 16:50): ใส่ "เท่านั้น" (ตรงความจริง — เลือกเส้นจุดแล้วแก้ได้แค่สี+แบบเส้น ปุ่มอื่นจาง) + ย้ายข้อความจากลอยเหนือเส้น → กลางช่อง (เดิมลอยทับหัวกลุ่มแถวบน)
- CSS .ln.typosel::after: bottom:100% → top:50% translate(-50%,-50%) · + max-width:100% box-sizing overflow:hidden text-overflow:ellipsis (ตัด … เมื่อช่องแคบ) · font:italic (คำแนะนำ ไม่ใช่เนื้อหา) · applyLang TH "เปลี่ยนสีและแบบเส้นได้เท่านั้น" / EN "Change color and line style only"
- lint ข้อ 44 เพิ่มเช็ค: ต้องมี text-overflow:ellipsis + max-width · ห้าม bottom:100% (ทับแถวบน) · ทดสอบไฟล์ที่ใส่บั๊ก 2 แบบ จับได้ครบ · html sha f19f256493a950c0
- ⚠ on-device write (run_python_on_device_with_write) ยังล่ม error 500 (ตั้งแต่ ~11:19 ถึง 16:50+) — ทำผ่าน file_edit ทั้งหมด · read-on-device ปกติ

## 10 ต.ค. 2026 (11:19) — ✅ ข้อความบอกเส้นจุด "เปลี่ยนสีและแบบเส้นได้" (ขึ้นจางเฉพาะเส้นที่เลือก) · lint ผ่าน · ยังไม่ทดสอบในเบราว์เซอร์ · ยังไม่ commit (ต่อจาก 0a4c5d1)
- CSS body.editmode .ln.typosel::after content var(--lnhint, ไทย) · .ln ได้ position:relative · @media screen · ::after ไม่อยู่ DOM = ไม่หลุดไฟล์/snapshot
- ⚠ ช่อง on-device write (run_python_on_device_with_write) ล่ม error 500/timeout ตั้งแต่ ~11:19 ยาวถึง 15:36+ (ยังล่ม) — อ่านได้ · แก้ไฟล์ผ่าน file_edit (SNCS fs) ได้ · ทำส่วนที่เหลือทาง file_edit ทั้งหมด
- TH/EN: เลี่ยงบรรทัด i18n ยาว ~11,000 ตัว (file_edit ไม่ไหว) → ใส่ TH/EN inline ใน applyLang: setProperty('--lnhint', _lang==='en'?EN:TH) · strip --lnhint ใน buildEditorHtml + buildMenuHtml (คู่กับ --a4lbl) · ข้อยกเว้น: ข้อความนี้ไม่ได้อยู่ใน I18N table (inline แทน) เพราะช่อง write ล่ม — ถ้าจะย้ายเข้า table ภายหลัง ใช้ ln.hint
- lint ข้อ 44 (ทดสอบไฟล์ที่ใส่บั๊ก 4 แบบ จับได้ครบ: no var / not @media screen / EN หาย / strip หาย) · html sha 5028b000ad19e121

## 10 ต.ค. 2026 (11:08) — ✅ press state ปุ่มกดครั้งเดียว (แบบ ก · :active) · ผู้ใช้ทดสอบผ่าน (กดเทา ปล่อยปกติ · ปุ่มอ่อนเขียวยุบแล้วกลับ) · ✅ commit แล้วใน 0a4c5d1 (11:17)
- CSS หลัง #typobar button.tbtn.on:hover: transform:translateY(1px) ทุกปุ่ม toolbar :active:not(:disabled) · พื้นเทา #e1dfdd (edbar/imgbar .b-lg · tbtn · shd-pop) :not(.on) · szbtn/qab พื้น #dce9e0 · ไม่ใช้เขียว
- qab press เดิม border เขียว #217346 → lint ข้อ 43 (ที่เพิ่งเขียน) จับได้ → แก้เป็น #9db3a5 · lint #7 ไม่ false-positive (:not(.on) มี .on substring = ถูกข้าม)
- lint ข้อ 43 (ทดสอบไฟล์ที่ใส่บั๊ก 4 แบบ จับได้ครบ: ไม่มี :active / เขียว / ไม่มี transform / background ไม่กัน .on) · UI_STANDARD ข้อ 1 · sha256 9d793961046ef531
- commit: รอบ 10:56 = fa20690 (lint #42) · รอบ 11:08 = 0a4c5d1 (lint #43) · ผู้ใช้ทดสอบผ่านทั้งคู่ 11:17 · git สะอาด
- ผู้ใช้ 11:05: ปุ่มกดครั้งเดียวควรแสดงจังหวะกด · agent ค้าน "เขียวแวบ" (ชนความหมายโหมด ข้อ 1) → เลือกแบบ ก = :active press (กดค้างยุบ+พื้นเข้มขึ้น ปล่อยกลับทันที ไม่ใช้เขียว)
- ⚠ commit ถัดไปจะรวม 2 รอบ (10:56 + 11:08) แยกไม่ได้ · sha ก่อนเริ่ม d3869e726b100edd

## 10 ต.ค. 2026 (10:56) — ✅ ใส่ Mortar1 หน้า 2 + ย้าย Plapao17 + ปุ่มคัดลอกตำแหน่งรูป · ผู้ใช้ทดสอบผ่าน (คัดลอกตำแหน่งวางใน Notepad ได้) · ✅ commit แล้วใน fa20690 (11:16)
- Mortar1.png (500×584 · 303,164 B ไม่ย่อ) หน้า 2 data-num 6 ratio 0.856 (กรอบ 0.858 · crop ~0) เงา soft · data-fname Mortar1.png · แทรกหลัง Beverage17 ใน DOM
- Plapao17: X155.1 Y278.3 → X154.6 Y276.7 (W/H เดิม) · ส่วนที่เห็น (alpha) ก่อนหน้าอยู่ล่างสุด ~293.2mm ตอนนี้ขยับขึ้น 1.6mm = ปลอดภัยขึ้น
- ปุ่มคัดลอกตำแหน่ง #btnImgCopyPos (imgCopyPos) ต่อจากคัดลอกชื่อ · _imgPos/_imgPosStr/_imgCopyPosSync · readout refactor ใช้ _imgPos (แถบล่าง + คัดลอก ค่าตรงกัน) · รูปแบบ X=..mm Y=..mm Width=..mm Height=..mm (เท่าที่ผู้ใช้พิมพ์สั่ง) · _copyText + สำรอง · buildEditorHtml ล้างสถานะ
- lint ข้อ 42 (ทดสอบไฟล์ที่ใส่บั๊ก 6 แบบ จับได้ครบ) · แก้ตัวนับ i18n ของ lint (เพิ่ม ; ในกลุ่มที่ข้าม ternary ok?A:B; — ternary ใน _imgCopyPosSync ลงท้าย ; ทำให้นับคำแปลเกิน) กระทบ lint 38/40/42 · UI_STANDARD ข้อ 6 · sha256 d3869e726b100edd
- Mortar1.png หน้า 2 X50.9 Y51.1 W27.3 H31.8 เงาอ่อน · Plapao17 → X154.6 Y276.7 W31.8 H15.9 · ปุ่มคัดลอกตำแหน่ง (เช่น X=50.9mm Y=51.1mm Width=27.3mm Height=31.8mm)
- sha ก่อนเริ่ม 5f5873a3d720d052

## 10 ต.ค. 2026 (10:50) — ✅ เงาทุกรูป → อ่อน · ยกเว้น PlaPaoPaiFai2 = ไม่มีเงา · lint ผ่าน · ยังไม่ดูในเบราว์เซอร์ · ยังไม่ commit (ต่อจาก 0654049)
- 4 รูป strong → soft (HotpotHeader2 p1/p2 · Plapao17 p1 · Beverage17 p2) · PlaPaoPaiFai2 p1 soft → ลบ data-shadow (ไม่มีเงา)
- บั๊กตอนทำ (ภายใน agent · แก้แล้ว): รอบแรกหา alt= ใน 400 ตัวหลัง <div> แต่ alt อยู่หลัง base64 ยาว → ไม่เจอ ไม่แก้อะไร · รอบ 2 ใช้ data-fname (อยู่ในแท็ก) สำเร็จ
- ค่าระดับ: soft ยังเป็นค่าเริ่มต้น 0.6/0.8/35 · --shd-strong 1.0/1.0/90 ยังอยู่บน .page style แต่ไม่มีรูปใช้ระดับ strong แล้ว (ค้างไว้ ไม่กระทบ) · sha256 5f5873a3d720d052
- ผู้ใช้: เปลี่ยนเงาทุกรูปเป็นอ่อน ยกเว้น PlaPaoPaiFai2-H500.png ไม่ใส่เงา · sha ก่อน 99af27d18ff63095

## 10 ต.ค. 2026 (10:40) — ✅ รายการแบบเส้น (typoLineStyle) เปลี่ยนไม่ได้ + เส้นจุด affordance (10:00) · ผู้ใช้ทดสอบผ่าน (ภาพ: dropdown จุด/ขีด/ทึบ เปิดได้ · เส้นจุดมีกรอบ) · ✅ commit แล้วใน 0654049 (10:48)
- แก้: เพิ่ม typoLineStyle ในรายการยกเว้น mousedown ของ #typobar · เสริม lint ข้อ 35 ตรวจทั้ง <input> และ <select> (เดิมแค่ <input>) ทดสอบ: ลบ typoLineStyle / typoFont ออกจากยกเว้น → จับได้ทั้งคู่ · UI_STANDARD ข้อ 5 · sha256 99af27d18ff63095
- หมายเหตุ: ยังไม่ได้ commit 2 งาน (เส้นจุด affordance 10:00 + แก้นี้) — ทดสอบรวมแล้ว commit ทีเดียว
- ผู้ใช้ 10:39: เส้นจุดเปลี่ยนได้แค่สี แบบเส้นเปลี่ยนไม่ได้ · สาเหตุ: #typobar mousedown preventDefault ยกเว้นเฉพาะ typoColor/Hex/OlHex/CpDlgHex/Size/Font + OPTION · ลืม typoLineStyle (select) → คลิกแล้ว dropdown ไม่เปิด · สีเปลี่ยนได้เพราะ typoColor อยู่ในรายการยกเว้น
- แก้: เพิ่ม typoLineStyle ในรายการยกเว้น · เสริม lint ข้อ 35 ให้ตรวจ <select> ใน typobar ด้วย (เดิมตรวจแค่ <input>) · sha ก่อน 1992a237cb64ae17

## 10 ต.ค. 2026 (10:00) — ✅ เส้นจุด (.ln) โชว์ว่าคลิกแก้ได้ (แบบ ก) · ✅ commit แล้วใน 0654049
- CSS @media screen body.editmode .ln: outline 1px dashed #1592d9 + bg rgba(21,146,217,.08) + border-radius 3px + cursor:pointer + min-height:1.2em · เหมือน affordance .nm/.pr (บรรทัดก่อนหน้า) ต่างที่ cursor (ไม่ใช่ contenteditable) + min-height
- ไม่แตะ JS (คลิกเลือกเส้นจุดทำงานอยู่แล้วผ่าน _typoFind closest(.ln) ที่ handler บรรทัด ~3758) · flex:1 เต็มช่องว่างอยู่แล้ว
- lint ข้อ 41 (ทดสอบไฟล์ที่ใส่บั๊ก 3 แบบ จับได้ครบ: ไม่มี affordance / ไม่มี outline / ไม่อยู่ใน @media screen) · UI_STANDARD ข้อ 5 · sha256 1992a237cb64ae17
- ผู้ใช้ 09:56: ไม่คลิกโดนเส้นก็ไม่รู้ว่าแก้ได้ · เลือกแบบ ก = กรอบเส้นประ+พื้นจางถาวรในโหมดแก้ เหมือน .nm/.pr + ขยายกล่องคลิก
- CSS @media screen body.editmode .ln (คลิกไต่ closest(.ln) อยู่แล้ว · flex:1 เต็มกว้างอยู่แล้ว · เพิ่ม min-height) · cursor:pointer (ไม่ใช่ contenteditable) · วัด overflow strip editmode = ไม่กระทบ · lint ข้อ 41 · sha ก่อน 3cab3e8a7e83bb66

## 10 ต.ค. 2026 (01:22) — ✅ ทำเสร็จ (01:50): แก้งานค้าง 6 ข้อ + lint ข้อ 40 · lint ผ่าน · ยังไม่ทดสอบในเบราว์เซอร์ · ยังไม่ commit (ต่อจาก d376244)
- 1) เส้นจุด: applyColorRange ทาสีเส้น (+ fl.lineColor/Same) · ปุ่มสีไม่จางตอนเลือกเส้น · _cpDlgOk ทาเส้นด้วย (ลบ var line ที่ไม่ใช้ + key fl.cpStoredLine) · typoLineApply เปลี่ยนเฉพาะแบบ + แจ้งผล · ลบ typoColorApply/typoColorLive (ไม่มีใครเรียก)
- 2) _restorePages: typoClear() เมื่อ _typoEl หลุด + ล้าง lastEditable/savedRange · 3) ลบ addEventListener change ของ typoFont · typoFontApply แจ้ง fl.fontRange/fontCell/fontSame
- 4) _imgReadout(null) setStatus เฉพาะ imgmode · 5) _styleExec (B/I/U/S) แจ้ง fl.styleOn/Off · 6) ลบรูป × แจ้ง fl.imgDel + _imgHideSync + checkOverflow
- i18n TH/EN 13 key · lint ข้อ 40 (ทดสอบไฟล์ที่ใส่บั๊ก 11 แบบ จับได้ครบ · แก้ข้อตรวจ i18n ของ lint 38/40 ที่นับค่าคำเดียวผิด) · UI_STANDARD ข้อ 6 · sha256 3cab3e8a7e83bb66
- ขั้น 1 อ่านโค้ด · ขั้น 2 แก้ไฟล์ · ขั้น 3 lint ข้อ 40 + ทดสอบไฟล์ที่ใส่บั๊ก · ขั้น 4 เอกสาร · sha ก่อนเริ่ม ebb03ab429f01566
- ขั้น 1 ✅ (เจอเพิ่ม: หน้าต่าง + กำหนดเอง ก็ข้ามเส้นจุด) · ขั้น 2 ✅ แก้ไฟล์ sha dc6956e856266e12 · ขั้น 3 lint ข้อ 40 = ถัดไป

## 10 ต.ค. 2026 (00:25) — ✅ ตรวจเสร็จ (รายงาน 01:20 — agent หยุดหลังตรวจโดยไม่รายงาน ซ้ำครั้งที่ 2): งานค้างกลุ่ม 1–2 ยังเป็นจริงครบ 6 ข้อ · ไม่ได้แก้ไฟล์ (sha ebb03ab429f01566 = d376244)
- 1) เส้นจุด: เลือกเส้นจุดแล้ว ปุ่มสี (typoCpApply) จาง · กดสีในจานสี → applyColorRange ข้ามเส้นจุด ไม่มีอะไรเปลี่ยน ไม่มีข้อความ · สีเปลี่ยนจริงเฉพาะตอนเปลี่ยนแบบเส้น (typoLineApply ใช้สีปัจจุบัน) · typoLineApply ไม่มีข้อความผล · typoColorApply / typoColorLive = code ที่ไม่มีใครเรียก
- 2) หลัง Ctrl+Z: _restorePages ไม่ล้าง _typoEl (มีตัวกันแค่ช่องขนาด live()) → ทาสีทั้งช่อง/ฟอนต์/ขนาดปุ่ม ฯลฯ แก้ช่องที่หลุดจากหน้า แถบล่างบอกว่าสำเร็จ แต่หน้าไม่เปลี่ยน (snapshot เท่าเดิม = ไม่มีจุด Undo)
- 3) ช่องฟอนต์: onchange="typoFontApply()" + addEventListener change (applyExec fontName + fl.fontRange) · ไม่มีไฮไลท์ = เปลี่ยนทั้งช่องถูก แต่แถบล่างขึ้น "ยังไม่ได้ไฮไลท์" แล้วตามด้วยผล "ช่วงที่เลือก" (ข้อความผิด) · มีไฮไลท์ = ทำ 2 รอบ
- 4) toggleImgMode ออก: setStatus(st.ready) แล้ว _imgReadout(null) ทับเป็น "คลิกรูป…"
- 5) B/I/U/S: applyExec ไม่มี flashStatus → มีไฮไลท์ ทำได้แต่ไม่มีข้อความผล
- 6) ลบรูป ×: el.remove + markDirty + _imgReadout(null) → แถบล่างขึ้น "คลิกรูป…" ไม่มีผล "ลบรูป N แล้ว" · ไม่เรียก _imgHideSync (ปุ่มซ่อนรูปไม่อัปเดตจำนวน)
- next: รอผู้ใช้เลือกแก้ (แนะนำแก้ทั้ง 6 ข้อรอบเดียว + lint ข้อ 40)
- ข้อที่ตรวจ: 1) ปุ่มสีเส้นจุด 2) แถบรูปแบบหลัง Ctrl+Z 3) ช่องฟอนต์ผูก 2 ครั้ง 4) ออกจากแก้รูปแล้วแถบล่างค้าง "คลิกรูป…" 5) B/I/U/S ไม่มีผล 6) ลบรูป (×) ไม่มีผล
- sha ตอนเริ่ม ebb03ab429f01566

## 9 ต.ค. 2026 (19:33) — ✅ ป้ายใต้รูป 2 แถว (ชื่อ / ขนาด) + ย้ายลงใต้ปุ่มย่อขยาย · ผู้ใช้ทดสอบผ่าน (ภาพหน้าจอ HotpotHeader2.png / 68.5 × 31.8 mm ใต้ปุ่มย่อขยาย) · ✅ commit แล้วใน d376244 (19:50)
- สถานะ: git สะอาดที่ d376244 · ไฟล์บนดิสก์ sha ebb03ab429f01566
- ค้าง: งานกลุ่ม A (ปุ่มสีเส้นจุดไม่ทำงาน · แถบรูปแบบหลัง Ctrl+Z · ช่องฟอนต์ผูก 2 ครั้ง) · กลุ่ม B/C/D ตามรายการต้นไฟล์ · ยังไม่เคยรัน verify_oe.py
- CSS .fimg .sizetag: margin-top 6px → 30px (.rz bottom:-26px) · white-space nowrap → pre + text-align center · JS _imgReadout: " · " → "\n" ระหว่างชื่อกับขนาด · ไม่มีชื่อ = แถวขนาดแถวเดียว
- lint ข้อ 39c (ทดสอบไฟล์ที่ใส่บั๊ก 3 แบบ จับได้ครบ) · UI_STANDARD ข้อ 6 · sha256 ebb03ab429f01566

## 9 ต.ค. 2026 (19:30) — สถานะ: git สะอาดที่ 3047534 · ไฟล์บนดิสก์ sha ecd8aa40aeca733b
- ภาพทดสอบของผู้ใช้: รูปทดสอบ Plapao18-H500…png อยู่ในกลุ่มข้าว & เส้น (ยังไม่บันทึก — อยู่แค่ในเบราว์เซอร์)
- พบจากภาพ: ป้ายใต้รูป (.sizetag กึ่งกลาง margin-top 6px) ถูกปุ่มย่อขยาย (.rz right/bottom -26px) ทับ เมื่อป้ายกว้างกว่ารูป → ตัวเลขขนาดอ่านไม่ได้
- ผู้ใช้ถาม: ป้ายเป็น 2 แถว (ชื่อ / ขนาด) ดีไหม · agent แนะนำ 2 แถว + ย้ายป้ายลงใต้ปุ่มย่อขยาย (รอตัดสินใจ)

## 9 ต.ค. 2026 (19:15) — ✅ ปุ่ม "คัดลอกชื่อ" + ชื่อไฟล์ยาว · ผู้ใช้ทดสอบชื่อยาวผ่าน · ✅ commit แล้วใน 3047534 (19:30 · รวม 3 รอบ 18:23 + 18:26 + 19:15)
- ทำจริง: #btnImgCopyName (ท้ายกลุ่ม จัดการรูป) · _imgCopySync / _copyText / _copyFallback / imgCopyName · _cutMid (ป้ายใต้รูป) · .edstatus-msg overflow-wrap:anywhere · tooltip mouseenter/leave ใน _imgBind (เฉพาะ imgmode) · ลบ .fimg[title] ใน _serializePages / buildEditorHtml / buildMenuHtml · บันทึกแล้วปุ่มจาง
- i18n TH/EN 6 key · lint ข้อ 39b (ทดสอบไฟล์ที่ใส่บั๊ก 7 แบบ จับได้ครบ) · UI_STANDARD ข้อ 6 · ยังไม่รู้: Chrome/Edge ยอมให้คัดลอกจาก file:// หรือไม่ (มีทางสำรอง) · sha256 ecd8aa40aeca733b
- เหตุ: แถบล่างแสดงชื่อเต็มแต่คัดลอกไม่ได้ (mousedown นอก #edbar ในโหมดแก้รูป = ยกเลิกเลือกรูป) · ชื่อยาว: _cut30 ตัดนามสกุลหาย · แถบล่างไม่ตัดคำยาวติดกัน
- sha ก่อนเริ่ม c0ac0891ffc8ab0e
- ขั้น 1 ✅ · ขั้น 2 ✅ แก้ไฟล์ sha ecd8aa40aeca733b · ขั้น 3 lint = ถัดไป

## 9 ต.ค. 2026 (18:26) — ✅ แสดงชื่อไฟล์รูปตอนแก้ (5 ข้อ) · ✅ commit แล้วใน 3047534
- ทำจริง: _imgFname · _imgReadout (แถบล่างชื่อเต็ม · ป้ายใต้รูป _cut30) · imgAdd จำ f.name · imgToAllPages คัดลอก · buildMenuHtml ลบ data-fname · 5 รูปเดิมใส่ชื่อจริง (HotpotHeader2.png ×2 · PlaPaoPaiFai2-H500.png · Plapao17-H500.png · Beverage17-H500.png)
- นอกขอบเขต: โลโก้ / ป้ายกลุ่ม (.secimg) ใช้ _readImageFile เหมือนกันแต่ไม่ใช่ .fimg — ยังไม่มีชื่อ
- lint ข้อ 39 (ทดสอบไฟล์ที่ใส่บั๊ก 7 แบบ จับได้ครบ หลังแก้ข้อตรวจ _imgReadout 1 รอบ · รูปไม่มีชื่อ = warning) · UI_STANDARD ข้อ 6 · sha256 c0ac0891ffc8ab0e
- แผน: data-fname บน .fimg · แถบล่าง + ป้ายขนาดใต้รูปที่เลือกแสดงชื่อไฟล์ · imgAdd จำ f.name · ใส่ทุกหน้าคัดลอก · ใส่ชื่อจริงให้ 5 รูปเดิม · ไม่พิมพ์ · lint ข้อ 39
- ผู้ใช้ถาม: ชื่อไฟล์รูปมีกฎไหม หรือตาม Windows · sha ก่อนเริ่ม dc677c5dad5400de · HEAD ตอนเริ่ม 16295fc
- ขั้น 1 ✅ (_renderStatus + ป้ายใต้รูปใช้ textContent = ชื่อไฟล์แสดงตรงตัว) · ขั้น 2 ✅ แก้ไฟล์ sha c0ac0891ffc8ab0e · ขั้น 3 lint ข้อ 39 = ถัดไป

## 9 ต.ค. 2026 (18:23) — เงา 1.0 / 1.0 / 90% ทุกรูปยกเว้น PlaPaoPaiFai2 · ✅ commit แล้วใน 3047534
- ค่าเงาเป็นของระดับ (ทั้งเมนู) ไม่ใช่ต่อรูป → ตั้งระดับ "ชัด" = 1.0mm / 1.0mm / 90% (--shd-strong บน style ทั้ง 2 .page · รูปแบบเดียวกับ _shdStr) · 4 รูป (HotpotHeader2 ×2 · Plapao17 · Beverage17) → data-shadow strong · PlaPaoPaiFai2 คง soft ค่าเริ่มต้น 0.6/0.8/35
- ผลข้างเคียง: รูปใดตั้ง "ชัด" ภายหลังได้ค่านี้ · ปุ่ม ค่าเริ่มต้น ของ ชัด = กลับ 1.2/1.6/55 · lint ผ่าน · sha256 dc677c5dad5400de
- ผู้ใช้ถาม: ควรแสดงชื่อรูปตอนแก้ไหม (รอตัดสินใจแบบ)

## 9 ต.ค. 2026 (18:16) — ✅ ย้ายรูปเครื่องดื่ม หน้า 2 · ✅ commit แล้วใน 16295fc (18:22)
- Beverage17: X148 Y189.0 → X146.9 Y198.3 (W38.4 H21.2 เดิม) · lint ผ่าน · sha256 e2bf08216312e5ba
- ผู้ใช้ตัดสินใจ 18:16: ยอมรับคำเตือนล้นหน้า 2 (เนื้อหาเข้าขอบล่าง ~1mm แต่พิมพ์ครบ) — เกณฑ์ของงานนี้ = พิมพ์แล้วไม่ขาด ไม่หลุดหน้า · ไม่ต้องให้ขอบเท่ากันเป๊ะ · ร้านลาบต้นทุนน้อย ผู้ใช้ทำให้ฟรี ทำเท่าที่อยู่ในความสามารถและเวลา

## 9 ต.ค. 2026 (18:08) — ✅ รูปหัวกระดาษเดียวกันทั้ง 2 หน้า (ผู้ใช้เลือก) · ✅ commit แล้วใน e587f36 (18:11)
- ⚠ 18:11 ผู้ใช้ตอบ "ไม่ล้น" แต่ภาพหน้าจอยังมีแถบล่างสีเหลือง (คำเตือนล้นหน้า) + กรอบทองหน้า 2 · agent วัดจากภาพ (1189px = 210mm): กลุ่มล่างสุดห่างขอบล่าง ~6.9mm < padding 8mm → เนื้อหาล้นเข้าขอบล่าง ~1mm (ประมาณ) · ไม่ถูกตัดตอนพิมพ์ (พิมพ์ไม่ได้แค่ 3mm) · รอผู้ใช้เลือกวิธีแก้
- หน้า 2: Jimjum5 (X81.6 Y5.3 W63.2 H31.8) → HotpotHeader2 ภาพเดียวกับหน้า 1 (คัดลอก base64 จากหน้า 1) X76.8 Y3.7 W68.5 H31.8 · data-num 4 · ratio 2.155 · เงา soft
- ทั้ง 2 รูปใส่ data-syncid="hdrpot" (แบบเดียวกับ ใส่ทุกหน้า) → กด ใส่ทุกหน้า ที่รูปนี้ = ไม่ใส่ซ้ำ · id ไม่ชนกับที่ระบบสร้าง (sync+N) · syncid ใช้กันซ้ำอย่างเดียว ย้าย/ย่อขยายยังแยกหน้า
- ยังค้าง: หน้า 2 ขอบสีทอง = ตัวเตือนล้นหน้า — ผู้ใช้ยังไม่ยืนยันว่าล้นจริงไหม · sha256 8d250e9598fcf2bd

## 9 ต.ค. 2026 (18:00) — ✅ ลบรูปข้าวเหนียว + ลบป้ายปลาเผา (เมนูปลา) + ใส่ PlaPaoPaiFai2 หน้า 1 + ย้าย Plapao17 · ✅ commit แล้วใน 0f6c25e (18:07)
- PlaPaoPaiFai2-H500.png (1877×500 · 558,160 B · ไฟล์ต้นฉบับไม่ย่อ) แทน StickyRice ที่ตำแหน่งเดิมใน DOM · data-num 2 (ใช้เลขที่ว่าง) · data-ratio 3.754 · data-shadow soft (เท่ารูปอื่น) · กรอบ 3.739 → cover ตัดซ้าย-ขวารวม ~0.2mm
- Plapao17: X136.6 Y240.7 → X155.1 Y278.3 (W/H เดิม) · ส่วนที่มองเห็น (alpha) ล่างสุด 293.2mm < 294mm (ขอบพิมพ์ไม่ได้ 3mm) ✓ · PlaPaoPaiFai2 ส่วนที่เห็น Y258.7–270.6mm
- ป้าย .secimg "ปลาเผา" ในหัวกลุ่มเมนูปลาลบแล้ว (เพิ่มกลับได้ด้วย + ป้าย ในโหมดแก้รูป) · ไม่มี .secimg เหลือในหน้าเมนู
- คำตอบผู้ใช้: ขอบสีทองหน้า 2 = .page.overflowed (outline 3px #e8a020) = ตัวเตือนล้นหน้า ไม่พิมพ์ (@media print outline:none) · น่าจะเกิดจากชื่อเมนู 17.5px คอลัมน์เมนูตำ 31 แถว (agent ประเมิน ยังไม่ยืนยัน) · รอผู้ใช้ดูแถบล่าง + ตัวอย่างก่อนพิมพ์หน้า 2
- คำถามรูปหัวกระดาษ: agent แนะนำรูปเดียวกันทั้ง 2 หน้า (หัวกระดาษ = ส่วนแบรนด์คงที่) หรืออย่างน้อยขนาด/ตำแหน่งเท่ากัน · รอผู้ใช้ตัดสินใจ
- ผู้ใช้: PlaPaoPaiFai2-H500.png X146.6 Y257.7 W51.6 H13.8 · Plapao17 X155.1 Y278.3 W31.8 H15.9 · ถาม: รูปหัวกระดาษ 2 หน้าควรเหมือนกันไหม · ทำไมหน้า 2 มีขอบสีทอง
- sha ก่อนเริ่ม 82f39e3178932746

## 9 ต.ค. 2026 (17:45) — สถานะ: git สะอาดที่ b23ce85 · ไฟล์บนดิสก์ sha 82f39e3178932746
- ⚠ หน้าจอผู้ใช้ตอนทดสอบ: "แจ่วฮ้อนรวม" ขนาด 19.5 (กด + ทดสอบ) — ยังไม่ได้บันทึกลงดิสก์ · ถ้ากด Save จากหน้านั้นจะติดลงไฟล์ · แจ้งผู้ใช้แล้ว
- ค้าง: รูปปลาเผา (Plapao17 Y240.7mm หน้า 1) ทับแถว "เฟรนช์ฟรายส์ทอด" หลังชื่อเมนู 17.5px · ตรวจรูปข้าวเหนียว p1 / เครื่องดื่ม p2 ด้วย · งานค้างกลุ่ม A (ปุ่มสีเส้นจุด · แถบรูปแบบหลัง Ctrl+Z · ฟอนต์ผูก 2 ครั้ง)

## 9 ต.ค. 2026 (17:38) — ✅ ปุ่ม +/− ขนาดตัวอักษรทีละ 0.5 (แบบ ข · ผู้ใช้เปลี่ยนจากแบบ ก) · ผู้ใช้ทดสอบผ่าน (ภาพหน้าจอ 19.5) · ✅ commit แล้วใน b23ce85 (17:43 · รวม 3 รอบ 16:56 + 17:15 + 17:38)
- เหตุผล: ปุ่มต้องไปถึงทุกค่าที่ช่องรับได้ (ช่องรับ .5 แต่ปุ่มทีละ 1 จากจำนวนเต็มไม่มีวันได้ .5) · ผู้ใช้ปรับละเอียดเพื่อให้ขอบบน/ล่างสมดุล
- แก้: typoSizeStep(±0.5) · ผล _sizeHalf(cur+d) · tooltip TH/EN "ใหญ่ขึ้น 0.5 / เล็กลง 0.5" · lint ข้อ 38 · UI_STANDARD ข้อ 6 · sha ก่อน 6b49b59c799a86c6 → 82f39e3178932746

## 9 ต.ค. 2026 (17:15) — ชื่อเมนูทั้งหมด (.nm) 16px → 17.5px · ✅ commit แล้วใน b23ce85
- ✅ ผู้ใช้ทดสอบ 17:31: ไม่ล้นหน้า · เหตุผลของผู้ใช้: ให้ขอบล่างสมดุลกับขอบบน (ขอบล่างไม่ว่างเกิน) + อ่านง่ายขึ้น · ภาพ 1 = ก่อนเปลี่ยน (CSS เดิม 16px — ผู้ใช้เรียกว่า 17)
- ⚠ พบจากภาพ 2 ของผู้ใช้: รูปปลาเผา (.fimg Plapao17 Y240.7mm) ตอนนี้ทับแถว "เฟรนช์ฟรายส์ทอด" ของกลุ่มข้าว & เส้น — เนื้อหาเลื่อนลงตามขนาดตัวอักษร แต่รูปวางด้วย top mm คงที่ · รูปอื่นที่อาจเลื่อนสัมพัทธ์: ข้าวเหนียว p1 Y183 · เครื่องดื่ม p2 Y189 · รอผู้ใช้ตัดสินใจ
- ผู้ใช้ถาม: ปุ่ม +/− ควรทีละ 0.5 ไหม (รอตอบ)
- ผู้ใช้ 17:11 ทดสอบรอบ 16:56: พิมพ์ 16.5 ได้ · เข้าใจผิดเรื่อง +/− (แบบ ก ทำงานถูก) · 17:13 ขอชื่อเมนูทั้งหมด 17.5
- แก้ CSS .nm 1 จุด · ตรวจแล้ว 115 ช่องไม่มีขนาดตั้งเฉพาะช่อง → เปลี่ยนตามทั้งหมด · (ราคาตามไซส์) .nm i 12.5px ไม่เปลี่ยน · ราคา .pr ไม่เปลี่ยน
- ⚠ เสี่ยงล้นหน้า 2 (คอลัมน์เมนูตำ 31 แถว) — agent ประเมินจากภาพตัวอย่างก่อนพิมพ์ ~+19mm ถ้าความสูงแถวโตตามขนาดตัวอักษร · รอผู้ใช้ดูคำเตือนล้นหน้า · หลักฐานเพิ่ม: comment เดิมใน CSS บอกว่า 17px เคยล้นหน้า 1, 2 (8 ต.ค. ก่อนลดขอบหัวกระดาษ) · lint ผ่าน · sha256 6b49b59c799a86c6

## 9 ต.ค. 2026 (16:56) — ✅ ขนาดตัวอักษรใส่ทีละ 0.5 ได้ (เช่น 16.5) · ผู้ใช้ทดสอบผ่าน · ✅ commit แล้วใน b23ce85
- ทำจริง: _sizeClean รับจุด 1 จุด ≤4 ตัว · _sizeHalf / _sizeParse ใหม่ · commit ช่องขนาดใช้ _sizeParse (+ fl.sizeStep) · typoSizeStep อ่าน _typoCurSize · reflectFromSelection ปัด 0.5 · inputmode decimal · ลบ curSize() ที่ไม่มีที่เรียก
- i18n: fl.sizeOnly / ttl.sizeType แก้ข้อความ (เดิม "ไม่เกิน 2 หลัก") · fl.sizeStep ใหม่ TH/EN · lint ข้อ 38 (ทดสอบไฟล์ที่ใส่บั๊ก 7 แบบ จับได้ครบ · แก้ข้อตรวจ 2 รอบ: เดิมจับไม่ได้ตอนตัวกรองไม่รับจุด และตอนข้อความ EN หาย) · UI_STANDARD ข้อ 6 · sha256 6a5698394098f020
- ผู้ใช้เลือกแบบ ก: ช่องพิมพ์รับ .5 · ปุ่ม +/− ทีละ 1 คงเศษ (16.5 → 17.5) · ไม่ใช่ .0/.5 = เตือน ไม่ปัดเอง · ช่วง 8–72 เดิม
- จุดที่ต้องแก้: _sizeClean (2 หลัก ไม่มีจุด) · commit ช่องขนาด parseInt · typoSizeStep Math.round · reflectFromSelection Math.round (ไม่ตรงกับ _typoCurSize ที่ปัด 0.5) · i18n fl.sizeOnly / ttl.sizeType · บั๊กเดิม: ช่อง 12.5 กด + ได้ 14
- sha ก่อนเริ่ม 8ccc3f100f3625d4
- ขั้น 1 ✅ · ขั้น 2 ✅ แก้ไฟล์แล้ว sha 6a5698394098f020 (+ ลบ curSize ที่ไม่มีที่เรียก · inputmode decimal) · ขั้น 3 lint ข้อ 38 = ถัดไป

## 9 ต.ค. 2026 (16:12) — ✅ โหมดแก้ หน้าเมนูยาวเกิน A4 + เส้นประขอบ A4 (แบบ ก · ทุกโหมดแก้) · ผู้ใช้ทดสอบผ่าน (TH/EN + ตัวอย่างก่อนพิมพ์ 2 แผ่น) · ✅ commit แล้วใน 9ab69ca (16:46) · ผู้ใช้บอกว่าป้ายขอบ A4 สังเกตยาก
- เปลี่ยนจากแผน: เอา min-width:721px ออก (lint ข้อ 11 ห้าม @media width ที่ไม่มีคู่ measuring) → หน้าต่าง ≤720px ก็ขยายด้วย แต่การตัดบรรทัดไม่เท่าตอนพิมพ์
- lint ข้อ 37 (ทดสอบไฟล์ที่ใส่บั๊ก 7 แบบ จับได้ครบ) · UI_STANDARD ข้อ 7 · sha256 8ccc3f100f3625d4
- งานถัดไปที่เสนอ (แบบ ข): ตอนแก้ รูปไม่เลื่อนตามเนื้อหา → ตำแหน่งรูปเทียบเนื้อหาต่างจากตอนพิมพ์
- ผู้ใช้ 16:04: ตอนแก้ ปุ่ม/กรอบแก้ไขดันเนื้อหาเกิน 297mm → .page overflow:hidden ตัดหาย · ขอขยายพื้นที่ล่างเฉพาะตอนแก้ + เส้นประบอกขอบ A4
- แผน: @media screen · body.editmode/headermode/pricemode/imgmode (ไม่ใช่ measuring) .page → height:auto min-height:297mm overflow:visible · พื้นใต้ 297mm ลายเฉียง · .page::after เส้นประที่ 297mm + ป้าย TH/EN (--a4lbl บน html จาก applyLang · ลบออกตอน buildEditorHtml/buildMenuHtml) · checkOverflow วัดแบบไม่มีโหมดอยู่แล้ว · lint ข้อ 37
- sha ก่อนเริ่ม a12eeedc681040e9
- ขั้น 1 ✅ ไม่มีของที่วางจากขอบล่างของหน้า (bottom: มีแค่ .rz ของรูป / แถบ fixed) · ขั้น 2 ✅ แก้ไฟล์แล้ว sha a07919ee79e42c28 · ขั้น 3 lint ข้อ 37 = ถัดไป

## 9 ต.ค. 2026 (15:55) — สีชื่อเมนู (.nm) #2B3038 → #171A1E · ผู้ใช้ทดสอบผ่าน · ✅ commit แล้วใน 587bcc8 (16:04)
- ผู้ใช้: เฉพาะสีชื่อเมนูเท่านั้น · แก้ CSS .nm 1 จุด + ค่าสำรองสีชื่อเมนูใน newRow (ใช้หาสีเส้นขอบเมื่อค่าเริ่มต้นมีเส้นขอบแต่ไม่มีสี) + comment
- ไม่แตะ (ใช้ #2B3038 เหมือนกัน): ราคา .pr · กล่อง "ทางร้านไม่มีเมนูปู" (.crab .body / .crab b) · ข้อความในหน้าต่างประวัติ · ค่าสำรองสีราคาใน newRow · (ราคาตามไซส์) .nm i #6f6456 ไม่เปลี่ยน
- ตรวจแล้ว: ชื่อเมนู 115 ช่องไม่มีสีที่ตั้งเฉพาะช่อง/บางคำ → เปลี่ยนตาม CSS ทั้งหมด · lint ผ่าน · sha256 a12eeedc681040e9 · ยังไม่ได้ดูในเบราว์เซอร์

## 9 ต.ค. 2026 (15:35) — ✅ ปุ่ม "ใช้กับทุกรูป" ในกลุ่มเงา · ผู้ใช้ทดสอบผ่าน · ✅ commit แล้วใน 9aaf85b (15:51)
- ทำจริง: panel ขอบเขต เฉพาะหน้านี้ / ทุกหน้า (ไม่เลือกไว้ก่อน — UI_STANDARD ข้อ 4 แบบ ใช้ทั้งประเภท) · preview นับรูปที่จะเปลี่ยน · 0 รูป = ปุ่มจาง + เหตุผล · imgShadowAllOpen / _shdAllPlan · hook _imgShdSync · _restorePages · toggleImgMode
- i18n TH/EN 7 key · lint ข้อ 36c (ทดสอบไฟล์ที่ใส่บั๊ก 7 แบบ จับได้ครบ · แก้ false positive ":checked" ใน querySelector) · UI_STANDARD ข้อ 6 · sha256 146b9b47810584b1
- ผู้ใช้: ตั้งเงาแยกรูปดีอยู่แล้ว แต่ขอ option/ปุ่ม apply กับทุกรูป
- แผน: ปุ่ม #btnShdAll → imgShadowAll(): ระดับของรูปที่เลือก → ทุก .fimg ทุกหน้า · 1 จุด Undo · ไม่มีอะไรเปลี่ยน = บอกตรงๆ · ไม่ได้เลือกรูป = ปุ่มจาง · lint ข้อ 36 · sha ก่อนเริ่ม a433b278ebedfac9

## 9 ต.ค. 2026 (15:15) — ✅ ปรับค่าเงา อ่อน/ชัด ทั้งเมนู (แบบ ก) · ผู้ใช้ทดสอบผ่าน 15:27 · ✅ commit แล้วใน 653b889 (15:31 · รวม 4 รอบ: 12:10 · 12:55 · 13:20 · รอบนี้)
- ปุ่ม #btnShdAdj "ปรับค่า" + หน้าต่าง #shdPop · JS: _SHD_DEF/_SHD_RNG · _shdGet/_shdSet/_shdCommit/_shdReset/_shdPopOpen/_shdPopClose/_shdPopRender · hook ใน _restorePages · applyLang · toggleImgMode · buildEditorHtml
- CSS เงา → var(--shd-soft|strong, ค่าเดิม) · i18n TH/EN 22 key · lint ข้อ 36b (ทดสอบไฟล์ที่ใส่บั๊ก 8 แบบ จับได้ครบ) + shd-num ในรายการช่องที่มีตัวกรอง · UI_STANDARD ข้อ 6
- ช่วงค่า (agent ตั้ง ยังไม่ได้ถามผู้ใช้): ระยะ 0–3 mm · เบลอ 0–4 mm · เข้ม 5–90 % (ต่ำสุด 5 = กันเงาที่มองไม่เห็น) · sha256 a433b278ebedfac9
- ✅ ผู้ใช้ทดสอบบนจอผ่าน (15:27 · ภาพหน้าจอ): หน้าต่างปรับค่าเปิดใต้ปุ่ม · "ชัด" ลากสุด 3.0/4.0/90 · "ระดับนี้ใช้อยู่ 1 รูป" · เงาเปลี่ยนจริงเทียบรูปไม่ปรับ · ยังไม่ได้พิมพ์จริง
- ⚠ ค่า "ชัด" ในหน้าจอของผู้ใช้ตอนนี้ = ค่าสูงสุด (ทดสอบ) — ถ้ากด Save จะติดลงไฟล์ · แจ้งผู้ใช้แล้ว
- next: ผู้ใช้ commit 4 รอบ (agent รัน git ไม่ได้ — sandbox บล็อก subprocess)
- 13:27–15:11 agent วิเคราะห์โค้ดแล้วหยุดโดยไม่แจ้งผู้ใช้ · ไม่ได้แก้ไฟล์ (sha ก่อนเริ่ม 19345f8aebf8f55c)
- แบบ: ปุ่ม "ปรับค่า" ในกลุ่มเงา → หน้าต่างเล็ก: เลือกระดับ อ่อน/ชัด + slider 3 ค่า (ระยะ 0–3 mm · เบลอ 0–4 mm · เข้ม 5–90 %) + ช่องตัวเลข + ค่าเริ่มต้น
- เก็บเป็น CSS variable --shd-soft/--shd-strong บน style ของทุก .page (Undo/บันทึก/พิมพ์/เพิ่มหน้า ตามไปเอง) · ค่าเริ่มต้น = ไม่มี variable · ลาก = เห็นทันที · จุด Undo ตอนปล่อย

## 9 ต.ค. 2026 (13:20) — ปุ่มเงารูป ไม่มี / อ่อน / ชัด (แทนการทดลองรอบ 12:55) · ✅ commit แล้วใน 653b889
- แท็บรูป กลุ่มใหม่ "เงา" ต่อจาก "จัดการรูป": ปุ่ม #btnShd_none/_soft/_strong → imgShadow(lv) · จางเมื่อไม่ได้เลือกรูป · ระดับของรูปที่เลือก .on (#imgbar button.b-lg.shd.on + svg + hover)
- CSS: ลบกฎทดลอง .fimg>img filter ทุกรูป → .fimg[data-shadow="soft"]>img drop-shadow(0 0.6mm 0.8mm rgba(60,40,20,.35)) · [data-shadow="strong"] drop-shadow(0 1.2mm 1.6mm rgba(60,40,20,.55)) (ค่า "ชัด" agent ตั้ง ยังไม่ได้พิมพ์ดู)
- รูปเดิม 5 รูปตั้ง data-shadow="soft" (คงหน้าตาที่ผู้ใช้เห็นรอบ 12:55) · รูปเพิ่มใหม่ = ไม่มีเงา
- เลือกระดับเดิม = ไม่เปลี่ยน ไม่มีจุด Undo · เปลี่ยน = _snapNow 1 จุด + flashStatus fl.shdSet (TH/EN) · ใส่ทุกหน้าคัดลอก data-shadow
- แก้บั๊กที่พบระหว่างทำ: (1) imgToAllPages จบด้วย if(vi) — ไม่มีตัวแปร vi → ReferenceError ผล "ใส่รูปไป N หน้าแล้ว" ไม่เคยแสดง → flashStatus(tk(img.allDone/allNone)) (2) _restorePages ไม่ยกเลิกรูปที่เลือกหลัง Undo → ขยาย/ย่อ/ใส่ทุกหน้า/เงา แก้รูปที่หลุดจากหน้า (หน้าไม่เปลี่ยน) → ยกเลิกเลือก + ปุ่มจาง
- refactor: ชื่อรูปใน _imgReadout ย้ายเป็น _imgName(el) ใช้ร่วมกับ imgShadow
- lint ข้อ 36 ใหม่ (CSS 2 ระดับ · ห้าม box-shadow/ filter ทุกรูป · ปุ่ม 3 ปุ่ม · ใส่ทุกหน้าคัดลอก · _imgReadout sync · _restorePages) ทดสอบไฟล์ที่มีบั๊ก 7 กรณี จับได้ครบ · UI_STANDARD ข้อ 6
- พบช่องโหว่ lint ข้อ 7 (ยังไม่แก้): selector .on ที่ไม่มี class ร่วมกับกฎ hover (เช่น #imgbar .shd.on vs #imgbar button.b-lg:hover) ตรวจไม่เจอ
- ตรวจ syntax JS ไม่ได้ในเครื่องมือของ agent (แค่ brace/paren สมดุล) · ยังไม่ได้ทดสอบในเบราว์เซอร์ · sha256 19345f8aebf8f55c
- ✅ ผู้ใช้ทดสอบบนจอผ่าน (13:24 · ภาพหน้าจอ ไม่มี / อ่อน / ชัด ที่รูป 1 · ปุ่ม .on + แถบล่าง + Undo นับ 5→7) · ยังไม่ได้พิมพ์จริง · ผู้ใช้ถามต่อ: ใส่ค่าเอง / slider ปรับเงา ได้ไหม (รอตัดสินใจแบบ)

## 9 ต.ค. 2026 (12:55) — ทดลองเงาอ่อนทุกรูป .fimg เพื่อพิมพ์ทดสอบ · ✅ commit แล้วใน 653b889
- ผู้ใช้ถามเรื่องเงา/ขอบรูป → เลือก "ทดลองเงาอ่อนก่อนพิมพ์ดู" (ยังไม่ทำปุ่ม ไม่มี/อ่อน/ชัด)
- CSS 1 บรรทัดต่อจาก .fimg>img: filter:drop-shadow(0 0.6mm 0.8mm rgba(60,40,20,.35)) · ครอบ 5 รูป .fimg (หม้อหัว 2 + ข้าวเหนียว ปลาเผา เครื่องดื่ม) · ไม่ครอบโลโก้ และรูปป้ายชื่อกลุ่ม (.secimg เช่น "ปลาเผา")
- รอผู้ใช้: ดูบนจอ + พิมพ์จริง 1 แผ่น → ตัดสินใจ เก็บ / ปรับค่า / ทำปุ่ม 3 ระดับ / ลบ · ลบ = ลบบรรทัด CSS ที่มี comment "ทดลองเงาอ่อน"
- lint ผ่าน (warning เดิม function 'p' 2 ครั้ง) · sha256 c008261640823158

## 9 ต.ค. 2026 (12:10) — เปลี่ยนรูปหม้อส่วนหัว หน้า 1 + ย้าย/ขยายรูปหม้อ หน้า 2 · ✅ commit แล้วใน 653b889
- หน้า 1: ลบ Jimjum3 (เดิม X103.2 Y7.1 W33.6 H26.2) → ใส่ HotpotHeader2.png (500×232 px, 146,512 B, ไฟล์ต้นฉบับไม่ย่อ) ที่ X76.8 Y3.7 W68.5 H31.8 mm · data-num 1 · data-ratio 2.155 · alt="HotpotHeader2" · ตำแหน่งเดิมใน DOM
- หน้า 2: Jimjum5 X95.5 Y7.3 W51.7 H26.0 → X81.6 Y5.3 W63.2 H31.8 mm · กรอบ 1.987 vs รูป 1.994 (object-fit:cover ตัดขอบซ้าย-ขวารวม ~0.2 mm)
- lint_oe.py ผ่าน (warning เดิม: function 'p' นิยาม 2 ครั้ง) · sha256 7e343fe330de365e · ยังไม่ได้เปิดดูในเบราว์เซอร์/พิมพ์จริง

## 9 ต.ค. 2026 (11:15) — แก้ช่อง HEX สีขอบ 2 จุด · ✅ commit แล้วใน 4a7174f (11:44) (รวมกับรอบ 09:45 · ต่อจาก 4091263)
- บั๊ก 1: ช่อง HEX สีขอบคลิกแล้วพิมพ์ไม่ได้ — สาเหตุ mousedown ของ #typobar preventDefault ทุกอย่าง ยกเว้นรายชื่อช่องกรอก (ไม่มี typoOlHex) → เพิ่มในรายชื่อ
- บั๊ก 2: "+ กำหนดเอง" ของสีขอบ เปิดหน้าต่างใต้ปุ่มสีตัวอักษร — สาเหตุ #typoCpDlg อยู่ใน #typoColorPick → _cpDlgOpen('edge') ย้ายไป #typoOlPick · ปิดแล้วกลับที่เดิม
- Enter ในช่อง HEX สีขอบ: ใส่สี แล้วรายการยังเปิดอยู่ (เหมือนช่อง HEX สีตัวอักษร)
- lint ข้อ 35: ทุก <input id="typo…"> ต้องอยู่ในรายชื่อยกเว้น · _cpDlgOpen ต้องย้ายไป #typoOlPick (ทดสอบกับไฟล์ที่มีบั๊ก จับได้ทั้ง 2)

## 9 ต.ค. 2026 (09:45) — ช่อง HEX ในหน้าต่างสีขอบ + แปล "Swatch" · ✅ commit แล้วใน 4a7174f (11:44) (ต่อจาก 4091263)
- ผู้ใช้ยืนยัน (09:37): พิมพ์จริงเทียบของเก่า แถบหัวกลุ่มไม่ได้สูงขึ้น · ที่เลื่อนลงมาจากขนาดชื่อเมนูรวมกัน · เคลียร์แล้ว
- ▾ ของปุ่ม A: เพิ่มช่อง HEX (#typoOlHex) ซ้าย "+ กำหนดเอง" ขวา แบบตัวเลือกสีตัวอักษร · แสดงสีขอบที่ปุ่ม A ใช้ · กฎตัวกรองเดียวกับ #typoHex · Enter = ใส่สีขอบ (ผล + Undo)
- ตัวเลือกสีตัวอักษร: หัวข้อ "Swatch" (เขียนตายตัว ไม่แปล) → data-i18n cp.swatchLbl · TH "สีมาตรฐาน" · EN "Swatch" (คงคำเดิม)
- lint ข้อ 16: typoOlHex อยู่ในรายการช่องที่มีตัวกรอง · ทดสอบตรรกะ 16/16 ผ่าน

## 9 ต.ค. 2026 (09:05) — ส่วนหัวสมดุล: ขอบบน 8 mm = ล่าง · ✅ commit แล้วใน 4091263 (09:30) (ต่อจาก 36dcfbe)
- ผู้ใช้: เครื่องพิมพ์พิมพ์ไม่ได้ ~2.5 mm เท่ากันทั้ง 4 ด้าน → เผื่อ 3 mm ทุกด้าน · ขอบข้าง 12 mm คงไว้ (นิ้วจับเมนู)
- วัดจากรูปหน้าจอผู้ใช้ (1191 px = 210 mm): ข้อความ ติดต่อสอบถาม เริ่มที่ ~8.3 mm · โลโก้เดิมเริ่ม 4.2 mm (ยื่นขึ้นไป)
- .page padding 4 → 8mm (+ body.measuring) · .brand align-items center → flex-start · โลโก้ 232 → 173px (สูง 22.7 mm)
- หม้อ p1: X103.2 Y7.1 W33.6 H26.2 · หม้อ p2: X95.5 Y7.3 W51.7 H26.0 (ส่วนที่มองเห็นเริ่ม 8.1 mm = โลโก้ · ล่างห่างเส้นทองเท่าเดิม)
- เนื้อหาเลื่อนขึ้น ~3.75 mm (คำนวณ) · ข้าวเหนียว Y183.0 · ปลาเผา Y240.7 · เครื่องดื่ม Y189.0
- lint ข้อ 34 ตรวจขอบครบ 4 ด้าน ≥ 3 mm (ทดสอบแล้วจับได้)

## 9 ต.ค. 2026 (08:35) — ลดพื้นที่หัวกระดาษ · ✅ commit แล้วใน 36dcfbe · ผู้ใช้ทดสอบ 4 ข้อผ่าน (08:44) · ป้ายล้นหน้า A4 หายแล้ว · ตัวอย่างก่อนพิมพ์ 2 แผ่น
- ขอบบน .page 12 → 4 mm (เครื่องพิมพ์พิมพ์ไม่ได้ ~2.5 mm ผู้ใช้วัดเอง → เผื่อ 3 mm) · body.measuring ตาม
- โลโก้ SVG ตัดขอบโปร่งใส (viewBox 11.5 18 510.5 253.5 · เทียบภาพแล้วตัวโลโก้ครบ) · กว้าง 250 → 232px (ตัวโลโก้ขนาดเท่าเดิม)
- เนื้อหาเลื่อนขึ้น ~13.2 mm (คำนวณจาก CSS) · รูปเลื่อนตาม: ข้าวเหนียว Y 186.8 · ปลาเผา Y 244.5 · เครื่องดื่ม Y 192.8 · หม้อหน้า 2 Y 1.9 (ติดเขต 3 mm)
- หม้อหน้า 1 ย่อพอดีส่วนหัว (ผู้ใช้เลือก): X 97.1 Y 1.6 W 45.8 H 35.7 (เดิม X85 Y2 W69.9 H54.5) · ส่วนที่มองเห็นสูง 33.1 mm เท่าหม้อหน้า 2
- lint ข้อ 34: padding .page = body.measuring · บน/ล่าง ≥ 3mm (ทดสอบแล้วจับได้ทั้ง 2 กรณี)

## 9 ต.ค. 2026 (07:30) — หมายเหตุกลุ่ม เพิ่ม/แก้/ลบได้ทุกกลุ่ม · ✅ commit แล้วใน 3fdc013 (08:32) (ต่อจาก a4d7d74)
- เดิม: "ที่ร้านไม่มีเหล้าขาย…" เป็น HTML ตายตัวใต้กลุ่มเครื่องดื่ม แก้ไม่ได้ · และพบบั๊กเพิ่ม: กด เพิ่มรายการ ในกลุ่มเครื่องดื่ม แถวใหม่ไปอยู่ใต้หมายเหตุ
- ใหม่: + หมายเหตุ / × ในโหมดแก้ข้อความ · Undo · ผูกกับกลุ่ม · แถบรูปแบบ (ประเภท "หมายเหตุกลุ่ม") · ≤80 ตัว ไม่ขึ้นบรรทัด · หน้าตาเริ่มต้นแบบเดิม · ว่าง = ไม่แสดง/ไม่พิมพ์
- แถวใหม่แทรกก่อนหมายเหตุ (_secRowsEnd) · ปุ่มตัดทิ้งตอน snapshot/บันทึก/ดาวน์โหลด/ทำซ้ำกลุ่ม/เพิ่มหน้า/พิมพ์/วัดล้นหน้า
- lint ข้อ 33 ใหม่ + ข้อ 17 / 29 ครอบคลุมหมายเหตุกลุ่ม · UI_STANDARD ข้อ 7 · ทดสอบตรรกะ 25/25 ผ่าน · ✅ ผู้ใช้ทดสอบในเบราว์เซอร์ 5 ขั้นตอนผ่าน (9 ต.ค. 07:59)

## 9 ต.ค. 2026 (00:55) — ชื่อเมนู "(กุ้งสด+กุ้งลวก)" → "(กุ้งสด + กุ้งลวก)" 4 รายการ หน้า 2 · ✅ commit แล้วใน a4d7d74 (07:18) (ต่อจาก ab8b09c)
- ตำกุ้งโลเล · ตำไทยข้าวโพด · ตำไหลบัวกุ้งโลเล · ยำกุ้งโลเล
- ข้อมูลจากผู้ใช้: เครื่องพิมพ์ของร้าน พิมพ์ไม่ได้ที่ขอบกระดาษ ~2.5 mm (วัดจากพิมพ์จริง) → ใช้ค่าเผื่อ 3 mm เป็นขอบที่พิมพ์ไม่ได้
- ข้อความใต้กลุ่มเครื่องดื่ม (.secnote) ตอนนี้: HTML ตายตัว ไม่มี JS รู้จัก → แก้ไม่ได้ · ลบกลุ่มแล้วหายไปด้วย · กำลังคุยเรื่องทำ "หมายเหตุกลุ่ม" เพิ่ม/แก้/ลบได้ทุกกลุ่ม

## 8 ต.ค. 2026 (23:00) — "เมนูข้าว & เส้น" สีเส้นขอบ #B9954A → #D79533 · ✅ commit แล้วใน ab8b09c
- 23:02 ผู้ใช้ตัดสิน: แถบด้านซ้ายของ "เมนูข้าว & เส้น" คงตามกฎเดิม (แถบ = สีตัวอักษรชื่อกลุ่ม) ไม่ต้องแก้เพิ่ม · rice_bar_mockup.html ใช้แล้ว
- แก้เฉพาะสีขอบ (data-ol-c + text-shadow 16 จุด) · ความหนา 2px · ตัวอักษรขาว · แถบหัวกลุ่ม (ยังขาว) ไม่แตะ — ผู้ใช้ยังไม่เลือกสีแถบจากหน้าเปรียบเทียบ
- ตัวขาวกับขอบ 2.55 : 1 · ขอบกับพื้นครีม 2.23 : 1 · #D79533 = สีประจำกลุ่ม "เมนูปลา"

## 8 ต.ค. 2026 (22:50) — ย้ายรูป: StickyRice X 152 → 162mm · Beverage17 Y 200 → 206mm · ✅ commit แล้วใน 5ced593
- 22:51 ผู้ใช้ขอดูหน้าเปรียบเทียบสีแถบ "เมนูข้าว & เส้น" ก่อนตัดสิน → C:\OE\rice_bar_mockup.html (ขาว / ทอง / เทา) · ยังไม่แก้ไฟล์เมนู
- แก้เฉพาะ left ของ StickyRice (หน้า 1) และ top ของ Beverage17 (หน้า 2) · ค่าอื่นและตัวรูปไม่เปลี่ยน · ยังไม่ทดสอบในเบราว์เซอร์

## 8 ต.ค. 2026 (22:40) — "เมนูข้าว & เส้น" ตัวอักษรสีขาว · ✅ commit แล้วใน 28afbdb
- ใส่แบบเดียวกับทาสีทั้งช่องในแอป: .sechead color #FFFFFF · แถบหัวกลุ่มตามกฎ 22:05 → --accent #FFFFFF · data-acc0 #666666 (คืนค่ากลับเป็นเทาได้) · เส้นขอบ #B9954A เดิมคงไว้ (สีขอบที่เลือกเองไม่เปลี่ยนตามสีตัวอักษร)
- ตัวขาวกับขอบทอง 2.81 : 1 · ตัวขาวกับพื้นครีม 1.14 : 1 (อ่านได้เพราะขอบ) · แถบสีขาวกับพื้นครีม 1.14 : 1 แทบมองไม่เห็น — แจ้งผู้ใช้ เสนอให้คงแถบเป็นเทา/ทอง

## 8 ต.ค. 2026 (22:35) — เปลี่ยนชื่อกลุ่ม: ข้าว & เส้น → เมนูข้าว & เส้น · เครื่องดื่ม → เมนูเครื่องดื่ม · ✅ commit แล้วใน 28afbdb
- ผู้ใช้เลือก "เปลี่ยนตามที่เสนอ" · แก้เฉพาะข้อความใน .sechead 2 ช่อง (เส้นขอบ / สี / data-ol-c เดิมคงไว้) · ชื่อเมนูและส่วนอื่นไม่แตะ
- ชื่อใหม่ยาวไม่เกินขีด 30 ตัวของชื่อกลุ่ม · ยังไม่ทดสอบในเบราว์เซอร์ว่าอยู่บรรทัดเดียวที่ 19px

## 8 ต.ค. 2026 (22:30) — เส้นขอบชื่อกลุ่ม 2px: ขาว #FFFFFF ทุกกลุ่ม · ข้าว & เส้น #B9954A · ✅ commit แล้วใน 28afbdb
- ผู้ใช้สั่ง · ใส่ตรงในไฟล์แบบเดียวกับปุ่ม A + ▾ เลือกสี (style text-shadow = _olShadow(สี,2) · data-ol-c = สีที่เลือกเอง) → ปุ่ม A เขียว · ▾ แสดง 2px + สีนั้น · คืนค่าล้างได้
- ขอบขาวกับพื้นครีม #F5EFE4 = 1.14 : 1 (ถ้าทำผ่านปุ่ม แอปจะเตือน fl.olWarnBg) · แจ้งผู้ใช้แล้ว
- ผู้ใช้ถามความเห็นเปลี่ยนชื่อ ข้าว & เส้น → เมนูข้าว & เส้น · เครื่องดื่ม → เมนูเครื่องดื่ม — ยังไม่เปลี่ยน รอผู้ใช้ตัดสิน

## 8 ต.ค. 2026 (22:15) — แถบสีหัวกลุ่มเปลี่ยนตามสีชื่อกลุ่มที่ทา · lint ข้อ 32 · ✅ commit แล้วใน 93b7d8f · ผู้ใช้ทดสอบผ่านครบ 4 ขั้น
- 22:18 รูปจากผู้ใช้ยังขึ้นป้าย "ล้นหน้า A4: หน้า 1, 2" (ชื่อกลุ่ม 19px · ชื่อเมนู 16px) — ยังไม่ได้แก้
- ผู้ใช้เลือก: แถบสีหัวกลุ่มเปลี่ยนตามสีที่ทา
- _secAccentFollow: ชื่อกลุ่มทั้งชื่อสีเดียว → .sec-h --accent = สีนั้น · หลายสี = ไม่เปลี่ยน · data-acc0 เก็บสีเดิม · _secAccentReset ในคืนค่า
- เรียกจาก: ทาทั้งช่อง · ทาแบบไฮไลท์ · ล้างรูปแบบจุดที่ไฮไลท์ · ใช้ทั้งประเภท (_typoApplyFormat) · กลุ่มใหม่ที่มีสีค่าเริ่มต้น (newSection)
- ทดสอบตรรกะ 13 กรณีผ่าน · lint ข้อ 32 (ก่อนแก้จับได้ · ลองลบจากใช้ทั้งประเภท จับได้) · ยังไม่ทดสอบในเบราว์เซอร์
- ข้อสังเกตแจ้งผู้ใช้: ทาชื่อกลุ่มเป็นสีขาว แถบจะเป็นสีขาวด้วย (แทบมองไม่เห็นบนการ์ดขาว)

## 8 ต.ค. 2026 (22:00) — ปรับตำแหน่ง/ขนาดรูปตามค่าที่ผู้ใช้ให้ · ✅ commit แล้วใน b015e2c
- StickyRice Y 192 → 200 · Plapao17 X 135.3 → 136.6, Y 247.4 → 257.7, W 37.6 → 31.8, H 18.3 → 15.9 · Beverage17 Y 192 → 200 · Jimjum3 / Jimjum5 ไม่เปลี่ยน
- แก้เฉพาะ style ของ 5 รูป (top/left/width/height เป็น mm) · ตัวรูป PNG ไม่เปลี่ยน · ยังไม่ทดสอบในเบราว์เซอร์

## 8 ต.ค. 2026 (21:45) — ชื่อเมนู 17px → 16px · ✅ commit แล้วใน 09c160f
- ผู้ใช้: 19/17 ล้น A4 หน้า 1, 2 (ป้ายแถบล่าง) · ถามว่าทำไมตอนลองเองไม่ล้น → ไฟล์ไม่มีช่องไหนตั้งขนาดเอง · กฎ CSS ใหม่ใช้กับชื่อเมนูทั้ง 115 ช่องและชื่อกลุ่ม 9 ช่อง = ผลเท่ากับใช้ปุ่มขนาด + ใช้ทั้งประเภท ทุกหน้า · ไม่รู้ว่าผู้ใช้ลองแบบไหน → ถามผู้ใช้
- รูปปลาเผา (Plapao17) ในรูปของผู้ใช้ทับข้อความ ข้าว & เส้น — รูปวางตาม mm บนหน้า ไม่เลื่อนตามข้อความที่ใหญ่ขึ้น
- ยังไม่ทดสอบในเบราว์เซอร์ว่า 16px พอดี A4 หรือไม่

## 8 ต.ค. 2026 (21:40) — สีชื่อกลุ่ม 9 สี · ลบรูปอาหารเดิม 12 รูป · ใส่รูปใหม่ 5 รูป · ✅ commit แล้วใน 09c160f
- 21:27:45 ไฟล์บนเครื่องถูกบันทึกใหม่หลัง commit โดยไม่ใช่ผม · เทียบกับ HEAD แล้วต่างแค่ --accent 9 ค่า = 9 สีที่ผู้ใช้สั่งตรงทุกค่า (หมู #B2304C · ไก่ #E98B73 · อื่นๆ #1592D9 · เนื้อ #A66C4E · ข้าว & เส้น #666666 · ปลา #D79533 · ตำ #D9531E · ยำ #5CB85C · เครื่องดื่ม #06A6C4) → ใช้ต่อ ไม่แก้ซ้ำ · แจ้งผู้ใช้แล้ว
- --accent ใช้ร่วมกันระหว่างสีชื่อกลุ่มกับแถบด้านซ้าย (border-left 5px) → แถบเปลี่ยนตามแล้ว · ข้อ "ทาสีชื่อกลุ่มแล้วแถบตาม" ผู้ใช้ยังไม่ตอบ (ยังไม่ทำ)
- ลบ .fimg 12 รูป (หน้า 1: 11 รวมหม้อหัวเมนู · หน้า 2: 1) · เก็บโลโก้ 2 + ป้ายปลาเผา
- ใส่ 5 รูปท้าย .page แบบ "เพิ่มรูป" · top/left/width/height เป็น mm ตามค่าที่ผู้ใช้ให้ (วัดจากขอบหน้าแบบตัวอ่านค่าในโหมดแก้รูป) · PNG เดิมไม่ย่อ · data-num 1–5
- สคริปต์และ <head> ไม่เปลี่ยน · ไฟล์ 5.97 MB → 4.05 MB · lint ผ่าน · ยังไม่ทดสอบในเบราว์เซอร์

## 8 ต.ค. 2026 (21:20) — ขนาดตัวอักษร: ชื่อกลุ่ม 19px · ชื่อเมนู 17px · ✅ commit แล้วใน 8fd5adf (รวมกับการเปลี่ยนชื่อ · git เห็นเป็น rename 99%) · ผู้ใช้ทดสอบผ่าน
- ผู้ใช้ถามความคืบหน้า 3 ครั้ง · ผมรอ commit เปลี่ยนชื่อโดยไม่จำเป็น (แก้เล็ก git ยังจับเปลี่ยนชื่อได้) → ทำทันที
- .sec-h .sechead font-size:19px (เดิม 17 จาก .sec-h · ไอคอนกลุ่ม .em 18px เท่าเดิม) · .nm font-size:17px (เดิม 15 จาก .row) · ราคา .pr 15px · "(ราคาตามไซส์)" .nm i 12.5px เท่าเดิม
- ไม่มีช่องไหนตั้งขนาดเองไว้ (inline) · ปุ่มคืนค่าจะกลับเป็น 19/17 · หน้าอาจล้น A4 — ต้องดูในเบราว์เซอร์
- ยังรอ: สีชื่อกลุ่ม 9 สี · ลบ/ใส่รูป (ทำหลัง commit เปลี่ยนชื่อ เพราะรูปเปลี่ยนเนื้อไฟล์มาก git จะไม่เห็นว่าเป็นการเปลี่ยนชื่อ)

## 8 ต.ค. 2026 (20:30) — เหลือไฟล์เมนูไฟล์เดียว: OEIsanHotpotMenuWithImageEditor.html → OEIsanHotpotMenuEditor.html · ✅ commit แล้วใน 0b89113 (ลบไฟล์เก่า) + 8fd5adf (เปลี่ยนชื่อ)
- ผู้ใช้สั่ง: ลบ OEIsanHotpotMenu.html, OEIsanHotpotMenuWithImage.html, OEIsanHotpotMenuEditor.html · เปลี่ยนชื่อไฟล์หลักเป็น OEIsanHotpotMenuEditor.html
- ก่อนแก้: OEIsanHotpotMenu.html และ OEIsanHotpotMenuEditor.html (ตัวเก่า) ไม่มีบนดิสก์แล้ว แต่ยังอยู่ใน git · ลบ OEIsanHotpotMenuWithImage.html (7.6 MB) จากดิสก์ · ทั้ง 3 ไฟล์ยังกู้ได้จากประวัติ git
- เปลี่ยนชื่อบนดิสก์ (เนื้อหาเดิมทุกไบต์ sha 99f861b8…) · แก้ชื่อใน lint_oe.py / verify_oe.py / README.md / STATUS_BAR_SPEC.md · บันทึกเก่าใน SESSION_STATUS ไม่แก้ (เป็นประวัติ)
- commit แยก 2 ครั้ง (ลบไฟล์เก่า → เปลี่ยนชื่อ) ให้ git เห็นเป็นการเปลี่ยนชื่อ ประวัติของไฟล์ editor ตามไปที่ชื่อใหม่ · แก้เนื้อหา (ขนาด สี รูป) ทำหลัง commit ทั้ง 2 ครั้ง

## 8 ต.ค. 2026 (20:05) — ปุ่ม A บอกสีขอบที่จะใช้ (แถบสีใต้ A + tooltip สี/ความหนา) · lint ข้อ 31 เพิ่ม 1 จุด · ✅ commit แล้วใน 28b189d · ผู้ใช้ทดสอบ 6 ขั้นที่เขียนใหม่ผ่าน (20:15)
- 20:10 ผู้ใช้แจ้ง: ขั้นทดสอบเดิมอ้างขอบเหลือง/เขียวจากรอบก่อน ซึ่งไม่ได้บันทึกลงไฟล์ (Ctrl+F5 = หายหมด) → เขียนใหม่ให้เริ่มจากหน้าที่เพิ่ง Ctrl+F5 · กฎ: ขั้นทดสอบต้องสร้างสถานะที่ใช้เองทุกครั้ง ห้ามอ้างผลรอบก่อน
- ผู้ใช้: กด A ที่ "ลาบหมู" แล้วจู่ๆ ได้สีเหลือง ไม่รู้ว่าสีมาจากไหน → ยอมรับว่าปุ่มไม่บอกผลก่อนกด (ขัด UI_STANDARD ข้อ 6)
- อ้างอิง Word: ปุ่มสีตัวอักษรแสดงสีล่าสุดที่เลือกใต้ตัว A
- ผู้ใช้เลือก: ช่องที่มีขอบ แถบ = สีขอบของช่องนั้น · ยังไม่มี = สีที่จะใส่
- #typoOlBar ใต้ A · tooltip ttl.olOnNextC/A · ttl.olOffNowC/A ({c} {w}) · ▾ ทำ .on ที่สี/ความหนาที่ A จะใช้ · ลบ ttl.outline (ไม่ใช้แล้ว)
- applyLang รองรับ data-i18n-args (tooltip ที่มีค่าแปลใหม่พร้อมค่า) — ใช้กับ _olTtl เท่านั้นตอนนี้
- ทดสอบตรรกะ 33 กรณี + แปลภาษา 2 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์ (หน้าตาแถบใต้ A ต้องดูในเบราว์เซอร์)

## 8 ต.ค. 2026 (19:40) — เลือกสีขอบเองได้ · ปุ่ม A ใช้ได้ทุกช่องข้อความ (ไม่ใส่ขอบที่มองไม่เห็น → เปิด ▾) · lint ข้อ 31 เพิ่ม 4 จุด · ✅ commit แล้วใน 1b9d5e3 · ผู้ใช้ทดสอบผ่านครบ 6 ขั้น
- ผู้ใช้: ไฮไลท์ "แจ่วฮ้อนหมู" ยังไม่ทาสีขาว ก็ควรกด A ได้ · ขอเปลี่ยนสีขอบได้ ไม่ใช่สีดำอย่างเดียว
- ผู้ใช้เลือก: กด A ที่ขอบอัตโนมัติจะกลืนกับพื้น = ไม่ใส่ขอบที่มองไม่เห็น · ใช้สีที่เลือกเองล่าสุดถ้ามี · ไม่งั้นเปิด ▾ ให้เลือกสี
- ข้อ 2 (จานสี) และข้อ 3 (คงสีที่เลือกเมื่อเปลี่ยนสีตัวอักษร) ผู้ใช้ไม่ได้ตอบ — ใช้ตัวเลือกที่แนะนำ แจ้งผู้ใช้แล้วว่าเปลี่ยนได้
- ▾: อัตโนมัติ + SWATCHES + สีที่กำหนดเอง (ร่วมกับสีตัวอักษร) + "+ กำหนดเอง" (_cpDlgOpen('edge') · ตกลง = typoOutlineSetColor) + ความหนา · data-ol-c ต่อช่อง · _olLastC
- ลบ ttl.outlineInvisible / fl.olInvisible · เพิ่ม 17 key TH/EN
- ทดสอบตรรกะ 24 กรณี (สีขอบ) + 46 กรณี (หน้าต่างสี เดิม 40 + โหมดสีขอบ 6) ผ่าน · ยังไม่ทดสอบในเบราว์เซอร์

## 8 ต.ค. 2026 (18:50) — แก้: ไฮไลท์แล้วทาสีขาว ปุ่มเส้นขอบยังจาง · lint ข้อ 31 เพิ่ม 3 จุด · ✅ commit แล้วใน 6f2b60e (รวมกับรอบ 18:30) · ผู้ใช้ทดสอบผ่าน
- ผู้ใช้ทดสอบรอบ 18:30: 5 ขั้นผ่าน ยกเว้นชื่อเมนู — ไฮไลท์ "แจ่วฮ้อนหมู" ทาสีขาวแล้วปุ่ม A ยังจาง ("ตัดกับพื้นชัดอยู่แล้ว")
- สาเหตุ: _olColorOf อ่านสีของช่อง แต่ทาสีแบบไฮไลท์ สีอยู่ใน span ข้างใน · applyColorRange (ทาแบบไฮไลท์) และ typoClearSel ไม่เรียก _olSync/_olRefresh
- แก้: สีที่เห็นจริง = สีที่มีจำนวนตัวอักษรมากที่สุด · ทาแบบไฮไลท์ / ล้างรูปแบบจุดที่ไฮไลท์ → _olRefresh + _olSync · ใช้ทั้งประเภท: _olRefresh ย้ายไปหลังทาสีบางคำ
- ขั้นทดสอบที่ผมเขียน ("ทาสีขาว") ไม่ได้บอกว่าไม่ต้องไฮไลท์ — แต่การไฮไลท์ทาสีต้องใช้ได้อยู่แล้ว จึงเป็นบั๊กจริง
- ทดสอบตรรกะ 8 กรณีใหม่ + 33 กรณีเดิมผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
- ผู้ใช้ขอเพิ่ม: เปลี่ยนสีขอบได้ ไม่ใช่สีดำอย่างเดียว — รอผู้ใช้เลือกแบบ (ยังไม่ทำ)

## 8 ต.ค. 2026 (18:30) — เส้นขอบได้ทุกช่อง (รวมดอกจัน) + เลือกความหนา 0.5–3px · ✅ commit แล้วใน 6f2b60e · ผู้ใช้ทดสอบผ่าน
- ผู้ใช้ถาม: ทำไมไม่ทำเส้นขอบได้ทุกข้อความ · ยอมรับว่าเหตุผลเดิม ("ตัวเล็ก ขอบ 2px กินตัวอักษร") เป็นการเดา · ทำหน้าเปรียบเทียบ C:\OE\text_outline_allfields_mockup.html (8 ช่อง × 6 แบบ)
- จากรูปผู้ใช้: ขอบ 2px ทำให้ตัวบาง/เล็กบวม · ดอกจันเป็นก้อน · ตัวเข้มบนพื้นขาว + ขอบอัตโนมัติ (ขาว) มองไม่เห็น (1.00 : 1)
- ผู้ใช้เลือก: ทุกช่อง (รวมดอกจัน) · ความหนาเป็นขั้นตายตัว
- A = เปิด/ปิด (ความหนาล่าสุด · ครั้งแรก: ตัวหนา ≥15px 2px · นอกนั้น 1px) · ▾ #typoOlCaret + #typoOlPop = 0.5/1/1.5/2/2.5/3 · _olState: ไม่มีช่อง / เส้นจุด / ขอบกลืนกับพื้น (_olBgOf < 1.5) = จาง + เหตุผล
- ลบ fl.olOn / fl.olOnWeak / fl.olOnlyGroup (ประวัติเก่าแสดงข้อความที่เก็บไว้) · เพิ่ม fl.olOnW / fl.olWidth / fl.olSame / fl.olNeed / fl.olLine / fl.olInvisible
- lint ข้อ 31 ปรับ (เดิมบังคับเฉพาะ sechead) · ข้อ 21 + typoOlCaret · ทดสอบตรรกะ 33 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
- เจอเพิ่ม (ยังไม่แก้ · มีมาก่อน): หลัง Ctrl+Z ช่องที่เลือกค้างชี้ช่องเก่าที่ถูกแทนแล้ว (_restorePages สร้างหน้าใหม่) → ปุ่มแถบจัดรูปแบบอาจแก้ช่องที่ไม่อยู่ในหน้าแล้วแต่บอกว่าสำเร็จ จนกว่าจะคลิกช่องใหม่ · ปุ่มเส้นขอบเช็คแล้ว (จาง)

## 8 ต.ค. 2026 (15:30) — เส้นขอบตัวอักษรสำหรับชื่อกลุ่มเมนู (แบบ 2 · ขอบ 2px · สีขอบอัตโนมัติ) · lint ข้อ 31 · ✅ commit แล้วใน 3851b39 · ผู้ใช้ทดสอบข้อ 1–3 ผ่าน (ข้อพิมพ์ข้ามไปก่อน)
- ผู้ใช้: "ข้าว & เส้น" ใช้สีขาวแล้วไม่ตัดกับพื้น · ทำหน้าเปรียบเทียบ C:\OE\text_effect_mockup.html (7 แบบ) · ผู้ใช้เลือกแบบ 2 เส้นขอบหนา
- ผู้ใช้: ขอบดำบนตัวสีส้ม/ฟ้าไม่สวย → อธิบายว่าขอบช่วยเฉพาะตัวอักษรสีอ่อน · ผู้ใช้เลือก: ตัวเลือกในแอป ใส่ทีละช่อง · เฉพาะชื่อกลุ่มเมนู
- ปุ่ม #typoOutline (ตัว A ขาวขอบเข้ม) หลังปุ่ม S · typoOutlineToggle / _olSync / _olRefresh / _olEdge · ใช้ทั้งประเภท คืนค่า ตั้งค่าเริ่มต้น ทาสีทั้งช่อง รองรับ
- ทดสอบตรรกะ 18 กรณีผ่าน · lint ข้อ 31 (ลองลบ _olRefresh จากการทาสี → จับได้) · ยังไม่ทดสอบในเบราว์เซอร์ · ผลพิมพ์ของเส้นขอบยังไม่รู้ (ผู้ใช้ต้องลองพิมพ์)
- ยังไม่ได้ใส่เส้นขอบให้ "ข้าว & เส้น" — ผู้ใช้กดเองในแอป

## 8 ต.ค. 2026 (14:40) — หน้าต่างสีที่กำหนดเองของแอป (HEX หลัก · ใหม่/เดิม · ตกลง/ยกเลิก) · lint ข้อ 30 · ✅ commit แล้วใน b0a18cd · ผู้ใช้ทดสอบผ่าน
- ผู้ใช้: เลือกสี custom แล้วไม่รู้ว่าสีไปไหน · อยากให้ขึ้น HEX เป็นหลัก · มีตกลง/ยกเลิก · ถามว่าโปรแกรมระดับ Professional ทำอย่างไร
- ตัวเลือกสีของ Chrome ตั้งให้ขึ้น HEX ไม่ได้และเพิ่มปุ่มไม่ได้ → สร้างหน้าต่างของแอป (#typoCpDlg) แบบ Word "สีเพิ่มเติม" / Photoshop
- ผู้ใช้เลือก: ตกลง = ทาสีและเก็บสี (แบบ Word) · ระหว่างเลือกดูในหน้าต่างเท่านั้น (เมนูไม่เปลี่ยน)
- ลบ listener input/change ของ #typoColor และ _cpLiveRes (เดิมทาสีทุกครั้งที่ลาก → span ซ้อนกัน) · #typoColor เหลือเป็นที่เก็บสีปัจจุบัน
- ปิดหน้าต่างเมื่อ: ยกเลิก · Esc · คลิกนอก · typoClear (ไม่มีช่องที่เลือก) · Save Editor ตัดสถานะเปิดออก
- ttl.cpAdd เดิม "เลือกสีเองแล้วบันทึก" (ไม่ตรงกับที่ทำ + ใช้คำ บันทึก) → "เลือกสีเอง (รหัส HEX) · กดตกลงเพื่อทาสีและเก็บสีไว้"
- lint ข้อ 30 (ก่อนแก้จับได้ 7) · ข้อ 16 + typoCpDlgHex · ข้อ 21 + typoCpDlgCancel/typoCpDlgEye · ทดสอบตรรกะ 40 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์ (หน้าตา/การลาก/ดูดสี ต้องดูในเบราว์เซอร์)

## 8 ต.ค. 2026 (13:15) — ซ่อนรูประหว่างแก้รูปได้ (แก้ป้าย/โลโก้โดยรูปอาหารไม่บัง) · เพิ่มรูปตอนซ่อน = แสดงกลับ · ✅ commit แล้วใน f30d5cd · ผู้ใช้ทดสอบผ่านทุกขั้น
- ผู้ใช้: จะแก้ป้าย แต่กดซ่อนรูปแล้วออกจากโหมดแก้รูป ปุ่มป้ายหาย · บางรูปบังป้าย
- ผู้ใช้เลือก: เข้าแก้รูปตอนซ่อน = คงซ่อน · เพิ่มรูปตอนซ่อน = แสดงกลับแล้ววางรูปใหม่
- toggleImgHide ไม่ออกจากโหมดแก้รูปแล้ว · toggleImgMode ไม่แสดงรูปกลับ · รูปที่ซ่อน pointer-events:none · ยกเลิกรูปที่เลือก · ข้อความโหมด img.clickEditHidden · fl.imgHiddenEdit
- imgAdd: ใช้ _readImageFile (ตรวจชนิดไฟล์ — ปิดเรื่องค้าง "เพิ่มรูปไม่ตรวจชนิดไฟล์") · แสดงรูปกลับ · ผล fl.imgAdd / fl.imgAddShown (เดิมไม่มีผล) · ยังไม่ย่อรูปใหญ่
- UI_STANDARD ข้อ 7 แก้กฎ 5 ต.ค. · ทดสอบตรรกะ 16 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
- เจอเพิ่ม (ยังไม่แก้): ออกจากโหมดแก้รูป แถบล่างค้างข้อความ "คลิกรูป…" (_imgReadout(null) เรียกหลัง setStatus พร้อมใช้งาน)

## 8 ต.ค. 2026 (13:00) — ช่องขนาดตัวอักษรพิมพ์ตัวเลข 8–72 ได้ · ✅ commit แล้วใน 84813e7 (รวมกับรอบ 12:45) · ผู้ใช้ทดสอบผ่าน
- ผู้ใช้: ช่องขนาดตัวอักษรควรพิมพ์ตัวเลขในขอบเขตได้เลย (เดิม readonly)
- เอา readonly ออก · ตัวกรอง _sizeClean · Enter/Tab ใช้ · Esc/ออกจากช่อง = กลับค่าจริง · นอกช่วงเตือน · เลขเดิมบอกไม่ได้เปลี่ยน · แถบเครื่องมือยอมให้ช่องนี้รับโฟกัส (เหมือนช่อง HEX)
- typoSizeStep กับช่องพิมพ์ใช้ _typoSizeApply เดียวกัน · _typoCurSize ใช้ใน typoSelect ด้วย (ค่าเดียวกับเดิม)
- lint ข้อ 16 เพิ่ม typoSize ในรายการที่มีตัวกรอง · ทดสอบตรรกะ 30 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์

## 8 ต.ค. 2026 (12:45) — ครั้งแรกที่ล้นหน้า: ผล + คำเตือนเต็มพร้อมกัน · lint ข้อ 28b · ✅ commit แล้วใน 84813e7 · ผู้ใช้ทดสอบผ่าน
- ผู้ใช้เลือก: เห็นผลกับคำเตือนเต็มพร้อมกัน ครั้งแรกที่ล้น
- flashStatus รวมผลกับ st.overflowNew เมื่อ _ovfFresh · checkOverflow รวมกับผลที่เพิ่งแสดงใน tick นี้ (_lastFlash) · รูปโหลดเสร็จหลังผล (_imgSetSrc onload) รวมได้ถ้าผลยังแสดงอยู่
- ป้ายไม่ซ้ำเมื่อข้อความบอกล้นอยู่แล้ว · ล้นโดยไม่มีผล = คำอธิบายเต็ม จด 1 รายการ (เดิมคำเตือนล้นไม่ถูกจดเลย)
- ทดสอบตรรกะ 17 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์

## 8 ต.ค. 2026 (12:20) — ✅ ปิดแล้ว · ผลทดสอบรอบป้ายกลุ่ม/โลโก้ + พบช่องโหว่ของรอบ 11:30
- ผู้ใช้ทดสอบป้ายกลุ่ม/โลโก้ 7 ขั้นผ่าน (ลบ · Ctrl+Z · เปลี่ยน · + ป้าย · เปลี่ยนโลโก้หน้า 1 · Ctrl+Z · ซ่อนรูปแล้วป้าย/โลโก้ยังอยู่)
- รูปทดสอบ +/− 72px: แถบเหลืองคำอธิบายเต็ม ไม่มีป้ายล้นหน้า = พฤติกรรมโค้ดเก่า (ก่อน 11:30) → แท็บนั้นยังไม่ได้ Ctrl+F5
- ช่องโหว่ที่พบจากการอ่านโค้ด: ปุ่มส่วนใหญ่เรียก checkOverflow ก่อน flashStatus → ผลของปุ่มทับคำอธิบายเต็มทันที · คำอธิบายเต็มเหลือแค่ใน tooltip ของป้าย · ขั้นทดสอบรอบ 11:30 ที่เขียนว่า "แถบล่างเตือนว่าล้น" ไม่ตรงกับโค้ด
- รอผู้ใช้เลือกวิธีแก้

## 8 ต.ค. 2026 (12:10) — ป้ายประจำกลุ่ม (ป้ายปลาเผา) แบบโลโก้ · เปลี่ยนโลโก้มี Undo + ผล · lint ข้อ 29 · ✅ commit แล้วใน 704aea6 (รวมกับรอบ 11:30)
- ผู้ใช้เลือก: ป้ายปลาเผา = ป้ายประจำกลุ่มแบบโลโก้ · แก้เปลี่ยนโลโก้ให้มี Undo และข้อความผลไปพร้อมกัน
- ป้าย: โหมดแก้รูป คลิกป้าย = เปลี่ยน · × = ลบ · + ป้าย = ใส่ให้กลุ่มอื่น · ไม่ถูกซ่อนด้วยปุ่มซ่อนรูป · ย่อรูปสูงเกิน 240px
- โลโก้: เดิมไม่มี Undo / ไม่ขึ้นยังไม่บันทึก / ไม่มีผล → มีครบ · ตรวจว่าเป็นไฟล์รูป · รูปเดิม = บอกว่าไม่ได้เปลี่ยน
- Save Menu ตัด class imgmode/headermode ด้วย (กันชั้นที่ 2 — แท็บไฟล์ออกจากโหมดอยู่แล้ว)
- ทดสอบตรรกะ 22 กรณีผ่าน · ส่วนย่อรูป (canvas) ทดสอบได้เฉพาะในเบราว์เซอร์ · ยังไม่ทดสอบในเบราว์เซอร์
- เจอเพิ่ม (ยังไม่แก้): ลบรูปอาหาร (×) ไม่มีข้อความผล · เพิ่มรูปอาหารไม่ตรวจชนิดไฟล์และไม่ย่อรูป

## 8 ต.ค. 2026 (11:30) — ตัวตรวจล้นหน้าวัดแบบไม่มีโหมดแก้ · ผลไม่หายตอนล้นหน้า (ป้ายในแถบล่าง) · lint ข้อ 28 · ✅ commit แล้วใน 704aea6
- ผู้ใช้: ตอนแก้ ระยะห่างเพิ่ม เนื้อหาเบียดตกหน้า แต่ออกจากโหมดแก้อาจไม่ล้น · เลือกแก้ "ผลหายตอนหน้าล้น"
- ยืนยันจาก CSS: body.editmode/headermode [data-edit] padding 1px 4px (ติดต่อ/หมายเหตุ) · .sechead padding 0 4px · .em padding 0 2px · .pr ว่าง min-width 3em min-height 1.15em — body.measuring ซ่อนแค่ปุ่ม ไม่ได้เอาระยะเหล่านี้ออก
- checkOverflow: เอา class 4 โหมดออกระหว่างวัด ใส่คืนใน finally (ใน tick เดียว ยังไม่ paint) · เก็บ _overflowPages
- flashStatus / setStatus / _statusHint / _actlogDoClear: ไม่หยุดเพราะ _overflowWarn แล้ว · _renderStatus ใส่ป้าย st.overflowPill (.edstatus-meta.ovf) ทุกข้อความตอนล้น · คำอธิบายเต็มเฉพาะเพิ่งล้น/หน้าเปลี่ยน
- lint ข้อ 28 (ก่อนแก้จับได้ 8) · ทดสอบตรรกะ 15 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์ (ผลการวัดจริงต้องดูในเบราว์เซอร์)
- รอบ 10:45 (ตัดขนาดบางคำ) ผู้ใช้ทดสอบผ่าน commit 00abe9f · ปุ่ม +/− ทีละคลิกเป็นแบบเดิม (ขั้นตอนทดสอบที่เขียนว่ากดค้างผิด) · ยังรอผู้ใช้ตอบว่าจะให้กดค้างได้ไหม

## 8 ต.ค. 2026 (10:45) — ตัดขนาดตัวอักษรบางคำออก · ไฮไลท์ + กด +/− = เปลี่ยนทั้งช่อง · lint ข้อ 27 · ✅ commit แล้วใน 00abe9f (ต่อจาก 719d3f5)
- ผู้ใช้ถามว่า "ตัดขนาดตัวอักษรบางคำออก" คืออะไร → อธิบาย → เลือก "เปลี่ยนทั้งช่อง"
- เดิม: ไฮไลท์ + กด +/− = applyFontSizePx (span font-size) ไม่มี Undo ไม่ markDirty ไม่มีข้อความ — ทั้งที่ตกลงตัดออก 28 ก.ย.
- typoSizeStep: ทั้งช่องเสมอ · ล้าง font-size/line-height ของ span ที่ไม่ใช่โครงสร้าง (_clrIsStruct) · markDirty · ข้อความ fl.sizeCell / fl.sizeCellHl (ตอนไฮไลท์) · ถึง 8/72 = fl.sizeLimit ไม่สร้างจุด Undo · เดิมไม่มีข้อความผลเลย
- ลบ applyFontSizePx (ผู้เรียกมีที่เดียว) · _typoCaptureFormat ไม่เก็บ fontSize ใน runs
- lint: _PENDING21B ว่าง (warning ขนาดบางคำหาย) · lint ข้อ 27 (ก่อนแก้จับได้ 2) · ทดสอบตรรกะ 9 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
- ในเมนูตอนนี้ไม่มีคำที่ถูกเปลี่ยนขนาดบางคำค้างอยู่ (นับจากไฟล์ = 0)

## 8 ต.ค. 2026 (10:10) — ประวัติเปลี่ยนภาษาตาม TH/EN (แบบ Windows Event Viewer) · lint ข้อ 26 · ✅ commit แล้วใน 719d3f5 · ผู้ใช้ทดสอบผ่าน (ต่อจาก 23fc144)
- ผู้ใช้เลือก (8 ต.ค.): ประวัติเปลี่ยนภาษาตาม TH/EN · เดิมเก็บข้อความสำเร็จรูป → สลับภาษาแล้วประวัติปน 2 ภาษา
- logAdd เก็บ e.m = _ttSer(tk/tkj) + e.msg สำรอง · _actlogText(e) แปลตอนแสดง (ถ้า key ทุกตัวยังมีใน I18N.th) · applyLang → _actlogRelang (ข้ามถ้า ACTLOG ยัง undefined ตอน applyLang ครั้งแรก)
- แก้ทางที่ทำให้เสีย key: _logFromFlash String(msg) · _actlogDoClear String(m) · _actlogFieldType t() → tk() · ข้อความแก้เมนู log.edited/editedNew/editedClear t() → tk()
- แถว / CSV ใช้ _actlogText · JSON: msg (ภาษาปัจจุบัน) + key + args
- รายการเก่า (ก่อนรอบนี้) ไม่มี key = ภาษาเดิม · key ที่ถูกลบแล้ว (เช่น fl.colorRange) = ข้อความเดิม
- lint ข้อ 26 (ก่อนแก้จับได้ 5 · หลังแก้ 0) · ทดสอบตรรกะ 18 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
- รอบ 18:10 (เส้นคั่น) ผู้ใช้ทดสอบผ่าน commit 23fc144

## 7 ต.ค. 2026 (18:10) — เส้นคั่นกลุ่มในแถบเครื่องมือชัดขึ้น · ไม่จางตอนกลุ่มปิด · lint ข้อ 25 · ✅ commit แล้วใน 23fc144 (ต่อจาก 4520e33)
- ผู้ใช้: เส้นคั่นจางมาก ตอนกลุ่มปิดแยกกลุ่มไม่ออก (แท็บ รูป และ ข้อความ)
- สาเหตุ 1: สี #eaeaea บนพื้น #faf9f8 = 1.14:1 · สาเหตุ 2: กลุ่มที่ปิดใช้ opacity:.45 ที่ตัว .rgroup ซึ่งเป็นเจ้าของเส้นคั่น → เส้นจางตามเหลือ 1.06:1
- แก้: เส้นคั่น #b3b0ad (2.05:1) · opacity ย้ายไป .rgroup>* (pointer-events:none ยังอยู่ที่ .rgroup) · ลบ border-right ของ #edbar .rgroup ที่ถูกทับอยู่ (ทุก .rgroup อยู่ใน #edribbon)
- lint ข้อ 25 · ลองกับไฟล์ก่อนแก้ จับได้ 3 · ยังไม่ทดสอบในเบราว์เซอร์ (agent ดูหน้าจอจริงไม่ได้)
- ผู้ใช้ทดสอบรอบ 18:00 ผ่าน (หน้าต่าง Save มี JSON + CSV (Excel) ไม่มี All Files)

## 7 ต.ค. 2026 (18:00) — บันทึกแล้วล้าง เลือก JSON/CSV ได้ · เขียนตามนามสกุลจริง · หน้าต่าง Save ทุกอันไม่มี All Files · lint ข้อ 24 · ✅ commit แล้วใน 4520e33 (17:59) (ต่อจาก c8d563e)
- ผู้ใช้ถาม: หน้าต่าง Save ของบันทึกแล้วล้าง เลือกได้ทั้ง JSON และ CSV ได้ไหม และบันทึกได้จริงตามที่เลือก → ตกลง: เลือกได้ในหน้าต่าง Save + เอา All Files ออกทุกปุ่ม
- ข้อจำกัด: หน้าเว็บไม่รู้ว่าเลือก Save as type อันไหน → _saveAs(fname, types) สร้างเนื้อหาหลังได้ชื่อ แล้วเลือกตามนามสกุลจริง (ไม่สนตัวพิมพ์เล็ก/ใหญ่ · ดูนามสกุลสุดท้าย)
- เดิม: เนื้อหาสร้างก่อนเปิดหน้าต่าง → ตั้งชื่อ .csv ได้ไฟล์ JSON · มี All Files ทุกหน้าต่าง (Chrome ใส่ให้)
- excludeAcceptAllOption:true ทั้ง 3 จุด (_saveAs · downloadMenu · saveEditorFile) — ยืนยันจาก MDN showSaveFilePicker
- นามสกุลผิด: ประวัติ = fl.saveBadExt / fl.logSaveClearBadExt (ไม่ล้าง) · Save Menu/Editor ตรวจ .html/.htm (fl.saveBadExt)
- ข้อความผลบอกชนิด: fl.logSavedCleared / Dl มี {fmt} · pnl.clearLogMsg บอกว่าเลือกชนิดในหน้าต่าง Save
- lint ข้อ 24 (ไม่มี excludeAcceptAllOption / เขียนโดยไม่ตรวจนามสกุล) · ก่อนแก้จับได้ 6 · หลังแก้ 0 · ลบการตรวจนามสกุลออก 1 จุด = จับได้
- ทดสอบตรรกะ 15 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
- ยังไม่รู้ (ต้องทดสอบในเครื่องจริง): 1) Windows เปลี่ยนนามสกุลในช่อง File name ให้เองไหมตอนเปลี่ยน Save as type 2) ตั้งนามสกุลผิดแล้วกด Save — Chrome สร้างไฟล์เปล่าค้างไว้ไหม (แอปไม่ลบให้ เพราะอาจเป็นไฟล์เดิมที่ผู้ใช้เลือกทับ)

## 7 ต.ค. 2026 (17:40) — panel ล้างประวัติ แบบ Windows: บันทึกแล้วล้าง / ล้างประวัติ / ยกเลิก · ✅ commit แล้วใน c8d563e (17:48) (รวมรอบ 16:15 สี + 16:50 ประวัติ · ต่อจาก c93259d)
- ผู้ใช้ถามว่า Professional/Enterprise ทำอย่างไร → Windows Event Viewer: Clear Log มี Save and Clear / Clear / Cancel · ผู้ใช้: ใช้ Save and Clear ข้างปุ่ม Clear
- ปุ่มหลัก (Enter) pnl.clearLogSave "บันทึกแล้วล้าง"/"Save and Clear": _actlogSaveAndClear → _saveAs JSON → picked/download = ล้าง (fl.logSavedCleared / fl.logSavedClearedDl) · cancel = ไม่ล้าง panel ยังเปิด (fl.logSaveClearCancel) · error = ไม่ล้าง (fl.logSaveClearFail) · keepOpen + _alSaving กันกดซ้ำ
- ปุ่มรอง .ep-clearonly ใช้ pnl.clearLogOk "ล้างประวัติ"/EN เปลี่ยนเป็น "Clear" · ลบปุ่ม "ส่งออกเป็น JSON" ในข้อความ + key pnl.clearLogExport · 1 การกระทำ = 1 ข้อความผล (_actlogDoClear)
- ทางสำรอง (เบราว์เซอร์ไม่มีหน้าต่าง Save) = ดาวน์โหลดแล้วล้าง — ยืนยันไม่ได้ว่าไฟล์ดาวน์โหลดสำเร็จ (ข้อจำกัดของเบราว์เซอร์)
- lint ข้อ 23 ยกเว้นวลี "บันทึกแล้วล้าง" (ยังจับคำว่าบันทึกที่หมายถึง log ได้) · ทดสอบตรรกะ 18 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
- ค้าง: ผู้ใช้ยังไม่ตอบเรื่องประวัติเปลี่ยนภาษาตาม TH/EN (แบบ Windows เก็บ key + ค่า)

## 7 ต.ค. 2026 (17:00) — ปุ่มใน panel ล้าง: "ส่งออกเป็น JSON" / "Export to JSON" · แทนที่ด้วยรอบ 17:40 (✅ commit แล้วใน c8d563e) (รวมรอบ 16:15 + 16:50 · ต่อจาก c93259d)
- ผู้ใช้ทดสอบรอบ 16:50 ผ่าน (หัวหน้าต่าง ประวัติการทำงาน · panel ล้างประวัติ · EN Activity Log) แล้วขอเปลี่ยนปุ่มเป็น "ส่งออกเป็น JSON" · ถาม Save to JSON หรือ Export to JSON → Export (Save = ปุ่ม Save Menu/Editor)
- pnl.clearLogExport TH/EN เปลี่ยน 1 key · ไม่มีข้อความเริ่มต้นใน HTML (JS ใส่ตอนเปิด panel)

## 7 ต.ค. 2026 (16:50) — "บันทึก" (log) → "ประวัติ" · ปุ่ม "ส่งออกเก็บไว้ก่อน (JSON)" · lint ข้อ 23 · ✅ commit แล้วใน c8d563e (รวมกับรอบ 16:15 · ต่อจาก c93259d)
- ผู้ใช้: "ล้างบันทึก" งง · ถามว่า "ล้างล็อก" ดีไหม / "ส่งออก JSON ก่อน" ใช่ไหม / "บันทึกไฟล์ JSON" ดีไหม
- เหตุผล: "บันทึก" ในแอปเป็นกริยา Save อยู่แล้ว · "ล็อก" ชนกับ lock · "บันทึกไฟล์ JSON" ซ้อนกับชื่อหน้าต่าง → ผู้ใช้เลือก ประวัติการทำงาน / ล้างประวัติ + ส่งออกเก็บไว้ก่อน (JSON)
- เปลี่ยน 16 key ภาษาไทย (log.* · pnl.clearLog* · fl.log* · ttl.closeLog) + ข้อความเริ่มต้นใน HTML 5 จุด · EN เปลี่ยน 1 key (pnl.clearLogExport → Export a copy first (JSON)) · ข้อความ Save 10 key ไม่แตะ
- ไม่ได้ยืนยันคำแปลไทยของ Microsoft (ค้นแล้วไม่พบหน้าที่ยืนยันได้) — เลือกจากการเลี่ยงคำชนในแอปนี้
- lint ข้อ 23: ข้อความไทยของ key ประวัติห้ามมี "บันทึก" (ลองกับไฟล์ก่อนแก้ จับได้ 15) · ยังไม่ทดสอบในเบราว์เซอร์
- รอบ 16:15 (สี) ผู้ใช้ทดสอบผ่านแล้ว แต่ commit ไม่สำเร็จ (รันที่ C:\Users\pjenkarn ไม่ใช่ C:\OE)

## 7 ต.ค. 2026 (16:15) — เปลี่ยนสี 1 ครั้ง = 1 รายการ · ข้อความบอกตามจริง · ตัวเลือกสีจดตอนปิด · ทาสีส่วนที่ไฮไลท์มี Undo · lint ข้อ 21b · ✅ commit แล้วใน c8d563e (ต่อจาก c93259d)
- ผู้ใช้ถาม "สีจดซ้ำ 2 รายการ คืออะไร" → อธิบายตารางทุกทาง → ตกลงทำ 4 ข้อ
- เดิม: ปุ่มทาสี / Enter รหัสสี = จด 2 รายการเหมือนกัน · ตัวเลือกสีระบบ = 2 รายการ (paintRange + colorRange) และยิงทุกครั้งที่ลาก · สีในตาราง/ปุ่มสีปัจจุบันตอนไม่มีไฮไลท์ = ไม่มีข้อความเลย · ทั้งช่องแต่ข้อความเขียน "ช่วงที่เลือก" · ทาสีส่วนที่ไฮไลท์ไม่ markDirty
- แก้: applyColorRange(hex,quiet) แจ้งผลที่เดียว คืนข้อความ · ลบ flashStatus ซ้ำที่ typoHex Enter / typoCpPaint / typoColor input · input = quiet + จำ _cpLiveRes → change แจ้ง 1 ครั้ง · ทางมีไฮไลท์เพิ่ม markDirty+checkOverflow
- ข้อความ: fl.paintRange "✓ ทาสี {c} ที่ "{txt}" ใน{label} "{cell}" แล้ว" · fl.colorCell ใหม่ "✓ เปลี่ยนสี{label} "{cell}" เป็น {c} แล้ว" · ลบ fl.colorRange · สีเป็นตัวใหญ่
- lint ข้อ 21b: หลัง insertNode ต้องมี markDirty/_snapNow ก่อน return/ท้ายฟังก์ชัน · _HELPER21B: _typoWrapRange (typoApplyAllSame markDirty) · _PENDING21B: applyFontSizePx = เตือน ไม่บล็อก · ลองกับไฟล์ก่อนแก้ จับ applyColorRange ได้
- ทดสอบตรรกะ 14 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์ · ยังไม่รู้ว่า Chrome ยิง change ตอนปิดตัวเลือกสีทุกกรณี (เช่น กด Esc)
- พบ (ยังไม่แก้): 1) เส้นจุด: กดสีแล้วไม่เปลี่ยน ไม่มีข้อความ (applyColorRange ข้ามเส้นจุด · typoColorApply ที่ทำสีเส้นจุดไม่มีใครเรียก) 2) ขนาดตัวอักษรบางคำยังทำงาน (typoSizeStep → applyFontSizePx) ทั้งที่ตัดสินใจตัดออก 28 ก.ย. และไม่มี Undo 3) ช่องฟอนต์ผูก change 2 ทาง (onchange=typoFontApply + addEventListener) = ทำ 2 รอบ 4) ทาสีซ้ำบนส่วนเดิม span ซ้อนกันเพิ่มทุกครั้ง (ลากในตัวเลือกสี = ซ้อนหลายชั้น)

## 7 ต.ค. 2026 (13:50) — ผลการกระทำไม่ถูก "เลือกอยู่" ทับ · "เลือกอยู่" ไม่จดบันทึก · ผลล้างรูปแบบบอกรายละเอียด · lint ข้อ 22 · ✅ commit แล้วใน c93259d (14:03) · ผู้ใช้ทดสอบผ่าน (ผลล้างรูปแบบค้างอยู่ ไม่ถูกทับ) (ต่อจาก e108d13)
- ผู้ใช้ทดสอบ (12:47–13:09): กดล้างรูปแบบจุดที่ไฮไลท์ → ผลถูกจดจริง (ACTLOG ยืนยัน 13:00:13.721) แต่ "เลือกอยู่: แจ่ว" ตามมา 5ms ทับทั้งแถบล่างและแถวบนสุดของบันทึก → ผู้ใช้เห็นว่าไม่ทำงาน · ผู้ใช้: "ไม่เมคเซนส์" → ตกลงทำ 4 ข้อ
- สาเหตุ: clearFormatSel (และทาสี/ฟอนต์) ไฮไลท์คำเดิมคืน → selectionchange → syncButtons → flashStatus(fl.selInfo) = ทั้งทับผลและจดบันทึก · ลากไฮไลท์ 1 ครั้ง = "เลือกอยู่" 3 แถว
- แก้: flashStatus จำ selection ตอนแจ้งผล (_selHold) · "เลือกอยู่" ผ่าน _statusHint() (แสดงอย่างเดียว ไม่จดบันทึก · ไม่แสดงขณะ selection = อันเดิม) · syncButtons เรียก _selHoldTouch() ทุกครั้ง → ผู้ใช้คลิก/ลาก/พิมพ์ = ปลด
- fl.clearedRange บอกรายละเอียด: ✓ ล้างรูปแบบ "{txt}" ใน{label} "{cell}" แล้ว (อ่านก่อนล้าง · _cut30 ตัด 30 ตัว + รวมช่องว่าง)
- lint ข้อ 22 · UI_STANDARD ข้อ 6 · ทดสอบตรรกะ 10 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
- พบ (ยังไม่แก้): B/I/U/S ไม่มีข้อความผลเลย (แถบล่างขึ้นแค่ "เลือกอยู่") · เปลี่ยนสีด้วยตัวเลือกสีมีช่วงไฮไลท์ = จดบันทึก 2 รายการ (fl.paintRange + fl.colorRange) · ระหว่างมีคำเตือนหน้าล้นค้าง flashStatus ไม่แสดงและไม่จดบันทึกผลใดๆ

## 7 ต.ค. 2026 (12:30) — "ล้างรูปแบบจุดที่ไฮไลท์" กดได้เฉพาะตอนไฮไลท์ · ✅ commit แล้วใน e108d13 (12:47) (ต่อจาก 0229a02 · รวมรอบ 11:40 + 12:15)
- ผู้ใช้เลือก: ใช้ชื่อ "ล้างรูปแบบจุดที่ไฮไลท์" ต่อ + ปุ่มกดได้เฉพาะตอนไฮไลท์ (แนะนำ)
- _clearSelSync(): กดได้เมื่อ มีช่องที่เลือก + ไม่ใช่เส้นจุด + อยู่โหมดแก้ข้อความ + _hlLive() (ช่วงไม่ว่าง อยู่ในช่องที่ยังอยู่ในหน้า — หลัง Undo ช่องเก่าถูกแทน)
- เรียกจาก: typoSelect (แทนการเปิดปุ่มตรงๆ) · typoClear · selectionchange (listener ใหม่ ลงทะเบียนหลังตัวที่ saveSelection) · คลิกนอกช่อง (savedRange=null)
- tooltip ตอนจาง = ttl.clearSelNeed "ไฮไลท์ข้อความก่อน — ลากคลุมส่วนที่จะล้างรูปแบบ" (EN มี) · ตอนกดได้ = ttl.clearSel · สลับ data-i18n-title → TH/EN เปลี่ยนตาม
- typoClearSel ใช้ _hlLive(): ช่วงเก่าหลัง Undo → "ยังไม่ได้ไฮไลท์" (เดิมจะขึ้น "ไม่มีรูปแบบให้ล้าง" ซึ่งไม่ตรง)
- ทดสอบตรรกะ 11 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์ · ยังไม่รู้ว่าทุกเบราว์เซอร์แสดง tooltip บนปุ่มที่ disabled หรือไม่ ต้องทดสอบ

## 7 ต.ค. 2026 (12:15) — เปลี่ยนชื่อปุ่ม "ล้างรูปแบบจุดที่เลือก" → "ล้างรูปแบบจุดที่ไฮไลท์" · ✅ commit แล้วใน e108d13 (12:47)
- ผู้ใช้เสนอ: คลิกในช่องแล้วกดปุ่ม งง ต้องอ่านแถบล่างถึงรู้ว่าต้องไฮไลท์ก่อน — "เลือก" อ่านได้ทั้ง เลือกช่อง/ไฮไลท์ · tooltip + ข้อความเตือนใช้ "ไฮไลท์" อยู่แล้ว
- btn.clearSel TH "ล้างรูปแบบจุดที่ไฮไลท์" · EN "Clear highlighted format" · ปุ่มยังกดได้เมื่อคลิกช่องแม้ยังไม่ไฮไลท์ (เสนอผู้ใช้: กดได้เฉพาะตอนไฮไลท์)

## 7 ต.ค. 2026 (11:40) — ลบปุ่ม "ล้างรูปแบบ" · แก้ "ล้างรูปแบบจุดที่เลือก" · lint ข้อ 21 · ✅ commit แล้วใน e108d13 (12:47) (ต่อจาก 0229a02)
- ผู้ใช้ทดสอบพบ: คืนค่า มี Undo + เลือกขอบเขต + ถามก่อน · ล้างรูปแบบ ไม่มี Undo + ล้างทันที → ตกลง: ลบ ล้างรูปแบบ (ซ้ำกับ คืนค่า·เฉพาะอันนี้) + แก้ จุดที่เลือก
- อ่านโค้ดพบ ล้างรูปแบบ (ed.textContent=ed.textContent): ไม่มี Undo + ไม่ markDirty (ปิดแท็บไม่เตือน) · ไม่ล้างสี/ฟอนต์ทั้งช่อง (ทั้งที่ title บอก "ทั้งช่อง") · ช่องติดต่อบรรทัดหายเบอร์ต่อกัน + คุณไก๋หลุดฟอนต์ Noto · หมายเหตุรวมเป็นก้อนเดียว
- ลบ: ปุ่ม #typoClearField · typoClearField() · clearFormatField() · listener ซ้ำ · CSS .clearfield · keys btn/ttl.clearField fl.clearedField fl.noCell (ใช้ที่นี่ที่เดียว) · verify_oe.py REQUIRED_FUNCS
- แก้ จุดที่เลือก: ผูก click ทางเดียว (เดิม onclick + addEventListener = ทำ 2 รอบ และขึ้น "ล้างแล้ว" ทั้งที่ยังไม่ได้ไฮไลท์) · markDirty = มี Undo · ไม่มีอะไรล้าง → fl.clearSelNone (ไม่สร้างจุด Undo)
- clearFormatSel เขียนใหม่: ทีละ text node ดึงออกจาก span ที่ทาไว้ (ไม่มี class) · ไม่ออกจากโครงสร้าง (class / TYPO_TYPES / data-edit) — เดิมลบช่วงแล้วใส่ข้อความล้วนที่ระดับช่อง: ไฮไลท์ข้ามหัวข้อ→คำอธิบายในหมายเหตุ ข้อความรวมกัน · คุณไก๋หลุด .kai
- ปุ่ม จุดที่เลือก เริ่มต้น disabled (UI_STANDARD ข้อ 5) เหมือนปุ่มอื่นในแถบ
- หมายเหตุ: บันทึกเก่าในไฟล์นี้ (ส่วน v80) เขียนว่า "typoClearSel/typoClearField มี _snapNow() → undo ได้ ✅" — ไม่ตรงกับโค้ดที่ commit อยู่ (ไม่มี _snapNow ทั้งสองปุ่ม)
- lint ข้อ 21: ปุ่มใน #typobar ต้องถึง markDirty/_snapNow/openPanel/execCommand · ห้ามผูก click 2 ทาง · ลองกับไฟล์ก่อนแก้ จับได้ 4 ข้อ (2 ปุ่ม × 2 เรื่อง) หลังแก้ผ่าน
- ทดสอบตรรกะ 11 กรณีผ่าน (ชื่อเมนู · ช่องติดต่อ · หมายเหตุ · ไม่มีอะไรให้ล้าง · ยังไม่ไฮไลท์) · ยังไม่ทดสอบในเบราว์เซอร์
- typo_partial_mockup.html ยังมีโค้ดล้างรูปแบบแบบเก่า (เป็น mockup แยก ไม่ได้แก้)

## 7 ต.ค. 2026 (11:00) — ปุ่มล้างบันทึก · ลบไฟล์ .bak · ✅ commit แล้วใน 0229a02 (11:10) · ผู้ใช้ทดสอบล้างบันทึกผ่าน (ต่อจาก 4a60440)
- ลบไฟล์ .bak ใน C:\OE ทั้ง 38 ไฟล์ (201.82 MB) ตามที่ผู้ใช้อนุมัติ (6 ต.ค. 22:15) · .bak อยู่ใน .gitignore ไม่เคยถูก track · git ไม่เปลี่ยน
- ปุ่ม "ล้าง" (id actlogClear) หัวหน้าต่างบันทึก ต่อจาก CSV/JSON · ไม่มีบันทึก = กดไม่ได้ · กดซ้ำ = ปิด panel · .on เขียว
- panel แดง: "ล้างบันทึกทั้งหมด N รายการใช่ไหม? กู้คืนไม่ได้" + ปุ่ม [ส่งออก JSON ก่อน] · จำนวนอัปเดตเองถ้ามีบันทึกเพิ่มระหว่างเปิด
- ยืนยัน: ACTLOG=[] + localStorage.removeItem → เหลือ 1 รายการ fl.logCleared (บันทึกตรงด้วย logAdd · ไม่ผ่าน flashStatus เพราะถ้ามีคำเตือนล้นหน้าค้าง flashStatus จะไม่จด)
- ไม่มี Undo (ตกลงกับผู้ใช้) · เพิ่ม storage event: แท็บอื่นล้าง/เขียน → แท็บนี้โหลดใหม่ ไม่เขียนบันทึกเก่ากลับ (สาเหตุที่ผู้ใช้ลบใน DevTools ไม่ออก 6 ต.ค.) — ยังไม่รู้ว่า Chrome ส่ง event นี้ให้ไฟล์ file:// หรือไม่ ต้องทดสอบ 2 แท็บ
- ทดสอบตรรกะ 21 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์

## 6 ต.ค. 2026 (21:35) — อีก 5 จุดเปลี่ยนตาม TH/EN + lint ข้อ 20 · ✅ commit แล้วใน 4a60440 (6 ต.ค. 22:13) · ผู้ใช้ทดสอบผ่าน 4 จุด (ต่อจาก 022d51d)
- data-i18n-title: ปุ่มลบแถว (ttl.delRow) · ปุ่มลบกลุ่ม (ttl.delGroup) · ที่จับย่อขยายรูป (ttl.resize)
- data-i18n: "ยังไม่มีสีที่กำหนดเอง" (cp.noCustom)
- ปุ่ม ✕ ปิดหน้าต่างบันทึก: เพิ่ม title + key ใหม่ ttl.closeLog (TH ปิดหน้าต่างบันทึก / EN Close the activity log) · keys 243/243
- lint ข้อ 20: ข้อความที่ใส่ด้วย t() ต้องมี data-i18n / data-i18n-title · ยกเว้นข้อความใน panel (onCustom/onInput/onRelang) — ตรวจแล้ว pnl.delPageHint / pnl.cannotDeleteAll / pr.setApply ถูกสร้างใหม่ตอนกด TH/EN อยู่แล้ว (ไม่ใช่ bug)
- ลองกับไฟล์ก่อนแก้ จับได้ 4 จุดพอดี · หลังแก้ผ่าน · ยังไม่ทดสอบในเบราว์เซอร์

## 6 ต.ค. 2026 (21:15) — "ยังไม่มีบันทึกกิจกรรม" เปลี่ยนตาม TH/EN · ✅ commit แล้วใน 022d51d · ผู้ใช้ทดสอบผ่าน (รูป 3 รูป) (ต่อจาก c681773)
- สาเหตุ: _actlogRender ใส่ข้อความด้วย t() ครั้งเดียว ไม่มี data-i18n → applyLang ไม่แปลใหม่
- แก้: ใส่ data-i18n='log.empty' ให้ .al-empty (applyLang แปลทุก [data-i18n] อยู่แล้ว) — ไม่เรียก _actlogRender จาก applyLang เพราะ applyLang() ถูกเรียกครั้งแรกก่อน var ACTLOG ถูกกำหนด
- ข้อความในบันทึกแต่ละรายการคงภาษาเดิม (เป็นประวัติ) — ไม่เปลี่ยน
- พบจุดแบบเดียวกัน (ยังไม่แก้): title ปุ่มลบแถว (ttl.delRow) · ลบกลุ่ม (ttl.delGroup) · ที่จับย่อขยายรูป (ttl.resize) · "ยังไม่มีสีที่กำหนดเอง" (cp.noCustom) · ปุ่ม ✕ ปิดหน้าต่างบันทึกไม่มี title

## 6 ต.ค. 2026 (21:05) — ชื่อไฟล์ Save Editor สะกดตรงกับปุ่มอื่น · ✅ commit แล้วใน c681773 (21:05) · ผู้ใช้ทดสอบผ่าน (ต่อจาก ee476a7)
- ผู้ใช้เห็นจากรูป: Save Editor เสนอชื่อ OEIsanHotPotMenuEditor_ (P ใหญ่) ต่างจาก Save Menu / ส่งออกบันทึก (OEIsanHotpotMenu…) และไฟล์หลัก
- แก้ 2 จุดใน saveEditorFile (suggestedName + ชื่อไฟล์ทางสำรอง) → OEIsanHotpotMenuEditor_ · ไม่มี HotPot เหลือในไฟล์ · ไฟล์ที่บันทึกไว้แล้วไม่เปลี่ยน

## 6 ต.ค. 2026 (20:55) — Save Menu / Save Editor บอกว่าไฟล์อยู่ไหน · ✅ commit แล้วใน ee476a7 (20:58) · ผู้ใช้ทดสอบ 2 ปุ่มผ่าน (ต่อจาก 96762e8)
- ทำตามกฎ UI_STANDARD ข้อ 6 ที่ตั้งรอบ 20:45 กับปุ่มเดิม 2 ปุ่ม (หน้าต่าง Save มีอยู่แล้ว ขาดแค่ข้อความ)
- fl.savedMenu / fl.savedEditor: "ไฟล์ {name} อยู่ในโฟลเดอร์ที่คุณเลือก"
- fl.fallbackMenu / fl.fallbackEditor: "ไฟล์ {fname} อยู่ในโฟลเดอร์ดาวน์โหลดของเบราว์เซอร์ (กด Ctrl+J เพื่อดู)" · saveEditorFile ส่งชื่อไฟล์จริงเข้าข้อความ (เดิมไม่มีชื่อ)
- ลบข้อความเดิมที่ไม่จริง: "ใช้ Chrome/Edge + เปิดผ่าน http เพื่อเขียนทับไฟล์เดิม" — ผู้ใช้เปิดผ่าน file:// ใน Chrome แล้วหน้าต่าง Save ก็ขึ้น (รูป 6 ต.ค. 20:44)
- lint ข้อ 19: หลัง triggerDownload ข้อความต้องบอก "โฟลเดอร์ดาวน์โหลด" (ลองกับไฟล์ก่อนแก้ จับได้ 2 จุด)
- ทางสำรองทดสอบในเบราว์เซอร์ไม่ได้ (Chrome/Edge มีหน้าต่าง Save เสมอ) — ตรวจโค้ดเท่านั้น

## 6 ต.ค. 2026 (20:45) — ส่งออกบันทึกต้องให้เลือกที่เก็บ · ✅ commit แล้วใน 96762e8 (20:47) · ผู้ใช้ทดสอบหน้าต่าง Save ผ่าน (ต่อจาก 360df8b)
- ผู้ใช้ทดสอบส่งออกได้ทั้ง CSV/JSON (เปิดใน Excel/VS Code ได้) แต่ถาม: "user จะรู้ได้ยังไงว่า save ไว้ที่ไหน" — รอบแรกผมใช้ดาวน์โหลดเงียบ ไม่ตามแบบปุ่ม Save Menu ที่มีหน้าต่างเลือกที่เก็บอยู่แล้ว
- แก้: _saveAs(content,fname,mime,desc,ext) → showSaveFilePicker · เลือกแล้ว = fl.logExported (ชื่อไฟล์ + โฟลเดอร์ที่คุณเลือก) · ยกเลิก = fl.logExportCancel · ไม่มีหน้าต่าง/error = ดาวน์โหลด + fl.logExportDl (โฟลเดอร์ดาวน์โหลด, Ctrl+J)
- work instruction ใหม่: UI_STANDARD ข้อ 6 "ทุกไฟล์ที่แอปสร้าง ผู้ใช้ต้องรู้ว่าอยู่ไหน" + lint ข้อ 18 (triggerDownload ต้องมี showSaveFilePicker ก่อน)
- ทดสอบตรรกะ 9 กรณีผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
- พบ (ยังไม่แก้): ข้อความสำรองของ Save Menu / Save Editor (fl.fallbackMenu / fl.fallbackEditor) ไม่บอกว่าไฟล์อยู่ในโฟลเดอร์ดาวน์โหลด · บันทึกกิจกรรมจด "เลือกอยู่: ..." ทุกครั้งที่พิมพ์ 1 ตัว และคำเตือนซ้ำทุกตัวอักษร (3,500+ รายการ)

## 6 ต.ค. 2026 (13:50) — ส่งออกบันทึกกิจกรรม CSV / JSON · ผู้ใช้ทดสอบส่งออกแล้ว · commit รวมกับรอบ 20:45 (ต่อจาก 360df8b)
- ปุ่ม CSV / JSON ที่หัวหน้าต่างบันทึกกิจกรรม (CSS .al-export มีมาก่อนแต่ไม่มีปุ่ม) · exportActLog(fmt) · ไม่มีบันทึก = ปุ่มกดไม่ได้ (title บอกเหตุผล)
- เรียงตามที่แสดงในหน้าต่าง (_actlogSorted) · ชื่อไฟล์ OEIsanHotpotMenu_log_YYYYMMDD-HHMMSS.csv/.json · triggerDownload รับ mime (ไม่ใส่ = text/html เหมือนเดิม)
- CSV: UTF-8 BOM (Excel อ่านไทยถูก) · CRLF · RFC 4180 · หัวคอลัมน์/ประเภทตามภาษาที่ใช้ · ขึ้นต้น = + - @ ใส่ ' นำหน้า (กัน CSV injection)
- JSON: {app, exported (มี +07:00), count, entries:[{time, ts, type ดิบ, msg}]} · ข้อความไม่ถูกแก้
- ไม่ใช่การแก้เอกสาร: ไม่ dirty ไม่ undo · ทดสอบตรรกะผ่าน · ยังไม่ทดสอบในเบราว์เซอร์
- พบระหว่างทำ (ยังไม่แก้): สลับ TH/EN แล้วข้อความ "ยังไม่มีบันทึกกิจกรรม" ในหน้าต่างไม่เปลี่ยนภาษา (applyLang ไม่ render บันทึกใหม่)

## 6 ต.ค. 2026 (11:50) — ✅ commit แล้วใน 360df8b (13:40) · ผู้ใช้ทดสอบในเบราว์เซอร์ผ่านทั้ง 6 ข้อ (ต่อจาก bdba991)
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
