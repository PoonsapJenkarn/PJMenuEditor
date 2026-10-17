# OE Isan Menu — Session Status

**อัปเดตล่าสุด:** 27 ก.ย. 2026, 16:14 — v74: align selection subsystem กับ mockup (แก้ไฮไลท์ไม่ activate + สีไม่ติด)

## ▶ เริ่ม session ใหม่ที่นี่ (ปิด session 9 ต.ค. 2026 11:40)
- งานล่าสุด: ช่อง HEX สีขอบ + หน้าต่างสีขึ้นใต้ปุ่มที่เปิด + "สีมาตรฐาน" + lint #35 — ผู้ใช้ทดสอบผ่าน (11:37) · ✅ commit แล้วใน 4a7174f (11:44) · git สะอาด (ตรวจ 9 ต.ค. 11:51)
- ไฟล์: C:\OE\OEIsanHotpotMenuEditor.html · ไม่ล้น A4 · พิมพ์ 2 แผ่น · ขอบหน้า 8/12/8 mm · เครื่องพิมพ์พิมพ์ไม่ได้ ~2.5 mm ทุกด้าน (เผื่อ 3 mm, lint #34)
- ค้าง (เลือกทำ): กลุ่มใหม่ยังใช้สีเดิม #4a8579 · ออกจากโหมดแก้รูปแล้วข้อความแถบล่างค้าง · ลบรูปอาหารไม่มีผล · เพิ่มรูปไม่ย่อ · หลัง Ctrl+Z แถบรูปแบบอาจชี้ช่องที่ถูกลบ · ไอคอน ⚠ ซ้ำในแถบล่าง · ประวัติถี่เกิน · สีเส้นจุดไม่ทำงาน · typoFont ผูก 2 ครั้ง · B/I/U/S ไม่มีผล · ปุ่ม [ใส่ราคา] ไม่ focus · QR code (รอ URL) · ชื่อเมนูกลับ 17px? (ท้ายหน้า 1 มีที่ว่าง) · จำสีขอบล่าสุดข้าม reload? · ไฟล์ mockup ที่ไม่ได้ track 3 ไฟล์ (ลบหรือเก็บ?)
- verify_oe.py รันผ่านแล้ว 61/61 บนเครื่อง (11 ต.ค. 2026) · ✅ ตัดสินใจแล้ว (13 ต.ค. 2026): ไม่เอาเข้า pre-commit hook — hook คง lint อย่างเดียว · verify_oe.py = เครื่องมือรันเองตอนตรวจ runtime (manual) ไม่ใช่ทุก commit

## 17 ต.ค. 2026 (23:00) — ✅ เสร็จ: ฝัง OFL 1.1 เต็มในไฟล์ .html (ระดับ A+B) — .html เดี่ยว self-contained + อ่านในแอปได้ (ผู้ใช้เลือก A+B)
- บริบท: ผู้ใช้ชี้ว่า app เป็นไฟล์เดียว (.html) · ถ้าจะให้ OFL เต็มติดไปกับไฟล์และอ่านได้ ต้องอยู่ใน .html เอง (THIRD-PARTY-LICENSES.txt อยู่ใน repo เท่านั้น คนได้ไฟล์เดี่ยวไม่มี)
- ระดับ B (หลัก): เพิ่ม <details class="ofl-full"> ในแท็บลิขสิทธิ์ · summary i18n about.oflView (ดูสัญญาอนุญาตเต็ม / View full license) · <pre class="ofl-text"> = OFL 1.1 เต็ม verbatim (3 copyright + ตัวบทจาก OFL.txt จริง อ่านจากเครื่อง ไม่พิมพ์ซ้ำ) · อังกฤษล้วน (license ห้ามแปล) · อ่านได้ทั้ง View Source + ในแอป · travels กับไฟล์ · CSS .ofl-text (pre-wrap, monospace 11px, max-height 200px scroll)
- ระดับ A (header comment): OFL notice ใน <head> ต่อจาก MIT · 3 copyright + ชื่อ OFL 1.1 + pointer · ⚠️ ไม่ใส่ตัวบทเต็มใน comment เพราะ OFL body มี "-----" separator + "--" → HTML comment ห้ามมี (จะ invalid) · แจ้งผู้ใช้แล้ว ตัวเต็มอยู่ใน <pre> แทน (ครบตาม intent ระดับ A)
- 🐛 lint ดักเจอ: OFL body มี list markers 1)..5) → paren เกิน 5 → lint paren-balance FAIL · แก้ lint ให้ strip <pre class="ofl-text"> ก่อนนับ brace/paren (verbatim text ไม่ใช่โค้ด) · lint #70 ขยาย: pre.ofl-text + ตัวบท OFL marker + header notice + i18n oflView · V0 PASS + 5 variant FAIL ตรงจุด · lint PASS 0/0
- html sha 95b3560c48ab9167 · 6,949,178 bytes · LF · UI_STANDARD เพิ่มข้อ 11.3 · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (22:41) — ✅ เสร็จ: สร้างไฟล์ THIRD-PARTY-LICENSES.txt (ปิด OFL compliance ก่อน publish · ผู้ใช้เลือก)
- สร้าง C:\OE\THIRD-PARTY-LICENSES.txt จาก OFL.txt จริง 3 ไฟล์ (C:\OE\Fonts\{Prompt,Sarabun,Noto_Sans_Thai}\OFL.txt) — เนื้อหา verbatim ไม่เดา · header อธิบาย: โค้ด MIT (ดู LICENSE) + ฟอนต์ฝัง 3 ตัว OFL 1.1 + copyright แต่ละตัว · ตามด้วย OFL.txt เต็มทั้ง 3 (คั่นด้วย separator)
- 14,359 bytes · LF (normalize จาก CRLF ต้นฉบับ 93 CRLF/ไฟล์) · sha 7891d4c3a51e7639 · OFL 1.1 body 3 ชุด · copyright ครบ (Cadson Demak 2015 / Sarabun 2018 / Noto 2022)
- README เพิ่มย่อหน้าชี้ไป THIRD-PARTY-LICENSES.txt (TH+EN) ใต้ Copyright line · ไม่แตะ HTML/lint (ไฟล์ license + markdown เท่านั้น)
- ปิดช่องว่าง OFL compliance ที่ค้างมาจาก About Licenses tab (b3323da) · ตอนนี้ repo มีทั้ง About สรุป + ไฟล์ license เต็ม = พร้อม publish ด้าน license
- ยังไม่ commit · (THIRD-PARTY-LICENSES.txt เป็นไฟล์ใหม่ ต้อง git add)

## 17 ต.ค. 2026 (22:30) — 🐛✅ แก้บั๊กแอปค้าง: apostrophe ไม่ escape ใน i18n (user's) ทำ JS พังทั้งไฟล์ (ผู้ใช้ "app ค้าง คลิกอะไรไม่ได้เลย")
- อาการ: ผู้ใช้แจ้งแอปค้าง คลิกไม่ได้ · Console: Uncaught SyntaxError: Unexpected identifier 's' (OEIsanHotpotMenuEditor.html:1969) — ไม่ใช่ draft ค้าง แต่เป็น syntax error ในไฟล์เอง → JS ทั้งไฟล์ไม่โหลด → handler ตายหมด
- 🐛 ต้นเหตุ (ความผิด agent รอบ licNote 614dad ที่ยังไม่ commit): note อังกฤษ "are the user's own responsibility..." · apostrophe ใน user's ปิด single-quote JS string ก่อนเวลา → "s own responsibility" = invalid JS
- 🔑 ทำไม lint ไม่จับ: lint นับ brace/paren ครบ (apostrophe ไม่กระทบ count) · lint PASS แต่ JS พัง — ช่องว่างจริงของ lint
- แก้: เขียน EN ใหม่เลี่ยง apostrophe "are the responsibility of the user to verify before distribution." (ตัวเลข/ความหมายเดิม) · สแกน I18N block ยืนยันไม่เหลือ letter'letter · TH ไม่กระทบ (ไม่มี apostrophe)
- เพิ่ม lint #73: สแกน I18N block หา regex [A-Za-z]'[A-Za-z] (apostrophe ไม่ escape) · V0 PASS + V1(user's)/V2(don't) FAIL + V3(escaped \') PASS ไม่ false-positive · lint PASS 0/0
- html sha 3dc5aaa650bab1c5 · 6,943,548 bytes · LF · UI_STANDARD เพิ่มข้อ 11.2 · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · (งาน licNote 614dad + fix นี้ รวม commit เดียวได้)

## 17 ต.ค. 2026 (22:05) — ✅ เสร็จ: แก้ note แท็บลิขสิทธิ์ให้ scope ถูก (ผู้ใช้ถาม "ฟอนต์ที่เพิ่มเองทีหลังไม่ได้ลงใน license จะเป็นอะไรไหม")
- บริบท: ผู้ใช้ถามเรื่องฟอนต์ที่ผู้ใช้ฝังเพิ่มทีหลัง (upload/Google) ไม่ได้อยู่ในแท็บลิขสิทธิ์ · ผมวิเคราะห์: (1) template ที่เจ้าของแจก = มีแค่ 3 ฟอนต์ ครบแล้ว (2) ฟอนต์ที่ผู้ใช้เพิ่มเอง = ผู้ใช้กลายเป็นผู้แจกจ่าย ภาระ license ตกที่ผู้ใช้ ไม่ย้อนถึง template
- 🔑 ช่องว่างจริง = ถ้อยคำ note เกินจริง: เดิม "ฟอนต์ทั้งหมดอยู่ภายใต้ OFL" เป็นเท็จทันทีที่ผู้ใช้เพิ่มฟอนต์เชิงพาณิชย์ · auto-list ฟอนต์ที่เพิ่มทำไม่ได้ (เบราว์เซอร์อ่าน license จากไฟล์ฟอนต์ไม่ได้ — พิสูจน์แล้วตอนทำ sync) → แก้ถ้อยคำแทน
- แก้ licNote 3 จุด (static TH + i18n th/en): "ฟอนต์ทั้งหมด" → "ฟอนต์ที่มากับแอป (3 ฟอนต์ด้านบน)" + เพิ่มประโยค "ฟอนต์ที่คุณเพิ่มเองภายหลัง (อัปโหลด/Google) เป็นความรับผิดชอบของผู้ใช้ในการตรวจสอบสิทธิ์ก่อนแจกจ่าย" · EN parallel
- ข้อความอย่างเดียว ไม่แตะ lint (key licNote มีอยู่) · lint PASS 0/0 · html sha 614dad177189b25d · 6,943,547 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (20:43) — ✅ เสร็จ: เพิ่มแท็บลิขสิทธิ์ (แท็บที่ 3) ใน About — ปิดช่องว่าง OFL (ผู้ใช้เลือก "แท็บลิขสิทธิ์")
- บริบท: ผู้ใช้ถามว่า pro/enterprise ใส่แท็บอะไรใน About บ้าง · ผมเสนอ licenses (ปิดช่องว่าง OFL จริงก่อน public) + help · ผู้ใช้เลือกแท็บลิขสิทธิ์
- 🔑 copyright ฟอนต์ = อ่านตัวจริงจาก OFL.txt (ไม่เดา): C:\OE\Fonts\{Prompt,Sarabun,Noto_Sans_Thai}\OFL.txt → Prompt "Copyright (c) 2015, Cadson Demak" · Sarabun "Copyright 2018 The Sarabun Project Authors" · Noto Sans Thai "Copyright 2022 The Noto Project Authors"
- เพิ่ม nav แท็บที่ 3 (data-tab=lic) + pane (data-pane=lic) · หัว "ลิขสิทธิ์และสัญญาอนุญาต" · body: โค้ด MIT (Copyright 2026 Poonsap Jenkarn) + ฟอนต์ฝัง OFL 1.1 (3 ฟอนต์ + copyright) · note: OFL อนุญาตฝัง/แจก/เชิงพาณิชย์ฟรี คงประกาศลิขสิทธิ์ · ใช้คลาส .about-tech-* เดิม ไม่เพิ่ม CSS · ย่อหน้า nbsp×3
- i18n 4 key (about.tabLic/licHead/licBody/licNote) th+en · lint #70 ขยาย: 3 แท็บ (about/tech/lic) + lic pane + i18n 4 key · V0 PASS + 5 variant FAIL ตรงจุด · lint PASS 0/0
- html sha ee8eba07a908f3e1 · 6,942,677 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit
- ⚠️ ยังค้าง (OFL compliance เต็ม): About แท็บ = สรุป · ควรมีไฟล์ THIRD-PARTY-LICENSES / OFL.txt (OFL 1.1 เต็ม + copyright 3 ฟอนต์) ใน repo ก่อน public — ยังไม่ได้ทำ (เสนอผู้ใช้เป็นงานถัดไป)

## 17 ต.ค. 2026 (20:34) — ✅ เสร็จ: ปรับ techBody About เป็นโครงใหม่ตามที่ผู้ใช้จัด (sub-list ค่าวัด + เพดานแนะนำ 50 หน้า)
- ผู้ใช้ให้โครงใหม่ 3 bullet (เดิม 4) · ผมเห็นด้วย (ตัวเลขตรงผลวัดจริง 11/51/101 หน้า = 0.1/0.5/1.1 วิ · เพดาน 50 หน้ามีเหตุผล) → ดำเนินการทันทีตามที่ตกลง
- bullet 1: "การทดสอบความเสถียรรองรับถึง 100 หน้า" + sub-list 3 ค่า (10 หน้า 0.1 วิ / 50 หน้า 0.5 วิ / 100 หน้า 1.1 วิ) — ย่อหน้าด้วย nbsp×3 + en-dash (pre-line กินช่องว่างปกติ nbsp ไม่ถูกกิน)
- bullet 2: "แนะนำการใช้งานไม่เกิน 50 หน้า ถึงแม้ไม่จำกัดจำนวนหน้าสูงสุด แต่ประสิทธิภาพจะลดลงแบบเชิงเส้นตามจำนวนหน้าและรูปภาพที่มากขึ้น" (รวมเพดานแนะนำ + ไม่จำกัดหน้า + ลดลงเชิงเส้นตามหน้า+รูป)
- bullet 3: บรรทัดจำนวนรูปเดิม (2 มิลลิวินาที/รูป · 400 รูป = 0.9 วิ) · techHead/techNote คงเดิม (ข้อมูลจำเพาะด้านประสิทธิภาพ / หน้าจริง 7 รูป/หน้า)
- เดิม bullet "ตอบสนอง 0.1 วิ สำหรับไม่เกิน 10 หน้า" + "ไม่จำกัดหน้า..." แยก → ยุบเข้าโครงใหม่ (10 หน้าเป็น sub-item, ไม่จำกัดหน้ารวมใน bullet 2)
- EN parallel: Stability tested up to 100 pages + sub-list + Recommended for up to 50 pages... · ข้อความอย่างเดียว ไม่แตะ lint (key techBody มีอยู่) · lint PASS 0/0
- html sha 380ed76c0c9555fa · 6,940,226 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (20:00) — ✅ เสร็จ: เพิ่ม bullet "จำนวนรูป" ในสเปค About ให้ตรงผลทดสอบรูปเยอะ (ผู้ใช้ "ปรับให้ตรงกับผลการทดสอบล่าสุด")
- 📊 วัดรูปเยอะในหน้าเดียว (โคลนรูป base64 จริง · Chrome 17 ต.ค. 2026): save = 72ms@25รูป · 110ms@50 · 220ms@100 · 431ms@200 · 887ms@400 (overflow/snapshot ต่ำกว่า 20ms ตลอด ไม่แตะ base64)
- ข้อสรุป: ตัวขับ performance จริง = จำนวนรูปรวมทั้งเอกสาร (~2.2ms/รูป เชิงเส้น) ไม่ใช่จำนวนหน้า · save เป็นคำสั่งเดียวที่หนัก (serialize base64 ทุกรูป) · ยืนยันสเปคเลขหน้าเดิม (100 หน้า × 7 รูป ≈ 700 รูป ~1.1 วิ ตรงเส้น 400 รูป = 0.89 วิ)
- เพิ่ม bullet 4 ใน techBody (static + i18n th/en): TH "เวลาที่ใช้ในการบันทึกแปรผันตามจำนวนรูปภาพรวมในเอกสาร (ประมาณ 2 มิลลิวินาทีต่อรูป ทดสอบที่ 400 รูปในหน้าเดียวใช้เวลา 0.9 วินาที)" · EN "Save time scales with the total number of images... approximately 2 milliseconds per image; tested at 400 images on a single page: 0.9 seconds"
- ตัวเลขเดิม (10/100 หน้า) คงไว้ — ถูกต้องแล้ว · ไม่แตะ lint (key techBody มีอยู่) · lint PASS 0/0 · html sha 740e2873bb5cadaa · 6,940,435 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (19:44) — ✅ เสร็จ: ชื่อ TH (พูนทรัพย์ เจนการ) + สเปค performance เลขหน้าจริง (ผู้ใช้เลือก "เลขหน้าจริง + เปลี่ยนชื่อ TH")
- ชื่อผู้สร้างใน About: <b>Poonsap Jenkarn</b> (ตายตัว) → <b data-i18n="about.byName"> สลับภาษาได้ · TH "พูนทรัพย์ เจนการ" / EN "Poonsap Jenkarn" (คงเดิม) · i18n about.byName th+en
- 📊 วัดหน้าจริง (clone หน้า 1 ที่มีรายการ+7 รูป · Chrome 17 ต.ค. 2026): save = 92ms@11น · 245ms@26น · 472ms@51น · 1066ms@101น (overflow 28→270ms, snapshot 6→35ms, clone 0.2ms) · หนักกว่าหน้าเปล่ามาก (รูป base64)
- เหตุผลวัดใหม่: เลขเดิม (0.1วิ/50น · 200น/0.27วิ) มาจากหน้าเปล่า — ใช้ไม่ได้กับหน้าจริง · save แตะ 0.1วิ ตั้งแต่ ~10น, ที่ 50น ~0.5วิ, 100น ~1.1วิ
- techBody ใหม่ (3 bullet · เลขจริง · TH+EN): ตอบสนอง 0.1วิ/ไม่เกิน 10 หน้า · เสถียรถึง 100 หน้า (0.5วิ@50น, 1.1วิ@100น) · ไม่จำกัดหน้า ลดลงเชิงเส้นตามจำนวนหน้า
- techNote เปลี่ยน "หน้าเอกสารเปล่า" → "หน้าเอกสารจริงที่มีรายการและรูปภาพ (7 รูปต่อหน้า)" (TH+EN)
- lint #70 เพิ่ม about.byName ใน i18n tuple (กันชื่อหายภาษาเดียว) · V0 PASS + 2 variant FAIL ตรงจุด · lint PASS 0/0
- html sha d5fe3e150bc45c99 · 6,939,567 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · (หมายเหตุ: tooltip ตรา P ttl.credit + header comment ยังเป็น "Poonsap Jenkarn" — ไม่แตะ)

## 17 ต.ค. 2026 (19:26) — ✅ เสร็จ: ปรับภาษาแท็บ "ข้อมูลเทคนิค" ใน About เป็นทางการ (ผู้ใช้ "บ้านๆเกิน ไม่น่าเชื่อถือ")
- บริบท: ผู้ใช้ชี้ว่าภาษาสเปคใน About แท็บข้อมูลเทคนิคยังบ้านๆ (ลื่น · ไม่ค้าง ไม่ crash · วิ) → ต้องการ Professional/Enterprise · เนื้อหา/ตัวเลขเดิมทั้งหมด ไม่แต่งตัวเลข
- techHead: "ประสิทธิภาพ (วัดจริง 17 ต.ค. 2026)" → "ข้อมูลจำเพาะด้านประสิทธิภาพ" / EN "Performance (measured...)" → "Performance specifications" (ย้ายวันที่ไปอยู่ note)
- techBody (TH): รองรับเอกสารขนาด 1–10 หน้า... / ตอบสนองทุกคำสั่งภายใน 0.1 วินาที สำหรับเอกสารไม่เกิน 50 หน้า / ผ่านการทดสอบความเสถียรถึง 200 หน้า (เวลาประมวลผลสูงสุดที่คำสั่งบันทึก 0.27 วินาที) / ไม่จำกัดจำนวนหน้าสูงสุด ประสิทธิภาพลดลงแบบเชิงเส้น ไม่มีการค้างหรือหยุดทำงาน
- techBody (EN): Designed for documents of 1–10 pages... / Sub-0.1-second response for all operations up to 50 pages / Verified stable to 200 pages (maximum operation time: save at 0.27 seconds) / No fixed page limit; performance scales linearly without freezing or crashes
- techNote: ประโยคเต็มเป็นทางการ (วัดผลบนเบราว์เซอร์ Chrome เมื่อ 17 ตุลาคม 2026 โดยใช้หน้าเอกสารเปล่าเป็นเกณฑ์...) · EN เช่นกัน
- คำบ้านๆ หมดเกลี้ยง: ลื่น=0, ไม่ crash=0, " วิ)"=0 · แก้ techHead/techBody/techNote ทุกจุด (static + i18n th/en)
- ข้อความอย่างเดียว ไม่แตะ lint/UI_STANDARD (lint #70 เช็ก key มีอยู่ ไม่เช็กเนื้อความ) · lint PASS 0/0 · html sha a12e51ba327345f2 · 6,939,750 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (18:52) — ✅ เสร็จ: About เป็นแท็บแนวตั้ง (เกี่ยวกับ/ข้อมูลเทคนิค) + สเปค performance จากตัวเลขวัดจริง (ผู้ใช้เลือก "About แบบมีแท็บ")
- บริบท: ผู้ใช้ถามว่า app รองรับกี่หน้า + กังวล worst-case performance test · ให้ผู้ใช้รันสคริปต์วัดใน Console (ผมต่อ Chrome เองไม่ได้: file:// ถูกบล็อก + browser automation คนละ instance กับแท็บผู้ใช้)
- 📊 ผลวัดจริง (Chrome 17 ต.ค. 2026, หน้าเปล่า): addPage/overflow/snapshot/save — 11น:18/11/1/33ms · 26น:25/13/2/55 · 51น:34/19/2/99 · 101น:42/30/5/144 · 201น:86/64/9/268ms · เชิงเส้น ไม่ crash · หนักสุด=save 0.27วิ@200น · ลื่น(<0.1วิ)ถึง~50น
- 🔎 โค้ด: addPage() ไม่มี limit จำนวนหน้า (ยืนยันจาก source) — ช้าลงเชิงเส้น ไม่ตายตัว
- แก้ About modal เป็น master-detail (vertical tabs แบบ Notepad What's New): markup (nav 2 แท็บ + 2 panes) + CSS (.about-tab/.about-pane/.about-tech-*) + JS aboutTab(name) + openAbout รีเซ็ตแท็บ about + i18n 5 key (tabAbout/tabTech/techHead/techBody/techNote) th+en
- แท็บ active = เขียวข้อความ+ขอบซ้าย (เท่า edtab.active · ไม่ใช่พื้นเขียว) · .about-tab เป็น navigation ยกเว้นจาก lint #72 (ui-btn) · about-box กว้าง 380→460px
- lint แก้ 2 จุด: #72 ยกเว้นปุ่ม .about-tab จากกฎ ui-btn (แต่ยังห้าม inline bg) · #70 ขยายล็อก aboutTab+2แท็บ+tech pane+i18n · V0 PASS + 5 variant FAIL ตรงจุด · lint PASS 0/0
- html sha 8e367e01845d9fd9 · 6,938,792 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (17:00) — ✅ เสร็จ: กล่องนำเข้า — เลือกคอลัมน์ปลายทาง (ซ้าย/ขวา) + สลับปุ่ม วางรายการ/แก้ข้อความ (ผู้ใช้เลือก A)
- บริบท: ผู้ใช้ชี้ว่านำเข้าไปกองคอลัมน์ขวาหมด (รูป 3) + เสนอสลับปุ่ม (รูป 1) · เลือก A = เพิ่มช่องเลือกคอลัมน์ + สลับปุ่ม · อ้าง InDesign เลือก frame + เข้าชุดช่องเลือกหน้า
- 🐛 ต้นเหตุกองขวา: doPasteImport เดิมใช้ .ed-addgroup ตัวสุดท้ายของหน้า = คอลัมน์ขวาเสมอ · หน้า 3 ซ้ายว่าง เลยไปขวาหมด
- แก้ 5 จุด HTML: (1) สลับ rgroup toolbar: วางรายการ (นำเข้า) มาก่อน แก้ข้อความ (โหมด) → ติดกลุ่ม font/สี (2) <select id="pasteCol"> ข้าง #pasteDest + label paste.colLbl + option paste.colLeft/colRight (default ซ้าย) (3) doPasteImport อ่าน pasteCol → หา .col[data-col=L/R] ในหน้าปลายทาง → แทรกก่อน .ed-addgroup ของคอลัมน์นั้น + fallback (4)(5) i18n th/en: colLbl คอลัมน์/Column · colLeft ซ้าย/Left · colRight ขวา/Right
- lint #71 ขยาย: เช็ก #pasteCol มีอยู่ + paste.colLbl/colLeft/colRight ใน i18n tuple · V0 PASS + 4 variant FAIL ตรงจุด · lint PASS 0/0
- html sha 3548b08eb7641deb · 6,934,170 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (16:19) — ✅ เสร็จ: กล่องนำเข้า — เพิ่มบรรทัดตัวอย่าง "น้ำ 666 30" + ขยายฟอนต์ 3 จุดให้เท่า bullet (ผู้ใช้)
- บริบท: ผู้ใช้ขอ (1) เพิ่ม "น้ำ 666 30" ท้ายตัวอย่างให้สมบูรณ์ (โชว์เคสชื่อเมนูลงท้ายด้วยเลข — น้ำ 666 = ชื่อ, 30 = ราคา) (2) ตัวหนังสือ 3 จุดยังเล็ก (3) ถาม dropdown หน้าเยอะ
- ต้นเหตุฟอนต์เล็ก: bullet (.about-desc ในกล่องนำเข้า) ไม่มี font-size scope → สืบทอดจาก body (~16px) · แต่ summary/exLabel/ph box ตั้ง inline 14/14/13px เลยเล็กกว่า bullet
- แก้: summary paste.title 14→16px · paste.exLabel "ตัวอย่าง" 14→16px · กล่องตัวอย่าง paste.ph 13→15px (monospace) · ลำดับชั้น: modalTitle 18 > summary/exLabel 16 ≈ bullet > ph box 15
- เพิ่มบรรทัดตัวอย่าง "น้ำ 666 30" 3 จุด: static markup (real \n) + i18n th paste.ph + i18n en (Soda 666 30 — parallel)
- dropdown #pasteDest: ตอบผู้ใช้ว่า native <select> เบราว์เซอร์จัดการ overflow เอง (scroll อัตโนมัติเมื่อเกิน viewport · ไม่หลุดจอ · ไม่ต้อง limit) — ไม่แก้โค้ด
- font-size inline ไม่แตะ lint (lint #71 เช็ก structure/i18n ไม่เช็ก px) · lint PASS 0/0 · html sha 356e4782cf2f4a71 · 6,933,224 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (15:15) — ✅ เสร็จ: กล่องนำเข้า — เพิ่มช่องเลือกหน้าปลายทาง + เด้งไปไฮไลท์กลุ่มใหม่ + ข้อความบอกหน้า (ผู้ใช้ "ไม่รู้ว่านำเข้าหน้าไหน สะเปะสะปะ")
- บริบท: ผู้ใช้ชี้ว่าตอนวางรายการนำเข้า ไม่รู้ว่าของไปโผล่หน้าไหน (เดิม doPasteImport ยัดเข้าคอลัมน์สุดท้ายของหน้าสุดท้ายเสมอ ไม่ให้เลือก ไม่เห็นผล) · ผู้ใช้เลือก "เลือกหน้า + เด้งไปเห็นของใหม่" · อ้าง Excel/Notion import
- แก้ 6 จุด HTML: (1) CSS .sec.just-imported ไฮไลท์ (keyframes justImp 2.2s · @media screen เท่านั้น · ไม่พิมพ์) (2) <select id="pasteDest"> + label paste.destLbl เหนือ textarea (3) openPaste เติม option หน้า 1..N default หน้าสุดท้าย (option = ตัวเลขล้วน ไม่ต้อง relang) (4) doPasteImport: อ่าน pasteDest → แทรกที่คอลัมน์สุดท้ายของหน้าที่เลือก + scrollIntoView + ไฮไลท์ 2.2s + destPage=_pageNoOf (5)(6) i18n paste.destLbl th/en + paste.done เพิ่ม {page}
- ปลายทาง: เดิม = หน้าสุดท้ายเสมอ → ใหม่ = หน้าที่ผู้ใช้เลือก (default หน้าสุดท้าย) · ข้อความ "✓ นำเข้า {n} เมนู {g} กลุ่ม ไปที่หน้า {page} แล้ว"
- lint #71 ขยาย: เช็ก #pasteDest มีอยู่ + _pageNoOf(made[0]) ใน doPasteImport + paste.destLbl ใน i18n tuple · V0 PASS + 5 variant FAIL ตรงจุด · lint PASS 0/0
- html sha 53cf2c821bbe90cc · 6,933,176 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (13:22) — ✅ เสร็จ: วางมาตรฐานปุ่มกลาง .ui-btn-* + ครอบ 2 modal (About + นำเข้า) + lint #72 (ผู้ใช้ "สร้างมาตรฐานเถอะ เพิ่มใหม่ทีไรต้องมาบอกแก้ทุกที")
- บริบท: ผู้ใช้ชี้ว่ากล่องนำเข้าปุ่มสีไม่เข้าธีม + บ่นว่าต้องสั่งแก้สีซ้ำทุกครั้งที่เพิ่มของใหม่ → ต้นเหตุ: app ไม่มีคลาสปุ่มกลาง · modal ใหม่ฝังสี inline มั่ว (ปุ่มนำเข้า background:#1592D9 = สีหัวกลุ่มเมนูอื่นๆ ไม่ใช่สี UI · ปุ่มยกเลิกไม่มี bg = เทา default) · ปุ่มใช้ class about-close ที่ scope แค่ #aboutModal เลยไม่ติดสไตล์
- มาตรฐานใหม่ (อ้างสีจริงจากโค้ด app): .ui-btn (ฐาน) · .ui-btn-primary เขียว #217346 hover #1a5c38 (เท่า btn-save/btn-dl) · .ui-btn-secondary ขาวขอบเทา #d2d0ce hover เขียว · press :active translateY(1px) ไม่มีเขียว (ข้อ 1/lint #43)
- แปลงปุ่ม 3 ตัว: About "ปิด" + นำเข้า (→primary) + ยกเลิก (→secondary) · ลบคลาส about-close ทิ้งทั้งหมด (3 ปุ่ม) + ลบกฎ CSS #aboutModal .about-close + :hover ที่กลายเป็น dead (2 กฎ) · ไม่เหลือ about-close ในไฟล์
- น้ำเงิน #1592D9 เหลือ 3 จุด = สีหัวกลุ่ม "เมนูอื่นๆ" + summary link (เนื้อหา/ไม่ใช่ปุ่ม · นอกขอบเขต ถูกต้องแล้ว)
- lint #72: (a) .ui-btn-primary มี #217346 + .ui-btn-secondary มี #d2d0ce (b) .ui-btn:active มี transform (c) ทุก <button> ใน #pasteModal/#aboutModal ใช้ ui-btn (d) ห้าม background:# inline บนปุ่ม 2 modal · V0 PASS + 4 variant FAIL ตรงจุด · lint PASS 0/0
- CSS+markup · html sha d050c894673e1ac5 · 6,931,628 bytes · LF · UI_STANDARD เพิ่มข้อ 13 · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (13:00) — ✅ เสร็จ: ลบบรรทัดกฎสรุป (paste.guide) + เปิด 4 bullet "วิธีการนำเข้า" เป็นค่าเริ่มต้น (ผู้ใช้ "เอาออกครับ")
- บริบท: ผู้ใช้ถามตรงๆ "บรรทัดนี้ (วาง 1 บรรทัด = 1 เมนู · เลขท้ายบรรทัด = ราคา) ควรเอาไว้ไหม" · ผมเอนไปทางเอาออก: บรรทัดสรุปนี้ซ้ำกับ 4 bullet ที่เพิ่งเขียน (คำอธิบาย format 2 ที่ในกล่องเดียว = รก) · ทางสะอาด = ลบสรุป + เปิด bullet default เป็น one source of truth
- แก้ 3 จุด HTML: (1) ลบ element <div data-i18n="paste.guide"> เหนือ textarea (2) ลบ i18n key paste.guide th+en (ไม่ทิ้ง dead code · เหลือ paste.modalTitle) (3) <details class="paste-howto"> → เพิ่ม open (เปิดค่าเริ่มต้น)
- เหตุผลเปิด default: ฟีเจอร์พึ่ง format 100% (พิมพ์ผิด format = นำเข้าพลาด) · ซ่อนข้อมูลสำคัญหลังคลิกเป็นดีไซน์ไม่ดี · Google Forms/Notion import โชว์ hint format ไว้เห็นเลย
- lint #71 แก้: เอาเช็ก element paste.guide + i18n key paste.guide ออก · เพิ่มเช็ก <details class="paste-howto" open> ต้องมี open · V0 PASS + 3 variant FAIL (no open / no modalTitle / no card bg) ตรงจุด · lint PASS 0/0
- html sha a1a3bd59f7cdeb97 · 6,930,898 bytes · LF · paste.guide = 0 ทั้งไฟล์ · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (12:44) — ✅ เสร็จ: วิธีการนำเข้า (paste.desc) เปลี่ยนจากประโยคยาวต่อกัน → bullet 4 ข้อแยกบรรทัด (ผู้ใช้เสนอ · ผมเห็นด้วย + ปรับถ้อยคำข้อ 3)
- เดิม: "วาง 1 บรรทัดต่อ 1 เมนู · เว้น 1 วรรคต่อด้วยตัวเลข = ราคา · บรรทัดที่ไม่มีราคา = หัวกลุ่ม" (ประโยคเดียวยาว)
- ใหม่ (4 bullet): วาง 1 บรรทัดต่อ 1 เมนู / เว้น 1 วรรคระหว่างชื่อเมนูและราคา / ราคาอยู่ท้ายบรรทัด (ต่อจากชื่อเมนู) / ชื่อกลุ่มเมนูไม่ต้องใส่ตัวเลขต่อท้าย (บรรทัดที่ไม่มีราคา = ชื่อกลุ่มเมนู)
- ปรับถ้อยคำข้อ 3 จากที่ผู้ใช้เขียน "(ชื่อเมนู)" → "(ต่อจากชื่อเมนู)" เพราะวงเล็บเดิมอ่านงง · ที่เหลือตามผู้ใช้
- กลไกขึ้นบรรทัด: เพิ่ม white-space:pre-line ที่ div.about-desc (เดิมไม่มี) + static markup ใช้ newline จริง + i18n th/en ใช้ \n (แบบเดียวกับ paste.ph) · applyLang set textContent → pre-line เรนเดอร์บรรทัด
- แก้ 3 จุด: static markup TH + i18n paste.desc th + en · ไม่แตะ lint (key paste.desc ยังอยู่ th+en, lint #71 ผ่าน) · lint PASS 0/0
- html sha ae30b4633f81e9ed · 6,931,273 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (12:26) — ✅ เสร็จ: เอา "บาท/THB" ออกจากตัวอย่าง paste (ผู้ใช้เลือก "คงไว้ง่ายๆ + เอาบาทออกจากตัวอย่าง")
- บริบท: ผู้ใช้ถามเรื่อง format วาง — บาทเอาออกดีไหม / quote / dash · ผมแนะนำ (1) ชื่อมีช่องว่างไม่ต้องทำอะไร parser ตัดเลขท้าย=ราคาอยู่แล้ว (2) ไม่ใช้ quote (ไม่มี delimiter) (3) dash เป็นออปชันได้แต่ชนช่วงราคา 230-280 · ผู้ใช้เลือกคงง่ายๆ + เอาบาทออกจากตัวอย่าง
- แก้ตัวอย่าง 3 จุด: TH i18n paste.ph + TH static HTML default (คอหมูย่าง 70 บาท → คอหมูย่าง 70, 2 จุด) + EN i18n paste.ph (Grilled pork 70 THB → Grilled pork 70)
- พาร์เซอร์ไม่แตะ: ยังรับ บาท/฿/THB ท้ายบรรทัดถ้าใครพิมพ์มา (ให้อภัย ไม่ลงโทษ) · แค่ตัวอย่างโชว์เลขเปล่าให้สะอาด · ไม่เพิ่ม quote/dash
- ไม่แตะ lint (paste.ph key ยังอยู่ แค่เปลี่ยน value) · lint PASS 0/0 · html sha 28413dbd35b38900 · 6,930,666 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (12:14) — ✅ เสร็จ: แก้บั๊ก popup นำเข้า "มองไม่เห็น" — ใส่การ์ดขาว+กรอบ+เงาให้ #pasteModal (ผู้ใช้ส่งรูป)
- บริบท: ผู้ใช้ "ใส่กรอบ หรือเป็นหน้าต่างเถอะ มันมองไม่เห็น" + รูป popup ที่เนื้อหาลอยบนพื้นมืดไม่มีการ์ด
- 🐛 ต้นเหตุ (บั๊กจริง ไม่ใช่แค่มองยาก): ตอนทำ type-scale ก่อนหน้า CSS การ์ด (background/border-radius/box-shadow/padding) ถูกย้ายจาก `.about-box` (base ใช้ร่วม 2 modal) → `#aboutModal .about-box` (เฉพาะ About) · ผล: `#pasteModal .about-box` เหลือแค่ max-width/overflow ไม่มีพื้นหลัง → กล่องนำเข้าลอยบนพื้นมืด rgba(0,0,0,.4) มองไม่เห็นขอบ
- แก้ CSS บรรทัด 178: `#pasteModal .about-box` เพิ่ม background:#fff + border:1px solid #e1dfdd + border-radius:12px + box-shadow:0 8px 32px rgba(0,0,0,.3) + padding:22px 24px + box-sizing · คง max-width/width/max-height/overflow เดิม
- lint #71 เพิ่มเช็ก: `#pasteModal .about-box` ต้องมี background (regex กลุ่ม) · V0 PASS + variant (ย้อน regress) FAIL ตรงจุด · lint PASS 0/0
- CSS-only · html sha 73a5541c637fdfcb · 6,930,690 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 17 ต.ค. 2026 (11:54) — ✅ เสร็จ: popup นำเข้ารายการเมนู — เพิ่มหัวข้อ + บรรทัดคำแนะนำเหนือช่อง (ผู้ใช้เลือก · ไม่ใช้ placeholder)
- บริบท: ผู้ใช้ถาม "Professional แล้วใช่ไหม" + ส่งรูป popup · ผมประเมิน 3 จุดขาด: (1) ไม่มีหัวข้อกล่อง (2) ช่องว่างไม่มี hint (3) คำแนะนำยุบไว้ · ผู้ใช้เลือก "หัวข้อ + บรรทัดคำแนะนำเหนือช่อง"
- ⚠️ บทเรียน: ตอนแรกผมเสนอ placeholder → lint #9 (UI_STANDARD ข้อ 6) จับ FAIL เพราะโปรเจกต์ห้าม placeholder (หายตอนพิมพ์ + screen reader ไม่อ่าน) · ผมหยุด บอกผู้ใช้ตรงๆ ว่าแนะนำผิด ไม่ยกเว้น lint ให้ตัวเอง · เปลี่ยนเป็นบรรทัดคำแนะนำนอกช่อง (เห็นตลอด) แทน
- แก้ 4 จุด HTML: (1) หัว modal <div data-i18n="paste.modalTitle"> "นำเข้ารายการเมนู" 18px เขียว #217346 บนสุด (2) บรรทัดคำแนะนำ <div data-i18n="paste.guide"> "วาง 1 บรรทัด = 1 เมนู · เลขท้ายบรรทัด = ราคา" 13px เหนือ textarea (3)(4) i18n paste.modalTitle/paste.guide th+en
- lint #71 ขยาย: เช็ก element paste.modalTitle + paste.guide มีอยู่ + เพิ่ม 2 key ใน i18n tuple · V0 PASS + 4 variant FAIL ตรงจุด · lint PASS 0/0
- html sha e17aed7cbc0dd6f5 · 6,930,553 bytes · LF · ไม่มี placeholder (regex placeholder[=:] = 0) · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 16 ต.ค. 2026 (16:04) — ✅ เสร็จ: เปลี่ยนชื่อโปรแกรม "OE Isan Hotpot Menu Editor" → "PJ Menu Editor" (ผู้ใช้ · OE = ตัวอย่าง, ตัว download จริง = template เปล่า)
- เหตุ: ชื่อโปรแกรม (TOOL) ควร generic ไม่ผูกร้าน OE · OE menu = ตัวอย่างให้ชม · ตัว download จริงจะเป็น template เปล่า (ยังไม่ทำ — งานถัดไป)
- แก้ 4 จุด HTML: (1) header comment "PJ Menu Editor — เครื่องมือทำเมนูร้านอาหารขนาดเล็ก (เมนู A4) · ไฟล์นี้เป็นตัวอย่าง" (2) about-name "PJ Menu Editor" (3) about.desc th "เครื่องมือทำเมนูร้านอาหารขนาดเล็ก" (4) about.desc en "Menu maker for small restaurants"
- README: title → "PJ Menu Editor — เครื่องมือทำเมนูร้านอาหารขนาดเล็ก" + ระบุว่าไฟล์ตัวอย่าง = เมนู OE
- lint ไม่ล็อกค่า about (lint #70 เช็กแค่ key มีอยู่) · lint PASS 0/0 · html sha 7318715a2ebd1f30 · 6,921,235 bytes · README sha 000a0e7e7c6e1c9f · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit
- ⚖️ รีวิวกฎหมาย (16 ต.ค.): ต้องแก้ก่อน public — (1) OFL notice: ต้องแนบข้อความ OFL + copyright ฟอนต์ (Prompt/Sarabun/Noto Sans Thai) · MIT ครอบแค่โค้ด ฟอนต์ที่ฝัง base64 ยังเป็น OFL (2) ข้อมูลร้าน OE (เบอร์โทรคุณไก่ = personal data ตาม PDPA 2562 + แบรนด์ร้าน) → แก้ด้วย template เปล่า (3) ที่มารูปอาหาร/โลโก้ร้าน = ยังไม่ทราบ ต้องถามผู้ใช้ · repo ยัง private = ยังไม่มี exposure

## 16 ต.ค. 2026 (15:53) — ✅ เสร็จ: เลือก license = MIT · เติมให้ครบทุกจุด (ผู้ใช้เลือก MIT · เป้า เครดิต→งาน→เงิน)
- สร้างไฟล์ LICENSE (MIT · Copyright (c) 2026 Poonsap Jenkarn) · ข้อความ MIT มาตรฐานเต็ม · LF · 1072 bytes
- HTML header comment: "License: ยังไม่กำหนด (รอเลือก) / TBD" → "License: MIT License · Copyright (c) 2026 Poonsap Jenkarn"
- About modal i18n about.licenseVal (th+en): "รอกำหนด (TBD)"/"To be decided (TBD)" → "MIT License" ทั้งคู่
- README: เพิ่มส่วน "สัญญาอนุญาต / License" (TH+EN) + ลิงก์ไปไฟล์ LICENSE + Copyright line
- เป็นข้อความ/ไฟล์ license ไม่แตะ lint · lint PASS 0/0 · html sha 20145442bf54c9e4 · 6,921,330 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit
- ✅ ตัวตนของงานครบแล้ว: ชื่อ (เครดิต 3 จุด) + About modal + GitHub repo (private) + MIT License · พร้อมเปลี่ยน repo เป็น public เมื่อผู้ใช้ต้องการ

## 16 ต.ค. 2026 (15:40) — ✅ เสร็จ: ป๊อปอัพ About เด้งจากตรา P (ผู้ใช้ท้วงว่าซอฟต์แวร์ควรมี About = การมีตัวตนของงาน · ผมยอมรับ ทำให้)
- ไม่ทำหน้าแยก (ซ้ำ README) · ทำป๊อปอัพ Help→About · คลิกตรา P (.edbrand onclick=openAbout) เปิด · ปิดด้วยปุ่ม/คลิกฉากหลัง/Escape · เก็บ tooltip ttl.credit ไว้
- เนื้อหา: ชื่อโปรแกรม + คำอธิบาย + สร้างโดย Poonsap Jenkarn 2026 + อีเมล mailto คลิกได้ + GitHub target=_blank + license (รอกำหนด TBD) · ลิงก์ #0b5fb0 (ไม่ใช่เขียว)
- เฉพาะจอ: @media print ซ่อน · buildEditorHtml ปิด .open ตอนบันทึก · buildMenuHtml เพิ่ม #aboutModal ใน strip list
- lint #70 ใหม่: #aboutModal + openAbout/closeAbout + ตรา P wired + mailto + github target=_blank + strip editor/menu + i18n about.* th+en · V0 PASS + 5 variant FAIL ครบ (รวม check (c) เจาะ list buildMenuHtml)
- lint PASS 0/0 · sha 3cab2fea5d2713ae · 6,921,368 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit
- ค้าง: license (จุด 4) — About + HTML header + LICENSE จะเติม license พร้อมกันตอนเลือก (MIT vs PolyForm NC)

## 16 ต.ค. 2026 (15:22) — ✅ เสร็จ: ใส่เครดิต Poonsap Jenkarn (3 จุด · ผู้ใช้ยืนยันชื่อ+อีเมล)
- ชื่อ: Poonsap Jenkarn · 2026 · ติดต่อ jenkarn2631@gmail.com · repo github.com/Justin-10/OE
- จุด 1: HTML comment หัวไฟล์ — วางไว้ "ใน <head>" (ไม่ใช่ระหว่าง DOCTYPE↔<html>) เพราะ buildEditorHtml/buildMenuHtml ใช้ DOCTYPE+documentElement.outerHTML → comment นอก <html> จะถูกตัดตอน save · ใน head = ติดไปกับไฟล์ที่บันทึก/ดาวน์โหลด
- จุด 2: tooltip ตรา P (.edbrand) — เดิม title="POONSAP" → "สร้างโดย Poonsap Jenkarn · 2026 · jenkarn2631@gmail.com" + data-i18n-title="ttl.credit" (เฉพาะจอ)
- จุด 3: i18n ttl.credit (th+en) · README เพิ่มส่วน "ผู้สร้าง / Credit" + แก้บรรทัด "Local Git repo (ไม่มี remote)" → ชี้ไป github.com/Justin-10/OE (private) เพราะ push แล้ว
- เครดิตเป็นข้อความ/i18n ไม่แตะ lint · lint PASS 0/0 · html sha 5c9b925eefadba7e · 6,917,055 bytes · README sha d7d4f2a1bf67bf12 · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit
- ค้าง: LICENSE (จุด 4) รอเลือก license (MIT vs PolyForm NC) · HTML header เขียน "License: ยังไม่กำหนด (รอเลือก) / TBD" ไว้ก่อน

## 16 ต.ค. 2026 (12:21) — ✅ เสร็จ: ช่อง % ของ zoom พิมพ์ค่าเองได้ (ผู้ใช้ขอ · ผมเห็นด้วย ทำต่อทันที)
- เปลี่ยน #zoomLvl จาก <button> (คลิก=reset 100%) → <input> พิมพ์ % เองได้ · focus=select-all · Enter=blur commit · onchange=_zoomType()
- รับค่าอิสระ 50–200 ทีละ 1 (ไม่ปัด 10): _zoomSet→_zoomCommit (clamp เท่านั้น ไม่ snap) · ปุ่ม −/+ ยังทีละ 10 เข้ากริด (zoomIn=floor+1, zoomOut=ceil−1) · _zoomLoad ไม่ snap แล้ว
- คลิก-reset หายไป (input คลิก=พิมพ์) → reset ด้วยพิมพ์ 100 (แบบ Figma/เบราว์เซอร์) · zoomReset() ยังอยู่
- i18n ttl.zoomType (th+en) เพิ่ม · เก็บ ttl.zoomReset ไว้ (lint #69 ต้องการ) · zoomLvl เพิ่มใน lint _FILTERED16 (มีตัวกรอง strip ตัวเลข — ไม่มี warning)
- #edtabs ไม่มี preventDefault ครอบ (ต่างจาก #typobar) → input focus/พิมพ์ได้ไม่ติด · lint #69(e) ใหม่: zoomLvl ต้องเป็น input + มี function _zoomType · V0 PASS + V1(button)/V2(no func) FAIL
- lint PASS 0/0 (0 warning) · sha 1c38ca74c968b64f · 6,916,405 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 16 ต.ค. 2026 (11:54) — ✅ เสร็จ: In-page Zoom หน้า A4 (ปุ่มแถบบนข้าง Undo/Redo · ผู้ใช้เลือกแบบ A + ตำแหน่งแถบบน)
- ปัญหา: Browser Zoom ขยาย toolbar ไปด้วยจนบังเนื้อหา · แก้ไม่ได้ที่ browser → ทำ In-page zoom เอง ขยายเฉพาะ .page
- CSS: @media screen{ body:not(.measuring) .page{ zoom:var(--pagezoom,1); } } (screen-only + กัน measuring) · ตัวควบคุม .zoomctl (−/%/+) ใน #edtabs · ปุ่ม % คลิก=รีเซ็ต 100% · press-state :not(.on) (lint #43)
- JS: _zoom 50–200% ทีละ 10% · _zoomSet/_zoomApply/zoomIn/zoomOut/zoomReset/_zoomLoad · ตั้ง --pagezoom บน body.style · จำข้าม reload ที่ localStorage oe_pagezoom
- strip ตอนบันทึก: buildEditorHtml + buildMenuHtml เพิ่ม removeProperty(--pagezoom) → ไฟล์เปิดครั้งหน้า = 100% เสมอ
- i18n ttl.zoomIn/zoomOut/zoomReset (th+en) · lint #69 ใหม่: V0 PASS + 4 variant (not-screen-only/no-zoomctl/strip<2/no-i18n) FAIL ครบ · lint PASS 0/0
- sha e7bf4159a1de3e5b · 6,915,741 bytes · LF · UI_STANDARD เพิ่ม §10 · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 16 ต.ค. 2026 (07:18) — ✅ เสร็จ: ไล่แก้ขนาดฟอนต์ editor ที่เหลือครบทั้ง 6 กลุ่ม A–F (59 จุด) ตาม type scale (ผู้ใช้: ไล่แก้ให้ครบ)
- หลักเดิม: หัวป๊อปอัพ 15 · เนื้อหา/ปุ่ม/ช่องกรอก 14 · ป้าย 13 · เล็กสุด/โน้ต 12 · caret 11 · เนื้อหาเมนูที่พิมพ์จริง (.nm/.pr/.sec-h/.row/.brand/.contact/.crab/.pagelabel/.secnote) ไม่แตะ
- A แท็บรูป+ป๊อปอัพเงา: #imgbar select/button 12→14 · shd-pop 12→13 · shd-ttl 11→15 · shd-pop button 12→14 · shd-row label 11.5→13 · shd-num 12→14 · shd-use 11→13
- B ป๊อปอัพฟอนต์ Google: gfont-pop 12→13 · ttl 11→15 · inlbl 11→13 · name 12→14 · in 12→14 · add 12→14 · msg 11→13 · note 10→12 · sub 11→13 · addbtn 12→14 (คง prev 16)
- C ป๊อปอัพสี/เส้นขอบ: olcaret 10→11 · ol-auto 12→14 · ol-msg 11→13 · ol-w 12→14 · cp-caret 10→11 · cp-sec-label 11→13 · cp-empty 11→13 · cp hex 12→14 · cp-add 11→13 · cp-paint 12→14 · cp-dlg 12→13 · cp-dlg-ttl 12.5→15 · CpDlgHex 13→14 · cp-dlg-msg 11→13 · cp-dlg-ok/cancel 12→14 (ไม่แตะปุ่ม A เส้นขอบบน toolbar)
- D ปุ่มในหน้า A4: ed-del 11→12 · ed-dup 10→12 · ed-add 12→14 · ed-delpage 12→14 · pk-hint 11→12 · ed-addgroup 13→14 · ed-delgroup 13→14 · ed-dupgroup 12→14 · ed-badgeadd 12→13 · ed-badgedel 13→14 (คง sechead 19, emoji 22)
- E พาเนลหน้า/ปรับราคา (ep-*): ep-msg 13→14 · label 12.5→14 · input 13→14 · preview 11.5→13 · goset 11.5→13 · chk 12→14 · seg label 12→14 · num 13→14 · sel 12.5→14 · flabel 12→13 · ok/cancel/clearonly 12.5→14
- F เบ็ดเตล็ด: #edbar .hint 12→13 · #edbar .rgl 10→13
- แก้แค่ CSS font-size ไม่แตะ lint · lint PASS 0/0 · sha e8f715ef0b37112d · 6,912,589 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · เสี่ยงปุ่ม/ป๊อปอัพล้นบรรทัด ต้องเทส

## 15 ต.ค. 2026 (21:28) — ✅ แก้บั๊ก: คลิกเส้นจุด (.ln) ไม่ติดถ้าคลิก textbox มาก่อน (ผู้ใช้รายงาน · lint #68)
- อาการ: โหมดแก้ข้อความ คลิก textbox (.nm/.pr) ก่อน → คลิกเส้นประ เส้นไม่ active แก้ไม่ได้ (ทุกช่อง) · แต่คลิกที่ว่างก่อนแล้วคลิกเส้น = ได้
- ต้นเหตุ: .nm/.pr เป็น contenteditable, .ln เป็น span ธรรมดา · คลิก .ln → click handler (capture ~4080) เลือก .ln ถูก แต่ selectionchange ยิงตามด้วย caret ที่ค้างใน textbox → _typoFind(.nm) → typoSelect(.nm) แย่งทับ .ln (บรรทัด 3261)
- แก้ 1 จุด: เพิ่ม guard `&& !(_typoType && _typoType.line)` ใน selectionchange re-select (บรรทัด 3261) — ถ้าเลือกเส้นจุดอยู่ อย่าให้ selectionchange สลับไป contenteditable · การคลิกสลับ text↔line ยังทำงานผ่าน click handler ปกติ
- lint #68 ใหม่: ล็อก pattern re-select ต้องมี _typoType.line guard · ทดสอบ V0 ผ่าน + V1 (ไม่มี guard) FAIL + V2 (ลบ re-select) FAIL · lint PASS 0/0
- sha 352f05d539d515bf · 6,912,607 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · UI_STANDARD เพิ่มหัวข้อ lint #68

## 15 ต.ค. 2026 (21:24) — ✅ เสร็จ: ขยายปุ่ม Undo/Redo + badge ตัวเลข (ผู้ใช้: เล็กไป)
- ต่อจาก type scale · ปุ่ม Undo/Redo เป็นไอคอน SVG (ไม่ใช่ font) → ขยายไอคอน #edtabs .qab button svg 17→20px (ปุ่มคง 30×30 เท่า B/I/U/S)
- badge ตัวเลขจำนวน (#edtabs .qab .qab-badge): font 9.5→11px · min-width/height 15→17px · line-height 15→17px · top/right -5→-6px · border-radius 8→9px (ขยายวงให้พอดีเลข 2 หลัก)
- แก้แค่ CSS ไม่แตะ lint · lint PASS 0/0 · sha 75796362517dd947 · 6,912,334 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 15 ต.ค. 2026 (21:15) — ✅ เสร็จ: ปรับขนาดฟอนต์กลุ่มล่าง (แถบสถานะ + พาเนลประวัติ + แถบกู้คืน) ตาม type scale (ผู้ใช้: เล็กมาก)
- ต่อจาก type scale ของ toolbar (21:07) · ขยายกลุ่มล่างให้เข้าชุด: หัวพาเนล 15 · เนื้อหา/row/ปุ่ม 14 · ป้าย/หัวคอลัมน์/เวลา 13 · metadata เล็ก 12 · ลูกศร sort 10
- แก้ 16 จุด CSS: #edstatus base 12→14 (ข้อความสถานะ) · .edstatus-ic 14→15 · .edstatus-meta 11.5→13 · .ovfnote 11→12.5 · #draftBar 14→15 · #draftBar button 13→14 · al-title 13→15 · al-count 11→12 · al-export-btn 11→13 · al-export-lbl 11→13 · al-close 15→16 · al-cols 11→13 · al-arrow 9→10 · al-empty 12→14 · al-row 12→14 (al-msg inherits) · al-ts 11→13
- แก้แค่ CSS font-size ไม่แตะ lint · lint PASS 0/0 · sha 5c7d7edec289650d · 6,912,335 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit
- ค้าง (ยังไม่ทำ): contrast ของ al-ts (#a0a4a8 = 2.5) และ al-export-lbl (#8a8f94 = 3.05) DevTools เตือนว่าต่ำ — คนละเรื่องกับขนาด แยก commit ถ้าผู้ใช้ต้องการ · แท็บ รูป (#imgbar 12px) ยังไม่ปรับ

## 15 ต.ค. 2026 (21:07) — ✅ เสร็จ: ปรับเป็น type scale ตัวควบคุมหลัก 16px · ป้ายเล็ก 13px (ผู้ใช้เทียบเว็บมาตรฐานผ่าน DevTools · เลือก type scale)
- หลักการ (จากที่ผู้ใช้วัด DevTools): เว็บมาตรฐานใช้ขนาดตามบทบาท — เนื้อหา/ปุ่มที่คลิก 16px · nav/ปุ่มรอง 14px · ป้ายกำกับ 10–13px · ขนาดต่างแต่คอนทราสต์เท่ากัน
- แก้ 5 จุดเป็น 16px: #typobar select+input[color] 14→16 · #typoSize 14→16 · #typobar .ttoggle (B/I/U/S) 14→16 · #edbar .b-lg (＋ ฟอนต์/＋ ฟอนต์ Google) 13.5→16 · #edtabs .edtab (แท็บ) 15→16
- คงเดิม: #typobar button.tbtn (ปุ่ม format: ใช้ทั้งประเภท/ตั้งค่า/คืนค่า) 14px · #edribbon .rgl (ป้ายกลุ่ม) 13px · .szbtn (+/−) 15px · .langsw (TH/EN) 14px · .hint 13.5px — รักษาลำดับชั้น (ตัวควบคุมหลัก > ปุ่มรอง > ป้ายกำกับ)
- ยังไม่แตะแท็บ รูป (#imgbar 12px) — ถ้าอยากให้ทุกแท็บเท่ากันบอกได้ · แก้แค่ CSS ไม่แตะ lint · lint PASS 0/0 · sha c65e1563122ebf6e · 6,912,334 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · เสี่ยงปุ่มขึ้นบรรทัด/แถบสูง ต้องเทส

## 15 ต.ค. 2026 (20:52) — ✅ เสร็จ: ดันขนาดฟอนต์แถบแท็บด้านบน +2px ให้เข้าชุดกับ toolbar (ผู้ใช้ชี้ว่าแท็บไม่ปรับตาม)
- เหตุ: รอบ 20:45 ดัน toolbar (#typobar/#edribbon/#edbar) +2px แต่แถบแท็บด้านบน (#edtabs) เป็นคนละ element ไม่ได้แตะ → แท็บเลยเล็กกว่า toolbar
- แก้ 3 จุด CSS #edtabs: .edtab (ข้อความ/รูป/หน้า/ไฟล์) 13→15 · .langsw button (TH/EN) 12→14 · .hint 11.5→13.5
- แก้แค่ CSS font-size ไม่แตะ lint · lint PASS 0/0 · sha 2c6b0b1ea34e39fd · 6,912,336 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 15 ต.ค. 2026 (20:45) — ✅ เสร็จ: ดันขนาดฟอนต์ toolbar เป็น +2px จากเดิม (ผู้ใช้: +1px แทบไม่เห็นต่างในภาพ · เลือก +2px)
- ต่อจาก 19:45 (+1px) · ดันต่อเป็น +2px จากค่าเดิม: dropdown+color 12→14 · button.tbtn 12→14 · #typoSize 12→14 · #edribbon .rgl 11→13 · .b-lg 11.5→13.5
- เพิ่มคราวนี้: B/I/U/S (#typobar .ttoggle) 13→14 ด้วย — ไม่งั้นเล็กกว่า dropdown (14) ที่อยู่ข้างกัน · คงเดิม: .szbtn (+/−) 15px
- แก้แค่ CSS font-size ไม่แตะ lint · lint PASS 0/0 · sha 95f79ba2f9e98150 · 6,912,336 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · เสี่ยงปุ่มขึ้นบรรทัด/แถบสูงขึ้น ต้องเทส

## 15 ต.ค. 2026 (19:45) — ✅ เสร็จ: บวมพ์ขนาดฟอนต์ toolbar +1px (ผู้ใช้เทียบกับหน้า Google Fonts · เลือก +1px)
- เหตุ: toolbar ใช้ 11–12px เล็กกว่าค่าปกติเบราว์เซอร์ (16px) · เป้าหมาย = อ่านสบายเท่า ribbon Word/Excel (~12–13px) ไม่ใช่ใหญ่เท่าเว็บ browse ของ Google
- แก้ 5 จุด CSS: (1) #typobar select+input[color] 12→13 (2) #typobar button.tbtn 12→13 (3) #typobar .sizebox #typoSize 12→13 (เลขขนาด ให้เข้าชุด dropdown แถวเดียวกัน) (4) #edribbon .rgl 11→12 (ป้ายกลุ่มทุก ribbon) (5) #edbar .b-lg 11.5→12.5 (ปุ่มใหญ่ incl ＋ ฟอนต์/＋ ฟอนต์ Google)
- คงเดิม: #typobar .ttoggle (B/I/U/S) 13px · .szbtn (+/− ขนาด) 15px (สัญลักษณ์ ใหญ่พออยู่แล้ว)
- ยังไม่แตะ #imgbar select/button (12px, แท็บรูป) — ถ้าอยากให้ข้ามแท็บเท่ากันบอกได้ · แก้แค่ CSS ไม่แตะ lint · lint PASS 0/0 · sha 5de026498ed6c0e7 · 6,912,336 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 15 ต.ค. 2026 (19:00) — ✅ เสร็จ: เปลี่ยนชื่อปุ่ม "＋ Google" → "＋ ฟอนต์ Google" (ผู้ใช้เลือก)
- เหตุ: "＋ Google" บอกแค่ยี่ห้อ ไม่บอกว่าทำอะไร + ไม่ขนานกับปุ่ม "＋ ฟอนต์" (upload) · เปลี่ยนให้ขนานกัน: ＋ ฟอนต์ (จากไฟล์) / ＋ ฟอนต์ Google (ออนไลน์)
- btn.addGFont: TH '＋ Google' → '＋ ฟอนต์ Google' · EN '＋ Google' → '＋ Google Font' (ใช้ ＋ full-width เข้าชุดกับ btn.addFont '＋ Font') · TH/EN เดิมค่าเดียวกัน แยกแก้โดยตัดครึ่งที่ en:{ block
- แก้แค่ label i18n (lint #66 เช็ก key มีอยู่ ไม่ล็อกข้อความ · ไม่แตะ lint) · lint PASS 0/0 · sha 2c8acbb758ded233 · 6,912,336 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 15 ต.ค. 2026 (18:55) — ✅ เสร็จ: แก้หัว popover ให้ตรง tooltip + ใส่ tooltip โหลดฟอนต์บนปุ่ม "＋ ฟอนต์" (ผู้ใช้เลือกทั้ง 2)
- (1) gfont.title (หัว popover): → "เพิ่มฟอนต์จาก Google โดยต่อ internet (เฉพาะฟอนต์รองรับภาษาไทย-อังกฤษเท่านั้น)" · EN "Add fonts from Google over the internet (Thai–English-capable fonts only)" — ตรงกับ ttl.addGFont (tooltip ปุ่ม ＋ Google)
- (2) ttl.addFont (tooltip ปุ่ม ＋ ฟอนต์ อัปโหลด): → "เลือกไฟล์ฟอนต์ (.ttf/.otf/.woff/.woff2) ที่โหลดไว้ในเครื่อง · โหลดฟอนต์ฟรีเพิ่มได้จาก fonts.google.com" · EN "Choose a font file ... download free fonts at fonts.google.com" — บอกที่มาฟอนต์ (ผู้ใช้กังวลว่าคนใช้จะงงว่าหาฟอนต์ที่ไหน) · ลิงก์เป็นข้อความ hover (คลิกไม่ได้)
- แก้แค่ข้อความ i18n TH+EN (ไม่แตะ lint · #66 เช็ก key มีอยู่ ไม่ล็อกข้อความ) · lint PASS 0/0 · sha d9082d2dbcd37179 · 6,912,315 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 15 ต.ค. 2026 (18:05) — ✅ เสร็จ: เปลี่ยนข้อความ tooltip ปุ่ม "＋ Google" (ผู้ใช้เลือกประโยคเอง)
- ttl.addGFont: เดิม "เพิ่มฟอนต์จาก Google (ต่อเน็ตตอนเพิ่ม · ฝังในไฟล์ · ใช้ต่อออฟไลน์ได้)" → ใหม่ "เพิ่มฟอนต์จาก Google โดยต่อ internet (เฉพาะฟอนต์รองรับภาษาไทย-อังกฤษเท่านั้น)" · EN "Add fonts from Google over the internet (Thai–English-capable fonts only)"
- แก้แค่ข้อความ i18n TH+EN (lint #66 เช็ก key มีอยู่ ไม่ล็อกข้อความ · ไม่แตะ lint) · gfont.title (หัว popover) ยังเป็นคำเดิม — ยังไม่แตะ
- lint PASS 0/0 · sha 2edd87fcaecc86e0 · 6,912,227 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 15 ต.ค. 2026 (18:00) — ✅ เสร็จ: ลบโน้ต "ฟอนต์ทุกตัว...ฝังในไฟล์" ใต้แถบฟอนต์ (ผู้ใช้)
- เหตุ: ผู้ใช้แจ้งว่าโน้ตกินพื้นที่ส่วนอื่น · ลบ `.fontembed-note` (markup + CSS + i18n font.embedNote th+en) ทั้งหมด · ไม่มี JS อ้างถึง (เช็ก ripgrep: เหลือ 0)
- lint #67: ลบ check (b) embedNote + เอา font.embedNote ออกจาก i18n loop · กฎที่เหลือ (optgroup typoFontBase · upload dup _gfontFamExists · i18n baseGroup/fontDup) ยืนยันด้วย 3 variant ยัง FAIL ครบ · V0 PASS 0/0
- sha 420a5d9844fae2fd · 6,912,221 bytes · LF · อัปเดต UI_STANDARD §8.3 · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 15 ต.ค. 2026 (14:54) — ✅ เสร็จ: เปลี่ยนชื่อกลุ่ม dropdown "ฟอนต์ในไฟล์" → "ฟอนต์มากับแอป" (ผู้ใช้เลือก)
- เหตุ: ใต้แถบมีโน้ต "ฟอนต์ทุกตัวฝังในไฟล์" → ฟอนต์ที่เพิ่มก็อยู่ในไฟล์เหมือนกัน คำว่า "ฟอนต์ในไฟล์" จึงไม่แยกความต่าง + ขัดโน้ตตัวเอง · ความต่างจริงคือ "มากับแอป" vs "เพิ่มเอง" (เทียบ Word/PowerPoint "Theme Fonts")
- แก้ 3 จุด: label HTML (optgroup typoFontBase) + i18n TH 'ฟอนต์มากับแอป' + i18n EN 'Built-in fonts' · อัปเดต comment lint #67 + UI_STANDARD §8.3 ให้ตรงคำใหม่
- lint PASS 0/0 · sha 405c79218da3fdcf · 6,912,917 bytes · LF · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit

## 15 ต.ค. 2026 (12:50) — ✅ เสร็จ: โน้ต OFL มีลิงก์ไปหน้า SIL OFL (ผู้ใช้ · รวม Phase 3)
- เปลี่ยน '— ใช้/ฝัง/แจกฟรีได้' → '(SIL Open Font License ฝัง/แจก/ใช้เชิงพาณิชย์ได้ฟรี)' · 'SIL Open Font License' เป็นลิงก์
- ข้อจำกัด: โน้ตเดิมใช้ textContent (data-i18n) ใส่ `<a>` ไม่ได้ → รื้อเป็น 3 ชิ้น: span oflPre + a.oflink oflName + span oflPost · ลบคีย์ gfont.note ทิ้ง (ไม่มี caller)
- ลิงก์ href=openfontlicense.org/ofl-fonts/ target=_blank rel=noopener · สี #0b5fb0 น้ำเงิน (ไม่เขียว กฎ #1) · editor UI เท่านั้น (ไม่พิมพ์)
- lint #66: tuple gfont.note→oflPre/oflName/oflPost + เพิ่มเช็กลิงก์ (มี + target=_blank + rel=noopener) · ✅ menu_ofllink.html sha 393bfe896d36c125 · 6,912,904 bytes · V0 ผ่าน 2.7s (0/0) · variant V1-V5 FAIL ถูก
- git: cd C:\OE && git add OEIsanHotpotMenuEditor.html lint_oe.py UI_STANDARD.md SESSION_STATUS.md && git commit -m "fonts Phase 3: OFL note links to SIL Open Font License page (new tab, safe); split note into i18n pieces; lint #66"
- ⚠ กด F5 ก่อนทดสอบ · ยังไม่ทดสอบ/ยังไม่ commit

## 15 ต.ค. 2026 (12:40) — ✅ เสร็จ: ลดข้อความแจ้งฟอนต์ซ้ำให้สั้น (ผู้ใช้ · รวม Phase 3)
- ผู้ใช้: 'เลือกให้แล้ว' ทำให้งง — 'ฟอนต์ "X" มีอยู่แล้ว' พอ
- fl.gfontDup + fl.fontDup (th+en) → 'ฟอนต์ "{name}" มีอยู่แล้ว' / 'Font "{name}" already exists' · ตัด 'เลือกให้แล้ว'/'ไม่เพิ่มซ้ำ'/'selected it for you' ออก
- behavior ไม่เปลี่ยน: ตัวฟอนต์ยังถูกเลือกให้เงียบๆ (_gfontUse) · แค่ไม่ประกาศ
- ไม่แก้ lint (เปลี่ยนแค่ค่าข้อความคีย์เดิม) · ✅ menu_dupmsg.html sha e8f02e5c49f96ac0 · 6,912,439 bytes · V0 ผ่าน 2.7s (0/0)
- git: cd C:\OE && git add OEIsanHotpotMenuEditor.html SESSION_STATUS.md && git commit -m "fonts Phase 3: simplify duplicate-font message to 'already exists' (drop confusing 'selected it for you')"
- ⚠ กด F5 ก่อนทดสอบ · ยังไม่ทดสอบ/ยังไม่ commit

## 15 ต.ค. 2026 (12:30) — ✅ เสร็จ: กลุ่ม 'ฟอนต์ในไฟล์' + โน้ตฝังไฟล์ + upload เตือนซ้ำ (ผู้ใช้ · รวม Phase 3)
- (1) optgroup `typoFontBase` 'ฟอนต์ในไฟล์' ครอบ 3 ตัวมาตรฐาน (Prompt/Sarabun/Noto Sans Thai) · i18n font.baseGroup th+en
- (2) โน้ต `.fontembed-note` (font.embedNote) flex-basis 100pct ท้าย pane home → ตกบรรทัดใต้แถบ · 'ฟอนต์ทุกตัว...ฝังอยู่ในไฟล์'
- (3) upload เตือนซ้ำ: `_fontUploadFile` เช็ก `_gfontFamExists` → ซ้ำ=fl.fontDup+เลือกตัวเดิม ไม่เพิ่ม (ตรงกับ Google) · ลบ `_fontFamFromName` (เปลี่ยนชื่ออัตโนมัติ) → `_fontBaseName` (sanitize ล้วน ไม่มี dead code)
- lint #67 +5 เช็ก · ✅ menu_filefont.html sha cbb7cbf39dd0c054 · 6,912,616 bytes · V0 ผ่าน 2.6s (0/0) · variant V1-V5 FAIL ถูก
- git: cd C:\OE && git add OEIsanHotpotMenuEditor.html lint_oe.py UI_STANDARD.md SESSION_STATUS.md && git commit -m "fonts Phase 3: group base fonts as 'Fonts in file' optgroup + embed note under toolbar + upload duplicate-reject (match Google); lint #67"
- ⚠ กด F5 ก่อนทดสอบ · ยังไม่ทดสอบ/ยังไม่ commit

## 15 ต.ค. 2026 (12:15) — ✅ เสร็จ: ขยาย popover เพิ่มฟอนต์ Google ให้กว้างขึ้น (ผู้ใช้)
- `.gfont-pop` width 320px → 440px · `.gfont-prev` max-width 155px → 220px (ชื่อยาวเช่น 'IBM Plex Sans Thai Looped' + ตัวอย่างแสดงครบแถวเดียว)
- CSS 2 จุด · ไม่กระทบ logic/lint · delta 0 bytes (แค่เปลี่ยนตัวเลข px)
- ✅ ผล: menu_wide.html sha 56d816004ba550a0 · 6,911,614 bytes · lint V0 ผ่าน 2.7s (0/0)
- git: cd C:\OE && git add OEIsanHotpotMenuEditor.html SESSION_STATUS.md && git commit -m "fonts Phase 3: widen Google font picker popover 320->440px, preview 155->220px"
- ⚠ กด F5 ก่อนทดสอบ · ยังไม่ทดสอบ/ยังไม่ commit (รวม Phase 3)

## 15 ต.ค. 2026 (12:05) — ✅ เสร็จ: ปรับข้อความ label ช่องค้นหา + โน้ต OFL ให้เข้าใจง่าย (ผู้ใช้)
- gfont.inlbl: 'ค้นหาฟอนต์ไทยทั้งหมด' → 'ค้นหาฟอนต์จากรายการด้านบน' (สื่อ scope ชัด — ค้นเฉพาะในลิสต์) · EN 'Search the list above'
- gfont.note: เลิกสำนวน 'เดินทางไปกับไฟล์' → 'ฟอนต์ติดไปกับไฟล์ บันทึกแล้วเปิดเครื่องอื่นก็เห็นฟอนต์เดิม' · EN 'the font is saved inside the file, so it looks the same on any computer'
- แก้ markup note ที่ตกค้าง 'ส่วนใหญ่เป็นฟอนต์ OFL' (ไม่ตรง i18n 'ทุกฟอนต์') → sync ให้ตรง
- แก้ 6 จุด (markup 2 + i18n 4 th/en) · ไม่แก้ lint (แค่เปลี่ยนข้อความของคีย์เดิม)
- ✅ ผล: menu_lbl.html sha b37693cd1cdbecf6 · 6,911,614 bytes · lint V0 ผ่าน 2.6s (0/0)
- git: cd C:\OE && git add OEIsanHotpotMenuEditor.html SESSION_STATUS.md && git commit -m "fonts Phase 3: clearer search label (scope = list above) + plainer OFL/embed note; sync note markup"
- ⚠ กด F5 ก่อนทดสอบ · ยังไม่ทดสอบ/ยังไม่ commit (รวม Phase 3)

## 15 ต.ค. 2026 (11:45) — ✅ เสร็จ: ลิสต์ Google Fonts โชว์ครบทุกตัว (33) + โน้ต OFL เดียว
- เปลี่ยนหัวลิสต์ 'ฟอนต์แนะนำ (14)' → 'ฟอนต์ที่ใช้ได้ทั้งหมด (XX)' · `_gfontList` สร้างจาก `_GTHAI` ทั้งชุด (โชว์ครบ 33) · ย้าย `#gfontCount` ขึ้นหัวลิสต์ · ลบ `_GFONTS` (14 คัดเลือก) ทิ้ง
- โน้ต OFL เดียว (`gfont.note`): 'ทุกฟอนต์เป็น OFL — ใช้/ฝัง/แจกฟรีได้' — ไม่ต่อท้าย (OFL) ทุกแถว (ตรวจ repo google/fonts: 33 ตัวเป็น OFL หมด ไม่มีใน apache/ufl)
- ลบ srchnote (markup+i18n+CSS) — count ย้ายขึ้นหัวลิสต์แล้ว ไม่ต้องมีโน้ตซ้ำ
- lint #66 +เช็ก `_gfontList` ต้องใช้ `_GTHAI` · tuple srchnote→browsehint · ข้อความ gfontCount แก้→'หัวลิสต์'
- ✅ ผล: menu_allfonts.html sha 8d1460c65615abba · 6,911,361 bytes · lint V0 ผ่าน 2.6s (0/0) · variant V1-V4 FAIL ถูก (subset/no-count/hardcode/browsehint)
- git: cd C:\OE && git add OEIsanHotpotMenuEditor.html lint_oe.py UI_STANDARD.md SESSION_STATUS.md && git commit -m "fonts Phase 3: Google Fonts picker — full list of all Thai Google fonts (count XX), single OFL note, select-then-add, live previews, input cursor fix; lint #66"
- ⚠ กด F5 ก่อนทดสอบ · ยังไม่ทดสอบเบราว์เซอร์/ยังไม่ commit

## 15 ต.ค. 2026 (11:23) — ✅ เสร็จ: เพิ่ม note จำนวนฟอนต์ไทยใต้ช่องค้นหา (lint ผ่าน 0/0 · รอทดสอบเบราว์เซอร์ · รอ commit รวม Phase 3)
- ผู้ใช้ขอ (เห็นด้วย ทำทันที): เพิ่ม note บอกว่าค้นหาได้เฉพาะฟอนต์ไทยบน Google (ตอบคำถาม "ทำไม roboto ไม่เจอ")
- ตัดสินใจ: ตัวเลขดึงจาก _GTHAI.length อัตโนมัติ (ไม่พิมพ์ 33 ตายตัว — กันเลขโกหกถ้ารายการเปลี่ยน · หลักปุ่มไม่หลอก)
- baseline: Phase3 บนดิสก์ sha 4f7f3a18fcac5ab2 (6,911,154 bytes, LF) ยังไม่ commit (git ที่ e112736)
- แก้: (1) markup +<div.gfont-srchnote> ใต้ gfont-inrow มี <span id=gfontCount>33</span> + label (2) i18n gfont.srchnote th+en (3) _gfontOpen เติม gfontCount.textContent=_GTHAI.length (4) CSS .gfont-srchnote (5) lint #66 +เช็ก gfontCount/_GTHAI.length/i18n
- next: build → lint V0+variants → copy back → git commit Phase 3 รวมทั้งหมด
- ✅ ผล: menu_noteout.html sha f05f10e8a2e67a36 · 6,911,748 bytes · lint V0 ผ่าน 2.6s (0/0) · variant V1-V3 FAIL ถูกต้อง (no-gfontCount/no-_GTHAI.length-fill/en-srchnote)
- แก้: markup +.gfont-srchnote (#gfontCount เลข + label) ใต้ gfont-inrow · i18n gfont.srchnote th+en · _gfontOpen เติม gfontCount=_GTHAI.length · CSS .gfont-srchnote · lint #66 +เช็ก 3 จุด · UI_STANDARD 8.2.3
- git (commit Phase 3 รวมทั้งหมด): cd C:\OE && git add OEIsanHotpotMenuEditor.html lint_oe.py UI_STANDARD.md SESSION_STATUS.md && git commit -m "fonts Phase 3: Google Fonts picker — searchable list of 33 Thai Google fonts, select-then-add, live FontFace previews, neutral sample word, count note; fix input cursor; lint #66"
- ⚠ กด F5 ก่อนทดสอบ · ยังไม่ทดสอบเบราว์เซอร์/ยังไม่ commit

## 15 ต.ค. 2026 (10:00) — ✅ เสร็จ: Google picker ยกเครื่อง (คำตัวอย่าง+Search+2รายการ+select-then-add) — คำตัวอย่างใหม่ + Search + 2 รายการ + select-then-add (พับใน commit Phase 3 ที่ยังไม่ commit)
- ผู้ใช้แจ้ง 5 ข้อ (15 ต.ค. 9:40): (1) เปลี่ยนคำตัวอย่าง "อีสาน" (คำที่คนเหยียด) เป็นคำกลาง (2) ช่องค้นหาพิมพ์ได้แล้ว (3) ทำปุ่ม Search (4) แสดงผลค้นหาตรง+ใกล้เคียง ชื่อซ้าย/ตัวอย่างขวา คลิกเลือกได้ (5) ปุ่มเพิ่ม enabled เฉพาะตอนเลือกฟอนต์ (ทั้งรายการบน+ผลค้นหาล่าง) ไม่เลือก=disabled
- ผู้ใช้เลือกคำ: "เตี๋ยวหมูโคล้ง" (เป็นกลาง · วรรณยุกต์ ตี๋/ต้/ล้ + สระหน้า โ ครบ) → _GPREV_SAMPLE='เตี๋ยวหมูโคล้ง Aa' (วัดแล้ว 116px พอดีกล่อง 155px)
- โมเดลใหม่ = select-then-add แบบ Word/Google Fonts/VS Code: คลิกแถว=เลือก (ไฮไลท์) · ปุ่มเพิ่ม disabled จนกว่าเลือก · เลือกข้ามรายการ=ยกเลิกอีกรายการ (เลือกได้ทีละตัว)
- 2 รายการตามที่ผู้ใช้ระบุ: บน=#gfontList (14 ตัวคัดสรร "ฟอนต์แนะนำ") · ล่าง=#gfontResults (ผลค้นหา ซ่อนจนกว่าค้นหา)
- ค้นหาจาก _GTHAI = ฟอนต์ไทยทั้งหมดบน Google 33 ตัว (ยืนยันจาก gwfh /api/fonts subset thai=true · 34 ตัว ตัด "Google Sans" แบรนด์ฟอนต์ออก) bake ในไฟล์ · ค้นแบบ offline ได้ (กรองชื่อ) · โหลดจริงตอนกดเพิ่ม (ต่อเน็ต)
- _GTHAI 33: Anuphan Athiti BaiJamjuree ChakraPetch Charm Charmonman Chonburi Fahkwang IBMPlexSansThai IBMPlexSansThaiLooped Itim K2D Kanit KoHo Kodchasan Krub Maitree Mali Mitr Niramit NotoSansThai NotoSansThaiLooped NotoSerifThai Pattaya PlaypenSansThai Pridi Prompt Sarabun Sriracha Srisakdi Taviraj Thasadith Trirong
- search scoring: exact=4 prefix=3 substring=2 fuzzy(subsequence,len>=3)=1 · ไม่พบ=fl.gfontNoMatch · ตัวอย่างทุกแถว FontFace (ของบนจอ) โหลด batch
- baseline: Phase3+fix บนดิสก์ sha 29e63d37484ed433 (6,906,703 bytes, LF) — ยังไม่ commit (git ที่ e112736)
- แก้: swap gfont JS block (gfont_v3.js) · markup +gfont-sub(browselbl)+gfontResults+gfontSearchBtn, gfontAddBtn ย้ายลงล่าง full-width disabled · CSS +gfont-sub/.gfont-row.sel(ไฮไลท์น้ำเงิน ไม่ใช้เขียว)/.gfont-addbtn+:disabled · whitelist mousedown มี gfontInput แล้ว · _NOEDIT21 +gfontSearchBtn · buildEditorHtml เคลียร์ gfontResults+input+disable addBtn · i18n repurpose gfont.inlbl(ค้นหา)+gfont.add(เพิ่มฟอนต์ที่เลือก) +ใหม่ btn.gfontSearch/gfont.browselbl/fl.gfontNoMatch · lint #66 ขยาย
- next: build → lint V0+variants → UI_STANDARD 8.2.2 + SESSION_STATUS → file_copy กลับ → git commit Phase 3 รวมทั้งหมด (ยังไม่ทดสอบเบราว์เซอร์/ยังไม่ commit)
- ✅ ผล: menu_srchout.html sha 4f7f3a18fcac5ab2 · 6,911,154 bytes (6.591MB) · lint V0 ผ่าน 2.6s (0/0) · variant V1-V7 FAIL ถูกต้อง (addBtn-not-disabled/no-gfontResults/no-_gfontSearch/select-no-enable/searchBtn-bad-onclick/en-key/cursor-whitelist)
- คำตัวอย่าง: อีสาน Aa → เตี๋ยวหมูโคล้ง Aa (116px พอดี) · ชื่อร้าน 'โอ อีสาน แจ่วฮ้อน' ในเนื้อเมนูคงไว้ (ชื่อจริงร้าน)
- _GTHAI 33 ตัว bake · search scoring exact/prefix/substring/fuzzy · select-then-add · addBtn disabled→enabled on select · preview FontFace (บนจอ)
- git (commit Phase 3 รวมทั้งหมด): cd C:\OE && git add OEIsanHotpotMenuEditor.html lint_oe.py UI_STANDARD.md SESSION_STATUS.md && git commit -m "fonts Phase 3: Google Fonts picker — searchable list of all 33 Thai Google fonts, select-then-add (Add enabled only on selection), live FontFace previews, neutral sample word; fix input cursor; lint #66"
- ⚠ กด F5 ก่อนทดสอบ · กด ﹢Google: เห็นรายการแนะนำ ชื่อซ้าย/ตัวอย่างขวา · พิมพ์ในช่อง+กดค้นหา/Enter = ผลค้นหาด้านล่าง · คลิกแถว=ไฮไลท์ · ปุ่มเพิ่มสว่างเฉพาะตอนเลือก · กดเพิ่ม=ฟอนต์เข้า dropdown
- คิวค้าง: ปุ่ม emoji ชุดคัดสรร · GitHub publish + license + credit

## 15 ต.ค. 2026 (09:01) — ✅ เสร็จ: แก้ Google font picker — บั๊ก cursor + chips→list+ตัวอย่าง (lint ผ่าน 0/0 · รอทดสอบเบราว์เซอร์ · รอ commit รวม Phase 3)
- ผู้ใช้แจ้ง 2 เรื่อง (15 ต.ค. เช้า): (1) ช่องพิมพ์ชื่อฟอนต์ไม่รับ cursor พิมพ์ไม่ได้ (2) อยากให้รายการฟอนต์เป็น list ซ้าย=ชื่อ ขวา=ตัวอย่างฟอนต์จริง + scroll · เลือกจากรายการได้
- ผู้ใช้เลือก (decision): A — list + ตัวอย่างจริง
- ต้นเหตุบั๊ก cursor (ยืนยันจากโค้ด): ตัวดัก mousedown #typobar เรียก e.preventDefault() กับทุก element นอก whitelist (typoColor/typoHex/typoOlHex/typoCpDlgHex/typoSize/typoFont/typoLineStyle/OPTION) → gfontInput ไม่อยู่ใน whitelist → focus ถูกบล็อก = พิมพ์ไม่ได้ (บั๊กประเภทเดียวกับ dropdown เส้นจุด lint #35)
- baseline: Phase 3 บนดิสก์ (sha d9dc394954582387, 6,904,614 bytes, LF) — ยังไม่ commit (git ที่ e112736)
- แก้: (1) เพิ่ม gfontInput เข้า whitelist mousedown (saveSelection();return; เหมือน typoHex) (2) เปลี่ยน <div.gfont-chips#gfontChips> เป็น <div.gfont-list#gfontList> (3) _gfontChips→_gfontList (สร้าง row: span.gfont-name ซ้าย + span.gfont-prev ขวา ว่างไว้ก่อน) + _gfontPrevLoad (FontFace API โหลดตัวอย่าง 14 ฟอนต์ตอนเปิด · fetch css2 รวม 14 family ครั้งเดียว · แยก woff2 ต่อ family เลือก thai>latin · new FontFace(__gpprev_X) → document.fonts.add → เติม textContent+fontFamily) + _gfontPrevFam/_gfontRows/_gfontPrevDone (4) _gfontOpen เรียก _gfontList+_gfontPrevLoad (5) CSS chips→list (max-height scroll) (6) buildEditorHtml เคลียร์ #gfontList ตอนบันทึก
- เหตุผล FontFace API ไม่ใช่ <link>/<style>: FontFace ที่ add ผ่าน JS ไม่ถูก serialize ลง outerHTML/cloneNode → ตัวอย่างไม่รั่วลงไฟล์ที่บันทึก (ของบนจอล้วน) · ตัวอย่างว่างถ้าโหลดไม่ได้/ออฟไลน์ = ไม่โชว์ของปลอม (ซื่อสัตย์)
- lint #66 เพิ่มเช็ก: gfontInput ใน whitelist mousedown · #gfontList มี · _gfontList/_gfontPrevLoad มี · FontFace preview (ของบนจอ)
- next: build menu_fixout.html → lint V0+variants → UI_STANDARD 8.2 (ปรับส่วน list) + SESSION_STATUS → file_copy กลับ → git commit Phase 3 รวมแก้นี้ (ยังไม่ทดสอบเบราว์เซอร์/ยังไม่ commit)
- ✅ ผล: menu_fixout.html sha 29e63d37484ed433 · 6,906,703 bytes (6.587MB) · lint V0 ผ่าน 2.6s (0/0) · variant V1-V5 FAIL ถูกต้อง (cursor-whitelist/no-gfontList/no-_gfontPrevLoad/no-FontFace/cdn-link)
- แก้ 6 จุด: (1) whitelist mousedown +gfontInput (2) markup gfont-chips→gfont-list (3) swap gfont JS block (เพิ่ม _gfontList/_gfontPrevLoad/_gfontPrevFam/_gfontRows/_gfontPrevDone · _gfontOpen เรียก list+prevload) (4) CSS chips→list (max-height:220 scroll · .gfont-row/.gfont-name/.gfont-prev) + popover 290→320px (5) buildEditorHtml เคลียร์ #gfontList (6) lint #66 +เช็ก cursor/list/FontFace
- preview: FontFace API (ของบนจอ ไม่ serialize) · เริ่มว่าง เติมเมื่อโหลดเสร็จ · ออฟไลน์=ชื่อครบ กดได้ ตัวอย่างว่าง
- git (commit Phase 3 รวมแก้นี้): cd C:\OE && git add OEIsanHotpotMenuEditor.html lint_oe.py UI_STANDARD.md SESSION_STATUS.md && git commit -m "fonts Phase 3: Google Fonts picker (fetch woff2, embed base64, travels with file; all browsers) — list view w/ live previews (FontFace, screen-only) + type-name input; fix typobar mousedown blocking input cursor; lint #66 + #64 refine"
- ⚠ กด F5 ก่อนทดสอบ · กดปุ่ม ﹢Google → เห็น list ชื่อซ้าย/ตัวอย่างขวา เลื่อนได้ · พิมพ์ชื่อในช่องได้แล้ว · คลิกแถว/กดเพิ่ม = ฟอนต์เข้า dropdown · ตัดเน็ต=ตัวอย่างว่าง+กดขึ้นต้องต่อเน็ต
- คิวค้าง: ปุ่ม emoji ชุดคัดสรร · GitHub publish + license + credit

## 14 ต.ค. 2026 (22:40) — ✅ เสร็จ Phase 3: เลือกฟอนต์จาก Google (แบบ B ดึง woff2 มาฝัง · ทุกเบราว์เซอร์ · เดินทางไปกับไฟล์) · lint ผ่าน 0/0 · รอทดสอบเบราว์เซอร์ · รอ commit
- ตัดสินใจ (user): ข้าม Phase 2 (ฟอนต์ในเครื่อง queryLocalFonts — Chromium-only) · ทำ Google แทน · แบบ B (ดึง woff2 ฝัง · ทุกเบราว์เซอร์ · เดินทางไปกับไฟล์) ไม่ใช่แบบ A (link online)
- CORS ทดสอบผ่าน: font_cors_test.html เปิดจาก file:// → fetch CSS+woff2 จาก Google = HTTP 200 (ไม่ถูก CORS บล็อก) · user ยืนยันแถบเขียว 14 ต.ค. 22:29 · ลบไฟล์ทดสอบแล้ว
- baseline: commit e112736 (sha b601ce2c81cde5d0, 6,894,394 bytes, LF)
- ยืนยันฟอนต์ไทยคัดสรรมีจริงบน Google (gwfh API, subset thai=true): Chakra Petch/Charm/Charmonman/Fahkwang/IBM Plex Sans Thai/K2D/Kodchasan/Krub/Mali/Niramit/Pridi/Sriracha/Thasadith/Athiti/Maitree/Trirong/Chonburi/Itim + Kanit/Mitr/Bai Jamjuree (ตัวที่ตัดจากชุดฝัง — ดึงผ่าน Google ได้)
- chips คัดสรร 14 ตัว: Kanit, Mitr, Bai Jamjuree, Chakra Petch, K2D, Krub, Mali, Niramit, Pridi, Charm, Charmonman, Sriracha, Itim, Chonburi
- โครงที่เพิ่ม: ปุ่ม #btnAddGFont "﹢ Google" + popover #gfontPop (chips + ช่องพิมพ์ชื่อ + ข้อความสถานะ inline + note) · ฟังก์ชัน _gfontToggle/_gfontOpen/_gfontClose/_gfontChips/_gfontMsg/_gfontPickInput/_gfontFamExists/_gfontUse/_gfontAdd/_ab2b64 + helper _fontAddOpt (refactor _fontUploadFile ให้ใช้ร่วม) · fetch css2 wght@400;700 → กรอง @font-face เฉพาะ thai+latin (ตาม unicode-range) → fetch woff2 แต่ละตัว → _ab2b64 → rewrite url() เป็น data: → ฝังใน #userFonts (ท่อ Phase 1) → เพิ่ม option → markDirty → เลือกใช้ทันที
- offline/error: fetch ล้ม=fl.gfontOffline · ไม่พบฟอนต์(ไม่ ok/ไม่มี block)=fl.gfontNotFound · ซ้ำ=fl.gfontDup (เลือกตัวเดิมให้) · โหลด=fl.gfontLoading · สำเร็จ=fl.gfontAdded
- ⚠ แก้ lint #64: ห้าม googleapis/gstatic เฉพาะ "นอก <script>" (strip script ก่อนเช็ก) — เพราะ fetch รันไทม์ใน JS ต้องมี URL googleapis (ไม่ใช่ <link>/@import dependency) · ยังห้าม <link>/@import CDN เหมือนเดิม
- lint ใหม่ #66: ปุ่ม #btnAddGFont + _gfontToggle · ฟังก์ชัน _gfontAdd/_gfontOpen/_gfontClose/_ab2b64/_fontAddOpt · _gfontAdd ต้อง fetch + data: + userFonts + markDirty + fl.gfontOffline + fl.gfontNotFound · buildEditorHtml strip #gfontPop open · i18n ครบ th+en
- next: build menu_g3out.html → lint V0+variants → UI_STANDARD 8.2 + SESSION_STATUS → file_copy กลับ → git commit (ยังไม่ทดสอบเบราว์เซอร์/ยังไม่ commit)
- ✅ ผล: menu_g3out.html sha d9dc394954582387 · 6,904,614 bytes (6.585MB) · lint V0 ผ่าน 2.8s (0/0) · variant V1-V7 FAIL ถูกต้อง (cdn-link/no-toggle/no-markDirty/no-offline-handler/no-userFonts-embed/en-key/no-gfontPop-strip)
- โครงที่เพิ่ม: ปุ่ม #btnAddGFont + popover #gfontPop (chips 14 + ช่องพิมพ์ชื่อ label .gfont-inlbl ไม่ใช้ placeholder + #gfontMsg + note) · ฟังก์ชัน _gfontToggle/_gfontOpen/_gfontClose/_gfontChips/_gfontMsg/_gfontPickInput/_gfontFamExists/_gfontUse/_gfontAdd/_ab2b64 + helper _fontAddOpt (refactor _fontUploadFile ใช้ร่วม) · CSS .gfont-* · i18n 12 key th+en
- lint: ปรับ #64 (ห้าม googleapis/gstatic นอก <script> + ห้าม <link>/@import) · เพิ่ม #66 · ใส่ btnAddGFont+gfontAddBtn ใน _NOEDIT21 · เพิ่ม gfontInput ใน _FILTERED16 (ฟรีเท็กซ์ชื่อฟอนต์) · UI_STANDARD เพิ่ม 8.2
- CORS: ยืนยันแล้ว fetch file://→Google = 200 ทุกเบราว์เซอร์ (font_cors_test.html ลบแล้ว)
- git: cd C:\OE && git add OEIsanHotpotMenuEditor.html lint_oe.py UI_STANDARD.md SESSION_STATUS.md && git commit -m "fonts Phase 3: add Google Fonts picker (fetch woff2, embed base64, travels with file; all browsers) + curated Thai chips; lint #66 + #64 refine"
- ⚠ กด F5 ก่อนทดสอบ · กดปุ่ม ﹢Google → เลือก chip หรือพิมพ์ชื่อ (ต่อเน็ต) → ฟอนต์โผล่ใน dropdown ใช้ได้ · ลองตัดเน็ตแล้วกด = ขึ้น 'ต้องต่อเน็ต' (ปุ่มไม่หลอก) · บันทึก Editor เปิดใหม่ = ฟอนต์ยังอยู่
- คิวค้าง: ปุ่ม emoji ชุดคัดสรร · GitHub publish + license + credit

## 14 ต.ค. 2026 (13:09) — ✅ เสร็จ+COMMITTED e112736 (14 ต.ค. 22:34): Phase 0+1 ฐานทะเบียนฟอนต์ + อัปโหลด .ttf ฝังเอง (lint ผ่าน 0/0 · user ยืนยัน Kanit-Black อัปโหลดโผล่ใน dropdown ใช้ได้)
- ตัดสินใจ (user, 14 ต.ค.): ทำครบ 3 แหล่งฟอนต์ (อัปโหลดเอง + ฟอนต์ในเครื่อง Windows + online Google) · agent แบ่ง 4 phase, ทำทีละ commit · เริ่ม Phase 0+1 ก่อน
- Phase 0 (ฐาน): เพิ่ม <style id="userFonts"> ใน <head> ว่างๆ (ฟอนต์อัปโหลดไปอยู่ที่นี่ · เดินทางไปกับไฟล์ผ่าน cloneNode ทั้ง buildMenuHtml/buildEditorHtml ที่ยืนยันแล้วว่า clone documentElement) + <optgroup id="typoFontUser"> ใน #typoFont
- Phase 1 (อัปโหลด): ปุ่ม btn.addFont "﹢ ฟอนต์" ในกลุ่ม fontgrp + <input type=file id=fontInput accept .ttf/.otf/.woff/.woff2> ซ่อน · fontUploadPick()+_fontUploadFile(f): validate ชนิด → อ่าน base64 → ฝัง @font-face ใน #userFonts → เพิ่ม <option> ใน optgroup → document.fonts.load → apply กับ selection → markDirty + flashStatus
- ที่มา baseline: commit bb61d86 (sha fbc21d9149217d36, 6,890,318 bytes, LF) — ยืนยันตรงแล้ว
- การ serialize: ฟอนต์ฝังอยู่ใน <head> ไม่ใช่ .page → _serializePages/POOL (autosave ร่าง) ไม่เก็บ bytes ฟอนต์ → crash ก่อนบันทึก Editor = ฟอนต์หาย (เหมือนรูปที่เพิ่งเพิ่ม lint #63) — ข้อจำกัดที่ยอมรับ บอก user แล้ว
- naming: ชื่อจากชื่อไฟล์ (ตัดนามสกุล) sanitize + กันซ้ำกับ option เดิม
- lint ใหม่ #65: <style id="userFonts"> ต้องมี + ห้ามถูก strip ใน build ทั้งสอง + fontUploadPick/_fontUploadFile ต้องมี + validate ชนิด + markDirty + <input id=fontInput> + i18n btn.addFont/ttl.addFont/fl.fontAdded/fl.fontBadType/fl.fontAddErr/font.userGroup ครบ th+en
- next: build menu_fontout.html → lint V0+variants → UI_STANDARD ข้อ 8 (เพิ่มส่วนอัปโหลด) + SESSION_STATUS → file_copy กลับ → git commit (ยังไม่ทดสอบเบราว์เซอร์/ยังไม่ commit)
- ✅ ผล: menu_fontout.html sha b601ce2c81cde5d0 · 6,894,394 bytes (6.575MB) · lint V0 ผ่าน 2.9s (0/0) · 8 variant (userFonts style/buildMenu strip/no markDirty/no optgroup/no type-check/en key/fontInput .ttf/no fontUploadPick) FAIL ถูกต้องที่ #65
- โครงที่เพิ่ม: <style id=userFonts> หลัง </style> หลัก · <optgroup id=typoFontUser data-i18n-label=font.userGroup> ใน #typoFont · ปุ่ม #btnAddFont + <input id=fontInput> หลัง </select> · applyLang +handler [data-i18n-label] · ฟังก์ชัน fontUploadPick/_fontUploadChange/_fontFmt/_fontFamFromName/_fontUploadFile หลัง typoFontApply · i18n 6 key (btn.addFont/font.userGroup/ttl.addFont/fl.fontAdded/fl.fontBadType/fl.fontAddErr) th+en
- lint: เพิ่ม #65 + ใส่ btnAddFont ใน _NOEDIT21 (เปิด dialog · markDirty อยู่ใน _fontUploadFile) · UI_STANDARD เพิ่มหัวข้อ 8.1
- ข้อจำกัด: ฟอนต์อัปโหลดเดินทางกับไฟล์ที่บันทึกเท่านั้น · crash ก่อนบันทึก = หาย (เหมือนรูป lint #63) — บอก user แล้ว
- git: cd C:\OE && git add OEIsanHotpotMenuEditor.html lint_oe.py UI_STANDARD.md SESSION_STATUS.md && git commit -m "fonts Phase 0+1: upload-your-own TTF/OTF/WOFF embed (travels with file) + font registry (userFonts style + optgroup); lint #65"
- ⚠ กด F5 ก่อนทดสอบ · ลองกดปุ่ม ﹢ฟอนต์ เลือก .ttf → ต้องเพิ่มใน dropdown ใช้ได้ · บันทึก Editor แล้วเปิดใหม่ ฟอนต์ต้องยังอยู่ · Phase 2/3 (ฟอนต์เครื่อง/online) ยังไม่ทำ

## 13 ต.ค. 2026 (23:18) — ✅ เสร็จ+COMMITTED bb61d86 (14 ต.ค. 13:07): ฝังฟอนต์ offline (TTF base64) + ตัด dropdown เหลือ 3 ฟอนต์ (lint ผ่าน 0/0 · user ยืนยัน dropdown 3 ตัว+สลับฟอนต์ทำงาน · ยังรอทดสอบ airplane-mode offline)
- เป้าหมาย: ทำให้ฟอนต์ offline จริง (ไม่พึ่ง Google CDN) สำหรับ publish GitHub · README จะเขียน "offline" ได้เต็มปาก
- ตัดสินใจ (user, 13 ต.ค.): ฝัง 3 ฟอนต์ที่มีหน้าที่จริงในโค้ด — Prompt (เนื้อหาหลัก) · Sarabun (หมายเหตุ .crab) · Noto Sans Thai (แก้วรรณยุกต์ลอย .kai) · ตัด Kanit/Mitr/Bai Jamjuree (ทรงซ้ำ Prompt/Sarabun, อยู่ใน dropdown เฉยๆ ไม่มีจุด CSS อ้าง) · ไม่ฝัง emoji (Color Emoji 24MB แพงเกิน, ระบบ OS วาดเอง)
- วิธี: (1) ลบ <link> fonts.googleapis/gstatic 3 เส้น (2) ฝัง @font-face 10 บล็อก base64 TTF ต้น <style> — Prompt 400/500/600/700 · Sarabun 400/600/700 · Noto 400/500/700 (3) ตัด option Kanit/Mitr/Bai Jamjuree ใน #typoFont เหลือ 3 (4) ไม่ใส่ unicode-range (ฝัง TTF เต็ม ครอบ latin+thai)
- ที่มาฟอนต์: TTF จาก C:\OE\Fonts\ (user โหลดจาก fonts.google.com ปุ่ม Download family) · ยืนยัน sfnt tag ถูกต้องทั้ง 10 · base64 รวม 1.355MB
- sha ก่อนแก้: 7de77705639f7e30 (5,468,894 bytes, LF) · ไฟล์ประเมินหลังฝัง ~6.57MB
- lint ใหม่ #64 (offline fonts: ห้ามมี googleapis/gstatic · ต้องมี @font-face Prompt/Sarabun/Noto · dropdown ห้ามมี Kanit/Mitr/Bai Jamjuree)
- next: build menu_out.html → lint V0+variants → UI_STANDARD + SESSION_STATUS → file_copy กลับเครื่อง → git commit (ยังไม่ทดสอบเบราว์เซอร์/ยังไม่ commit)
- ✅ ผล: menu_out.html = 6,890,318 bytes · sha fbc21d9149217d36 · lint V0 ผ่าน 4.1s (0 error 0 warning) · 5 variant (googleapis/gstatic/Kanit-opt/no-Prompt-face/no-Noto-opt) FAIL ถูกต้องที่ #64
- ⚡ แก้ประสิทธิภาพ lint: ฝัง @font-face แล้ว lint เดิม timeout (>200s) เพราะ rule 43 (`[^{}\n]*:active`) backtrack O(n²) บนบรรทัด base64 220KB → แก้โดยตัด @font-face ออกจาก `_css`/`_css25`/`_css36` 3 จุด (ฟอนต์ฝังไม่ใช่ CSS จัดหน้า) → lint กลับมา 4s
- lint ข้อ 64 ใหม่: ห้าม googleapis/gstatic · ต้องมี @font-face Prompt/Sarabun/Noto · dropdown ห้ามมี Kanit/Mitr/Bai Jamjuree + ต้องมี 3 ตัวที่เก็บ · UI_STANDARD เพิ่มข้อ 8
- git: cd C:\OE && git add OEIsanHotpotMenuEditor.html lint_oe.py UI_STANDARD.md SESSION_STATUS.md && git commit -m "offline fonts: embed 3 TTF base64, drop Google CDN link, trim font dropdown to 3 (lint #64 + perf fix)"
- ⚠ กด F5 ก่อนทดสอบ (อย่ากด Save จากหน้าเดิม) · เทียบหน้าตาฟอนต์ให้เหมือนเดิม · git ย้อนได้ถ้าไม่โอเค

## 13 ต.ค. 2026 (19:40) — ✅ Autosave ร่างกันงานหาย · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha 4bc422453b4f15ea → 7de77705639f7e30
- ผู้ใช้เลือก (decision 19:20): ทำ autosave กันงานหาย (ข้อ 1 จากที่ agent เสนอ · เป็นสิ่งเดียวที่แนะนำว่าคุ้ม)
- ดีไซน์: ต่อยอดระบบ snapshot เดิม · _serializePages คืน HTML บีบอัด (รูป=data-pool id ไม่เก็บ base64 → KB) · ตอนโหลด _lastSnap=_serializePages เติม POOL ด้วย base64 ของไฟล์ → ร่างกู้รูปกลับได้
- แก้ html 6 กลุ่ม: (1) +ฟังก์ชัน _draftKey/_draftSave/_draftClear/_draftRestore/_draftDiscard/_draftOffer ท้าย _takeSnapshot (2) hook _draftSave() ใน _takeSnapshot (3) _draftClear() ใน clearDirty (4) _draftOffer() ใน load handler (5) strip #draftBar ใน buildEditorHtml+buildMenuHtml (6) i18n draft.*/fl.draft* th+en + CSS #draftBar (แถบล่างกลางจอ กู้คืน/ละทิ้ง · @media print ซ่อน)
- กลไก: เก็บร่างทุกครั้งที่แก้ (ผ่าน _takeSnapshot debounce 500ms) key oe_draft_<ไฟล์> · บันทึกไฟล์สำเร็จ=ลบร่าง · เปิดไฟล์เจอร่าง=เสนอกู้คืน (ไม่ auto) · กู้คืนใช้ _restorePages + ดรอปรูปที่ POOL ไม่มี (รูปเพิ่มใหม่ยังไม่บันทึก) แจ้งจำนวน
- จุดจำกัด (บอกผู้ใช้แล้ว): รูปเพิ่มใหม่ระหว่างยังไม่บันทึกแล้วเครื่องดับ กู้พิกเซลไม่ได้ (base64 ไม่อยู่ในไฟล์) · กู้ข้อความ/ตำแหน่ง/โครงสร้างได้ครบ
- lint #63 ใหม่ (5 ฟังก์ชัน + hook 3 จุด + strip 2 build + _restorePages + i18n th+en + CSS) · V0 ผ่าน · ทดสอบบั๊ก 6 แบบจับครบ · brace 2529:2529
- git: layer ต่อจาก commit 48af6f4 (docs verify_oe) · เปลี่ยน 4 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS
- วิธี: workspace menu_work.html + lint_oe_cur.py · copy กลับ sha ตรง 7de77705639f7e30

## 13 ต.ค. 2026 (19:05) — ✅ ปิดเรื่อง verify_oe.py (ตัดสินใจ: ไม่เอาเข้า pre-commit hook) · ไม่แตะโค้ด/lint · เปลี่ยนเฉพาะ SESSION_STATUS
- ผู้ใช้ยืนยัน (decision 19:01): ไม่เอา verify_oe.py เข้า pre-commit hook ตามที่ agent แนะนำ
- เหตุผล: (1) หนัก — ต้อง Chrome headless + subprocess ทุก commit (2) fail-closed — Chrome ไม่พร้อม = บล็อก commit ทั้งที่โค้ดไม่ผิด (3) ซ้ำซ้อน — lint 62 ข้อจับ regression เชิงโครงสร้างครบแล้ว
- บทบาทลงตัว: lint_oe.py = pre-commit hook (เบา เร็ว fail-safe) · verify_oe.py = รันเอง manual ตอนตรวจ runtime ลึก
- backlog app เมนู: เคลียร์หมด · เหลือเฝ้าดู 1 เรื่อง (รูป add หายตำแหน่ง — รอค่า Y ถ้าเจออีก) · save เป็นรูป = ผู้ใช้ตัดสินใจไม่ทำ (ทำออกจาก app ตรงๆ ไม่ได้)

## 13 ต.ค. 2026 (17:30) — ✅ แนว B: คำเตือนกรอกช่อง input ไม่จดประวัติ (แสดงแถบล่างอย่างเดียว) · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha 70f9f8e4f4896b60 → 4bc422453b4f15ea
- ผู้ใช้ถามเรื่อง log ซ้ำ (3 แถวเวลาเดียว) → agent ยืนยันว่าแสดงตามจำนวนครั้งจริง ไม่ใช่บั๊ก (1 keystroke = 1 warning = 1 แถว · log ล้นหน้ามี guard _was/_prev) · ผู้ใช้เสนอ coalesce ต่อ run → agent เสนอ 2 แนว (A coalesce / B ไม่ log) → ผู้ใช้เลือก B
- หลักการ B: การพิมพ์ตัวที่ช่องไม่รับ = input validation ไม่ใช่ action → ไม่จดประวัติ (เหมือน Word/Excel/form validation) · ประวัติเก็บเฉพาะการกระทำจริง
- ตรวจก่อนแก้: ไล่ call context ทุกคีย์เตือน input-filter → ยืนยันแต่ละคีย์ใช้เฉพาะใน filter (prWarn/_bulkPriceCleanInput/hex input×3/size input/shd input/txtWarn/pages onFiltered) ไม่ซ้ำ action จริง → denylist by key ปลอดภัย
- แก้ html 1 จุด: เพิ่ม var _NOLOG={20 คีย์} + guard ใน _logFromFlash: if(msg._k && _NOLOG[msg._k]) return; ก่อน logAdd · คำเตือนยังแสดงแถบล่าง (flashStatus→_renderStatus) แค่ไม่ logAdd · ไม่แตะ call site ไหนเลย (จุดเดียว centralized)
- _NOLOG: prNumOnly/prTooLong/amtNumOnly/amtTooLong/hexOnly/hexOnlyTh/sizeOnly/sizeOnlyTh/sizeRange/sizeStep/shdOnly/shdOnlyTh/shdRange/pagesOnly/pagesOnlyTh/pagesFull/pagesTooLong/txtLines/txtNoEnter/txtTooLong · ข้อยกเว้น fl.sizeLimit (ปุ่ม +/− = action ปุ่ม คงจด)
- lint #62 ใหม่ (_NOLOG มีครบ 20 คีย์ + ไม่มี sizeLimit + _logFromFlash มี guard) · V0 ผ่าน · ทดสอบบั๊ก 4 แบบจับครบ
- git: layer ต่อจาก #61 (⚠ ซ้ำ · ยังไม่ commit · disk 70f9f8e4) → #61+#62 ควร commit รวมเป็นชุด activity-log refinement · เปลี่ยน 4 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS
- วิธี: workspace menu_work.html + lint_oe_cur.py · copy กลับ sha ตรง 4bc422453b4f15ea

## 13 ต.ค. 2026 (16:10) — ✅ แก้ไอคอน ⚠ ซ้ำในแถบล่าง/ประวัติ (เอา ⚠️ ออกจากข้อความ i18n) · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha ddde2a62670a3dc7 → 70f9f8e4f4896b60
- ผู้ใช้เลือกจาก backlog (decision 16:04): แก้ ⚠ ซ้ำ (ข้อ 1 จาก 3 ข้อเก่า 9 ต.ค. · ข้อ 3 ชื่อเมนู 17px = ไม่ใช่บั๊ก ปิดไป · ข้อ 2 ประวัติถี่ = รอ user ระบุเคส)
- root cause: แถบล่าง (_renderStatus edstatusIc) + ประวัติ (_actlogIcon บรรทัด 3970/3976) ต่าง render ไอคอนตามชนิดเอง (warning→⚠️ error→⛔ edit→✏️ อื่น→•) · แต่ข้อความ i18n 44 คีย์ (88 ค่า TH+EN) ขึ้นต้นด้วย ⚠️ อีก = ซ้ำทั้ง 2 ที่ (สามเหลี่ยม 2 อัน)
- ตรวจ call type ทุกคีย์ก่อนแก้: ส่วนใหญ่ flashStatus('warning') · fl.imgCopyFail/imgPosCopyFail = ok?'info':'warning' (เคส fail=warning) · fl.noHighlight = info-type (ไอคอนวงกลม+⚠️ = ขัดกัน)
- แก้ html: เอา ⚠️/⛔ นำหน้าออกจากทุกค่า i18n ยกเว้น st.overflowPill (แสดงในป้าย edstatus-meta ที่ไม่มี element ไอคอน → ⚠️ เป็นเครื่องหมายตัวเดียว) · regex strip 88 instances/44 keys · st.overflow ไม่มี ⚠️ อยู่แล้ว (pattern ถูก) · fl.noHighlight เอาออกด้วย (กฎ #6)
- lint #61 ใหม่: scan ค่า i18n ห้ามขึ้นต้น ⚠️/⛔ ยกเว้น allowlist {st.overflowPill} · V0 ผ่าน · ทดสอบบั๊ก 3 แบบจับครบ (⚠️ กลับมา 2 คีย์ + ⛔)
- delta -264 bytes · braces สมดุล · git: layer ต่อจาก commit c0dbfb4 (#59/#60) · เปลี่ยน 4 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS
- วิธี: workspace menu_work.html + lint_oe_cur.py · copy กลับ sha ตรง 70f9f8e4f4896b60

## 13 ต.ค. 2026 (12:55) — ✅ เตือนล้นหน้า: tolerance 3mm + เตือนเฉพาะตอนแก้ไข + หมายเหตุเล็กตอนเปิดไฟล์ · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha d667219bb396a2fe → ddde2a62670a3dc7
- ผู้ใช้วัดจริง (Console): หน้า1 เกิน 0.00mm · หน้า2 เกิน 11px=2.91mm → หน้า2 ล้นจริง (ไม่ใช่ false positive จากฟอนต์ · #58 แก้ผิดจุด สมมติฐานฟอนต์ผิด) · #59 (margin section ท้าย) ลดเหลือ ~0.5-2px
- ผู้ใช้สั่ง 3 ข้อ: (1) ขอบล่าง ~3mm — เกิน 3mm ค่อยเตือน (2) เตือนเฉพาะตอนแก้ไขที่ยังไม่ save · เปิดไฟล์/หลัง save = พร้อมใช้งาน (3) มี * หรือหมายเหตุเล็กบอกหน้าที่เกินขอบ
- แก้ html 7 จุด: (1) var _OVF_TOL=Math.round(3*96/25.4)=11px (2) checkOverflow เทียบ +_OVF_TOL + กรอบทอง if(_dirty) (3) chain bad.length gate ด้วย if(_dirty){เตือนเต็ม}else{_overflowWarn=false·หมายเหตุเล็ก} (4) _renderStatus pill: _overflowWarn→ovf(ส้ม) / ไม่→ovfnote(จางเอียง) · แสดงเมื่อ _overflowPages.length (5) CSS .edstatus-meta.ovfnote (6) i18n st.overflowNote/NoteTtl TH+EN (7) clearDirty เรียก checkOverflow() refresh หลัง save
- ไม่แตะสูตรวัด: #28/#28b (_ovfFresh=true/_ovfCombine/mode strings/finally ยังอยู่) · #34 padding คงเดิม · #58/#59 ยังอยู่ (layer ร่วมกัน)
- lint #60 ใหม่ (ก tolerance 3mm · ข กรอบทอง+คำเตือน gate _dirty · ค หมายเหตุเล็ก ovfnote · ง clearDirty refresh · จ i18n+CSS) · V0 ผ่าน · ทดสอบบั๊ก 8 แบบจับครบ
- ผล: เปิดไฟล์ → หน้า2 (~0.5-2px < 3mm) ไม่ flag เลย = พร้อมใช้งาน ไม่มีกรอบ/คำเตือน/pill · หน้าที่เกิน >3mm → เปิดไฟล์ขึ้นหมายเหตุเล็ก · แก้ไข → เตือนเต็ม
- git: layer ต่อจาก #59 (ยังไม่ commit · disk d667219b) → รวมเป็น commit เดียวหรือแยก? เปลี่ยน 4 ไฟล์ · ⚠ ขอผู้ใช้วัดซ้ำ Console ยืนยันก่อน commit (เคยเดาผิด 2 รอบ)
- วิธี: workspace menu_work.html + lint_oe_cur.py · copy กลับ sha ตรง ddde2a62670a3dc7

## 13 ต.ค. 2026 (12:00) — ✅ แก้ false positive เตือนล้นหน้าตอนเปิด (รอ document.fonts.ready) · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha a889e9d68e2b430e → 2060d74d3c30f7c1
- ผู้ใช้แจ้ง (ภาพ 2 ใบ): เปิดไฟล์มา warning เด้งทันทีว่าหน้า 2 จะล้น ทั้งที่ยังไม่ล้น (มีที่ว่างท้ายหน้า) + กรอบทอง 3mm ดูไม่เรียบร้อย → อยากให้เตือนเฉพาะตอนล้นจริง
- root cause: window.load (บรรทัด 1793) เรียก checkOverflow() ทันที · ฟอนต์เว็บ (Google Fonts display=swap) โหลด async ยังไม่มา → วัดด้วย fallback ระบบ (ตัวไทยสูงกว่า Sarabun) → เกิน 297mm → เตือน+กรอบทองผิด · ฟอนต์ swap มาเนื้อหาหด แต่ไม่ตรวจซ้ำ = ค้าง · โค้ดไม่เคยมี document.fonts/fonts.ready (count=0)
- แก้ html 1 จุด (window.load handler): แยก checkOverflow() ครั้งแรกออกจาก init อื่น → เรียกผ่าน document.fonts.ready.then(checkOverflow) · fallback else checkOverflow() ถ้าไม่มี document.fonts (เบราว์เซอร์เก่า) · init อื่น (renumber/_lastSnap/_updateUndoButtons/_initDragReorder) คงรันทันที
- กรอบทอง 3mm (.overflowed outline #e8a020) ผูกกับผลตรวจเดียวกัน → false positive หายไปด้วย (ไม่ขึ้นตอนไม่ล้นจริง) · ไม่แตะสูตรวัด/กรอบทอง
- lint #58 ใหม่ (load handler ต้องมี document.fonts.ready + .then(checkOverflow) + else fallback) · V0 ผ่าน · ทดสอบบั๊ก 2 แบบจับครบ
- git: layer ต่อจาก commit b7f998c (จำสีขอบล่าสุด) · เปลี่ยน 4 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS
- วิธี: workspace menu_work.html + lint_oe_cur.py · copy กลับ sha ตรง 2060d74d3c30f7c1 · (คอมเมนต์ไทยพิมพ์ escape ผิดรอบแรก fail ก่อนเขียน → แก้เป็นอักษรไทยตรงๆ)

## 13 ต.ค. 2026 (11:30) — ✅ จำสีขอบ/ความหนาล่าสุด (_olLastC/_olLastW) ข้าม reload · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha 888b803edce46363 → a889e9d68e2b430e
- ผู้ใช้เลือกจาก backlog (decision 11:27): จำสีขอบล่าสุดข้าม reload · agent บอกตรงว่าคุณค่าต่ำ (สีที่ใส่แล้วอยู่ในไฟล์ · จานสี custom จำแล้ว) เหลือแค่ความสะดวก _olLastC/_olLastW ที่ reset ตอน reload — ผู้ใช้เลือกทำ
- วิเคราะห์: _olLastC/_olLastW set กระจาย 6 จุด (auto 2609 / color-same 2616 / _olApply 2700 / toggle-off 2708 / width-same 2723 / HEX-stored 3385) · ถ้าใส่ setItem ทีละจุด = เปราะแบบ _msgT (เผลอตก) → เลือก setter เดียว
- แก้ html: (1) เพิ่ม OL_LAST_KEY='oe_outline_last' + _olPersistLast (setItem JSON {c,w}) + _olLoadLast (validate hex #RRGGBB + ค่าใน _OL_WIDTHS ก่อนรับ) + _olSetLastC/_olSetLastW (set→persist) + เรียก _olLoadLast() ตอนโหลด · (2) แทนจุด set ทั้ง 6 ให้เรียกผ่าน setter · raw _olLastC=/_olLastW= เหลืออย่างละ 3 (ประกาศ+setter+loader) ยืนยันไม่มีหลุด
- lint #57 ใหม่ (OL_LAST_KEY + persist เขียน localStorage + _olLoadLast ถูกเรียก + setter เรียก persist + _olApply ผ่าน setter + ห้าม raw assignment หลุด >3) · V0 ผ่าน · ทดสอบบั๊ก 4 แบบจับครบ
- git: layer ต่อจาก commit b7a58e7 (สีกลุ่มใหม่ #171A1E) · เปลี่ยน 4 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS
- วิธี: workspace menu_work.html + lint_oe_cur.py · copy กลับ sha ตรง a889e9d68e2b430e · device python/sandbox ไม่เสถียร (ใช้ workspace + file_copy)

## 13 ต.ค. 2026 (10:40) — ✅ สี default กลุ่มเมนูใหม่ #4a8579 → #171A1E (เท่าสีชื่อเมนู) · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha ad70758f3c77f762 → 888b803edce46363
- ผู้ใช้เลือกจาก backlog: กลุ่มใหม่โผล่มาเป็นเขียวเทา #4a8579 ไม่เข้าชุด 9 กลุ่มที่มีสีเฉพาะ · agent ชี้ว่าแอปไม่มี theme สี (ไม่มี :root vars · แต่ละกลุ่มฝัง --accent ตายตัว) → ไม่มีชุดสีให้ match
- ผู้ใช้เลือก #171A1E (= สีชื่อรายการเมนู .nm) เหตุผล: พิมพ์ default ออกมาเข้ากับตัวหนังสือเมนู ไม่อ่อนไม่แก่กว่า
- แก้ html 3 จุดใน newSection: (893) baseline --accent:#4a8579→#171A1E · (897) ตัวเทียบ override !=='#4A8579'→'#171A1E' + data-acc0 '#4A8579'→'#171A1E' (ปุ่มคืนค่าสีต้องกลับมา #171A1E ไม่ใช่เขียวเก่า) · (899) fallback outline '#4a8579'→'#171A1E' + comment · delta 0 bytes (hex ยาวเท่ากัน)
- ไม่แตะปุ่ม '+ เพิ่มกลุ่ม' (.ed-addgroup บรรทัด 372-373) คง #4a8579 — ปุ่ม editor บนจอ ไม่พิมพ์ (เหลือ 4a8579 ในไฟล์ 2 จุด = ปุ่มนี้)
- lint #56 ใหม่ (newSection: --accent:#171A1E + ห้ามมี 4a8579 ค้าง + data-acc0=#171A1E) · V0 ผ่าน · ทดสอบบั๊ก 3 แบบจับครบ · lint ไม่ผูกกับ #4a8579 เดิม (#32 ตรวจพฤติกรรม ไม่ hardcode สี)
- git: layer ต่อจาก commit 9c4c80c (imgScale undo) · เปลี่ยน 4 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS
- วิธี: workspace menu_work.html + lint_oe_cur.py · copy กลับ sha ตรง 888b803edce46363 · device python/sandbox ไม่เสถียร (ใช้ workspace + file_copy)

## 13 ต.ค. 2026 (10:00) — ✅ ปุ่มขยาย/ย่อรูป (imgScale) สร้างจุด Undo · lint ผ่าน · ยังไม่ทดสอบเบราว์เซอร์ · ยังไม่ commit · html sha 99f3f3d051d56d99 → ad70758f3c77f762
- ผู้ใช้เลือกจาก backlog (decision 09:58): แก้ imgScale ไม่มี Undo (ช่องว่างที่รู้อยู่นานแล้ว)
- บั๊กเดิม: imgScale ไม่เรียก markDirty → กดขยาย/ย่อแล้ว Ctrl+Z ไม่คืน · ลากมุมรีไซส์คืนได้ (mouseup → markDirty บรรทัด 2344)
- แก้ html 1 จุด (imgScale บรรทัด 2220): เพิ่ม cw=parseInt(cs.width) · guard if(nw===cw){_imgReadout;return;} (ชนขอบ 30px ย่อไม่ลง = ไม่สร้าง undo กฎ #6) · ท้ายฟังก์ชันเรียก markDirty() (debounced เหมือน resize-drag · กดรัวรวมเป็น 1 undo)
- เลือก markDirty (debounced) ไม่ใช่ _snapNow (ทันที) เพื่อให้สอดคล้องกับ resize-drag + กดรัวๆ ไม่สร้าง undo หลายจุดเกินจำเป็น
- lint #55 ใหม่ (imgScale ต้องมี markDirty + guard nw===cw) · V0 ผ่าน · ทดสอบบั๊ก 2 แบบจับครบ
- git: layer ต่อจาก commit f330421 (lint #54) · เปลี่ยน 4 ไฟล์: html + lint_oe.py + UI_STANDARD + SESSION_STATUS
- วิธี: workspace menu_work.html + lint_oe_cur.py · copy กลับ sha ตรง ad70758f3c77f762 · device python/sandbox ไม่เสถียร (ใช้ workspace + file_copy)

## 12 ต.ค. 2026 (22:40) — ✅ lint #54 ล็อก pattern กัน XSS (defense-in-depth) · ไม่แก้ HTML · lint ผ่าน · ยังไม่ commit · html คงที่ 99f3f3d (commit 5cbfb2c)
- ผู้ใช้ถาม security assessment ของ app เมนู → agent ไล่ตรวจ XSS: innerHTML 27 จุด + sink อื่นทั้งหมด → ไม่พบช่องโหว่ใช้โจมตีได้จริง (โค้ด pattern ถูกต้องอยู่แล้ว)
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
