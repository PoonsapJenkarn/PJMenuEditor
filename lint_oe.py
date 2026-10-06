#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pre-save lint สำหรับ OEIsanHotpotMenuWithImageEditor.html
จับบั๊ก pattern ที่เคยหลุดจริง — เปลี่ยน 'ความจำ' เป็น check อัตโนมัติ

รันเอง:   python lint_oe.py
เป็น git hook: ก็อปเป็น .git/hooks/pre-commit (ดูวิธีท้ายไฟล์)

exit code: 0 = ผ่าน, 1 = พบ error (บล็อก commit ถ้าเป็น hook)
"""
import re, sys, os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "OEIsanHotpotMenuWithImageEditor.html")

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
    _FILTERED16 = {'ep-input', 'ep-amt', 'ep-price', 'typoHex'}  # ช่องที่มีตัวกรองแล้ว — เพิ่มช่องใหม่ต้องมีตัวกรองก่อนแล้วค่อยใส่ชื่อที่นี่
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
