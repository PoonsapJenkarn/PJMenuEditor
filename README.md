# PJ Menu Editor — เครื่องมือทำเมนูร้านอาหารขนาดเล็ก

เครื่องมือทำเมนูร้านอาหารในรูปแบบ HTML (A4) — แก้ราคา/เมนู จัดวางรูป แล้วพิมพ์เป็น PDF · ไฟล์ตัวอย่างในโปรเจกต์นี้คือเมนูร้าน โอ อีสาน แจ่วฮ้อน (ตัวอย่างการใช้งาน)

## ไฟล์ในโปรเจกต์

| ไฟล์ | บทบาท | มีรูป | Editor UI |
|---|---|---|---|
| `OEIsanHotpotMenuEditor.html` | editor + รูปอาหาร | มี | มี |

## วิธีเปิด
เปิดใน Chrome / Edge โดยตรง (ดับเบิลคลิก หรือวาง path ใน address bar)
กด **Ctrl+Shift+R** เพื่อโหลดเวอร์ชันล่าสุด (ล้าง cache)

## editor — ปุ่มการทำงาน
- **แก้ไขเมนู / ปิดการแก้ไขเมนู** — แก้ชื่อ/ราคา/หัวข้อ/เพิ่ม-ลบกลุ่ม/รายการ/หน้า
- **แก้ไขรูป / ปิดการแก้ไขรูป** — ลากย้าย/ปรับขนาด/ลบ/เพิ่มรูป และเปลี่ยนโลโก้
- **Save Editor File** — บันทึกไฟล์ editor (เลือกที่เก็บทุกครั้ง) มีจุดเหลืองเตือนเมื่อมีการแก้ที่ยังไม่บันทึก
- **Save Menu File** — บันทึกไฟล์เมนูสำหรับพิมพ์ (ตัด editor ออก)

## พิมพ์เป็น PDF
Ctrl+P (Chrome/Edge) → A4, Margins = None, Background graphics = ON

## Version control
Git repo + remote บน GitHub (private): https://github.com/Justin-10/OE — commit ทุกครั้งที่แก้เสร็จเพื่อให้ย้อนกลับได้

## ผู้สร้าง / Credit
สร้างโดย **Poonsap Jenkarn** (2026)
เครื่องมือแก้เมนูร้านอาหารอีสาน — ตั้งใจทำให้ร้านเล็กใช้ฟรี

- GitHub: https://github.com/Justin-10/OE
- ติดต่อ: jenkarn2631@gmail.com

## สัญญาอนุญาต / License
เผยแพร่ภายใต้ **MIT License** — ใช้ แก้ไข แจกจ่าย หรือใช้เชิงพาณิชย์ได้ฟรี โดยต้องคงประกาศลิขสิทธิ์และข้อความอนุญาตของผู้สร้างไว้ · ดูไฟล์ [LICENSE](LICENSE)

Released under the **MIT License** — free to use, modify, distribute, and use commercially, provided the original copyright and permission notice are kept. See [LICENSE](LICENSE).

Copyright (c) 2026 Poonsap Jenkarn

ฟอนต์ที่ฝังในแอป (Prompt, Sarabun, Noto Sans Thai) อยู่ภายใต้ SIL Open Font License 1.1 · ดูข้อความอนุญาตเต็มและประกาศลิขสิทธิ์ของแต่ละฟอนต์ได้ที่ไฟล์ [THIRD-PARTY-LICENSES.txt](THIRD-PARTY-LICENSES.txt)

The fonts embedded in the app (Prompt, Sarabun, Noto Sans Thai) are licensed under the SIL Open Font License 1.1. See [THIRD-PARTY-LICENSES.txt](THIRD-PARTY-LICENSES.txt) for the full license text and each font's copyright notice.
