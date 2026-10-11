#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_oe.py - ตรวจ OEIsanHotpotMenuEditor.html หลังแก้ทุกครั้ง (fail-closed)

รัน:
  python verify_oe.py               ตรวจครบ: lint + static + เทียบกับ HEAD + เปิดเบราว์เซอร์ headless ทดสอบจริง
  python verify_oe.py --no-browser  ตรวจแค่ static -> ผลเป็น INCOMPLETE (ไม่ใช่ PASS)

ตั้งใจลบ element id:  set OE_ALLOW_REMOVE_IDS=id1,id2   (ไม่งั้นการลบ id = FAIL)

exit code: 0 = PASS ครบทุกข้อ | 1 = FAIL | 2 = INCOMPLETE (ตรวจไม่ครบ ห้ามถือว่าผ่าน)
ใช้เป็น pre-commit hook ได้: .git/hooks/pre-commit -> python verify_oe.py || exit 1
"""
import os, re, sys, json, html, difflib

ROOT = os.path.dirname(os.path.abspath(__file__))
TARGET = "OEIsanHotpotMenuEditor.html"  # เปลี่ยนชื่อจาก OEIsanHotpotMenuWithImageEditor.html (8 ต.ค. 2026)
PATH = os.path.join(ROOT, TARGET)

# ฟังก์ชันหลักที่ต้องมี "ครั้งเดียวพอดี"
REQUIRED_FUNCS = [
    "switchTab", "toggleEdit", "toggleImgMode", "editHeader", "setLang", "t",
    "undo", "redo", "markDirty", "_snapNow", "decorate", "checkOverflow", "renumber",
    "newRow", "newSection", "saveEditorFile", "downloadMenu", "addPage",
    "typoSelect", "typoClear", "typoSetDefault", "typoApplyAllSame", "typoResetSel",
    "typoClearSel", "typoFontApply", "applyColorRange", "typoSizeStep",
    "_typoFind", "_typoTypeDef", "_rgbToHex", "toggleActLog", "logAdd", "flashStatus", "setStatus",
]
TABS = ["image", "page", "view", "home"]
SCRIPT_RE = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", re.I)


# ---------------------------------------------------------------- JS scan
def js_scan(src, base_line):
    """ตรวจโครงสร้าง JS แบบรู้จัก string/comment/regex. คืน (error|None, code_ที่ตัด_string_ออก)"""
    out = []; st = []; i = 0; n = len(src); prev = ""
    pairs = {")": "(", "]": "[", "}": "{"}
    import bisect
    nls = [k for k, ch in enumerate(src) if ch == "\n"]
    ln = lambda k: base_line + bisect.bisect_left(nls, k) + 1
    keep_nl = lambda seg: "\n" * seg.count("\n") if "\n" in seg else "S"
    while i < n:
        c = src[i]
        if c in "\"'`":
            q = c; j = i + 1
            while j < n and src[j] != q:
                if src[j] == "\\": j += 1
                elif src[j] == "\n" and q != "`":
                    return "string ไม่ปิด (บรรทัด %d)" % ln(i), None
                j += 1
            if j >= n: return "string ไม่ปิด (บรรทัด %d)" % ln(i), None
            out.append(keep_nl(src[i:j + 1])); i = j + 1; prev = "a"; continue
        if src.startswith("//", i):
            j = src.find("\n", i); j = n if j < 0 else j
            i = j; continue
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            if j < 0: return "comment /* ไม่ปิด (บรรทัด %d)" % ln(i), None
            out.append(keep_nl(src[i:j + 2])); i = j + 2; continue
        if c == "/" and prev in "(,=:[!&|?{};+-*%<>~^":
            j = i + 1; inc = False
            while j < n and (src[j] != "/" or inc):
                if src[j] == "\\": j += 1
                elif src[j] == "[": inc = True
                elif src[j] == "]": inc = False
                elif src[j] == "\n": return "regex ไม่ปิด (บรรทัด %d)" % ln(i), None
                j += 1
            out.append("S"); i = j + 1; prev = "a"; continue
        if c in "([{": st.append((c, i))
        elif c in ")]}":
            if not st or st[-1][0] != pairs[c]:
                return "วงเล็บ '%s' ไม่มีคู่ (บรรทัด %d)" % (c, ln(i)), None
            st.pop()
        if not c.isspace(): prev = "a" if (c.isalnum() or c in "_$") else c
        out.append(c); i += 1
    if st: return "วงเล็บ '%s' เปิดค้าง (บรรทัด %d)" % (st[-1][0], ln(st[-1][1])), None
    return None, "".join(out)


def ids_of(s):
    return (set(re.findall(r"""\bid\s*=\s*\\?["']([A-Za-z_][\w-]*)""", s)) |
            set(re.findall(r"""\.id\s*=\s*["']([A-Za-z_][\w-]*)""", s)))


def funcs_of(s):
    return (set(re.findall(r"function\s+([A-Za-z_$][\w$]*)\s*\(", s)) |
            set(re.findall(r"window\.([A-Za-z_$][\w$]*)\s*=", s)) |
            set(re.findall(r"(?:var|let|const)\s+([A-Za-z_$][\w$]*)\s*=\s*function", s)))


def inline_handlers(s):
    return sorted(set(re.findall(r'on(?:click|change|input|keydown|mousedown)="\s*([A-Za-z_$][\w$]*)\s*\(', s)))


# ---------------------------------------------------------------- static checks
def static_checks(cur, head):
    E, W, I = [], [], []
    # 1) script tags + JS structure
    if cur.count("<script") != cur.count("</script>"):
        E.append("<script> เปิด/ปิดไม่เท่ากัน")
    for m in SCRIPT_RE.finditer(cur):
        base = cur.count("\n", 0, m.start(1))
        err, code = js_scan(m.group(1), base)
        if err:
            E.append("JS: " + err); continue
        mm = re.search(r"=\s*(var|let|const|if|for|while|return)\b", code)
        if mm:
            E.append("JS: ค่าหลัง '=' หายไป เจอ '%s' แทน (บรรทัด %d)" %
                     (mm.group(1), base + code.count("\n", 0, mm.start()) + 1))
    # 2) required functions exactly once
    for fn in REQUIRED_FUNCS:
        c = len(re.findall(r"(?<![\w$.])function\s+" + re.escape(fn) + r"\s*\(", cur))
        if c != 1: E.append("ฟังก์ชันหลัก %s() พบ %d ครั้ง (ต้อง 1)" % (fn, c))
    # 3) getElementById / querySelector('#id') ต้องมี id จริง
    ids = ids_of(cur)
    refs = (set(re.findall(r"""getElementById\(\s*["']([A-Za-z_][\w-]*)["']\s*\)""", cur)) |
            set(re.findall(r"""querySelector(?:All)?\(\s*["']#([A-Za-z_][\w-]*)""", cur)))
    for r in sorted(refs - ids): E.append("อ้าง id '%s' แต่ไม่มี element นี้" % r)
    # 4) inline handler ต้องมีฟังก์ชันจริง
    fdef = funcs_of(cur)
    for h in inline_handlers(cur):
        if h not in fdef: E.append("ปุ่มเรียก %s() แต่ไม่มีฟังก์ชันนี้" % h)
    # 5) id ซ้ำใน HTML
    body = re.sub(r"<(script|style)[^>]*>[\s\S]*?</\1>", "", cur, flags=re.I)
    cnt = {}
    for x in re.findall(r'\sid="([^"]+)"', body): cnt[x] = cnt.get(x, 0) + 1
    for k, v in sorted(cnt.items()):
        if v > 1: E.append("id '%s' ซ้ำ %d ครั้ง" % (k, v))
    # 6) เทียบกับ HEAD
    if head is not None:
        allow = set(x.strip() for x in os.environ.get("OE_ALLOW_REMOVE_IDS", "").split(",") if x.strip())
        hid = ids_of(head)
        for x in sorted(hid - ids - allow): E.append("id '%s' หายไปเทียบกับ commit ล่าสุด" % x)
        for x in sorted((hid - ids) & allow): I.append("id '%s' ถูกลบ (อนุญาตแล้ว)" % x)
        if ids - hid: I.append("id ใหม่: " + ", ".join(sorted(ids - hid)))
        gone = sorted(funcs_of(head) - fdef)
        for x in gone:
            refs_left = len(re.findall(r"(?<![\w$])" + re.escape(x) + r"\s*\(", cur))
            (E if refs_left else W).append("ฟังก์ชัน %s() ถูกลบ%s" % (x, " แต่ยังมีที่เรียกใช้ %d จุด" % refs_left if refs_left else ""))
        hl, cl = head.split("\n"), cur.split("\n")
        ops = [o for o in difflib.SequenceMatcher(None, hl, cl, autojunk=False).get_opcodes() if o[0] != "equal"]
        I.append("บรรทัดที่เปลี่ยนเทียบ HEAD: %d ช่วง" % len(ops))
        for tag, a1, a2, b1, b2 in ops[:40]:
            prev_txt = (cl[b1].strip() if b1 < len(cl) and tag != "delete" else hl[a1].strip())[:110]
            I.append("  %-7s HEAD %d-%d -> ไฟล์ %d-%d | %s" % (tag, a1 + 1, a2, b1 + 1, b2, prev_txt))
        if len(ops) > 40: I.append("  ... อีก %d ช่วง" % (len(ops) - 40))
    # 7) CSS class ที่ไม่มีใครใช้ (warning)
    css = " ".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", cur))
    cls = set(re.findall(r"\.([A-Za-z_][\w-]*)", re.sub(r"\{[^{}]*\}", "{}", css)))
    rest = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", cur)
    rest = re.sub(r"data:[\w/+.-]+;base64,[A-Za-z0-9+/=]+", "", rest)   # ตัดรูป base64 ออก (เร็วขึ้นมาก)
    tokens = set(re.findall(r"[\w-]+", rest))
    unused = sorted(c for c in cls if c not in tokens)
    if unused: W.append("CSS class ไม่มีใครใช้: " + ", ".join(unused))
    return E, W, I


# ---------------------------------------------------------------- browser smoke test
def harness(handlers):
    need = sorted(set(REQUIRED_FUNCS) | set(handlers) | {"_setCurrent"})
    js = (
        "(function(){var Q=window.__qa={errors:[],steps:[]};"
        "window.addEventListener('error',function(e){Q.errors.push(String(e.message||'error')+' (line '+(e.lineno||'?')+')');});"
        "function S(n,f){try{var r=f();Q.steps.push({n:n,ok:r===true,msg:(r===true?'':'ผลไม่ตรงที่คาด')});}"
        "catch(x){Q.steps.push({n:n,ok:false,msg:String(x&&x.message||x)});}}"
        "function colorOf(el){return String(_rgbToHex(getComputedStyle(el).color)).toLowerCase();}"
        "function tbColor(){return String(document.getElementById('typoColor').value).toLowerCase();}"
        "window.addEventListener('load',function(){setTimeout(function(){"
        "__NEED__.forEach(function(fn){S('มีฟังก์ชัน '+fn,function(){return typeof window[fn]==='function';});});"
        "__TABS__.forEach(function(tb){S('คลิกแท็บ '+tb,function(){switchTab(tb);"
        "var a=document.querySelector('#edtabs .edtab.active'),p=document.querySelector('#edribbon .rpane.active');"
        "return !!a&&a.getAttribute('data-tab')===tb&&!!p&&p.getAttribute('data-pane')===tb;});});"
        "S('เข้าโหมดแก้ข้อความ',function(){if(!document.body.classList.contains('editmode'))toggleEdit();return document.body.classList.contains('editmode');});"
        "['nm','sechead'].forEach(function(k){"
        "S('เลือก '+k+' -> ปุ่มตั้งค่าเริ่มต้นกดได้',function(){var el=document.querySelector('.page .'+k);if(!el)return false;"
        "typoSelect(el,_typoTypeDef(k));var b=document.getElementById('typoSetDefault');return !!b&&!b.disabled;});"
        "S('เลือก '+k+' -> ปุ่มสีตรงกับสี element',function(){var el=document.querySelector('.page .'+k);return colorOf(el)===tbColor();});});"
        "S('ไม่เลือกอะไร -> ปุ่มตั้งค่าเริ่มต้นกดไม่ได้',function(){typoClear();var b=document.getElementById('typoSetDefault');"
        "return !!b&&b.disabled===true&&!b.classList.contains('on');});"
        "S('ออกโหมดแก้ข้อความ',function(){if(document.body.classList.contains('editmode'))toggleEdit();return !document.body.classList.contains('editmode');});"
        "var o=document.createElement('pre');o.id='__qa_out';o.textContent=JSON.stringify(Q);document.body.appendChild(o);"
        "},500);});})();"
    )
    js = js.replace("__NEED__", json.dumps(need)).replace("__TABS__", json.dumps(TABS))
    return "<script>" + js + "</script>"   # บรรทัดเดียว -> เลขบรรทัด error ตรงกับไฟล์จริง


def find_browser():
    env = os.environ.get("OE_BROWSER")
    cands = [env] if env else []
    cands += [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]
    for c in cands:
        if c and os.path.exists(c): return c
    return None


def browser_smoke(cur):
    import subprocess, tempfile, shutil, pathlib
    exe = find_browser()
    if not exe: return None, "ไม่พบ Chrome/Edge (ตั้ง OE_BROWSER=path ได้)"
    m = re.search(r"<head[^>]*>", cur, re.I)
    if not m: return None, "ไม่พบ <head>"
    tmpd = tempfile.mkdtemp(prefix="oe_verify_")
    try:
        page = os.path.join(tmpd, "page.html")
        with open(page, "w", encoding="utf-8", newline="") as f:
            f.write(cur[:m.end()] + harness(inline_handlers(cur)) + cur[m.end():])
        cmd = [exe, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
               "--disable-extensions", "--user-data-dir=" + os.path.join(tmpd, "profile"),
               "--virtual-time-budget=15000", "--dump-dom", pathlib.Path(page).as_uri()]
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=180)
        except subprocess.TimeoutExpired:
            return None, "เบราว์เซอร์ค้างเกิน 180 วินาที"
        out = r.stdout.decode("utf-8", "replace")
        mm = re.search(r'<pre id="__qa_out">([\s\S]*?)</pre>', out)
        if not mm:
            return None, "ไม่ได้ผลทดสอบจากเบราว์เซอร์ (exit %s) %s" % (r.returncode, r.stderr.decode("utf-8", "replace")[-300:])
        return json.loads(html.unescape(mm.group(1))), None
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)


# ---------------------------------------------------------------- main
def read_head():
    import subprocess
    try:
        r = subprocess.run(["git", "-C", ROOT, "show", "HEAD:" + TARGET], capture_output=True, timeout=60)
        if r.returncode != 0: return None, r.stderr.decode("utf-8", "replace").strip()
        return r.stdout.decode("utf-8").replace("\r\n", "\n"), None
    except Exception as e:
        return None, str(e)


def run_lint():
    import subprocess
    p = os.path.join(ROOT, "lint_oe.py")
    if not os.path.exists(p): return None, "ไม่พบ lint_oe.py"
    r = subprocess.run([sys.executable, p], capture_output=True, timeout=120)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def main():
    no_browser = "--no-browser" in sys.argv
    E, W, I, INC = [], [], [], []
    if not os.path.exists(PATH):
        print("FAIL: ไม่พบไฟล์", PATH); sys.exit(1)
    with open(PATH, encoding="utf-8") as f:
        cur = f.read().replace("\r\n", "\n")

    rc, lint_out = run_lint()
    if rc is None: INC.append("lint: " + lint_out)
    elif rc != 0: E.append("lint_oe.py FAIL:\n" + "\n".join("      " + x for x in lint_out.splitlines() if x.strip().startswith("-")))

    head, herr = read_head()
    if head is None: INC.append("อ่านไฟล์จาก commit ล่าสุดไม่ได้: " + herr)
    e, w, i = static_checks(cur, head); E += e; W += w; I += i

    if no_browser:
        INC.append("ไม่ได้ทดสอบในเบราว์เซอร์ (--no-browser)")
    else:
        res, berr = browser_smoke(cur)
        if res is None: INC.append("ทดสอบเบราว์เซอร์ไม่สำเร็จ: " + berr)
        else:
            for x in res.get("errors", []): E.append("JS error ตอนโหลด/รัน: " + x)
            steps = res.get("steps", [])
            bad = [s for s in steps if not s.get("ok")]
            for s in bad: E.append("ทดสอบ '%s' ไม่ผ่าน: %s" % (s.get("n"), s.get("msg")))
            I.append("ทดสอบในเบราว์เซอร์: ผ่าน %d/%d ข้อ" % (len(steps) - len(bad), len(steps)))

    print("=" * 60); print(" verify_oe.py  -  " + TARGET); print("=" * 60)
    for x in I: print(" i  " + x)
    for x in W: print(" !  " + x)
    for x in INC: print(" ?  " + x)
    for x in E: print(" X  " + x)
    print("-" * 60)
    if E:   print(" FAIL - %d error(s)  -> ห้ามบอกว่าเสร็จ / ห้าม commit" % len(E)); code = 1
    elif INC: print(" INCOMPLETE - ตรวจไม่ครบ %d ข้อ -> ยังถือว่าไม่ผ่าน" % len(INC)); code = 2
    else:   print(" PASS - ผ่านทุกข้อ (warning %d)" % len(W)); code = 0
    print(" หมายเหตุ: PASS = โค้ดโหลดได้และฟังก์ชันหลักทำงาน ยังต้องให้คนกดดูหน้าตาจริง")
    sys.exit(code)


if __name__ == "__main__":
    main()
