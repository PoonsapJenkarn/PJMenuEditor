# OE Isan Menu — SESSION STATUS

อัปเดตล่าสุด: Thu 22 Oct 2026, 22:17 +07

## งานล่าสุด: icon info เป็น DEFAULT-OFF สำหรับ panel โทน info (toolbar ทุกตัวไม่มี icon อัตโนมัติ)
ผู้ใช้สั่ง: เอา icon info ออกจากเพิ่มหน้า(caret)ด้วย + กฎถาวร "toolbar/ribbon ไม่มี icon info และห้ามเพิ่มให้ของใหม่" + กังวลว่า agent จะลืมข้าม session
วิธีแก้ (ตอบ "จะจำได้ไหม"): เปลี่ยนจากพึ่งความจำ → สถาปัตยกรรม + lint

## สถานะ: ✅ เขียนลงดิสก์แล้ว · lint จริงจากดิสก์ PASS (rc=0) — รอผู้ใช้ทดสอบใน browser
- icon guard: var html=(opts.hideIcon||tone==='info')?'':... → โทน info ไม่มี icon โดย default
- ถอด hideIcon:true ที่ใส่ทีละ panel รอบก่อน (bg+price) ออก — ให้ default จัดการแทน (ไม่ทิ้งขยะ · ไม่เหลือ hideIcon:true ในไฟล์)
- re-run lint จากดิสก์: rc=0 · braces 3383:3383 สมดุล
- **ยังไม่ commit**

## ทำไมวิธีนี้ตอบ "จะจำได้ไหม" (3 ชั้น)
1. สถาปัตยกรรม (default) — toolbar ใหม่โทน info ไม่มี icon อัตโนมัติ ไม่ต้องจำเพิ่ม/ถอด = ไม่พึ่งความจำเลย
2. lint ข้อ 90 (เขียนใหม่) — ล็อก guard (opts.hideIcon||tone==='info') · ถ้าใครถอด default = fail ก่อน commit
3. memory + agent instruction ข้อ 12 (draft) — เตือนข้าม session

## ขอบเขตผล (ยืนยันจากของจริง)
- โทน info ที่หาย icon = toolbar ทำงานทั้งหมด: เพิ่มหน้า(caret), เงา(btnShdAll), ใช้ทั้งประเภท(typoApplyAll), คืนค่า(typoResetBtn), พื้นหลัง, ปรับราคา
- โทน danger ที่ยังมี icon = dialog ยืนยันจริง: ลบกลุ่ม/ลบหน้า/ช่วงลบหน้า/ยืนยันลบ/ล้าง log (icon มีความหมาย ถูกต้อง)
- แถบล่าง (_renderStatus) info = i จุดทึบ (แบบ B จากรอบก่อน) ไม่กระทบ

## agent instruction
- ข้อ 11 (ปุ่ม active เขียว) — PUBLISHED แล้ว
- ข้อ 12 (toolbar โทน info ไม่มี icon) — เพิ่มแล้วเป็น DRAFT · ยังไม่ publish (lint+memory คุมแล้ว · publish เมื่อผู้ใช้สั่งชัด)

## รอทดสอบ (browser · refresh F5 ก่อน)
1. caret ▾ เพิ่มหลายหน้า → panel ไม่มี icon info นำหน้า (เริ่มที่ "เพิ่ม [ ] หน้า" เลย)
2. toolbar ปรับราคา + พื้นหลัง → ไม่มี icon (ยืนยันซ้ำรอบก่อน)
3. panel เงา / ใช้ทั้งประเภท / คืนค่า (แท็บข้อความ) → ไม่มี icon info แล้วเหมือนกัน
4. dialog ลบหน้า/ลบกลุ่ม (danger) → ยังมี icon (ไม่กระทบ)
5. แถบล่าง info → i จุดทึบเหมือนเดิม

## ขั้นถัดไป (หลังผู้ใช้ยืนยันผ่าน)
commit ทั้งชุด → push (ฐานล่าสุด 0b2f92c)

## ค้างสะสม (ยังไม่ commit)
1. บั๊กปุ่มซ่อนเนื้อหา sync ตอนคลิกเปลี่ยนหน้า — ทดสอบผ่านแล้ว
2. ปุ่มเพิ่มหน้า split button + label "เพิ่ม [ ] หน้า" — ทดสอบผ่านแล้ว
3. icon info ออกจาก toolbar (bg/price) + แถบล่าง B — ทดสอบผ่านบางส่วน
4. icon info เป็น default-off โทน info (รวม caret เพิ่มหน้า + เงา/ใช้ทั้งประเภท/คืนค่า) — รอทดสอบ

## ค้างตัดสิน
- GF_Knowledge_Notes.md จะเก็บใน repo หรือถอด (git rm --cached)
- slider ความจาง จะให้ sync ตามหน้าที่เลือกด้วยไหม (ค่าเป็น global)
- agent instruction ข้อ 12 จะ publish ไหม (ตอนนี้ draft · lint+memory คุมแล้ว)
