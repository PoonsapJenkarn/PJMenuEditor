# OE Isan Menu — SESSION STATUS

อัปเดตล่าสุด: Fri 23 Oct 2026, 10:06 +07

## งานล่าสุด: #edbar fixed → sticky (แก้จอแคบเนื้อหาหาย · เกณฑ์ยั่งยืน)
ผู้ใช้เลือก B (sticky) · scope B-เฉพาะ top bar (bottom bar/actlog ไม่แตะ)

## สถานะ: ✅ ทดสอบผ่านแล้ว (ย่อเฉพาะกว้าง เห็น scrollbar แนวนอน + เนื้อหาครบ) — รอ commit
- ผู้ใช้ทดสอบ: ย่อ browser เฉพาะด้านกว้าง → มี scrollbar แนวนอนด้านล่าง · toolbar + เมนูแสดงครบ ไม่หาย (ภาพ 23 ต.ค. 10:05)
- lint จากดิสก์ PASS (rc=0) · braces 3401:3401
- **ยังไม่ commit**

## สิ่งที่เปลี่ยน (B-เฉพาะ top bar)
- #edbar: position:fixed → position:sticky;top:0;min-width:960px
- body: + min-width:960px (จอแคบกว่านี้ scroll แนวนอน เนื้อหาไม่หด/หาย)
- ตัด body{padding-top:56px} + ตัด paddingTop ใน syncBarHeight (sticky กินที่เอง · ลด hack)
- _pageFitMetrics: padT จาก #edbar.offsetHeight แทน cs.paddingTop
- bottom bar (#edstatus/#actlog) ไม่แตะ · paddingBottom คงเดิม
- lint ข้อ 92 ล็อก: #edbar sticky + min-width:960 (body+#edbar) + syncBarHeight ห้ามตั้ง paddingTop

## ขั้นถัดไป
commit → push (ฐานล่าสุด 2fc242e)

## ค้างตัดสิน / งานถัดไป
- icon identity (glyph generic ดูเป็น AI โหล) — งานใหญ่แยก · ยังไม่ตัดสิน (A รื้อ system / B เปลี่ยนชุด / C ทีละจุด)
- GF_Knowledge_Notes.md จะเก็บใน repo หรือถอด (git rm --cached)
- slider ความจาง จะให้ sync ตามหน้าที่เลือกด้วยไหม (ค่าเป็น global)
