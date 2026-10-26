# SESSION STATUS - OE Isan Menu Editor

ปรับปรุงล่าสุด: 2026-10-26 14:55 (+07)

## เสร็จรอบนี้ (ยังไม่ commit) - ซ่อนกล่องโน้ต / ป้ายหน้า (เพิ่มพื้นที่เมนู)
- แยก 2 toggle ในแท็บเท็มเพลต กลุ่มใหม่ "แสดง/ซ่อน" (grp.show):
  - btnNoteHide -> toggleNoteHide() -> data-notehide บน <html>
  - btnPLabelHide -> togglePageLabelHide() -> data-plabelhide บน <html>
- CSS (วางหลัง base .crab โดยตั้งใจ — กัน lint #93/#112/#113 regex \.crab\{ จับกฎ display:none แทน base ที่มี var):
  - html[data-notehide] .crab{display:none}
  - html[data-notehide] .pagelabel{margin-left:auto} (ดันป้ายหน้าชิดขวาเมื่อ crab หาย เพราะ crab flex:1 ที่ดันขวาหายไป)
  - html[data-plabelhide] .pagelabel{display:none}
  - html[data-notehide][data-plabelhide] .noterow{display:none} (ซ่อนทั้งคู่ = ซ่อนทั้งแถว คืน margin เต็ม)
- pattern เดียวกับ data-rulehide: attribute บน html, จอ+พิมพ์+ติดไฟล์ (clone จับไป), ไม่ใช้ localStorage (document setting)
- _noteHideSync (อัปเดต 2 ปุ่ม .on+label) + toggle x2 (markDirty + checkOverflow quiet) · startup เรียก _noteHideSync() หลัง _layoutLoad()
- active-green: เพิ่ม btnNoteHide/btnPLabelHide ใน 3 selector
- i18n ครบ TH+EN: btn.noteHide/noteShow, btn.plabelHide/plabelShow, grp.show, ttl.noteHide/plabelHide
- lint #115 ล็อกครบ
- lint PASS (rc=0), เขียนดิสก์ (html 8,151,670 bytes)

## บทเรียน (lint regex gotcha)
- lint #93/#112/#113 ใช้ re.search(r'\.crab\{...') จับตัวแรกในไฟล์ · ถ้าเพิ่ม `html[...] .crab{display:none}` ไว้ก่อน base .crab -> regex จับตัว display:none (ไม่มี var) -> false FAIL
- แก้: วางกฎ variant (html[data-x] .crab) ไว้หลัง base .crab เสมอ · assert-gate จับได้ ไฟล์ไม่ถูกเขียนตอน fail

## รอผู้ใช้ทดสอบ (F5)
1. แท็บ เท็มเพลต: กลุ่มใหม่ "แสดง/ซ่อน" มี 2 ปุ่ม ซ่อนโน้ต / ซ่อนป้ายหน้า
2. กดซ่อนโน้ต -> กล่อง * ทางร้านไม่มีเมนูปู หาย · ป้ายหน้ายังชิดขวา · ปุ่มเขียว label=แสดงโน้ต
3. กดซ่อนป้ายหน้า -> "เมนูอาหาร หน้า 1/2" หาย · ปุ่มเขียว
4. ซ่อนทั้งคู่ -> แถวหายทั้งแถว เมนูขยับขึ้น (ได้พื้นที่คืน)
5. พิมพ์/Save -> สถานะติดไฟล์
6. ทุกหน้าได้ผลเหมือนกัน (data บน html = global ทุกหน้า)

## ค้างถัดไป
- รูปทับข้อความในโหมด 3 คอลัมน์ (ผู้ใช้ถามไว้ ยังไม่เคาะ: ซ่อนรูปอัตโนมัติใน 3col / ย่อรูป / ปล่อยไว้)
- กล่องโน้ต หดกว้างตามข้อความ? · contrast .ep-preview 4.42 · ปุ่มยืนยันปรับราคาแยกโซน? · ตัวคั่น สี·รูป · popup เล็ก · local override ต่อ element

## commit ที่จะใช้ (ผู้ใช้รันเองที่ C:\OE)
git add -A
git commit -m "feat: ซ่อนกล่องโน้ต/ป้ายหน้า แยก 2 toggle ในแท็บเท็มเพลต (เพิ่มพื้นที่เมนู · ติดไฟล์+พิมพ์) + lint #115"
git push

HEAD ก่อนหน้า: ecb96f5
