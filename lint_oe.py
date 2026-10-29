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
    #   strip verbatim OFL license <pre> (third-party text, not code — list markers 1)..5) ทำ paren ไม่สมดุลโดยธรรมชาติ · ผู้ใช้ 17 ต.ค. 2026)
    _bptxt = txt
    _ops = _bptxt.find('<pre class="ofl-text">')
    if _ops >= 0:
        _ope = _bptxt.find("</pre>", _ops)
        if _ope >= 0:
            _bptxt = _bptxt[:_ops] + _bptxt[_ope+6:]
    if _bptxt.count("{") != _bptxt.count("}"):
        errors.append("Brace imbalance: {{={} }}={}".format(_bptxt.count("{"), _bptxt.count("}")))
    if _bptxt.count("(") != _bptxt.count(")"):
        errors.append("Paren imbalance: (={} )={}".format(_bptxt.count("("), _bptxt.count(")")))

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
    _css = re.sub(r'@font-face\{[^{}]*\}', '', _css) # ตัดฟอนต์ฝัง (base64 บรรทัดยาว) ออกจาก CSS วิเคราะห์ layout — กัน regex O(n^2) (ผู้ใช้ 13 ต.ค. 2026)
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
    _FILTERED16 = {'ep-input', 'ep-amt', 'ep-price', 'typoHex', 'bgHex', 'bgRange', 'typoSize', 'typoCpDlgHex', 'typoOlHex', 'thcpHex', 'shd-num', 'gfontInput', 'zoomLvl', 'calInch', 'flAng', 'flLen'}  # ช่องที่มีตัวกรองแล้ว (gfontInput = ชื่อฟอนต์ ฟรีเท็กซ์ · ชื่อผิด = fl.gfontNotFound ไม่ต้องกรอง) — เพิ่มช่องใหม่ต้องมีตัวกรองก่อนแล้วค่อยใส่ชื่อที่นี่
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
        if 'secnote' in txt: _need.add('.sec-b > .secnote')  # หมายเหตุกลุ่ม (9 ต.ค. 2026)
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
        'typoCpApply': 'เปิด/ปิดถาดสี (ตกลงในถาด = _tcpCommit → applyColorRange ซึ่งมี markDirty)',
        'typoCpCaret': 'เปิด/ปิดกล่องเลือกสี',
        'typoCpAdd': 'เปิดหน้าต่างสีที่กำหนดเอง (ตกลงในหน้าต่าง = ทาสีผ่าน applyColorRange ซึ่งมี markDirty)',
        'typoCpDlgCancel': 'ปิดหน้าต่างสีโดยไม่เปลี่ยนอะไร',
        'typoCpDlgEye': 'ดูดสีจากหน้าจอใส่หน้าต่างสี (ยังไม่ทาจนกว่าจะกดตกลง)',
        'typoOlCaret': 'เปิด/ปิดรายการความหนาเส้นขอบ (เลือกความหนา = typoOutlineSetWidth ซึ่งมี markDirty)',
        'btnAddFont': 'เปิด dialog เลือกไฟล์ฟอนต์ — markDirty อยู่ใน _fontUploadFile ตอนไฟล์โหลดเสร็จ (async · lint #65 บังคับ markDirty ในนั้น)',
        'btnAddGFont': 'เปิด popover เลือกฟอนต์ Google (toggle) — ไม่ได้แก้เมนูเอง',
        'gfontSearchBtn': 'ค้นหาฟอนต์ Google ในรายการ — ไม่แก้เมนู (search เฉยๆ)',
        'gfontAddBtn': 'สั่งเพิ่มฟอนต์ Google — markDirty อยู่ใน _gfontAdd ตอน fetch เสร็จ (async · lint #66 บังคับ markDirty ในนั้น)',
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
    _css25 = re.sub(r'@font-face\{[^{}]*\}', '', _css25)
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
        for _c29 in ('.ed-badgeadd', '.ed-badgedel', '.ed-noteadd', '.ed-notedel'):  # + ปุ่มหมายเหตุกลุ่ม (9 ต.ค. 2026)
            if _c29 not in _m29.group(1):
                errors.append('บรรทัด {}: รายการตัดปุ่มแก้ไขไม่มี {} — ปุ่มชั่วคราว (ป้าย / หมายเหตุกลุ่ม) จะหลุดลงไฟล์/undo (ดู UI_STANDARD.md ข้อ 7)'.format(_l29, _c29))
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

    # ---- 32) แถบสีหัวกลุ่ม (--accent) ต้องตามสีชื่อกลุ่มทุกเครื่องมือ (ผู้ใช้ 8 ต.ค. 2026 22:05) ----
    #   ทาสีทั้งช่อง + ทาแบบไฮไลท์ (applyColorRange) · ล้างรูปแบบจุดที่ไฮไลท์ · ใช้ทั้งประเภท (_typoApplyFormat) → _secAccentFollow
    #   คืนค่า (typoResetSel) → _secAccentReset (กลับเป็นสีเดิม data-acc0) · ดู UI_STANDARD.md ข้อ 6
    def _fb32(name, ind):
        _m = re.search(r'\n' + ind + r'function ' + name + r'\([^)]*\)\{[\s\S]*?\n' + ind + r'\}', txt)
        return _m.group(0) if _m else ''
    if 'function _secAccentFollow(' not in txt:
        errors.append('ไม่พบ _secAccentFollow — แถบสีหัวกลุ่มจะไม่ตามสีชื่อกลุ่ม (ดู UI_STANDARD.md ข้อ 6)')
    else:
        if _fb32('applyColorRange', '  ').count('_secAccentFollow(') < 2:
            errors.append('applyColorRange ต้องเรียก _secAccentFollow ทั้งทาทั้งช่องและทาแบบไฮไลท์ (ดู UI_STANDARD.md ข้อ 6)')
        for _n32, _f32 in (('_typoApplyFormat', '_secAccentFollow('), ('typoClearSel', '_secAccentFollow('), ('typoResetSel', '_secAccentReset(')):
            if _f32 not in _fb32(_n32, ''):
                errors.append('{} ไม่เรียก {} — แถบสีหัวกลุ่มไม่ตาม (ดู UI_STANDARD.md ข้อ 6)'.format(_n32, _f32.rstrip('(')))

    # ---- 33) หมายเหตุกลุ่ม (.secnote) — เพิ่ม/แก้/ลบได้ทุกกลุ่ม (ผู้ใช้ 9 ต.ค. 2026) ----
    #   เดิม: ข้อความตายตัวใต้กลุ่มเครื่องดื่ม แก้ไม่ได้ · แถวใหม่ไปต่อใต้หมายเหตุ (insertBefore ปุ่ม เพิ่มรายการ)
    #   ต้อง: แก้ได้ในโหมดแก้ข้อความ + หลัง Undo · ปุ่ม + หมายเหตุ / × มาจาก decorate · แถวใหม่แทรกก่อนหมายเหตุ
    #   ปุ่มไม่พิมพ์/ไม่นับตอนวัดล้นหน้า · อยู่ในแถบรูปแบบ (TYPO_TYPES + ค่าเริ่มต้น) · ดู UI_STANDARD.md ข้อ 7
    if 'secnote' in txt:
        def _fb33(name):
            _m = re.search(r'\nfunction ' + name + r'\([^)]*\)\{[\s\S]*?\n\}', txt)
            return _m.group(0) if _m else ''
        for _n33 in ('toggleEdit', '_reapplyEditable'):
            if '.sec-b > .secnote' not in _fb33(_n33):
                errors.append('{} ไม่ทำให้หมายเหตุกลุ่ม (.secnote) แก้ได้ — หมายเหตุแก้ไม่ได้ / Undo แล้วแก้ไม่ได้ (ดู UI_STANDARD.md ข้อ 7)'.format(_n33))
        if '_noteDecorate(' not in _fb33('decorate'):
            errors.append('decorate ไม่เรียก _noteDecorate — ปุ่ม + หมายเหตุ / × ไม่ขึ้น หรือไม่หายตอนออกโหมดแก้ (ดู UI_STANDARD.md ข้อ 7)')
        if re.search(r'body\.insertBefore\(_nr,\s*btn\)', txt):
            errors.append('แถวใหม่แทรกก่อนปุ่ม เพิ่มรายการ ตรงๆ — จะไปอยู่ใต้หมายเหตุกลุ่ม ใช้ _secRowsEnd(body) (ดู UI_STANDARD.md ข้อ 7)')
        for _css33, _w33 in ((r'@media print\{([^{}]*)\{display:none !important;\}\}', 'พิมพ์'), (r'(body\.measuring \.ed-add,[^{]*)\{display:none !important;\}', 'วัดล้นหน้า')):
            if not any(('.ed-noteadd' in _m.group(1) and '.ed-notedel' in _m.group(1)) for _m in re.finditer(_css33, txt)):
                errors.append('CSS ซ่อนปุ่มตอน{} ไม่มี .ed-noteadd / .ed-notedel (ดู UI_STANDARD.md ข้อ 7)'.format(_w33))
        if not re.search(r"\{key:'secnote',\s*sel:'\.sec-b > \.secnote'", txt):
            errors.append('TYPO_TYPES ไม่มี secnote — หมายเหตุกลุ่มใช้แถบรูปแบบไม่ได้ (ดู UI_STANDARD.md ข้อ 7)')
        if not re.search(r'var _defaultStyles=\{[^}]*\bsecnote:null', txt):
            errors.append('_defaultStyles ไม่มี secnote — ตั้งค่าเริ่มต้นของหมายเหตุกลุ่มไม่ได้ (ดู UI_STANDARD.md ข้อ 7)')

    # ---- 34) ระยะขอบหน้า: ตัวตรวจล้นหน้าต้องใช้ค่าเดียวกับหน้าจริง · ทั้ง 4 ด้านไม่น้อยกว่าขอบที่เครื่องพิมพ์พิมพ์ไม่ได้ (ผู้ใช้ 9 ต.ค. 2026) ----
    #   ผู้ใช้วัดจากการพิมพ์จริง ≈ 2.5 mm → เผื่อ 3 mm · .page กับ body.measuring .page มีค่า padding แยกกัน 2 ที่ — แก้ที่เดียว = วัดล้นหน้าผิด
    _pp34 = re.search(r'\n\.page\{[^}]*?padding:([^;]+);', txt)
    _mp34 = re.search(r'body\.measuring \.page\{[^}]*?padding:([^;!]+?)\s*!important', txt)
    if not _pp34 or not _mp34:
        errors.append('หา padding ของ .page / body.measuring .page ไม่พบ — lint ข้อ 34 ตรวจไม่ได้ (ดู UI_STANDARD.md ข้อ 7)')
    else:
        _a34, _b34 = _pp34.group(1).split(), _mp34.group(1).split()
        if _a34 != _b34:
            errors.append('padding ของ .page ({}) ไม่เท่ากับ body.measuring .page ({}) — ตัวตรวจล้นหน้าจะวัดผิด (ดู UI_STANDARD.md ข้อ 7)'.format(' '.join(_a34), ' '.join(_b34)))
        _v34 = [float(x[:-2]) if x.endswith('mm') else None for x in _a34]
        _v34 = (_v34 * 4)[:4] if len(_v34) == 1 else (_v34 + _v34)[:4] if len(_v34) == 2 else (_v34 + [_v34[1]])[:4] if len(_v34) == 3 else _v34[:4]  # บน ขวา ล่าง ซ้าย
        for _n34, _x34 in zip(('บน', 'ขวา', 'ล่าง', 'ซ้าย'), _v34):  # ทั้ง 4 ด้าน — เครื่องพิมพ์ร้านพิมพ์ไม่ได้ ~2.5 mm เท่ากันทุกด้าน (ผู้ใช้ 9 ต.ค. 2026)
            if _x34 is None or _x34 < 3:
                errors.append('ขอบ{} ของ .page ต้องเป็น mm และไม่น้อยกว่า 3mm (ขอบที่เครื่องพิมพ์พิมพ์ไม่ได้) (ดู UI_STANDARD.md ข้อ 7)'.format(_n34))

    # ---- 35) ช่องกรอกในแถบเครื่องมือต้องพิมพ์ได้ (ผู้ใช้ 9 ต.ค. 2026: ช่อง HEX สีขอบคลิกแล้วพิมพ์ไม่ได้) ----
    #   #typobar mousedown → preventDefault (กันไม่ให้ไฮไลท์ในเมนูหาย) · ช่องกรอกต้องได้รับยกเว้น ไม่งั้นคลิกแล้วพิมพ์ไม่ได้
    _md35 = re.search(r"getElementById\('typobar'\)\.addEventListener\('mousedown',[^\n]*\n(?:[^\n]*\n){0,3}?[^\n]*saveSelection\(\); return; \}", txt)
    if not _md35:
        errors.append('หาตัวยกเว้นช่องกรอกใน mousedown ของ #typobar ไม่พบ — lint ข้อ 35 ตรวจไม่ได้ (ดู UI_STANDARD.md ข้อ 5)')
    else:
        # <input> พิมพ์ไม่ได้ ถ้าไม่ยกเว้น · <select> (เช่น typoLineStyle) dropdown ไม่เปิด ถ้าไม่ยกเว้น (ผู้ใช้ 10 ต.ค. 2026) · typo* อยู่ใน #typobar ทั้งหมด
        for _tag35 in ('input', 'select'):
            for _id35 in sorted(set(re.findall(r'<' + _tag35 + r'\b[^>]*\bid="(typo\w+)"', txt))):
                if "'" + _id35 + "'" not in _md35.group(0):
                    _why35 = 'คลิกแล้วพิมพ์ไม่ได้' if _tag35 == 'input' else 'คลิกแล้ว dropdown ไม่เปิด เปลี่ยนค่าไม่ได้'
                    errors.append('{} #{} ไม่อยู่ในตัวยกเว้น mousedown ของ #typobar — {} (ดู UI_STANDARD.md ข้อ 5)'.format(_tag35, _id35, _why35))
    _op35 = re.search(r'\n\s*function _cpDlgOpen\([^)]*\)\{[\s\S]*?\n  \}', txt)
    if 'id="typoOlPick"' in txt and (not _op35 or "'typoOlPick'" not in _op35.group(0)):
        errors.append('หน้าต่างสีที่กำหนดเองของสีขอบไม่ได้ขึ้นใต้ปุ่ม A (_cpDlgOpen ต้องย้ายไป #typoOlPick) (ดู UI_STANDARD.md ข้อ 5)')

    # ---- 36) เงารูป (.fimg data-shadow) — ไม่มี / อ่อน / ชัด ต่อรูป (ผู้ใช้ 9 ต.ค. 2026) ----
    #   ดู UI_STANDARD.md ข้อ 6 · ค่าเงาอยู่ใน CSS ที่เดียว · ห้าม box-shadow (กรอบสี่เหลี่ยมรอบรูปโปร่งใส)
    #   ห้ามกฎ filter บน .fimg>img ที่ไม่มี [data-shadow] (ปุ่ม "ไม่มี" จะไม่มีผลจริง) · ใส่ทุกหน้าต้องคัดลอกเงา
    #   Undo แทนรูปทั้งหน้า → รูปที่เลือกค้าง (หลุดจากหน้า) ต้องถูกยกเลิก ไม่งั้นปุ่มขึ้นว่าทำแล้วแต่หน้าไม่เปลี่ยน
    _css36 = re.sub(r'/\*[\s\S]*?\*/', '', ''.join(re.findall(r'<style[^>]*>([\s\S]*?)</style>', txt)))
    _css36 = re.sub(r'@font-face\{[^{}]*\}', '', _css36)
    for _lv36 in ('soft', 'strong'):
        if not re.search(r'\.fimg\[data-shadow="' + _lv36 + r'"\]>img\{[^}]*filter:(?:var\(--shd-' + _lv36 + r',\s*)?drop-shadow\(', _css36):
            errors.append('ไม่มี CSS เงา "{}" (.fimg[data-shadow="{}"]>img filter:drop-shadow) (ดู UI_STANDARD.md ข้อ 6)'.format(_lv36, _lv36))
    for _sel36, _body36 in re.findall(r'([^{}]+)\{([^{}]*)\}', _css36):
        for _one36 in _sel36.split(','):
            _one36 = _one36.strip()
            if re.search(r'\.fimg(\[[^\]]*\])?(\s*>\s*img|\s+img)?$', _one36) and 'box-shadow' in _body36 and 'body.imgmode' not in _one36:  # ตัวรูป/กรอบรูป (ไม่รวมปุ่มจับ .rz/.delbtn)
                errors.append("'{}' ใช้ box-shadow — รูปโปร่งใสจะเห็นกรอบสี่เหลี่ยม ใช้ data-shadow แทน (ดู UI_STANDARD.md ข้อ 6)".format(_one36))
            if re.search(r'\.fimg\s*>\s*img$|\.fimg\s+img$', _one36) and re.search(r'(?<![-\w])filter\s*:', _body36):
                errors.append("'{}' ใส่ filter ทุกรูป — ปุ่มเงา \"ไม่มี\" จะไม่มีผลจริง (ดู UI_STANDARD.md ข้อ 6)".format(_one36))
    for _lv36 in ('none', 'soft', 'strong'):
        if len(re.findall(r'id="btnShd_' + _lv36 + r'" onclick="imgShadow\(\'' + _lv36 + r'\'\)"', txt)) != 1:
            errors.append('ปุ่มเงา "{}" ต้องมี 1 ปุ่ม ผูก onclick imgShadow(\'{}\') (ดู UI_STANDARD.md ข้อ 6)'.format(_lv36, _lv36))
    _ta36 = re.search(r'\nfunction imgToAllPages\(\)\{[\s\S]*?\n\}', txt)
    if not _ta36 or 'data-shadow' not in _ta36.group(0):
        errors.append('ใส่ทุกหน้า (imgToAllPages) ไม่คัดลอกเงา data-shadow (ดู UI_STANDARD.md ข้อ 6)')
    _rd36 = re.search(r'\nfunction _imgReadout\(el\)\{[\s\S]*?\n\}', txt)
    if not _rd36 or '_imgShdSync()' not in _rd36.group(0):
        errors.append('_imgReadout ไม่เรียก _imgShdSync — ปุ่มเงาไม่จาง/ไม่แสดงระดับของรูปที่เลือก (ดู UI_STANDARD.md ข้อ 5)')
    _rp36 = re.search(r'\nfunction _restorePages\(html\)\{[\s\S]*?\n\}', txt)
    if not _rp36 or 'document.contains(_imgSel)' not in _rp36.group(0):
        errors.append('_restorePages ไม่ยกเลิกรูปที่เลือกที่หลุดจากหน้า — หลัง Undo ปุ่มรูปจะแก้รูปที่มองไม่เห็น (ดู UI_STANDARD.md ข้อ 5)')

    # ---- 36b) ปรับค่าเงาอ่อน/ชัดทั้งเมนู (ผู้ใช้ 9 ต.ค. 2026 · แบบ ก) ----
    #   ค่าเก็บเป็น --shd-soft/--shd-strong บน style ของ .page · ค่าสำรองใน CSS ต้องเท่า _SHD_DEF ใน JS (2 ที่ต้องตรงกัน)
    #   ทุกจุดที่หน้าเปลี่ยน/ภาษาเปลี่ยน/ออกจากโหมด/บันทึก ต้องดูแลหน้าต่างปรับค่า · ปรับค่า/ค่าเริ่มต้น ต้องมีจุด Undo
    if 'id="shdPop"' in txt:
        _def36 = re.search(r'var _SHD_DEF=\{soft:\{y:([\d.]+),b:([\d.]+),a:(\d+)\},strong:\{y:([\d.]+),b:([\d.]+),a:(\d+)\}\};', txt)
        if not _def36:
            errors.append('ไม่พบ _SHD_DEF — ค่าเริ่มต้นเงาต้องประกาศที่เดียว (ดู UI_STANDARD.md ข้อ 6)')
        else:
            for _lv36, (_y, _b, _a) in (('soft', _def36.group(1, 2, 3)), ('strong', _def36.group(4, 5, 6))):
                _fb36 = re.search(r'\.fimg\[data-shadow="' + _lv36 + r'"\]>img\{filter:var\(--shd-' + _lv36 + r',drop-shadow\(0 ([\d.]+)mm ([\d.]+)mm rgba\(60,40,20,(0?\.\d+)\)\)\);\}', _css36)
                if not _fb36:
                    errors.append('CSS เงา "{}" ไม่ได้ใช้ var(--shd-{},drop-shadow(...)) — ปรับค่าแล้วรูปจะไม่เปลี่ยน (ดู UI_STANDARD.md ข้อ 6)'.format(_lv36, _lv36))
                elif (float(_fb36.group(1)), float(_fb36.group(2)), round(float(_fb36.group(3)) * 100)) != (float(_y), float(_b), int(_a)):
                    errors.append('ค่าสำรองใน CSS เงา "{}" ไม่ตรงกับ _SHD_DEF — ปุ่ม "ค่าเริ่มต้น" จะไม่ตรงกับที่เห็น (ดู UI_STANDARD.md ข้อ 6)'.format(_lv36))
        for _fn36, _need36, _why36 in (
                ('_restorePages', '_shdPopRender', 'หลัง Undo ค่าในหน้าต่างปรับเงาไม่ตรงกับหน้า'),
                ('toggleImgMode', '_shdPopClose', 'ออกจากโหมดแก้รูปแล้วหน้าต่างปรับเงาค้าง'),
                ('applyLang', '_shdPopRender', 'กด TH/EN แล้วข้อความในหน้าต่างปรับเงาไม่เปลี่ยน'),
                ('buildEditorHtml', '#shdPop', 'บันทึกแล้วหน้าต่างปรับเงาค้างเปิดในไฟล์'),
                ('_shdCommit', '_snapNow()', 'ปรับค่าเงาไม่มีจุด Undo'),
                ('_shdReset', '_snapNow()', 'ค่าเริ่มต้นเงาไม่มีจุด Undo')):
            _f36 = re.search(r'\nfunction ' + _fn36 + r'\([^)]*\)\{[\s\S]*?\n\}', txt)
            if not _f36 or _need36 not in _f36.group(0):
                errors.append('{} ไม่มี {} — {} (ดู UI_STANDARD.md ข้อ 6)'.format(_fn36, _need36, _why36))
        if not re.search(r"r\.addEventListener\('change',function\(\)\{ _shdCommit\(", txt):
            errors.append('slider เงาไม่จดตอนปล่อย (change → _shdCommit) (ดู UI_STANDARD.md ข้อ 6)')

    # ---- 36c) ใช้เงากับทุกรูป (ผู้ใช้ 9 ต.ค. 2026) — ขอบเขตแบบ ใช้ทั้งประเภท (UI_STANDARD ข้อ 4) ----
    if 'id="btnShdAll"' in txt:
        if len(re.findall(r'id="btnShdAll" onclick="imgShadowAllOpen\(\)"', txt)) != 1:
            errors.append('ปุ่ม "ใช้กับทุกรูป" ต้องมี 1 ปุ่ม ผูก onclick imgShadowAllOpen() (ดู UI_STANDARD.md ข้อ 6)')
        _sa36 = re.search(r'\nfunction imgShadowAllOpen\(\)\{[\s\S]*?\n\}', txt)
        _sa36 = _sa36.group(0) if _sa36 else ''
        for _need36, _why36 in (("activeBtn:'btnShdAll'", 'ปุ่มไม่เป็น .on ระหว่าง panel เปิด (UI_STANDARD ข้อ 2)'),
                                ('_snapNow()', 'ใช้เงากับทุกรูปไม่มีจุด Undo'),
                                ('validate:', 'ยังไม่เลือกขอบเขตแล้วกด Enter ได้ (UI_STANDARD ข้อ 4)'),
                                ('ok.disabled=', 'ปุ่มนำไปใช้ไม่จางตอนยังไม่เลือกขอบเขต / ไม่มีอะไรเปลี่ยน (UI_STANDARD ข้อ 4)')):
            if _need36 not in _sa36:
                errors.append('imgShadowAllOpen ไม่มี {} — {} (ดู UI_STANDARD.md ข้อ 4)'.format(_need36, _why36))
        if re.search(r'<input\b[^>]*name="shScope"[^>]*\bchecked\b', txt):  # เฉพาะในแท็ก <input> (ไม่ใช่ ':checked' ใน querySelector)
            errors.append('ขอบเขตของ ใช้กับทุกรูป ถูกเลือกไว้ล่วงหน้า — ผู้ใช้ต้องเลือกเอง (ดู UI_STANDARD.md ข้อ 4)')
        for _fn36, _why36 in (('_imgShdSync', 'ปุ่มไม่จางเมื่อไม่ได้เลือกรูป'),
                              ('_restorePages', 'หลัง Undo panel ยังเปิดอยู่กับรูปที่ถูกแทนแล้ว'),
                              ('toggleImgMode', 'ออกจากแก้รูปแล้ว panel ยังเปิดอยู่')):
            _f36 = re.search(r'\nfunction ' + _fn36 + r'\([^)]*\)\{[\s\S]*?\n\}', txt)
            if not _f36 or 'btnShdAll' not in _f36.group(0):
                errors.append('{} ไม่ดูแลปุ่ม btnShdAll — {} (ดู UI_STANDARD.md ข้อ 5)'.format(_fn36, _why36))

    # ---- 37) โหมดแก้: หน้าเมนูยาวเกิน A4 ได้ + ลายเฉียงบอกขอบเขต (ผู้ใช้ 9 ต.ค. 2026 · แบบ ก · เอาเส้นประ/ป้ายออก 11 ต.ค. 2026) ----
    #   ดู UI_STANDARD.md ข้อ 7 · ขนาดพิมพ์คงเดิม · ส่วนขยายอยู่ใน @media screen + :not(.measuring) ทุกโหมดแก้ · ขอบเขต A4 บอกด้วยลายเฉียง (ไม่มีเส้นประ/ป้ายแล้ว — บังการแก้) · ห้ามเหลือ ::after ขอบ / --a4lbl / pg.a4end
    _pg37 = re.search(r'\n\.page\{([^}]*)\}', txt)
    if not _pg37 or not re.search(r'(?<![-\w])height:297mm', _pg37.group(1)) or 'overflow:hidden' not in _pg37.group(1):
        errors.append('.page ต้องสูง 297mm + overflow:hidden (ขนาดพิมพ์ A4) — ส่วนขยายตอนแก้ใส่ได้เฉพาะในโหมดแก้ (ดู UI_STANDARD.md ข้อ 7)')
    for _md37 in ('editmode', 'headermode', 'pricemode', 'imgmode'):
        _sel37 = 'body.' + _md37 + ':not(.measuring) .page'
        _i37 = txt.find(_sel37 + ',') if txt.find(_sel37 + ',') >= 0 else txt.find(_sel37 + '{')
        if _i37 < 0:
            errors.append('โหมด {} ไม่มีส่วนขยายหน้า ({}) — ปุ่มแก้ไขดันเนื้อหาเกิน A4 แล้วถูกตัด (ดู UI_STANDARD.md ข้อ 7)'.format(_md37, _sel37)); continue
        _m37 = txt.rfind('@media', 0, _i37)
        _seg37 = txt[_m37:_i37] if _m37 >= 0 else ''
        if not _seg37.startswith('@media screen') or _seg37.count('{') - _seg37.count('}') != 1:
            errors.append('ส่วนขยายหน้าของโหมด {} ไม่อยู่ใน @media screen — Ctrl+P ระหว่างแก้จะพิมพ์เกิน A4 (ดู UI_STANDARD.md ข้อ 7)'.format(_md37))
    _ru37 = re.search(r'body\.editmode:not\(\.measuring\) \.page,[^{]*\{([^}]*)\}', txt)
    if not _ru37 or not ('height:auto' in _ru37.group(1) and 'overflow:visible' in _ru37.group(1)):
        errors.append('ส่วนขยายหน้าต้องเป็น height:auto + overflow:visible (ดู UI_STANDARD.md ข้อ 7)')
    elif 'repeating-linear-gradient' not in _ru37.group(1):
        errors.append('ส่วนขยายหน้าต้องมีลายเฉียง (repeating-linear-gradient) บอกขอบเขตใต้ A4 — เป็นตัวบอกขอบเดียวหลังเอาเส้นประออก (ดู UI_STANDARD.md ข้อ 7)')
    if '.page::after' in txt:
        errors.append('ยังมี .page::after (เส้นประ/ป้ายขอบ A4) — เอาออกแล้ว 11 ต.ค. 2026 (บังการแก้) ต้องลบ (ไม่ทิ้งขยะ)')
    if '--a4lbl' in txt or 'pg.a4end' in txt:
        errors.append('ยังมีโค้ด --a4lbl / pg.a4end ค้าง — ป้ายขอบ A4 เอาออกแล้ว ต้องลบให้หมด (ไม่ทิ้งขยะ)')

    # ---- 38) ขนาดตัวอักษรทีละ 0.5 (ผู้ใช้ 9 ต.ค. 2026 · แบบ ก) ----
    #   ดู UI_STANDARD.md ข้อ 6 · ทุกที่ที่อ่าน/ตั้งขนาดต้องใช้ความละเอียดเดียวกัน (0.5) ไม่งั้นช่องแสดงค่าไม่ตรงกับที่ใช้จริง
    _sc38 = re.search(r'\nfunction _sizeClean\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _sc38 or "(c==='.'&&!dot)" not in _sc38.group(0):  # เงื่อนไขรับจุด 1 จุด (ไม่ใช่แค่มีคำว่า c==='.')
        errors.append('_sizeClean ไม่รับจุดทศนิยม — พิมพ์ 16.5 ไม่ได้ (ดู UI_STANDARD.md ข้อ 6)')
    _sp38 = re.search(r'\nfunction _sizeParse\([^)]*\)\{[^\n]*\}', txt)
    if not _sp38 or "bad:'step'" not in _sp38.group(0) or "bad:'range'" not in _sp38.group(0):
        errors.append('ไม่พบ _sizeParse ที่ตรวจช่วง + ทีละ 0.5 (ดู UI_STANDARD.md ข้อ 6)')
    _st38 = re.search(r'\nfunction typoSizeStep\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _st38 or '_typoCurSize(' not in _st38.group(0) or re.search(r'Math\.round\(parseFloat\(inp\.value\)', _st38.group(0)):
        errors.append('typoSizeStep ต้องอ่านขนาดจริงด้วย _typoCurSize — ปัดเป็นจำนวนเต็มแล้ว 12.5 กด + ได้ 14 (ดู UI_STANDARD.md ข้อ 6)')
    if re.search(r'Math\.round\(\s*parseFloat\([^)]*fontSize', txt) or re.search(r'parseInt\(\s*raw\s*,\s*10\s*\)', txt):
        errors.append('มีที่อ่านขนาดตัวอักษรแบบปัดเป็นจำนวนเต็ม (Math.round(parseFloat(..fontSize)) / parseInt(raw,10)) — ใช้ _sizeHalf / _sizeParse (ดู UI_STANDARD.md ข้อ 6)')
    for _k38 in ('fl.sizeStep', 'fl.sizeOnly', 'ttl.sizeType'):
        _n38 = len(re.findall(r"'" + re.escape(_k38) + r"':'(?!\w+\.[\w.]+'\s*[),;])", txt))  # ข้อความแปลจริง (ไม่นับ 'k':'อีกkey' ใน ternary)
        if _n38 != 2:
            errors.append("ข้อความ {} ต้องมีทั้ง TH และ EN (พบ {} ที่) (ดู UI_STANDARD.md ข้อ 6)".format(_k38, _n38))
    #   ปุ่ม +/− ทีละ 0.5 (ผู้ใช้ 9 ต.ค. 2026 17:38 · แบบ ข แทนแบบ ก) — ปุ่มต้องไปถึงทุกค่าที่ช่องรับได้
    if not re.search(r'typoSizeStep\(0\.5\)', txt) or not re.search(r'typoSizeStep\(-0\.5\)', txt) or re.search(r'typoSizeStep\(-?1\)', txt):
        errors.append('ปุ่ม +/− ขนาดตัวอักษรต้องเรียก typoSizeStep(0.5) / typoSizeStep(-0.5) (ดู UI_STANDARD.md ข้อ 6)')
    if not _st38 or '_sizeHalf(cur+d)' not in _st38.group(0):
        errors.append('typoSizeStep ต้องปัดผลด้วย _sizeHalf(cur+d) — ขนาดต้องลงที่ทีละ 0.5 เสมอ (ดู UI_STANDARD.md ข้อ 6)')
    if not re.search(r"tk\(pz\.bad==='step'\?'fl\.sizeStep'", txt):
        errors.append("ช่องขนาดไม่เตือน fl.sizeStep เมื่อไม่ใช่ทีละ 0.5 (ดู UI_STANDARD.md ข้อ 6)")

    # ---- 39) ชื่อไฟล์รูป (.fimg data-fname) แสดงตอนแก้ (ผู้ใช้ 9 ต.ค. 2026) ----
    #   ดู UI_STANDARD.md ข้อ 6 · เพิ่มรูปต้องจำชื่อ · ใส่ทุกหน้าคัดลอก · แถบล่าง + ป้ายใต้รูปแสดง · ไฟล์เมนูที่ดาวน์โหลดไม่มีชื่อ
    _ia39 = re.search(r'\nfunction imgAdd\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _ia39 or "setAttribute('data-fname'" not in _ia39.group(0):
        errors.append('imgAdd ไม่จำชื่อไฟล์ (data-fname) — รูปที่เพิ่มใหม่จะไม่มีชื่อ (ดู UI_STANDARD.md ข้อ 6)')
    _ta39 = re.search(r'\nfunction imgToAllPages\(\)\{[\s\S]*?\n\}', txt)
    if not _ta39 or 'data-fname' not in _ta39.group(0):
        errors.append('ใส่ทุกหน้า (imgToAllPages) ไม่คัดลอกชื่อไฟล์ data-fname (ดู UI_STANDARD.md ข้อ 6)')
    _rd39 = re.search(r'\nfunction _imgReadout\(el\)\{[\s\S]*?\n\}', txt)
    if not _rd39 or "tkj([nm].concat(fnm?" not in _rd39.group(0) or "tg.textContent=(fnm?" not in _rd39.group(0):  # แถบล่าง + ป้ายใต้รูป แยกกันตรวจ
        errors.append('_imgReadout ไม่แสดงชื่อไฟล์ในแถบล่าง + ป้ายใต้รูป (ดู UI_STANDARD.md ข้อ 6)')
    _bm39 = re.search(r'\nfunction buildMenuHtml\(\)\{[\s\S]*?\n\}', txt)
    if not _bm39 or "removeAttribute('data-fname')" not in _bm39.group(0):
        errors.append('buildMenuHtml ไม่ลบชื่อไฟล์รูป — ติดไปในไฟล์เมนูที่ดาวน์โหลด (ดู UI_STANDARD.md ข้อ 6)')
    if re.search(r'innerHTML\s*=[^;\n]*_imgFname\(|innerHTML\s*=[^;\n]*\bfnm\b', txt):
        errors.append('ชื่อไฟล์รูปใส่ผ่าน innerHTML — ต้องใช้ textContent (ชื่อไฟล์มี & ได้) (ดู UI_STANDARD.md ข้อ 6)')
    #   39b) คัดลอกชื่อ + ชื่อยาว (ผู้ใช้ 9 ต.ค. 2026)
    if len(re.findall(r'id="btnImgCopyName" onclick="imgCopyName\(\)"', txt)) != 1:
        errors.append('ปุ่ม "คัดลอกชื่อ" ต้องมี 1 ปุ่ม ผูก onclick imgCopyName() (ดู UI_STANDARD.md ข้อ 6)')
    if not _rd39 or '_imgCopySync(el)' not in _rd39.group(0):
        errors.append('_imgReadout ไม่เรียก _imgCopySync — ปุ่มคัดลอกชื่อไม่จางเมื่อไม่ได้เลือกรูป (ดู UI_STANDARD.md ข้อ 5)')
    _cp39 = re.search(r'\nfunction imgCopyName\(\)\{[\s\S]*?\n\}', txt)
    _ct39 = re.search(r'\nfunction _copyText\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _cp39 or "'fl.imgCopyFail'" not in _cp39.group(0) or not _ct39 or '_copyFallback(' not in _ct39.group(0):
        errors.append('คัดลอกชื่อต้องมีทางสำรอง (_copyFallback) และแจ้ง fl.imgCopyFail เมื่อคัดลอกไม่ได้ — ห้ามขึ้นว่าสำเร็จทั้งที่ไม่ได้คัดลอก (ดู UI_STANDARD.md ข้อ 6)')
    if not _rd39 or 'tg.textContent=(fnm?_cutMid(' not in _rd39.group(0):
        errors.append('ป้ายใต้รูปต้องตัดชื่อด้วย _cutMid (เก็บนามสกุล) (ดู UI_STANDARD.md ข้อ 6)')
    if not re.search(r'#edstatus \.edstatus-msg\{[^}]*overflow-wrap:anywhere', txt):
        errors.append('แถบล่าง .edstatus-msg ไม่ตัดคำยาว — ชื่อไฟล์ยาวไม่มีเว้นวรรคล้นจอ (ดู UI_STANDARD.md ข้อ 7)')
    for _fn39 in ('_serializePages', 'buildEditorHtml', 'buildMenuHtml'):
        _f39 = re.search(r'\nfunction ' + _fn39 + r'\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _f39 or ".fimg[title]" not in _f39.group(0):
            errors.append('{} ไม่ลบ tooltip ชื่อไฟล์ (.fimg[title]) — หลุดลง snapshot / ไฟล์ (ดู UI_STANDARD.md ข้อ 6)'.format(_fn39))
    #   39c) ป้ายใต้รูป 2 แถว + ไม่ถูกปุ่มย่อขยายทับ (ผู้ใช้ 9 ต.ค. 2026 19:33)
    _tg39 = re.search(r'\.fimg \.sizetag\{([^}]*)\}', _css)
    _rz39 = re.search(r'\.fimg \.rz\{([^}]*)\}', _css)
    _mt39 = re.search(r'margin-top:(\d+)px', _tg39.group(1)) if _tg39 else None
    _bt39 = re.search(r'bottom:-(\d+)px', _rz39.group(1)) if _rz39 else None
    if not (_mt39 and _bt39) or int(_mt39.group(1)) <= int(_bt39.group(1)):
        errors.append('ป้ายใต้รูป (.sizetag margin-top) ต้องต่ำกว่าปุ่มย่อขยาย (.rz bottom) — ไม่งั้นปุ่มทับตัวเลขขนาด (ดู UI_STANDARD.md ข้อ 6)')
    if not _tg39 or 'white-space:pre' not in _tg39.group(1) or not _rd39 or "_cutMid(fnm,30)+'\\n'" not in _rd39.group(0):
        errors.append("ป้ายใต้รูปต้องเป็น 2 แถว (ชื่อ\\nขนาด + white-space:pre) (ดู UI_STANDARD.md ข้อ 6)")
    _pg39 = re.sub(r'<script[\s\S]*?</script>', '', txt)
    for _m39 in re.finditer(r'<div class="fimg"(?![^>]*data-fname=)[^>]*>', _pg39):
        warnings.append('รูปในหน้าเมนูไม่มีชื่อไฟล์ (data-fname): {}'.format(_m39.group(0)[:90]))

    # ---- 40) งานค้าง 6 ข้อ (ตรวจ 10 ต.ค. 2026 00:25 · แก้ 01:22) — ปุ่มต้องทำตามที่บอก และบอกผล ----
    #   ดู UI_STANDARD.md ข้อ 5–6
    _ac40 = re.search(r'\n\s*function applyColorRange\([^)]*\)\{[\s\S]*?\n  \}', txt)
    if not _ac40 or not re.search(r"_typoType\.line\)\{[\s\S]{0,600}borderBottomColor=C[\s\S]{0,200}'fl\.lineColor'", _ac40.group(0)):
        errors.append('applyColorRange ไม่ทาสีเส้นจุด (borderBottomColor + fl.lineColor) — กดสีแล้วไม่มีอะไรเกิดขึ้น (ดู UI_STANDARD.md ข้อ 6)')
    if re.search(r"'typoCpApply'\][^\n]*disabled=isLine", txt):
        errors.append('ปุ่มสี (typoCpApply) จางเมื่อเลือกเส้นจุด — เส้นจุดต้องเปลี่ยนสีได้ (ดู UI_STANDARD.md ข้อ 5)')
    _cd40 = re.search(r'\n\s*function _cpDlgOk\(\)\{[\s\S]*?\n  \}', txt)
    if _cd40 and '_typoEl && !line)?applyColorRange' in _cd40.group(0):
        errors.append('หน้าต่าง + กำหนดเอง ข้ามเส้นจุด — ต้องทาสีเส้นจุดด้วย (ดู UI_STANDARD.md ข้อ 6)')
    _la40 = re.search(r'\nfunction typoLineApply\(\)\{[\s\S]*?\n\}', txt)
    if not _la40 or "'fl.lineStyle'" not in _la40.group(0) or "'fl.lineStyleSame'" not in _la40.group(0):
        errors.append('typoLineApply ไม่แจ้งผล (fl.lineStyle / fl.lineStyleSame) (ดู UI_STANDARD.md ข้อ 6)')
    if re.search(r'function typoColorApply\(|function typoColorLive\(', txt):
        errors.append('typoColorApply / typoColorLive เป็น code ที่ไม่มีใครเรียก — ลบออก (ไม่ทิ้งขยะ)')
    _rp40 = re.search(r'\nfunction _restorePages\(html\)\{[\s\S]*?\n\}', txt)
    if not _rp40 or 'document.contains(_typoEl)' not in _rp40.group(0) or 'typoClear()' not in _rp40.group(0) or 'lastEditable.isConnected' not in _rp40.group(0):
        errors.append('_restorePages ไม่ยกเลิกช่อง/ไฮไลท์ที่หลุดจากหน้า — หลัง Ctrl+Z แถบรูปแบบแก้ช่องที่มองไม่เห็นแล้วบอกว่าสำเร็จ (ดู UI_STANDARD.md ข้อ 5)')
    if re.search(r"getElementById\('typoFont'\)\.addEventListener\('change'", txt) and 'id="typoFont" onchange=' in txt:
        errors.append('ช่องฟอนต์ผูก 2 ทาง (onchange + addEventListener) — เลือกครั้งเดียวทำ 2 รอบ (ดู UI_STANDARD.md ข้อ 6)')
    _fa40 = re.search(r'\nfunction typoFontApply\(\)\{[\s\S]*?\n\}', txt)
    if not _fa40 or not all(k in _fa40.group(0) for k in ("'fl.fontRange'", "'fl.fontCell'", "'fl.fontSame'")):
        errors.append('typoFontApply ต้องแจ้งผล fl.fontRange / fl.fontCell / fl.fontSame (ดู UI_STANDARD.md ข้อ 6)')
    if not _rd39 or "if(!el){ if(document.body.classList.contains('imgmode')) setStatus(" not in _rd39.group(0):
        errors.append('_imgReadout(null) ตั้งข้อความ "คลิกรูป…" นอกโหมดแก้รูป — ออกจากแก้รูปแล้วแถบล่างค้าง (ดู UI_STANDARD.md ข้อ 6)')
    for _id40, _k40 in (('typoBold', 'sty.bold'), ('typoItalic', 'sty.italic'), ('typoUnderline', 'sty.underline'), ('typoStrike', 'sty.strike')):
        if not re.search(r"getElementById\('" + _id40 + r"'\)\.addEventListener\('click', function\(\)\{ _styleExec\('\w+','" + re.escape(_k40) + r"'\); \}\);", txt):
            errors.append('ปุ่ม {} ต้องเรียก _styleExec (มีข้อความผล) (ดู UI_STANDARD.md ข้อ 6)'.format(_id40))
    _se40 = re.search(r'\n\s*function _styleExec\([^)]*\)\{[\s\S]*?\n  \}', txt)
    if not _se40 or "'fl.styleOn'" not in _se40.group(0) or 'needSel()' not in _se40.group(0):
        errors.append('_styleExec ต้องแจ้งผล fl.styleOn/fl.styleOff และบอกเมื่อไม่ได้ไฮไลท์ (ดู UI_STANDARD.md ข้อ 6)')
    _db40 = re.search(r"d\.onclick=function\(ev\)\{[^\n]*\};", txt)
    if not _db40 or "'fl.imgDel'" not in _db40.group(0) or '_imgHideSync()' not in _db40.group(0):
        errors.append('ปุ่มลบรูป (×) ต้องแจ้งผล fl.imgDel และนับปุ่มซ่อนรูปใหม่ (_imgHideSync) (ดู UI_STANDARD.md ข้อ 6)')
    for _k40 in ('fl.lineColor', 'fl.lineColorSame', 'fl.lineStyle', 'fl.lineStyleSame', 'fl.fontCell', 'fl.fontSame', 'fl.styleOn', 'fl.styleOff', 'sty.bold', 'sty.italic', 'sty.underline', 'sty.strike', 'fl.imgDel'):
        _n40 = len(re.findall(r"'" + re.escape(_k40) + r"':'(?!\w+\.[\w.]+'\s*[),;])", txt))
        if _n40 != 2:
            errors.append('ข้อความ {} ต้องมีทั้ง TH และ EN (พบ {} ที่) (ดู UI_STANDARD.md ข้อ 6)'.format(_k40, _n40))

    # ---- 41) เส้นจุด (.ln) ต้องโชว์ว่าคลิกแก้ได้ในโหมดแก้ (ผู้ใช้ 10 ต.ค. 2026 · แบบ ก) ----
    #   ดู UI_STANDARD.md ข้อ 5 · element ที่แก้ได้ต้องมี affordance เหมือน .nm/.pr · @media screen เท่านั้น (ไม่พิมพ์)
    _af41 = re.search(r'body\.editmode \.ln\{([^}]*)\}', _css)
    if not _af41:
        errors.append('เส้นจุด (.ln) ไม่มี affordance ในโหมดแก้ (body.editmode .ln) — ผู้ใช้ไม่รู้ว่าคลิกแก้ได้ (ดู UI_STANDARD.md ข้อ 5)')
    else:
        _b41 = _af41.group(1)
        if 'outline' not in _b41 or 'background' not in _b41:
            errors.append('affordance เส้นจุด (.ln) ต้องมี outline + background เหมือน .nm/.pr (ดู UI_STANDARD.md ข้อ 5)')
        _mi41 = re.search(r'body\.editmode \.ln\{[^}]*\}', txt)
        _wrap41 = txt.rfind('@media', 0, _mi41.start()) if _mi41 else -1
        _seg41 = txt[_wrap41:_mi41.start()] if _wrap41 >= 0 else ''
        if not _seg41.startswith('@media screen') or _seg41.count('{') - _seg41.count('}') != 1:
            errors.append('affordance เส้นจุด (.ln) ต้องอยู่ใน @media screen — ไม่งั้นกรอบติดตอนพิมพ์ (ดู UI_STANDARD.md ข้อ 7)')

    # ---- 42) ปุ่มคัดลอกตำแหน่งรูป (ผู้ใช้ 10 ต.ค. 2026) ----
    #   ดู UI_STANDARD.md ข้อ 5–6 · ตำแหน่ง mm คำนวณที่เดียว (_imgPos) ใช้ทั้งแถบล่างและคัดลอก · มีทางสำรอง · ไม่ขึ้นว่าสำเร็จถ้าคัดลอกไม่ได้
    if 'id="btnImgCopyPos"' in txt:
        if len(re.findall(r'id="btnImgCopyPos" onclick="imgCopyPos\(\)"', txt)) != 1:
            errors.append('ปุ่ม "คัดลอกตำแหน่ง" ต้องมี 1 ปุ่ม ผูก onclick imgCopyPos() (ดู UI_STANDARD.md ข้อ 6)')
        _ip42 = re.search(r'\nfunction _imgPos\(el\)\{[\s\S]*?\n\}', txt)
        if not _ip42 or 'getBoundingClientRect' not in _ip42.group(0):
            errors.append('ไม่พบ _imgPos (คำนวณตำแหน่ง mm จาก getBoundingClientRect) (ดู UI_STANDARD.md ข้อ 6)')
        _rd42 = re.search(r'\nfunction _imgReadout\(el\)\{[\s\S]*?\n\}', txt)
        if not _rd42 or '_imgPos(el)' not in _rd42.group(0):
            errors.append('_imgReadout ต้องใช้ _imgPos(el) — ค่าตำแหน่งในแถบล่างกับที่คัดลอกต้องมาจากที่เดียวกัน (ดู UI_STANDARD.md ข้อ 6)')
        if not _rd42 or '_imgCopyPosSync(el)' not in _rd42.group(0):
            errors.append('_imgReadout ไม่เรียก _imgCopyPosSync — ปุ่มคัดลอกตำแหน่งไม่จางเมื่อไม่ได้เลือกรูป (ดู UI_STANDARD.md ข้อ 5)')
        _cp42 = re.search(r'\nfunction imgCopyPos\(\)\{[\s\S]*?\n\}', txt)
        if not _cp42 or "'fl.imgPosCopyFail'" not in _cp42.group(0) or '_copyText(' not in _cp42.group(0):
            errors.append('imgCopyPos ต้องใช้ _copyText + แจ้ง fl.imgPosCopyFail เมื่อคัดลอกไม่ได้ (ห้ามขึ้นว่าสำเร็จ) (ดู UI_STANDARD.md ข้อ 6)')
        _be42 = re.search(r'\nfunction buildEditorHtml\(\)\{[\s\S]*?\n\}', txt)
        if not _be42 or 'btnImgCopyPos' not in _be42.group(0):
            errors.append('buildEditorHtml ไม่ล้างสถานะปุ่มคัดลอกตำแหน่ง (btnImgCopyPos) (ดู UI_STANDARD.md ข้อ 6)')
        for _k42 in ('btn.imgCopyPos', 'ttl.imgCopyPos', 'ttl.imgCopyPosNeed', 'fl.imgPosCopied', 'fl.imgPosCopyFail'):
            _n42 = len(re.findall(r"'" + re.escape(_k42) + r"':'(?!\w+\.[\w.]+'\s*[),;])", txt))
            if _n42 != 2:
                errors.append('ข้อความ {} ต้องมีทั้ง TH และ EN (พบ {} ที่) (ดู UI_STANDARD.md ข้อ 6)'.format(_k42, _n42))

    # ---- 43) press state ปุ่มกดครั้งเดียว (ผู้ใช้ 10 ต.ค. 2026 · แบบ ก) ----
    #   ดู UI_STANDARD.md ข้อ 1 · :active เท่านั้น (กลับเองเมื่อปล่อย) · ห้ามเขียว (เขียว = โหมดเปิด) · ปุ่มพื้นเทาต้องกัน .on
    _pa43 = re.findall(r'([^{}\n]*:active[^{}\n]*)\{([^}\n]*)\}', _css)
    _pa43 = [(sel, body) for sel, body in _pa43 if 'dh' not in sel]  # .dh:active = grab cursor (ไม่เกี่ยว)
    if not _pa43:
        errors.append('ไม่มี press state (:active) ของปุ่ม — ปุ่มกดครั้งเดียวไม่แสดงจังหวะกด (ดู UI_STANDARD.md ข้อ 1)')
    else:
        if not any('transform' in _b for _s, _b in _pa43):
            errors.append('press state ปุ่มควรยุบด้วย transform (:active) (ดู UI_STANDARD.md ข้อ 1)')
        for _s43, _b43 in _pa43:
            for _grn in ('#217346', '#1a5c38', '#1a5c38'):
                if _grn in _b43:
                    errors.append("press state '{}' ใช้สีเขียว {} — เขียวสงวนไว้สำหรับโหมดที่เปิดอยู่ (ดู UI_STANDARD.md ข้อ 1)".format(_s43.strip()[:60], _grn))
            # ปุ่มพื้นเทาตอนกด ต้องกัน .on (ไม่ทับพื้นเขียวของ toggle)
            if 'background' in _b43 and re.search(r'#e1dfdd|#dce9e0', _b43) and ('.on' not in _s43) and ('.szbtn' not in _s43) and ('.qab' not in _s43):
                errors.append("press state '{}' ตั้ง background แต่ไม่ได้กัน .on — อาจทับพื้นเขียวของปุ่ม toggle (ดู UI_STANDARD.md ข้อ 1)".format(_s43.strip()[:60]))

    # ---- 44) ข้อความบอกเส้นจุดที่เลือก "เปลี่ยนสีและแบบเส้นได้เท่านั้น" ที่แถบล่าง — อ่านจากตารางภาษา ln.hint (ผู้ใช้ 10 ต.ค. 2026) ----
    #   ดู UI_STANDARD.md ข้อ 5-6 · ย้ายจากในช่อง → แถบล่าง (17:30) แล้ว migration เข้าตารางภาษา key ln.hint · _lnSelMsg อ่าน t('ln.hint') · typoSelect ใช้ตอนเลือกเส้นจุด · applyLang สร้างใหม่ตอนสลับภาษา · ห้ามเหลือ ::after/--lnhint (ของเก่าแบบในช่อง)
    if '_lnSelMsg' in txt:
        _lm44 = re.search(r'\nfunction _lnSelMsg\([^)]*\)\{[^\n]*\}', txt)
        if not _lm44 or "t(\'ln.hint\')" not in _lm44.group(0):
            errors.append("_lnSelMsg ต้องอ่านข้อความจากตารางภาษา t(\'ln.hint\') ไม่ใช่ inline (ดู UI_STANDARD.md ข้อ 6)")
        _hints44 = re.findall(r"'ln\.hint':'([^']*)'", txt)
        if len(_hints44) < 2:
            errors.append('ตารางภาษาต้องมี key ln.hint ทั้ง TH และ EN (ดู UI_STANDARD.md ข้อ 6)')
        elif not any('เปลี่ยนสีและแบบเส้น' in h for h in _hints44) or not any('line style' in h for h in _hints44):
            errors.append('ln.hint ต้องมีทั้งข้อความไทย (เปลี่ยนสีและแบบเส้น) และอังกฤษ (line style) (ดู UI_STANDARD.md ข้อ 6)')
        _ts44 = re.search(r'\nfunction typoSelect\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _ts44 or 'isLine?_lnSelMsg(type)' not in _ts44.group(0):
            errors.append('typoSelect ไม่แสดงข้อความเส้นจุดที่แถบล่าง (isLine?_lnSelMsg(type)) (ดู UI_STANDARD.md ข้อ 6)')
        _al44 = re.search(r'\nfunction applyLang\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _al44 or '_lnSelMsg(_typoType)' not in _al44.group(0):
            errors.append('applyLang ไม่สร้างข้อความเส้นจุดใหม่ตอนสลับภาษา (_lnSelMsg(_typoType)) (ดู UI_STANDARD.md ข้อ 6)')
        if 'body.editmode .ln.typosel::after' in txt:
            errors.append('ยังมี ::after ในช่อง (.ln.typosel::after) — ย้ายไปแถบล่างแล้ว ต้องลบออก (ไม่ทิ้งขยะ)')
        if "setProperty('--lnhint'" in txt or "removeProperty('--lnhint')" in txt:
            errors.append('ยังมีโค้ด --lnhint ค้าง — ย้ายเข้าตารางภาษาแล้ว ต้องลบออก (ไม่ทิ้งขยะ)')
    else:
        errors.append('ไม่พบ _lnSelMsg — ข้อความบอกเส้นจุดที่แถบล่างหาย (ดู UI_STANDARD.md ข้อ 5)')

    # ---- 45) โฟกัสช่องกรอกเมื่อ selector ครบ (ปรับราคา→.ep-amt · ใส่ราคา→.ep-price) (ผู้ใช้ 11 ต.ค. 2026) ----
    #   จับที่ตัวโค้ดจริง (var _selDone + if(_selDone){...}) ไม่ใช่คำในคอมเมนต์ · _selDone = v.scope + v.gidx/v.pidx ครบ · focus เฉพาะใน if(_selDone) (ไม่แย่ง dropdown) · ช่องตามโหมด isSet?.ep-price:.ep-amt · setTimeout + document.contains · ห้ามเหลือ _wasSet/_wasFill
    _pp45 = re.search(r'\nfunction _bulkPricePreview\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _pp45:
        errors.append('ไม่พบ _bulkPricePreview — โฟกัสช่องกรอกหาย (ดู UI_STANDARD.md ข้อ 5)')
    else:
        _b45 = _pp45.group(0)
        _def45 = re.search(r'var _selDone\s*=[^\n]*', _b45)
        _foc45 = re.search(r'if\(_selDone\)\{[^\n]*\}', _b45)
        _fl45 = _foc45.group(0).replace(' ', '') if _foc45 else ''
        if not _def45 or 'v.scope' not in _def45.group(0) or 'v.gidx' not in _def45.group(0) or 'v.pidx' not in _def45.group(0):
            errors.append('_bulkPricePreview ต้องมี var _selDone เช็ก selector ครบ (v.scope + v.gidx + v.pidx) ก่อนโฟกัส (ดู UI_STANDARD.md ข้อ 6)')
        elif not _foc45:
            errors.append('_bulkPricePreview ต้องโฟกัสภายใน if(_selDone){...} — focus เฉพาะตอน selector ครบ ไม่แย่ง dropdown (ดู UI_STANDARD.md ข้อ 6)')
        elif "isSet?'.ep-price':'.ep-amt'" not in _fl45:
            errors.append('โฟกัสต้องเลือกช่องตามโหมด: isSet?.ep-price:.ep-amt (ปรับราคา→.ep-amt · ใส่ราคา→.ep-price) (ดู UI_STANDARD.md ข้อ 6)')
        elif 'setTimeout' not in _fl45 or 'document.contains' not in _fl45 or '.focus()' not in _fl45:
            errors.append('โฟกัสต้องใช้ setTimeout + document.contains + .focus() ในประโยคเดียว (กัน focus element ที่ถูกลบ) (ดู UI_STANDARD.md ข้อ 6)')
        if 'p._wasSet' in _b45 or 'p._wasFill' in _b45:
            errors.append('ยังมีโค้ดเก่า p._wasSet/p._wasFill ค้าง — เปลี่ยนเป็นเช็ก selector ครบแล้ว ต้องลบออก (ไม่ทิ้งขยะ)')

    # ---- 46) โน้ต (ราคาตามไซส์) ต้องรอดจาก "ใช้ทั้งประเภท" / เปลี่ยนฟอนต์ (ผู้ใช้ 11 ต.ค. 2026) ----
    #   โน้ตต้องใช้ <i class="note"> (ไม่ใช่ <i> เปล่า — _typoClearInner รื้อแท็กเปล่าที่ไม่มี class) · .nm .note คุมสี/ขนาด/เอียง แต่ไม่มี font-family (ให้ font inherit ตามช่อง) · _typoClearInner ต้องคง guard d.className
    if '<i>(' in txt:
        errors.append('พบโน้ตแบบ <i>(...) ไม่มี class — ต้องใช้ <i class="note"> ไม่งั้น "ใช้ทั้งประเภท" รื้อทิ้ง (ดู UI_STANDARD.md ข้อ 6)')
    _note46 = re.search(r'\.nm\s+\.note\s*\{([^}]*)\}', _css)
    if not _note46:
        errors.append('ไม่พบกฎ .nm .note — โน้ต (ราคาตามไซส์) จะไม่มีสไตล์ (ดู UI_STANDARD.md ข้อ 6)')
    else:
        _nb46 = _note46.group(1).replace(' ', '')
        if 'font-style:italic' not in _nb46:
            errors.append('.nm .note ต้องมี font-style:italic (โน้ตต้องเอียง) (ดู UI_STANDARD.md ข้อ 6)')
        if 'font-family' in _nb46:
            errors.append('.nm .note ต้องไม่มี font-family — ให้ฟอนต์ inherit จากช่อง (เปลี่ยนฟอนต์แล้วโน้ตเปลี่ยนตาม style เดิม) (ดู UI_STANDARD.md ข้อ 6)')
    _tci46 = re.search(r'\nfunction _typoClearInner\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _tci46:
        errors.append('ไม่พบ _typoClearInner (ดู UI_STANDARD.md ข้อ 5)')
    elif 'd.className' not in _tci46.group(0):
        errors.append('_typoClearInner ต้องคง guard d.className (ข้าม element ที่มี class) ไม่งั้นโน้ต <i class="note"> ถูกรื้อตอนใช้ทั้งประเภท (ดู UI_STANDARD.md ข้อ 6)')

    # ---- 47) ปุ่ม "เพิ่มรูป" กดได้ตลอด + เข้าโหมดแก้รูปอัตโนมัติ (ผู้ใช้ 12 ต.ค. 2026) ----
    #   เพิ่มรูปเป็น action สร้างรูปใหม่ (ไม่ขึ้นกับรูปที่เลือก) จึงกดได้นอกโหมดแก้รูป เหมือน "ซ่อนรูป" · ปุ่ม = <button class="...imgalways"> · gate imgbar dim รายปุ่ม .rgb>*:not(.imgalways) ไม่ dim .rgb ทั้งกล่อง · imgAdd เข้า imgmode อัตโนมัติ · typobar ต้องไม่พังตาม
    _addbtn47 = re.search(r'<button[^>]*\bclass="[^"]*\bimgalways\b[^"]*"[^>]*>(?:(?!</button>)[\s\S])*?btn\.addImage', txt)
    if not _addbtn47:
        errors.append('ปุ่มเพิ่มรูป (btn.addImage) ต้องมี class imgalways เพื่อยกเว้นจาก gate (กดได้นอกโหมดแก้รูป) (ดู UI_STANDARD.md ข้อ 6)')
    if 'body:not(.imgmode) #imgbar .imgalways{pointer-events:auto;}' not in txt:
        errors.append('ต้องมี body:not(.imgmode) #imgbar .imgalways{pointer-events:auto} — ไม่งั้นปุ่มเพิ่มรูปกดไม่ได้นอกโหมดแก้รูป (ดู UI_STANDARD.md ข้อ 6)')
    if '#imgbar .rgb>*:not(.imgalways)' not in txt:
        errors.append('gate imgbar ต้อง dim รายปุ่ม (.rgb>*:not(.imgalways)) ไม่ใช่ dim .rgb ทั้งกล่อง — ไม่งั้นเพิ่มรูปจะจางทั้งที่กดได้ (หลอกผู้ใช้ · ดู UI_STANDARD.md ข้อ 6)')
    if 'body:not(.editmode) #typobar .rgroup{pointer-events:none;}' not in txt or 'body:not(.editmode) #typobar .rgroup>*{opacity:.45' not in txt:
        errors.append('gate #typobar (แก้ข้อความ) หาย/เปลี่ยน — ต้องคง pointer-events:none ที่ .rgroup + opacity ที่ .rgroup>* (ดู UI_STANDARD.md ข้อ 6)')
    _ia47 = re.search(r'\nfunction imgAdd\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _ia47:
        errors.append('ไม่พบ imgAdd (ดู UI_STANDARD.md ข้อ 5)')
    elif "classList.contains('imgmode')" not in _ia47.group(0) or 'toggleImgMode()' not in _ia47.group(0):
        errors.append('imgAdd ต้องเข้าโหมดแก้รูปอัตโนมัติ (ถ้ายังไม่ imgmode → toggleImgMode()) (ดู UI_STANDARD.md ข้อ 6)')

    # ---- 48) ปุ่ม "คืนขนาด" รูป — คืนเป็นขนาดฐาน data-w0/h0 (ผู้ใช้ 12 ต.ค. 2026) ----
    #   รูปทุก .fimg ต้องมี data-w0/data-h0 (ขนาดฐาน) · ปุ่ม btnImgReset + imgResetSize ใช้ dataset.w0/h0 + markDirty (undo กฎ #6) · _imgReadout wire _imgResetSync · imgAdd เก็บ baseline รูปใหม่
    if '_imgResetSync' in txt or 'btnImgReset' in txt or 'imgResetSize' in txt:
        _nobl48 = re.findall(r'<div class="fimg"(?![^>]*data-w0)[^>]*>', txt)
        if _nobl48:
            errors.append('มี .fimg {} ตัวไม่มี data-w0/h0 (ขนาดฐาน) — ปุ่มคืนขนาดจะใช้ไม่ได้ (ดู UI_STANDARD.md ข้อ 6)'.format(len(_nobl48)))
        if not re.search(r'id="btnImgReset"[^>]*>(?:(?!</button>)[\s\S])*?btn\.resetSize', txt):
            errors.append('ไม่พบปุ่มคืนขนาด (id=btnImgReset + btn.resetSize) (ดู UI_STANDARD.md ข้อ 6)')
        _irs48 = re.search(r'\nfunction imgResetSize\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _irs48:
            errors.append('ไม่พบ imgResetSize (ดู UI_STANDARD.md ข้อ 5)')
        else:
            _b48=_irs48.group(0)
            if 'dataset.w0' not in _b48 or 'dataset.h0' not in _b48:
                errors.append('imgResetSize ต้องคืนขนาดจาก dataset.w0/h0 (ขนาดฐาน) (ดู UI_STANDARD.md ข้อ 6)')
            if 'markDirty()' not in _b48:
                errors.append('imgResetSize ต้อง markDirty() = จุด undo เมื่อเปลี่ยนขนาดจริง (กฎ #6) (ดู UI_STANDARD.md ข้อ 6)')
        _rd48 = re.search(r'\nfunction _imgReadout\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _rd48 or '_imgResetSync(el)' not in _rd48.group(0):
            errors.append('_imgReadout ไม่ได้เรียก _imgResetSync(el) — ปุ่มคืนขนาดจะไม่ enable/disable ตามการเลือกรูป (ดู UI_STANDARD.md ข้อ 6)')
        _ia48 = re.search(r'\nfunction imgAdd\([^)]*\)\{[\s\S]*?\n\}', txt)
        if _ia48 and 'dataset.w0' not in _ia48.group(0):
            errors.append('imgAdd ไม่ได้เก็บ data-w0/h0 ให้รูปใหม่ — รูปที่เพิ่มจะคืนขนาดไม่ได้ (ดู UI_STANDARD.md ข้อ 6)')
        if txt.count("'btn.resetSize':'") < 2:
            errors.append('btn.resetSize ต้องมีทั้ง TH และ EN ในตารางภาษา (ดู UI_STANDARD.md ข้อ 6)')
    else:
        errors.append('ไม่พบระบบปุ่มคืนขนาดรูป (btnImgReset/imgResetSize/_imgResetSync) (ดู UI_STANDARD.md ข้อ 5)')

    # ---- 49) ปุ่ม "ขนาดจริง" (actual/original pixel size) + honest-dim ทั้ง 2 ปุ่ม (ผู้ใช้ 12 ต.ค. 2026) ----
    #   ปุ่มที่ 2 = คืนรูปเป็นขนาด pixel จริงของไฟล์ (ผู้ใช้เลือกเองว่าจะเอาขนาดไหน — เตรียมเครื่องมือ ไม่บังคับ) · btnImgActual + imgActualSize (naturalWidth/Height) + markDirty · _imgResetSync จางปุ่มเมื่อรูปอยู่ขนาดนั้นแล้ว (เทียบ style string) ทั้งคู่ (กฎ #6 ไม่หลอกตา)
    if '_imgResetSync' in txt or 'btnImgActual' in txt or 'imgActualSize' in txt:
        if not re.search(r'id="btnImgActual"[^>]*>(?:(?!</button>)[\s\S])*?btn\.actualSize', txt):
            errors.append('ไม่พบปุ่มขนาดจริง (id=btnImgActual + btn.actualSize) (ดู UI_STANDARD.md ข้อ 6)')
        _ias49 = re.search(r'\nfunction imgActualSize\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _ias49:
            errors.append('ไม่พบ imgActualSize (ดู UI_STANDARD.md ข้อ 5)')
        else:
            _b49=_ias49.group(0)
            if 'naturalWidth' not in _b49 or 'naturalHeight' not in _b49:
                errors.append('imgActualSize ต้องใช้ naturalWidth/naturalHeight (ขนาด pixel จริงของไฟล์) (ดู UI_STANDARD.md ข้อ 6)')
            if 'markDirty()' not in _b49:
                errors.append('imgActualSize ต้อง markDirty() = จุด undo (กฎ #6) (ดู UI_STANDARD.md ข้อ 6)')
        _rs49 = re.search(r'\nfunction _imgResetSync\([^)]*\)\{[\s\S]*?\n\}', txt)
        if not _rs49:
            errors.append('ไม่พบ _imgResetSync (ดู UI_STANDARD.md ข้อ 5)')
        else:
            _rb49=_rs49.group(0)
            if 'btnImgActual' not in _rb49:
                errors.append('_imgResetSync ต้องคุมปุ่ม btnImgActual ด้วย (ดู UI_STANDARD.md ข้อ 6)')
            if 'el.style.width===el.dataset.w0' not in _rb49 or 'el.style.width===ow' not in _rb49:
                errors.append('_imgResetSync ต้องเทียบขนาดปัจจุบันกับขนาดเป้า (honest-dim: จางเมื่อรูปอยู่ขนาดนั้นแล้ว ทั้ง 2 ปุ่ม · กฎ #6) (ดู UI_STANDARD.md ข้อ 6)')
        if txt.count("'btn.actualSize':'") < 2:
            errors.append('btn.actualSize ต้องมีทั้ง TH และ EN (ดู UI_STANDARD.md ข้อ 6)')
    else:
        errors.append('ไม่พบระบบปุ่มขนาดจริง (btnImgActual/imgActualSize) (ดู UI_STANDARD.md ข้อ 5)')

    # ---- 50) ขนาดเริ่มรูปใหม่ = cap ไม่เกิน 100mm คงสัดส่วน ไม่ขยายเกินจริง (ผู้ใช้ 12 ต.ค. 2026) ----
    #   imgAdd: เริ่มจากขนาดจริงไฟล์ (im.width/height) แล้ว _sc=Math.min(_CAPpx/w,_CAPpx/h,1) โดย _CAPpx=100*96/25.4 (100mm@96dpi)
    #   · ด้านยาวสุดชน 100mm อีกด้านย่อตามสัดส่วน · min(...,1)=รูปเล็กกว่า 100mm ไม่ถูกขยาย · baseline data-w0/h0 = ขนาดหลัง cap
    #   · ห้ามกลับไปใช้กรอบเพดาน _HMAX/_WMAX หรือ fixed 120*r
    _ia50 = re.search(r'\nfunction imgAdd\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _ia50:
        errors.append('ไม่พบ imgAdd (ดู UI_STANDARD.md ข้อ 5)')
    else:
        _b50=_ia50.group(0)
        if '_HMAX' in _b50 or '_WMAX' in _b50 or 'Math.round(120*r)' in _b50:
            errors.append('imgAdd ยังมีโค้ดเพดานเดิม (_HMAX/_WMAX/120*r) — ต้องเปลี่ยนเป็น cap 100mm (ดู UI_STANDARD.md ข้อ 6)')
        elif 'im.width' not in _b50 or 'im.height' not in _b50:
            errors.append('imgAdd ต้องเริ่มจากขนาดจริงไฟล์ (im.width/im.height) (ดู UI_STANDARD.md ข้อ 6)')
        elif '100*96/25.4' not in _b50:
            errors.append('imgAdd ต้อง cap 100mm โดยแปลงหน่วย 100*96/25.4 (px@96dpi) (ดู UI_STANDARD.md ข้อ 6)')
        elif not re.search(r'Math\.min\([^)]*,\s*1\s*\)', _b50):
            errors.append('imgAdd ต้องใช้ Math.min(...,1) กัน upscale เกินขนาดจริง (ดู UI_STANDARD.md ข้อ 6)')
        elif not (re.search(r'w=Math\.round\(w\*_sc\)', _b50) and re.search(r'h=Math\.round\(h\*_sc\)', _b50)):
            errors.append('imgAdd ต้องย่อ w/h ตาม _sc (Math.round(w*_sc)/Math.round(h*_sc)) (ดู UI_STANDARD.md ข้อ 6)')
        elif "el.dataset.w0=w+'px';el.dataset.h0=h+'px';" not in _b50:
            errors.append('imgAdd baseline (data-w0/h0) ต้อง = ขนาดหลัง cap (w/h) (ดู UI_STANDARD.md ข้อ 6)')

    # ---- 51) ป้ายใต้รูป 3 บรรทัด (ชื่อ / ต้นฉบับ px / ปัจจุบัน mm) + bake baseline ตอน save (ผู้ใช้ 12 ต.ค. 2026) ----
    #   sizetag: Original = naturalWidth×naturalHeight px (ความละเอียดไฟล์) · Current = wmm×hmm mm (ขนาดพิมพ์) · คนละหน่วยโดยตั้งใจ (แบบ InDesign/Photoshop)
    #   buildEditorHtml: ตอน save ต้อง bake data-w0/h0 = ขนาดปัจจุบัน (el.style.width/height) → ปุ่มคืนขนาด = ขนาด ณ ครั้ง save ล่าสุด
    #   คีย์ img.origSize/img.curSize ต้องมีทั้ง th + en
    _st = re.search(r"querySelector\('\.sizetag'\);\s*if\(tg\)\{[\s\S]*?\}", txt)
    if not _st:
        errors.append('ไม่พบการสร้างป้าย .sizetag (textContent) (ดู UI_STANDARD.md ข้อ 7)')
    else:
        _bst=_st.group(0)
        _need=['naturalWidth','naturalHeight',"t('img.origSize')","t('img.curSize')"," px"," mm"]
        _miss=[x for x in _need if x not in _bst]
        if _miss:
            errors.append('ป้ายใต้รูปต้องมี: '+', '.join(_miss)+' (ต้นฉบับ px + ปัจจุบัน mm) (ดู UI_STANDARD.md ข้อ 7)')
    _be = re.search(r'function buildEditorHtml\(\)\{[\s\S]*?\n\}', txt)
    if not _be:
        errors.append('ไม่พบ buildEditorHtml (ดู UI_STANDARD.md ข้อ 7)')
    elif not re.search(r"querySelectorAll\('\.fimg'\)\.forEach\([\s\S]*?dataset\.w0=el\.style\.width", _be.group(0)):
        errors.append('buildEditorHtml ต้อง bake data-w0/h0 = ขนาดปัจจุบัน (el.style.width/height) ตอน save (ดู UI_STANDARD.md ข้อ 7)')
    _iobj = txt.find("var I18N={")
    if _iobj>=0:
        _ths=txt.find("th:{",_iobj); _ens=txt.find("en:{",_iobj)
        _thb=txt[_ths:_ens] if (_ths>=0 and _ens>_ths) else ""
        _enb=txt[_ens:_ens+20000] if _ens>=0 else ""
        for _k in ('img.origSize','img.curSize'):
            if ("'"+_k+"'") not in _thb: errors.append('i18n '+_k+' ขาดใน th (ดู UI_STANDARD.md ข้อ 7)')
            if ("'"+_k+"'") not in _enb: errors.append('i18n '+_k+' ขาดใน en (ดู UI_STANDARD.md ข้อ 7)')

    # ---- 52) ป้ายใต้รูป (ขนาดต้นฉบับ/ปัจจุบัน) ต้องเปลี่ยนภาษาตาม TH/EN (ผู้ใช้ 12 ต.ค. 2026) ----
    #   applyLang ต้อง re-render ป้ายของรูปที่เลือกค้างอยู่ (เรียก _imgReadout(_imgSel)) ไม่งั้นคำ "ขนาดต้นฉบับ/ขนาดปัจจุบัน" ค้างภาษาเดิมจนคลิกรูปใหม่
    #   ต้องมี guard: typeof _imgSel + document.contains(_imgSel) (โหลดหน้าแรก var ยังไม่ assign · รูปถูกลบหลัง Undo)
    _al = re.search(r'function applyLang\(\)\{[\s\S]*?\n\}', txt)
    if not _al:
        errors.append('ไม่พบ applyLang (ดู UI_STANDARD.md ข้อ 7)')
    else:
        _bal=_al.group(0)
        if '_imgReadout(_imgSel)' not in _bal:
            errors.append('applyLang ต้องเรียก _imgReadout(_imgSel) เพื่อให้ป้ายใต้รูปเปลี่ยนภาษาตาม TH/EN (ดู UI_STANDARD.md ข้อ 7)')
        elif 'document.contains(_imgSel)' not in _bal:
            errors.append('applyLang re-render ป้ายรูปต้องมี guard document.contains(_imgSel) กันรูปที่ถูกลบหลัง Undo (ดู UI_STANDARD.md ข้อ 7)')


    # ---- 53) รูป add ใหม่ต้องวางในกรอบ A4 คงที่ ไม่ใช่ prc.height ที่ยืดในโหมดแก้ (ผู้ใช้ 12 ต.ค. 2026) ----
    #   บั๊ก: imgAdd เดิมวาง top=prc.height/2-h/2 · prc.height ในโหมดแก้ยืดเกิน 297mm → รูปตกใต้เส้น 297mm → ออกโหมด/เปิดไฟล์ (overflow:hidden) รูปถูกตัดหาย
    #   แก้: top อ้าง A4 คงที่ (297*96/25.4) + clamp ด้วย padding (8*96/25.4) ให้อยู่ในพื้นที่พิมพ์เสมอ · ห้ามใช้ prc.height ในสูตร top
    _ia53 = re.search(r'\nfunction imgAdd\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _ia53:
        errors.append('ไม่พบ imgAdd (ดู UI_STANDARD.md ข้อ 5)')
    else:
        _b53=_ia53.group(0)
        _mtop=re.search(r"top:'\+([^+]+)\+'px", _b53)  # นิพจน์ที่ใช้คำนวณ top ของรูปใหม่
        if not _mtop:
            errors.append("imgAdd ต้องตั้ง top เป็น px ของรูปใหม่ (ดู UI_STANDARD.md ข้อ 6)")
        elif 'prc.height' in _mtop.group(1):
            errors.append("imgAdd ห้ามวาง top จาก prc.height (โหมดแก้หน้ายืดเกิน A4 → รูปตกใต้เส้นตัดหาย) ต้องอ้าง A4 คงที่ (ดู UI_STANDARD.md ข้อ 6)")
        elif '297*96/25.4' not in _b53:
            errors.append("imgAdd ต้องอ้างกรอบ A4 คงที่ (297*96/25.4) ในการวาง top (ดู UI_STANDARD.md ข้อ 6)")
        elif ('Math.max' not in _b53) or ('Math.min' not in _b53):
            errors.append("imgAdd ต้อง clamp top ด้วย Math.max/Math.min ให้อยู่ในพื้นที่พิมพ์ (ดู UI_STANDARD.md ข้อ 6)")


    # ---- 54) client-side XSS: ล็อก pattern ปลอดภัย (defense-in-depth · ผู้ใช้ 12 ต.ค. 2026) ----
    #   app นี้เป็น HTML ไฟล์เดียว รันในเครื่อง — ความเสี่ยงจริงต่ำ แต่ user content (ชื่อเมนู/กลุ่ม/ไฟล์รูป) ไหลเข้า DOM ได้
    #   ล็อกจุดที่ "ปลอดภัยเพราะ pattern" ไม่ให้ถอยหลัง: (ก) epEsc escape ครบ (ข) _renderStatus ใช้ textContent
    #   (ค) _typoGroupOptsHtml escape ชื่อกลุ่ม (ง) dialog ลบกลุ่ม pre-escape (จ) ไม่มี sink อันตราย
    # (ก) epEsc ต้อง escape & < > " ครบทั้ง 4
    _ep54 = re.search(r'function epEsc\([^)]*\)\{[^\n]*\}', txt)
    if not _ep54:
        errors.append('ไม่พบ epEsc (ตัว escape HTML กัน XSS) (ดู UI_STANDARD.md ข้อ 7)')
    elif not all(x in _ep54.group(0) for x in ['&amp;','&lt;','&gt;','&quot;']):
        errors.append('epEsc ต้อง escape & < > " ให้ครบทั้ง 4 (กัน XSS) (ดู UI_STANDARD.md ข้อ 7)')
    # (ข) _renderStatus: ข้อความสถานะต้องลงด้วย textContent ไม่ใช่ innerHTML (ชื่อกลุ่ม/ไฟล์ไหลผ่าน t() แบบไม่ escape)
    _rs54 = re.search(r'function _renderStatus\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _rs54:
        _rsb=_rs54.group(0)
        if 'msgEl.textContent=' not in _rsb:
            errors.append('_renderStatus ต้องตั้งข้อความสถานะด้วย textContent (กัน XSS จากชื่อกลุ่ม/ไฟล์) (ดู UI_STANDARD.md ข้อ 7)')
        elif re.search(r'msgEl\.innerHTML', _rsb):
            errors.append('_renderStatus ห้ามใส่ข้อความสถานะด้วย innerHTML — ใช้ textContent (กัน XSS) (ดู UI_STANDARD.md ข้อ 7)')
    # (ค) _typoGroupOptsHtml: ชื่อกลุ่ม (user content) ต้องผ่าน epEsc ก่อนลง innerHTML
    _tg54 = re.search(r'function _typoGroupOptsHtml\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _tg54 and 'epEsc(' not in _tg54.group(0):
        errors.append('_typoGroupOptsHtml ต้อง escape ชื่อกลุ่มด้วย epEsc ก่อนลง innerHTML (กัน XSS) (ดู UI_STANDARD.md ข้อ 7)')
    # (ง) dialog ลบกลุ่ม: ชื่อกลุ่มที่ส่งเข้า msgArgs ต้อง pre-escape (เพราะ _msgT ลง innerHTML โดยไม่ escape)
    if "msgKey:'pnl.delGroupMsg'" in txt:
        _dg54 = re.search(r"msgKey:'pnl\.delGroupMsg'[^}]*\}", txt)
        if not _dg54 or 'epEsc(' not in _dg54.group(0):
            errors.append('dialog ลบกลุ่ม: ชื่อกลุ่มต้อง epEsc ก่อนส่งเข้า msgArgs (_msgT ลง innerHTML ไม่ escape ในตัว) (ดู UI_STANDARD.md ข้อ 7)')
    # (จ) ห้ามมี sink อันตราย
    for _pat,_lbl in [(r'\beval\s*\(','eval()'),(r'new\s+Function','new Function'),(r'document\.write','document.write'),(r'javascript:','javascript:')]:
        if re.search(_pat, txt):
            errors.append('พบ sink อันตราย "'+_lbl+'" ใน HTML — ห้ามใช้ (กัน XSS) (ดู UI_STANDARD.md ข้อ 7)')


    # ---- 55) ปุ่มขยาย/ย่อรูป (imgScale) ต้องสร้างจุด Undo (ผู้ใช้ 13 ต.ค. 2026) ----
    #   บั๊กเดิม: imgScale ไม่เรียก markDirty → กดขยาย/ย่อแล้ว Ctrl+Z ไม่คืน (ลากมุมคืนได้เพราะ mouseup → markDirty)
    #   แก้: imgScale เรียก markDirty() (debounced เหมือน resize-drag · กดรัวรวมเป็น 1 undo) + guard ไม่เปลี่ยน (ชนขอบ 30px) = ไม่สร้างจุด Undo
    _is55 = re.search(r'\nfunction imgScale\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _is55:
        errors.append('ไม่พบ imgScale (ดู UI_STANDARD.md ข้อ 7)')
    else:
        _b55=_is55.group(0)
        if 'markDirty(' not in _b55:
            errors.append('imgScale ต้องเรียก markDirty() เพื่อสร้างจุด Undo (กดขยาย/ย่อแล้วต้อง Ctrl+Z คืนได้ · กฎ #6) (ดู UI_STANDARD.md ข้อ 7)')
        elif 'nw===cw' not in _b55:
            errors.append('imgScale ต้องมี guard ไม่เปลี่ยน (nw===cw ชนขอบ 30px) = ไม่สร้างจุด Undo (กฎ #6) (ดู UI_STANDARD.md ข้อ 7)')


    # ---- 56) สี default กลุ่มเมนูใหม่ = #171A1E (เท่าสีชื่อเมนู .nm · ผู้ใช้ 13 ต.ค. 2026) ----
    #   เดิมกลุ่มใหม่ (newSection) ใช้ --accent:#4a8579 (เขียวเทา theme เดิม) ไม่เข้าชุดกับ 9 กลุ่มที่มีสีเฉพาะ
    #   ผู้ใช้เลือก #171A1E (= สีชื่อรายการเมนู .nm) → พิมพ์ออกมาเข้ากัน · ต้อง consistent ทั้ง baseline + ตัวเทียบ override + data-acc0 (คืนค่าสี) + fallback outline
    #   ปุ่ม '+ เพิ่มกลุ่ม' (.ed-addgroup) คง #4a8579 ไว้ (ปุ่ม editor บนจอ ไม่พิมพ์ · คนละเรื่อง)
    _ns56 = re.search(r'function newSection\(\)\{[\s\S]*?\n\}', txt)
    if not _ns56:
        errors.append('ไม่พบ newSection (ดู UI_STANDARD.md ข้อ 7)')
    else:
        _b56=_ns56.group(0)
        if '--accent:#171A1E' not in _b56:
            errors.append('newSection baseline --accent ต้อง = #171A1E (ไม่ใช่ #4a8579) (ดู UI_STANDARD.md ข้อ 6)')
        elif '4a8579' in _b56.lower():
            errors.append('newSection ยังมี #4a8579 ค้าง — ต้องเปลี่ยนเป็น #171A1E ให้ครบ (baseline/ตัวเทียบ/data-acc0/fallback outline) (ดู UI_STANDARD.md ข้อ 6)')
        elif "data-acc0','#171A1E'" not in _b56:
            errors.append('newSection: data-acc0 (คืนค่าสี) ต้อง = #171A1E ให้ตรง baseline ใหม่ (ดู UI_STANDARD.md ข้อ 6)')


    # ---- 57) จำสีขอบ/ความหนาล่าสุด (_olLastC/_olLastW) ข้าม reload ผ่าน localStorage (ผู้ใช้ 13 ต.ค. 2026) ----
    #   persist ผ่าน setter เดียว (_olSetLastC/_olSetLastW → _olPersistLast) ไม่กระจาย setItem ทุกจุด (defense-in-depth แบบ lint #54)
    #   โหลดกลับด้วย _olLoadLast() (validate hex + ค่าความหนาที่ถูกต้องก่อนรับ) · key = OL_LAST_KEY
    #   จุด set _olLastC/_olLastW (นอกประกาศ/setter/loader) ต้องเรียกผ่าน setter — ห้าม raw assignment หลุดที่ action sites
    if 'OL_LAST_KEY' not in txt:
        errors.append('ไม่พบ OL_LAST_KEY (จำสีขอบล่าสุดข้าม reload) (ดู UI_STANDARD.md ข้อ 7)')
    else:
        _pl=re.search(r'function _olPersistLast\([^)]*\)\{[^\n]*\}', txt)
        if not _pl or 'localStorage.setItem(OL_LAST_KEY' not in _pl.group(0):
            errors.append('_olPersistLast ต้องเขียน localStorage.setItem(OL_LAST_KEY,...) (ดู UI_STANDARD.md ข้อ 7)')
        if not re.search(r'function _olLoadLast\(', txt):
            errors.append('ไม่พบ _olLoadLast (อ่านสีขอบล่าสุดกลับตอนโหลด) (ดู UI_STANDARD.md ข้อ 7)')
        elif not re.search(r'(?<!function )_olLoadLast\(\)\s*;', txt):
            errors.append('_olLoadLast ต้องถูกเรียกตอนโหลด (ไม่ใช่แค่ประกาศ) (ดู UI_STANDARD.md ข้อ 7)')
        if not re.search(r'function _olSetLastC\([^)]*\)\{[^}]*_olPersistLast\(\)', txt):
            errors.append('_olSetLastC ต้อง set แล้วเรียก _olPersistLast (ดู UI_STANDARD.md ข้อ 7)')
        if not re.search(r'function _olSetLastW\([^)]*\)\{[^}]*_olPersistLast\(\)', txt):
            errors.append('_olSetLastW ต้อง set แล้วเรียก _olPersistLast (ดู UI_STANDARD.md ข้อ 7)')
        # chokepoint หลัก (_olApply) ต้อง persist ผ่าน setter
        if '_olSetLastC(custom||null)' not in txt.replace(' ',''):
            errors.append('_olApply ต้องเก็บสีขอบล่าสุดผ่าน setter (_olSetLastC(custom||null)) (ดู UI_STANDARD.md ข้อ 7)')
        # ห้าม raw assignment หลุดที่ action sites: _olLastC=/_olLastW= ต้องเหลือแค่ประกาศ+setter+loader (อย่างละ 3)
        if len(re.findall(r'_olLastC=', txt))>3:
            errors.append('มี raw assignment _olLastC= หลุดนอก setter — ต้องเรียกผ่าน _olSetLastC (จำไม่ครบข้าม reload) (ดู UI_STANDARD.md ข้อ 7)')
        if len(re.findall(r'_olLastW=', txt))>3:
            errors.append('มี raw assignment _olLastW= หลุดนอก setter — ต้องเรียกผ่าน _olSetLastW (จำไม่ครบข้าม reload) (ดู UI_STANDARD.md ข้อ 7)')


    # ---- 58) ตรวจล้นหน้าครั้งแรกต้องรอฟอนต์เว็บโหลดเสร็จ (document.fonts.ready) (ผู้ใช้ 13 ต.ค. 2026) ----
    #   บั๊ก: window.load เรียก checkOverflow() ทันที → ฟอนต์เว็บ (display=swap) ยังไม่มา วัดด้วย fallback ระบบ (สูงกว่า)
    #   → เตือนล้น + กรอบทองผิดทั้งที่ยังไม่ล้น · พอฟอนต์ swap เข้ามาเนื้อหาหด แต่ไม่ตรวจซ้ำ = คำเตือนค้าง
    #   แก้: ครั้งแรกเรียกผ่าน document.fonts.ready.then(checkOverflow) + fallback checkOverflow ตรงถ้าไม่มี document.fonts
    _lh = re.search(r"window\.addEventListener\('load',\s*function\(\)\{[\s\S]*?\n\}\);", txt)
    if not _lh:
        errors.append('ไม่พบ window load handler (ดู UI_STANDARD.md ข้อ 7)')
    else:
        _blh=_lh.group(0)
        if 'document.fonts.ready' not in _blh:
            errors.append('ตรวจล้นหน้าครั้งแรกต้องรอ document.fonts.ready ก่อน (กันเตือนล้นผิดตอนฟอนต์ยังไม่โหลด) (ดู UI_STANDARD.md ข้อ 7)')
        elif not re.search(r'document\.fonts\.ready\.then\(function\(\)\{\s*checkOverflow\(\)', _blh):
            errors.append('document.fonts.ready.then ต้องเรียก checkOverflow() (ดู UI_STANDARD.md ข้อ 7)')
        elif 'else checkOverflow()' not in _blh:
            errors.append('load handler ต้องมี fallback checkOverflow() ตรงเมื่อไม่มี document.fonts (เบราว์เซอร์เก่า) (ดู UI_STANDARD.md ข้อ 7)')


    # ---- 59) section สุดท้ายในคอลัมน์ต้องตัด margin ล่าง (กันเตือนล้นหน้าจากระยะเกินท้ายหน้า · ผู้ใช้ 13 ต.ค. 2026) ----
    #   .sec มี margin-bottom:9px (2.38mm) · section สุดท้ายในคอลัมน์ทิ้งระยะนี้ท้ายหน้า → ตัวตรวจเตือนล้นทั้งที่ขอบหน้า 8mm ให้ที่ว่างอยู่แล้ว
    #   แก้: .col section.sec:last-of-type{margin-bottom:0} · ใช้ :last-of-type (ปุ่มเพิ่มกลุ่ม .ed-addgroup เป็น child ท้ายสุด → :last-child ผิดตัว)
    _m59 = re.search(r'\.col\s+section\.sec:last-of-type\s*\{[^}]*margin-bottom:\s*0', txt)
    if not _m59:
        errors.append('ต้องมี .col section.sec:last-of-type{margin-bottom:0} (ตัดระยะเกินท้ายคอลัมน์ กันเตือนล้นผิด) (ดู UI_STANDARD.md ข้อ 7)')


    # ---- 60) เตือนล้นหน้า: tolerance 3mm + เตือนเฉพาะตอนแก้ไข (ยังไม่ save) + หมายเหตุเล็กตอนเปิดไฟล์ (ผู้ใช้ 13 ต.ค. 2026) ----
    #   (ก) tolerance 3mm: var _OVF_TOL=Math.round(3*96/25.4) · เทียบ scrollHeight > clientHeight + _OVF_TOL (ไม่ใช่ +2)
    #   (ข) กรอบทอง .overflowed + คำเตือนเต็ม เฉพาะตอน _dirty (แก้ไขยังไม่ save) · เปิดไฟล์/หลัง save = ไม่เตือน
    #   (ค) หมายเหตุเล็ก (st.overflowNote + class ovfnote) ตอนไม่ dirty · (ง) clearDirty refresh checkOverflow · (จ) i18n + CSS ครบ
    _co60 = re.search(r'\nfunction checkOverflow\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _co60:
        errors.append('ไม่พบ checkOverflow — lint ข้อ 60 ตรวจไม่ได้')
    else:
        _b60=_co60.group(0)
        if 'Math.round(3*96/25.4)' not in txt:
            errors.append('ต้องมี _OVF_TOL=Math.round(3*96/25.4) (ผ่อนปรนล้นหน้า 3mm) (ดู UI_STANDARD.md ข้อ 7)')
        if 'clientHeight + _OVF_TOL' not in _b60:
            errors.append('checkOverflow ต้องเทียบ clientHeight + _OVF_TOL (3mm) ไม่ใช่ +2 (ดู UI_STANDARD.md ข้อ 7)')
        if not re.search(r'if\(_dirty\)\s*pg\.classList\.add\(', _b60):
            errors.append('checkOverflow: กรอบทอง .overflowed ต้องใส่เฉพาะตอน _dirty (เปิดไฟล์ไม่ขึ้นกรอบ) (ดู UI_STANDARD.md ข้อ 7)')
        if not re.search(r'if\(bad\.length\)\{\s*if\(_dirty\)\{', _b60):
            errors.append('checkOverflow: คำเตือนเต็มต้อง gate ด้วย if(_dirty) (เตือนเฉพาะตอนแก้ไข) (ดู UI_STANDARD.md ข้อ 7)')
    # (ค) หมายเหตุเล็กใน _renderStatus
    _rs60 = re.search(r'function _renderStatus\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _rs60:
        _rb=_rs60.group(0)
        if "st.overflowNote" not in _rb or "ovfnote" not in _rb:
            errors.append('_renderStatus ต้องมีหมายเหตุเล็ก (st.overflowNote + class ovfnote) ตอนไม่เตือนเต็ม (ดู UI_STANDARD.md ข้อ 7)')
    # (ง) clearDirty refresh
    _cd60 = re.search(r'function clearDirty\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _cd60 or 'checkOverflow()' not in _cd60.group(0):
        errors.append('clearDirty ต้องเรียก checkOverflow() (หลัง save เอากรอบทอง/คำเตือนออก) (ดู UI_STANDARD.md ข้อ 7)')
    # (จ) i18n + CSS
    _iobj60 = txt.find("var I18N={")
    if _iobj60>=0:
        _ths=txt.find("th:{",_iobj60); _ens=txt.find("en:{",_iobj60)
        _thb=txt[_ths:_ens] if (_ths>=0 and _ens>_ths) else ""
        _enb=txt[_ens:_ens+20000] if _ens>=0 else ""
        for _k in ('st.overflowNote','st.overflowNoteTtl'):
            if ("'"+_k+"'") not in _thb: errors.append('i18n '+_k+' ขาดใน th (ดู UI_STANDARD.md ข้อ 7)')
            if ("'"+_k+"'") not in _enb: errors.append('i18n '+_k+' ขาดใน en (ดู UI_STANDARD.md ข้อ 7)')
    if '.edstatus-meta.ovfnote' not in txt:
        errors.append('ขาด CSS .edstatus-meta.ovfnote (สไตล์หมายเหตุเล็ก) (ดู UI_STANDARD.md ข้อ 7)')


    # ---- 61) ข้อความ I18N ห้ามขึ้นต้นด้วยไอคอนเตือน ⚠️/⛔ (ไอคอนซ้ำ · ผู้ใช้ 13 ต.ค. 2026) ----
    #   แถบล่าง (_renderStatus) + ประวัติ (_actlogIcon) render ไอคอนตามชนิดเองแล้ว (warning→⚠️ error→⛔)
    #   → ถ้าข้อความขึ้นต้นด้วย ⚠️ อีก = ไอคอนซ้ำ (เห็นสามเหลี่ยม 2 อัน) · ข้อยกเว้นเดียว: st.overflowPill (แสดงในป้าย edstatus-meta ที่ไม่มีไอคอน)
    _OVF_PILL_OK={'st.overflowPill'}
    for _m61 in re.finditer(r"'([A-Za-z][A-Za-z0-9_.]*)':'(?:\u26a0|\u26d4)", txt):
        if _m61.group(1) not in _OVF_PILL_OK:
            errors.append('ข้อความ i18n "'+_m61.group(1)+'" ขึ้นต้นด้วย ⚠️/⛔ — ไอคอนซ้ำกับ _renderStatus/_actlogIcon ให้เอาออก (ยกเว้น st.overflowPill) (ดู UI_STANDARD.md ข้อ 7)')


    # ---- 62) คำเตือนกรอกช่อง input (input validation) ไม่จดประวัติ — แสดงแถบล่างอย่างเดียว (แนว B · ผู้ใช้ 13 ต.ค. 2026) ----
    #   พิมพ์ตัวที่ช่องไม่รับ / เกินช่วง = ไม่ใช่การกระทำกับเมนู → _logFromFlash ข้าม (ไม่ logAdd) ด้วย denylist _NOLOG ตาม i18n key
    #   _NOLOG ต้องมีคีย์ input-filter ครบ (price/amount/hex/size/shadow/pages/text) · guard: if(msg._k && _NOLOG[msg._k]) return; ก่อน logAdd
    _need62=['fl.prNumOnly','fl.prTooLong','fl.amtNumOnly','fl.amtTooLong','fl.hexOnly','fl.hexOnlyTh',
             'fl.sizeOnly','fl.sizeOnlyTh','fl.sizeRange','fl.sizeStep','fl.shdOnly','fl.shdOnlyTh','fl.shdRange',
             'fl.pagesOnly','fl.pagesOnlyTh','fl.pagesFull','fl.pagesTooLong','fl.txtLines','fl.txtNoEnter','fl.txtTooLong']
    _m62 = re.search(r'var _NOLOG=\{([^}]*)\}', txt)
    if not _m62:
        errors.append('ไม่พบ _NOLOG (ชุดคีย์คำเตือน input ที่ไม่จดประวัติ · แนว B) (ดู UI_STANDARD.md ข้อ 7)')
    else:
        _body62=_m62.group(1)
        _miss62=[k for k in _need62 if ("'"+k+"'") not in _body62]
        if _miss62:
            errors.append('_NOLOG ขาดคีย์ input-filter: '+', '.join(_miss62)+' (ดู UI_STANDARD.md ข้อ 7)')
        # sizeLimit ต้อง NOT อยู่ใน NOLOG (เป็น action ปุ่ม +/−)
        if "'fl.sizeLimit'" in _body62:
            errors.append('_NOLOG ไม่ควรมี fl.sizeLimit (ปุ่ม +/− ชนขีด = action ปุ่ม ต้องจดประวัติ) (ดู UI_STANDARD.md ข้อ 7)')
    _lf62 = re.search(r'function _logFromFlash\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _lf62:
        errors.append('ไม่พบ _logFromFlash (ดู UI_STANDARD.md ข้อ 7)')
    elif not re.search(r'_NOLOG\[msg\._k\]\s*\)\s*return', _lf62.group(0)):
        errors.append('_logFromFlash ต้องข้าม logAdd เมื่อ msg._k อยู่ใน _NOLOG (แนว B) (ดู UI_STANDARD.md ข้อ 7)')


    # ---- 63) autosave ร่างกันงานหาย (ผู้ใช้ 13 ต.ค. 2026) ----
    #   เก็บ _lastSnap (HTML บีบอัด pool-id) ลง localStorage ทุกครั้งที่แก้ (_draftSave ใน _takeSnapshot) · บันทึกสำเร็จ=ลบร่าง (_draftClear ใน clearDirty)
    #   เปิดไฟล์เจอร่าง=เสนอกู้คืน (_draftOffer ใน load) · กู้คืนใช้ _restorePages + ดรอปรูปที่ POOL ไม่มี (รูปเพิ่มใหม่ที่ยังไม่บันทึก)
    #   แถบ #draftBar เป็นของจอ ต้องถูก strip ใน buildEditorHtml + buildMenuHtml · i18n draft.* + fl.draft* ครบ th+en
    for _fn63 in ('_draftKey','_draftSave','_draftClear','_draftRestore','_draftOffer'):
        if ('function '+_fn63+'(') not in txt:
            errors.append('ไม่พบ '+_fn63+' (autosave ร่างกันงานหาย) (ดู UI_STANDARD.md ข้อ 7)')
    _ts63 = re.search(r'function _takeSnapshot\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _ts63 or '_draftSave()' not in _ts63.group(0):
        errors.append('_takeSnapshot ต้องเรียก _draftSave() (autosave ทุกครั้งที่แก้) (ดู UI_STANDARD.md ข้อ 7)')
    _cd63 = re.search(r'function clearDirty\([^)]*\)\{[\s\S]*?\n\}', txt)
    if not _cd63 or '_draftClear()' not in _cd63.group(0):
        errors.append('clearDirty ต้องเรียก _draftClear() (บันทึกสำเร็จ=ลบร่าง) (ดู UI_STANDARD.md ข้อ 7)')
    _lh63 = re.search(r"window\.addEventListener\('load',\s*function\(\)\{[\s\S]*?\n\}\);", txt)
    if not _lh63 or '_draftOffer()' not in _lh63.group(0):
        errors.append('load handler ต้องเรียก _draftOffer() (เสนอกู้คืนร่าง) (ดู UI_STANDARD.md ข้อ 7)')
    _dr63 = re.search(r'function _draftRestore\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _dr63 and '_restorePages(' not in _dr63.group(0):
        errors.append('_draftRestore ต้องใช้ _restorePages (กลไกเดียวกับ Undo) (ดู UI_STANDARD.md ข้อ 7)')
    # #draftBar ต้องถูก strip ทั้ง 2 build (เป็นของจอ ไม่ลงไฟล์)
    _be63 = re.search(r'function buildEditorHtml\(\)\{[\s\S]*?\n\}', txt)
    if _be63 and '#draftBar' not in _be63.group(0):
        errors.append('buildEditorHtml ต้อง strip #draftBar (แถบกู้คืนเป็นของจอ) (ดู UI_STANDARD.md ข้อ 7)')
    _bm63 = re.search(r'function buildMenuHtml\(\)\{[\s\S]*?\n\}', txt)
    if _bm63 and '#draftBar' not in _bm63.group(0):
        errors.append('buildMenuHtml ต้อง strip #draftBar (แถบกู้คืนเป็นของจอ) (ดู UI_STANDARD.md ข้อ 7)')
    # i18n ครบ th+en
    _iobj63 = txt.find("var I18N={")
    if _iobj63>=0:
        _ths=txt.find("th:{",_iobj63); _ens=txt.find("en:{",_iobj63)
        _thb=txt[_ths:_ens] if (_ths>=0 and _ens>_ths) else ""
        _enb=txt[_ens:_ens+20000] if _ens>=0 else ""
        for _k in ('draft.found','draft.restore','draft.discard','fl.draftRestored','fl.draftRestoredLost','fl.draftDiscarded'):
            if ("'"+_k+"'") not in _thb: errors.append('i18n '+_k+' ขาดใน th (ดู UI_STANDARD.md ข้อ 7)')
            if ("'"+_k+"'") not in _enb: errors.append('i18n '+_k+' ขาดใน en (ดู UI_STANDARD.md ข้อ 7)')
    if '#draftBar{' not in txt:
        errors.append('ขาด CSS #draftBar (สไตล์แถบกู้คืน) (ดู UI_STANDARD.md ข้อ 7)')


    # ---- 64) ฟอนต์ offline: ฝัง @font-face ครบ 3 · ห้ามพึ่ง Google CDN · dropdown เหลือ 3 (ผู้ใช้ 13 ต.ค. 2026) ----
    #   ฝัง Prompt/Sarabun/Noto Sans Thai เป็น base64 TTF ใน @font-face (offline จริง) · ตัด Kanit/Mitr/Bai Jamjuree ออกจาก dropdown
    #   base64 ไม่มีอักขระ . หรือ ' จึงไม่ชน false positive กับ fonts.gstatic.com / 'Kanit' ฯลฯ
    # ห้าม CDN เฉพาะ "นอก <script>" — fetch รันไทม์ใน JS (Phase 3 เลือกฟอนต์ Google) มี URL googleapis ได้ แต่ <link>/@import ห้าม
    _nojs64=re.sub(r'<script[\s\S]*?</script>','',txt)
    for _cdn64 in ("fonts.googleapis.com","fonts.gstatic.com"):
        if _cdn64 in _nojs64:
            errors.append("พบ "+_cdn64+" นอก <script> — ฟอนต์ base ต้องฝัง offline ห้ามพึ่ง Google CDN ผ่าน <link>/@import (ดู UI_STANDARD.md ข้อ 8)")
    if re.search(r'<link[^>]*fonts\.(?:googleapis|gstatic)', txt) or re.search(r'@import[^;]*fonts\.(?:googleapis|gstatic)', txt):
        errors.append("พบ <link>/@import ไป Google Fonts — ห้ามพึ่ง CDN (ฟอนต์ base ต้องฝัง · ฟอนต์ Google ที่เลือกเพิ่มใช้ fetch รันไทม์เท่านั้น) (ดู UI_STANDARD.md ข้อ 8)")
    for _ff64 in ("'Prompt'","'Sarabun'","'Noto Sans Thai'"):
        if ("@font-face{font-family:"+_ff64) not in txt:
            errors.append("ขาด @font-face ฝังฟอนต์ "+_ff64+" (offline) (ดู UI_STANDARD.md ข้อ 8)")
    _sel64=re.search(r'<select id="typoFont"[\s\S]*?</select>', txt)
    if _sel64:
        _sb64=_sel64.group(0)
        for _rm64 in ("'Kanit'","'Mitr'","'Bai Jamjuree'"):
            if _rm64 in _sb64:
                errors.append("dropdown #typoFont ยังมี "+_rm64+" — ต้องตัดฟอนต์ที่ไม่ได้ฝังออก (ดู UI_STANDARD.md ข้อ 8)")
        for _keep64 in ("'Prompt'","'Sarabun'","'Noto Sans Thai'"):
            if _keep64 not in _sb64:
                errors.append("dropdown #typoFont ขาด "+_keep64+" (ดู UI_STANDARD.md ข้อ 8)")
    else:
        errors.append("ไม่พบ <select id=\"typoFont\"> — lint ข้อ 64 ตรวจไม่ได้")


    # ---- 65) อัปโหลดฟอนต์เอง + ฐานทะเบียนฟอนต์ (Phase 0+1 · ผู้ใช้ 14 ต.ค. 2026) ----
    #   ฟอนต์อัปโหลดฝังเป็น @font-face ใน <style id="userFonts"> (อยู่ใน <head> → เดินทางไปกับไฟล์ผ่าน cloneNode ทั้ง 2 build)
    #   buildMenuHtml/buildEditorHtml ห้ามแตะ/ลบ #userFonts (ไม่งั้นฟอนต์ที่อัปโหลดจะไม่ติดไปกับไฟล์ที่บันทึก)
    if '<style id="userFonts">' not in txt:
        errors.append('ไม่พบ <style id="userFonts"> — ฐานฟอนต์อัปโหลด (ดู UI_STANDARD.md ข้อ 8)')
    _bm65=re.search(r'\nfunction buildMenuHtml\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _bm65 and 'userFonts' in _bm65.group(0):
        errors.append('buildMenuHtml แตะ #userFonts — ฟอนต์อัปโหลดต้องเดินทางไปกับไฟล์ ห้าม strip (ดู UI_STANDARD.md ข้อ 8)')
    _be65=re.search(r'\nfunction buildEditorHtml\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _be65 and 'userFonts' in _be65.group(0):
        errors.append('buildEditorHtml แตะ #userFonts — ฟอนต์อัปโหลดต้องเดินทางไปกับไฟล์ ห้าม strip (ดู UI_STANDARD.md ข้อ 8)')
    for _fn65 in ('fontUploadPick','_fontUploadFile'):
        if ('function '+_fn65+'(') not in txt:
            errors.append('ไม่พบ '+_fn65+' (อัปโหลดฟอนต์เอง) (ดู UI_STANDARD.md ข้อ 8)')
    _uf65=re.search(r'\nfunction _fontUploadFile\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _uf65:
        _b65=_uf65.group(0)
        if '_fontFmt(' not in _b65 or 'fl.fontBadType' not in _b65:
            errors.append('_fontUploadFile ไม่ได้ตรวจชนิดไฟล์ (_fontFmt + fl.fontBadType) — ปุ่มต้องปฏิเสธไฟล์ที่ไม่ใช่ฟอนต์ (ดู UI_STANDARD.md ข้อ 8)')
        if 'markDirty' not in _b65:
            errors.append('_fontUploadFile ไม่เรียก markDirty — อัปโหลดฟอนต์ต้องเป็นจุด Undo/บันทึก (ดู UI_STANDARD.md ข้อ 6)')
        if '@font-face' not in _b65 or 'format(' not in _b65 or 'data:' not in _b65:
            errors.append('_fontUploadFile ไม่ได้ฝังเป็น @font-face base64 (data: + format()) (ดู UI_STANDARD.md ข้อ 8)')
    else:
        errors.append('ไม่พบตัว _fontUploadFile — lint ข้อ 65 ตรวจไม่ได้')
    _fi65=re.search(r'<input\b[^>]*id="fontInput"[^>]*>', txt)
    if not _fi65:
        errors.append('ไม่พบ <input id="fontInput"> (เลือกไฟล์ฟอนต์) (ดู UI_STANDARD.md ข้อ 8)')
    elif '.ttf' not in _fi65.group(0):
        errors.append('<input id="fontInput"> ไม่ได้จำกัดชนิดฟอนต์ (.ttf/.otf/.woff/.woff2) (ดู UI_STANDARD.md ข้อ 8)')
    _sel65=re.search(r'<select id="typoFont"[\s\S]*?</select>', txt)
    if _sel65 and 'id="typoFontUser"' not in _sel65.group(0):
        errors.append('dropdown #typoFont ขาด <optgroup id="typoFontUser"> (กลุ่มฟอนต์ที่อัปโหลด) (ดู UI_STANDARD.md ข้อ 8)')
    _i65=txt.find("var I18N={")
    if _i65>=0:
        _th65=txt.find("th:{",_i65); _en65=txt.find("en:{",_i65)
        _thb65=txt[_th65:_en65] if (_th65>=0 and _en65>_th65) else ""
        _enb65=txt[_en65:_en65+30000] if _en65>=0 else ""
        for _k65 in ('btn.addFont','font.userGroup','ttl.addFont','fl.fontAdded','fl.fontBadType','fl.fontAddErr'):
            if ("'"+_k65+"'") not in _thb65: errors.append('i18n '+_k65+' ขาดใน th (ดู UI_STANDARD.md ข้อ 8)')
            if ("'"+_k65+"'") not in _enb65: errors.append('i18n '+_k65+' ขาดใน en (ดู UI_STANDARD.md ข้อ 8)')


    # ---- 66) เลือกฟอนต์จาก Google (Phase 3 · แบบ B ดึง woff2 มาฝัง · ผู้ใช้ 14 ต.ค. 2026) ----
    #   ปุ่ม #btnAddGFont เปิด popover #gfontPop → fetch css2 → fetch woff2 → ฝัง base64 ใน #userFonts (ท่อ Phase 1) → เดินทางไปกับไฟล์
    #   ทุกเบราว์เซอร์ (fetch universal) · ต่อเน็ตเฉพาะตอนเพิ่ม · ปุ่มต้องไม่หลอก = ต้องมี handler offline/not-found
    if 'id="btnAddGFont"' not in txt:
        errors.append('ไม่พบปุ่ม #btnAddGFont (เลือกฟอนต์ Google) (ดู UI_STANDARD.md ข้อ 8)')
    elif 'onclick="_gfontToggle()"' not in txt:
        errors.append('#btnAddGFont ไม่ผูก onclick _gfontToggle() (ดู UI_STANDARD.md ข้อ 8)')
    if 'id="gfontPop"' not in txt:
        errors.append('ไม่พบ popover #gfontPop (ดู UI_STANDARD.md ข้อ 8)')
    for _fn66 in ('_gfontToggle','_gfontOpen','_gfontClose','_gfontAdd','_ab2b64','_fontAddOpt'):
        if ('function '+_fn66+'(') not in txt:
            errors.append('ไม่พบ '+_fn66+' (เลือกฟอนต์ Google) (ดู UI_STANDARD.md ข้อ 8)')
    # list ชื่อซ้าย/ตัวอย่างขวา + scroll (ผู้ใช้ 15 ต.ค. 2026) — chips เดิมถูกแทนด้วย list
    for _fn66b in ('_gfontList','_gfontPrevLoad'):
        if ('function '+_fn66b+'(') not in txt:
            errors.append('ไม่พบ '+_fn66b+' (รายการฟอนต์ Google แบบ list) (ดู UI_STANDARD.md ข้อ 8)')
    if 'id="gfontList"' not in txt:
        errors.append('ไม่พบ #gfontList (รายการฟอนต์แบบ list) (ดู UI_STANDARD.md ข้อ 8)')
    # _gfontList ต้องสร้างรายการจาก _GTHAI (โชว์ครบทุกตัว ให้ตรงกับ #gfontCount — list ไม่โกหกจำนวน) ผู้ใช้ 15 ต.ค. 2026
    _glln66=[l for l in txt.split('\n') if 'function _gfontList(' in l]
    if _glln66 and '_GTHAI' not in _glln66[0]:
        errors.append('_gfontList ต้องสร้างรายการจาก _GTHAI (โชว์ครบทุกตัว ให้ตรงกับ #gfontCount) (ดู UI_STANDARD.md ข้อ 8)')
    # โน้ต OFL มีลิงก์ไปหน้า SIL OFL จริง (ผู้ใช้ 15 ต.ค. 2026) — ลิงก์ต้องเปิดแท็บใหม่อย่างปลอดภัย (signifier ต้องทำงานจริง · กฎ #6)
    _ofl66=re.search(r'<a\b[^>]*href="https://openfontlicense\.org/ofl-fonts/"[^>]*>', txt)
    if not _ofl66:
        errors.append('ไม่พบลิงก์ OFL (<a href=openfontlicense.org/ofl-fonts/>) ในโน้ตฟอนต์ (ดู UI_STANDARD.md ข้อ 8)')
    elif 'target="_blank"' not in _ofl66.group(0) or 'noopener' not in _ofl66.group(0):
        errors.append('ลิงก์ OFL ต้องเปิดแท็บใหม่อย่างปลอดภัย (target="_blank" + rel="noopener") (ดู UI_STANDARD.md ข้อ 8)')
    # ช่องพิมพ์ชื่อฟอนต์ gfontInput ต้องอยู่ใน whitelist mousedown #typobar ไม่งั้นพิมพ์ไม่ได้ (บั๊ก cursor 15 ต.ค. · แบบเดียวกับ #35)
    _md66=re.search(r"getElementById\('typobar'\)\.addEventListener\('mousedown',[\s\S]{0,600}?saveSelection\(\); return; \}", txt)
    if not _md66 or "e.target.id==='gfontInput'" not in _md66.group(0):
        errors.append("gfontInput ไม่อยู่ใน whitelist mousedown #typobar — ช่องพิมพ์ชื่อฟอนต์จะไม่รับ cursor (ดู UI_STANDARD.md ข้อ 8)")
    # ตัวอย่างฟอนต์ต้องเป็นของบนจอ (FontFace API) ไม่ใช่ <link>/<style> ที่ serialize ลงไฟล์
    _pl66=re.search(r'\n(?:async )?function _gfontPrevLoad\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _pl66 and ('new FontFace' not in _pl66.group(0) or 'document.fonts.add' not in _pl66.group(0)):
        errors.append('_gfontPrevLoad ต้องใช้ FontFace API (new FontFace + document.fonts.add) — ตัวอย่างเป็นของบนจอ ไม่รั่วลงไฟล์ (ดู UI_STANDARD.md ข้อ 8)')
    _ga66=re.search(r'\n(?:async )?function _gfontAdd\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _ga66:
        _b66=_ga66.group(0)
        if 'fetch(' not in _b66:
            errors.append('_gfontAdd ไม่ได้ fetch จาก Google (ดู UI_STANDARD.md ข้อ 8)')
        if 'data:' not in _b66 or 'userFonts' not in _b66:
            errors.append('_gfontAdd ไม่ได้ฝังเป็น base64 (data:) ลง #userFonts — ฟอนต์ต้องเดินทางไปกับไฟล์ (ดู UI_STANDARD.md ข้อ 8)')
        if 'markDirty' not in _b66:
            errors.append('_gfontAdd ไม่เรียก markDirty — เพิ่มฟอนต์ต้องเป็นจุด Undo/บันทึก (ดู UI_STANDARD.md ข้อ 6)')
        if 'fl.gfontOffline' not in _b66 or 'fl.gfontNotFound' not in _b66:
            errors.append('_gfontAdd ไม่มี handler offline/not-found — ปุ่มต้องไม่หลอกเมื่อไม่มีเน็ต/ไม่พบฟอนต์ (ดู UI_STANDARD.md ข้อ 8)')
    else:
        errors.append('ไม่พบตัว _gfontAdd — lint ข้อ 66 ตรวจไม่ได้')
    _be66=re.search(r'\nfunction buildEditorHtml\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _be66 and '#gfontPop' not in _be66.group(0):
        errors.append('buildEditorHtml ไม่ได้ปิด/ล้าง #gfontPop ก่อนบันทึก (popover ไม่ควรบันทึกค้างเปิด) (ดู UI_STANDARD.md ข้อ 8)')
    # select-then-add + search (ผู้ใช้ 15 ต.ค. 2026): 2 รายการ (บน=แนะนำ · ล่าง=ผลค้นหา) · ปุ่มเพิ่ม enabled เฉพาะตอนเลือก
    for _fn66c in ('_gfontSearch','_gfontSelect','_gfontClearSel','_gfontAddSel'):
        if ('function '+_fn66c+'(') not in txt:
            errors.append('ไม่พบ '+_fn66c+' (select-then-add + ค้นหา) (ดู UI_STANDARD.md ข้อ 8)')
    if 'id="gfontResults"' not in txt:
        errors.append('ไม่พบ #gfontResults (รายการผลค้นหา) (ดู UI_STANDARD.md ข้อ 8)')
    # note จำนวนฟอนต์ไทยในหัวลิสต์ (ผู้ใช้ 15 ต.ค. 2026) — ตัวเลขต้องดึงจาก _GTHAI.length อัตโนมัติ ไม่ hardcode (ปุ่มไม่หลอก)
    if 'id="gfontCount"' not in txt:
        errors.append('ไม่พบ #gfontCount (ป้ายจำนวนฟอนต์ไทยในหัวลิสต์) (ดู UI_STANDARD.md ข้อ 8)')
    _go66=re.search(r'\nfunction _gfontOpen\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _go66 and "getElementById('gfontCount')" not in _go66.group(0):
        errors.append('_gfontOpen ไม่ได้เติมจำนวนฟอนต์ลง #gfontCount จาก _GTHAI.length — ป้ายจำนวนต้องตรงกับรายการจริง (ดู UI_STANDARD.md ข้อ 8)')
    if _go66 and '_GTHAI.length' not in _go66.group(0):
        errors.append('#gfontCount ต้องใช้ _GTHAI.length (ห้าม hardcode ตัวเลข — ปุ่มไม่หลอก) (ดู UI_STANDARD.md ข้อ 8)')
    _sb66=re.search(r'<button\b[^>]*id="gfontSearchBtn"[^>]*>', txt)
    if not _sb66:
        errors.append('ไม่พบปุ่ม #gfontSearchBtn (ปุ่มค้นหา) (ดู UI_STANDARD.md ข้อ 8)')
    elif 'onclick="_gfontSearch()"' not in _sb66.group(0):
        errors.append('#gfontSearchBtn ไม่ผูก onclick _gfontSearch() (ดู UI_STANDARD.md ข้อ 8)')
    _ab66=re.search(r'<button\b[^>]*id="gfontAddBtn"[^>]*>', txt)
    if not _ab66:
        errors.append('ไม่พบปุ่ม #gfontAddBtn (ปุ่มเพิ่มฟอนต์ที่เลือก) (ดู UI_STANDARD.md ข้อ 8)')
    else:
        _abt=_ab66.group(0)
        if 'disabled' not in _abt:
            errors.append('#gfontAddBtn ต้อง disabled เป็นค่าเริ่มต้น — enabled เฉพาะตอนเลือกฟอนต์ (ดู UI_STANDARD.md ข้อ 5)')
        if 'onclick="_gfontAddSel()"' not in _abt:
            errors.append('#gfontAddBtn ไม่ผูก onclick _gfontAddSel() (ดู UI_STANDARD.md ข้อ 8)')
    _sel66=re.search(r'\nfunction _gfontSelect\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _sel66 and 'disabled=false' not in _sel66.group(0):
        errors.append('_gfontSelect ต้อง enable #gfontAddBtn (ab.disabled=false) เมื่อเลือกฟอนต์ (ดู UI_STANDARD.md ข้อ 5)')
    _cl66=re.search(r'\nfunction _gfontClearSel\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _cl66 and 'disabled=true' not in _cl66.group(0):
        errors.append('_gfontClearSel ต้อง disable #gfontAddBtn เมื่อไม่มีฟอนต์ที่เลือก (ดู UI_STANDARD.md ข้อ 5)')
    _i66=txt.find("var I18N={")
    if _i66>=0:
        _th66=txt.find("th:{",_i66); _en66=txt.find("en:{",_i66)
        _thb66=txt[_th66:_en66] if (_th66>=0 and _en66>_th66) else ""
        _enb66=txt[_en66:_en66+30000] if _en66>=0 else ""
        for _k66 in ('btn.addGFont','ttl.addGFont','gfont.title','gfont.inlbl','gfont.add','gfont.oflPre','gfont.oflName','gfont.oflPost','gfont.browsehint','btn.gfontSearch','gfont.browselbl','fl.gfontNoMatch','fl.gfontLoading','fl.gfontAdded','fl.gfontNotFound','fl.gfontOffline','fl.gfontDup','fl.gfontAddErr'):
            if ("'"+_k66+"'") not in _thb66: errors.append('i18n '+_k66+' ขาดใน th (ดู UI_STANDARD.md ข้อ 8)')
            if ("'"+_k66+"'") not in _enb66: errors.append('i18n '+_k66+' ขาดใน en (ดู UI_STANDARD.md ข้อ 8)')

    # ---- 67) จัดกลุ่ม "ฟอนต์มากับแอป" + โน้ตฝังไฟล์ใต้แถบ + upload เตือนซ้ำ (ผู้ใช้ 15 ต.ค. 2026) ----
    # (a) optgroup ฟอนต์มาตรฐาน 3 ตัว ต้องอยู่ในกลุ่ม typoFontBase (ชื่อกลุ่มสื่อว่ามากับแอป)
    _sel67=re.search(r'<select id="typoFont"[\s\S]*?</select>', txt)
    if _sel67 and 'id="typoFontBase"' not in _sel67.group(0):
        errors.append('dropdown #typoFont ขาด <optgroup id="typoFontBase"> (กลุ่มฟอนต์มากับแอป) (ดู UI_STANDARD.md ข้อ 8)')
    # (c) upload เตือนซ้ำ ไม่เอาเข้า — _fontUploadFile ต้องเช็ก _gfontFamExists ก่อนเพิ่ม (ให้ตรงกับ Google)
    _uf67=re.search(r'\nfunction _fontUploadFile\([^)]*\)\{[\s\S]*?\n\}', txt)
    if _uf67 and '_gfontFamExists(' not in _uf67.group(0):
        errors.append('_fontUploadFile ไม่เช็กฟอนต์ซ้ำ (_gfontFamExists) — อัปโหลดชื่อซ้ำต้องเตือน+ไม่เพิ่มซ้ำ ให้ตรงกับ Google (ดู UI_STANDARD.md ข้อ 8)')
    if _uf67 and 'fl.fontDup' not in _uf67.group(0):
        errors.append('_fontUploadFile ไม่แจ้ง fl.fontDup ตอนเจอฟอนต์ซ้ำ (ดู UI_STANDARD.md ข้อ 8)')
    # (d) i18n ครบ th+en
    _i67=txt.find("var I18N={")
    if _i67>=0:
        _th67=txt.find("th:{",_i67); _en67=txt.find("en:{",_i67)
        _thb67=txt[_th67:_en67] if (_th67>=0 and _en67>_th67) else ""
        _enb67=txt[_en67:_en67+30000] if _en67>=0 else ""
        for _k67 in ('font.baseGroup','fl.fontDup'):
            if ("'"+_k67+"'") not in _thb67: errors.append('i18n '+_k67+' ขาดใน th (ดู UI_STANDARD.md ข้อ 8)')
            if ("'"+_k67+"'") not in _enb67: errors.append('i18n '+_k67+' ขาดใน en (ดู UI_STANDARD.md ข้อ 8)')

    # ---- 68) selectionchange ต้องไม่แย่งเลือกทับเส้นจุด (.ln) ที่เพิ่งคลิก (ผู้ใช้ 15 ต.ค. 2026) ----
    # อาการเดิม: คลิก textbox (.nm/.pr) ก่อน caret ค้างใน contenteditable → คลิกเส้นประ click handler เลือก .ln
    #           แต่ selectionchange ยิงตามด้วย caret ที่ค้าง → _typoFind(.nm) → typoSelect(.nm) แย่งเลือกทับ .ln
    # กัน: re-select ใน selectionchange ต้องมี guard !(_typoType && _typoType.line)
    _m68=re.search(r'_f\.el!==_typoEl[^\n{]*\)\{\s*typoSelect\(_f\.el', txt)
    if not _m68:
        errors.append('หา selectionchange re-select (_f.el!==_typoEl ... typoSelect) ไม่พบ — โครงสร้างเปลี่ยน ตรวจ lint #68 (ดู UI_STANDARD.md ข้อ 9)')
    elif '_typoType.line' not in _m68.group(0):
        errors.append('selectionchange re-select ขาด guard !(_typoType && _typoType.line) — คลิกเส้นจุดจาก textbox แล้วจะถูกแย่งเลือกทับ (ดู UI_STANDARD.md ข้อ 9)')

    # ---- 69) In-page zoom: ย่อ/ขยายเฉพาะหน้า A4 · toolbar ไม่โตตาม (ผู้ใช้ 16 ต.ค. 2026) ----
    # (a) apply rule ต้อง screen-only (อยู่ใน @media screen) + กันตอน measuring
    if '@media screen{ body:not(.measuring) .page{ zoom:var(--pagezoom,1); }' not in txt:
        errors.append('ไม่พบกฎ zoom หน้า A4 แบบ screen-only (@media screen{ body:not(.measuring) .page{ zoom:var(--pagezoom,1); }) — zoom ต้องไม่กระทบพิมพ์/ตอนวัดล้นหน้า (ดู UI_STANDARD.md ข้อ 10)')
    # (b) markup ปุ่ม zoom 3 ปุ่มในแถบบน
    if 'class="zoomctl"' not in txt:
        errors.append('ไม่พบ .zoomctl (ปุ่ม zoom แถบบน) (ดู UI_STANDARD.md ข้อ 10)')
    for _zid in ('id="zoomOut"','id="zoomLvl"','id="zoomIn"'):
        if _zid not in txt: errors.append('ไม่พบปุ่ม zoom '+_zid+' (ดู UI_STANDARD.md ข้อ 10)')
    # (c) ต้อง strip --pagezoom ออกตอนบันทึก ทั้ง buildEditorHtml + buildMenuHtml (เปิดไฟล์ครั้งหน้า = 100%)
    if txt.count("removeProperty('--pagezoom')") < 2:
        errors.append('build* ไม่ได้ strip --pagezoom ครบทั้ง 2 ที่ (buildEditorHtml + buildMenuHtml) — ไฟล์ที่บันทึกต้องไม่ติด zoom (ดู UI_STANDARD.md ข้อ 10)')
    # (d) i18n ttl.zoom* ครบ th+en
    _i69=txt.find('var I18N={')
    if _i69>=0:
        _th69=txt.find('th:{',_i69); _en69=txt.find('en:{',_i69)
        _thb69=txt[_th69:_en69] if (_th69>=0 and _en69>_th69) else ''
        _enb69=txt[_en69:_en69+30000] if _en69>=0 else ''
        for _k69 in ('ttl.zoomIn','ttl.zoomOut','ttl.zoomReset','ttl.zoomFit','ttl.zoomA4','zoom.a4','cal.title','cal.desc','cal.card','cal.startlbl','cal.endlbl','cal.save','cal.cancel','cal.a4is','cal.note','btn.cal','cal.inchdesc','cal.method1','cal.method2','cal.inchlbl','cal.reslbl','fl.a4Nominal'):
            if ("'"+_k69+"'") not in _thb69: errors.append('i18n '+_k69+' ขาดใน th (ดู UI_STANDARD.md ข้อ 10)')
            if ("'"+_k69+"'") not in _enb69: errors.append('i18n '+_k69+' ขาดใน en (ดู UI_STANDARD.md ข้อ 10)')
    # (e) ช่อง % (#zoomLvl) ต้องเป็น <input> พิมพ์ค่าเองได้ + มี _zoomType รับค่า (ผู้ใช้ 16 ต.ค. 2026)
    if 'id="zoomLvl"' in txt and not re.search(r'<input[^>]*id="zoomLvl"', txt):
        errors.append('#zoomLvl ต้องเป็น <input> (พิมพ์ % เองได้) ไม่ใช่ปุ่ม (ดู UI_STANDARD.md ข้อ 10)')
    if 'function _zoomType' not in txt:
        errors.append('ขาด function _zoomType (รับค่า % ที่พิมพ์ในช่อง zoomLvl) (ดู UI_STANDARD.md ข้อ 10)')
    # (f) ช่อง zoomLvl ต้องมี oninput filter กรองสดขณะพิมพ์ (ไม่ใช่แค่ whitelist — ผู้ใช้ 18 ต.ค. 2026) · ดู UI_STANDARD.md ข้อ 6.1
    _zt=re.search(r'<input[^>]*id="zoomLvl"[^>]*>', txt)
    if _zt and 'oninput="_zoomFilter' not in _zt.group(0):
        errors.append('#zoomLvl ไม่มี oninput="_zoomFilter" — ช่องตัวเลขต้องกรองสดขณะพิมพ์ (onchange กรองตอน blur ไม่พอ · ดู UI_STANDARD.md ข้อ 6.1)')
    if 'function _zoomFilter' not in txt or 'function _zoomClean' not in txt:
        errors.append('ขาด function _zoomFilter/_zoomClean (filter ตัวเลขช่อง zoom · ดู UI_STANDARD.md ข้อ 6.1)')
    # (g) ปุ่ม Fit / Fit Width (ผู้ใช้ 18 ต.ค. 2026) · ดู UI_STANDARD.md ข้อ 10
    for _zfid in ('id="zoomFit"','id="zoomA4"'):
        if _zfid not in txt: errors.append('ไม่พบปุ่ม zoom '+_zfid+' (Fit/Fit Width) (ดู UI_STANDARD.md ข้อ 10)')
    if 'zbtn zfitic' not in txt: errors.append('ปุ่ม Fit ต้องเป็นไอคอน (class zfitic · ไม่ใช้ข้อความยาว) (ดู UI_STANDARD.md ข้อ 10)')
    for _zfn in ('function zoomFitPage','function _pageFitMetrics'):
        if _zfn not in txt: errors.append('ขาด '+_zfn+' (คำนวณ zoom จากขนาดจอ) (ดู UI_STANDARD.md ข้อ 10)')
    # (h) A4 ปรับเทียบจอด้วยบัตร (ผู้ใช้ 18 ต.ค. 2026) · ดู UI_STANDARD.md ข้อ 10.2
    if 'id="calModal"' not in txt: errors.append('ขาด #calModal (ปรับเทียบจอด้วยบัตร) (ดู UI_STANDARD.md ข้อ 10.2)')
    if 'id="calInch"' not in txt: errors.append('ขาด #calInch (วิธีที่ 2: พิมพ์ขนาดจอนิ้ว · สูตร PPI) (ดู UI_STANDARD.md ข้อ 10.2)')
    for _calfn in ('function zoomA4','function openCal','function _calSave','function _calLoad','function _calFromInches'):
        if _calfn not in txt: errors.append('ขาด '+_calfn+' (A4 calibration) (ดู UI_STANDARD.md ข้อ 10.2)')
    if "'#calModal'," not in txt and "'#calModal']" not in txt: errors.append('calModal ไม่ถูก strip ใน buildMenuHtml (ดู UI_STANDARD.md ข้อ 10.2)')
    # (i) ปุ่ม A4 ต้องซูมทันที ไม่เปิด modal (ผู้ใช้ 18 ต.ค. 2026) · ปรับเทียบจอเปิดจากปุ่ม ปรับเทียบจอ (btnCal) เท่านั้น
    _z4lint=re.search(r'function zoomA4\([^)]*\)\{.*?\n', txt)
    if _z4lint and 'openCal(' in _z4lint.group(0):
        errors.append('zoomA4 ยังเรียก openCal — ปุ่ม A4 ต้องซูมทันที ไม่เปิด modal (ปรับเทียบจอเปิดจากปุ่ม ปรับเทียบจอ เท่านั้น · ดู UI_STANDARD.md ข้อ 10.2)')
    if 'fl.a4Nominal' not in txt:
        errors.append('ขาด i18n fl.a4Nominal — A4 ตอนยังไม่ปรับเทียบต้องแจ้งว่าเป็นค่าโดยประมาณ (กัน signifier หลอก · ดู UI_STANDARD.md ข้อ 10.2)')
    # (j) วิธีหลัก = พิมพ์นิ้ว ต้องมาก่อนทาบบัตร · %readout แยกจากปุ่ม −/+ (ผู้ใช้ 18 ต.ค. 2026)
    _ci18=txt.find('id="calInch"'); _cb18=txt.find('id="calBar"')
    if _ci18>=0 and _cb18>=0 and _ci18>_cb18:
        errors.append('ลำดับ modal ปรับเทียบจอผิด — ช่องพิมพ์นิ้ว (calInch) ต้องมาก่อนแถบทาบบัตร (calBar) · วิธีหลัก=พิมพ์นิ้ว ทาบบัตร=ตัวเลือก (ดู UI_STANDARD.md ข้อ 10.2)')
    if 'cal.inchdesc' not in txt:
        errors.append('ขาด i18n cal.inchdesc — คำอธิบายวิธีหลัก พิมพ์นิ้ว (ดู UI_STANDARD.md ข้อ 10.2)')
    # (k) openCal ต้องเรียก applyLang — modal อยู่หลัง editorScript ปิด init ไม่ถึง → เปิดครั้งแรกเห็น default สั้นไม่ตรง i18n (ผู้ใช้ 18 ต.ค. 2026)
    _oc69=re.search(r'function openCal\([^)]*\)\{.*?\n', txt)
    if _oc69 and 'applyLang(' not in _oc69.group(0):
        errors.append('openCal ไม่เรียก applyLang — เปิด modal ครั้งแรกจะเห็นข้อความ default สั้นไม่ตรง i18n (modal อยู่หลัง editorScript ปิด · ดู UI_STANDARD.md ข้อ 10.2)')
    # (l) แถบทาบบัตรต้องไม่ล้นกรอบ — barwrap overflow:hidden + _calSetWidth clamp ด้วย _calMaxWidth (ผู้ใช้ 18 ต.ค. 2026)
    if '#calModal .cal-barwrap{overflow:hidden' not in txt:
        errors.append('cal-barwrap ต้อง overflow:hidden — แถบทาบบัตรห้ามล้น/มี scrollbar (ดู UI_STANDARD.md ข้อ 10.2)')
    if 'function _calMaxWidth' not in txt:
        errors.append('ขาด _calMaxWidth — _calSetWidth ต้อง clamp ความกว้างแถบไม่ให้เกินกรอบ modal (ดู UI_STANDARD.md ข้อ 10.2)')
    # (m) แถบทาบบัตรแบบมาตรฐาน: เส้นเริ่ม/เส้นสิ้นสุดเป็นเส้นตรงชัดเจน · grip กึ่งกลางเส้นสิ้นสุด = จุดวัดจริง (ผู้ใช้ 18 ต.ค. 2026)
    if 'cal-startline' not in txt or 'cal-endline' not in txt:
        errors.append('แถบทาบบัตรต้องมีเส้นเริ่ม (cal-startline) + เส้นสิ้นสุด (cal-endline) เป็นเส้นตรงบอกจุดวางขอบซ้าย/ขวาบัตรชัดเจน (ดู UI_STANDARD.md ข้อ 10.2)')
    # (n) ปุ่มเปิด modal (btnCal) ต้องขึ้น active เขียว .on ระหว่างเปิด + ถอดตอนปิด — theme มาตรฐาน (ผู้ใช้ 18 ต.ค. 2026)
    if _oc69 and "getElementById('btnCal')" not in _oc69.group(0):
        errors.append('openCal ไม่ตั้ง .on ให้ btnCal — ปุ่มเปิด modal ต้องขึ้น active เขียวระหว่างเปิด (theme · ดู UI_STANDARD.md ข้อ 1/2)')
    _cc69n=re.search(r'function closeCal\([^)]*\)\{.*?\n', txt)
    if _cc69n and "classList.remove('on')" not in _cc69n.group(0):
        errors.append('closeCal ไม่ถอด .on ของ btnCal — ปิด modal แล้วปุ่มต้องเลิกเขียว (ดู UI_STANDARD.md ข้อ 1/2)')
    if '#edtabs #btnCal.on{' not in _css:
        errors.append('ขาด CSS #edtabs #btnCal.on (ปุ่มปรับเทียบจอ active เขียว) — ปุ่มเปิด modal ต้องเขียวระหว่างเปิด (ดู UI_STANDARD.md ข้อ 1)')
    # (o) จุดแสดง % (calPct) ต้องเป็น global อยู่บนสุด ไม่ซ่อนในวิธีใดวิธีหนึ่ง (ผู้ใช้ 18 ต.ค. 2026)
    if 'class="cal-result"' not in txt:
        errors.append('จุดแสดงผล % (calPct) ต้องอยู่ในกล่อง global cal-result บนสุด ไม่ซ่อนในวิธีที่ 1/2 (ดู UI_STANDARD.md ข้อ 10.2)')
    # (g) Ctrl/Cmd+scroll zoom-to-cursor + ตัวบอกหน้า/ซูมในแถบล่าง (ผู้ใช้ 20 ต.ค. 2026) ----
    if 'function _zoomWheel' not in txt or "addEventListener('wheel', _zoomWheel" not in txt:
        errors.append('ขาด Ctrl/Cmd+scroll zoom (_zoomWheel + wheel listener) (ดู UI_STANDARD.md ข้อ 10)')
    if 'function _zoomAtPoint' not in txt or 'function _pageAtClientY' not in txt:
        errors.append('ขาด zoom-to-cursor (_zoomAtPoint/_pageAtClientY) — Ctrl+scroll ต้องซูมเข้าตรงตำแหน่งเคอร์เซอร์ (ดู UI_STANDARD.md ข้อ 10)')
    if 'e.ctrlKey||e.metaKey' not in txt:
        errors.append('_zoomWheel ต้องทำงานเฉพาะเมื่อกด Ctrl/Cmd — ไม่งั้นเลื่อนล้อปกติจะซูมมั่ว (ดู UI_STANDARD.md ข้อ 10)')
    if 'id="edstatusPage"' not in txt or 'function _zoomMetaUpdate' not in txt:
        errors.append('ขาดตัวบอกหน้า/ซูมในแถบล่าง (#edstatusPage + _zoomMetaUpdate) (ดู UI_STANDARD.md ข้อ 10)')
    if "'st.pg'" not in txt:
        errors.append('ขาด i18n st.pg (ป้ายหน้าในตัวบอกสถานะ) (ดู UI_STANDARD.md ข้อ 10)')
    if '_ZGRID' not in txt or "classList.toggle('gridview', _zoom<=_ZGRID)" not in txt:
        errors.append('ขาดโหมดกริด (gridview) ตอนซูมออกต่ำ — ดูภาพรวมทุกหน้าแบบกริด (ผู้ใช้ 20 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 10)')
    if 'body.gridview:not(.presentmode){display:flex' not in _css:
        errors.append('ขาด CSS gridview (body.gridview flex-wrap grid) — ซูมออกต้องเรียงหน้าเป็นกริด (ดู UI_STANDARD.md ข้อ 10)')
    if "'focusmode','gridview'" not in txt or "'presentmode','gridview'" not in txt:
        errors.append('gridview ไม่ถูก strip ตอน save (editor+menu) — ไฟล์ที่บันทึกจะเปิดมาเป็นกริด (ดู UI_STANDARD.md ข้อ 10)')

    # ---- 75) default font ของเมนู = Prompt ที่ .page (ผู้ใช้ 18 ต.ค. 2026) ----
    #   ชื่อเมนู/หมายเหตุ/sub สืบทอดจาก .page · ตั้ง Prompt ที่ .page = เปลี่ยน default ทุกเมนูทุกหน้าในที่เดียว (ไม่แตะ UI editor)
    _pg75=re.search(r'\.page\{[^}]*\}', _css)
    if not _pg75 or "font-family:'Prompt'" not in _pg75.group(0):
        errors.append('.page ต้องตั้ง font-family:\'Prompt\' — default font ของเมนูทุกหน้า (ชื่อเมนู/หมายเหตุสืบทอดจาก .page · ดู UI_STANDARD.md ข้อ 6)')

    # ---- 77) แถบบน 2 โซน: [undo/redo · zoom+A4] ‖(.edbar-sep) [ขนาด UI · ภาษา] · ในโซน 8px · เส้นคั่นให้ boundary (ผู้ใช้ 23 ต.ค. 2026) ----
    #   ปรับเทียบจอ = caret ▾ ติด A4 (id=btnCal ยังอยู่) · โมโนโครม/นำเสนอ อยู่แท็บหน้าจอ · โซนในชิด 8px · ข้ามเส้นคั่น 14px
    for _s77, _need77, _msg77 in (
        ('#edtabs .zoomctl{', 'margin-left:8px', 'zoomctl (zoom · โซนเอกสาร) ชิด undo/redo 8px'),
        ('#edtabs .uiscalectl{', 'margin-left:0', 'uiscalectl หลังเส้นคั่น (margin-left:0 — เส้นคั่นให้ระยะแล้ว · ปุ่มซ่อนริบบอนย้ายไปมุมริบบอน 27 ต.ค. 2026)'),
        ('#edtabs .langsw{', 'margin-left:8px', 'langsw (TH/EN · โซนสภาพแวดล้อม) 8px'),
    ):
        _m77=re.search(re.escape(_s77)+r'[^}]*\}', _css)
        if _m77 and _need77 not in _m77.group(0):
            errors.append('ระยะแถบปุ่มบนไม่สม่ำเสมอ: '+_msg77+' (ดู UI_STANDARD.md ข้อ 1)')
    if re.search(r'#edtabs \.qab\{[^}]*margin-right:8px', _css):
        errors.append('#edtabs .qab ยังมี margin-right:8px เก่า — ระยะกลุ่มต้องคุมด้วย margin-left:16px ที่กลุ่มถัดไป ไม่ใช่ margin-right มั่ว (ดู UI_STANDARD.md ข้อ 1)')
    if '#edtabs .edbar-sep{' not in _css or 'class="edbar-sep"' not in txt:
        errors.append('แถบบนต้องมีเส้นคั่น 2 โซน (.edbar-sep): [undo/redo · zoom A4] ‖ [ขนาด UI · ภาษา] (ผู้ใช้ 23 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 1)')

    # ---- 80) โหมดนำเสนอ (present/fullscreen): 2 แกน Fit Width + Fit Screen (preset หน้า/จอ 1/2/3/4/6/8 โชว์ครบเสมอ · ตัวเกินจำนวนหน้า = disabled+tooltip · เอนจินเลือกกริดใหญ่สุด) · รองรับหลายจอ (จำค่าล่าสุด localStorage + เตือนจอเล็ก + เพดานสเกล ultrawide) · แถบลอย+คีย์ 1/2/3/4/6/8 · เฉพาะจอ · strip ตอน save (ผู้ใช้ 18-19 ต.ค. 2026) ----
    if 'function togglePresent' not in txt:
        errors.append('ขาด togglePresent — ปุ่มนำเสนอ (fullscreen) ใช้ไม่ได้ (ดู UI_STANDARD.md ข้อ 5)')
    if 'id="btnPresent"' not in txt:
        errors.append('ขาดปุ่ม btnPresent (นำเสนอ) (ดู UI_STANDARD.md ข้อ 5)')
    if "'btn.present'" not in txt:
        errors.append('ขาด i18n btn.present (ดู UI_STANDARD.md ข้อ 5)')
    if 'requestFullscreen' not in txt:
        errors.append('โหมดนำเสนอต้องเรียก requestFullscreen — ผู้ใช้เลือกเต็มจอ JS (ยอมรับปุ่มวงกลมออกเต็มจอของเบราว์เซอร์) 19 ต.ค. 2026 (ดู UI_STANDARD.md ข้อ 5)')
    if "addEventListener('fullscreenchange'" not in txt:
        errors.append('ขาด fullscreenchange listener — ออกจากเต็มจอด้วยปุ่มวงกลมเบราว์เซอร์ ต้องออกจากโหมดนำเสนอ (_presentExit) ด้วย (ดู UI_STANDARD.md ข้อ 5)')
    if 'function _presentFit' not in txt:
        errors.append('ขาด _presentFit — โหมดนำเสนอต้องย่อหน้าพอดีจอ (fit) ไม่ค้าง zoom เดิม (ดู UI_STANDARD.md ข้อ 5)')
    if "presentmode')) _presentFit();" not in txt:
        errors.append('_presentFit ไม่ถูกเรียกตอน resize — หน้าไม่ปรับพอดีเมื่อขนาดจอ/fullscreen เปลี่ยน (ดู UI_STANDARD.md ข้อ 5)')
    if "if(typeof _zoomApply==='function') _zoomApply();" not in txt:
        errors.append('ออกจากนำเสนอไม่คืน zoom เดิมด้วย _zoomApply (ดู UI_STANDARD.md ข้อ 5)')
    if "k==='Escape'){ e.preventDefault(); _presentExit(); }" not in txt:
        errors.append('ปุ่ม Esc ในโหมดนำเสนอต้องเรียก _presentExit ผ่าน keydown (ไม่พึ่ง fullscreenchange ของเบราว์เซอร์แล้ว) (ดู UI_STANDARD.md ข้อ 5)')
    # ---- โฟกัส (focus mode): ซ่อนริบบอน #edribbon ให้พื้นที่กว้างขึ้น · toggle จริง · strip ตอน save editor (ผู้ใช้ 19 ต.ค. 2026) ----
    if 'function toggleFocus' not in txt or 'id="btnFocus"' not in txt:
        errors.append('ขาดปุ่มโฟกัส (btnFocus/toggleFocus) — toggle ซ่อนแถบเครื่องมือให้พื้นที่กว้างขึ้น (ดู UI_STANDARD.md ข้อ 5)')
    if 'body.focusmode #edribbon' not in _css:
        errors.append('ขาด CSS body.focusmode #edribbon (ซ่อนริบบอนในโหมดโฟกัส) (ดู UI_STANDARD.md ข้อ 5)')
    # ---- canvas เทา + ช่องว่างหัวเพจ: หน้ากระดาษลอยบน canvas เทา เว้นจากริบบอน (editor-only · screen-only · ผู้ใช้ 20 ต.ค. 2026) ----
    #   อยู่ใน #editorUI (strip จากเมนูดาวน์โหลด) · presentmode override ทั้ง bg+margin จึงใช้ body:not(.presentmode)
    if 'body:not(.presentmode){background:#e9e6e1;}' not in _css:
        errors.append('ขาด canvas เทาหลังหน้ากระดาษในโหมดแก้ (body:not(.presentmode) background) — หน้ากระดาษควรลอยบน canvas ไม่ชนริบบอน (ดู UI_STANDARD.md ข้อ 1)')
    if 'body:not(.presentmode) .page{margin-top:20px;}' not in _css:
        errors.append('ขาดช่องว่างหัวเพจ (.page margin-top ในโหมดแก้) — หน้ากระดาษชนริบบอน (ดู UI_STANDARD.md ข้อ 1)')
    if "closest('#edtabs .edtab')" not in txt:
        errors.append('โหมดโฟกัสไม่มี auto-exit ตอนคลิกแท็บเครื่องมือ — คลิกแท็บแล้วริบบอนไม่โผล่ = คลิกตาย (ดู UI_STANDARD.md ข้อ 6)')
    if txt.count("'ttl.focusOn':'")<2:
        errors.append('ขาด i18n ttl.focusOn TH+EN (ชื่อปุ่มพับริบบอน · ปุ่มไม่มีตัวหนังสือ ใช้ title) (ดู UI_STANDARD.md ข้อ 5)')
    if 'data-tab="screen"' not in txt or "'tab.screen'" not in txt:
        errors.append('ขาดแท็บ หน้าจอ (data-tab="screen" + i18n tab.screen) (ดู UI_STANDARD.md ข้อ 5)')
    if 'data-pane="screen"' not in txt:
        errors.append('ขาด rpane หน้าจอ (data-pane="screen" รวมโมโนโครม+นำเสนอ) (ดู UI_STANDARD.md ข้อ 5)')
    if '#edtabs #btnBoard{' in _css or '#edtabs #btnPresent{' in _css:
        errors.append('โมโนโครม/นำเสนอ ต้องย้ายออกจาก #edtabs เข้าแท็บหน้าจอ (ribbon) — ไม่ควรเหลือ CSS #edtabs #btnBoard/#btnPresent (ดู UI_STANDARD.md ข้อ 5)')
    if "'imgmode','imghidden','boardmode','presentmode','focusmode'" not in txt:
        errors.append('focusmode ไม่ถูก strip ตอนบันทึก editor — เปิดไฟล์มาติดโหมดโฟกัส (ดู UI_STANDARD.md ข้อ 7)')

    # ---- 81) ลูกศรคีย์บอร์ดเลื่อนรูปที่เลือกในโหมดแก้รูป (ผู้ใช้ 20 ต.ค. 2026) ----
    #   รูป active (_imgSel) + imgmode → Arrow เลื่อน 1mm (Shift 5mm) · ต้อง guard imgmode+_imgSel · preventDefault (กันจอเลื่อน) · markDirty (มี undo) · _isLeft (รองรับ anchor right ไม่ให้เลื่อนกลับทาง)
    _ak = txt.find("if(k!=='ArrowUp'&&k!=='ArrowDown'&&k!=='ArrowLeft'&&k!=='ArrowRight')return;")
    if _ak < 0:
        errors.append('ขาด keydown ลูกศรเลื่อนรูป (ArrowUp/Down/Left/Right) ในโหมดแก้รูป (ดู UI_STANDARD.md ข้อ 5)')
    else:
        _akseg = txt[max(0,_ak-400):_ak+800]
        if 'imgmode' not in _akseg or '_imgSel' not in _akseg:
            errors.append('ลูกศรเลื่อนรูปต้อง guard ด้วย imgmode + _imgSel (ดู UI_STANDARD.md ข้อ 5)')
        if 'preventDefault' not in _akseg:
            errors.append('ลูกศรเลื่อนรูปต้อง preventDefault — กันหน้าจอเลื่อนตอนกดลูกศร (ดู UI_STANDARD.md ข้อ 5)')
        if 'markDirty' not in _akseg:
            errors.append('ลูกศรเลื่อนรูปต้องเรียก markDirty — ต้องมีจุด Undo (ดู UI_STANDARD.md ข้อ 6)')
        if '_isLeft' not in _akseg:
            errors.append('ลูกศรเลื่อนรูปต้องใช้ _isLeft เลือกแกน left/right — รูป anchor right จะเลื่อนกลับทาง (ดู UI_STANDARD.md ข้อ 6)')

    # ---- 82) พื้นหลังหน้า (page background): สี/รูป + ตัวหรี่ · เฉพาะหน้า/ทุกหน้า · เป็นเนื้อหา (ติดไฟล์+พิมพ์) · layer .pgbg ใน <style> ก้อนแรก (ผู้ใช้ 20 ต.ค. 2026) ----
    if 'id="btnPageBg"' not in txt or 'function openPageBgPanel' not in txt:
        errors.append('ขาดปุ่มพื้นหลัง (btnPageBg/openPageBgPanel) ในแท็บหน้า (ดู UI_STANDARD.md ข้อ 5)')
    if '.pgbg{' not in _css or '.pgbg::before' not in _css or 'opacity:calc(1 - var(--pgdim' not in _css:
        errors.append('ขาด CSS .pgbg / .pgbg::before หรือ dim รูป opacity:calc(1 - var(--pgdim)) บน .pgbgimg>img — layer ซ้อน (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    _pgcss = _css[_css.find('.pgbg{'):_css.find('.pgbg{')+400] if '.pgbg{' in _css else ''
    if 'print-color-adjust:exact' not in _pgcss:
        errors.append('.pgbg ต้องมี print-color-adjust:exact — พื้นหลังต้องพิมพ์ออกด้วย (ดู UI_STANDARD.md ข้อ 10.2)')
    if txt.count('<div class="pgbg"></div>') < 2:
        errors.append('ทุกหน้าต้องมีเลเยอร์ .pgbg (พบ < 2) (ดู UI_STANDARD.md ข้อ 5)')
    if '_bgPending' in txt or '_pgbgApplyPending' in txt:
        errors.append('ห้ามมี _bgPending/_pgbgApplyPending (โมเดล pending เก่า) — พื้นหลังเป็น instant: เลือกสี/รูป/จาง/ล้าง มีผลทันทีกับหน้าในขอบเขต (ผู้ใช้ 21 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    for _f82 in ('function _pageBgSetColor','function _pageBgSetImage','function _pageBgSetDim','function _pageBgClear','function _bgFlashScope'):
        if _f82 not in txt:
            errors.append('ขาด '+_f82+' (พื้นหลัง instant — ทาสีทันทีกับทุกหน้าในขอบเขต) (ผู้ใช้ 21 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if "'btn.pageBg'" not in txt or "'bg.scope'" not in txt:
        errors.append('ขาด i18n พื้นหลัง (btn.pageBg/bg.scope) (ดู UI_STANDARD.md ข้อ 5)')
    if 'id="pageBgInput"' not in txt:
        errors.append('ขาด #pageBgInput (hidden file input พื้นหลัง) (ดู UI_STANDARD.md ข้อ 5)')
    if '#secIconInput,#pageBgInput' not in txt:
        errors.append('buildMenuHtml ไม่ strip #pageBgInput — hidden input หลุดลงไฟล์เมนู (ดู UI_STANDARD.md ข้อ 6)')
    if '#edpanel .cp-pop{' not in _css or '#edpanel .cp-trigger{overflow:visible' not in _css:
        errors.append('ถาดสีพื้นหลังต้องมี box CSS ใน #edpanel (กฎ cp-* เดิม scope #typobar) + overflow:visible กัน popup โดน clip — ไม่งั้นถาดกางแบนเต็มแถบ (ผู้ใช้ 20 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if 'window._cpDlgOpen=_cpDlgOpen' not in txt or "window._cpDlgOpen('bg')" not in txt:
        errors.append('ปุ่มกำหนดเองพื้นหลังต้องเปิดหน้าต่าง HSV ตัวเดียวกับสีตัวหนังสือ (expose window._cpDlgOpen + เรียก (bg)) (ผู้ใช้ 20 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if "if(mode==='bg'){ _cpDlgClose();" not in txt:
        errors.append('_cpDlgOk ขาด branch mode bg — ตกลงในหน้าต่าง HSV ต้องทาสีพื้นหลัง (ดู UI_STANDARD.md ข้อ 5)')
    if 'id="bgCpPick"' not in txt or '#edpanel .cp-dlg{' not in _css:
        errors.append('ขาด host bgCpPick หรือ CSS หน้าต่าง HSV ใน #edpanel (mirror จาก #typobar) — หน้าต่างจะไม่ขึ้น/ไม่มีสไตล์ (ดู UI_STANDARD.md ข้อ 5)')
    if 'function _parsePageRange' not in txt or 'function _pageBgScopeIdx' not in txt:
        errors.append('ขาด _parsePageRange/_pageBgScopeIdx — เลือกหน้าแบบ print-style (คี่/คู่/ช่วง) (ผู้ใช้ 20 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if 'value="odd"' not in txt or 'value="even"' not in txt or 'value="range"' not in txt:
        errors.append('ขอบเขตพื้นหลังต้องมี คี่/คู่/ระบุช่วง (print-style) (ดู UI_STANDARD.md ข้อ 5)')
    if 'function _bgScopeApply' not in txt or "addEventListener('change',_bgScopeApply)" not in txt:
        errors.append('ขาด _bgScopeApply หรือ listener เปลี่ยนขอบเขต (scope radio change -> _bgScopeApply แสดง/ซ่อนช่องระบุ) (ดู UI_STANDARD.md ข้อ 5)')
    if 'function _bgReapply' not in txt or 'var _bgCur' not in txt or '_bgReapply(sc)' not in txt:
        errors.append('เปลี่ยนขอบเขตต้องทาสี/รูปปัจจุบันลงขอบเขตใหม่ทันที — _bgScopeApply ต้องเรียก _bgReapply + จำสีปัจจุบันใน _bgCur (ทุกการเปลี่ยนมีผลทันที ผู้ใช้ 21 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if "e.stopPropagation(); _closePop(); } }, true);" not in txt or "e.stopPropagation(); pop.classList.remove('open'); } }, true);" not in txt:
        errors.append('ถาดสี (typoCpPop/bgCpPop) ต้องปิดด้วย Esc ได้ — popover ทุกตัวต้องปิดได้ 2 ทาง: คลิกนอก + Esc (ผู้ใช้ 21 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if 'function _bgSelectPage' not in txt or 'var _bgSelPage' not in txt or '.page.pgcur{' not in _css:
        errors.append('พื้นหลังต้องคลิกเลือกหน้าได้ + ไฮไลท์หน้าที่เลือก (_bgSelPage/_bgSelectPage + .page.pgcur) — "เฉพาะหน้านี้" ตอน zoom out เห็นหลายหน้าต้องรู้/เลือกได้ว่าหน้าไหน · คลิก=เลือก+ไฮไลท์ ไม่ทาสี (ผู้ใช้ 21 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if 'function _pgbgImgOf' not in txt or '.pgbgimg{' not in _css or 'function _bgCoverBox' not in txt:
        errors.append('รูปพื้นหลังต้องเป็น element .pgbgimg (ไม่ใช่ CSS background): _pgbgImgOf + _bgCoverBox + CSS .pgbgimg — ลาก/ย่อ/ขยายด้วยมือเหมือน .fimg (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if 'window._bgDragBound' not in txt or "e.target.closest('.pgbgimg')" not in txt or 'body.pgbgmode' not in _css:
        errors.append('รูปพื้นหลังลาก/ย่อ/ขยายแบบ element: drag จับ .pgbgimg ใน body.pgbgmode (กดกลาง=ย้าย · ลากมุม .rz=ย่อ/ขยาย) (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if 'function _bgAddBox' not in txt or '_bgAddBox(im.naturalWidth' not in txt or 'var FILL=90' not in txt:
        errors.append('ตอน add รูปพื้นหลัง ต้องคำนวณขนาดเริ่มด้วย _bgAddBox — fit ภายใน 90% ของหน้า (var FILL=90) เว้นขอบทั้ง 4 ด้าน เพื่อเห็นกรอบรูป + ใช้ปุ่ม resize ที่มุมได้ทันที (รูปใหญ่กว่าหน้าก็ไม่ชนขอบ · ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if '#edbar #btnPageBg.on' not in _css or '#edbar #btnBoard.on' not in _css or '#edbar #btnPresent.on' not in _css:
        errors.append('ปุ่ม ribbon (พื้นหลัง/โมโนโครม/นำเสนอ) ต้องมี rule เขียว #edbar #<id>.on — .b-lg.on ถูก #edbar .b-lg{background:none} ทับ (ปุ่ม ribbon active/เปิดพาเนลทุกปุ่มต้องเขียวตาม pattern) (ดู UI_STANDARD.md ข้อ 1)')
    if "noOutsideClose:true, toggleBtn:'btnPageBg'" not in txt:
        errors.append('พาเนลพื้นหลังต้อง noOutsideClose:true — ปิดด้วยกดปุ่มพื้นหลังซ้ำเท่านั้น ไม่ใช่คลิกที่หน้า (งานยังไม่เสร็จ ไม่ควรปิดเอง · ผู้ใช้ 20 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    _swt = txt[txt.find('function switchTab(name){'):txt.find('function switchTab(name){')+600] if 'function switchTab(name){' in txt else ''
    if "!_ep.classList.contains('ep-hidden')" not in _swt or 'closePanel()' not in _swt:
        errors.append('switchTab ต้องปิด panel ที่เปิดอยู่เมื่อสลับแท็บ (closePanel เมื่อ #edpanel ไม่ใช่ ep-hidden) — panel ผูกกับแท็บที่เปิดมัน ครอบคลุมทุก panel (ผู้ใช้ 20 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3)')
    if 'if(opts.noOutsideClose) return; e.preventDefault(); closePanel();' not in txt:
        errors.append('_panelKey (Esc ของ openPanel) ต้อง guard opts.noOutsideClose — โหมดค้าง (noOutsideClose เช่น พื้นหลัง/ปรับราคา) Esc ต้องไม่ปิดโหมด — ปิดด้วยกดปุ่มซ้ำ/สลับแท็บเท่านั้น (ผู้ใช้ 21 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if 'opts.hideOk' not in txt:
        errors.append('openPanel ต้องรองรับ hideOk — พาเนล toggle ปิดด้วยกดปุ่มซ้ำ/คลิกนอก ไม่ต้องมีปุ่มเสร็จซ้ำซ้อน (ผู้ใช้ 20 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if "okKey:'bg.apply'" in txt or 'onOk:_pageBgApplyScope' in txt:
        errors.append('พื้นหลังต้องไม่มีปุ่มนำไปใช้ (okKey bg.apply/onOk) — instant: ทาทันทีเมื่อเลือกสี/รูป/จาง/ล้าง (ผู้ใช้ 21 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if 'onchange="_bgDimCommit(+this.value)"' not in txt or 'function _bgDimCommit' not in txt:
        errors.append('สไลเดอร์ความจางต้อง live ขณะลาก (_bgDimLive ทุกหน้าในขอบเขต) + commit ทั้งขอบเขตตอนปล่อย (onchange _bgDimCommit) — real-time ทุกหน้าในขอบเขต ไม่ใช่เฉพาะหน้าแรก (ผู้ใช้ 21 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if 'function _bgApply(col){' not in txt or '_pageBgSetColor(_pageBgScope(), col)' not in txt:
        errors.append('_bgApply ต้องทาสีทันที (_pageBgSetColor ตามขอบเขต) ไม่ใช่ตั้ง pending (ผู้ใช้ 21 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    # ---- 83) ถาดสีพื้นหลัง = ถาดสีกลาง (cp-* เดียวกับสีตัวหนังสือ) · ใช้ SWATCHES ร่วม + custom localStorage คีย์เดียวกัน · จำสีปัจจุบันตอนเปิด · ห้าม native color picker (ผู้ใช้ 20 ต.ค. 2026) ----
    if 'id="bgCpPop"' not in txt or 'id="bgCpGrid"' not in txt:
        errors.append('พื้นหลังต้องใช้ถาดสีกลาง (bgCpPop/bgCpGrid คลาส cp-*) ไม่ใช่ native color picker (ดู UI_STANDARD.md ข้อ 5)')
    if 'window._cpSwatches=SWATCHES' not in txt:
        errors.append('ถาดสีพื้นหลังต้องใช้ SWATCHES ร่วม (expose window._cpSwatches) — ไม่ hardcode จานสีซ้ำ (ดู UI_STANDARD.md ข้อ 5)')
    if 'function _bgWirePalette' not in txt or '_bgWirePalette();' not in txt:
        errors.append('ขาด _bgWirePalette (สร้าง/เดินสายถาดสีพื้นหลังตอนเปิด panel) (ดู UI_STANDARD.md ข้อ 5)')
    if "localStorage.getItem('oe_custom_swatches')" not in txt:
        errors.append('ถาดสีพื้นหลังต้องอ่านสีกำหนดเองจาก localStorage คีย์เดียวกับสีตัวหนังสือ (oe_custom_swatches) (ดู UI_STANDARD.md ข้อ 5)')
    # ---- 84) พื้นหลัง layer ซ้อน: สี=ชั้นล่าง (.pgbg::before) + รูป=ลอยทับ · ใส่ก่อน/หลังได้ทั้งคู่ไม่ลบกัน · แยกความจางสี/รูป (ผู้ใช้ 22 ต.ค. 2026) ----
    _fsc = txt[txt.find('function _pageBgSetColor'):txt.find('function _pageBgSetColor')+420] if 'function _pageBgSetColor' in txt else ''
    if '.pgbgimg' in _fsc or 'w.remove()' in _fsc:
        errors.append('_pageBgSetColor ห้ามลบรูป — layer ซ้อน (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    _fsi = txt[txt.find('function _pageBgSetImage'):txt.find('function _pageBgSetImage')+520] if 'function _pageBgSetImage' in txt else ''
    if 'backgroundColor=' in _fsi:
        errors.append('_pageBgSetImage ห้ามล้างสีพื้น — layer ซ้อน (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if 'function _pageBgSetColorAlpha' not in txt or 'function _bgColorDimCommit' not in txt or 'onchange="_bgColorDimCommit(+this.value)"' not in txt:
        errors.append('ขาดสไลเดอร์ความจางสี (_pageBgSetColorAlpha + _bgColorDimCommit + slider) (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if "'bg.colorDim'" not in txt:
        errors.append('ขาด i18n bg.colorDim (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if "setProperty('--pgcolor'" not in txt or "setProperty('--pgcoloralpha'" not in txt:
        errors.append('สีพื้นต้องเก็บใน --pgcolor + --pgcoloralpha (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if "getAttribute('data-bgcolor')" not in txt or "getAttribute('data-bgimage')" not in txt:
        errors.append('พื้นหลังต้องแยก flag data-bgcolor/data-bgimage (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    # ---- 85) ความจางกลุ่มเมนู (semi-transparent panel) ต่อหน้า: .sec/.sec-h พื้น rgba(var --secalpha) + slider แยก + i18n (ผู้ใช้ 22 ต.ค. 2026) ----
    if '--secalpha' not in _css:
        errors.append('กลุ่มเมนูต้องรองรับกึ่งโปร่งใส: .sec/.sec-h พื้นเป็น rgba(...,var(--secalpha)) เพื่อเห็นพื้นหลังลอด ตัวอักษรทึบเสมอ (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if "setProperty('--secalpha'" not in txt or 'function _pageBgSetSecAlpha' not in txt:
        errors.append('ขาด _pageBgSetSecAlpha (ตั้ง --secalpha ต่อหน้าตามขอบเขต) — ความจางกลุ่มเมนูต่อหน้า (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if 'function _bgSecDimCommit' not in txt or 'onchange="_bgSecDimCommit(+this.value)"' not in txt or 'function _bgSecDimLive' not in txt:
        errors.append('ขาดสไลเดอร์ความจางกลุ่มเมนู (_bgSecDimLive live + _bgSecDimCommit commit ตามขอบเขต) (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if "'bg.menuDim'" not in txt:
        errors.append('ขาด i18n bg.menuDim (ความจางกลุ่มเมนู) (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    # ---- 86) รูปพื้นหลังเลื่อนตำแหน่งด้วยปุ่มลูกศร (เหมือน .fimg) ตอน pgbgmode + เลือกรูป (ผู้ใช้ 22 ต.ค. 2026) ----
    if 'window._bgNudgeBound' not in txt:
        errors.append('รูปพื้นหลังต้องเลื่อนตำแหน่งด้วยปุ่มลูกศรได้เหมือนรูปพื้นหน้า (.fimg) — ขาด window._bgNudgeBound (keydown nudge ตอน pgbgmode เลือกรูปพื้นหลัง · 1mm/Shift 5mm · reapply ตามขอบเขต) (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    # ---- 87) ซ่อนเนื้อหาต่อหน้า (ตาม scope) บนจอ: .page.pgcontenthide > *:not(.pgbg) · ปุ่มในพาเนลพื้นหลัง · เคารพ scope เหมือนสี/รูป/ความจาง · เฉพาะจอ ไม่กระทบพิมพ์/บันทึก/undo (ผู้ใช้ 22 ต.ค. 2026) ----
    if '.page.pgcontenthide' not in _css or ':not(.pgbg)' not in _css:
        errors.append('ขาด CSS .page.pgcontenthide > *:not(.pgbg) — ซ่อนเนื้อหาต่อหน้า (ตาม scope) เหลือพื้นหลัง (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 3.1)')
    if 'body.pgcontenthide' in _css:
        errors.append('ห้ามใช้ body.pgcontenthide (ซ่อนทั้งเอกสาร) — ต้องเป็น .page.pgcontenthide ต่อหน้าตาม scope: เลือก "เฉพาะหน้านี้" ต้องซ่อนเฉพาะหน้าที่เลือก ไม่ใช่ทุกหน้า (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 6)')
    if 'function togglePgContentHide' not in txt or 'id="btnPgContentHide"' not in txt or 'function _pgContentHideSync' not in txt:
        errors.append('ขาดปุ่มซ่อนเนื้อหา (btnPgContentHide + togglePgContentHide + _pgContentHideSync) ในพาเนลพื้นหลัง (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    _ftg = txt[txt.find('function togglePgContentHide'):txt.find('function togglePgContentHide')+500] if 'function togglePgContentHide' in txt else ''
    if '_pageBgTargets' not in _ftg:
        errors.append('togglePgContentHide ต้องซ่อนตาม scope (_pageBgTargets) ไม่ใช่ทั้ง body — "เฉพาะหน้านี้" ต้องซ่อนเฉพาะหน้าที่เลือก (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 6)')
    _fsy = txt[txt.find('function _pgContentHideSync'):txt.find('function _pgContentHideSync')+400] if 'function _pgContentHideSync' in txt else ''
    if '_pageBgTargets' not in _fsy:
        errors.append('_pgContentHideSync ต้องเช็คสถานะปุ่มตาม scope (_pageBgTargets) — ปุ่ม on/off ตรงกับหน้าในขอบเขต (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 6)')
    if "remove('pgcontenthide')" not in txt:
        errors.append('ปิดพาเนลพื้นหลัง (_bgSelClear) ต้อง reset .pgcontenthide ทุกหน้า — ไม่ค้างซ่อนหลังออกจากโหมด (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if txt.count(".page.pgcontenthide')") < 3:
        errors.append('ต้อง strip .page.pgcontenthide ทั้งใน snapshot (_serializePages) + save (cleanForSave + buildMenuHtml) — สถานะซ่อน (view) ไม่ติดไฟล์/undo (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 6)')
    _fsp = txt[txt.find('function _bgSelectPage'):txt.find('function _bgSelectPage')+500] if 'function _bgSelectPage' in txt else ''
    if '_pgContentHideSync' not in _fsp:
        errors.append('_bgSelectPage (คลิกเลือกหน้า) ต้องเรียก _pgContentHideSync — scope "เฉพาะหน้านี้" เปลี่ยนหน้า=เปลี่ยนเป้าหมายปุ่มซ่อนเนื้อหา ปุ่มต้อง sync ตามหน้าใหม่ ไม่งั้นปุ่มบอกสถานะผิด (signifier หลอก ข้อ 6) (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 6)')
    if '#edpanel .ep-mini.on{background:#217346' not in _css:
        errors.append('ปุ่ม toggle ในพาเนล (.ep-mini ที่สลับ .on เช่น ซ่อนเนื้อหา) ต้องเป็นสีเขียว #217346 ตอน active — ทุกปุ่มที่ "เปิดอยู่/ทำงานอยู่" ต้องเขียวตามมาตรฐาน (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 1)')
    if "'bg.hideContent'" not in txt or "'bg.showContent'" not in txt:
        errors.append('ขาด i18n bg.hideContent/bg.showContent (ปุ่มซ่อน/แสดงเนื้อหา) (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    # ---- 88) สไลเดอร์ความจางทั้ง 3 (รูป/สี/กลุ่มเมนู) ต้อง live ทุกหน้าในขอบเขต real-time ไม่ใช่เฉพาะหน้าแรก (ผู้ใช้ 22 ต.ค. 2026) ----
    for _lf88 in ('_bgDimLive','_bgColorDimLive','_bgSecDimLive'):
        _seg88 = txt[txt.find('function '+_lf88):txt.find('function '+_lf88)+320] if ('function '+_lf88) in txt else ''
        if '_pageBgTargets' not in _seg88 or '.forEach' not in _seg88:
            errors.append(_lf88+' ต้อง live ทุกหน้าในขอบเขต (_pageBgTargets(...).forEach) ไม่ใช่เฉพาะหน้าแรก t[0] — เลื่อน slider ต้องเห็นผล real-time ทุกหน้าที่เลือก (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
        if 't&&t[0]' in _seg88 or 't[0]' in _seg88:
            errors.append(_lf88+' ยังใช้ t[0] (หน้าแรกอย่างเดียว) — ต้อง loop ทุกหน้าในขอบเขต (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    # ---- 89) เพิ่มหน้า: panel กรอกจำนวน 1-20/ครั้ง + batch DocumentFragment + เตือน ~200 + ปุ่ม active เขียว (ผู้ใช้ 22 ต.ค. 2026) ----
    _fap = txt[txt.find('function addPage('):txt.find('function addPage(')+120] if 'function addPage(' in txt else ''
    if '_addPagesBatch(1)' not in _fap:
        errors.append('ปุ่มเพิ่มหน้าหลัก (addPage) ต้องเพิ่ม 1 หน้าทันที (_addPagesBatch(1)) ไม่เปิด panel — เคสปกติกดครั้งเดียวจบ (ผู้ใช้ 22 ต.ค. 2026 · ตรง InDesign New Page) (ดู UI_STANDARD.md ข้อ 5)')
    _fapm = txt[txt.find('function openAddPagesPanel('):txt.find('function openAddPagesPanel(')+600] if 'function openAddPagesPanel(' in txt else ''
    if 'openPanel' not in _fapm:
        errors.append('ปุ่ม caret เพิ่มหลายหน้า (openAddPagesPanel) ต้องเปิด panel กรอกจำนวน (openPanel prompt) แยกจากปุ่มหลัก (ผู้ใช้ 22 ต.ค. 2026 · ตรง InDesign Insert Pages) (ดู UI_STANDARD.md ข้อ 5)')
    if 'id="btnAddPageMore"' not in txt or 'class="addpage-caret"' not in txt:
        errors.append('ขาดปุ่ม caret เพิ่มหลายหน้า (btnAddPageMore / .addpage-caret) ข้างปุ่มเพิ่มหน้า — split button ตรง InDesign (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if 'function _addPagesBatch' not in txt or 'createDocumentFragment' not in txt:
        errors.append('เพิ่มหลายหน้าต้อง batch ด้วย DocumentFragment (_addPagesBatch) — clone N หน้าทีเดียว เรียก renumber/decorate/checkOverflow/_snapNow ครั้งเดียวตอนจบ (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if "'pnl.addPageLabel'" not in txt or "'pnl.addPagePreview'" not in txt or "'pnl.addPageMax'" not in txt or "'pnl.addPageWarn'" not in txt:
        errors.append('ขาด i18n เพิ่มหน้า (pnl.addPageLabel/addPagePreview/addPageMax/addPageWarn) (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if "'pnl.addPageSuf'" not in txt or 'ep-suffix' not in txt or 'suffixKey' not in txt:
        errors.append('panel เพิ่มหลายหน้าต้องเป็น "เพิ่ม [จำนวน] หน้า" — label (pnl.addPageLabel) นำหน้าช่อง + suffix (pnl.addPageSuf/.ep-suffix) ต่อท้ายช่อง ผ่าน openPanel suffixKey (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if '#edbar #btnAddPageMore.on' not in _css:
        errors.append('ปุ่ม caret เพิ่มหลายหน้า (btnAddPageMore) ตอนเปิด panel ต้องเขียว #217346 — ต้องมี #edbar #btnAddPageMore.on ตามกฎปุ่ม active เขียว ข้อ 11 (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 1)')
    # ---- 90) toolbar/ribbon/panel โทน info ไม่มี icon — info=เครื่องมือทำงาน ไม่ใช่ alert · เป็น DEFAULT ของ openPanel (ไม่ใช่ใส่ hideIcon ทีละ panel) → toolbar ใหม่ไม่มี icon อัตโนมัติ ไม่ต้องจำเพิ่ม/ถอด · icon เหลือเฉพาะ warn/danger (ผู้ใช้ 22 ต.ค. 2026) ----
    if "(opts.hideIcon||tone==='info')" not in txt:
        errors.append('openPanel ต้องซ่อน icon เมื่อ tone info เป็น default (var html=(opts.hideIcon||tone===info)?...) — toolbar/ribbon โทน info ห้ามมี icon info, ให้เป็น default ไม่ใช่ใส่ hideIcon ทีละ panel (toolbar ใหม่ไม่ต้องจำ) · icon เหลือเฉพาะ alert warn/danger (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 6)')
    if 'ep-ic' in txt and "tone==='info'" not in txt[txt.find('class="ep-ic"')-120:txt.find('class="ep-ic"')+10]:
        errors.append('guard icon (.ep-ic) ต้องผูกกับ tone!==info — ห้าม render icon บน panel โทน info (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 6)')
    # ---- 91) ปรับขนาด UI chrome (toolbar) แยกจากซูมเพจ: zoom บน #edbar/#edstatus เท่านั้น ห้ามแตะ .page (กันซูมซ้อนซูมกับ --pagezoom) · ปุ่ม A−/A+ บน toolbar (ผู้ใช้ 22 ต.ค. 2026) ----
    if 'id="uiIn"' not in txt or 'id="uiOut"' not in txt or 'function _uiscaleApply' not in txt or 'function _uiscaleLoad' not in txt:
        errors.append('ขาดปุ่มปรับขนาด UI (uiIn/uiOut + _uiscaleApply/_uiscaleLoad) บน toolbar (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if '#edbar{zoom:var(--uiscale' not in _css or '#edstatus{zoom:var(--uiscale' not in _css or '#actlog{zoom:var(--uiscale' not in _css:
        errors.append('--uiscale ต้อง zoom chrome ครบ #edbar + #edstatus + #actlog (ประวัติเป็น chrome ขยายตาม UI scale ด้วย) (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if 'zoom:var(--uiscale' in _css.replace('#edbar{zoom:var(--uiscale,1);}','').replace('#edstatus{zoom:var(--uiscale,1);}','').replace('#actlog{zoom:var(--uiscale,1);}',''):
        errors.append('--uiscale ห้าม zoom element อื่นนอกจาก chrome (#edbar/#edstatus/#actlog) — โดยเฉพาะ .page จะซ้อนกับ --pagezoom ซูมซ้อนซูม (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if 'UISCALE_KEY' not in txt or 'localStorage.getItem(UISCALE_KEY' not in txt:
        errors.append('ขนาด UI ต้องจำค่าใน localStorage (UISCALE_KEY) (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if "'ttl.uiOut'" not in txt or "'ttl.uiIn'" not in txt:
        errors.append('ขาด i18n ปุ่มขนาด UI (ttl.uiOut/ttl.uiIn) (ผู้ใช้ 22 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    # ---- 92) #edbar = sticky (ไม่ fixed) → เลื่อนตาม scroll แนวนอนตอนจอแคบ ปุ่มขวาเข้าถึงครบ + อยู่ใน flow กินที่เอง · body/#edbar min-width:960 กันเนื้อหาหด/หายตอนจอแคบ (ผู้ใช้ 23 ต.ค. 2026) ----
    _eb92=re.search(r'#edbar\{[^}]*\}', _css)
    if not _eb92 or 'position:sticky' not in _eb92.group(0):
        errors.append('#edbar ต้อง position:sticky (ไม่ใช่ fixed) — เลื่อนตาม scroll แนวนอนตอนจอแคบ ปุ่มขวาเข้าถึงได้ + อยู่ใน flow กินที่เอง (เลิก fixed+syncBarHeight paddingTop hack) (ผู้ใช้ 23 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 7)')
    if not _eb92 or 'min-width:960px' not in _eb92.group(0):
        errors.append('#edbar ต้องมี min-width:960px — toolbar ไม่ wrap/หดตอนจอแคบ (ผู้ใช้ 23 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 7)')
    _bd92=re.search(r'(?<![.\w])body\{[^}]*background:#e8e2d9[^}]*\}', _css)
    if not _bd92 or 'min-width:960px' not in _bd92.group(0):
        errors.append('body ต้องมี min-width:960px — จอแคบกว่านี้ scroll แนวนอน เนื้อหาไม่หด/หาย (ผู้ใช้ 23 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 7)')
    if re.search(r'function syncBarHeight\([^)]*\)\{[^}]*?style\.paddingTop', txt):
        errors.append('syncBarHeight ต้องไม่ตั้ง body paddingTop — #edbar เป็น sticky อยู่ใน flow กินที่เอง (ผู้ใช้ 23 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 7)')
    if 'display:grid !important' not in _css or 'grid-template-columns:repeat(var(--pcols' not in _css:
        errors.append('โหมดนำเสนอไม่ได้ใช้ grid หลายคอลัมน์ (body.presentmode ต้อง display:grid + grid-template-columns repeat(var(--pcols)) ) (ดู UI_STANDARD.md ข้อ 5)')
    if 'grid-auto-rows:var(--prowh' not in _css or 'align-items:center !important' not in _css:
        errors.append('โหมดนำเสนอขาด grid-auto-rows:var(--prowh) + align-items:center — แถวจะไม่สูงเท่าจอ ทำให้แถวถัดไปโผล่ขึ้นมา (3/4 หน้าเพี้ยน) (ดู UI_STANDARD.md ข้อ 5)')
    if "setProperty('--prowh'" not in txt:
        errors.append('_presentFit ไม่ได้ตั้ง --prowh (ความสูงแถว = จอ/จำนวนแถว) — Fit Screen จะมีแถวถัดไปโผล่กันไม่พอดีจอ (ดู UI_STANDARD.md ข้อ 5)')
    if 'rowsPer=g.rows' not in txt:
        errors.append('_presentFit ไม่ได้ใช้จำนวนแถวจาก _presentBestGrid (rowsPer) คุมความสูงแถว (ดู UI_STANDARD.md ข้อ 5)')
    if 'cols*pw' not in txt:
        errors.append('_presentFit ไม่ได้คำนวณ fit ตามจำนวนคอลัมน์ (ต้องหาร cols*pw) — หลายคอลัมน์จะล้นจอ (ดู UI_STANDARD.md ข้อ 5)')
    if ('gap:20px !important' in _css) != ('gap=20' in txt):
        errors.append('ค่า gap ของโหมดนำเสนอใน CSS กับ JS ไม่ตรงกัน — fit จะคลาด (ดู UI_STANDARD.md ข้อ 5)')
    if 'function _presentApply' not in txt or 'function _presentBuildBar' not in txt:
        errors.append('ขาด _presentApply/_presentBuildBar — แถบเลือกโหมดนำเสนอใช้ไม่ได้ (ดู UI_STANDARD.md ข้อ 5)')
    if "bar.id='presentBar'" not in txt:
        errors.append('ขาดการสร้างแถบลอย #presentBar (ดู UI_STANDARD.md ข้อ 5)')
    if '_presentSetK(parseInt(k' not in txt:
        errors.append('ขาดคีย์ลัด 1/2/4/6/9 เลือกจำนวนหน้า/จอในโหมดนำเสนอ (ดู UI_STANDARD.md ข้อ 5)')
    if 'function _presentKPresets' not in txt:
        errors.append('ขาด _presentKPresets — จำนวนหน้า/จอไม่ปรับตามจำนวนหน้า (ดู UI_STANDARD.md ข้อ 5)')
    if '_presentView' not in txt or 'function _presentToggleWidth' not in txt:
        errors.append('ขาดโหมด Fit Width (เลื่อนอ่านเต็มกว้าง) หรือคีย์ W (ดู UI_STANDARD.md ข้อ 5)')
    if "'pres.fitWidth'" not in txt:
        errors.append('ขาด i18n pres.fitWidth (ปุ่มเต็มกว้าง) (ดู UI_STANDARD.md ข้อ 5)')
    if 'function _presentBestGrid' not in txt:
        errors.append('ขาด _presentBestGrid — เอนจินเลือกกริดหน้าใหญ่สุดต่อ K หน้า/จอ (ดู UI_STANDARD.md ข้อ 5)')
    if 'function _presentWarn' not in txt:
        errors.append('ขาด _presentWarn — จอเล็กต้องเตือนตัวเล็กอาจอ่านยาก (ดู UI_STANDARD.md ข้อ 5)')
    if "'oe_present_k'" not in txt or 'function _presentLoad' not in txt:
        errors.append('ขาดการจำค่า view/จำนวนหน้าล่าสุด (localStorage oe_present_k + _presentLoad) — เปิดจอเดิมต้องได้ค่าเดิม (ดู UI_STANDARD.md ข้อ 5)')
    if "'pres.small'" not in txt:
        errors.append('ขาด i18n pres.small (ป้ายเตือนจอเล็ก) (ดู UI_STANDARD.md ข้อ 5)')
    if '.pb-warn' not in _css:
        errors.append('ขาด CSS .pb-warn (ป้ายเตือนจอเล็ก) (ดู UI_STANDARD.md ข้อ 6)')
    if 'return [1,2,3,4,6,8,12,16];' not in txt:
        errors.append('preset หน้า/จอ ต้องเป็นชุด 1/2/3/4/6/8/12/16 ครบเสมอ (เพดาน 16 ตามมาตรฐาน N-up · ไม่กรองตามจำนวนหน้า) (ดู UI_STANDARD.md ข้อ 5)')
    if "lab.className='pb-ico'" not in txt or '#presentBar .pb-ico' not in _css:
        errors.append('ป้ายจำนวนหน้า/จอ ต้องเป็นไอคอน grid (.pb-ico) ไม่ใช่คำว่าหน้าต่อจอ (ตามธรรมเนียม viewer บนจอ) (ดู UI_STANDARD.md ข้อ 5/6)')
    if "xb.className='pb-exit'" not in txt or '#presentBar .pb-exit' not in _css:
        errors.append('แถบลอยนำเสนอต้องมีปุ่มออก ✕ (.pb-exit) ของตัวเอง — ไม่พึ่งปุ่มออกเต็มจอของเบราว์เซอร์ (ตามมาตรฐาน PowerPoint/Acrobat) (ดู UI_STANDARD.md ข้อ 5/6)')
    if 'xb.onclick=function(){ _presentExit(); }' not in txt:
        errors.append('ปุ่มออก ✕ ในแถบลอยไม่ได้ wired _presentExit (ดู UI_STANDARD.md ข้อ 5)')
    if "'pres.exit'" not in txt:
        errors.append('ขาด i18n pres.exit (tooltip ปุ่มออกนำเสนอ) (ดู UI_STANDARD.md ข้อ 5)')
    if 'e.clientY>=window.innerHeight-_PRES_HOTZONE' not in txt or 'var _PRES_HOTZONE' not in txt:
        errors.append('แถบลอยนำเสนอต้องโผล่เฉพาะ hot zone ขอบล่าง (mousemove เช็ค e.clientY>=window.innerHeight-_PRES_HOTZONE) — ย้ายลงล่างหนีปุ่มวงกลมปิดเต็มจอของเบราว์เซอร์ที่อยู่บนเสมอ · ผู้ใช้ 19 ต.ค. 2026 (ดู UI_STANDARD.md ข้อ 5)')
    if 'function _presentBarHideSoon' not in txt or 'else { _presentBarHideSoon(); }' not in txt:
        errors.append('แถบลอยนำเสนอต้องซ่อนทันทีเมื่อเมาส์ออกจากเขตบน (hide-on-leave หน่วง ~400ms ผ่าน _presentBarHideSoon) — ไม่ให้คนใจร้อนต้องรอ 2.8 วิ (ผู้ใช้ 19 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if '_PRES_GRACE' not in txt or '_presentGrace=true;' not in txt:
        errors.append('ตอนเข้าโหมดนำเสนอครั้งแรก แถบกริดต้องค้าง grace (_PRES_GRACE ~4 วิ) โดยไม่ถูกซ่อนด้วย hide-on-leave/auto-hide — ให้ผู้ใช้ใหม่สังเกตเห็นแถบทัน (ผู้ใช้ 19 ต.ค. 2026) (ดู UI_STANDARD.md ข้อ 5)')
    if 'if(!_presentGrace){ _presentIdleT=setTimeout' not in txt or 'function _presentBarHideSoon(){ if(_presentGrace) return;' not in txt:
        errors.append('grace ตอนเข้าโหมดต้องบล็อกทั้ง auto-hide (2.8 วิ) และ hide-on-leave (0.4 วิ) — ไม่งั้นแถบหายก่อนผู้ใช้ทันเห็น (ดู UI_STANDARD.md ข้อ 5)')
    if "else { b.disabled=true; b.setAttribute('data-i18n-title','pres.kNeed');" not in txt:
        errors.append('ปุ่ม preset ที่เกินจำนวนหน้าต้อง disabled + tooltip pres.kNeed (โชว์ครบแต่กดไม่ได้ ไม่ซ่อน) (ดู UI_STANDARD.md ข้อ 5)')
    if "'pres.kNeed'" not in txt:
        errors.append('ขาด i18n pres.kNeed (tooltip ปุ่มที่ยังใช้ไม่ได้ ต้องบอกเหตุผล) (ดู UI_STANDARD.md ข้อ 5)')
    if '#presentBar button:disabled' not in _css:
        errors.append('ขาด CSS #presentBar button:disabled (ปุ่มที่ใช้ไม่ได้ต้องดูต่างจากปุ่มปกติ · signifier ซื่อสัตย์) (ดู UI_STANDARD.md ข้อ 6)')
    if "'#calModal','#presentBar']" not in txt:
        errors.append('buildMenuHtml ไม่ strip #presentBar — แถบลอยหลุดลงไฟล์เมนู (ดู UI_STANDARD.md ข้อ 6)')
    if "'pres.perScreen'" not in txt:
        errors.append('ขาด i18n pres.perScreen (ป้ายแถบจำนวนหน้า/จอ) (ดู UI_STANDARD.md ข้อ 5)')
    if '#presentBar{display:none' not in _css or 'body.presentmode #presentBar{display:flex' not in _css:
        errors.append('#presentBar ต้อง display:none โดย default + แสดงเฉพาะ body.presentmode (กันแถบค้างนอกโหมดนำเสนอ) (ดู UI_STANDARD.md ข้อ 6)')
    if "'headermode','presentmode','gridview','pgbgmode')" not in txt:
        errors.append('buildMenuHtml ไม่ strip presentmode — state นำเสนอหลุดลงไฟล์เมนู (ดู UI_STANDARD.md ข้อ 6)')
    if "'boardmode','presentmode'" not in txt:
        errors.append('buildEditorHtml ไม่ strip presentmode — ไฟล์ editor เปิดมาติดโหมดนำเสนอ (ดู UI_STANDARD.md ข้อ 7)')
    if 'body.presentmode{' not in _css or 'body.presentmode #edbar' not in _css:
        errors.append('ขาด CSS body.presentmode (ซ่อน toolbar + พื้นเข้ม) (ดู UI_STANDARD.md ข้อ 5)')

    # ---- 78) ตัวเลือกไอคอนหัวกลุ่ม (emoji picker): ต้องมี 'ไม่ใช้ไอคอน' + ช่องไอคอนว่างคลิกเพิ่มกลับได้ในโหมดแก้ (ผู้ใช้ 18 ต.ค. 2026) ----
    #   เดิมเลือกได้อย่างเดียว ลบ/ไม่ใช้ไม่ได้ · เพิ่มปุ่ม pk.none (_emojiNone ล้าง textContent) + .em:empty editmode affordance (＋ คลิกเพิ่ม) · .em:empty default display:none (ไม่มี gap ตอนพิมพ์)
    if 'function _emojiNone' not in txt:
        errors.append('ขาด _emojiNone — ปุ่มไม่ใช้/ลบไอคอนหัวกลุ่มใช้ไม่ได้ (ดู UI_STANDARD.md ข้อ 5)')
    if "'pk.none'" not in txt:
        errors.append('ขาด i18n pk.none (ปุ่มไม่ใช้ไอคอนใน emoji picker) (ดู UI_STANDARD.md ข้อ 5)')
    if 'body.editmode .sec-h .em:empty' not in _css:
        errors.append('ช่องไอคอนหัวกลุ่มที่ว่าง ไม่มี affordance คลิกเพิ่มในโหมดแก้ (body.editmode .sec-h .em:empty) — ลบไอคอนแล้วเพิ่มกลับไม่ได้ (ดู UI_STANDARD.md ข้อ 5)')
    if '.sec-h .em:empty{display:none' not in _css:
        errors.append('.sec-h .em:empty ต้อง display:none โดย default — ไอคอนว่างไม่ควรเกิด gap ตอนพิมพ์/บันทึก (ดู UI_STANDARD.md ข้อ 6)')

    # ---- 79) ไอคอนหัวกลุ่มจากไฟล์ในเครื่อง: .em รองรับ <img> · ปุ่ม 'เลือกจากไฟล์' ใน picker · resize ~64px (ผู้ใช้ 18 ต.ค. 2026) ----
    if 'function _emojiFromFile' not in txt:
        errors.append('ขาด _emojiFromFile — ปุ่มเลือกไอคอนหัวกลุ่มจากไฟล์ใช้ไม่ได้ (ดู UI_STANDARD.md ข้อ 5)')
    if "'pk.file'" not in txt:
        errors.append('ขาด i18n pk.file (ปุ่มเลือกจากไฟล์ใน emoji picker) (ดู UI_STANDARD.md ข้อ 5)')
    if 'id="secIconInput"' not in txt:
        errors.append('ขาด #secIconInput (hidden file input ไอคอนหัวกลุ่ม) (ดู UI_STANDARD.md ข้อ 5)')
    if '.sec-h .em img' not in _css:
        errors.append('ขาด CSS .sec-h .em img — ไอคอนรูปจากไฟล์ไม่ถูกคุมขนาดในหัวกลุ่ม (ดู UI_STANDARD.md ข้อ 6)')
    if '#badgeInput,#secIconInput' not in txt:
        errors.append('buildMenuHtml ไม่ strip #secIconInput — hidden input หลุดลงไฟล์เมนู (ดู UI_STANDARD.md ข้อ 6)')
    # ---- 70) About modal: เด้งจากตรา P · เครดิต+ลิงก์คลิกได้ · เฉพาะจอ (ผู้ใช้ 16 ต.ค. 2026) ----
    # (a) element #aboutModal + wired คลิกตรา P (openAbout)
    if 'id="aboutModal"' not in txt:
        errors.append('ไม่พบ #aboutModal (ป๊อปอัพ About) (ดู UI_STANDARD.md ข้อ 11)')
    if 'function openAbout' not in txt or 'function closeAbout' not in txt:
        errors.append('ขาด function openAbout/closeAbout (ดู UI_STANDARD.md ข้อ 11)')
    if 'function aboutTab' not in txt:
        errors.append('ขาด function aboutTab (สลับแท็บ About) (ดู UI_STANDARD.md ข้อ 11)')
    if txt.count('class="about-tab') < 5 or 'data-tab="about"' not in txt or 'data-tab="tech"' not in txt or 'data-tab="lic"' not in txt or 'data-tab="full"' not in txt:
        errors.append('About ไม่ครบ 4 แท็บ (about/tech/lic/full) (ดู UI_STANDARD.md ข้อ 11)')
    if 'data-pane="full"' not in txt or 'data-i18n="about.fullBody"' not in txt:
        errors.append('About ขาดแท็บเต็มจอ (full pane + about.fullBody — วิธี App Window/Kiosk/F11) (ดู UI_STANDARD.md ข้อ 11)')
    if '--kiosk' not in txt:
        errors.append('แท็บเต็มจอต้องมีคำสั่ง kiosk (--kiosk) ให้ผู้ใช้คัดลอกไปตั้ง shortcut (ดู UI_STANDARD.md ข้อ 11)')
    if 'data-pane="tech"' not in txt or 'data-i18n="about.techBody"' not in txt:
        errors.append('About ไม่มีแท็บข้อมูลเทคนิค (about.techBody) (ดู UI_STANDARD.md ข้อ 11)')
    if 'data-pane="lic"' not in txt or 'data-i18n="about.licBody"' not in txt:
        errors.append('About ไม่มีแท็บลิขสิทธิ์ (about.licBody · OFL notice) (ดู UI_STANDARD.md ข้อ 11)')
    if 'class="ofl-text"' not in txt or 'SIL OPEN FONT LICENSE Version 1.1' not in txt:
        errors.append('About ไม่มีข้อความ OFL เต็มในไฟล์ (pre.ofl-text + ตัวบท OFL 1.1) — ต้องฝังเต็มให้ .html เดี่ยว self-contained (ดู UI_STANDARD.md ข้อ 11)')
    if 'THIRD-PARTY FONT LICENSES' not in txt:
        errors.append('ไม่พบ OFL notice ใน header comment (ดู UI_STANDARD.md ข้อ 11)')
    _eb70=re.search(r'<span class="edbrand"[^>]*>', txt)
    if not _eb70 or 'openAbout()' not in _eb70.group(0):
        errors.append('ตรา P (.edbrand) ไม่ได้ wired openAbout() — คลิกแล้วต้องเปิด About (ดู UI_STANDARD.md ข้อ 11)')
    # (b) ลิงก์ติดต่อ/GitHub ต้องคลิกได้จริง (mailto + github target=_blank)
    _am70=re.search(r'<div id="aboutModal"[\s\S]*?</div></div>', txt)
    _ams=_am70.group(0) if _am70 else ''
    if 'href="mailto:jenkarn2631@gmail.com"' not in _ams:
        errors.append('About ไม่มีลิงก์อีเมล mailto คลิกได้ (ดู UI_STANDARD.md ข้อ 11)')
    if 'github.com/Justin-10/OE' not in _ams or 'target="_blank"' not in _ams:
        errors.append('About ไม่มีลิงก์ GitHub แบบเปิดแท็บใหม่ (target=_blank) (ดู UI_STANDARD.md ข้อ 11)')
    # (c) ปิด .open ตอนบันทึก editor + ตัดทิ้งใน buildMenuHtml
    if "_abm.classList.remove('open')" not in txt:
        errors.append('buildEditorHtml ไม่ได้ปิด About (.open) ตอนบันทึก (ดู UI_STANDARD.md ข้อ 11)')
    _ml70=re.search(r"\['#edbar','#edstatus'[^\]]*\]", txt)
    if not _ml70 or "'#aboutModal'" not in _ml70.group(0):
        errors.append('buildMenuHtml ไม่ได้ตัด #aboutModal ออกจากไฟล์เมนู (ดู UI_STANDARD.md ข้อ 11)')
    # (d) i18n about.* ครบ th+en
    _i70=txt.find('var I18N={')
    if _i70>=0:
        _th70=txt.find('th:{',_i70); _en70=txt.find('en:{',_i70)
        _thb70=txt[_th70:_en70] if (_th70>=0 and _en70>_th70) else ''
        _enb70=txt[_en70:_en70+30000] if _en70>=0 else ''
        for _k70 in ('about.title','about.desc','about.by','about.byName','about.licenseLbl','about.close','about.tabAbout','about.tabTech','about.techHead','about.techBody','about.techNote','about.tabLic','about.licHead','about.oflView','about.licBody','about.licNote','about.tabFull','about.fullHead','about.fullBody','about.fullNote'):
            if ("'"+_k70+"'") not in _thb70: errors.append('i18n '+_k70+' ขาดใน th (ดู UI_STANDARD.md ข้อ 11)')
            if ("'"+_k70+"'") not in _enb70: errors.append('i18n '+_k70+' ขาดใน en (ดู UI_STANDARD.md ข้อ 11)')

    # ---- 71) Paste-import รายการ: ปุ่ม + modal + parser + strip + i18n (ผู้ใช้ 17 ต.ค. 2026) ----
    if 'id="btnPasteImport"' not in txt:
        errors.append('ไม่พบปุ่ม #btnPasteImport (วางรายการ) ในแท็บข้อความ (ดู UI_STANDARD.md ข้อ 12)')
    _pb71=re.search(r'<button[^>]*id="btnPasteImport"[^>]*>', txt)
    if not _pb71 or 'openPaste()' not in _pb71.group(0):
        errors.append('ปุ่ม #btnPasteImport ไม่ได้ wired openPaste() (ดู UI_STANDARD.md ข้อ 12)')
    if 'id="pasteModal"' not in txt:
        errors.append('ไม่พบ #pasteModal (ป๊อปอัพวางรายการ) (ดู UI_STANDARD.md ข้อ 12)')
    if 'data-i18n="paste.modalTitle"' not in txt:
        errors.append('ไม่พบหัวข้อ modal paste.modalTitle (ดู UI_STANDARD.md ข้อ 12)')
    if '<details class="paste-howto" open>' not in txt:
        errors.append('<details class="paste-howto"> ต้องมี open (เปิดวิธีนำเข้าเป็นค่าเริ่มต้น — เห็น format ตั้งแต่แรก) (ดู UI_STANDARD.md ข้อ 12)')
    if 'id="pasteDest"' not in txt:
        errors.append('ไม่พบ #pasteDest (ช่องเลือกหน้าปลายทางนำเข้า) (ดู UI_STANDARD.md ข้อ 12)')
    if 'id="pasteCol"' not in txt:
        errors.append('ไม่พบ #pasteCol (ช่องเลือกคอลัมน์ปลายทาง ซ้าย/ขวา) (ดู UI_STANDARD.md ข้อ 12)')
    if '_pageNoOf(made[0])' not in txt:
        errors.append('doPasteImport ไม่ได้รายงานหน้าปลายทาง (_pageNoOf) — ต้องบอกหน้าหลังนำเข้า (ดู UI_STANDARD.md ข้อ 12)')
    _pbox71=re.search(r'#pasteModal \.about-box\{([^}]*)\}', txt)
    if not _pbox71 or 'background' not in _pbox71.group(1):
        errors.append('#pasteModal .about-box ไม่มี background (การ์ดหาย — กล่องลอยบนพื้นมืด) (ดู UI_STANDARD.md ข้อ 12)')
    for _f71 in ('function openPaste','function closePaste','function doPasteImport','function _pasteParseLine'):
        if _f71 not in txt:
            errors.append('ขาด '+_f71+' (paste-import) (ดู UI_STANDARD.md ข้อ 12)')
    # strip: menu print array + editor save close
    _arr71=re.search(r"\['#edbar'[^\]]*\]", txt)
    if not _arr71 or "'#pasteModal'" not in _arr71.group(0):
        errors.append('buildMenuHtml ไม่ได้ตัด #pasteModal ออกจากไฟล์เมนู (ดู UI_STANDARD.md ข้อ 12)')
    if "_pm=clone.querySelector('#pasteModal')" not in txt or "_pm.classList.remove('open')" not in txt:
        errors.append('buildEditorHtml ไม่ได้ปิด #pasteModal (.open) ตอนบันทึก (ดู UI_STANDARD.md ข้อ 12)')
    # i18n ครบ th+en
    _i71=txt.find('var I18N={')
    if _i71>=0:
        _th71s=txt.find('th:{',_i71); _en71s=txt.find('en:{',_i71)
        _thb71=txt[_th71s:_en71s] if (_th71s>=0 and _en71s>_th71s) else ''
        _enb71=txt[_en71s:_en71s+30000] if _en71s>=0 else ''
        for _k71 in ('btn.pasteImport','paste.title','paste.modalTitle','paste.destLbl','paste.colLbl','paste.colLeft','paste.colRight','paste.desc','paste.import','paste.cancel','paste.empty','paste.done','paste.grpDefault','paste.ph'):
            if ("'"+_k71+"'") not in _thb71: errors.append('i18n '+_k71+' ขาดใน th (ดู UI_STANDARD.md ข้อ 12)')
            if ("'"+_k71+"'") not in _enb71: errors.append('i18n '+_k71+' ขาดใน en (ดู UI_STANDARD.md ข้อ 12)')

    # ---- 72) ปุ่มมาตรฐานกลาง ui-btn-* ในทุก dialog/modal (ผู้ใช้ 17 ต.ค. 2026) ----
    #   ทุก modal ใช้ .ui-btn-primary/.ui-btn-secondary · ห้ามปุ่มใน modal ฝัง background:# สีเอง (กันดริฟต์ธีม) · ดู UI_STANDARD.md ข้อ 13
    for _sel72,_need72 in (('.ui-btn-primary{','#217346'),('.ui-btn-secondary{','#d2d0ce')):
        _m72=re.search(re.escape(_sel72)+r'([^}]*)\}', _css)
        if not _m72 or _need72 not in _m72.group(1):
            errors.append('คลาส '+_sel72+' หาย/สีไม่ถูก (ต้องมี '+_need72+') (ดู UI_STANDARD.md ข้อ 13)')
    _mp72=re.search(r'\.ui-btn:active[^{]*\{([^}]*)\}', _css)
    if not _mp72 or 'transform' not in _mp72.group(1):
        errors.append('.ui-btn:active ต้องมี transform (press state · ดู UI_STANDARD.md ข้อ 13)')
    _abt72=txt.find('id="aboutModal"'); _pst72=txt.find('id="pasteModal"')
    if _abt72>=0 and _pst72>_abt72:
        _segs72={'aboutModal':txt[_abt72:_pst72], 'pasteModal':txt[_pst72:txt.find('</body>',_pst72)]}
        for _mid72,_seg72 in _segs72.items():
            for _bm72 in re.finditer(r'<button\b[^>]*>', _seg72):
                _tag72=_bm72.group(0)
                if 'ui-btn' not in _tag72 and 'about-tab' not in _tag72:
                    errors.append('ปุ่มใน #'+_mid72+' ไม่ได้ใช้คลาส ui-btn-* (ปุ่ม dialog ต้องใช้คลาสกลาง · ยกเว้นแท็บนำทาง .about-tab · ดู UI_STANDARD.md ข้อ 13)')
                if 'background:#' in _tag72:
                    errors.append('ปุ่มใน #'+_mid72+' ฝัง background:# สี inline (ห้าม — ใช้ ui-btn-primary/secondary · ดู UI_STANDARD.md ข้อ 13)')

    # ---- 73) i18n: apostrophe ไม่ escape ในสตริง single-quote (ผู้ใช้ 17 ต.ค. 2026 · บั๊ก user's ทำ JS พังทั้งไฟล์) ----
    #   ค่า i18n ทุกตัวครอบด้วย single quote · apostrophe ในคำ (เช่น user's, don't) ปิดสตริงก่อนเวลา → SyntaxError → script ไม่โหลด → แอปค้าง
    #   สัญญาณ: letter'letter ในบล็อก I18N = apostrophe ไม่ escape (delimiter ที่ถูกต้องมี : , { } หรือช่องว่างติด · escaped มี \\ นำหน้า)
    _i73 = txt.find('var I18N={')
    if _i73 >= 0:
        _end73 = txt.find('};', _i73)
        _blk73 = txt[_i73:_end73] if _end73 > _i73 else txt[_i73:_i73+60000]
        _apos73 = re.findall(r"[A-Za-z]'[A-Za-z]", _blk73)
        if _apos73:
            errors.append("i18n มี apostrophe ไม่ escape ในสตริง (เช่น user's/don't) — ปิด string กลางคัน JS พัง: {} — เขียนใหม่เลี่ยง ' หรือ escape \\' (ดู UI_STANDARD.md ข้อ 11)".format(', '.join(sorted(set(_apos73))[:5])))

    # ---- 74) โหมดจอป้าย (display board) จอ + พิมพ์ — ล็อกครบทุกส่วน (ผู้ใช้ 18 ต.ค. 2026) ----
    #   พื้น #ECEDEF + ตัวอักษร/ราคา #171A1E · @media screen, print + print-color-adjust:exact · CSS อยู่ใน <style> ก้อนแรก (รอด buildMenuHtml) · Save Menu คงโหมด (WYSIWYG) · Save Editor ถอด · i18n TH/EN
    _e74 = []
    if 'body.boardmode' not in _css: _e74.append('ไม่พบ CSS body.boardmode')
    if 'function toggleBoardMode(' not in txt: _e74.append('ไม่พบ toggleBoardMode')
    if 'id="btnBoard"' not in txt: _e74.append('ไม่พบปุ่ม btnBoard')
    if "'imgmode','imghidden','boardmode'" not in txt: _e74.append('boardmode ไม่ถูก strip ตอนบันทึก editor')
    if "'editmode','editing-on','pricemode','imghidden','imgmode','headermode','presentmode','gridview','pgbgmode')" not in txt: _e74.append('buildMenuHtml strip ไม่ตรง — boardmode คงไว้ (WYSIWYG) · presentmode ต้องถูก strip')
    if "'btn.board':'โมโนโครม'" not in txt: _e74.append('ไม่พบ i18n TH btn.board (โมโนโครม)')
    if "'btn.board':'Monochrome'" not in txt: _e74.append('ไม่พบ i18n EN btn.board (Monochrome)')
    if '@media screen, print{' not in _css: _e74.append('board CSS ไม่ได้อยู่ใน @media screen, print — จอป้ายจะไม่พิมพ์')
    if 'print-color-adjust:exact' not in _css: _e74.append('ไม่มี print-color-adjust:exact — พื้นเทาจอป้ายจะไม่พิมพ์ (ต้องติ๊ก Background graphics เอง)')
    if '.sec-h .sechead *{color:#171A1E' not in _css: _e74.append('หัวข้อกลุ่มที่ทาสีบางคำ (child span) ไม่ถูก override เป็น #171A1E ในจอป้าย — ต้องมี .sec-h .sechead * ครอบ child run')
    if 'body.boardmode .sec-h .sechead{text-shadow' not in _css: _e74.append('จอป้ายไม่บังคับขอบขาวหัวข้อกลุ่ม (text-shadow) — ขอบที่ผู้ใช้ตั้งเองจะค้าง ไม่เป็นดำ/ขอบขาวตามมาตรฐานจอป้าย')
    if _e74: errors.append('lint #74 (โหมดจอป้าย): ' + ' · '.join(_e74))

    # ---- 93) ธีมสี: :root ตัวแปรสีกลาง 5 โซน + สีตัวอักษร · ห้าม hardcode สีเดิมกลับ (ผู้ใช้ 23 ต.ค. 2026 · รอบ1 refactor) ----
    _e93 = []
    if ':root{' not in _css and ':root {' not in _css:
        _e93.append('ไม่พบ :root ใน CSS')
    for _v93 in ('--note-bd','--note-bg','--grp-bd','--grp-head-bg','--grp-body-bg','--txt-name','--txt-note','--txt-price','--line-dot'):
        if (_v93 + ':') not in _css:
            _e93.append('ไม่พบตัวแปร ' + _v93)
    _zones93 = [
        (r'\.crab\{([^}]*)\}', ('var(--note-bg)','var(--note-bd)'), ('#ffffff','#d8ccb8'), '.crab'),
        (r'\.sec\{break-inside:avoid;([^}]*)\}', ('var(--grp-bd)','rgba(var(--grp-body-bg)'), ('#e3d8c6','rgba(255,255,255'), '.sec'),
        (r'\.sec-h\{([^}]*)\}', ('rgba(var(--grp-head-bg)','var(--grp-bd)'), ('rgba(245,239,228','#e3d8c6'), '.sec-h'),
        (r'\.nm\{([^}]*)\}', ('var(--txt-name)',), ('#171a1e',), '.nm'),
        (r'\.nm \.note\{([^}]*)\}', ('var(--txt-note)',), ('#6f6456',), '.nm .note'),
        (r'\.ln\{([^}]*)\}', ('var(--line-dot)',), ('#cdbfa8',), '.ln'),
        (r'\.pr\{([^}]*)\}', ('var(--txt-price)',), ('#2b3038',), '.pr'),
        (r'\.secnote\{([^}]*)\}', ('var(--txt-note)',), ('#6f6456',), '.secnote'),
    ]
    for _rx93,_need93,_ban93,_nm93 in _zones93:
        _m93 = re.search(_rx93, _css)
        if not _m93:
            _e93.append(_nm93 + ' ไม่พบบล็อก'); continue
        _b93 = _m93.group(1)
        for _nd93 in _need93:
            if _nd93 not in _b93: _e93.append(_nm93 + ' ขาด ' + _nd93)
        for _bn93 in _ban93:
            if _bn93 in _b93: _e93.append(_nm93 + ' ยัง hardcode ' + _bn93)
    if _e93: errors.append('lint #93 (ตัวแปรสีกลาง/ธีม): ' + ' · '.join(_e93))

    # ---- 94) ธีมสี: 4 ธีม (:root[data-theme]) + ปุ่มเลือกธีม + JS + i18n · ธีมเข้มบังคับหัวกลุ่มอ่านออก (ผู้ใช้ 23 ต.ค. 2026 · รอบ2) ----
    _e94=[]
    for _t94 in ('white-green','dark-gold','paper-brick','bw','white-gray','pine-cream','navy-white','maroon-cream','terracotta','plum','teal','mustard','blue-ocean','vivid-red','vivid-blue','vivid-green','navy-dark','wine-dark','sage','dusty-blue','dusty-rose','mono-dark','mono-gray','vivid-orange','vivid-yellow','vivid-purple','forest-dark','coffee-dark','purple-dark','dusty-orange','dusty-yellow','dusty-purple','vivid-pink','pink-white','pink-dark','dusty-red','orange-dark','dusty-brown','red-white','blush','sakura','peach','orange-white','latte','kraft','vivid-brown','lemon','honey','denim-cream','lavender','lilac-cream'):
        if (':root[data-theme="'+_t94+'"]') not in _css:
            _e94.append('ไม่พบธีม ' + _t94)
    _m_themes94=re.search(r"var _THEMES=\[([^\]]*)\]", txt)
    for _tid94 in ('bw','white-gray','pine-cream','navy-white','maroon-cream','terracotta','plum','teal','mustard','blue-ocean','vivid-red','vivid-blue','vivid-green','navy-dark','wine-dark','sage','dusty-blue','dusty-rose','mono-dark','mono-gray','vivid-orange','vivid-yellow','vivid-purple','forest-dark','coffee-dark','purple-dark','dusty-orange','dusty-yellow','dusty-purple','vivid-pink','pink-white','pink-dark','dusty-red','orange-dark','dusty-brown','red-white','blush','sakura','peach','orange-white','latte','kraft','vivid-brown','lemon','honey','denim-cream','lavender','lilac-cream'):
        if not _m_themes94 or ("'"+_tid94+"'") not in _m_themes94.group(1): _e94.append('_THEMES ขาด ' + _tid94)
    if 'data-theme="dark-gold"] .sec-h' not in _css:
        _e94.append('ธีมเข้มไม่ override สีหัวกลุ่ม (.sec-h อ่านไม่ออกบนพื้นเข้ม)')
    if 'data-theme="dark-gold"] .crab' not in _css:
        _e94.append('ธีมเข้มไม่ override สีตัวหนังสือกล่องโน้ต (.crab อ่านไม่ออกบนพื้นเข้ม)')
    if 'function _themeDdHtml(' not in txt:
        _e94.append('preset ธีมต้องเป็น custom dropdown (_themeDdHtml)')
    if 'onmouseenter="_themeDdPreview(' not in txt:
        _e94.append('dropdown ธีมต้อง live preview ตอนชี้ (_themeDdPreview)')
    if 'onclick="_themeDdCommit(' not in txt:
        _e94.append('dropdown ธีมต้อง commit ตอนคลิก (_themeDdCommit)')
    if '#edbar #btnTheme.on' not in _css:
        _e94.append('btnTheme ไม่มี active เขียวในแถบ (ข้อ 11)')
    for _fn94 in ('function _themeApply(','function _themeLoad(','function openThemePanel(','function _themePick('):
        if _fn94 not in txt: _e94.append('ไม่พบ ' + _fn94)
    if 'var _THEMES' not in txt: _e94.append('ไม่พบ _THEMES')
    if "'oe_theme'" not in txt: _e94.append('ไม่พบคีย์ oe_theme')
    if 'id="btnTheme"' not in txt: _e94.append('ไม่พบปุ่ม btnTheme')
    if '_themeLoad();' not in txt: _e94.append('ไม่เรียก _themeLoad() ตอนเปิดแอป')
    for _k94 in ('btn.theme','grp.theme','th.pick','th.cream','th.whiteGreen','th.darkGold','th.paperBrick','th.bw','th.whiteGray','th.pineCream','th.navyWhite','th.maroonCream','th.terracotta','th.plum','th.teal','th.mustard','th.blueOcean','th.vividRed','th.vividBlue','th.vividGreen','th.navyDark','th.wineDark','th.sage','th.dustyBlue','th.dustyRose','th.monoDark','th.monoGray'):
        if ("'"+_k94+"'") not in txt: _e94.append('ไม่พบ i18n ' + _k94)
    _mdd94=re.search(r"var _THEME_ORDER=\['([a-z-]+)'", txt)
    if not _mdd94 or _mdd94.group(1)!='custom': _e94.append('dropdown ธีม: กำหนดเองต้องเป็นลำดับแรก (_THEME_ORDER[0]==custom)')
    if ':root[data-theme="bw"] .sec-h' not in _css:
        _e94.append('ธีมขาว-ดำไม่ override สีหัวกลุ่มเป็นขาว (หัวกลุ่มพื้นดำอ่านไม่ออก)')
    if _e94: errors.append('lint #94 (ธีมสี): ' + ' · '.join(_e94))

    # ---- 95) ธีมกำหนดเอง (custom theme): 9 โซนเลือกสีเอง + mode theme ในหน้าต่างสีกลาง + หัวกลุ่มอ่านออก (ผู้ใช้ 23 ต.ค. 2026) ----
    _e95=[]
    if ':root[data-theme="custom"] .sec-h' not in _css:
        _e95.append('ธีมกำหนดเองไม่ override สีหัวกลุ่ม (อ่านไม่ออกบนพื้นเข้ม)')
    if '#edpanel .thcp-grp' not in _css:
        _e95.append('ไม่พบ CSS กลุ่มพิกเกอร์ธีม (.thcp-grp)')
    if '.thcp-dot' in _css:
        _e95.append('ยังมี .thcp-dot (ปุ่มกรอบเดี่ยวแบบเก่า — ต้องใช้ถาดสี cp-trigger)')
    if 'id="thcpPop"' not in txt or 'id="thcpGrid"' not in txt or 'id="thcpHex"' not in txt:
        _e95.append('ไม่พบถาดสีธีม (thcpPop/thcpGrid)')
    for _fn95 in ('function _themeCustomSet(','function _themeEnterCustom(','function _themeCpOpen(','function _themeVarHex(','function _themeRenderPanel(','function _themeApplyCustomVars(','function _themeClearCustomInline(','function _themeSwatchOpen(','function _themePickSwatch(','function _themeMkSw(','function _themeCpCommit(','function _themeCpCancel(','function _themePreviewVar('):
        if _fn95 not in txt: _e95.append('ไม่พบ ' + _fn95)
    if '_thcpOrig' not in txt: _e95.append('ไม่พบ _thcpOrig (snapshot สีเดิมก่อน preview)')
    if 'onclick="_themeCpCommit()"' not in txt: _e95.append('ปุ่มตกลงถาดธีมไม่ได้ผูก _themeCpCommit')
    if "_cpMode==='theme'" not in txt: _e95.append('หน้าต่างสีกลางไม่มี mode theme')
    if 'thcpPick_' not in txt: _e95.append('ไม่พบ home element พิกเกอร์ (thcpPick_)')
    if "'oe_theme_custom'" not in txt: _e95.append('ไม่พบคีย์ oe_theme_custom')
    if 'var _THEME_VARS' not in txt: _e95.append('ไม่พบ _THEME_VARS')
    if "id==='custom'" not in txt: _e95.append('_themePick ไม่จัดการ custom')
    for _k95 in ('th.custom','th.resetCustom','th.grpSet','th.grpNote','th.grpGroup','th.grpText','th.zNoteBg','th.zNoteBd','th.zHeadBg','th.zBodyBg','th.zGrpBd','th.zName','th.zPrice','th.zNote','th.zDot'):
        if ("'"+_k95+"'") not in txt: _e95.append('ไม่พบ i18n ' + _k95)
    if '.cp-actions' not in _css: _e95.append('ไม่พบ .cp-actions (ตกลง/ยกเลิก ต้องอยู่แถวล่างของตัวเอง)')
    if '<div class="cp-actions">' not in txt: _e95.append('markup ไม่มี .cp-actions ครอบปุ่มตกลง/ยกเลิก')
    _mtr95=re.search(r'#edpanel \.thcp-row\{([^}]*)\}', _css)
    if not _mtr95 or 'flex-start' not in _mtr95.group(1): _e95.append('.thcp-row ต้อง align-items:flex-end (baseline ถาดสี/dropdown/คืนค่าตรงกัน)')
    if '#edpanel .thcp-head' not in _css: _e95.append('ไม่พบ .thcp-head (dropdown ธีมต้องชิดล่าง)')
    _mgl95=re.search(r'#edpanel \.thcp-grp \.thcp-gl\{([^}]*)\}', _css)
    if not _mgl95 or 'font-size:16px' not in _mgl95.group(1): _e95.append('.thcp-gl ป้ายโซนต้อง 16px (อ่านง่ายเท่าปุ่ม ribbon)')
    elif 'font-weight:600' in _mgl95.group(1) or 'font-weight:700' in _mgl95.group(1) or 'font-weight:bold' in _mgl95.group(1): _e95.append('.thcp-gl ห้าม bold (คงความเป็น panel ไม่หนา)')
    _mch95=re.search(r'#edpanel \.thcp-cat-h\{([^}]*)\}', _css)
    if not _mch95 or 'font-size:13px' not in _mch95.group(1): _e95.append('.thcp-cat-h ต้อง 13px (เท่าป้ายกลุ่ม ribbon .rgl)')
    _msep95=re.search(r'#edpanel \.thcp-sep\{([^}]*)\}', _css)
    if not _msep95 or '#b3b0ad' not in _msep95.group(1): _e95.append('.thcp-sep ต้อง #b3b0ad (เส้นคั่นชัดเท่า ribbon)')
    _nsep95=_css.count('.thcp-sep')
    _ntr95=txt.count('<span class="thcp-sep">')
    if _ntr95 < 5: _e95.append('ต้องมีเส้นคั่นอย่างน้อย 5 เส้น (1 หน้ากลุ่มแรก + 3 คั่นกลุ่ม + 1 ปิดท้าย) — พบ '+str(_ntr95))
    for _epc95,_epn95 in (('ep-sel','dropdown'),('ep-flabel','ป้าย label'),('ep-mini','ปุ่มเล็ก')):
        _mep95=re.search(r'#edpanel \.'+_epc95+r'\{([^}]*)\}', _css)
        if not _mep95 or 'font-size:16px' not in _mep95.group(1): _e95.append('.'+_epc95+' ('+_epn95+') ต้อง 16px (สม่ำเสมอกับป้ายโซน)')
    _mfl95b=re.search(r'#edpanel \.ep-flabel\{([^}]*)\}', _css)
    if _mfl95b and ('font-weight:600' in _mfl95b.group(1) or 'font-weight:700' in _mfl95b.group(1) or 'font-weight:bold' in _mfl95b.group(1)): _e95.append('.ep-flabel ห้าม bold (panel ไม่หนา)')
    if _e95: errors.append('lint #95 (ธีมกำหนดเอง): ' + ' · '.join(_e95))

    # ---- 96) มาตรฐานถาดสีใหม่: ถาดข้อความ/ขอบใช้ ตกลง/ยกเลิก (preview+commit) · ตัด 'ทาสี' (ผู้ใช้ 23 ต.ค. 2026) ----
    _e96=[]
    if 'id="typoCpPaint"' in txt: _e96.append('ถาดข้อความยังมีปุ่มทาสี typoCpPaint (ต้องตัดออก)')
    for _fn96 in ('function _tcpCommit(','function _tcpCancel(','function _tcpPreview(','function _tcpSnap(','function _tcpRestore(','function _olCommit(','function _olCancel(','function _olPvSnap(','function _olPvColor(','function _olPvWidth('):
        if _fn96 not in txt: _e96.append('ไม่พบ '+_fn96)
    if 'onclick="_tcpCommit()"' not in txt: _e96.append('ถาดข้อความไม่มีปุ่มตกลง')
    if "cl('.cp-ok')" not in txt: _e96.append('ถาดขอบไม่มีปุ่มตกลง (_olCommit)')
    if _e96: errors.append('lint #96 (มาตรฐานถาดสี ตกลง/ยกเลิก): '+' · '.join(_e96))

    # ---- 97) มาตรฐานปุ่มถาดสี (cp-trigger) = split เดียวกับ A4: ขอบ #d2d0ce · caret 22px · สีเต็มกล่องไม่มีขอบซ้อน (ผู้ใช้ 23 ต.ค. 2026) ----
    _e97=[]
    for _sc97 in ('#typobar','#edpanel'):
        _mt97=re.search(re.escape(_sc97+' .cp-trigger{')+r'([^}]*)\}', _css)
        if not _mt97 or '#d2d0ce' not in _mt97.group(1): _e97.append(_sc97+' .cp-trigger ขอบไม่ใช่ #d2d0ce')
        _mc97=re.search(re.escape(_sc97+' .cp-trigger .cp-caretbtn{')+r'([^}]*)\}', _css)
        if not _mc97 or 'width:22px' not in _mc97.group(1): _e97.append(_sc97+' caret ไม่กว้าง 22px')
        _mcur97=re.search(re.escape(_sc97+' .cp-trigger .cp-current{')+r'([^}]*)\}', _css)
        if not _mcur97: _e97.append(_sc97+' ไม่พบ cp-current')
        elif '1px solid #bbb' in _mcur97.group(1): _e97.append(_sc97+' cp-current ยังมีขอบซ้อน #bbb')
    _mol97=re.search(r'#typobar \.olpick\{([^}]*)\}', _css)
    if not _mol97 or '#d2d0ce' not in _mol97.group(1): _e97.append('ปุ่มขอบ A (.olpick) frame ไม่ใช้ #d2d0ce')
    _moc97=re.search(r'#typobar \.ttoggle\.olcaret\{([^}]*)\}', _css)
    if not _moc97 or 'width:22px' not in _moc97.group(1): _e97.append('olcaret ไม่กว้าง 22px')
    if _e97: errors.append('lint #97 (ปุ่มถาดสี): '+' · '.join(_e97))

    # ---- 98) checkOverflow ต้องเก็บ/คืน scrollTop รอบ measuring (กัน scroll เด้งหน้า 2 ตอนเข้าโหมดแก้/เพิ่ม/ลบ · ผู้ใช้ 23 ต.ค. 2026) ----
    _co98=re.search(r'function checkOverflow\([\s\S]*?\n  \}', txt)
    if _co98:
        _cob98=_co98.group(0)
        if 'scrollTop' not in _cob98 or '_sy98' not in _cob98:
            errors.append('lint #98: checkOverflow ไม่เก็บ/คืน scrollTop รอบ measuring (scroll จะเด้งหน้าตอนแก้/เพิ่ม/ลบ)')

    # ---- 99) toggleEdit ต้องตรึงหน้าที่ดูอยู่ (เข้าโหมดแก้→หน้าสูงขึ้น ไม่เด้งไปหน้าอื่น · ผู้ใช้ 23 ต.ค. 2026) ----
    _te99=re.search(r'function toggleEdit\([\s\S]*?\n\}', txt)
    if _te99:
        _teb99=_te99.group(0)
        if '_veIdx99' not in _teb99 or '_priceVisiblePage' not in _teb99 or 'scrollTop' not in _teb99:
            errors.append('lint #99: toggleEdit ไม่ตรึงหน้าที่ดูอยู่ (จะเด้งหน้าตอนเข้าโหมดแก้)')

    # ---- 100) cursor/caret: เส้นบางปกติ (ห้าม caret-shape · ผู้ใช้ 29 ต.ค. 2026) + เห็นทุกธีม (currentColor) · note โหมดแก้ cursor ชิดซ้าย (ผู้ใช้ 23 ต.ค. 2026) ----
    if 'caret-shape' in _css: errors.append('lint #100: ห้ามใช้ caret-shape — cursor ต้องเป็นเส้นบางปกติ (ช่องเล็กแล้วก้อนดำเต็มช่อง ดูไม่ออกว่าพร้อมพิมพ์ · ผู้ใช้ 29 ต.ค. 2026)')
    _mcar=re.search(r'\[contenteditable="true"\][^{]*\{([^}]*)\}', _css)
    if not _mcar or 'caret-color:currentColor' not in _mcar.group(1): errors.append('lint #100: caret-color ต้องเป็น currentColor (กันหายในธีมเข้ม)')
    _msn=re.search(r'body\.editmode \.secnote\[contenteditable\]\{([^}]*)\}', _css)
    if not _msn or 'padding-right' not in _msn.group(1): errors.append('lint #100: หมายเหตุโหมดแก้ต้อง padding-right (เว้นที่ให้ปุ่ม × — cursor ไม่ชน)')
    if _msn and 'text-align:left' in _msn.group(1): errors.append('lint #100: หมายเหตุโหมดแก้ห้าม text-align:left (ต้อง WYSIWYG ชิดขวาเหมือนตอนพิมพ์)')

    # ---- 101) panel มาตรฐานเดียวกับต้นแบบธีม: ฟอนต์ control 16px + ปรับราคาแบ่งกลุ่ม thcp (ผู้ใช้ 24 ต.ค. 2026) ----
    for _sel,_rule in [('.ep-seg label','.ep-seg label{'),('.ep-num','.ep-num{'),('.ep-chk','.ep-chk{'),('.ep-label','.ep-label{'),('.ep-input','.ep-input{'),('.ep-suffix','.ep-suffix{')]:
        _m101=re.search(re.escape(_rule)+r'([^}]*)\}', _css)
        if not _m101:
            errors.append('lint #101: ไม่พบ CSS rule '+_sel)
        elif 'font-size:16px' not in _m101.group(1):
            errors.append('lint #101: '+_sel+' ต้อง font-size:16px (control tier เท่ากันทุก panel แบบต้นแบบธีม)')
    if '#edpanel .thcp-unit{display:contents' not in _css:
        errors.append('lint #101: ไม่พบ .thcp-unit{display:contents} (หน่วยกลุ่มซ่อน-แสดงพร้อมเส้นคั่น)')
    _pp101=re.search(r'function openPricePanel\(\)\{[\s\S]*?openPanel\(\{mode:', txt)
    if not _pp101:
        errors.append('lint #101: หา openPricePanel ไม่เจอ')
    else:
        _ppb=_pp101.group(0)
        for _tok in ['thcp-row','thcp-cat-z','thcp-cat-h','thcp-sep','thcp-unit']:
            if _tok not in _ppb:
                errors.append('lint #101: panel ปรับราคาต้องใช้โครง '+_tok+' (แบ่งกลุ่มแบบต้นแบบธีม)')
        for _lbl in ['pr.task','pr.scope','pr.fillLbl','pr.amtLbl','pr.priceLbl']:
            if ('thcp-cat-h" data-i18n="'+_lbl) not in _ppb:
                errors.append('lint #101: ชื่อกลุ่ม '+_lbl+' ต้องอยู่ใน .thcp-cat-h (ใต้ control)')
        if 'ep-flabel' in _ppb:
            errors.append('lint #101: panel ปรับราคาห้ามใช้ ep-flabel แล้ว (ย้ายชื่อกลุ่มไป thcp-cat-h ใต้ control)')
    # ---- 101b) control tier ห้ามหนา (<=500) + ปรับราคามีเส้นปิดท้ายกลุ่มสุดท้าย (ผู้ใช้ 24 ต.ค. 2026) ----
    for _sel2,_rule2 in [('.ep-seg label','.ep-seg label{'),('.ep-num','.ep-num{'),('.ep-chk','.ep-chk{'),('.ep-label','.ep-label{'),('.ep-suffix','.ep-suffix{')]:
        _mw=re.search(re.escape(_rule2)+r'([^}]*)\}', _css)
        if _mw:
            _wm=re.search(r'font-weight:(\d+)', _mw.group(1))
            if _wm and int(_wm.group(1))>500:
                errors.append('lint #101: '+_sel2+' ห้าม font-weight>500 (ตัวหนาเกิน — ต้องเสมอต้นแบบธีมที่ไม่หนา)')
    if _pp101:
        _ppb2=_pp101.group(0)
        if _ppb2.rfind('thcp-sep') < _ppb2.rfind('class="thcp-cat"'):
            errors.append('lint #101: panel ปรับราคาต้องมีเส้นคั่นปิดท้าย (thcp-sep หลังกลุ่มสุดท้าย — ปิดกลุ่มสองฝั่งแบบต้นแบบธีม)')

    # ---- 101c) panel พื้นหลังใช้โครงกลุ่มต้นแบบธีม + ห้ามเส้นคั่นนำหน้ากลุ่มแรก + i18n ครบ (ผู้ใช้ 24 ต.ค. 2026) ----
    _bg101=re.search(r'function openPageBgPanel\(\)\{[\s\S]*?openPanel\(\{mode:', txt)
    if not _bg101:
        errors.append('lint #101: หา openPageBgPanel ไม่เจอ')
    else:
        _bgb=_bg101.group(0)
        for _tok in ['thcp-row','thcp-cat-z','thcp-cat-h','thcp-sep','thcp-grp']:
            if _tok not in _bgb:
                errors.append('lint #101: panel พื้นหลังต้องใช้โครง '+_tok+' (แบ่งกลุ่มแบบต้นแบบธีม)')
        for _lbl in ['bg.scope','bg.grpColorImg','bg.grpDim','bg.grpContent','th.grpSet']:
            if ('thcp-cat-h" data-i18n="'+_lbl) not in _bgb:
                errors.append('lint #101: ชื่อกลุ่ม '+_lbl+' ต้องอยู่ใน .thcp-cat-h (panel พื้นหลัง)')
        if 'ep-flabel' in _bgb:
            errors.append('lint #101: panel พื้นหลังห้ามใช้ ep-flabel แล้ว (ย้ายชื่อไป thcp-gl/thcp-cat-h)')
        if _bgb.rfind('thcp-sep') < _bgb.rfind('class="thcp-cat"'):
            errors.append('lint #101: panel พื้นหลังต้องมีเส้นคั่นปิดท้ายกลุ่มสุดท้าย')
        for _idk in ['bgCpApply','bgCpCurrent','bgCpCaret','bgCpPop','bgCpGrid','bgCpCustom','bgHex','bgCpAdd','bgCpPaint','bgCpPick','bgRangeWrap','bgRange','btnPgContentHide']:
            if _idk not in _bgb:
                errors.append('lint #101: panel พื้นหลังต้องคง id '+_idk+' (JS ผูกด้วย id)')
    # ห้ามเส้นคั่นนำหน้ากลุ่มแรก ทั้ง price และ bg (ชิดขอบ panel อยู่แล้ว · ผู้ใช้ 24 ต.ค. 2026)
    for _nm,_m in [('ปรับราคา',_pp101),('พื้นหลัง',_bg101)]:
        if _m:
            _b=_m.group(0); _ir=_b.find('thcp-row')
            if _ir>=0:
                _ic=_b.find('thcp-cat',_ir); _is=_b.find('thcp-sep',_ir)
                if _is>=0 and _ic>=0 and _is<_ic:
                    errors.append('lint #101: panel '+_nm+' ห้ามมีเส้นคั่นนำหน้ากลุ่มแรก (ชิดขอบ panel อยู่แล้ว)')
    # needScope ไม่โชว์เป็นข้อความ preview (ลอยเดี่ยว ผู้ใช้ไม่เอา · ปุ่มที่ปิดอยู่คือ signifier แล้ว)
    _mp=re.search(r'var err=_bulkPriceCheck\(v\);\s*\n\s*if\(err\)\{([^\n]*)\}', txt)
    if _mp and "needScope" not in _mp.group(1):
        errors.append('lint #101: preview ปรับราคาต้องซ่อนข้อความ needScope (โชว์ค่าว่างแทน — ไม่ลอยเดี่ยว)')
    # i18n ครบ 4 key กลุ่มใหม่ (TH+EN = 2 ครั้ง)
    for _k in ['bg.grpColorImg','bg.grpDim','bg.grpContent','bg.menuShort']:
        if txt.count("'"+_k+"':'")<2:
            errors.append('lint #101: i18n key '+_k+' ต้องมีครบทั้ง TH+EN')

    # ---- 102) ตีม ขาว-ดำ (bw) ต้องล้างขอบตัวอักษรหัวกลุ่ม (text-shadow:none) — ตัวขาวบนพื้นดำ ขอบขาวทำให้เป็นก้อนทึบ (ผู้ใช้ 24 ต.ค. 2026) ----
    _m102=re.search(r':root\[data-theme="bw"\] \.sec-h \.sechead \*\{([^}]*)\}', _css)
    if not _m102:
        errors.append('lint #102: ไม่พบ bw override .sec-h .sechead *')
    elif 'text-shadow:none' not in _m102.group(1):
        errors.append('lint #102: ตีม bw ต้องมี text-shadow:none !important (เอาขอบขาวรอบหัวกลุ่มออก — กันก้อนขาวทึบบนพื้นดำ)')

    # ---- 103) ปุ่มเครื่องมือใน panel (.ep-mini / #bgFit) ต้องบาง: font-weight:400 + สีไม่เข้มเกิน (#605e5c เท่าป้าย ไม่ใช่ #3a3937 ที่ตาอ่านเป็นหนา) ทุก panel (ผู้ใช้ 24 ต.ค. 2026) ----
    for _m103 in re.finditer(r'\.ep-mini\{([^}]*)\}', _css):
        _bd=_m103.group(1)
        if 'font-weight:400' not in _bd:
            errors.append('lint #103: .ep-mini ต้องมี font-weight:400 (ปุ่ม panel บาง ไม่หนา)')
        if 'color:#3a3937' in _bd:
            errors.append('lint #103: .ep-mini ห้ามสีเข้ม #3a3937 (ตาอ่านเป็นหนา — ใช้ #605e5c เท่าป้าย)')
    _mbgf=re.search(r'#edpanel #bgFit\{([^}]*)\}', _css)
    if _mbgf:
        if 'font-weight:400' not in _mbgf.group(1):
            errors.append('lint #103: #bgFit ต้องมี font-weight:400')
        if 'color:#3a3937' in _mbgf.group(1):
            errors.append('lint #103: #bgFit ห้ามสีเข้ม #3a3937 (ใช้ #605e5c)')

    # ---- 104) ปุ่ม action/ยืนยันใน panel (.ep-ok/.ep-cancel/.ep-clearonly/.cp-dlg-ok/.ep-goset) ต้องบาง font-weight:400 เท่าปุ่มอื่นใน panel — ไม่มี 600 (ผู้ใช้ 24 ต.ค. 2026: ปุ่มปรับราคายังหนา ข้ามไป) ----
    for _sel104,_rule104 in [('.ep-ok','#edpanel .ep-ok{'),('.ep-cancel','#edpanel .ep-cancel{'),('.ep-clearonly','#edpanel .ep-clearonly{'),('.cp-dlg-ok','#edpanel .cp-dlg-ok{'),('.ep-goset','#edpanel .ep-goset{')]:
        _m104=re.search(re.escape(_rule104)+r'([^}]*)\}', _css)
        if not _m104:
            errors.append('lint #104: ไม่พบ CSS rule '+_sel104)
        else:
            _b104=_m104.group(1)
            if 'font-weight:400' not in _b104:
                errors.append('lint #104: '+_sel104+' ต้อง font-weight:400 (ปุ่ม panel บาง ไม่หนา)')
            if 'font-weight:600' in _b104 or 'font-weight:500' in _b104:
                errors.append('lint #104: '+_sel104+' ห้าม font-weight 500/600 (ปุ่ม panel ต้องบางเท่ากันหมด)')

    # ---- 105) ปุ่ม action ระดับ toolbar ใน panel (.ep-ok/.ep-cancel/.ep-clearonly) ต้อง font-size:16px เท่า .ep-mini (ผู้ใช้ 24 ต.ค. 2026: ปุ่มปรับราคา 14px ไม่เท่าปุ่มอื่น) · cp-dlg/cp-ok (กล่องสี) + ep-goset (inline preview) คนละบริบท ไม่รวม ----
    for _sel105,_rule105 in [('.ep-ok','#edpanel .ep-ok{'),('.ep-cancel','#edpanel .ep-cancel{'),('.ep-clearonly','#edpanel .ep-clearonly{')]:
        _m105=re.search(re.escape(_rule105)+r'([^}]*)\}', _css)
        if not _m105:
            errors.append('lint #105: ไม่พบ CSS rule '+_sel105)
        elif 'font-size:16px' not in _m105.group(1):
            errors.append('lint #105: '+_sel105+' ต้อง font-size:16px (ปุ่ม toolbar ใน panel เท่า .ep-mini)')

    # ---- 106) ปุ่ม action (.ep-btns) ต้อง align-self:flex-start — อยู่ระดับแถว control ไม่ลอยกลางความสูงรวมของ panel (panel 2 ชั้น: control บน + label ล่าง) · ผู้ใช้เลือก align แถว control 24 ต.ค. 2026 ----
    _m106=re.search(r'#edpanel \.ep-btns\{([^}]*)\}', _css)
    if not _m106:
        errors.append('lint #106: ไม่พบ #edpanel .ep-btns')
    elif 'align-self:flex-start' not in _m106.group(1):
        errors.append('lint #106: .ep-btns ต้อง align-self:flex-start (ปุ่ม action ตรงแถว control ไม่ลอยกลางความสูง panel)')

    # ---- 107) พรีวิวเพิ่มหน้า (pnl.addPagePreview) ต้องสั้น: บอกเฉพาะผลรวม {sum} ไม่เล่าย้อน 'ตอนนี้/เพิ่ม/ลูกศร' (ผู้ใช้ 24 ต.ค. 2026: ตอนนี้ X/เพิ่ม Y ซ้ำกับที่เห็นบนจอแล้ว) ----
    _m107=re.findall(r"'pnl\.addPagePreview':'([^']*)'", txt)
    if not _m107:
        errors.append('lint #107: ไม่พบ pnl.addPagePreview')
    for _v107 in _m107:
        if '{sum}' not in _v107:
            errors.append('lint #107: addPagePreview ต้องมี {sum} (ผลรวมสุดท้าย)')
        if '→' in _v107 or 'ตอนนี้ {total}' in _v107 or '{total} now' in _v107:
            errors.append('lint #107: addPagePreview ต้องไม่เล่าย้อน (ห้าม → / ตอนนี้ {total} / {total} now) — บอกเฉพาะผลรวม')

    # ---- 108) บรรทัดพรีวิวใน panel (.ep-preview) ต้อง font-size:16px (ผู้ใช้ 24 ต.ค. 2026: 'รวมเป็น N หน้า' เป็น 16) ----
    _m108=re.search(r'#edpanel \.ep-preview\{([^}]*)\}', _css)
    if not _m108:
        errors.append('lint #108: ไม่พบ #edpanel .ep-preview')
    elif 'font-size:16px' not in _m108.group(1):
        errors.append('lint #108: .ep-preview ต้อง font-size:16px')

    # ---- 109) custom dropdown ธีม + live preview (ผู้ใช้ 24 ต.ค. 2026): ชี้/เลื่อน=ดูจริง, คลิก=ยืนยัน, Esc/นอก/ปิด=คืนเดิม ----
    for _fn109 in ('function _themePreviewVisual(','function _themeDdHtml(','function _themeDdToggle(','function _themeDdOpen(','function _themeDdClose(','function _themeDdPreview(','function _themeDdCommit(','function _themeDdKey(','var _THEME_ORDER='):
        if _fn109 not in txt: errors.append('lint #109: ไม่พบ '+_fn109+' (custom dropdown ธีม live preview)')
    if '_themePreviewVisual(committed)' not in txt:
        errors.append('lint #109: ปิด dropdown ไม่ยืนยันต้องคืนธีมเดิม (_themePreviewVisual committed)')
    if '.ep-dd-pop' not in _css:
        errors.append('lint #109: ไม่พบ CSS .ep-dd-pop')

    # ---- 110) เส้นคั่นใต้ส่วนหัว (.rule): สีตามตีม var(--line-dot) ไม่ฝัง #c9a227 + ซ่อนได้จอ+พิมพ์ (html[data-rulehide], ติดไปกับไฟล์) + ปุ่ม btnRuleHide แท็บหน้า active เขียว (ผู้ใช้ 24 ต.ค. 2026) ----
    _mr110=re.search(r'\.rule\{([^}]*)\}', _css)
    if not _mr110:
        errors.append('lint #110: ไม่พบ .rule')
    else:
        if 'var(--line-dot)' not in _mr110.group(1):
            errors.append('lint #110: .rule ต้องใช้ var(--line-dot) (สีตามตีม)')
        if '#c9a227' in _mr110.group(1):
            errors.append('lint #110: .rule ห้ามฝังสีทอง #c9a227 (ต้องตามตีม)')
    if 'html[data-rulehide] .rule' not in _css:
        errors.append('lint #110: ไม่พบ html[data-rulehide] .rule (ซ่อนเส้น จอ+พิมพ์)')
    if 'function _ruleHideSync(' not in txt: errors.append('lint #110: ไม่พบ function _ruleHideSync(')
    if '#edbar #btnLineEdge.on' not in _css:
        errors.append('lint #110: btnLineEdge ไม่มี active เขียว (ข้อ 11)')
    if 'function openLineEdgePanel(' not in txt:
        errors.append('lint #110: ไม่พบ openLineEdgePanel (ปุ่มเส้น·ขอบเปิดพาเนลรวม)')
    if 'id="btnLineEdge"' not in txt:
        errors.append('lint #110: ไม่พบปุ่ม btnLineEdge')
    if '_ruleHideSync();' not in txt:
        errors.append('lint #110: ไม่เรียก _ruleHideSync() ตอนเปิดแอป')
    if txt.count("'grp.rule':'")<2: errors.append('lint #110: i18n grp.rule ไม่ครบ TH+EN')

    # ---- 111) @media print ต้อง reset body min-width:0 (body มี min-width:960px สำหรับจอแคบ แต่ถ้าไม่ปลดตอนพิมพ์ body=254mm เกิน A4 210mm -> Chrome ย่อทั้งหน้าชิดมุมซ้ายบน = พิมพ์ไม่เต็ม · ผู้ใช้ 25 ต.ค. 2026) ----
    _mp111=re.search(r'@media print\{body\{([^}]*)\}', _css)
    if not _mp111:
        errors.append('lint #111: ไม่พบ @media print body rule')
    else:
        _b111=_mp111.group(1)
        if 'min-width:0' not in _b111:
            errors.append('lint #111: @media print body ต้อง min-width:0 !important (กัน body 960px ย่อหน้าตอนพิมพ์ไม่เต็ม A4)')

    # ---- 112) ขอบกล่องปรับได้ (ความหนา+แบบเส้น) อิสระจากตีม + คุมเส้นใต้หัวกลุ่มด้วย (ผู้ใช้ 25 ต.ค. 2026) ----
    _mcrab=re.search(r'\.crab\{([^}]*)\}', _css)
    if not _mcrab or 'var(--note-bw' not in _mcrab.group(1):
        errors.append('lint #112: .crab ต้องใช้ var(--note-bw)/var(--note-bs) (ขอบกล่องโน้ตปรับได้)')
    _msec=re.search(r'\.sec\{break-inside:avoid;([^}]*)\}', _css)
    if not _msec or 'var(--grp-bw' not in _msec.group(1):
        errors.append('lint #112: .sec ต้องใช้ var(--grp-bw)/var(--grp-bs) (ขอบกล่องกลุ่มปรับได้)')
    _msh112=re.search(r'\.sec-h\{([^}]*)\}', _css)
    if not _msh112 or 'border-bottom:var(--grp-bw' not in _msh112.group(1):
        errors.append('lint #112: .sec-h เส้นใต้หัวกลุ่มต้องใช้ var(--grp-bw) ด้วย (คุมไปพร้อมกล่องกลุ่ม)')
    for _f112 in ('function _lineEdgeRenderPanel(','function _borderSet(','function _borderVal(','var _BORDER_WIDTHS=','var _BORDER_STYLES='):
        if _f112 not in txt: errors.append('lint #112: ไม่พบ '+_f112)
    if 'note-bw' not in txt or 'grp-bw' not in txt:
        errors.append('lint #112: พาเนลเส้น·ขอบไม่ได้คุมขอบกล่องโน้ต/กลุ่ม')
    for _k112 in ('th.edgeW','th.edgeS','th.grpNoteEdge','th.grpGrpEdge','th.bsSolid','th.bsDashed','th.bsDotted','th.bsNone'):
        if txt.count("'"+_k112+"':'")<2: errors.append('lint #112: i18n '+_k112+' ไม่ครบ TH+EN')

    # ---- 113) เส้นคั่นปรับได้ (หนา --rule-h ถึง 8px + แบบ ไล่เฉด/ทึบ/ประ/จุด/ไม่มี ผ่าน data-rule-style) + ขอบกล่องหนาถึง 5px + ความโค้งมุม --note-radius/--grp-radius (ผู้ใช้ 25 ต.ค. 2026) ----
    _mrule113=re.search(r'\.rule\{([^}]*)\}', _css)
    if not _mrule113 or 'var(--rule-h' not in _mrule113.group(1):
        errors.append('lint #113: .rule ต้องใช้ var(--rule-h) (เส้นคั่นปรับความหนาได้)')
    for _rs113 in ('solid','dashed','dotted'):
        if ('html[data-rule-style="'+_rs113+'"] .rule') not in _css:
            errors.append('lint #113: ไม่พบ rule-style '+_rs113+' (เส้นคั่นแบบเส้น)')
    _mcrab113=re.search(r'\.crab\{([^}]*)\}', _css)
    if not _mcrab113 or 'var(--note-radius' not in _mcrab113.group(1):
        errors.append('lint #113: .crab ต้องใช้ var(--note-radius) (ความโค้งมุมกล่องโน้ต)')
    _msec113=re.search(r'\.sec\{break-inside:avoid;([^}]*)\}', _css)
    if not _msec113 or 'var(--grp-radius' not in _msec113.group(1):
        errors.append('lint #113: .sec ต้องใช้ var(--grp-radius) (ความโค้งมุมกล่องกลุ่ม)')
    for _f113 in ('function _ruleStyleSet(','function _ruleStyleApply(','function _ruleCur(','function _edgeDdBtn(','function _edgeDdCfg(','var _RULE_WIDTHS=','var _RULE_STYLES=','var _RADIUS_VALS='):
        if _f113 not in txt: errors.append('lint #113: ไม่พบ '+_f113)
    if "'8px'" not in re.search(r'var _RULE_WIDTHS=\[([^\]]*)\]', txt).group(1):
        errors.append('lint #113: _RULE_WIDTHS ต้องมีถึง 8px')
    if "'5px'" not in re.search(r'var _BORDER_WIDTHS=\[([^\]]*)\]', txt).group(1):
        errors.append('lint #113: _BORDER_WIDTHS ต้องขยายถึง 5px')
    if "_edgeDdBtn('note-radius')" not in txt or "_edgeDdBtn('grp-radius')" not in txt:
        errors.append('lint #113: พาเนลเส้น·ขอบต้องมีมุมโค้งทั้งกล่องโน้ตและกล่องกลุ่ม')
    if "_edgeDdBtn('rule-style')" not in txt or "_edgeDdTrigSet('rule-style',_ruleCur())" not in txt:
        errors.append('lint #113: พาเนลต้องมีแบบเส้นคั่นส่วนหัว และ sync ป้ายกับสถานะจริง (_ruleHideSync)')
    if _mrule113 and 'max-width:70%' in _mrule113.group(1):
        errors.append('lint #113: .rule ห้าม max-width:70% (เส้นคั่น header ยืดเต็มความกว้างเนื้อหา · ผู้ใช้ 25 ต.ค. 2026)')
    _mle113=re.search(r'function _lineEdgeRenderPanel\(\)\{[\s\S]*?openPanel\(\{mode', txt)
    if _mle113 and _mle113.group(0).rfind('thcp-sep') < _mle113.group(0).rfind('data-i18n="th.grpGrpEdge"'):
        errors.append('lint #113: พาเนลเส้น·ขอบต้องมีเส้นคั่นปิดท้ายกลุ่มสุดท้าย (เข้าชุดพาเนลปรับราคา/พื้นหลัง)')
    for _k113 in ('th.edgeR','th.bsGradient'):
        if txt.count("'"+_k113+"':'")<2: errors.append('lint #113: i18n '+_k113+' ไม่ครบ TH+EN')

    # ---- 114) ระบบเลย์เอาต์ (เท็มเพลต เฟส 1): default 2col(A) + 1col(B) ผ่าน :root[data-layout] · แท็บเท็มเพลต + ปุ่มเลือก active เขียว · measuring override กัน overflow เพี้ยน · ติดไฟล์ (ผู้ใช้ 26 ต.ค. 2026) ----
    if ':root[data-layout="1col"] .grid' not in _css:
        errors.append('lint #114: ไม่พบ CSS :root[data-layout="1col"] .grid (Layout B)')
    if ':root[data-layout="3col"] .grid' not in _css or 'column-count:3' not in _css:
        errors.append('lint #114: ไม่พบ CSS 3col (column-count:3 · Layout C)')
    if ':root[data-layout="3col"] .col' not in _css or 'display:contents' not in _css:
        errors.append('lint #114: 3col ต้องมี .col{display:contents} (ยก .sec เป็น flow items)')
    _msecbi=re.search(r'\.sec\{break-inside:avoid', _css)
    if not _msecbi:
        errors.append('lint #114: .sec ต้องมี break-inside:avoid (กันกลุ่มแตกข้ามคอลัมน์ใน 3col)')
    if 'id="btnLayout_3col"' not in txt:
        errors.append('lint #114: ไม่พบปุ่ม btnLayout_3col')
    if "'3col'" not in re.search(r'var _LAYOUTS=\[([^\]]*)\]', txt).group(1):
        errors.append('lint #114: _LAYOUTS ต้องมี 3col')
    if txt.count("'lay.3col':'")<2:
        errors.append('lint #114: i18n lay.3col ไม่ครบ TH+EN')
    if ':root[data-layout="1col"] body.measuring .grid' not in _css:
        errors.append('lint #114: ต้อง override measuring ของ 1col เป็น column (กันแบ่งหน้าเพี้ยน)')
    for _f114 in ('var _LAYOUTS=','function _layoutApply(','function _layoutLoad(','function _layoutPick(','function _layoutSyncBtns('):
        if _f114 not in txt: errors.append('lint #114: ไม่พบ '+_f114)
    _p1=txt.find('id="btnLayout_1col"'); _p2=txt.find('id="btnLayout_2col"'); _p3=txt.find('id="btnLayout_3col"')
    if not (0<=_p1<_p2<_p3):
        errors.append('lint #114: ปุ่มเลย์เอาต์ต้องเรียง 1 คอลัมน์ · 2 คอลัมน์ · 3 คอลัมน์ (ผู้ใช้ 27 ต.ค. 2026)')
    for _id114 in ('btnLayout_2col','btnLayout_1col'):
        if ('id="'+_id114+'"') not in txt: errors.append('lint #114: ไม่พบปุ่ม '+_id114)
    if 'data-tab="template"' not in txt: errors.append('lint #114: ไม่พบแท็บ template')
    if 'data-pane="template"' not in txt: errors.append('lint #114: ไม่พบ rpane template')
    if '#edbar #btnLayout_2col.on' not in _css: errors.append('lint #114: ปุ่มเลย์เอาต์ไม่มี active เขียว (ข้อ 11)')
    if '_layoutLoad();' not in txt: errors.append('lint #114: ไม่เรียก _layoutLoad() ตอนเปิดแอป')
    for _k114 in ('tab.template','lay.2col','lay.1col','grp.layout','fl.layoutSet'):
        if txt.count("'"+_k114+"':'")<2: errors.append('lint #114: i18n '+_k114+' ไม่ครบ TH+EN')

    # ---- 115) ซ่อนกล่องโน้ต/ป้ายหน้า (เพิ่มพื้นที่เมนู): data-notehide/data-plabelhide บน <html> จอ+พิมพ์+ติดไฟล์ · ปุ่ม toggle ในแท็บเท็มเพลต active เขียว (ผู้ใช้ 26 ต.ค. 2026) ----
    if 'html[data-notehide] .crab' not in _css:
        errors.append('lint #115: ไม่พบ html[data-notehide] .crab (ซ่อนกล่องโน้ต)')
    if 'html[data-plabelhide] .pagelabel' not in _css:
        errors.append('lint #115: ไม่พบ html[data-plabelhide] .pagelabel (ซ่อนป้ายหน้า)')
    if 'html[data-notehide][data-plabelhide] .noterow' not in _css:
        errors.append('lint #115: ซ่อนทั้งคู่ต้องซ่อน .noterow (คืน margin)')
    for _f115 in ('function _noteHideSync(','function toggleNoteHide(','function togglePageLabelHide('):
        if _f115 not in txt: errors.append('lint #115: ไม่พบ '+_f115)
    for _id115 in ('btnNoteHide','btnPLabelHide'):
        if ('id="'+_id115+'"') not in txt: errors.append('lint #115: ไม่พบปุ่ม '+_id115)
    if '#edbar #btnNoteHide.on' not in _css: errors.append('lint #115: ปุ่มซ่อนโน้ต/ป้ายหน้าไม่มี active เขียว (ข้อ 11)')
    if '_noteHideSync();' not in txt: errors.append('lint #115: ไม่เรียก _noteHideSync() ตอนเปิดแอป')
    for _k115 in ('btn.noteHide','btn.noteShow','btn.plabelHide','btn.plabelShow','grp.show'):
        if txt.count("'"+_k115+"':'")<2: errors.append('lint #115: i18n '+_k115+' ไม่ครบ TH+EN')

    # ---- 116) ธีมเรียงตามสี 7 หมวด (แดง·ชมพู/ส้ม·น้ำตาล/เหลือง·ทอง/เขียว/น้ำเงิน·ฟ้า/ม่วง/ขาวดำ) อ่อน->แก่ · ป้ายหมึก น้อย/ปานกลาง/มาก คำนวณจากสีพื้น (ผู้ใช้ 26 ต.ค. 2026) ----
    _mg116=re.search(r"var _THEME_GROUPS=\[(.*?)\];", txt)
    _mo116=re.search(r"var _THEME_ORDER=\[([^\]]*)\]", txt)
    _mt116=re.search(r"var _THEMES=\[([^\]]*)\]", txt)
    _mi116=re.search(r"var _THEME_INK=\{([^}]*)\}", txt)
    if not (_mg116 and _mo116 and _mt116 and _mi116):
        errors.append('lint #116: ไม่พบ _THEME_GROUPS/_THEME_ORDER/_THEMES/_THEME_INK')
    else:
        _gk116=re.findall(r"\['(thg\.[a-z]+)'", _mg116.group(1))
        _gi116=re.findall(r"'([a-z-]+)'", re.sub(r"'thg\.[a-z]+'", "", _mg116.group(1)))
        _oi116=re.findall(r"'([a-z-]+)'", _mo116.group(1))
        _ti116=re.findall(r"'([a-z-]+)'", _mt116.group(1))
        if _gk116!=['thg.red','thg.pink','thg.orange','thg.brown','thg.yellow','thg.green','thg.blue','thg.purple','thg.gray','thg.black']:
            errors.append('lint #116: หมวดธีมต้องเป็น 10 สีหลัก แดง/ชมพู/ส้ม/น้ำตาล/เหลือง/เขียว/น้ำเงิน/ม่วง/เทา/ดำ ตามลำดับ')
        if _oi116[:1]!=['custom'] or _oi116[1:]!=_gi116:
            errors.append('lint #116: _THEME_ORDER ต้อง = custom + ธีมใน _THEME_GROUPS ตามลำดับ (keyboard nav ใช้ลำดับนี้)')
        if sorted(_gi116)!=sorted(_ti116) or len(set(_gi116))!=len(_gi116):
            errors.append('lint #116: ทุกธีมใน _THEMES ต้องอยู่ใน _THEME_GROUPS ครั้งเดียวพอดี')
        _ink116=dict(re.findall(r"'?([a-z-]+)'?:'(lo|mid|hi)'", _mi116.group(1)))
        for _t116 in _ti116:
            _blk116=re.search(r':root\{([^}]*--grp-body-bg[^}]*)\}', _css) if _t116=='cream' else re.search(r':root\[data-theme="'+re.escape(_t116)+r'"\]\{([^}]*)\}', _css)
            if not _blk116:
                errors.append('lint #116: ไม่พบ CSS ธีม '+_t116); continue
            _b116=_blk116.group(1)
            try:
                _bd116=[int(x) for x in re.search(r'--grp-body-bg:([0-9, ]+);', _b116).group(1).split(',')]
                _hd116=[int(x) for x in re.search(r'--grp-head-bg:([0-9, ]+);', _b116).group(1).split(',')]
                _nh116=re.search(r'--note-bg:#([0-9a-fA-F]{6})', _b116).group(1)
                _nt116=[int(_nh116[i:i+2],16) for i in (0,2,4)]
            except Exception:
                errors.append('lint #116: อ่านสีธีม '+_t116+' ไม่ได้'); continue
            _sc116=0.75*(1-sum(_bd116)/765.0)+0.20*(1-sum(_hd116)/765.0)+0.05*(1-sum(_nt116)/765.0)
            _lv116='lo' if _sc116<0.08 else ('mid' if _sc116<0.40 else 'hi')
            if _ink116.get(_t116)!=_lv116:
                errors.append('lint #116: ป้ายหมึกธีม '+_t116+' ต้องเป็น '+_lv116+' (คำนวณได้ '+('%.3f'%_sc116)+') แต่ _THEME_INK เป็น '+str(_ink116.get(_t116)))
    if 'ep-dd-grp' in txt or 'ep-dd-empty' in txt:
        errors.append('lint #116: dropdown ธีมต้องไม่มีหัวหมวด/เส้นคั่น (ผู้ใช้ 27 ต.ค. 2026)')
    if '#edpanel .ep-dd-ink' not in _css or 'class="ep-dd-ink ink-' not in txt:
        errors.append('lint #116: dropdown ธีมต้องมีป้ายหมึก .ep-dd-ink')
    if "_THEME_INK[id]==='hi'" not in txt:
        errors.append('lint #116: เลือกธีมหมึกมากต้องเตือนในแถบล่าง (fl.themeInkHi)')
    for _t116 in ('navy-dark','wine-dark','mono-dark','forest-dark','coffee-dark','purple-dark','pink-dark','orange-dark'):
        if (':root[data-theme="'+_t116+'"] .crab b') not in _css:
            errors.append('lint #116: ธีมพื้นเข้ม '+_t116+' ต้อง override สีตัวหนังสือกล่องโน้ต')
    for _t116 in ('vivid-red','vivid-blue','vivid-green','mono-dark','navy-dark','wine-dark','vivid-orange','vivid-purple','forest-dark','coffee-dark','purple-dark','vivid-pink','pink-dark','orange-dark','vivid-brown'):
        if (':root[data-theme="'+_t116+'"] .sec-h .sechead *') not in _css:
            errors.append('lint #116: ธีม '+_t116+' ต้อง override สีหัวกลุ่ม')
    for _k116 in ('ink.lo','ink.mid','ink.hi','fl.themeInkHi'):
        if txt.count("'"+_k116+"':'")<2: errors.append('lint #116: i18n '+_k116+' ไม่ครบ TH+EN')
    if re.search(r"'thg\.[a-z]+':'", txt):
        errors.append('lint #116: ห้ามมี i18n หมวดสี thg.* (ไม่ได้แสดงแล้ว ผู้ใช้ 27 ต.ค. 2026)')

    # ---- 117) ตัวกรองธีม ประเภท + กลุ่มสี (ผู้ใช้ 26 ต.ค. 2026) · _THEME_TYPE ครอบทุกธีมครั้งเดียว · คีย์บอร์ดเดินตามรายการที่แสดงจริง ----
    _mty117=re.search(r"var _THEME_TYPE=\{([^}]*)\}", txt)
    _mth117=re.search(r"var _THEMES=\[([^\]]*)\]", txt)
    if not _mty117 or not _mth117:
        errors.append('lint #117: ไม่พบ _THEME_TYPE / _THEMES')
    else:
        _ty117=re.findall(r"'([a-z-]+)':'([a-z]+)'", _mty117.group(1))
        _th117=re.findall(r"'([a-z-]+)'", _mth117.group(1))
        if sorted(k for k,v in _ty117)!=sorted(_th117) or len(_ty117)!=len(set(k for k,v in _ty117)):
            errors.append('lint #117: _THEME_TYPE ต้องครอบทุกธีมใน _THEMES ครั้งเดียวพอดี')
        _bad117=[k for k,v in _ty117 if v not in ('vivid','pastel','dark','muted')]
        if _bad117: errors.append('lint #117: ประเภทธีมไม่ถูกต้อง '+','.join(_bad117))
    for _f117 in ('function _themeDdListHtml(','function _themeFltHtml(','function _themeFltSet(','var _themeFlt='):
        if _f117 not in txt: errors.append('lint #117: ไม่พบ '+_f117)
    if 'id="themeFltType"' not in txt or 'themeFltColor' in txt or '_themeFlt.color' in txt:
        errors.append('lint #117: แผงธีมต้องมีตัวกรองประเภทอย่างเดียว — ช่องสีถูกเอาออก (ผู้ใช้ 27 ต.ค. 2026)')
    if "var ids=_THEME_ORDER" in txt:
        errors.append('lint #117: คีย์บอร์ดใน dropdown ธีมต้องเดินตามรายการที่แสดงจริง ไม่ใช่ _THEME_ORDER ทั้งหมด')
    for _f117 in ('function _themeFltMatch(','function _themeFltFirst('):
        if _f117 not in txt: errors.append('lint #117: ไม่พบ '+_f117)
    if "var nid=!_themeFltMatch(_theme) ? _themeFltFirst() : null;" not in txt or "_themePick(nid)" not in txt:
        errors.append('lint #117: เปลี่ยนตัวกรองแล้วธีมปัจจุบันไม่ตรง ต้องเปลี่ยนเป็นธีมแรกที่ตรง (ยกเว้นกำหนดเอง)')
    # 117b) ทุกช่อง ประเภท x สี (ยกเว้นหมวดขาวดำ) ต้องมีธีมอย่างน้อย 1 ตัว (ผู้ใช้ 26 ต.ค. 2026 เลือก "เติมให้ครบทุกช่อง")
    if _mty117:
        _tm117=dict(re.findall(r"'([a-z-]+)':'([a-z]+)'", _mty117.group(1)))
        _mg117=re.search(r"var _THEME_GROUPS=\[(.*?)\];", txt)
        if _mg117:
            for _gk117,_gl117 in re.findall(r"\['(thg\.[a-z]+)',\[([^\]]*)\]\]", _mg117.group(1)):
                if _gk117 in ('thg.gray','thg.black'): continue  # เทา/ดำ ไม่มีสี (achromatic) ไม่ต้องครบทุกประเภท
                _ids117=re.findall(r"'([a-z-]+)'", _gl117)
                for _ty117b in ('vivid','pastel','dark','muted'):
                    if not any(_tm117.get(_i)==_ty117b for _i in _ids117):
                        errors.append('lint #117: ช่องประเภท '+_ty117b+' x สี '+_gk117+' ไม่มีธีม')
    # 117c) สีมีโครมา 8 สี: สีแท้ (สีหลัก) >=1 · พาสเทล >=3 · หม่น >=1 · พื้นเข้ม >=1 (ผู้ใช้ 26 ต.ค. 2026 เลือก "พาสเทล 3 ประเภทอื่น 1") · พาสเทลต้องหมึกน้อย
    if _mty117:
        _tm117c=dict(re.findall(r"'([a-z-]+)':'([a-z]+)'", _mty117.group(1)))
        _mg117c=re.search(r"var _THEME_GROUPS=\[(.*?)\];", txt)
        _mi117c=re.search(r"var _THEME_INK=\{([^}]*)\}", txt)
        _ink117c=dict(re.findall(r"'([a-z-]+)':'(lo|mid|hi)'", _mi117c.group(1))) if _mi117c else {}
        if _mg117c:
            for _gk117c,_gl117c in re.findall(r"\['(thg\.[a-z]+)',\[([^\]]*)\]\]", _mg117c.group(1)):
                if _gk117c in ('thg.gray','thg.black'): continue
                _ids117c=re.findall(r"'([a-z-]+)'", _gl117c)
                _np117c=sum(1 for _i in _ids117c if _tm117c.get(_i)=='pastel')
                if _np117c<3: errors.append('lint #117: สี '+_gk117c+' ต้องมีพาสเทลอย่างน้อย 3 ธีม (มี '+str(_np117c)+')')
                for _i in _ids117c:
                    if _tm117c.get(_i)=='pastel' and _ink117c.get(_i)!='lo':
                        errors.append('lint #117: ธีมพาสเทล '+_i+' ต้องหมึกน้อย')
    if "var _fd=(_theme==='custom')" in txt or "if(_theme==='custom') return;  /* กันไว้อีกชั้น" in txt or "_themeFlt.type=''; }" in txt:
        errors.append('lint #117: ตัวกรองประเภทต้องเป็นอิสระ ห้ามล็อก/รีเซ็ตเมื่อเป็นธีมกำหนดเอง (ผู้ใช้ 27 ต.ค. 2026)')
    # 117d) กำหนดเอง แสดงเฉพาะประเภท ทั้งหมด · เลือกประเภทตอนกำหนดเอง -> เปลี่ยนเป็นธีมแรกของประเภท · จำสีกำหนดเองไว้ (ผู้ใช้ 27 ต.ค. 2026)
    if "if(id==='custom') return !_themeFlt.type;" not in txt or "if(_themeFltMatch('custom')) html+=opt('custom');" not in txt:
        errors.append('lint #117: กำหนดเองต้องแสดงเฉพาะประเภท ทั้งหมด')
    for _f117d in ('function _themeCustomStash(','function _themeCustomStashSet(','function _themeCustomStashClear('):
        if _f117d not in txt: errors.append('lint #117: ไม่พบ '+_f117d+' (จำสีกำหนดเอง)')
    _mc117d=re.search(r'function _themeClearCustomInline\(\)\{[^\n]*', txt)
    if not _mc117d or 'removeItem' in _mc117d.group(0) or 'StashClear' in _mc117d.group(0):
        errors.append('lint #117: _themeClearCustomInline ต้องล้างเฉพาะสีบนหน้า ห้ามลบสีกำหนดเองที่จำไว้')
    if "var st=_themeCustomStash()" not in txt or "_themeFlt.type='';  /* กำหนดเองไม่มีประเภท" not in txt:
        errors.append('lint #117: เลือกกำหนดเองต้องคืนสีที่จำไว้ และรีเซ็ตประเภทเป็น ทั้งหมด')
    if "_themeFltSet" in txt and re.search(r'id="themeFltType"[^>]*disabled', txt):
        errors.append('lint #117: ตัวกรองประเภทห้าม disabled')
    # 117e) ช่องประเภทแสดงจำนวนธีม นับจากข้อมูลจริง (ผู้ใช้ 27 ต.ค. 2026)
    if 'function _themeFltN(' not in txt or "' ('+_themeFltN(v)+')</option>'" not in txt:
        errors.append('lint #117: ตัวเลือกประเภทต้องแสดงจำนวนธีม (นับด้วย _themeFltN ห้ามเขียนตัวเลขตายตัว)')
    for _k117 in ('tht.vivid','tht.pastel','tht.dark','tht.muted','flt.type','flt.all'):
        if txt.count("'"+_k117+"':'")<2: errors.append('lint #117: i18n '+_k117+' ไม่ครบ TH+EN')
    for _k117 in ('flt.color','flt.none'):
        if ("'"+_k117+"':'") in txt: errors.append('lint #117: ลบ i18n '+_k117+' ไม่หมด (ช่องสีถูกเอาออก)')

    # 118) รายการธีม (dropdown) ยืดตามพื้นที่จอจริง ห้ามความสูงตายตัว (ผู้ใช้ 27 ต.ค. 2026)
    _m118=re.search(r'#edpanel \.ep-dd-pop\{[^}]*\}', txt)
    if not _m118 or re.search(r'max-height:\s*\d+px', _m118.group(0)):
        errors.append('lint #118: .ep-dd-pop ห้ามใช้ max-height เป็น px ตายตัว (ต้องคำนวณจากพื้นที่จอ)')
    _f118=re.search(r'function _themeDdFit\(\)\{.*?\n\}', txt, re.S)
    if not _f118 or 'edstatus' not in _f118.group(0) or 'innerHeight' not in _f118.group(0) or 'maxHeight' not in _f118.group(0):
        errors.append('lint #118: ไม่พบ _themeDdFit ที่คำนวณจากขอบแถบสถานะ/ความสูงหน้าต่าง')
    _o118=re.search(r'function _themeDdOpen\(\)\{.*?\n\}', txt, re.S)
    if not _o118 or not re.search(r"pop\.classList\.add\('open'\);\s*_themeDdFit\(\);", _o118.group(0)) or "window.addEventListener('resize',_themeDd.onRes)" not in _o118.group(0):
        errors.append('lint #118: _themeDdOpen ต้องเรียก _themeDdFit และฟัง resize')
    if "window.removeEventListener('resize',_themeDd.onRes)" not in txt:
        errors.append('lint #118: ต้องถอด resize listener ตอนปิดรายการธีม')

    # 119) ป้ายประเภท หม่น อมเทา ต้องมีเว้นวรรค ให้อ่านง่าย (ผู้ใช้ 27 ต.ค. 2026)
    if "'tht.muted':'หม่น อมเทา'" not in txt or "'tht.muted':'หม่นอมเทา'" in txt:
        errors.append('lint #119: ป้ายประเภท tht.muted (TH) ต้องเป็น หม่น อมเทา (มีเว้นวรรค)')

    # ---- 118) สีกระดาษ แยกจากธีม (ผู้ใช้ 27 ต.ค. 2026): ครีมเดิมทุกธีม · ช่อง พื้นกระดาษ ในแผงธีม · ตัวอักษรบนกระดาษสลับอัตโนมัติ ----
    if 'background:var(--page-bg);' not in _css or 'linear-gradient(#fbf8f3' in _css or 'background:#fbf8f3' in _css:
        errors.append('lint #118: .page ต้องใช้ var(--page-bg) ห้ามล็อก #fbf8f3 ตรงๆ')
    _mr118=re.search(r':root\{([^}]*--grp-body-bg[^}]*)\}', _css)
    if not _mr118 or '--page-bg:#fbf8f3' not in _mr118.group(1):
        errors.append('lint #118: ค่าเริ่มต้นกระดาษต้องเป็นครีม #fbf8f3 ใน :root')
    for _bk118 in re.findall(r':root\[data-theme="[a-z-]+"\]\{([^}]*)\}', _css):
        if '--page-' in _bk118:
            errors.append('lint #118: ธีมห้ามกำหนดสีกระดาษ/ตัวอักษรบนกระดาษ (กระดาษแยกจากธีม)'); break
    _mv118=re.search(r"var _THEME_VARS=\[([^\]]*)\]", txt)
    if not _mv118 or 'page-' in _mv118.group(1):
        errors.append('lint #118: _THEME_VARS ห้ามมี page-* (ธีมกำหนดเองไม่ดูแลกระดาษ)')
    for _sel118,_v118 in ((r'(?m)^\.brand h1\{([^}]*)\}','var(--page-title)'),(r'(?m)^\.contact \.ph\{([^}]*)\}','var(--page-txt)'),(r'(?m)^\.contact \.lbl\{([^}]*)\}','var(--page-sub)'),(r'(?m)^\.pagelabel\{([^}]*)\}','var(--page-sub)')):
        _m118=re.search(_sel118, _css)
        if not _m118 or _v118 not in _m118.group(1): errors.append('lint #118: '+_sel118+' ต้องใช้ '+_v118)
    for _f118 in ('function _paperSet(','function _paperTextAuto(','function _paperTrigHtml(','function _paperReset(','id="thcpPick_page-bg"',"+_themeDdHtml()+_paperTrigHtml()+"):
        if _f118 not in txt: errors.append('lint #118: ไม่พบ '+_f118)
    if ":root[data-paper] .page{-webkit-print-color-adjust:exact;print-color-adjust:exact;}" not in _css:
        errors.append('lint #118: เลือกสีกระดาษเองต้องพิมพ์สีกระดาษ')
    if "if(_cpThemeVar==='page-bg'){ _thcpOrig=null; _paperSet(hex);" not in txt or "if(_cpThemeVar==='page-bg'){ _paperSet(h);" not in txt:
        errors.append('lint #118: ตกลงสีกระดาษ (ถาด + HSV) ต้องไป _paperSet ไม่ใช่ _themeCustomSet (ห้ามเปลี่ยนธีมเป็นกำหนดเอง)')
    def _l118(h):
        _r=[]
        for _i in (0,2,4):
            _c=int(h[_i:_i+2],16)/255.0
            _r.append(_c/12.92 if _c<=0.03928 else ((_c+0.055)/1.055)**2.4)
        return 0.2126*_r[0]+0.7152*_r[1]+0.0722*_r[2]
    def _c118(a,b):
        _x,_y=_l118(a),_l118(b); return (max(_x,_y)+0.05)/(min(_x,_y)+0.05)
    _dk118=re.search(r"var _PAPER_TXT_DARK=\{([^}]*)\}", txt); _lt118=re.search(r"var _PAPER_TXT_LIGHT=\{([^}]*)\}", txt)
    if not _dk118 or not _lt118:
        errors.append('lint #118: ไม่พบชุดสีตัวอักษรบนกระดาษ เข้ม/สว่าง')
    else:
        _dkv=re.findall(r"#([0-9a-fA-F]{6})", _dk118.group(1)); _ltv=re.findall(r"#([0-9a-fA-F]{6})", _lt118.group(1))
        if any(_c118(_v,'fbf8f3')<4.5 for _v in _dkv): errors.append('lint #118: ชุดเข้มบนครีมต้อง contrast >= 4.5')
        if any(_c118(_v,'1b1816')<4.5 for _v in _ltv): errors.append('lint #118: ชุดสว่างบนกระดาษเข้มต้อง contrast >= 4.5')
    for _k118 in ('th.zPageBg','th.paperReset','fl.paperSet'):
        if txt.count("'"+_k118+"':'")<2: errors.append('lint #118: i18n '+_k118+' ไม่ครบ TH+EN')

    # ---- 119) พาเนลพื้นหลัง: ทุกหน้า = ปุ่มแรกซ้ายสุด + ค่าเริ่มต้น (ผู้ใช้ 27 ต.ค. 2026) ----
    _sc119=re.findall(r'name="pgbgScope" value="([a-z]+)"( checked)?', txt)
    if [v for v,c in _sc119]!=['all','page','odd','even','range'] or [v for v,c in _sc119 if c]!=['all']:
        errors.append('lint #119: ขอบเขตพื้นหลังต้องเรียง ทุกหน้า·เฉพาะหน้านี้·หน้าคี่·หน้าคู่·ระบุ และ ทุกหน้า เป็นค่าเริ่มต้น')

    # ---- 120) ปรับเทียบจอ: % เปลี่ยนทันทีเมื่อพิมพ์นิ้ว/ทาบบัตร · ไม่มีปุ่ม ใช้ค่านี้ · ช่องนิ้วตามแถบบัตร (ผู้ใช้ 27 ต.ค. 2026) ----
    if 'oninput="_calInchFilter(this);_calFromInches()"' not in txt:
        errors.append('lint #120: ช่องนิ้วต้องคำนวณ % ทันทีขณะพิมพ์ (oninput -> _calFromInches)')
    if 'cal.inchbtn' in txt:
        errors.append('lint #120: ลบปุ่ม ใช้ค่านี้ ออกแล้ว (คำนวณทันที ปุ่มไม่มีหน้าที่) ห้ามเหลือ cal.inchbtn')
    if "if(src!=='inch') _calInchSync(w);" not in txt or 'function _calInchSync(' not in txt or "_calSetWidth(diag/din/25.4*_CARD_MM,'inch')" not in txt:
        errors.append('lint #120: ทาบบัตร/ปุ่ม -/+ ต้องอัปเดตช่องนิ้ว และพิมพ์นิ้วต้องไม่เขียนทับช่องที่กำลังพิมพ์')
    if not re.search(r"function _calSetWidth\(w,src\)\{[^\n]*_calReadout\(\);", txt):
        errors.append('lint #120: _calSetWidth ต้องอัปเดต % (_calReadout) ทุกครั้ง')

    # ---- 121) ขนาดเครื่องมือ (A-/A+) ต่ำสุด 80% (ผู้ใช้ 27 ต.ค. 2026) ----
    if not re.search(r"_UIMIN=80,", txt):
        errors.append('lint #121: ขนาดเครื่องมือ A- ต้องลดได้ถึง 80% (_UIMIN=80)')

    # ---- 122) ขนาดเครื่องมือ: คลิก % เปิดรายการ 80-150% (ผู้ใช้ 27 ต.ค. 2026) ----
    if 'id="uiLvl" aria-haspopup="listbox"' not in txt or 'onclick="_uiDdToggle(event)"' not in txt or 'id="uiLvlTxt"' not in txt:
        errors.append('lint #122: ตัวเลข % ต้องเป็นปุ่มเปิดรายการขนาด (#uiLvl + #uiLvlTxt)')
    for _f122 in ('function _ddOpen(','function _ddClose(','function _ddPick(','function _ddKey(','function _ddOutside(','function _ddHl(','function _uiscalePreview(','function _uiScaleList(','function _uiDdCfg('):
        if _f122 not in txt: errors.append('lint #122: ไม่พบ '+_f122)
    if 'for(var v=_UIMIN; v<=_UIMAX; v+=_UISTEP)' not in txt:
        errors.append('lint #122: รายการขนาดต้องสร้างจาก _UIMIN.._UIMAX ห้ามเขียนตัวเลขตายตัว')
    _mp122=re.search(r'function _uiscalePreview\(v\)\{[^\n]*', txt)
    if not _mp122 or '_uiscale=' in _mp122.group(0) or 'localStorage' in _mp122.group(0):
        errors.append('lint #122: ชี้ดูขนาดต้องไม่บันทึกค่า (ห้ามแตะ _uiscale/localStorage ใน _uiscalePreview)')
    if 'document.body.appendChild(pop);' not in txt or 'pop.style.zoom' in txt:
        errors.append('lint #122: รายการต้องอยู่ใน body นอกโซน zoom และไม่ใช้ zoom (กันรายการย่อขยายใต้เมาส์)')
    if "else if(e.key==='Escape'){ e.preventDefault(); e.stopPropagation(); _ddClose(true); }" not in txt:
        errors.append('lint #122: Esc ต้องคืนขนาดเดิม')
    if '#edtabs .uiscalectl #uiLvl.on{background:#217346;color:#fff;border-color:#217346;}' not in _css:
        errors.append('lint #122: ปุ่ม % ตอนรายการเปิดต้องเป็นสีเขียว (ข้อ 11)')
    if '@media print{#uiDdPop{display:none !important;}}' not in _css or "'#uiDdPop','#calModal','#presentBar']" not in txt or "clone.querySelector('#uiDdPop')" not in txt:
        errors.append('lint #122: รายการขนาดต้องไม่พิมพ์ และต้องถูกตัดออกตอนบันทึก')
    if txt.count("'ttl.uiLvl':'")<2: errors.append('lint #122: i18n ttl.uiLvl ไม่ครบ TH+EN')

    # ---- 123) ปรับเทียบจอ ช่องขนาดจอ: ว่าง=คืนค่าก่อนพิมพ์ · นอกช่วง=ไม่ขยับ+บอกช่วง (ผู้ใช้ 27 ต.ค. 2026 แก้บั๊ก 205% ค้าง) ----
    _mf123=re.search(r'function _calFromInches\(\)\{[\s\S]*?\n  _calHintSet\(null\); _calSetWidth', txt)
    if not _mf123:
        errors.append('lint #123: ไม่พบ _calFromInches แบบใหม่')
    else:
        _b123=_mf123.group(0)
        if "if(!(din>0)||!(diag>0)){ _calHintSet(null); if(_calInchBase>0) _calSetWidth(_calInchBase,'inch'); return; }" not in _b123:
            errors.append('lint #123: ช่องขนาดจอว่าง ต้องคืนแถบเป็นค่าก่อนพิมพ์')
        if "if(w<_CAL_MINW||w>_calMaxWidth()){ _calHintSet(_calInchRange()); return; }" not in _b123:
            errors.append('lint #123: ค่าที่แถบแสดงไม่ได้ ต้องไม่ขยับแถบ (ห้าม clamp ไปค้างสุดขอบ) และต้องบอกช่วงที่ใช้ได้')
    if '_calInchBase=w; _calHintSet(null);' not in txt:
        errors.append('lint #123: ทาบบัตร/ปุ่ม/เปิดหน้าต่าง ต้องตั้งค่าก่อนพิมพ์ใหม่ (_calInchBase)')
    if 'id="calInchHint"' not in txt or "_calHintRelang();" not in txt:
        errors.append('lint #123: ต้องมีข้อความช่วงที่ใช้ได้ (#calInchHint) และแปลภาษาใหม่ตอนสลับ TH/EN')
    if 'Math.max(_CAL_MINW,' not in txt:
        errors.append('lint #123: ความกว้างแถบต่ำสุดต้องใช้ _CAL_MINW ที่เดียว (ช่วงนิ้วคำนวณจากค่าเดียวกัน)')
    if txt.count("'cal.inchRange':'")<2 or '{a}' not in txt or '{b}' not in txt:
        errors.append('lint #123: i18n cal.inchRange ไม่ครบ TH+EN')

    # ---- 124) ซูมหน้า A4: ปุ่ม ▾ ข้างช่อง % เปิดรายการสำเร็จรูป ชี้ดูก่อน (ผู้ใช้ 27 ต.ค. 2026) · ใช้ engine เดียวกับขนาดเครื่องมือ (ห้ามเขียนซ้ำ) ----
    if 'id="zoomDd" aria-haspopup="listbox"' not in txt or 'onclick="_zoomDdToggle(event)"' not in txt:
        errors.append('lint #124: ต้องมีปุ่ม ▾ (#zoomDd) ข้างช่อง % ซูม เปิดรายการ')
    if not re.search(r'<span class="a4split"><input id="zoomLvl"[^>]*><button type="button" class="a4caret" id="zoomDd"', txt):
        errors.append('lint #124: ช่อง % ซูมต้องยังพิมพ์ได้ และปุ่ม ▾ ต้องติดกันแบบ split (เหมือน A4 ▾)')
    for _f124 in ('function _zoomPresets(','function _zoomPreview(','function _zoomDdRevert(','function _zoomDdAnchorSet(','function _zoomDdCfg('):
        if _f124 not in txt: errors.append('lint #124: ไม่พบ '+_f124)
    _mp124=re.search(r'function _zoomPreview\(v\)\{[^\n]*', txt)
    if not _mp124 or '_zoom=' in _mp124.group(0) or 'localStorage' in _mp124.group(0):
        errors.append('lint #124: ชี้ดูซูมต้องไม่บันทึกค่า (ห้ามแตะ _zoom/localStorage ใน _zoomPreview)')
    if 'v>=_ZMIN && v<=_ZMAX' not in txt:
        errors.append('lint #124: รายการซูมต้องกรองตาม _ZMIN.._ZMAX')
    if 'sc.scrollTop=a.top; sc.scrollLeft=a.left;' not in txt:
        errors.append('lint #124: ยกเลิกซูมต้องคืนตำแหน่งเลื่อนเดิม')
    if 'function _zoomCommit(z){ if(_dd) _ddClose(true);' not in txt or 'function _uiscaleCommit(z){ if(_dd) _ddClose(true);' not in txt:
        errors.append('lint #124: ปุ่ม +/− หรือ A−/A+ ระหว่างรายการเปิด ต้องปิดรายการและคืนค่าที่ชี้ดูก่อน')
    if txt.count('function _ddOpen(')!=1 or 'function _uiDdOpen(' in txt or 'function _zoomDdOpen(' in txt:
        errors.append('lint #124: รายการชี้ดูก่อนต้องใช้ engine เดียว (_ddOpen) ห้ามเขียนซ้ำ')
    if '#edtabs #zoomDd.on,#edtabs #btnCal.on{' not in _css:
        errors.append('lint #124: ปุ่ม ▾ ซูมตอนรายการเปิดต้องเป็นสีเขียว (ข้อ 11)')
    if '@media print{#zoomDdPop{display:none !important;}}' not in _css or "'#zoomDdPop','#uiDdPop'" not in txt or "clone.querySelector('#zoomDdPop')" not in txt:
        errors.append('lint #124: รายการซูมต้องไม่พิมพ์ และต้องถูกตัดออกตอนบันทึก')
    if txt.count("'ttl.zoomDd':'")<2: errors.append('lint #124: i18n ttl.zoomDd ไม่ครบ TH+EN')

    # ---- 125) ปุ่มพับริบบอน ปุ่มเดียว ขวาสุดถัด TH/EN (ผู้ใช้ 27 ต.ค. 2026 แบบ Google Docs) · ⌃ ซ่อน / ⌄ แสดง · เขียวตอนพับ (ข้อ 11) ----
    if """<button id="langEN" onclick="setLang('en')">EN</button></span><button type="button" id="btnFocus" onclick="toggleFocus()\"""" not in txt:
        errors.append('lint #125: ปุ่มพับริบบอน (#btnFocus) ต้องอยู่ถัดปุ่ม TH/EN ทางขวา')
    if txt.count('id="btnFocus"')!=1 or 'btnRibbonShow' in txt or 'rb-collapse' in txt or '#edribbon #btnFocus' in _css:
        errors.append('lint #125: ต้องมีปุ่มพับริบบอนปุ่มเดียว (ลบ ⌃ มุมริบบอน / ⌄ ห้อย ออกให้หมด)')
    if "p.setAttribute('d', on?'M6 9l6 6 6-6':'M6 15l6-6 6 6')" not in txt or 'id="btnFocusPath" d="M6 15l6-6 6 6"' not in txt:
        errors.append('lint #125: ปุ่มต้องเป็นลูกศรหัวเดียว ⌃ ตอนริบบอนแสดง และสลับเป็น ⌄ ตอนพับ')
    if '#edtabs #btnFocus.on{background:#217346;border-color:#217346;color:#fff;}' not in _css or "b.classList.toggle('on',on);" not in txt:
        errors.append('lint #125: ริบบอนพับ ปุ่มต้องเป็นพื้นเขียว (ข้อ 11)')
    _mr125=re.search(r'#edribbon\{([^}]*)\}', _css)
    if not _mr125 or 'padding:7px 12px;' not in _mr125.group(1):
        errors.append('lint #125: ริบบอนต้องคืน padding เดิม (ไม่ต้องเว้นที่ให้ปุ่มแล้ว)')
    if "ttl.focusOff" in txt or "'btn.focus'" in txt:
        errors.append('lint #125: ห้ามเหลือ i18n เก่า btn.focus / ttl.focusOff')
    if txt.count("'ttl.ribbonShow':'")<2 or "flashStatus('info', tk('fl.ribbonHidden'))" not in txt or txt.count("'fl.ribbonHidden':'")<2:
        errors.append('lint #125: i18n ttl.ribbonShow / fl.ribbonHidden ไม่ครบ TH+EN')
    if "document.addEventListener('DOMContentLoaded',_focusSync); else _focusSync();" not in txt:
        errors.append('lint #125: เปิดไฟล์ต้อง sync สถานะปุ่มกับริบบอน')

    # ---- 126) เส้น·ขอบ ชี้ดูก่อน (ผู้ใช้ 27 ต.ค. 2026 รอบ 3/5): 8 ช่องเป็นรายการ engine _dd · ไม่มี <select> · ชี้ดูไม่ markDirty · Esc คืนค่าเดิม ----
    _mp126=re.search(r'function _lineEdgeRenderPanel\(\)\{[\s\S]*?openPanel\(\{mode', txt)
    if not _mp126 or '<select' in _mp126.group(0):
        errors.append('lint #126: พาเนลเส้น·ขอบต้องไม่มี <select> (ใช้รายการชี้ดูก่อน)')
    else:
        for _k126 in ('rule-h','rule-style','note-bw','note-bs','note-radius','grp-bw','grp-bs','grp-radius'):
            if ("_edgeDdBtn('"+_k126+"')") not in _mp126.group(0): errors.append('lint #126: ขาดรายการ '+_k126)
    _mc126=re.search(r'function _edgeDdCfg\(key\)\{[\s\S]*?\n\}', txt)
    if not _mc126:
        errors.append('lint #126: ไม่พบ _edgeDdCfg')
    else:
        _pv126=re.search(r'preview:function\(v\)\{[^\n]*', _mc126.group(0))
        if not _pv126 or 'markDirty' in _pv126.group(0) or '_borderSet' in _pv126.group(0) or '_ruleStyleSet' in _pv126.group(0):
            errors.append('lint #126: ชี้ดูต้องเปลี่ยนภาพอย่างเดียว ห้าม markDirty/_borderSet/_ruleStyleSet')
        if 'revert:function()' not in _mc126.group(0) or "he.style.removeProperty('--'+key)" not in _mc126.group(0):
            errors.append('lint #126: ยกเลิกต้องคืนค่าเดิม (ไม่มีค่าเดิม = ลบ inline กลับค่าเริ่มต้น)')
    _ma126=re.search(r'function _ruleStyleApply\(val\)\{[^\n]*', txt)
    if not _ma126 or 'markDirty' in _ma126.group(0):
        errors.append('lint #126: _ruleStyleApply ต้องไม่ markDirty')
    for _f126 in ('function _borderWidthOpts(','function _borderStyleOpts(','function _ruleWidthOpts(','function _ruleStyleOpts(','function _radiusOpts(','ruleStyleSel'):
        if _f126 in txt: errors.append('lint #126: ลบของเก่าไม่หมด '+_f126)
    if "onClose:function(){ if(_dd) _ddClose(true); }" not in txt:
        errors.append('lint #126: ปิดพาเนลระหว่างรายการเปิดต้องคืนค่าเดิม')
    if '#edpanel .ep-dd-trigger.ep-edge-dd.on{background:#217346;border-color:#217346;color:#fff;}' not in _css:
        errors.append('lint #126: ปุ่มรายการเส้น·ขอบตอนเปิดต้องเป็นสีเขียว (ข้อ 11)')
    if '@media print{#edgeDdPop{display:none !important;}}' not in _css or "'#edgeDdPop','#zoomDdPop'" not in txt or "clone.querySelector('#edgeDdPop')" not in txt:
        errors.append('lint #126: รายการเส้น·ขอบต้องไม่พิมพ์ และถูกตัดออกตอนบันทึก')
    if txt.count('function _ddOpen(')!=1:
        errors.append('lint #126: ต้องใช้ engine _ddOpen เดียว')

    # ---- 127) กดค้าง −/+ ค่าเปลี่ยนต่อเนื่อง (ผู้ใช้ 27 ต.ค. 2026 รอบ 4/5) ----
    _mh127=re.search(r'var _HOLD_BTNS=\{([\s\S]*?)\n\};', txt)
    if not _mh127:
        errors.append('lint #127: ไม่พบ _HOLD_BTNS')
    else:
        for _id127 in ('typoSizeUp','typoSizeDown','zoomIn','zoomOut','uiIn','uiOut'):
            if ('\n  '+_id127+':{') not in ('\n'+_mh127.group(1)): errors.append('lint #127: ปุ่ม '+_id127+' ต้องกดค้างได้')
            elif ('id="'+_id127+'"') not in txt: errors.append('lint #127: ไม่พบปุ่ม #'+_id127)
    for _f127 in ('function _holdTick(','function _holdStop('):
        if _f127 not in txt: errors.append('lint #127: ไม่พบ '+_f127)
    if "document.addEventListener('mouseup',_holdStop,true);" not in txt or "window.addEventListener('blur',_holdStop);" not in txt:
        errors.append('lint #127: ต้องหยุดเมื่อปล่อยเมาส์และเมื่อหน้าต่างเสียโฟกัส')
    if 'if(c.val()===before || h.btn.disabled){ _holdStop(); return; }' not in txt:
        errors.append('lint #127: ชนขอบต้องหยุด (ค่าไม่เปลี่ยน/ปุ่ม disabled)')
    if '_holdSwallow=_hold.btn;' not in txt:
        errors.append('lint #127: กดค้างแล้วปล่อยต้องกลืน click (ไม่นับเพิ่มอีก 1)')
    _md127=re.search(r"document\.addEventListener\('mousedown',function\(e\)\{\n  if\(e\.button!==0[\s\S]*?\},true\);", txt)
    if not _md127 or 'preventDefault' in _md127.group(0):
        errors.append('lint #127: ตัวจับกดค้างห้าม preventDefault ตอน mousedown (แถบตัวอักษรต้องเก็บข้อความที่เลือกไว้)')

    # ---- 128) หมุนล้อเมาส์บนช่องตัวเลข เฉพาะช่องที่โฟกัส (ผู้ใช้ 27 ต.ค. 2026 รอบ 5/5) ----
    _mw128=re.search(r'var _WHEEL_FIELDS=\{([\s\S]*?)\n\};', txt)
    if not _mw128:
        errors.append('lint #128: ไม่พบ _WHEEL_FIELDS')
    else:
        for _id128 in ('typoSize','zoomLvl','calInch'):
            if ('\n  '+_id128+':function(d)') not in ('\n'+_mw128.group(1)): errors.append('lint #128: ช่อง '+_id128+' ต้องหมุนล้อปรับได้')
        for _no128 in ('ep-amt','ep-price','shdNum'):
            if _no128 in _mw128.group(1): errors.append('lint #128: ห้ามใช้ล้อกับ '+_no128+' (เงิน/เงา)')
    if 'document.activeElement!==el) return;' not in txt:
        errors.append('lint #128: หมุนล้อต้องเปลี่ยนค่าเฉพาะช่องที่โฟกัส (ชี้ผ่านเฉยๆ ต้องเลื่อนหน้าตามปกติ)')
    if "if(e.ctrlKey||e.metaKey) return;\n  var el=e.target;" not in txt:
        errors.append('lint #128: Ctrl+ล้อ ต้องปล่อยให้ซูมหน้าเดิมทำงาน')
    if 'Math.abs(_wheelAcc)>=50' not in txt:
        errors.append('lint #128: ต้องสะสม deltaY เป็นขั้น (ทัชแพดไม่รัว)')
    if txt.count("'ttl.calInchWheel':'")<2:
        errors.append('lint #128: i18n ttl.calInchWheel ไม่ครบ TH+EN')

    # ---- 129) หน้า A4 เปล่า (ผู้ใช้ 27 ต.ค. 2026 ขั้น A · แบบที่ 2): ปุ่มแยก [หน้าเปล่า ▾] ข้าง [เพิ่มหน้า ▾] ทำงานเหมือนกัน · หน้าเปล่าเหลือแค่ .pgbg · หน้าเมนูใหม่คัดจากหน้าเมนูล่าสุด ----
    if 'function _addPagesBatch(n,type){' not in txt or 'function _lastMenuPage(' not in txt:
        errors.append('lint #129: _addPagesBatch ต้องรับแบบหน้า + มี _lastMenuPage')
    if "np.classList.add('pgblank'); Array.prototype.slice.call(np.children).forEach(function(c){ if(!c.classList.contains('pgbg')) c.remove(); });" not in txt:
        errors.append('lint #129: หน้าเปล่าต้องเหลือแค่ .pgbg (ไม่มีหัว/เส้นคั่น/โน้ต/เลขหน้า/กลุ่ม)')
    if "src=blank?last:_lastMenuPage();" not in txt or "flashStatus('warning',tk('fl.addPageNoMenu'))" not in txt:
        errors.append('lint #129: หน้าเมนูใหม่ต้องคัดจากหน้าเมนูล่าสุด (ไม่ใช่หน้าเปล่า) และเตือนเมื่อไม่มีหน้าเมนู')
    if 'function addPage(){ _addPagesBatch(1); }' not in txt or 'id="btnAddPageMore" onclick="openAddPagesPanel()"' not in txt:
        errors.append('lint #129: เพิ่มหน้า ▾ ต้องคงเดิม (ปุ่มหลัก +1 หน้าเมนู · ▾ = panel เพิ่มหลายหน้า)')
    if 'id="btnAddBlank" onclick="addBlankPage()"' not in txt or "function addBlankPage(){ _addPagesBatch(1,'blank'); }" not in txt:
        errors.append('lint #129: ต้องมีปุ่ม หน้าเปล่า (+1 หน้าเปล่าทันที)')
    if """id="btnAddBlankMore" onclick="openAddPagesPanel('blank')\"""" not in txt or "_addPagesBatch(n,_blank?'blank':'menu');" not in txt:
        errors.append('lint #129: หน้าเปล่า ▾ ต้องเปิด panel เพิ่มหลายหน้าเดียวกัน (แบบหน้าเปล่า)')
    if '#edbar #btnAddBlankMore.on' not in _css:
        errors.append('lint #129: ▾ หน้าเปล่าตอน panel เปิดต้องเป็นสีเขียว (ข้อ 11)')
    for _b129 in ('addPgDdPop','_addPgDd','addPgType','opts.preHtml','addPgBlankItem'):
        if _b129 in txt: errors.append('lint #129: ห้ามเหลือของแบบเก่า '+_b129+' (เมนูเลื่อนลง/ตัวเลือก แบบหน้า)')
    for _k129 in ('btn.addBlank','ttl.addBlank','ttl.addBlankMore','pnl.addBlankLabel','fl.addBlank','fl.addBlanks','fl.addPageNoMenu'):
        if txt.count("'"+_k129+"':'")<2: errors.append('lint #129: i18n '+_k129+' ไม่ครบ TH+EN')

    # ---- 130) กล่องข้อความลอย (ผู้ใช้ 27 ต.ค. 2026 ขั้น B · แบบ 1 คลิก=เลือก ดับเบิลคลิก=พิมพ์) ----
    if 'id="btnFtextAdd" onclick="ftextAdd()"' not in txt or 'data-i18n="grp.insert"' not in txt:
        errors.append('lint #130: แท็บข้อความต้องมีปุ่ม กล่องข้อความ (กลุ่ม แทรก)')
    for _f130 in ('function ftextAdd(','function _ftSelect(','function _ftDeselect(','function _ftStartEdit(','function _ftStopEdit(','function _ftDelete(','function _ftHandles('):
        if _f130 not in txt: errors.append('lint #130: ไม่พบ '+_f130)
    if "{key:'ftext',      sel:'.ftext .ftxt'" not in txt:
        errors.append('lint #130: แถบตัวอักษรต้องรู้จักกล่องข้อความ (TYPO_TYPES ftext)')
    if "document.addEventListener('dblclick',function(e){\n  if(!document.body.classList.contains('editmode')) return;" not in txt or "_ftStartEdit(box,e.clientX,e.clientY);" not in txt:
        errors.append('lint #130: ดับเบิลคลิก = พิมพ์ (แบบ 1)')
    if "if(_ftEdit===box && !hd) return;" not in txt:
        errors.append('lint #130: คลิกครั้งเดียวต้องเลือก/ลาก ไม่เข้าโหมดพิมพ์ (กำลังพิมพ์ = วางเคอร์เซอร์)')
    if '@media screen{body.editmode .ftext{pointer-events:auto;' not in _css or not re.search(r'(?m)^\.ftext\{[^}]*pointer-events:none', _css):
        errors.append('lint #130: กล่องข้อความต้องคลิกได้เฉพาะโหมดแก้ข้อความ (ไม่บังรูป/พื้นหลังในโหมดอื่น)')
    if not re.search(r'(?m)^\.ftext\{[^}]*color:var\(--txt-name\)', _css):
        errors.append('lint #130: สีเริ่มต้นกล่องข้อความต้องตามธีม (--txt-name)')
    if txt.count('.rz,.delbtn,.sizetag,.fth,.ftdel')!=3 or txt.count("querySelectorAll('.ftext').forEach(function(el){el.classList.remove('sel','fedit');")!=3:
        errors.append('lint #130: ปุ่มจับ/สถานะเลือกของกล่องข้อความต้องถูกตัดออกทั้ง บันทึก editor · ดาวน์โหลดเมนู · snapshot')
    if '@media print{.ftext{outline:none !important;}.ftext .fth,.ftext .ftdel{display:none !important;}}' not in _css:
        errors.append('lint #130: พิมพ์ต้องไม่มีกรอบ/ปุ่มจับกล่องข้อความ')
    if "if(!on && typeof _ftDeselect==='function') _ftDeselect();" not in txt or "_ftSel=null; _ftEdit=null; _ftDrag=null;" not in txt:
        errors.append('lint #130: ออกจากโหมดแก้ข้อความ/undo ต้องล้างสถานะกล่องข้อความ')
    if "np.querySelectorAll('.fimg,.ftext')" not in txt:
        errors.append('lint #130: หน้าใหม่ต้องไม่คัดกล่องข้อความจากหน้าต้นแบบ')
    if "x.appendChild(document.createTextNode(t('ft.default')))" not in txt:
        errors.append('lint #130: คำเริ่มต้นในกล่อง = เนื้อหาผู้ใช้ ห้ามผูก data-i18n (สลับภาษาจะทับข้อความที่พิมพ์)')
    # 130b) × ข้างขวาระดับขอบบน (ไม่ยื่นเหนือกล่อง) · เส้นช่วยจัดแนว + ดูดเข้าแนว · ไม่ซ้อนกรอบฟ้า (ผู้ใช้ 27 ต.ค. 2026)
    if '.ftext .ftdel{position:absolute;right:-30px;top:0;' not in _css:
        errors.append('lint #130: × ของกล่องข้อความต้องอยู่ข้างขวา ระดับขอบบน (ไม่ยื่นเหนือกล่อง — วางเรียงแล้ว × ต้องติดกล่องตัวเอง)')
    for _f130b in ('function _ftSnap(','function _ftTargets(','function _ftGuides(','function _ftGuideClear('):
        if _f130b not in txt: errors.append('lint #130: ไม่พบ '+_f130b+' (ดูดเข้าแนว)')
    if "var sn=e.altKey?{l:l,t:tp,w:w,h:h,gx:null,gy:null}:_ftSnap(D,l,tp,w,h);" not in txt or "_ftDrag=null; _ftGuideClear();" not in txt:
        errors.append('lint #130: ลาก/ยืดต้องดูดเข้าแนว (Alt ค้าง = ปิด) และลบเส้นแนวตอนปล่อยเมาส์')
    if '@media print{.ftguide{display:none !important;}}' not in _css or txt.count('.fth,.ftdel,.ftguide')!=3:
        errors.append('lint #130: เส้นแนวต้องไม่พิมพ์ และถูกตัดออกตอนบันทึก/snapshot')
    if '.ftext .ftxt.typosel{outline:none !important;}' not in _css:
        errors.append('lint #130: กล่องข้อความห้ามซ้อนกรอบฟ้า typosel')
    for _k130 in ('typ.ftext','btn.ftextAdd','ttl.ftextAdd','grp.insert','ttl.ftextDel','ft.default','fl.ftextAdd','fl.ftextDel','fl.ftextEmpty','st.ftextSel','st.ftextEdit'):
        if txt.count("'"+_k130+"':'")<2: errors.append('lint #130: i18n '+_k130+' ไม่ครบ TH+EN')

    # ---- 131) ลำดับแท็บ: หน้า · ข้อความ · รูป · เท็มเพลต · หน้าจอ · ไฟล์ (ผู้ใช้ 27 ต.ค. 2026 ย้าย หน้า ไปซ้ายสุด) ----
    _ord131=re.findall(r'<button class="edtab[^"]*" data-tab="([a-z]+)"', txt)
    if _ord131!=['page','home','image','template','screen','view','fmt','fln']:  # fmt = แท็บตามบริบท ท้ายสุดเสมอ (lint #137)
        errors.append('lint #131: ลำดับแท็บต้องเป็น หน้า · ข้อความ · รูป · เท็มเพลต · หน้าจอ · ไฟล์ (ตอนนี้ '+','.join(_ord131)+')')
    if not re.search(r'<button class="edtab active" data-tab="page"', txt) or not re.search(r'<div class="rpane active" data-pane="page">', txt) or 'function _tabStartup(' not in txt:
        errors.append('lint #131: แท็บเริ่มต้นต้องเป็น หน้า (markup + _tabStartup ตอนเปิดไฟล์)')
    if len(re.findall(r'class="edtab active"', txt))!=1 or len(re.findall(r'class="rpane active"', txt))!=1:
        errors.append('lint #131: ต้องมีแท็บ/ริบบอน active อย่างละ 1 เท่านั้น')
    # ---- 132) กล่องข้อความใหม่ไม่ทับกัน: วางต่อใต้กล่องที่เลือก/ล่าสุด + Tab วนเลือก + บอก i/n (ผู้ใช้ 27 ต.ค. 2026) ----
    if "var ref=(_ftSel && _ftSel.isConnected)?_ftSel:null;" not in txt or "if(!ref){ var _all=pg.querySelectorAll('.ftext'); if(_all.length) ref=_all[_all.length-1]; }" not in txt:
        errors.append('lint #132: กล่องใหม่ต้องวางต่อใต้กล่องที่เลือก หรือกล่องล่าสุดในหน้า (ไม่ทับที่เดิม)')
    if 'left=Math.min(210-w,left+5)' in txt:
        errors.append('lint #132: ห้ามเยื้องกล่องใหม่ 5mm (ทำให้ซ้อนเป็นขั้นบันได) — ต่อลงไป + เตือนแทน (ผู้ใช้ 28 ต.ค. 2026)')
    if "if(e.key==='Tab'){ e.preventDefault(); _ftCycle(_ftSel,e.shiftKey?-1:1); return; }" not in txt or 'function _ftCycle(' not in txt:
        errors.append('lint #132: Tab / Shift+Tab ต้องวนเลือกกล่องในหน้า')
    if txt.count("'st.ftextSel':'")<2 or '{i} / {n}' not in txt:
        errors.append('lint #132: แถบล่างต้องบอก กล่อง i / n ในหน้านี้')
    if '@media screen{body.editmode .ftext.sel{outline:1.5px solid #217346;z-index:24;}}' not in _css:
        errors.append('lint #132: กล่องที่เลือกต้องลอยหน้าสุด (เห็นจุดจับแม้ซ้อน)')

    # ---- 133) หน้าใหม่ไม่ซ่อนขอบบนใต้ริบบอน + ปุ่มลบหน้านี้ของหน้าเปล่าอยู่ล่างหน้า (ผู้ใช้ 27 ต.ค. 2026) ----
    if 'function _scrollToPageTop(' not in txt or 'if(firstNew) _scrollToPageTop(firstNew);' not in txt or "firstNew.scrollIntoView(" in txt:
        errors.append('lint #133: เพิ่มหน้าแล้วต้องเลื่อนให้ขอบบนกระดาษอยู่ใต้ริบบอน (ห้าม scrollIntoView start — แถบ sticky บังขอบบน)')
    if '.page.pgblank > .ed-delpage{position:absolute;left:50%;top:var(--blankdel,277mm);' not in _css:
        errors.append('lint #133: ปุ่ม ลบหน้านี้ ของหน้าเปล่าต้องอยู่ล่างหน้า (เหมือนหน้าเมนู)')

    # ---- 134) เลือกหลายกล่องข้อความ: Shift+คลิก + ลากกรอบเลือก · ลาก/ลูกศร/Delete ทั้งชุด · ดูดแนวด้วยกรอบรอบนอก (ผู้ใช้ 27 ต.ค. 2026) ----
    for _f134 in ('function _ftToggle(','function _ftSyncHandles(','function _ftBBox(','function _ftDeleteSel(','function _ftMarqEnd(','var _ftSet=[], _ftMarq=null;'):
        if _f134 not in txt: errors.append('lint #134: ไม่พบ '+_f134)
    if "if((e.ctrlKey||e.metaKey) && !hd){ _ftToggle(box); _ftAnchor=box;" not in txt:
        errors.append('lint #134: Ctrl+คลิก ต้องเพิ่ม/เอาออกจากชุดที่เลือก (ผู้ใช้ 28 ต.ค. 2026 เปลี่ยนจาก Shift)')
    if "else if(!(_ftSet.length>1 && _ftSet.indexOf(box)>=0 && !hd)){ if(hd) _ftSelect(box); else _ftSelectG(box); }" not in txt:
        errors.append('lint #134: คลิกกล่องในชุดที่เลือกอยู่ต้องลากทั้งชุด (ไม่แตกชุด)')
    if "if(!d && D.grp.length>1){" not in txt or "_ftSnap(D,G.l+dx,G.t+dy,G.w,G.h)" not in txt:
        errors.append('lint #134: ลากทั้งชุดต้องขยับทุกกล่องเท่ากัน + ดูดแนวด้วยกรอบรอบนอก')
    if "(_ftSet.length?_ftSet:[b]).forEach(function(x){ x.style.left=" not in txt or "e.preventDefault(); _ftDeleteSel(); }" not in txt:
        errors.append('lint #134: ลูกศร/Delete ต้องทำกับทั้งชุด')
    if "if(_ftMarq){ _ftMarqEnd(); return; }" not in txt or "_ftMarq={pg:pgE," not in txt:
        errors.append('lint #134: ต้องลากกรอบเลือกบนพื้นที่ว่างของหน้าได้')
    if "function _ftTargets(ex,pxmm){" not in txt or "if(ex.indexOf(o)>=0) return;" not in txt:
        errors.append('lint #134: แนวดูดต้องไม่รวมกล่องในชุดที่กำลังลาก')
    if '@media print{.ftmarq{display:none !important;}}' not in _css or txt.count('.fth,.ftdel,.ftguide,.ftmarq')!=3 or "_ftSet=[]; _ftMarq=null; }" not in txt:
        errors.append('lint #134: กรอบลากเลือกต้องไม่พิมพ์ · ตัดออกตอนบันทึก/snapshot · undo ล้างชุดที่เลือก')
    for _k134 in ('st.ftextMulti','fl.ftextDelN'):
        if txt.count("'"+_k134+"':'")<2: errors.append('lint #134: i18n '+_k134+' ไม่ครบ TH+EN')

    # ---- 135) ซ่อน/แสดงริบบอน: กระดาษเลื่อนตามขอบล่างแถบ ไม่เกิดช่องว่าง (ผู้ใช้ 27 ต.ค. 2026) ----
    if 'function _barKeep(fn){' not in txt or "window.scrollBy({top:now-(t0+d), behavior:'instant'}); }catch(_e){}" not in txt:
        errors.append('lint #135: _barKeep ต้องชดเชยการเลื่อนใน try (ห้ามทำให้ปุ่มซ่อนริบบอนตาย)')
    if "pg=pages[pi>=0?pi:0];" not in txt or "pg=(typeof _priceVisiblePage==='function' && _priceVisiblePage())" in txt:
        errors.append('lint #135: _priceVisiblePage คืน index — ต้องแปลงเป็น element ก่อนใช้')
    if 'function _barKeep(fn){' not in txt:
        errors.append('lint #135: ต้องมี _barKeep ชดเชยการเลื่อนตามความสูงแถบที่เปลี่ยน')
    if "function toggleFocus(){ _barKeep(function(){" not in txt or "if(tb){ _barKeep(function(){ document.body.classList.remove('focusmode');" not in txt:
        errors.append('lint #135: ปุ่มซ่อนริบบอน + คลิกแท็บตอนซ่อน ต้องผ่าน _barKeep')

    # ---- 136) ยืด/หดความกว้างหลายกล่องพร้อมกัน · ตัวอักษรคงขนาด · ยึดมุมซ้ายบน กล่องที่ต่อกันยังชิดกัน (ผู้ใช้ 27 ต.ค. 2026) ----
    for _f136 in ('function _ftGrpFrame(','if(D.grs){',"tg.classList.contains('ftgh') && _ftSet.length>1"):
        if _f136 not in txt: errors.append('lint #136: ไม่พบ '+_f136)
    if "if(Math.abs(s.t-(q.t+q.h))<=0.5 && s.l<q.l+q.w && q.l<s.l+s.w) s.p=q;" not in txt or "if(s.p) s.b.style.top=(_ftNum(s.p.b.style.top)+s.p.b.getBoundingClientRect().height/D.pxmm)" not in txt:
        errors.append('lint #136: ยืดหลายกล่องต้องจัดกล่องที่ต่อกันให้ชิดกันใหม่ (ยึดมุมซ้ายบน)')
    if "if(dd==='w') gx=Math.min(gx,D.minW-10); else gx=Math.max(gx,10-D.minW);" not in txt or "gy=Math.max(gy,G.h*D.minSc-G.h);" not in txt:
        errors.append('lint #136: กล่องแคบสุดต้องไม่ต่ำกว่า 10mm')
    if "['n','w','e','s','se'].forEach(function(d){ var h=document.createElement('div'); h.className='ftgh';" not in txt:
        errors.append('lint #136: กรอบชุดต้องมีจุดจับ บน/ซ้าย/ขวา/ล่าง/มุมขวาล่าง')
    if "hasH=(dd==='s'||dd==='se'||dd==='n');" not in txt or "off=(G.t+G.h)-(B.t+B.h);" not in txt or '.ftgh[data-d="n"]{top:-6px;' not in _css:
        errors.append('lint #136: จุดบนต้องปรับความสูงโดยขอบล่างชุดอยู่กับที่')
    if "s.b.style.minHeight=(sc===1)?s.mh:(s.h*sc).toFixed(1)+'mm';" not in txt or 'mh:b.style.minHeight' not in txt:
        errors.append('lint #136: ยืดความสูงหลายกล่องต้องขยายตามสัดส่วน + คืน min-height เดิมเมื่อกลับขนาดเดิม')
    if '.ftgh[data-d="se"]{top:auto;bottom:-6px;right:-6px;cursor:nwse-resize;}' not in _css or '.ftgh[data-d="s"]{top:auto;bottom:-6px;' not in _css:
        errors.append('lint #136: จุดจับล่าง/มุมขวาล่างต้องอยู่ขอบล่างกรอบ + cursor ถูกทิศ')
    if 'font-size' in txt[txt.find('if(D.grs){'):txt.find('if(D.grs){')+1500]:
        errors.append('lint #136: ยืดหลายกล่องต้องไม่เปลี่ยนขนาดตัวอักษร')
    if '@media print{.ftgrp{display:none !important;}}' not in _css or txt.count('.fth,.ftdel,.ftguide,.ftmarq,.ftgrp')!=3:
        errors.append('lint #136: กรอบชุดต้องไม่พิมพ์ + ตัดออกตอนบันทึก/snapshot')
    for _k136 in ('st.ftextMultiW','ttl.ftgrpW'):
        if txt.count("'"+_k136+"':'")<2: errors.append('lint #136: i18n '+_k136+' ไม่ครบ TH+EN')

    # ---- 137) แท็บตามบริบท รูปแบบข้อความ: ฟอนต์+จัดรูปแบบ อยู่ในแท็บนี้ · โผล่เฉพาะตอนแก้ข้อความ · เข้าโหมด=เลือกให้เอง (ผู้ใช้ 27 ต.ค. 2026 · Office contextual tab) ----
    _pf137=txt.find('<div class="rpane" data-pane="fmt">'); _pi137=txt.find('<div class="rpane" data-pane="image">'); _ph137=txt.find('<div class="rpane" data-pane="home">'); _tb137=txt.find('<div id="typobar">')
    if not (0<=_ph137<_pf137<_tb137<_pi137):
        errors.append('lint #137: #typobar (ฟอนต์+จัดรูปแบบ) ต้องอยู่ใน rpane fmt ไม่ใช่แท็บข้อความ')
    if '<button class="edtab ctx" data-tab="fmt" onclick="switchTab(\'fmt\')"' not in txt or 'data-i18n="tab.fmt"' not in txt or 'data-i18n="tab.fmtCtx"' not in txt:
        errors.append('lint #137: ไม่พบปุ่มแท็บ รูปแบบข้อความ (edtab ctx)')
    if 'body:not(.editmode) #edtabs .edtab[data-tab="fmt"]{display:none;}' not in _css or '#edribbon .rpane[data-pane="fmt"] #typobar{display:contents;}' not in _css or '#edtabs .edtab.ctx.active{background:#fff;}' not in _css:
        errors.append('lint #137: แท็บตามบริบทต้องซ่อนตอนไม่ได้แก้ข้อความ + typobar display:contents ใน pane fmt + สถานะ active')
    if "if(document.body.classList.contains('editmode') && name!=='fmt' && name!=='home' && name!=='fln') toggleEdit();" not in txt:
        errors.append('lint #137: สลับ ข้อความ ↔ รูปแบบข้อความ ต้องไม่ออกจากโหมดแก้ข้อความ')
    if "if(on){ if(!keepTab) switchTab('fmt'); } else { var _atab=document.querySelector('#edtabs .edtab.active'); if(_atab && _atab.getAttribute('data-tab')==='fmt') switchTab('home'); }" not in txt:
        errors.append('lint #137: เข้าโหมด=เลือกแท็บรูปแบบข้อความ · ออกโหมดตอนอยู่แท็บนั้น=กลับแท็บข้อความ')
    for _k137 in ('tab.fmt','tab.fmtCtx','ttl.tabFmt'):
        if txt.count("'"+_k137+"':'")<2: errors.append('lint #137: i18n '+_k137+' ไม่ครบ TH+EN')

    # ---- 138) แท็บรูปแบบข้อความ มีปุ่ม กล่องข้อความ (แทรก) + ปิดแก้ข้อความ (ขวาสุด) ไม่ต้องกลับแท็บข้อความ (ผู้ใช้ 28 ต.ค. 2026) ----
    _pf138=txt.find('<div class="rpane" data-pane="fmt">'); _pi138=txt.find('<div class="rpane" data-pane="image">')
    _seg138=txt[_pf138:_pi138] if 0<=_pf138<_pi138 else ''
    _a138=_seg138.find('id="btnFtextAddFmt" onclick="ftextAdd()"'); _c138=_seg138.find('id="btnEditClose" onclick="toggleEdit()"'); _f138=_seg138.find('data-i18n="grp.format"')
    if not (0<=_f138<_a138<_c138):
        errors.append('lint #138: แท็บรูปแบบข้อความต้องมี [กล่องข้อความ] แล้ว [ปิดแก้ข้อความ] ขวาสุด ต่อจากกลุ่มจัดรูปแบบ')
    if _seg138.find('<div id="typobar">')<0 or _seg138.find('id="btnFtextAddFmt"')<_seg138.find('data-i18n="grp.format"'):
        errors.append('lint #138: ปุ่มใหม่ต้องอยู่นอก #typobar (ไม่ถูกปิดตอนยังไม่เลือกข้อความ)')
    if "if(on){ if(!keepTab) switchTab('fmt'); } else { var _atab=document.querySelector('#edtabs .edtab.active'); if(_atab && _atab.getAttribute('data-tab')==='fmt') switchTab('home'); }" not in txt:
        errors.append('lint #138: ปิดแก้ข้อความจากแท็บนี้ต้องกลับแท็บข้อความ')
    for _k138 in ('btn.editClose','ttl.editClose','grp.close'):
        if txt.count("'"+_k138+"':'")<2: errors.append('lint #138: i18n '+_k138+' ไม่ครบ TH+EN')

    # ---- 139) ออกโหมดแก้ข้อความไม่เด้ง + ไฮไลท์ในกล่องข้อความไม่ค้าง + แถบรูปแบบชี้กล่องที่เลือก (ผู้ใช้ 28 ต.ค. 2026) ----
    if "if(on && _veIdx99>=0" in txt or "  if(_veIdx99>=0 && _veTop99!=null){" not in txt:
        errors.append('lint #139: toggleEdit ต้องชดเชยตำแหน่งหน้าทั้งตอนเข้าและออกโหมด (ห้าม on && เฉพาะเข้า)')
    if "if(_ws && _ws.rangeCount && b.contains(_ws.anchorNode)) _ws.removeAllRanges();" not in txt:
        errors.append('lint #139: เลิกพิมพ์กล่องข้อความต้องล้างไฮไลท์ในกล่องนั้น')
    if 'function _ftTypo(' not in txt or "_ftHandles(box,true); _ftTypo(box); _ftStatus(box); }" not in txt or "_ftSyncHandles(); _ftTypo(_ftSel); _ftStatus(_ftSel);" not in txt:
        errors.append('lint #139: เลือกกล่อง (คลิก/Shift/ลากกรอบ) ต้องให้แถบรูปแบบชี้กล่องที่เลือก')
    if "function _ftDeselect(){ _ftStopEdit(); if(_typoEl && _typoEl.closest && _typoEl.closest('.ftext')" not in txt:
        errors.append('lint #139: เลิกเลือกกล่องต้องปล่อยแถบรูปแบบ')

    # ---- 140) เพิ่มกล่องข้อความ = อยู่แท็บเดิม เลือกกล่อง (ไม่พิมพ์) · ดับเบิลคลิก/Enter = พิมพ์ + ไปแท็บรูปแบบข้อความ (ผู้ใช้ 28 ต.ค. 2026) ----
    _fa140=re.search(r'function ftextAdd\(\)\{[\s\S]*?\n\}', txt); _fa140=_fa140.group(0) if _fa140 else ''
    if 'toggleEdit(true);' not in _fa140 or '_ftSelect(box);' not in _fa140 or '_ftStartEdit(' in _fa140:
        errors.append('lint #140: ftextAdd ต้องเข้าโหมดโดยไม่สลับแท็บ + แค่เลือกกล่อง (ห้ามเริ่มพิมพ์เอง)')
    if 'function toggleEdit(keepTab){' not in txt:
        errors.append('lint #140: toggleEdit ต้องรับ keepTab')
    _se140=re.search(r'function _ftStartEdit\([^)]*\)\{[\s\S]*?\n\}', txt); _se140=_se140.group(0) if _se140 else ''
    if "switchTab('fmt');" not in _se140 or _se140.find("switchTab('fmt');")>_se140.find('x.focus();'):
        errors.append('lint #140: เริ่มพิมพ์กล่องข้อความต้องสลับไปแท็บรูปแบบข้อความก่อน focus')
    if "'fl.ftextAdd':'➕ เพิ่มกล่องข้อความแล้ว · ดับเบิลคลิกเพื่อพิมพ์'" not in txt:
        errors.append('lint #140: ข้อความแจ้งตอนเพิ่มกล่องต้องบอกว่าดับเบิลคลิกเพื่อพิมพ์ (ไม่ใช่ พิมพ์ได้เลย)')

    # ---- 141) เลือกกล่องกลางแถวแล้วเพิ่ม = แทรกตรงนั้น ดันกล่องที่ต่อกันข้างล่างลง (ไม่ทับ) · เลยขอบพิมพ์ = เตือน (ผู้ใช้ 28 ต.ค. 2026) ----
    if 'function _ftChainBelow(ref,px){' not in txt or 'Math.abs(s.t-(c.t+c.h))<=0.5 && s.l<c.l+c.w && c.l<s.l+s.w' not in txt:
        errors.append('lint #141: ต้องมี _ftChainBelow หากล่องที่ต่อกันลงไป (คลาด ≤0.5mm + ซ้อนแนวนอน)')
    _fa141=re.search(r'function ftextAdd\(\)\{[\s\S]*?\n\}', txt); _fa141=_fa141.group(0) if _fa141 else ''
    if '_ch=_ftChainBelow(ref,pxmm);' not in _fa141 or "b.style.top=(_ftNum(b.style.top)+_nh).toFixed(1)+'mm';" not in _fa141:
        errors.append('lint #141: ftextAdd ต้องแทรกใต้กล่องที่เลือก แล้วดันกล่องที่ต่อกันข้างล่างลงเท่าความสูงกล่องใหม่')
    if _fa141.find('pg.appendChild(box);')>_fa141.find('var _nh=box.getBoundingClientRect()'):
        errors.append('lint #141: ต้องวัดความสูงกล่องใหม่หลัง appendChild')
    if "if(_over) flashStatus('warning',tk('fl.ftextPushOver'));" not in _fa141 or txt.count("'fl.ftextPushOver':'")<2:
        errors.append('lint #141: ดันเลยขอบพิมพ์ล่างต้องเตือน (TH+EN)')

    # ---- 142) หน้าเปล่าแบบหน้าเมนู: ยืดตามกล่องข้อความในโหมดแก้ไข · ปุ่มลบหน้าใต้กล่องล่างสุด · ไม่ติดไฟล์/undo (ผู้ใช้ 28 ต.ค. 2026) ----
    if 'function _blankFit(pg){' not in txt or 'function _blankFitAll(){' not in txt or "var dt=Math.max(297-10-dh, bot+6), H=Math.max(297, dt+dh+10);" not in txt:
        errors.append('lint #142: ต้องมี _blankFit (ปุ่มลบหน้าใต้กล่องล่างสุด + หน้ายืด)')
    if 'body.editmode:not(.measuring) .page.pgblank{min-height:var(--blankh,297mm) !important;}' not in _css:
        errors.append('lint #142: หน้าเปล่าต้องยืดตาม --blankh เฉพาะโหมดแก้ไข (ไม่กระทบการวัดล้น/พิมพ์)')
    for _c142,_m142 in (("_restorePages(_lastSnap); _blankFitAll(); _dirty=true;",'undo/redo'),("if(D.moved) _blankFitAll();",'ลาก/ยืดกล่อง'),("_blankFitAll(); markDirty(); if(_over)",'เพิ่มกล่อง'),("if(typeof _blankFitAll==='function') _blankFitAll();  /* เข้าโหมด",'เข้า/ออกโหมด')):
        if _c142 not in txt: errors.append('lint #142: ต้องจัดหน้าเปล่าใหม่หลัง '+_m142)
    if txt.count("p.style.removeProperty('--blankh'); p.style.removeProperty('--blankdel'); });")!=3:
        errors.append('lint #142: ต้องล้าง --blankh/--blankdel ตอนบันทึกไฟล์ (2 จุด) + snapshot undo')
    _fa142=re.search(r'function ftextAdd\(\)\{[\s\S]*?\n\}', txt); _fa142=_fa142.group(0) if _fa142 else ''
    if "if(_ftNum(box.style.top)+box.getBoundingClientRect().height/pxmm>289+0.05) _over=true;" not in _fa142:
        errors.append('lint #142: กล่องใหม่เลยขอบพิมพ์ล่างต้องเตือน (แทนการเยื้อง 5mm)')

    # ---- 143) พิมพ์ไม่มีหน้าขาวต่อท้าย: ขึ้นหน้าใหม่ก่อนหน้าที่ 2+ (ไม่ใช่หลังทุกหน้า) + print body padding 0 (ผู้ใช้ 28 ต.ค. 2026) ----
    _pg143=re.search(r'\n\.page\{[^}]*\}', _css)
    if (_pg143 and 'page-break-after:always' in _pg143.group(0)) or '.page:last-child{page-break-after:auto;}' in _css:
        errors.append('lint #143: ห้าม page-break-after ทุกหน้า + :last-child (หน้าสุดท้ายไม่ใช่ลูกสุดท้ายของ body → หน้าขาวต่อท้ายตอนพิมพ์)')
    if '.page ~ .page{break-before:page;page-break-before:always;}' not in _css or '@media print{html>body{padding:0 !important;}}' not in _css:
        errors.append('lint #143: ต้องขึ้นหน้าใหม่ด้วย .page ~ .page break-before + print body padding:0')
    # ---- 144) เตือนทุกครั้งที่กล่องข้อความเลยขอบพิมพ์ 289mm (เพิ่ม/ลาก/ยืด/ลูกศร/พิมพ์) ไม่เตือนซ้ำ (ผู้ใช้ 28 ต.ค. 2026) ----
    if 'function _ftOverCheck(pg,silent,moved){' not in txt or 'if(ov && (!b._ftOv || (moved && moved.indexOf(b)>=0))) nw=true; b._ftOv=ov;' not in txt:
        errors.append('lint #144: ต้องมี _ftOverCheck เตือนตอนเพิ่งเลยขอบพิมพ์ (ธงกันเตือนซ้ำ)')
    for _c144,_m144 in (("_ftOverCheck(D.pg||(_ob&&_ob.closest('.page')),false,(D.items||D.grp||[]).map(function(s){ return s.b; }));",'ลาก/ยืด (เตือนทุกครั้งถ้ายังเลย)'),("markDirty(); _ftOverCheck(b.closest('.page'));",'ลูกศร'),("if(bx) _ftOverCheck(bx.closest('.page'));",'พิมพ์'),("_ftOverCheck(pg,true); _blankFitAll();",'เพิ่มกล่อง (เงียบ)')):
        if _c144 not in txt: errors.append('lint #144: ต้องตรวจขอบพิมพ์หลัง '+_m144)
    if txt.count("'fl.ftextOverPrint':'")<2: errors.append('lint #144: i18n fl.ftextOverPrint ไม่ครบ TH+EN')
    # ---- 145) ออกโหมดบนหน้าสุดท้ายไม่เด้ง: #scrollKeep เติมที่ว่างชั่วคราว หดตามการเลื่อน · ไม่ติดไฟล์/ไม่พิมพ์ (ผู้ใช้ 28 ต.ค. 2026) ----
    if 'function _scrollKeepTo(y){' not in txt or "_scrollKeepTo(_veSe99.scrollTop + (_veTp99.getBoundingClientRect().top - _veTop99));" not in txt:
        errors.append('lint #145: toggleEdit ต้องชดเชยผ่าน _scrollKeepTo (กัน clamp ที่หน้าสุดท้าย)')
    if "if(nh<=0.5) k.remove(); else if(nh<h-0.5)" not in txt or txt.count("var _sk=clone.querySelector('#scrollKeep'); if(_sk) _sk.remove();")!=2 or '@media print{#scrollKeep{display:none !important;}}' not in _css:
        errors.append('lint #145: #scrollKeep ต้องหดตามการเลื่อน + ตัดออกตอนบันทึก 2 จุด + ไม่พิมพ์')

    # ---- 146) พิมพ์: ตัดกล่องข้อความที่เลยขอบกระดาษชั่วคราว (กันหน้าขาวเกิน) · อยู่ใน printTitleScript ใช้ได้ในไฟล์ Save Menu ด้วย (ผู้ใช้ 28 ต.ค. 2026) ----
    _ps146=txt.find('<script id="printTitleScript">'); _pe146=txt.find('</script>',_ps146)
    _seg146=txt[_ps146:_pe146] if _ps146>=0 else ''
    if 'function _ftPrintClip(on){' not in _seg146 or "window.addEventListener('beforeprint',function(){ _ftPrintClip(true); });" not in _seg146 or "window.addEventListener('afterprint',function(){ _ftPrintClip(false); });" not in _seg146:
        errors.append('lint #146: _ftPrintClip ต้องอยู่ใน printTitleScript (ตัดตอน beforeprint · คืนค่าตอน afterprint)')
    if "b.style.minHeight='0'; b.style.maxHeight=lim.toFixed(2)+'mm'; b.style.overflow='hidden';" not in _seg146 or 'b._pc=null;' not in _seg146:
        errors.append('lint #146: ต้องตัดด้วย max-height (min-height 0 กันชนะ max) และคืนค่าเดิมทุกตัว')
    if "'#printTitleScript'" in txt:
        errors.append('lint #146: ห้ามตัด printTitleScript ออกจากไฟล์ Save Menu (การตัดกล่องตอนพิมพ์อยู่ในนั้น)')

    # ---- 147) บันทึกไฟล์: ปิดหน้าต่าง = ยกเลิก · เขียนไม่สำเร็จหลังกด Save = บอก error จริง + ดาวน์โหลดแทน (ห้ามแจ้ง "ยกเลิก" ทั้งที่ผู้ใช้กด Save · ผู้ใช้ 28 ต.ค. 2026) ----
    if 'function _saveErrTxt(e){' not in txt or txt.count("'fl.saveWriteErr':'")<2:
        errors.append('lint #147: ต้องมี _saveErrTxt + i18n fl.saveWriteErr TH/EN')
    for _f147 in ('async function downloadMenu(){','async function saveEditorFile(){'):
        _m147=re.search(re.escape(_f147)+r'[\s\S]*?\n\}', txt); _b147=_m147.group(0) if _m147 else ''
        if 'catch(err){ _wErr=err; }' not in _b147 or "tk('fl.saveWriteErr'," not in _b147 or _b147.count('AbortError')!=1:
            errors.append('lint #147: '+_f147+' ต้องแยก catch หน้าต่างเลือกที่เก็บ (AbortError=ยกเลิก) ออกจาก catch การเขียน (error จริง + ดาวน์โหลดแทน)')
    if "err:_wErr?_saveErrTxt(_wErr):''" not in txt:
        errors.append('lint #147: _saveAs ต้องแยกยกเลิกจริงออกจากเขียนไม่สำเร็จ')

    # ---- 148) คลิกกล่องข้อความลอย: ตัวเลือก element ทั่วไป (click) ต้องข้าม .ftext — ไม่ทับคำเตือน/สถานะของกล่อง · ไม่ชี้กล่องที่เพิ่งเอาออกจากชุด (ผู้ใช้ 28 ต.ค. 2026) ----
    _ck148=txt.find("/* คลิกบนเอกสารในโหมดแก้ไข → เลือก element */")
    _cs148=txt[_ck148:_ck148+900] if _ck148>=0 else ''
    if "if(ev.target.closest('.ftext')) return;" not in _cs148 or _cs148.find("if(ev.target.closest('.ftext')) return;")>_cs148.find('var found=_typoFind(ev.target);'):
        errors.append('lint #148: click handler เลือก element ต้อง return ก่อน _typoFind เมื่อคลิกใน .ftext (กันทับคำเตือนเลยขอบพิมพ์)')

    # ---- 149) เลือกหลายกล่อง: Ctrl+คลิก เพิ่ม/เอาออก · Shift+คลิก เลือกช่วง (ตามตำแหน่งที่เห็น) · สี/ฟอนต์/ขนาด ใช้กับทั้งชุด (ผู้ใช้ 28 ต.ค. 2026) ----
    for _f149 in ('function _ftMultiTargets(){','function _ftRange(box){','function _typoSizeSetEl(el,v){','var _ftAnchor=null;'):
        if _f149 not in txt: errors.append('lint #149: ไม่พบ '+_f149)
    if "else if(e.shiftKey && !hd){ _ftRange(box); e.preventDefault(); }" not in txt or "add:(e.shiftKey||e.ctrlKey||e.metaKey)" not in txt:
        errors.append('lint #149: Shift+คลิก = เลือกช่วง · ลากกรอบ + Ctrl/Shift = เพิ่ม')
    for _fn149,_lb149 in (('function applyColorRange(','สี'),('function typoFontApply(','ฟอนต์'),('function _typoSizeApply(','ขนาด (พิมพ์)'),('function typoSizeStep(','ขนาด (+/−)')):
        _i149=txt.find(_fn149); _seg149=txt[_i149:_i149+900] if _i149>=0 else ''
        if 'var _mt=_ftMultiTargets(); if(_mt){' not in _seg149:
            errors.append('lint #149: '+_lb149+' ต้องใช้กับทุกกล่องที่เลือก (_ftMultiTargets)')
    if 'var _mtp=_ftMultiTargets(); if(_mtp) _mtp.forEach(function(x){ x.style.color=hex; });' not in txt or "if(_tcpOrig.mt) _tcpOrig.mt.forEach(function(r){" not in txt:
        errors.append('lint #149: ชี้ดูสีต้องแสดงทุกกล่อง + ยกเลิกต้องคืนสีเดิมทุกกล่อง')
    for _k149 in ('fl.colorMulti','fl.fontMulti','fl.sizeMulti','fl.sizeMultiStep'):
        if txt.count("'"+_k149+"':'")<2: errors.append('lint #149: i18n '+_k149+' ไม่ครบ TH+EN')

    # ---- 150) ลากกรอบเลือกหลายกล่องแล้วแถบรูปแบบต้องใช้ได้ (click ปิดท้ายห้าม typoClear) · ยกเลิกถาดสีคืนสีทุกกล่องแม้แถบไม่ชี้กล่อง (ผู้ใช้ 28 ต.ค. 2026) ----
    if 'var _ftMarqClick=false;' not in txt or "_ftMarqClick=true; setTimeout(function(){ _ftMarqClick=false; },0);" not in txt:
        errors.append('lint #150: ลากกรอบเลือกต้องตั้งธง _ftMarqClick กัน click ปิดท้าย')
    _ck150=txt.find("/* คลิกบนเอกสารในโหมดแก้ไข → เลือก element */"); _cs150=txt[_ck150:_ck150+1200] if _ck150>=0 else ''
    if "if(_ftMarqClick){ _ftMarqClick=false; return; }" not in _cs150 or _cs150.find("if(_ftMarqClick)")>_cs150.find('var found=_typoFind(ev.target);'):
        errors.append('lint #150: click handler เลือก element ต้องข้าม click ปิดท้ายการลากกรอบ ก่อน typoClear')
    if "if(!el && !_mts.length){ _tcpOrig=null; return; }" not in txt or "function _tcpRestore(){ if(!_tcpOrig) return; if(_tcpOrig.mt)" not in txt:
        errors.append('lint #150: _tcpSnap/_tcpRestore ต้องเก็บ/คืนสีหลายกล่องแม้ _typoEl ว่าง')

    # ---- 151) หลายกล่อง: เปลี่ยนขนาด/ฟอนต์/B-I-U-S แล้วกล่องที่ต่อกันจัดชิดใหม่ (ไม่ทับกัน) · B/I/U/S + เส้นขอบตัวอักษร ใช้ทั้งชุดไม่ต้องไฮไลท์ (ผู้ใช้ 28 ต.ค. 2026) ----
    for _f151 in ('function _ftRestack(L,fn){','function _ftAfterMulti(L){','function _ftStyleMulti(cmd,k,L){'):
        if _f151 not in txt: errors.append('lint #151: ไม่พบ '+_f151)
    for _c151,_m151 in (("_ftRestack(_mt,function(){ _mt.forEach(function(x){ var c=_typoCurSize(x)",'ขนาด +/−'),("_ftRestack(_mt,function(){ _mt.forEach(function(x){ _typoSizeSetEl(x,v); }); });",'ขนาด (พิมพ์)'),("_ftRestack(_mt,function(){ _mt.forEach(function(x){ x.style.fontFamily=f; }); });",'ฟอนต์')):
        if _c151 not in txt: errors.append('lint #151: '+_m151+' หลายกล่องต้องจัดกล่องที่ต่อกันใหม่ (_ftRestack)')
    if 'var _mt=_ftMultiTargets(); if(_mt){ _ftStyleMulti(cmd,k,_mt); return; }' not in txt:
        errors.append('lint #151: B/I/U/S หลายกล่องต้องใช้ทั้งชุด (ไม่ต้องไฮไลท์)')
    if txt.count('var _mo=_ftMultiTargets(); if(_mo){')!=2 or "mt:(_ftMultiTargets()||[]).map(function(x){ return {el:x, shadow:x.style.textShadow||''" not in txt or 'if(_olPv.mt && _olPv.mt.length){' not in txt or 'if(pv.mt && pv.mt.length){' not in txt:
        errors.append('lint #151: เส้นขอบตัวอักษรหลายกล่อง (ปุ่ม A · สีขอบ · ชี้ดู · ตกลง · ยกเลิก) ต้องใช้ทั้งชุด')
    for _k151 in ('fl.styleMultiOn','fl.styleMultiOff','fl.olMulti','fl.olOffMulti','fl.olColorMulti','fl.olAutoMulti'):
        if txt.count("'"+_k151+"':'")<2: errors.append('lint #151: i18n '+_k151+' ไม่ครบ TH+EN')

    # ---- 152) ถาดเส้นขอบตัวอักษร: ชี้ดูสี/อัตโนมัติ/ความหนา แล้วช่อง HEX + ไฮไลท์ในถาดต้องตามค่าที่กำลังดู (ผู้ใช้ 28 ต.ค. 2026) ----
    if 'function _olPvUi(){' not in txt or "hx.value=String(cu||pv.color).toUpperCase();" not in txt:
        errors.append('lint #152: ต้องมี _olPvUi อัปเดตช่อง HEX ตามสีที่กำลังดู')
    for _f152 in ('function _olPvColor(','function _olPvAuto(','function _olPvWidth('):
        _i152=txt.find(_f152); _s152=txt[_i152:txt.find('\n',_i152)] if _i152>=0 else ''
        if '_olPvUi();' not in _s152: errors.append('lint #152: '+_f152+' ต้องเรียก _olPvUi()')

    # ---- 153) จอแคบ/ซูมเกินหน้าต่าง: ไม่หด ไม่ตกแถว ใช้แถบเลื่อนแนวนอน · แถบบนคลุมเต็มความกว้างที่เลื่อนได้ (ผู้ใช้ 28 ต.ค. 2026) ----
    if '#edtabs{display:flex;align-items:center;gap:2px;padding:0 8px;background:#f3f2f1;border-bottom:1px solid #e1dfdd;flex-wrap:nowrap;' not in _css:
        errors.append('lint #153: #edtabs ต้อง flex-wrap:nowrap (แถบแท็บไม่ตกเป็น 2 แถว)')
    if '@media screen{body:not(.gridview){width:max-content;min-width:max(960px,100%);}}' not in _css:
        errors.append('lint #153: body ต้องกว้างเท่าเนื้อหา (max-content) บนจอ ยกเว้น gridview — แถบบนคลุมเต็มตอนเลื่อนขวา')

    # ---- 154) จัดกลุ่มกล่องข้อความ Ctrl+G / Ctrl+Shift+G + ปุ่มในแท็บรูปแบบข้อความ · คลิก=ทั้งกลุ่ม · ดับเบิลคลิก=พิมพ์ในกล่อง · ไม่มีกลุ่มซ้อน (ผู้ใช้ 28 ต.ค. 2026) ----
    for _f154 in ('function _ftGroupOf(b){','function _ftSelectG(box){','function _ftGroupClean(pg){','function _ftGroupSync(){','function ftGroup(){','function ftUngroup(){','function _ftGroupExpand(L){','function _ftIsOneGroup(L){'):
        if _f154 not in txt: errors.append('lint #154: ไม่พบ '+_f154)
    _pf154=txt.find('<div class="rpane" data-pane="fmt">'); _pi154=txt.find('<div class="rpane" data-pane="image">'); _sg154=txt[_pf154:_pi154] if 0<=_pf154<_pi154 else ''
    _a154=_sg154.find('id="btnFtextAddFmt"'); _g154=_sg154.find('id="btnFtGroup" onclick="ftGroup()" disabled'); _u154=_sg154.find('id="btnFtUngroup" onclick="ftUngroup()" disabled'); _c154=_sg154.find('id="btnEditClose"')
    if not (0<=_a154<_g154<_u154<_c154):
        errors.append('lint #154: ปุ่ม จัดกลุ่ม/ยกเลิกกลุ่ม ต้องอยู่ระหว่างกลุ่มแทรกกับปิด ในแท็บรูปแบบข้อความ (เริ่มต้น disabled + tooltip เหตุผล)')
    for _c154,_m154 in (("if((e.ctrlKey||e.metaKey) && !e.altKey && (e.code==='KeyG' || e.key==='g' || e.key==='G')){",'ปุ่มลัด Ctrl+G'),
                        ("var _h0=hits; hits=_h0.filter(function(b){ return _ftGroupOf(b).every(",'ลากกรอบ = กลุ่มต้องอยู่ในกรอบครบ'),
                        ("_ftSet=_ftGroupExpand(L.slice(",'Shift+คลิกช่วง = ได้ทั้งกลุ่ม'),
                        ("var i=_ftSet.indexOf(box), _gm=_ftGroupOf(box);",'Ctrl+คลิก = ทั้งกลุ่ม'),
                        ("if(_rg.length>1) ref=_rg.reduce(",'กล่องใหม่ต่อใต้กลุ่ม'),
                        ("box.remove(); _ftGroupClean(_dpg);",'ลบกล่อง = ล้างกลุ่มที่เหลือกล่องเดียว'),
                        ("_ftGroupClean(_dpg2); _ftGroupSync();",'ลบหลายกล่อง = ล้างกลุ่ม'),
                        ("if(_ftGroupOf(b0).length>1) _ftSelectG(b0);",'Esc หลังพิมพ์ = เลือกทั้งกลุ่ม'),
                        ("_ftMarq=null; } if(typeof _ftGroupSync==='function') _ftGroupSync();",'undo = ปุ่มจัดกลุ่มตามสถานะใหม่')):
        if _c154 not in txt: errors.append('lint #154: ขาด '+_m154)
    for _k154 in ('btn.ftGroup','btn.ftUngroup','grp.arrange','ttl.ftGroup','ttl.ftGroupNeed','ttl.ftGroupSame','ttl.ftUngroup','ttl.ftUngroupNeed','fl.ftGrouped','fl.ftGroupNeed','fl.ftGroupSame','fl.ftUngrouped','fl.ftUngroupNeed','st.ftextGroup'):
        if txt.count("'"+_k154+"':'")<2: errors.append('lint #154: i18n '+_k154+' ไม่ครบ TH+EN')

    # ---- 155) พิมพ์ทับไฮไลท์ในกล่องข้อความ: แถบล่างกลับเป็นสถานะกำลังพิมพ์ ไม่ค้าง "เลือกอยู่" · ไม่ทับผลที่เพิ่งแจ้ง (ผู้ใช้ 28 ต.ค. 2026) ----
    if "else if(!_selHold && typeof _ftEdit!=='undefined' && _ftEdit && _ftEdit.isConnected && typeof _ftStatus==='function') _ftStatus(_ftEdit);" not in txt:
        errors.append('lint #155: syncButtons ต้องคืนสถานะกำลังพิมพ์ของกล่องข้อความเมื่อไฮไลท์หมด (เว้น _selHold)')

    # ---- 156) เส้นลอย (ขั้น C): แบบ 3 (ทุกมุม · ≤5° ดูดตรง · Shift 45° · Alt ไม่ดูด) · แท็บตามบริบท รูปแบบเส้น · ไม่ติดไฟล์/undo/พิมพ์ส่วนเครื่องมือ (ผู้ใช้ 28 ต.ค. 2026) ----
    for _f156 in ('function flineAdd(){','function _flRender(l){','function _flSelect(l){','function _flDeselect(){','function _flOverlay(){','function _flDelete(){','function _flAfterRestore(){','function _flTargets(l,px){','function _flSync(){'):
        if _f156 not in txt: errors.append('lint #156: ไม่พบ '+_f156)
    if 'if(_ay<=_FT_SNAP && _ax>_ay) P.y=F.y; else if(_ax<=_FT_SNAP && _ay>_ax) P.x=F.x;' not in txt or 'if(e.shiftKey) sa=Math.round(a/(Math.PI/4))*(Math.PI/4);' not in txt or '5*Math.PI/180' in txt:
        errors.append('lint #156: ลากปลายเส้นต้องดูดตรงตามระยะ 1.5 มม. (ไม่ใช่ ±5°) · Shift ล็อก 45° (ผู้ใช้ 29 ต.ค. 2026)')
    if '<button class="edtab ctx" data-tab="fln"' not in txt or '<div class="rpane" data-pane="fln" id="flPane">' not in txt or 'body:not(.flsel) #edtabs .edtab[data-tab="fln"]' not in _css:
        errors.append('lint #156: ต้องมีแท็บตามบริบท รูปแบบเส้น (ซ่อนเมื่อไม่ได้เลือกเส้น)')
    if "name!=='fmt' && name!=='home' && name!=='fln') toggleEdit();" not in txt:
        errors.append('lint #156: สลับไปแท็บรูปแบบเส้นต้องไม่ออกจากโหมดแก้ข้อความ')
    if txt.count('.ftmarq,.ftgrp,.flh,.fldel,.flhl')!=3 or '@media print{.flh,.fldel,.flhl{display:none !important;}}' not in _css or txt.count("var _bfl=clone.querySelector('body'); if(_bfl) _bfl.classList.remove('flsel');")!=2:
        errors.append('lint #156: จุดจับ/×/แสงของเส้นต้องตัดออกตอนบันทึก 2 จุด + undo · ไม่พิมพ์ · flsel ไม่ติดไฟล์')
    _ps156=txt.find('<script id="printTitleScript">'); _pe156=txt.find('</script>',_ps156)
    if "querySelectorAll('.fline')" not in (txt[_ps156:_pe156] if _ps156>=0 else ''):
        errors.append('lint #156: พิมพ์ต้องตัดเส้นที่เลยขอบกระดาษ (printTitleScript)')
    _ck156=txt.find("/* คลิกบนเอกสารในโหมดแก้ไข → เลือก element */"); _cs156=txt[_ck156:_ck156+1400] if _ck156>=0 else ''
    if "if(ev.target.closest('.fline,.flh,.fldel')) return;" not in _cs156 or _cs156.find("if(ev.target.closest('.fline,.flh,.fldel'))")>_cs156.find('var found=_typoFind(ev.target);'):
        errors.append('lint #156: click เลือก element ต้องข้ามเส้นลอย (ไม่ทับสถานะเส้น)')
    for _b156 in ('id="btnFlineAdd" onclick="flineAdd()"','id="btnFlineAddFmt" onclick="flineAdd()"','id="btnFlineAddLn" onclick="flineAdd()"','id="btnFlDel" onclick="_flDelete()"'):
        if _b156 not in txt: errors.append('lint #156: ไม่พบปุ่ม '+_b156)
    if '#edribbon .flopt.on{background:#217346;border-color:#217346;color:#fff;}' not in _css:
        errors.append('lint #156: ปุ่มที่ใช้อยู่ในแท็บรูปแบบเส้นต้องเขียว (ข้อ 11)')
    if "pg.querySelectorAll('.fline').forEach(function(q){ var v=Math.max(" not in txt:
        errors.append('lint #156: หน้าเปล่าต้องยืดตามเส้นที่เลยขอบล่าง')
    for _k156 in ('tab.fln','tab.flnCtx','ttl.tabFln','btn.flineAdd','ttl.flineAdd','btn.flDel','ttl.flDel','grp.flColor','grp.flWidth','grp.flStyle','grp.flOrient','grp.flDelete','fl.theme','ttl.flTheme','fls.solid','fls.dashed','fls.dotted','fls.double','ttl.flsDouble','btn.flH','btn.flV','st.flSel','fl.flineAdd','fl.flineDel','fl.flColor','fl.flWidth','fl.flStyle','fl.flOrient'):
        if txt.count("'"+_k156+"':'")<2: errors.append('lint #156: i18n '+_k156+' ไม่ครบ TH+EN')

    # ---- 157) ช่องมุม/ความยาวของเส้นลอย: พิมพ์ได้ · −/+ กดค้าง · ล้อเมาส์ · หมุนรอบกลางเส้น · ความยาวยึดจุดเริ่ม · ค่าเดิมไม่มีจุด Undo (ผู้ใช้ 29 ต.ค. 2026) ----
    for _f157 in ('function _flSetAng(v){','function _flSetLen(v){','function _flAngStep(s){','function _flLenStep(s){','function _flFieldsSync(force){','function _flNum(s){','function _flDeg(a){'):
        if _f157 not in txt: errors.append('lint #157: ไม่พบ '+_f157)
    _pf157=txt.find('<div class="rpane" data-pane="fln" id="flPane">'); _pe157=txt.find('<div class="rpane" data-pane="view">',_pf157); _sg157=txt[_pf157:_pe157] if 0<=_pf157<_pe157 else ''
    for _i157 in ('id="flAng"','id="flLen"','id="flAngUp" onclick="_flAngStep(1)"','id="flAngDown" onclick="_flAngStep(-1)"','id="flLenUp" onclick="_flLenStep(1)"','id="flLenDown" onclick="_flLenStep(-1)"','data-i18n="grp.flGeom"'):
        if _i157 not in _sg157: errors.append('lint #157: แท็บรูปแบบเส้นต้องมี '+_i157)
    _mh157=re.search(r'var _HOLD_BTNS=\{([\s\S]*?)\n\};', txt); _mw157=re.search(r'var _WHEEL_FIELDS=\{([\s\S]*?)\n\};', txt)
    for _h157 in ('flAngUp','flAngDown','flLenUp','flLenDown'):
        if not _mh157 or ('\n  '+_h157+':{') not in ('\n'+_mh157.group(1)): errors.append('lint #157: ปุ่ม '+_h157+' ต้องกดค้างได้')
    for _w157 in ('flAng','flLen'):
        if not _mw157 or ('\n  '+_w157+':function(d)') not in ('\n'+_mw157.group(1)): errors.append('lint #157: ช่อง '+_w157+' ต้องหมุนล้อปรับได้')
    if 'function _flClean(v,neg){' not in txt or "el.addEventListener('blur',function(){ _flFieldsSync(true); });" not in txt:
        errors.append('lint #157: ช่องมุม/ความยาวต้องกรองตัวอักษร + ไม่กด Enter = ไม่เปลี่ยน (เหมือนช่องขนาดตัวอักษร)')
    if 'if(Math.abs(v-_flDeg(g.a))<0.05) return false;' not in txt or '_flFieldsSync(false);' not in txt or "String(Math.round(d[k]*100)/100)" not in txt:
        errors.append('lint #157: มุมเดิม = ไม่มีจุด Undo · ช่องตามเส้น · พิกัดเก็บ 0.01 มม.')
    for _k157 in ('grp.flGeom','fl.angLbl','fl.lenLbl','fl.mmUnit','ttl.flAng','ttl.flAngDown','ttl.flAngUp','ttl.flLen','ttl.flLenDown','ttl.flLenUp','fl.flAngSet','fl.flLenSet','fl.flNumBad','fl.flLenRange','fl.flNumOnly','fl.flNumOnlyTh'):
        if txt.count("'"+_k157+"':'")<2: errors.append('lint #157: i18n '+_k157+' ไม่ครบ TH+EN')

    # ---- 158) แท็บเต็มจอ: ข้อ 1 = shortcut --app (ไม่ใช้เมนู Chrome ที่เปลี่ยนชื่อ/ถูกปิดได้) · ข้อ 2 = ขั้นตอนสร้าง shortcut + คำสั่ง kiosk อยู่ใต้ข้อ 2 · ข้อ 3 F11 ไม่มีกล่องคำสั่ง (ผู้ใช้ 29 ต.ค. 2026) ----
    _fp158=txt.find('<div class="about-pane" data-pane="full">'); _fs158=txt[_fp158:_fp158+5000] if _fp158>=0 else ''
    _o158=[_fs158.find(x) for x in ('data-i18n="about.fullBody"','--app=&quot;file:///' if '--app=&quot;file:///' in _fs158 else '--app="file:///','data-i18n="about.full2"','--kiosk','data-i18n="about.full3"','data-i18n="about.fullNote"')]
    if min(_o158)<0 or _o158!=sorted(_o158):
        errors.append('lint #158: ลำดับแท็บเต็มจอต้องเป็น ข้อ 1 → คำสั่ง --app → ข้อ 2 → คำสั่ง --kiosk → ข้อ 3 (F11 ไม่มีกล่องคำสั่ง) → หมายเหตุ')
    if 'Cast, save' in txt:
        errors.append('lint #158: ห้ามอ้างเมนู Chrome (Cast, save and share) — ชื่อเมนูเปลี่ยนตามรุ่น และ Create shortcut ถูกปิดได้')
    for _k158 in ('about.full2','about.full3'):
        if txt.count("'"+_k158+"':'")<2: errors.append('lint #158: i18n '+_k158+' ไม่ครบ TH+EN')
    if txt.count('New → Shortcut')<2: errors.append('lint #158: ต้องบอกขั้นตอนสร้าง shortcut (คลิกขวา Desktop → New → Shortcut) ทั้ง TH/EN')

    # ---- 159) สีแท้ครบ 15 สี: แดง ชมพู ส้ม เหลือง เขียว น้ำเงิน ฟ้า ม่วง เทา ขาว ดำ(bw) น้ำตาล ทอง เงิน ครีม · ทอง/เงิน หัวกลุ่มไล่สีแวววาว ทำตาม --secalpha ไม่ทับจอป้าย (ผู้ใช้ 29 ต.ค. 2026) ----
    _v159={'แดง':'vivid-red','ชมพู':'vivid-pink','ส้ม':'vivid-orange','เหลือง':'vivid-yellow','เขียว':'vivid-green','น้ำเงิน':'vivid-blue','ฟ้า':'vivid-sky','ม่วง':'vivid-purple','เทา':'vivid-gray','ขาว':'vivid-white','ดำ':'bw','น้ำตาล':'vivid-brown','ทอง':'vivid-gold','เงิน':'vivid-silver','ครีม':'vivid-cream'}
    _mt159=re.search(r"var _THEMES=\[([^\]]*)\]", txt); _my159=re.search(r"var _THEME_TYPE=\{([^}]*)\}", txt)
    _ty159=dict(re.findall(r"'([a-z-]+)':'([a-z]+)'", _my159.group(1))) if _my159 else {}
    for _c159,_id159 in _v159.items():
        if not _mt159 or ("'"+_id159+"'") not in _mt159.group(1) or (':root[data-theme="'+_id159+'"]{') not in txt or _ty159.get(_id159)!='vivid':
            errors.append('lint #159: สีแท้ '+_c159+' ('+_id159+') ต้องมีธีม + CSS + ประเภท vivid')
    for _id159 in ('vivid-gold','vivid-silver'):
        _mg159=re.search(r':root\[data-theme="'+_id159+r'"\] body:not\(\.boardmode\) \.sec-h\{background:linear-gradient\(([^\n]*)\) !important;\}', txt)
        if not _mg159 or _mg159.group(1).count('var(--secalpha,1)')<3:
            errors.append('lint #159: '+_id159+' หัวกลุ่มต้องไล่สี (linear-gradient ≥3 จุด ใช้ var(--secalpha,1)) และไม่ทับโหมดจอป้าย (body:not(.boardmode))')
    _pb159=txt.find('\n.sec-h{color:var(--accent)'); _pg159=txt.find('body:not(.boardmode) .sec-h{background:linear-gradient(')
    if _pb159<0 or _pg159<_pb159:
        errors.append('lint #159: กฎไล่สีหัวกลุ่ม ทอง/เงิน ต้องอยู่หลัง .sec-h หลัก (lint #93/#112 อ่าน .sec-h{ ตัวแรก)')
    # 159b) ชื่อธีมสีแท้ไม่มีคำ สด/แท้ (TH) · Vivid/True (EN) — ประเภทบอกอยู่แล้ว · ชื่อธีมห้ามซ้ำกัน (ผู้ใช้ 29 ต.ค. 2026)
    for _k159b in ('th.vividRed','th.vividPink','th.vividOrange','th.vividYellow','th.vividGreen','th.vividBlue','th.vividSky','th.vividPurple','th.vividGray','th.vividWhite','th.vividBrown','th.vividGold','th.vividSilver','th.vividCream'):
        for _v159b in re.findall("'"+re.escape(_k159b)+"':'([^']*)'", txt):
            if re.search(r'(สด|แท้)$|^(Vivid|True) ', _v159b):
                errors.append('lint #159: ชื่อธีมสีแท้ '+_k159b+' ต้องไม่มี สด/แท้/Vivid/True ('+_v159b+')')
    _mk159=re.search(r"var _THEME_KEYS=\{([^}]*)\}", txt)
    if _mk159:
        _tk159=set(re.findall(r":'(th\.[A-Za-z]+)'", _mk159.group(1)))
        for _ln159 in [l for l in txt.split('\n') if "'th.vividRed':'" in l]:
            _nm159=[v for k,v in re.findall(r"'(th\.[A-Za-z]+)':'([^']*)'", _ln159) if k in _tk159]
            _dup159=sorted(set(x for x in _nm159 if _nm159.count(x)>1))
            if _dup159: errors.append('lint #159: ชื่อธีมซ้ำกัน '+', '.join(_dup159))

    if ':root[data-theme="vivid-gray"] .sec-h .sechead *' not in txt:
        errors.append('lint #159: เทาแท้ หัวกลุ่มต้องตัวขาว')
    for _k159 in ('th.vividSky','th.vividGold','th.vividSilver','th.vividGray','th.vividWhite','th.vividCream'):
        if txt.count("'"+_k159+"':'")<2: errors.append('lint #159: i18n '+_k159+' ไม่ครบ TH+EN')

    # ---- 160) dropdown ธีม เรียงตามตัวอักษรของชื่อธีม (TH ลำดับพจนานุกรม localeCompare 'th' · EN 'en') · กำหนดเองอยู่บนสุด · ธีมแรกของประเภท = ตัวแรกในรายการ · สร้างรายการใหม่ตอนเปิด (สลับภาษาแล้วยังเรียงถูก) (ผู้ใช้ 29 ต.ค. 2026) ----
    _ms160=re.search(r"function _themeSortedIds\(\)\{[^\n]*", txt)
    if not _ms160 or ".localeCompare(" not in _ms160.group(0) or "'th'" not in _ms160.group(0) or "'en'" not in _ms160.group(0):
        errors.append('lint #160: ไม่พบ _themeSortedIds เรียงตามตัวอักษร (localeCompare th/en)')
    _ml160=re.search(r"function _themeDdListHtml\(\)\{(.*?)\n\}", txt, re.S)
    if not _ml160 or '_themeSortedIds().forEach' not in _ml160.group(1) or '_THEME_ORDER.forEach' in _ml160.group(1):
        errors.append('lint #160: รายการธีมต้องใช้ _themeSortedIds() ไม่ใช่ _THEME_ORDER')
    if not _ml160 or _ml160.group(1).find("html+=opt('custom')")<0 or _ml160.group(1).find("html+=opt('custom')")>_ml160.group(1).find('_themeSortedIds().forEach'):
        errors.append('lint #160: กำหนดเองต้องอยู่บนสุดของรายการธีม')
    if 'function _themeFltFirst(){ var ids=_themeSortedIds();' not in txt:
        errors.append('lint #160: ธีมแรกของประเภทต้องเป็นตัวแรกในรายการที่เรียงแล้ว')
    _mo160=re.search(r"function _themeDdOpen\(\)\{(.*?)\n\}", txt, re.S)
    if not _mo160 or 'pop.innerHTML=_themeDdListHtml();' not in _mo160.group(1):
        errors.append('lint #160: เปิด dropdown ธีมต้องสร้างรายการใหม่ (ลำดับตามภาษาปัจจุบัน)')

    # ---- 162) ปุ่ม ปิด (Exit) แท็บไฟล์ ต่อจากกลุ่มพิมพ์ · ยังไม่ Save Editor = ถามก่อน · ยืนยันแล้วไม่ถามซ้ำ · ปิดไม่ได้ = แจ้ง Alt+F4 ตรงๆ (ผู้ใช้ 29 ต.ค. 2026) ----
    if txt.count('id="btnExit"')!=1 or 'id="btnExit" onclick="exitApp()"' not in txt:
        errors.append('lint #162: ต้องมีปุ่ม #btnExit 1 ปุ่ม ผูก exitApp()')
    else:
        _pe162=txt.find('id="btnExit"'); _pp162=txt.find('data-i18n="grp.print"'); _pn162=txt.find('<div class="rpane', _pp162)
        if not (0<=_pp162<_pe162<_pn162): errors.append('lint #162: ปุ่ม ปิด ต้องอยู่แท็บไฟล์ ต่อจากกลุ่ม พิมพ์')
    _fx162=re.search(r"\nfunction exitApp\(\)\{[\s\S]*?\n\}", txt)
    for _n162 in ("activeBtn:'btnExit'","if(!_dirty){ _exitNow(); return; }","msgKey:'pnl.exitMsg'"):
        if not _fx162 or _n162 not in _fx162.group(0): errors.append('lint #162: exitApp ขาด '+_n162)
    _fn162=re.search(r"\nfunction _exitNow\(\)\{[\s\S]*?\n\}", txt)
    for _n162 in ('_exiting=true;','window.close()','window.closed','_exiting=false;',"tk('st.exitBlocked')","_takeSnapshot()"):
        if not _fn162 or _n162 not in _fn162.group(0): errors.append('lint #162: _exitNow ขาด '+_n162)
    if 'if(_dirty && !_exiting){ e.preventDefault();' not in txt:
        errors.append('lint #162: beforeunload ต้องข้ามเมื่อยืนยันปิดแล้ว (_exiting)')
    if '#edbar #btnExit.on{background:#217346;' not in txt:
        errors.append('lint #162: ปุ่ม ปิด ไม่เขียวตอน panel เปิด (กฎข้อ 11)')
    for _k162 in ('btn.exit','ttl.exit','grp.app','pnl.exitOk','pnl.exitMsg','st.exitBlocked'):
        if txt.count("'"+_k162+"':'")<2: errors.append('lint #162: i18n '+_k162+' ไม่ครบ TH+EN')
    if "'#edbar'," not in txt[txt.find('function buildMenuHtml('):txt.find('function buildMenuHtml(')+600]:
        errors.append('lint #162: Save Menu ต้องตัด #edbar (ปุ่ม ปิด ไม่ติดไปในไฟล์เมนู)')

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
