#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pre-save lint สำหรับ OEIsanHotpotMenuEditor.html
จับบั๊ก pattern ที่เคยหลุดจริง — เปลี่ยน 'ความจำ' เป็น check อัตโนมัติ

รันเอง:   python lint_oe.py
เป็น git hook: ก็อปเป็น .git/hooks/pre-commit (ดูวิธีท้ายไฟล์)

exit code: 0 = ผ่าน, 1 = พบ error (บล็อก commit ถ้าเป็น hook)
"""
import re, sys, os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "OEIsanHotpotMenuEditor.html")  # เปลี่ยนชื่อจาก OEIsanHotpotMenuWithImageEditor.html (8 ต.ค. 2026)

def main():
    if not os.path.exists(PATH):
        print("LINT ERROR: ไม่พบไฟล์", PATH)
        sys.exit(1)
    with open(PATH, encoding="utf-8") as f:
        txt = f.read()

    errors = []
    warnings = []

    # ---- 1) brace / paren / bracket balance ----
    if txt.count("{") != txt.count("}"):
        errors.append("Brace imbalance: {{={} }}={}".format(txt.count("{"), txt.count("}")))
    if txt.count("(") != txt.count(")"):
        errors.append("Paren imbalance: (={} )={}".format(txt.count("("), txt.count(")")))

    # ---- 2) <script> paired ----
    if txt.count("<script") != txt.count("</script>"):
        errors.append("<script> unbalanced: open={} close={}".format(
            txt.count("<script"), txt.count("</script>")))

    # ---- 3) t() i18n shadow — per function block ----
    #   บั๊กที่หลุดซ้ำ v35, v48: ตัวแปร local ชื่อ t ไป shadow ฟังก์ชัน i18n t()
    funcs = [m.start() for m in re.finditer(r'\bfunction\b', txt)]
    for idx, start in enumerate(funcs):
        end = funcs[idx+1] if idx+1 < len(funcs) else len(txt)
        block = txt[start:end]
        if re.match(r'function t\(', block):   # ตัวนิยาม t() เอง
            continue
        if not re.search(r"\bt\(", block):     # block นี้ไม่เรียก t()
            continue
        binds = []
        if re.search(r'\bvar\s+t\b\s*[=;,]', block):   binds.append("var t")
        if re.search(r'\blet\s+t\b\s*[=;,]', block):   binds.append("let t")
        if re.search(r'\bconst\s+t\b\s*[=;,]', block): binds.append("const t")
        if re.search(r'for\s*\(\s*var\s+t\b', block):  binds.append("for var t")
        if re.search(r'catch\s*\(\s*t\s*\)', block):   binds.append("catch t")
        hdr = re.match(r'function\s+[A-Za-z0-9_]*\s*\(([^)]*)\)', block)
        if hdr:
            params = [p.strip() for p in hdr.group(1).split(",")]
            if "t" in params: binds.append("param t")
        if binds:
            nm = re.match(r'function\s+([A-Za-z0-9_]+)', block)
            nm = nm.group(1) if nm else "(anonymous)"
            errors.append("t() i18n shadow in {}: {}".format(nm, ", ".join(binds)))

    # ---- 4) i18n keys ที่ใช้ผ่าน t('...') ต้องมีจริงใน I18N.th ----
    iobj = txt.find("var I18N={")
    if iobj >= 0:
        th_start = txt.find("th:{", iobj)
        en_start = txt.find("en:{", iobj)
        th_block = txt[th_start:en_start] if (th_start >= 0 and en_start > th_start) else ""
        used = set(re.findall(r"t\('([a-zA-Z]+\.[a-zA-Z]+)'", txt))
        missing = [k for k in sorted(used) if ("'" + k + "'") not in th_block]
        if missing:
            errors.append("i18n keys ใช้แต่ไม่มีใน th: " + ", ".join(missing))

    # ---- 5) duplicate named function (override risk) = warning ----
    defs = re.findall(r'function\s+([A-Za-z0-9_]+)\s*\(', txt)
    seen = {}
    for d in defs: seen[d] = seen.get(d, 0) + 1
    for name, cnt in sorted(seen.items()):
        if cnt > 1:
            warnings.append("function '{}' นิยาม {} ครั้ง".format(name, cnt))

    # ---- 6) #edhint ต้องว่าง (กฎถาวร v11+) = warning ถ้าพบ assignment ----
    if re.search(r"edhint'?\)?\.textContent\s*=\s*['\"][^'\"]+['\"]", txt):
        warnings.append("#edhint ถูก set ข้อความ (ต้องว่างถาวรตาม v11+)")

    # ---- 7) ปุ่มสถานะ .on ต้องไม่ถูก CSS อื่นทับพื้นหลัง (บั๊ก 2 ต.ค. 2026: พื้นไม่เขียว ตัวอักษรขาว อ่านไม่ออก) ----
    #   ดู UI_STANDARD.md ข้อ 1: กฎ .on ต้องใช้ selector ที่ specificity ไม่ต่ำกว่ากฎอื่น และวางไว้หลังสุด
    _css = ''.join(re.findall(r'<style[^>]*>([\s\S]*?)</style>', txt))
    _css = re.sub(r'/\*[\s\S]*?\*/', '', _css)
    _rules = []
    for _i, (_sel, _body) in enumerate(re.findall(r'([^{}]+)\{([^{}]*)\}', _css)):
        for _one in _sel.split(','):
            _rules.append((_i, _one.strip(), _body))
    def _spec(sel):
        return (len(re.findall(r'#[\w-]+', sel)),
                len(re.findall(r'\.[\w-]+|\[[^\]]+\]|:(?!:)[\w-]+', sel)),
                len(re.findall(r'(?:^|[\s>+~])([a-zA-Z][\w-]*)', sel)))
    _seen = set()
    for _oi, _osel, _obody in [r for r in _rules if '.on' in r[1] and 'background' in r[2] and not r[1].endswith('svg')]:
        _toks = set(re.findall(r'[.#][\w-]+', _osel.split()[-1])) - {'.on'}
        for _ri, _rsel, _rbody in _rules:
            if _ri == _oi or 'background' not in _rbody or '.on' in _rsel or ':disabled' in _rsel: continue
            if _rsel.split()[0] != _osel.split()[0]: continue
            if not (set(re.findall(r'[.#][\w-]+', _rsel.split()[-1])) & _toks): continue
            _sr, _so = _spec(_rsel), _spec(_osel)
            if (_sr > _so or (_sr == _so and _ri > _oi)) and (_osel, _rsel) not in _seen:
                _seen.add((_osel, _rsel))
                errors.append("สถานะ .on ถูกทับ: '{}' แพ้ '{}' (พื้นจะไม่เขียว)".format(_osel, _rsel))

    # ---- 8) คลิกนอก panel ต้องไม่ปิด panel ตอน mousedown (layout เลื่อน → click ตกผิด element) ----
    _m = re.search(r'_panelOutside=function\(e\)\{([\s\S]*?)\n\s*\};', txt)
    if _m and re.search(r'(?<![\w.])closePanel\(\)', _m.group(1)):
        errors.append('_panelOutside เรียก closePanel() ตอน mousedown — ใช้ _panelCloseAfterRelease(seq) (ดู UI_STANDARD.md ข้อ 2)')

    # ---- 9) ห้ามใช้ placeholder ในช่องกรอก (หายตอนพิมพ์ · ดูเหมือนค่าที่กรอกแล้ว · screen reader บางตัวไม่อ่าน) ----
    #   ดู UI_STANDARD.md ข้อ 6: label อยู่นอกช่อง · ตัวอย่าง/คำแนะนำอยู่ใน .ep-preview หรือแถบสถานะ
    for _m in re.finditer(r'\bplaceholder\s*[=:]', txt):
        errors.append('ใช้ placeholder ที่บรรทัด {} — ใช้ label นอกช่อง + คำแนะนำใน .ep-preview (ดู UI_STANDARD.md ข้อ 6)'.format(txt.count('\n', 0, _m.start()) + 1))

    # ---- 10) แถบ/panel ห้ามสูงตายตัว และข้อความยาวห้าม nowrap (บั๊ก 3 ต.ค. 2026: หน้าต่างแคบ ปุ่มตกทับหน้าเมนู / panel ดันกันเป็น 2 บรรทัด) ----
    #   ดู UI_STANDARD.md ข้อ 7
    _m = re.search(r'#edribbon\{([^}]*)\}', _css)
    if _m and re.search(r'(?<![-\w])height\s*:', _m.group(1)):
        errors.append('#edribbon ตั้ง height ตายตัว — ใช้ min-height (ดู UI_STANDARD.md ข้อ 7)')
    for _sel in ('#edpanel .ep-preview', '#edpanel .ep-msg'):
        _m = re.search(re.escape(_sel) + r'\{([^}]*)\}', _css)
        if _m and 'nowrap' in _m.group(1):
            errors.append(_sel + ' ใช้ white-space:nowrap — ข้อความยาวจะดันส่วนอื่น (ดู UI_STANDARD.md ข้อ 7)')

    # ---- 11) ตัวตรวจล้นหน้า A4 ต้องวัดด้วยขนาดพิมพ์จริง (บั๊ก 3 ต.ค. 2026: หน้าต่าง <720px หน้าเมนูเป็น 1 คอลัมน์ → เตือนล้นปลอม) ----
    #   ทุก selector ที่ @media (max/min-width) เปลี่ยน ต้องมีกฎ body.measuring <selector> คืนค่าแบบ A4 · ดู UI_STANDARD.md ข้อ 7
    for _mb in re.finditer(r'@media[^{]*(?:max|min)-width[^{]*\{((?:[^{}]*\{[^}]*\})*)[^}]*\}', _css):
        for _sel in re.findall(r'([^{}]+)\{', _mb.group(1)):
            for _one in _sel.split(','):
                _one = _one.strip()
                if _one and ('body.measuring ' + _one) not in _css:
                    errors.append('@media width เปลี่ยน {} แต่ไม่มี body.measuring {} — ตัวตรวจล้นหน้าจะวัดผิดตอนหน้าต่างแคบ (ดู UI_STANDARD.md ข้อ 7)'.format(_one, _one))

    # ---- 12) openPanel ต้องส่งข้อความเป็น key (okKey/cancelKey/msgKey/labelKey) ไม่ใช่ t(...) — ไม่งั้นเปลี่ยนภาษาขณะ panel เปิดแล้วข้อความไม่เปลี่ยน (บั๊ก 3 ต.ค. 2026) ----
    for _m in re.finditer(r'(?<![\w.])(okText|cancelText|msg|label)\s*:\s*t\(', txt):
        errors.append('openPanel: {}:t(...) ที่บรรทัด {} — ใช้ {} แทน (ดู UI_STANDARD.md ข้อ 6)'.format(_m.group(1), txt.count('\n', 0, _m.start()) + 1, {'okText':'okKey','cancelText':'cancelKey','msg':'msgKey+msgArgs','label':'labelKey'}[_m.group(1)]))

    # ---- 13) ข้อความแถบล่างต้องใช้ tk()/tkj() ไม่ใช่ t() — ไม่งั้นกด TH/EN แล้วแถบล่างไม่เปลี่ยนภาษา (บั๊ก 3 ต.ค. 2026) ----
    def _span13(x, i):
        d = 0; j = i; n = len(x)
        while j < n:
            c = x[j]
            if c in '\'"':
                q = c; j += 1
                while j < n and x[j] != q:
                    if x[j] == '\\': j += 1
                    j += 1
            elif c == '(': d += 1
            elif c == ')':
                d -= 1
                if d == 0: return j
            j += 1
        return -1
    for _m in re.finditer(r'(?<![\w.])(setStatus|flashStatus|_renderStatus)\(', txt):
        if 'function ' in txt[max(0, _m.start()-9):_m.start()]: continue
        _b = _span13(txt, _m.end()-1)
        if _b > 0 and re.search(r'(?<![\w.])t\(', txt[_m.end():_b]):
            errors.append('{}(...t(...)) ที่บรรทัด {} — ข้อความแถบล่างใช้ tk()/tkj() (ดู UI_STANDARD.md ข้อ 6)'.format(_m.group(1), txt.count('\n', 0, _m.start()) + 1))

    # ---- 14) ตอนพิมพ์ต้องล้าง padding ของ body ด้วย !important — syncBarHeight ใส่ body.style.paddingTop/Bottom แบบ inline (บั๊ก 5 ต.ค. 2026: หน้า 1 เลื่อนลง ~41mm + พิมพ์ 4 แผ่นแทน 2) ----
    if re.search(r'body\.style\.padding(Top|Bottom)\s*=', txt):
        _ok14 = False
        for _pm in re.finditer(r'@media\s+print\s*\{((?:[^{}]*\{[^}]*\})*)[^}]*\}', _css):
            for _sel, _body in re.findall(r'([^{}]+)\{([^}]*)\}', _pm.group(1)):
                if re.search(r'(^|[\s,])body\s*$', _sel.strip()) or _sel.strip() == 'body':
                    if re.search(r'padding-top\s*:\s*0\s*!important', _body) and re.search(r'padding-bottom\s*:\s*0\s*!important', _body):
                        _ok14 = True
        if not _ok14:
            errors.append('@media print ต้องมี body{padding-top:0 !important;padding-bottom:0 !important} — syncBarHeight ใส่ padding แบบ inline (ดู UI_STANDARD.md ข้อ 7)')

    # ---- 15) เส้นประ/พื้นสี/padding ของโหมดแก้ (body.editmode/imgmode/headermode/pricemode) ต้องอยู่ใน @media screen — ไม่งั้น Ctrl+P ระหว่างอยู่ในโหมดแก้ จะพิมพ์เส้นประติดไป (บั๊ก 5 ต.ค. 2026) ----
    _c15 = _css; _i = 0; _top = []
    while _i < len(_c15):
        if _c15[_i] == '@':
            _j = _c15.find('{', _i)
            if _j < 0: break
            _d = 1; _j += 1
            while _d and _j < len(_c15):
                if _c15[_j] == '{': _d += 1
                elif _c15[_j] == '}': _d -= 1
                _j += 1
            _i = _j; continue
        _m = re.compile(r'([^{}@]+)\{([^}]*)\}').match(_c15, _i)
        if _m: _top.append((_m.group(1).strip(), _m.group(2))); _i = _m.end(); continue
        _i += 1
    for _sel, _body in _top:
        if re.search(r'body\.(editmode|imgmode|headermode|pricemode)', _sel) and re.search(r'outline|background|box-shadow|border(?!-radius)|(?<![-\w])content\s*:|padding', _body):
            errors.append('กฎหน้าตาโหมดแก้ไม่ได้อยู่ใน @media screen: "{}" — จะติดไปตอนพิมพ์ (ดู UI_STANDARD.md ข้อ 7)'.format(_sel[:80]))

    # ---- 16) ช่องกรอกต้องรับได้เฉพาะตัวอักษรของข้อมูลนั้น (บั๊ก 5 ต.ค. 2026: ช่องลบหน้าพิมพ์ภาษาไทยได้) ----
    #   openPanel mode:'prompt' ต้องมี filter: · <input type="text"> ที่ไม่ readonly ต้องอยู่ในรายการที่มีตัวกรองแล้ว · ดู UI_STANDARD.md ข้อ 6
    for _m in re.finditer(r"mode\s*:\s*'prompt'", txt):
        _a = txt.rfind('openPanel(', 0, _m.start())
        _b = _span13(txt, _a + len('openPanel')) if _a >= 0 else -1
        if _a < 0 or _b < 0 or not re.search(r'(?<![\w.])filter\s*:', txt[_a:_b]):
            errors.append("openPanel mode:'prompt' ที่บรรทัด {} ไม่มี filter: — ช่องกรอกต้องรับเฉพาะตัวอักษรที่ใช้ (ดู UI_STANDARD.md ข้อ 6)".format(txt.count('\n', 0, _m.start()) + 1))
    _FILTERED16 = {'ep-input', 'ep-amt', 'ep-price', 'typoHex', 'typoSize', 'typoCpDlgHex'}  # ช่องที่มีตัวกรองแล้ว — เพิ่มช่องใหม่ต้องมีตัวกรองก่อนแล้วค่อยใส่ชื่อที่นี่
    for _m in re.finditer(r'<input\b[^>]*>', txt):
        _tag = _m.group(0)
        if not re.search(r'type\s*=\s*\\?["\']text', _tag) or 'readonly' in _tag: continue
        _ids = set(re.findall(r'id\s*=\s*\\?["\']([\w-]+)', _tag)) | set(' '.join(re.findall(r'class\s*=\s*\\?["\']([^"\'\\]+)', _tag)).split())
        if not (_ids & _FILTERED16):
            warnings.append('ช่องกรอก text ที่บรรทัด {} ยังไม่อยู่ในรายการที่มีตัวกรอง: {}'.format(txt.count('\n', 0, _m.start()) + 1, _tag[:80]))

    # ---- 17) ทุกช่องที่แก้บนหน้าเมนูต้องมีความยาวสูงสุด (work instruction 5 ต.ค. 2026: ช่องเลขหน้าพิมพ์ได้ไม่จำกัด) ----
    #   ช่องข้อความ = อยู่ใน _TXT_LIMITS · ราคา = _PR_MAXDIG · ดู UI_STANDARD.md ข้อ 6
    _lim = re.search(r'var _TXT_LIMITS=\[([\s\S]*?)\];', txt)
    if not _lim:
        errors.append('ไม่พบ _TXT_LIMITS — ช่องข้อความต้องกำหนดความยาวสูงสุด (ดู UI_STANDARD.md ข้อ 6)')
    else:
        _need = {'.nm', '.sec-h .sechead'} | {'[data-edit="%s"]' % _k for _k in set(re.findall(r'data-edit="([\w-]+)"', txt))}
        for _sel in sorted(_need):
            if ("sel:'%s'" % _sel) not in _lim.group(1):
                errors.append('ช่อง {} ไม่มีความยาวสูงสุดใน _TXT_LIMITS (ดู UI_STANDARD.md ข้อ 6)'.format(_sel))
    if not re.search(r'var _PR_MAXDIG=\d+;', txt):
        errors.append('ไม่พบ _PR_MAXDIG — ราคาต้องจำกัดจำนวนหลัก (ดู UI_STANDARD.md ข้อ 6)')

    # ---- 18) บันทึกไฟล์ออกจากแอปต้องให้ผู้ใช้เลือกที่เก็บก่อน (บั๊ก 6 ต.ค. 2026: ส่งออกบันทึกดาวน์โหลดเงียบๆ ผู้ใช้ไม่รู้ว่าไฟล์อยู่ไหน) ----
    #   ทุกจุดที่เรียก triggerDownload( ต้องมี showSaveFilePicker ก่อนในฟังก์ชันเดียวกัน (ดาวน์โหลด = ทางสำรองเท่านั้น) · ดู UI_STANDARD.md ข้อ 6
    for _m in re.finditer(r'triggerDownload\(', txt):
        if txt[max(0, _m.start() - 9):_m.start()] == 'function ': continue
        _a = max(txt.rfind('\nfunction ', 0, _m.start()), txt.rfind('\nasync function ', 0, _m.start()))
        if 'showSaveFilePicker' not in txt[_a:_m.start()]:
            _fn = re.match(r'\n(?:async )?function (\w+)', txt[_a:])
            errors.append('{} ที่บรรทัด {} ดาวน์โหลดไฟล์โดยไม่ให้เลือกที่เก็บ — ใช้ _saveAs() (ดู UI_STANDARD.md ข้อ 6)'.format(_fn.group(1) if _fn else '?', txt.count('\n', 0, _m.start()) + 1))

    # ---- 19) ทางสำรองดาวน์โหลดต้องบอกว่าไฟล์อยู่ในโฟลเดอร์ดาวน์โหลด (บั๊ก 6 ต.ค. 2026: ข้อความ Save Menu/Editor ไม่บอกว่าไฟล์อยู่ไหน) ----
    #   หลัง triggerDownload( ในฟังก์ชันเดียวกัน ข้อความแถบล่างถัดไปต้องเป็น key ที่ภาษาไทยมีคำว่า "โฟลเดอร์ดาวน์โหลด" · ดู UI_STANDARD.md ข้อ 6
    _thA = txt.find('th:{', txt.find('var I18N={')); _enA = txt.find('en:{', _thA)
    _TH19 = dict(re.findall(r"'([A-Za-z0-9_.]+)':'((?:[^'\\]|\\.)*)'", txt[_thA:_enA]))
    for _m in re.finditer(r'triggerDownload\(', txt):
        if txt[max(0, _m.start() - 9):_m.start()] == 'function ': continue
        _body = txt[_m.start():txt.find('\n}', _m.start())]
        _fm = re.search(r"flashStatus\([^;]*?tk\('([\w.]+)'", _body)
        _ln = txt.count('\n', 0, _m.start()) + 1
        if not _fm:
            if "how:'download'" in _body: continue  # _saveAs: ผู้เรียกเป็นคนแจ้ง
            errors.append('บรรทัด {} ดาวน์โหลดไฟล์แล้วไม่แจ้งผู้ใช้ว่าไฟล์อยู่ไหน (ดู UI_STANDARD.md ข้อ 6)'.format(_ln)); continue
        if 'โฟลเดอร์ดาวน์โหลด' not in _TH19.get(_fm.group(1), ''):
            errors.append("บรรทัด {} ข้อความ '{}' ไม่บอกว่าไฟล์อยู่ในโฟลเดอร์ดาวน์โหลด (ดู UI_STANDARD.md ข้อ 6)".format(_ln, _fm.group(1)))

    # ---- 20) ข้อความที่ใส่ด้วย t() ต้องเปลี่ยนตาม TH/EN (บั๊ก 6 ต.ค. 2026: "ยังไม่มีบันทึกกิจกรรม", tooltip ปุ่มลบแถว/กลุ่ม/ที่จับย่อขยาย ไม่เปลี่ยนภาษา) ----
    #   el.title=t('k') ต้องมี el.setAttribute('data-i18n-title','k') บรรทัดเดียวกัน · el.textContent=t('k') ต้องมี data-i18n='k'
    #   ยกเว้น: ข้อความใน openPanel(...) และฟังก์ชันที่ส่งเป็น onCustom/onInput/onRelang (panel แปลใหม่เองตอนกด TH/EN) · ดู UI_STANDARD.md ข้อ 6
    _i2 = txt.rfind('<script'); _js = txt[_i2:]; _off = txt.count('\n', 0, _i2)
    _hooks = set(re.findall(r'\bon(?:Custom|Input|Relang)\s*:\s*(\w+)\b', _js)) - {'function'}
    _fst = [(_x.start(), _x.group(1)) for _x in re.finditer(r'\nfunction\s+(\w+)\s*\(', _js)]
    for _m in re.finditer(r"(\w+)\.(title|textContent)\s*=\s*t\('([\w.]+)'", _js):
        _v, _pp, _k = _m.group(1), _m.group(2), _m.group(3)
        _a = _js.rfind('\n', 0, _m.start()) + 1; _e = _js.find('\n', _m.end()); _line = _js[_a:_e]
        _attr = 'data-i18n-title' if _pp == 'title' else 'data-i18n'
        if re.search(re.escape(_v) + r"\.setAttribute\('" + _attr + r"',\s*'" + re.escape(_k) + r"'\)", _line): continue
        _own = None
        for _st, _nm in _fst:
            if _st < _m.start(): _own = _nm
            else: break
        if _own in _hooks: continue
        _po = _js.rfind('openPanel(', 0, _m.start()); _inpanel = False
        if _po >= 0:
            _d = 0; _q = _po + len('openPanel')
            while _q < len(_js):
                if _js[_q] == '(': _d += 1
                elif _js[_q] == ')':
                    _d -= 1
                    if _d == 0: break
                _q += 1
            _inpanel = _q > _m.start()
        if _inpanel: continue
        errors.append("บรรทัด {} {}.{}=t('{}') ไม่มี {} — กด TH/EN แล้วไม่เปลี่ยนภาษา (ดู UI_STANDARD.md ข้อ 6)".format(_off + _js.count('\n', 0, _m.start()) + 1, _v, _pp, _k, _attr))

    # ---- 21) ปุ่มในแถบจัดรูปแบบ (#typobar) ที่แก้เมนู ต้องสร้างจุด Undo (บั๊ก 7 ต.ค. 2026: "ล้างรูปแบบ" / "ล้างรูปแบบจุดที่เลือก" ไม่มี Undo + ไม่เตือนก่อนปิดแท็บ) ----
    #   ทางที่นับว่าสร้างจุด Undo: markDirty( / _snapNow( / openPanel( (onOk ของ panel) / document.execCommand(คำสั่งแก้ข้อความ) (เบราว์เซอร์ยิง input → markDirty)
    #   ไล่จาก onclick หรือ addEventListener('click') ของปุ่ม ลึก 4 ชั้น · ปุ่มที่ไม่ได้แก้เมนูต้องอยู่ใน _NOEDIT21 พร้อมเหตุผล · ดู UI_STANDARD.md ข้อ 6
    _NOEDIT21 = {
        'typoCpCaret': 'เปิด/ปิดกล่องเลือกสี',
        'typoCpAdd': 'เปิดหน้าต่างสีที่กำหนดเอง (ตกลงในหน้าต่าง = ทาสีผ่าน applyColorRange ซึ่งมี markDirty)',
        'typoCpDlgCancel': 'ปิดหน้าต่างสีโดยไม่เปลี่ยนอะไร',
        'typoCpDlgEye': 'ดูดสีจากหน้าจอใส่หน้าต่างสี (ยังไม่ทาจนกว่าจะกดตกลง)',
        'typoOlCaret': 'เปิด/ปิดรายการความหนาเส้นขอบ (เลือกความหนา = typoOutlineSetWidth ซึ่งมี markDirty)',
    }
    _js21 = '\n'.join(re.findall(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', txt, re.I))
    def _blk21(src, k):
        _d = 0; _j = k
        while _j < len(src):
            if src[_j] == '{': _d += 1
            elif src[_j] == '}':
                _d -= 1
                if _d == 0: break
            _j += 1
        return src[k:_j + 1]
    _F21 = {}
    for _m in re.finditer(r'(?:^|[\n;{}])\s*function\s+([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{', _js21):
        _F21.setdefault(_m.group(1), _blk21(_js21, _m.end() - 1))
    def _dirty21(body, depth=0, seen=None):
        seen = seen if seen is not None else set()
        if re.search(r"\b(markDirty|_snapNow|openPanel)\s*\(|execCommand\(\s*(?!'styleWithCSS')", body): return True
        if depth >= 4: return False
        for _c in set(re.findall(r'\b([A-Za-z_$][\w$]*)\s*\(', body)):
            if _c in _F21 and _c not in seen:
                seen.add(_c)
                if _dirty21(_F21[_c], depth + 1, seen): return True
        return False
    _tb = txt.find('id="typobar"')
    if _tb < 0:
        errors.append('ไม่พบ #typobar — lint ข้อ 21 ตรวจไม่ได้')
    else:
        _tbEnd = txt.find('</div>', txt.find('data-i18n="grp.format"', _tb))
        for _m in re.finditer(r'<button\b[^>]*\bid="([\w-]+)"[^>]*>', txt[_tb:_tbEnd]):
            _bid = _m.group(1)
            _bodies = re.findall(r'onclick="([^"]*)"', _m.group(0))
            _nOn = len(_bodies)
            for _lm in re.finditer(r"getElementById\('" + re.escape(_bid) + r"'\)\.addEventListener\('click',\s*function\s*\([^)]*\)\s*\{", _js21):
                _bodies.append(_blk21(_js21, _lm.end() - 1))
            if _nOn and len(_bodies) > _nOn:
                errors.append('ปุ่ม #{} ผูก click 2 ทาง (onclick + addEventListener) — กดครั้งเดียวทำงาน 2 รอบ (ดู UI_STANDARD.md ข้อ 6)'.format(_bid))
            if _bid not in _NOEDIT21 and not any(_dirty21(_b) for _b in _bodies):
                errors.append('ปุ่ม #{} ในแถบจัดรูปแบบไม่สร้างจุด Undo (ไม่ถึง markDirty/_snapNow) — ถ้าไม่ได้แก้เมนูให้ใส่ใน _NOEDIT21 พร้อมเหตุผล (ดู UI_STANDARD.md ข้อ 6)'.format(_bid))

    # ---- 22) ผลการกระทำห้ามถูกข้อความสถานะทับ + ข้อความสถานะไม่จดบันทึก (บั๊ก 7 ต.ค. 2026: กดล้างรูปแบบแล้ว "เลือกอยู่" ทับผลภายใน 5ms ผู้ใช้เห็นว่าไม่ทำงาน · บันทึกเต็มไปด้วย "เลือกอยู่") ----
    #   key ใน _HINT22 (ข้อความสถานะ) ต้องส่งผ่าน _statusHint() เท่านั้น — ห้ามผ่าน flashStatus/setStatus/logAdd (จะจดบันทึก/ทับผล)
    #   flashStatus ต้องจำ selection ตอนแจ้งผล (_selHold=) · _statusHint ต้องเช็ค _selHold ก่อนแสดง · ดู UI_STANDARD.md ข้อ 6
    _HINT22 = {'fl.selInfo'}
    for _m in re.finditer(r"\b(flashStatus|setStatus|logAdd|_logFromFlash)\s*\([^;\n]*?tk\('([\w.]+)'", txt):
        if _m.group(2) in _HINT22:
            errors.append("บรรทัด {} ส่งข้อความสถานะ '{}' ผ่าน {}() — ใช้ _statusHint() (ไม่จดบันทึก ไม่ทับผล · ดู UI_STANDARD.md ข้อ 6)".format(txt.count('\n', 0, _m.start()) + 1, _m.group(2), _m.group(1)))
    _fs22 = re.search(r'\nfunction flashStatus\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _fs22 or '_selHold=' not in _fs22.group(0):
        errors.append('flashStatus ไม่จำ selection ตอนแจ้งผล (_selHold=) — ข้อความสถานะจะทับผลได้ (ดู UI_STANDARD.md ข้อ 6)')
    _sh22 = re.search(r'\nfunction _statusHint\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _sh22 or '_selHold' not in _sh22.group(0):
        errors.append('ไม่พบ _statusHint() ที่เช็ค _selHold — ข้อความสถานะต้องไม่ทับผล (ดู UI_STANDARD.md ข้อ 6)')

    # ---- 21b) ทุกทางที่แทรกรูปแบบลงช่อง (insertNode) ต้องมีจุด Undo ในทางนั้นเอง (บั๊ก 7 ต.ค. 2026: ทาสีเฉพาะส่วนที่ไฮไลท์ไม่ markDirty — lint ข้อ 21 ไม่จับเพราะเห็น markDirty ในทาง "ทั้งช่อง" ของฟังก์ชันเดียวกัน) ----
    #   หลัง insertNode( ต้องมี markDirty( / _snapNow( ก่อนถึง return หรือท้ายฟังก์ชัน · ฟังก์ชันตัวช่วยที่ผู้เรียกเป็นคนสร้างจุด Undo ใส่ใน _HELPER21B พร้อมเหตุผล
    #   _PENDING21B = รู้แล้วว่าขาด รอผู้ใช้ตัดสินใจ → เตือนทุกครั้งที่ commit (ไม่บล็อก) · ดู UI_STANDARD.md ข้อ 6
    _HELPER21B = {'_typoWrapRange': 'ตัวช่วยของ ใช้ทั้งประเภท — typoApplyAllSame เรียก markDirty หลังทำครบทุกช่อง'}
    _PENDING21B = {}  # 8 ต.ค. 2026: applyFontSizePx ถูกลบ (ผู้ใช้ตัดสินใจตัดขนาดตัวอักษรบางคำออก)
    _js21b = '\n'.join(re.findall(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', txt, re.I))
    for _m in re.finditer(r'(?:^|[\n;{}])\s*function\s+([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{', _js21b):
        _nm = _m.group(1); _k = _m.end() - 1; _d = 0; _j = _k
        while _j < len(_js21b):
            if _js21b[_j] == '{': _d += 1
            elif _js21b[_j] == '}':
                _d -= 1
                if _d == 0: break
            _j += 1
        _body = _js21b[_k:_j + 1]
        if 'insertNode(' not in _body or _nm in _HELPER21B: continue
        for _im in re.finditer(r'insertNode\(', _body):
            _rest = _body[_im.end():]
            _ret = re.search(r'\breturn\b', _rest)
            _seg = _rest[:_ret.start()] if _ret else _rest
            if not re.search(r'\b(markDirty|_snapNow)\s*\(', _seg):
                _msg21b = '{}() แทรกรูปแบบลงช่อง (insertNode) แต่ทางนั้นไม่สร้างจุด Undo (markDirty/_snapNow) (ดู UI_STANDARD.md ข้อ 6)'.format(_nm)
                if _nm in _PENDING21B: warnings.append(_msg21b + ' — รอตัดสินใจ: ' + _PENDING21B[_nm])
                else: errors.append(_msg21b)
                break

    # ---- 23) คำว่า "บันทึก" ใช้กับ Save เท่านั้น — ประวัติ/log ใช้ "ประวัติ" (ตกลงกับผู้ใช้ 7 ต.ค. 2026: "ล้างบันทึก" อ่านเป็น ล้างไฟล์ที่ Save ไว้) ----
    #   ข้อความภาษาไทยของ key ประวัติ (log.* · ttl.closeLog · pnl.clearLog* · fl.log*) ห้ามมีคำว่า "บันทึก" · ดู UI_STANDARD.md ข้อ 6
    _thA23 = txt.find('th:{', txt.find('var I18N={')); _enA23 = txt.find('en:{', _thA23)
    for _k, _v in re.findall(r"'([A-Za-z0-9_.]+)':'((?:[^'\\]|\\.)*)'", txt[_thA23:_enA23]):
        if (_k.startswith('log.') or _k == 'ttl.closeLog' or _k.startswith('pnl.clearLog') or _k.startswith('fl.log')) and 'บันทึก' in _v.replace('บันทึกแล้วล้าง', ''):  # บันทึกแล้วล้าง = Save and Clear (กริยา Save · แบบ Windows Event Viewer) ไม่ใช่ log
            errors.append("ข้อความ '{}' ใช้คำว่า \"บันทึก\" กับประวัติ — ใช้ \"ประวัติ\" (บันทึก = Save · ดู UI_STANDARD.md ข้อ 6)".format(_k))

    # ---- 24) หน้าต่าง Save ทุกอันต้องไม่มี "All Files (*.*)" (ตกลงกับผู้ใช้ 7 ต.ค. 2026: เลือก All Files แล้วตั้งชื่อ .txt = ได้ไฟล์ที่ชื่อไม่ตรงกับเนื้อหา) ----
    #   showSaveFilePicker({...}) ต้องมี excludeAcceptAllOption:true · และฟังก์ชันนั้นต้องตรวจนามสกุลของ .name ก่อนเขียน (หน้าเว็บไม่รู้ว่าผู้ใช้เลือก Save as type อันไหน) · ดู UI_STANDARD.md ข้อ 6
    for _m in re.finditer(r'showSaveFilePicker\(\{', txt):
        _q = txt.find('})', _m.end())
        _ln = txt.count('\n', 0, _m.start()) + 1
        if 'excludeAcceptAllOption:true' not in txt[_m.end():_q]:
            errors.append('บรรทัด {} หน้าต่าง Save มี "All Files" (ไม่มี excludeAcceptAllOption:true) — ผู้ใช้ตั้งนามสกุลอะไรก็ได้ ไฟล์จะไม่ตรงกับเนื้อหา (ดู UI_STANDARD.md ข้อ 6)'.format(_ln))
        _w = txt.find('createWritable(', _m.end())
        _seg24 = txt[_q:_w] if _w > 0 else ''
        if _w < 0 or not (re.search(r'\.name\b', _seg24) and re.search(r'\b(test|slice|endsWith)\(', _seg24)):
            errors.append('บรรทัด {} เขียนไฟล์โดยไม่ตรวจนามสกุลของชื่อที่ผู้ใช้เลือก (ดู UI_STANDARD.md ข้อ 6)'.format(_ln))

    # ---- 25) เส้นคั่นกลุ่มในแถบเครื่องมือต้องมองเห็นทั้งตอนกลุ่มเปิดและปิด (ผู้ใช้ 7 ต.ค. 2026: เส้นจางมาก ตอนกลุ่มปิดแยกกลุ่มไม่ออก) ----
    #   ห้ามตั้ง opacity ที่ตัว .rgroup (เส้นคั่น = border-right ของ .rgroup จะจางตาม) — ให้จางที่ .rgroup>* แทน
    #   สีเส้นคั่น (#edribbon .rgroup border-right) ต้องต่างจากพื้น #faf9f8 อย่างน้อย 2:1 · ดู UI_STANDARD.md ข้อ 7
    _css25 = '\n'.join(re.findall(r'<style[^>]*>([\s\S]*?)</style>', txt))
    _css25 = re.sub(r'/\*[\s\S]*?\*/', '', _css25)
    for _m in re.finditer(r'([^{}]+)\{([^{}]*)\}', _css25):
        _sels = [x.strip() for x in _m.group(1).split(',')]
        if re.search(r'(?<![\w-])opacity\s*:', _m.group(2)) and any(re.search(r'\.rgroup$', x) for x in _sels):
            errors.append('opacity ตั้งที่ตัว .rgroup ({}) — เส้นคั่นกลุ่มจะจางตาม ใช้ .rgroup>* (ดู UI_STANDARD.md ข้อ 7)'.format(_m.group(1).strip()[:80]))
    _sep = re.search(r'#edribbon \.rgroup\{[^}]*border-right:\s*1px solid (#[0-9a-fA-F]{6})', _css25)
    if not _sep:
        errors.append('ไม่พบสีเส้นคั่นกลุ่ม (#edribbon .rgroup border-right) — lint ข้อ 25 ตรวจไม่ได้')
    else:
        def _lum25(h):
            _c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            _c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in _c]
            return 0.2126 * _c[0] + 0.7152 * _c[1] + 0.0722 * _c[2]
        _a, _b = sorted([_lum25(_sep.group(1)), _lum25('#faf9f8')], reverse=True)
        if (_a + 0.05) / (_b + 0.05) < 2.0:
            errors.append('เส้นคั่นกลุ่ม {} ต่างจากพื้นแค่ {:.2f}:1 (ต้อง ≥ 2:1 · ดู UI_STANDARD.md ข้อ 7)'.format(_sep.group(1), (_a + 0.05) / (_b + 0.05)))

    # ---- 26) ประวัติต้องเปลี่ยนภาษาตาม TH/EN (ตกลงกับผู้ใช้ 8 ต.ค. 2026 · แบบ Windows Event Viewer เก็บ key + ค่า) ----
    #   logAdd( ห้ามส่ง String(...) หรือ t(...) — ใช้ tk()/tkj() (String() ทำให้เสีย key แปลใหม่ไม่ได้)
    #   logAdd ต้องเก็บ e.m (_ttSer) · แถว/CSV ต้องแสดงผ่าน _actlogText · applyLang ต้องเรียก _actlogRelang · ดู UI_STANDARD.md ข้อ 6
    for _m in re.finditer(r'\blogAdd\(([^;\n]*)\)', txt):
        if re.search(r'(?<![\w.])(String|t)\(', _m.group(1)):
            errors.append('บรรทัด {} logAdd({}) — ส่งเป็นข้อความสำเร็จรูป ประวัติจะไม่เปลี่ยนภาษา ใช้ tk()/tkj() (ดู UI_STANDARD.md ข้อ 6)'.format(txt.count('\n', 0, _m.start()) + 1, _m.group(1)[:40]))
    _la26 = re.search(r'\nfunction logAdd\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _la26 or '_ttSer(' not in _la26.group(0):
        errors.append('logAdd ไม่เก็บ key + ค่า (_ttSer) — ประวัติจะไม่เปลี่ยนภาษาตาม TH/EN (ดู UI_STANDARD.md ข้อ 6)')
    if re.search(r"\.textContent=e\.msg\b|_logTypeLabel\(arr\[i\]\.type\),arr\[i\]\.msg\]", txt):
        errors.append('แสดง/ส่งออกประวัติจาก e.msg ตรงๆ — ใช้ _actlogText(e) (ดู UI_STANDARD.md ข้อ 6)')
    _al26 = re.search(r'\nfunction applyLang\(\)\{[\s\S]*?\n\}', txt)
    if not _al26 or '_actlogRelang(' not in _al26.group(0):
        errors.append('applyLang ไม่แปลประวัติใหม่ (_actlogRelang) (ดู UI_STANDARD.md ข้อ 6)')
    _ft26 = re.search(r'\nfunction _actlogFieldType\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _ft26 and re.search(r"return t\('", _ft26.group(0)):
        errors.append('_actlogFieldType คืน t(...) — ชื่อช่องในประวัติจะไม่เปลี่ยนภาษา ใช้ tk() (ดู UI_STANDARD.md ข้อ 6)')

    # ---- 27) ไม่มีขนาดตัวอักษรบางคำ (ผู้ใช้ตัดสินใจ 28 ก.ย. 2026 · ยืนยัน 8 ต.ค. 2026: ไฮไลท์ + กด +/− = เปลี่ยนทั้งช่อง) ----
    #   ห้ามสร้าง span แล้วตั้ง .style.fontSize ในฟังก์ชันเดียวกัน · "ใช้ทั้งประเภท" ต้องไม่คัดลอก fontSize เป็นช่วงตัวอักษร · ดู UI_STANDARD.md ข้อ 6
    _js27 = '\n'.join(re.findall(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', txt, re.I))
    for _m in re.finditer(r'(?:^|[\n;{}])\s*function\s+([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{', _js27):
        _k = _m.end() - 1; _d = 0; _j = _k
        while _j < len(_js27):
            if _js27[_j] == '{': _d += 1
            elif _js27[_j] == '}':
                _d -= 1
                if _d == 0: break
            _j += 1
        _b = _js27[_k:_j + 1]
        if "createElement('span')" in _b and re.search(r'\.style\.fontSize\s*=', _b):
            errors.append('{}() สร้าง span แล้วตั้งขนาดตัวอักษร = ขนาดบางคำ (ตัดออกแล้ว · ดู UI_STANDARD.md ข้อ 6)'.format(_m.group(1)))
    _cf27 = re.search(r'\nfunction _typoCaptureFormat\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _cf27 and "k!=='fontSize'" not in _cf27.group(0):
        errors.append('_typoCaptureFormat คัดลอก fontSize เป็นช่วงตัวอักษร — ขนาดบางคำตัดออกแล้ว (ดู UI_STANDARD.md ข้อ 6)')

    # ---- 28) ตัวตรวจล้นหน้าต้องวัดแบบไม่มีโหมดแก้ + ผลของปุ่มต้องไม่หายตอนล้นหน้า (ผู้ใช้ 8 ต.ค. 2026) ----
    #   checkOverflow ต้องเอา class editmode/imgmode/headermode/pricemode ออกระหว่างวัด และใส่คืนใน finally (โหมดแก้เพิ่มระยะ → เตือนล้นปลอม)
    #   flashStatus / _statusHint / setStatus ห้ามหยุดเพราะ _overflowWarn (เดิมผลไม่แสดงและไม่จดประวัติ) — ล้นหน้าแสดงเป็นป้าย (_overflowPages) · ดู UI_STANDARD.md ข้อ 7
    _co28 = re.search(r'\nfunction checkOverflow\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _co28:
        errors.append('ไม่พบ checkOverflow — lint ข้อ 28 ตรวจไม่ได้')
    else:
        _b28 = _co28.group(0)
        for _c in ('editmode', 'imgmode', 'headermode', 'pricemode'):
            if "'" + _c + "'" not in _b28:
                errors.append("checkOverflow ไม่เอา class '{}' ออกระหว่างวัด — โหมดแก้เพิ่มระยะ จะเตือนล้นปลอม (ดู UI_STANDARD.md ข้อ 7)".format(_c))
        if 'finally' not in _b28:
            errors.append('checkOverflow ไม่ใส่ class โหมดคืนใน finally — ถ้าวัดพังจะค้างนอกโหมดแก้ (ดู UI_STANDARD.md ข้อ 7)')
    for _fn in ('flashStatus', '_statusHint', 'setStatus'):
        _m28 = re.search(r'\nfunction ' + _fn + r'\([^)]*\)\{[\s\S]*?\n\}', txt)
        if _m28 and re.search(r'_overflowWarn\s*\)\s*return|_overflowWarn\s*\|\||\|\|\s*_overflowWarn', _m28.group(0)):
            errors.append('{}() หยุดทำงานตอนล้นหน้า (_overflowWarn) — ผลจะไม่แสดง/ไม่จดประวัติ ใช้ป้ายล้นหน้าแทน (ดู UI_STANDARD.md ข้อ 7)'.format(_fn))

    # ---- 29) ปุ่มชั่วคราวของป้ายกลุ่ม (× / + ป้าย) ต้องไม่หลุดลงไฟล์ / snapshot / สำเนา (ผู้ใช้ 8 ต.ค. 2026) ----
    #   ทุกรายการ querySelectorAll ที่ตัดปุ่มแก้ไข (มี .ed-delgroup) ต้องตัด .ed-badgeadd และ .ed-badgedel ด้วย
    #   _restorePages ต้องเรียก _badgeDecorate (snapshot ไม่เก็บปุ่ม → undo ในโหมดแก้รูปต้องใส่ปุ่มคืน) · ดู UI_STANDARD.md ข้อ 7
    for _m29 in re.finditer(r"querySelectorAll\('([^']*\.ed-delgroup[^']*)'\)", txt):
        _l29 = txt.count('\n', 0, _m29.start()) + 1
        for _c29 in ('.ed-badgeadd', '.ed-badgedel'):
            if _c29 not in _m29.group(1):
                errors.append('บรรทัด {}: รายการตัดปุ่มแก้ไขไม่มี {} — ปุ่มป้ายกลุ่มจะหลุดลงไฟล์/undo (ดู UI_STANDARD.md ข้อ 7)'.format(_l29, _c29))
    _rp29 = re.search(r'\nfunction _restorePages\([^)]*\)\{[\s\S]*?\n\}', txt)
    if 'secimg' in txt and (not _rp29 or '_badgeDecorate' not in _rp29.group(0)):
        errors.append('_restorePages ไม่เรียก _badgeDecorate — Undo ในโหมดแก้รูปแล้วปุ่ม × / + ป้าย หาย (ดู UI_STANDARD.md ข้อ 7)')

    # ---- 28b) ครั้งแรกที่ล้นหน้า: ผลของปุ่ม + คำเตือนเต็มในข้อความเดียว จดประวัติครั้งเดียว (ผู้ใช้ 8 ต.ค. 2026 12:29) ----
    _fs28b = re.search(r'\nfunction flashStatus\([^)]*\)\{[\s\S]*?\n\}', txt)
    _co28b = re.search(r'\nfunction checkOverflow\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _fs28b or '_ovfFresh' not in _fs28b.group(0) or '_ovfCombine' not in _fs28b.group(0):
        errors.append('flashStatus ไม่รวมผลกับคำเตือนตอนเพิ่งล้นหน้า (_ovfFresh/_ovfCombine) — ผลจะทับคำเตือนเต็ม (ดู UI_STANDARD.md ข้อ 7)')
    if not _co28b or '_ovfCombine' not in _co28b.group(0) or '_ovfFresh=true' not in _co28b.group(0):
        errors.append('checkOverflow ไม่รวมคำเตือนเต็มกับผลที่เพิ่งแสดง / ไม่ตั้ง _ovfFresh (ดู UI_STANDARD.md ข้อ 7)')

    # ---- 30) เลือกสีเองต้องใช้หน้าต่างของแอป ไม่ใช่ตัวเลือกสีของเบราว์เซอร์ (ผู้ใช้ 8 ต.ค. 2026) ----
    #   ตัวเลือกสีของเบราว์เซอร์: ตั้งให้ขึ้น HEX ไม่ได้ · ไม่มีตกลง/ยกเลิก · เดิมทาสีทุกครั้งที่ลาก (span ซ้อนกัน)
    #   ห้ามเปิด <input type=color> (.click() / showPicker) · ห้ามผูก input/change กับ #typoColor
    #   ระหว่างเลือกในหน้าต่างห้ามทาสี: applyColorRange เรียกได้เฉพาะใน _cpDlgOk · ดู UI_STANDARD.md ข้อ 6
    if re.search(r"getElementById\('typoColor'\)\.(click|showPicker)\(", txt) or re.search(r"getElementById\('typoColor'\)\.addEventListener\('(input|change)'", txt):
        errors.append('#typoColor ถูกเปิดหรือผูก input/change — เลือกสีเองต้องใช้หน้าต่างสีของแอป (HEX หลัก · ตกลง/ยกเลิก) (ดู UI_STANDARD.md ข้อ 6)')
    if 'id="typoCpDlg"' not in txt:
        errors.append('ไม่พบหน้าต่างสีที่กำหนดเอง #typoCpDlg (ดู UI_STANDARD.md ข้อ 6)')
    for _fn30 in ('_cpDlgRender', '_cpDlgSetHex', '_cpDragAt', '_cpDlgOpen'):
        _m30 = re.search(r'\n\s*function ' + _fn30 + r'\([^)]*\)\{[\s\S]*?\n  \}', txt)
        if not _m30:
            errors.append('ไม่พบ {} — lint ข้อ 30 ตรวจไม่ได้'.format(_fn30))
        elif 'applyColorRange' in _m30.group(0) or 'markDirty' in _m30.group(0):
            errors.append('{} ทาสี/แก้เมนูระหว่างเลือกในหน้าต่างสี — ต้องทาเฉพาะตอนกดตกลง (_cpDlgOk) (ดู UI_STANDARD.md ข้อ 6)'.format(_fn30))
    _ok30 = re.search(r'\n\s*function _cpDlgOk\([^)]*\)\{[\s\S]*?\n  \}', txt)
    if not _ok30 or 'applyColorRange' not in _ok30.group(0) or '_saveCustom' not in _ok30.group(0):
        errors.append('_cpDlgOk ต้องทาสี (applyColorRange) และเก็บสี (_saveCustom) (ดู UI_STANDARD.md ข้อ 6)')

    # ---- 31) เส้นขอบตัวอักษร (text-shadow) ต้องตามทุกเครื่องมือจัดรูปแบบ (ผู้ใช้ 8 ต.ค. 2026) ----
    #   ใช้ทั้งประเภทคัดลอก (base มี textShadow) · สีขอบตามช่องปลายทาง (_typoApplyFormat เรียก _olRefresh) · คืนค่าล้าง (text-shadow)
    #   ทาสีทั้งช่อง → สีขอบตาม (applyColorRange เรียก _olRefresh) · ดู UI_STANDARD.md ข้อ 6
    #   18:17 เปิดให้ทุกช่อง + เลือกความหนา: ปุ่มต้องเช็ค _olState (เส้นจุด / ขอบจะกลืนกับพื้น = จาง + เหตุผล) · _olRefresh ต้องคงความหนาเดิม (_olWidthOf)
    if 'id="typoOutline"' in txt:
        if not re.search(r"_TYPO_FMT_PROPS\.concat\(\[[^\]]*'textShadow'", txt):
            errors.append('ใช้ทั้งประเภทไม่คัดลอกเส้นขอบ (_typoCaptureFormat base ไม่มี textShadow) (ดู UI_STANDARD.md ข้อ 6)')
        _af31 = re.search(r'\nfunction _typoApplyFormat\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _af31 or '_olRefresh(' not in _af31.group(0):
            errors.append('_typoApplyFormat ไม่เรียก _olRefresh — เส้นขอบที่คัดลอกมาจะใช้สีขอบของช่องต้นทาง (ดู UI_STANDARD.md ข้อ 6)')
        _ac31 = re.search(r'\n\s*function applyColorRange\([^)]*\)\{[\s\S]*?\n  \}', txt)
        if not _ac31 or '_olRefresh(' not in _ac31.group(0):
            errors.append('applyColorRange ไม่เรียก _olRefresh — เปลี่ยนสีทั้งช่องแล้วสีขอบไม่ตาม (ดู UI_STANDARD.md ข้อ 6)')
        if not re.search(r"\[[^\]]*'text-decoration-line','text-shadow'\]\.forEach\(function\(pp\)\{el\.style\.removeProperty\(pp\);\}\)", txt):
            errors.append('คืนค่าไม่ล้างเส้นขอบ (text-shadow) (ดู UI_STANDARD.md ข้อ 6)')
        _cf31 = re.search(r'\nfunction _olColorOf\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _cf31 or 'createTreeWalker' not in _cf31.group(0):
            errors.append('_olColorOf ต้องอ่านสีที่เห็นจริงจากตัวอักษรในช่อง (createTreeWalker) — ไฮไลท์แล้วทาสี สีอยู่ใน span ข้างใน (บั๊ก 8 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 6)')
        if _ac31 and _ac31.group(0).count('_olSync(') < 2:
            errors.append('applyColorRange ต้องเรียก _olSync ทั้งทาทั้งช่องและทาแบบไฮไลท์ — ปุ่มเส้นขอบไม่ตามสีใหม่ (บั๊ก 8 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 6)')
        _cs31 = re.search(r'\nfunction typoClearSel\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _cs31 or '_olSync(' not in _cs31.group(0):
            errors.append('typoClearSel ต้องเรียก _olRefresh/_olSync — ล้างสีบางคำแล้วปุ่มเส้นขอบไม่ตาม (ดู UI_STANDARD.md ข้อ 6)')
        # 19:23 สีขอบเลือกเองได้ (data-ol-c): คงไว้เมื่อเปลี่ยนสีตัวอักษร · ใช้ทั้งประเภทคัดลอก · คืนค่าล้าง · ปุ่ม A ไม่ใส่ขอบที่มองไม่เห็น (เปิด ▾ ให้เลือกสี)
        _rf31b = re.search(r'\nfunction _olRefresh\([^)]*\)\{[^\n]*', txt)
        if not _rf31b or '_olEdgeFor(' not in _rf31b.group(0):
            errors.append('_olRefresh ไม่ใช้ _olEdgeFor — สีขอบที่เลือกเองจะหายเมื่อเปลี่ยนสีตัวอักษร (ดู UI_STANDARD.md ข้อ 6)')
        if not _af31 or 'data-ol-c' not in _af31.group(0):
            errors.append('_typoApplyFormat ไม่คัดลอกสีขอบที่เลือกเอง (data-ol-c) — ใช้ทั้งประเภทแล้วสีขอบกลายเป็นอัตโนมัติ (ดู UI_STANDARD.md ข้อ 6)')
        _rs31 = re.search(r'\nfunction typoResetSel\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _rs31 or "removeAttribute('data-ol-c')" not in _rs31.group(0):
            errors.append('คืนค่าไม่ล้างสีขอบที่เลือกเอง (data-ol-c) (ดู UI_STANDARD.md ข้อ 6)')
        _tgA = re.search(r'\nfunction typoOutlineToggle\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _tgA or '_olPopOpen(' not in _tgA.group(0) or 'st.cand' not in _tgA.group(0):
            errors.append('typoOutlineToggle ต้องเปิด ▾ ให้เลือกสีขอบเมื่อขอบจะมองไม่เห็น (_olPopOpen · st.cand) — ห้ามใส่ขอบที่มองไม่เห็น (ดู UI_STANDARD.md ข้อ 6)')
        _sy31 = re.search(r'\nfunction _olSync\([^)]*\)\{[\s\S]*?\n\}', txt)
        if 'id="typoOlBar"' not in txt or not _sy31 or 'typoOlBar' not in _sy31.group(0):
            errors.append('ปุ่ม A ต้องแสดงสีขอบที่จะใช้ (แถบ #typoOlBar อัปเดตใน _olSync) — ผู้ใช้ 8 ต.ค. 2026: กด A แล้วจู่ๆ ได้สีที่ไม่รู้ที่มา (ดู UI_STANDARD.md ข้อ 6)')
        for _fn31 in ('typoOutlineToggle', 'typoOutlineSetWidth'):
            _tg31 = re.search(r'\nfunction ' + _fn31 + r'\([^)]*\)\{[\s\S]*?\n\}', txt)
            if not _tg31 or '_olState(' not in _tg31.group(0):
                errors.append('{} ไม่เช็ค _olState — ปุ่มจะใส่เส้นขอบที่มองไม่เห็น หรือใส่ให้เส้นจุด (ดู UI_STANDARD.md ข้อ 6)'.format(_fn31))
        _st31 = re.search(r'\nfunction _olState\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _st31 or '.line' not in _st31.group(0) or '_olBgOf(' not in _st31.group(0):
            errors.append('_olState ต้องเช็คเส้นจุด (.line) และพื้นจริงใต้ช่อง (_olBgOf) (ดู UI_STANDARD.md ข้อ 6)')
        _rf31 = re.search(r'\nfunction _olRefresh\([^)]*\)\{[^\n]*', txt)
        if not _rf31 or '_olWidthOf(' not in _rf31.group(0):
            errors.append('_olRefresh ไม่คงความหนาเดิม (_olWidthOf) — เปลี่ยนสีแล้วเส้นขอบกลับเป็น 2px (ดู UI_STANDARD.md ข้อ 6)')

    # ---- report ----
    print("=" * 54)
    print(" OE Menu Editor — pre-save lint")
    print("=" * 54)
    print(" ไฟล์:", os.path.basename(PATH), "({:,} bytes)".format(len(txt)))
    print(" braces {}:{}  parens {}:{}  <script>:{}/{}".format(
        txt.count("{"), txt.count("}"), txt.count("("), txt.count(")"),
        txt.count("<script"), txt.count("</script>")))
    if errors:
        print("\n [X] FAIL — {} error(s):".format(len(errors)))
        for e in errors: print("     -", e)
    else:
        print("\n [OK] PASS — ไม่มี error ที่บล็อก")
    if warnings:
        print("\n [!] {} warning(s):".format(len(warnings)))
        for w in warnings: print("     -", w)
    print()
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
