# Google Fonts Knowledge — สรุปบทความ (เก็บไว้อ้างอิงโปรเจกต์ PJ Menu Editor)

**ที่มา:** https://fonts.google.com/knowledge · อ่านผ่านเบราว์เซอร์บนเครื่อง TH-JH3W034 (หน้า render ด้วย JS) · สรุปโดย agent 15 ต.ค. 2026
**License ต้นฉบับ:** เนื้อหา Knowledge เป็น CC BY-SA 4.0 ของ Google — โน้ตนี้สรุปด้วยคำของเราเอง ไม่ใช่สำเนา
**บทความทั้งหมด:** 91 · ⭐ = เกี่ยวกับงานเมนูโดยตรง

## ความคืบหน้า (checkpoint 15 ต.ค. 2026)
- [x] using_type (24) ✅
- [x] choosing_type (13) ✅
- [x] introducing_type (11) ✅
- [x] readability_and_accessibility (2) ✅
- [x] glossary (6 คำหลัก) ✅
- [ ] history_of_type (9) — ยังไม่อ่าน (ไม่เกี่ยวกับเมนูไทย)
- [ ] designing_hangeul (5) — ยังไม่อ่าน (ออกแบบอักษรเกาหลี)
- [ ] the_canadian_syllabics (5) — ยังไม่อ่าน (อักษรพื้นเมืองแคนาดา)
- [ ] type_in_china_japan_and_korea (6) — ยังไม่อ่าน (CJK)
- [ ] using_type_in_ar_and_vr (5) — ยังไม่อ่าน (AR/VR)
- [ ] using_variable_fonts_on_the_web (5) — ยังไม่อ่าน (variable fonts เชิงลึก)

**อ่านแล้ว 56/91 บทความ — ครบทุกหมวดที่เกี่ยวกับงานเมนู** · 35 ที่เหลือเป็นการออกแบบอักษรต่างชาติ/ประวัติ/AR-VR/variable เชิงลึก (ไม่เกี่ยวกับเมนูร้านไทย)

---


## using_type (ชุด 1/4)

### ⭐ Avoiding widows & orphans (คำโดดท้าย/ต้นคอลัมน์)
- widow = บรรทัด/คำโดดบนยอดคอลัมน์ · orphan = คำโดดท้ายย่อหน้า · แก้โดยดันคำลงบรรทัดถัดไป
- บนเว็บแก้ยากเพราะ responsive (ห้าม hard break ตายตัว — ติดไปตอน copy) · ใช้ `&nbsp;` (non-breaking space) ยึดคำท้ายให้อยู่ด้วยกันแทน
- **กับงานเรา:** เมนูพิมพ์เองในกล่องสั้นๆ ไม่ค่อยเจอ · ถ้าชื่อเมนูยาวตัดบรรทัดแปลกๆ ใช้วิธีดันคำได้

### ⭐ Choosing a suitable line height (ความสูงบรรทัด)
- Latin อ่านง่ายช่วง **115–150%** ของขนาดฟอนต์ · ภาษาที่มีวรรณยุกต์/diacritics เยอะ (เช่น **ไทย**) ต้องการ leading มากกว่าปกติ
- ฟอนต์ x-height สูง → ดูใหญ่ → ต้องการ line height มากขึ้น · ตัวเล็กยิ่งต้อง leading เยอะ · ตัว display ใหญ่ (72px) ใช้ line height 90–100% ได้
- **กับงานเรา:** ชื่อเมนูเป็น display สั้น · ไทยมีวรรณยุกต์ → อย่าตั้ง line height แน่นเกิน (เผื่อวรรณยุกต์บน+สระล่าง)

### Understanding measure / line length (ความยาวบรรทัด)
- บรรทัดอ่านสบาย: **45–75 ตัวอักษร** (Bringhurst) · Material Design = 40–60 · อังกฤษ ~10 คำ
- เทคนิค Trent Walton: วาง `*` ที่ตัวอักษรที่ 45 และ 75 เพิ่ม media query เมื่อ * มาอยู่บรรทัดเดียวกัน
- **กับงานเรา:** เมนูเป็นรายการสั้น ไม่ใช่ body ยาว — ไม่ค่อยเกี่ยว

### ⭐ The foundations of web typography (พื้นฐาน)
- เว็บ = fluid (เนื้อหาไหลตาม viewport) + text flow ไม่แน่นอน · ต่างจากสิ่งพิมพ์ที่ fix ขนาดหน้า
- เป้าหมาย typographer: ทำให้อ่านง่าย สื่อสารได้ · ใช้ HTML hierarchy (h1-h6, p) ให้ถูก
- **กับงานเรา:** เมนูเราเป็น fixed A4 (ไม่ fluid) ซึ่งเป็นข้อยกเว้น — เราคุมขนาดเองเพื่อพิมพ์

### ⭐ The complications of typographic size (ขนาดฟอนต์ซับซ้อน)
- ฟอนต์ขนาด (em) เท่ากันดูใหญ่ไม่เท่ากัน เพราะ x-height/cap-height ต่างกัน · em = body height ของ glyph
- CSS px = ขนาด em · แต่ตัวจริงที่ตาเห็นขึ้นกับ x-height ของแต่ละฟอนต์ (Verdana x-height 55% em ดูใหญ่กว่า Baskerville 40%)
- **กับงานเรา:** ตรงกับที่เราวัดความกว้าง/สูงฟอนต์เอง — ขนาด px เดียวกันแต่ละฟอนต์ดูไม่เท่ากัน เป็นเรื่องจริง

### ⭐⭐ Using web fonts from a font delivery service (โหลดฟอนต์จาก CDN)
- วิธีมาตรฐาน Google Fonts = `<link rel=preconnect>` + `<link ...css2?family=...&display=swap>` ใน `<head>` · หรือ `@import` ใน CSS (สำหรับ HTML email)
- CSS ที่ Google เสิร์ฟ = `@font-face` ผูก family + style + weight → **เหมือนที่เราฝังเองเป๊ะ** (เราแค่เปลี่ยน src เป็น base64 แทน URL)
- **กับงานเรา:** นี่คือวิธีที่เรา**เอาออก** (CDN) แล้วแทนด้วยฝัง base64 · ยืนยันว่าโครง @font-face เราถูกต้อง


## using_type (ชุด 2/4)

### ⭐⭐ Language support in fonts (รองรับภาษา)
- script = กลุ่มอักขระที่หลายภาษาใช้ร่วม (Latin ใช้โดยอังกฤษ/ฝรั่งเศส/เยอรมัน; ไทยเป็น script ของตัวเอง) · UI หลายภาษาต้องปรับ typography ตามภาษา
- ความยาวคำต่างกันมากข้ามภาษา (เยอรมันคำประสมยาว) · RTL (อาหรับ/ฮีบรู) ต้อง mirror UI · **หลาย script (รวมไทย) ต้องการ line height/spacing มากกว่าอังกฤษ**
- **กับงานเรา:** ยืนยันเหตุผลที่เราใช้ Noto สำหรับวรรณยุกต์ไทย + ตั้ง line height เผื่อไทย · ตรงกับที่ทำ

### Manual kerning is rarely required (kern เองไม่ค่อยจำเป็น)
- kerning = ระยะระหว่าง glyph คู่หนึ่ง (AV, To) · ฟอนต์ดีมี kerning pair ในไฟล์แล้ว ไม่ต้อง kern เอง
- จำเป็นเฉพาะฟอนต์ไม่ดี หรือทำโลโก้ · บนเว็บทำโดย wrap `<span>` + `letter-spacing`
- **กับงานเรา:** ไม่เกี่ยว — เมนูใช้ฟอนต์ Google ดีอยู่แล้ว

### Track carefully or not at all (tracking/letter-spacing)
- tracking = letter-spacing ทั้งก้อน (ต่างจาก kerning รายคู่) · ปรับต้องระวัง เพราะขัดเจตนา type designer
- กฎ: (1) all-caps/small-caps เพิ่ม tracking โดยเฉพาะตัวเล็ก (2) อย่า track กว้างไป (3) display ลบ tracking นิด · ตัวเล็กบวก tracking
- **กับงานเรา:** ไม่ได้ใช้ letter-spacing ในเมนู — ข้ามได้

### Working with hanging punctuation (เครื่องหมายล้ำขอบ)
- เครื่องหมาย (เช่น " เปิด) กินที่แต่ไม่เต็มที่ → เกิดรอยเยื้องตาเห็น · แก้โดยดันออกนอก margin ให้ขอบตรง
- บนเว็บ: `hanging-punctuation` รองรับแค่ Safari · ข้ามเบราว์เซอร์ต้อง wrap `<span>` + margin ลบ
- **กับงานเรา:** ไม่เกี่ยว — เมนูไม่มี body ย่อหน้ายาว

### Vertical spacing & line-height in design systems
- line-height มาจาก "leading" (ตะกั่วคั่นบรรทัดสมัยเรียงพิมพ์โลหะ) · ปัญหา: แต่ละฟอนต์วางตัวในกล่องต่างกัน → เปลี่ยนฟอนต์แล้ว spacing เพี้ยน ต้องปรับใหม่
- **กับงานเรา:** อธิบายว่าทำไมเปลี่ยนฟอนต์แล้วเลย์เอาต์ขยับ — เป็นเหตุผลที่เราต้องทดสอบตาเวลาสลับฟอนต์

### Breaking the rules (แหกกฎเมื่อจำเป็น)
- typography ดี = รู้ว่าเมื่อไรควรแหกกฎ · เช่น ตัวอักษรขาวบนพื้นดำดู "หนา" กว่าดำบนขาว → ควรปรับ weight/grade ชดเชย (จอ vs พิมพ์ ต่างกัน)
- **กับงานเรา:** หัวเมนูเราขาวบนพื้นสี — ถ้าดูหนาไปปรับ weight ได้ · เป็นหลักการ ไม่ใช่สิ่งต้องแก้ตอนนี้


## using_type (ชุด 3/4)

### From type to logotype (ทำโลโก้จากฟอนต์)
- กระบวนการทำโลโก้: sketch → เลือก typeface → ผสม mark → finalize · โลโก้ยังสำคัญ เป็นสิ่งแรกที่คนเห็นของแบรนด์
- **กับงานเรา:** โลโก้ร้านทำแล้ว (รูปคางหมู P + โออี) — อ้างอิงหลักการได้ถ้าทำโลโก้ร้านอื่น

### How to make type feel authentic (ทำให้ตัวอักษรดูมีชีวิต)
- ฟอนต์ลายมือถ้าตัวซ้ำๆ จะดูไม่เป็นธรรมชาติ · แก้ด้วย OpenType alternates (glyph สลับ) หรือ contextual alternates ให้ตัวซ้ำไม่เหมือนกัน
- **กับงานเรา:** ไม่เกี่ยว — เมนูไม่ได้เน้นฟอนต์ลายมือ

### ⭐ Implementing OpenType features on the web (ฟีเจอร์ OpenType)
- เปิดฟีเจอร์ (ligatures, alternates, numerals) ผ่าน CSS `font-feature-settings` หรือ `font-variant-*` · ต้องมีโค้ด 4 ตัวอักษร + ฟอนต์ต้องมีฟีเจอร์นั้นจริง
- **กับงานเรา:** ส่วนใหญ่ไม่จำเป็น · ถ้าอยากได้เลขสวย (tabular/oldstyle) ใช้ได้ แต่ยังไม่มีความต้องการ

### Installing & managing fonts (ติดตั้ง/จัดการฟอนต์ในเครื่อง)
- ที่เก็บฟอนต์: macOS `/Library/Fonts`, Windows `C:\Windows\Fonts` · ใช้ font manager จัดการ collection ได้ · variable fonts มีข้อควรระวังเพิ่ม
- **กับงานเรา:** เกี่ยวกับที่เราคุยเรื่องฟอนต์ในเครื่อง (queryLocalFonts) ที่ตัดสินใจไม่ทำ (Chromium-only)

### Introducing parametric axes (แกน parametric ใน variable fonts)
- variable font มี axis (weight/width/optical size/slant) · parametric axis จูนทีละมิติละเอียด · 4 พารามิเตอร์พื้นฐาน (opaque/transparent stroke ฯลฯ)
- **กับงานเรา:** ไม่เกี่ยว — เราฝัง static weight ไม่ใช่ variable

### Typesetting on a curved path (ตัวอักษรบนเส้นโค้ง)
- 2 วิธี: warping (บิด glyph ตามโค้ง — มักไม่สวย) vs wrapping (วางตัวตามโค้งไม่บิด) · ใช้ในหน้าปัดนาฬิกากลม
- **กับงานเรา:** ไม่เกี่ยวเลย


## using_type (ชุด 4/4 — variable fonts, ไม่เกี่ยวกับงานเราโดยตรง)

> ทั้ง 4 บทความนี้ว่าด้วย **variable fonts** (ฟอนต์ไฟล์เดียวปรับ weight/width ต่อเนื่อง) · โปรเจกต์เราใช้ **static weight ฝัง base64** ไม่ใช่ variable จึงไม่กระทบงานปัจจุบัน · เก็บไว้เป็น reference เผื่ออนาคต

### Switching from static to variable fonts
- เปลี่ยนจาก static เป็น variable = ลองของใหม่โดยคงระบบ typographic เดิม · ปรับค่า axis แทนการโหลดหลายไฟล์

### Loading variable fonts on the web
- โหลด variable ผ่าน `@font-face` ระบุช่วง weight (เช่น `wght@200..900`) ไฟล์เดียวครอบทุกน้ำหนัก · CSS `font-variation-settings`

### Styling type on the web with variable fonts
- ใช้ `font-weight`/`font-stretch`/`font-variation-settings` คุม axis · ได้ความยืดหยุ่นสูงแต่ไฟล์ variable ใหญ่กว่า static ตัวเดียว

### Designing with variable fonts in desktop apps
- Illustrator/Photoshop/Figma รองรับ variable fonts · ปรับ slider axis ได้ในแอป

**สรุปกับงานเรา:** ถ้าในอนาคตอยากลดจำนวนไฟล์ weight (ตอนนี้ Prompt ฝัง 4 น้ำหนัก) อาจใช้ variable font ตัวเดียวแทนได้ · แต่ variable ไฟล์ใหญ่กว่า + เราฝัง base64 อยู่แล้วคุมขนาดได้ดีกว่าด้วย static เฉพาะน้ำหนักที่ใช้ · **ไม่แนะนำเปลี่ยนตอนนี้**


## choosing_type (ชุด 1/2)

### ⭐ Choosing web fonts: beginner's guide
- เลือกฟอนต์ตามความต้องการจริงของงาน (ไม่ใช่แค่สวย) — ทั้งด้านความงาม เทคนิค และฟังก์ชัน · บางฟอนต์เหมาะหัวข้อ บางฟอนต์เหมาะ body · ดู language/script support + น้ำหนัก/สไตล์
- **กับงานเรา:** ยืนยันหลักเลือกฟอนต์ไทยที่รองรับวรรณยุกต์ครบ

### ⭐ A checklist for choosing type (เช็กลิสต์)
- เช็กลิสต์เลือกฟอนต์: personality เรียกอารมณ์ถูก · ดีไซน์เข้างาน · รองรับภาษา · อ่านง่าย · มีหลายน้ำหนัก/สไตล์ · (มีบน GitHub)
- **กับงานเรา:** 33 ฟอนต์ไทยที่คัดผ่านเช็กนี้ได้หมด (รองรับไทย+หลายน้ำหนัก)

### ⭐⭐ Choosing reliable typefaces (ฟอนต์ที่เชื่อถือได้)
- ฟอนต์ดีต้องมี: (1) language support (2) รายละเอียดอ่านง่าย (3) หลายน้ำหนัก/สไตล์ (4) alternates/OpenType
- **อย่าตกหลุมรักฟอนต์ที่ขาดอักขระที่ต้องใช้** — ถ้าขาดตัวเดียวก็ใช้แบรนด์ไม่ได้
- **กับงานเรา:** ตรงหลักที่เราคัดเฉพาะฟอนต์มี subset ไทย (ถ้าขาดวรรณยุกต์ = ใช้ไม่ได้) · เหตุผลที่ Roboto ไม่อยู่ในรายการ

### Emotive considerations (อารมณ์ของฟอนต์)
- คนตอบสนองต่อรูปทรงตัวอักษรเชิงอารมณ์ก่อนเหตุผล · เลือกตามอารมณ์ได้แต่อย่าลืมด้านเทคนิค
- **กับงานเรา:** ฟอนต์ร้านอาหารอีสาน/ส้มตำ — เลือกโทนเป็นกันเอง อ่านง่าย (Prompt/Kanit สมัยใหม่)

### Pairing typefaces (จับคู่ฟอนต์)
- ถามก่อนว่าจำเป็นต้องมีฟอนต์ที่สองไหม — ฟอนต์เดียวปรับ weight/case/size/tracking ก็สร้าง contrast ได้
- **กับงานเรา:** เราใช้ Prompt หลัก + Sarabun (หมายเหตุ) — คู่ที่พอเพียงแล้ว ไม่ต้องเพิ่ม

### ⭐ Exploring x-height & the em square (ทำไมเปลี่ยนฟอนต์แล้วเลย์เอาต์ขยับ)
- ตัวอักษรอยู่ใน em square มี vertical metrics (ascender/cap height/x-height/baseline/descender) · แต่ละฟอนต์วางต่างกัน → เปลี่ยนฟอนต์แล้ว layout ขยับเล็กน้อย
- **กับงานเรา:** อธิบายว่าทำไมสลับฟอนต์ในเมนูแล้วความสูง/ตำแหน่งขยับ — ต้องเช็กตาเวลาเปลี่ยน

### Adding fonts to Google Docs/Slides
- Google Workspace เพิ่มฟอนต์จาก Google Fonts library เข้าเมนู Font ได้ (คลิกชื่อฟอนต์ > More fonts)
- **กับงานเรา:** ไม่เกี่ยว — แต่เป็นตัวอย่าง font picker แบบ Pro (คล้ายปุ่ม Google ที่เราทำ)


## choosing_type (ชุด 2/2)

### ⭐ Exploring typefaces with multiple weights or grades
- regular/bold/italic/bold-italic มักพอ · แต่บางงานต้องการน้ำหนักหลายระดับเพื่อ hierarchy · grade = เปลี่ยนความหนาโดยความกว้างไม่เปลี่ยน (layout ไม่ขยับ)
- **กับงานเรา:** Prompt ฝัง 4 น้ำหนัก (400/500/600/700) ครอบคลุม hierarchy หัวข้อ/ชื่อเมนู/ราคา

### Exploring width in type (ความกว้างฟอนต์)
- width variation (narrow/condensed ↔ wide) ช่วยใส่คำได้มากขึ้นต่อบรรทัด หรือเน้น · ตัวแคบดีเวลาเนื้อหายาว
- **กับงานเรา:** ตรงกับที่ user เคยถาม — ฟอนต์แคบช่วยชื่อเมนูยาว · แต่เราวัดแล้วต่างกันแค่ ~6% (ดู UI_STANDARD 8.0)

### Optical sizes (ขนาดเชิงแสง)
- type foundry ทำฟอนต์หลายเวอร์ชันตามขนาดใช้งาน: ตัวเล็ก (body) = contrast น้อย x-height ใหญ่ ระยะโปร่ง · ตัวใหญ่ (display) = รายละเอียดคม ระยะชิด
- **กับงานเรา:** ฟอนต์ไทยส่วนใหญ่ไม่มี optical size axis — ไม่เกี่ยว

### Pairing within a family & superfamily
- จับคู่ในตระกูลเดียว/superfamily (serif+sans+slab ที่ออกแบบคู่กัน) = consistency สูง เสี่ยงน้อย
- **กับงานเรา:** Prompt มีครบน้ำหนักในตระกูลเดียว — ใช้ตัวเดียวพอ

### Pairing by same designer/foundry
- ฟอนต์จากดีไซเนอร์/โรงหล่อเดียวกันมักเข้ากัน (สไตล์การวาด + เทคนิคคล้าย)
- **กับงานเรา:** ไม่จำเป็น — ใช้ฟอนต์เดียว

### Pairing using the font matrix
- font matrix (Indra Kupferschmid) = จับคู่ตามโครงสร้างตัวอักษร · เลือกตัวที่ต่างพอแต่ไม่ต่างเกิน
- **กับงานเรา:** ขั้นสูง ไม่จำเป็นสำหรับเมนู


## introducing_type (ชุด 1/2)

### ⭐ Why care about typography?
- typography = การตัดสินใจว่าจะ "ใช้" ฟอนต์ยังไงให้อ่านสบาย+สื่อสไตล์ (ไม่ใช่แค่เลือกฟอนต์) · ได้ฟอนต์มาแล้วก็ต้องใช้ให้ดี
- **กับงานเรา:** เมนูเราคุม line-height/ขนาด/สี = typography ที่ดีแม้ฟอนต์ธรรมดา

### ⭐ Introducing weights & styles (น้ำหนัก+สไตล์)
- family พื้นฐาน = regular/bold + italic 2 ตัว · bold/italic ใช้เน้นบางส่วน · ควรใช้ italic/bold ของจริงจากฟอนต์ ไม่ใช่ faux (เบราว์เซอร์สังเคราะห์)
- **กับงานเรา:** ตรงกับที่เราเคยเจอ — Prompt/Sarabun ไม่มี italic axis → เบราว์เซอร์ทำ faux italic (เรายอมรับ note styling as-is)

### Making sense of typographic classifications (หมวดฟอนต์)
- จัดหมวดฟอนต์ช่วยค้นหา: serif/sans/slab/display/script ฯลฯ · หมวดส่วนใหญ่ใช้กับ Latin · script อื่นมีเกณฑ์ต่าง
- **กับงานเรา:** ฟอนต์ไทยเราเป็น sans-serif สมัยใหม่เกือบหมด (Prompt/Kanit/Mitr) + Sarabun (มีหัว)

### ⭐ Understanding numerals (ตัวเลข)
- เลข 4 แบบ: lining (สูงเท่า cap) · oldstyle (มี ascender/descender) · tabular (กว้างเท่ากันทุกตัว — เหมาะตาราง/ราคา) · proportional (กว้างต่างกัน)
- **กับงานเรา:** ราคาในเมนู! ถ้าใช้ **tabular numerals** เลขจะเรียงตรงคอลัมน์สวย · เป็นจุดที่ปรับปรุงได้ (font-feature `tnum`) ถ้า user สนใจ

### ⭐ An overview of Latin type anatomy (กายวิภาคตัวอักษร)
- ศัพท์: x-height/baseline/cap height (สัดส่วนแนวตั้ง) · ascender/descender/small caps · shoulder/spine/foot (เฉพาะส่วน)
- **กับงานเรา:** พื้นฐานเข้าใจว่าทำไมฟอนต์ขนาดเท่ากันดูไม่เท่า

### Introducing color fonts (ฟอนต์หลายสี)
- color/chromatic font = glyph หลายสี/gradient ในตัว · ใช้เหมือนฟอนต์ปกติ · เบราว์เซอร์รองรับยังไม่ทั่ว
- **กับงานเรา:** ไม่เกี่ยว (เมนูใช้ฟอนต์สีเดียว) · เกี่ยวโยง Noto Color Emoji ที่เราตัดสินใจไม่ฝัง


## introducing_type (ชุด 2/2)

### ⭐ Exploring punctuation (เครื่องหมายวรรคตอน)
- ใช้ glyph ที่ถูก: " " curly quotes (ไม่ใช่ straight) · en-dash/em-dash · apostrophe ที่ถูก · ไทยมีเครื่องหมายของตัวเอง
- **กับงานเรา:** เมนูมีน้อย — แต่ถ้าพิมพ์ราคา/หมายเหตุควรใช้เครื่องหมายถูกแบบ

### Introducing alternate glyphs (glyph ทางเลือก)
- type designer ทำ glyph สำรอง (stylistic alternates/sets) นอกเหนือตัว default · บางทีแยกเป็น family (เช่น Montserrat Alternates)
- **กับงานเรา:** ไม่จำเป็น

### ⭐ OpenType features in practice (ใช้ฟีเจอร์ OpenType จริง)
- ก่อนใช้ต้องเช็ก 4 อย่าง: ฟอนต์มีฟีเจอร์ไหม · ไฟล์รองรับไหม · เบราว์เซอร์/อุปกรณ์รองรับไหม · ผู้อ่านได้ประโยชน์ไหม
- **กับงานเรา:** ถ้าจะใช้ tabular numerals (ราคาตรงคอลัมน์) ต้องเช็กว่าฟอนต์ไทยที่ใช้มี `tnum` — ไม่ใช่ทุกตัวมี

### How typefaces are designed & fonts are made (ฟอนต์ถูกสร้างยังไง)
- type designer: ideate → sketch → วาด glyph → ทำไฟล์ฟอนต์ → ปล่อย · ซอฟต์แวร์สมัยใหม่ทำให้คนทำฟอนต์หลากหลายขึ้น
- **กับงานเรา:** background ความรู้ ไม่กระทบงาน

### Introducing variable fonts (variable fonts คืออะไร)
- variable font (OpenType Font Variations) = ไฟล์เดียวปรับ weight/slant/width ต่อเนื่อง · ให้ผู้ใช้คุมละเอียด · ก้าวใหญ่ของเทคโนโลยีฟอนต์
- **กับงานเรา:** เราใช้ static ฝัง — ดู using_type ชุด 4

### ⭐⭐ How type influences readability (ฟอนต์กับการอ่าน)
- readability = คุณสมบัติที่ทำให้อ่านง่าย · legibility = ตัวอักษรแยกแยะได้ชัด · ขึ้นกับ x-height, counter เปิด, ความต่างของตัวที่คล้ายกัน (I/l/1)
- **กับงานเรา:** เมนูต้องอ่านง่ายในพริบตา — เลือกฟอนต์ legible (Prompt/Sarabun ชัด) ถูกทาง

### ⭐ Introducing accessibility in typography (เข้าถึงได้)
- accessibility ไปไกลกว่า legibility/readability · เผื่อผู้มีความบกพร่องการมองเห็น · ขนาดพอ, contrast สูง, ไม่พึ่งสีอย่างเดียว
- **กับงานเรา:** เมนูพิมพ์ควร contrast สูง (เราใช้ตัวเข้มบนพื้นอ่อน) · ขนาด 17.5px อ่านง่าย


## glossary (คำนิยามหลัก)

> หมายเหตุ license: เนื้อหา Knowledge เป็น **CC BY-SA 4.0** (ของ Google) — โน้ตนี้สรุปด้วยคำของเราเอง ไม่ก็อปต้นฉบับ

- **Typeface vs Font:** typeface = ดีไซน์ที่เห็น · font = ไฟล์/instance ที่ใช้ (เทียบ: typeface=เพลง, font=ไฟล์ MP3) · เช่น Roboto = typeface, Roboto Bold = font
- **X-height:** ความสูงตัวพิมพ์เล็กที่ไม่มี ascender/descender (วัดจาก "x") · x-height ใหญ่ = ดูใหญ่/อ่านง่าย ascender สั้น
- **Em:** หน่วยเท่าขนาดฟอนต์ (16px → 1em=16px) · em square = กล่องที่ glyph อิง · em dash กว้าง ~1 em, en dash ~ครึ่ง
- **Contrast:** ความต่างเส้นหนา-บาง · monolinear = contrast ต่ำ · serif contrast สูงกว่า sans · display contrast สูงกว่า body
- **Optical sizes:** ฟอนต์เวอร์ชันต่างตามขนาดใช้ · body = contrast ต่ำ x-height สูง ระยะโปร่ง · display = คม ชิด
- **⭐ Weight axis (wght):** variable font axis · Google CSS v2: default 400, min 1, max 1000 · **ข้อสำคัญกับ API:** ใน URL Google Fonts axis ตัวพิมพ์เล็กมาก่อน ตามด้วยตัวพิมพ์ใหญ่ เรียง alphabetical (เกี่ยวถ้าใช้ variable — เราใช้ static ไม่กระทบ)

