# OE Isan Menu — SESSION STATUS

อัปเดตล่าสุด: Thu 22 Oct 2026, 17:51 +07

## งานล่าสุด: แก้บั๊ก slider ความจาง live เฉพาะหน้าแรก → ให้ real-time ทุกหน้าในขอบเขต
ผู้ใช้พบ: เลือก scope "ทุกหน้า" เลื่อน slider ความจางกลุ่มเมนู หน้าแรกเปลี่ยน real-time แต่หน้าอื่นเปลี่ยนตอนปล่อยเมาส์เท่านั้น
ผู้ใช้เลือก A: แก้ทั้ง 3 slider (รูป/สี/กลุ่มเมนู) ให้ live ทุกหน้า สม่ำเสมอ

## สถานะ: ✅ เขียนลงดิสก์แล้ว · lint จริงจากดิสก์ PASS (rc=0) — รอผู้ใช้ทดสอบใน browser
- เขียน OEIsanHotpotMenuEditor.html + lint_oe.py (assert-gated)
- re-run lint จากดิสก์: rc=0 · braces 3343:3343 สมดุล
- ยืนยัน: _bgDimLive/_bgColorDimLive/_bgSecDimLive ทั้ง 3 เป็น forEach (ทุกหน้า) · ไม่มี t[0] เหลือ
- **ยังไม่ commit**

## สาเหตุบั๊ก (วิเคราะห์จากของจริง)
- live function เดิมตั้งใจ set เฉพาะ t[0] (หน้าแรก) ขณะลาก แล้ว commit ทั้งขอบเขตตอนปล่อยเมาส์ (onchange)
- pattern นี้ตัดสินไว้ 21 ต.ค. (lint 1776) เหตุผล "กันค้างตอนหลายหน้า" — แต่เมนู 4 หน้า set CSS var เบามาก ไม่มีทางค้าง เหตุผลเดิมไม่สมจริง
- บั๊กมีครบทั้ง 3 slider (รูป/สี/กลุ่มเมนู) ไม่ใช่แค่กลุ่มเมนู

## สิ่งที่เปลี่ยน
- 3 live functions: เปลี่ยนจาก `var t=...; var pg=t&&t[0]; if(pg){...}` → `_pageBgTargets(_pageBgScope()).forEach(function(pg){...})` ทุกหน้าในขอบเขต
- live ยังไม่ markDirty (เจตนาเดิม: live=อัปเดต view ไม่สร้าง undo · commit ตอนปล่อยเมาส์ค่อย markDirty) — แยก live/commit ยังอยู่ครบ
- set functions (_pageBgSetDim/_pageBgSetColorAlpha/_pageBgSetSecAlpha) ไม่แตะ (commit + _bgReapply ยังเรียกเหมือนเดิม)
- lint 1776: แก้ข้อความ "หน้าแรกในขอบเขต" → "ทุกหน้าในขอบเขต"
- lint ข้อ 88 ใหม่: บังคับ live ทั้ง 3 ต้องมี _pageBgTargets+forEach + ห้ามมี t[0] (กันถอยกลับ)

## รอทดสอบ (browser · refresh F5 ก่อน)
1. scope "ทุกหน้า" → เลื่อน slider ความจางกลุ่มเมนู: ทุกหน้าเปลี่ยน real-time พร้อมกันขณะลาก (ไม่ใช่หน้าแรกอย่างเดียว)
2. slider ความจางรูป + ความจางสี: real-time ทุกหน้าเหมือนกัน
3. ปล่อยเมาส์: ค่าคงเดิม (commit ถูกต้อง) + markDirty มีจุด undo
4. scope คี่/คู่/ช่วง: live เฉพาะหน้าในขอบเขต

## ขั้นถัดไป (หลังผู้ใช้ยืนยันผ่าน)
commit ทั้งชุด → push (ฐานล่าสุด f08c076)

## ค้างสะสม (ยังไม่ commit)
1. รูปพื้นหลังเลื่อนด้วยปุ่มลูกศร (window._bgNudgeBound) — ทดสอบผ่านแล้ว
2. ปุ่มซ่อนเนื้อหา scope-aware (.page.pgcontenthide) — ทดสอบผ่านแล้ว
3. ปุ่ม toggle พาเนลเขียวตอน active (.ep-mini.on) — ทดสอบผ่านแล้ว
4. slider ความจาง live ทุกหน้า (3 ตัว) — รอทดสอบ

## บันทึกแล้ว
- agent instruction ข้อ 11 (ปุ่ม toggle active เขียว) — PUBLISHED แล้ว (ผู้ใช้สั่ง publish 22 ต.ค.)

## ค้างตัดสิน
- GF_Knowledge_Notes.md จะเก็บใน repo หรือถอด (git rm --cached)
