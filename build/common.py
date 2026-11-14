# -*- coding: utf-8 -*-
import json, re, html as H
from bible import verses
CCI = "/workspace/cci"
VER = "v3.1.0"; DATE = "2026-11-14"; ASSET_V = "20261114h"
def strip(t): return re.sub(r'\^\d+', '', t)
_c = json.load(open(f"{CCI}/creeds.json")); _h = json.load(open(f"{CCI}/heidelberg.json"))
_b = json.load(open(f"{CCI}/belgic.json")); _d = json.load(open(f"{CCI}/dort.json"))
HCQ = {q['q']: dict(q, ld=l['number'], url=l.get('url', _h['url'])) for l in _h['lordsdays'] for q in l['questions']}
BCA = {a['number']: a for a in _b['articles']}
DH = {1: _d['heads'][0], 2: _d['heads'][1], 3: _d['heads'][2], 4: _d['heads'][2], 5: _d['heads'][3]}
DLAB = {1: "第一项教义", 2: "第二项教义", 3: "第三、四项教义", 4: "第三、四项教义", 5: "第五项教义"}
CREEDS = _c
QUOTES = []   # (source_key, text) for verification
def bc_body(n): return strip(BCA[n]['text']).split('\n\n- ')[0].strip()
def dort_art(h, n):
    for a in DH[h]['articles']:
        if a['number'] == n: return a
    raise KeyError((h, n))
def dort_body(h, n): return strip(dort_art(h, n)['text']).split('\n\n- ')[0].strip()
def esc(s): return H.escape(s, quote=True)

def cq(item, compact=False):
    """返回逐字引文块（来自 ccifellowship.org）。item: ('hc',n[,excerpt]) / ('bc',n[,excerpt]) / ('dort',head,n[,excerpt])"""
    kind = item[0]
    if kind == 'hc':
        n = item[1]; q = HCQ[n]; full = strip(q['answer']); qq = strip(q['question'])
        ex = item[2] if len(item) > 2 else None
        label = f"海德堡要理问答 第{n}问（主日{q['ld']}）"; url = q['url']
        body = ex or full
        if ex: assert ex in full, ("HC", n, ex)
        QUOTES.append(('hc', n, body)); QUOTES.append(('hcq', n, qq))
        inner = f'<p class="q">{esc(qq)}</p><p class="a">{esc(body)}</p>'
        cls = "hc"
    elif kind == 'bc':
        n = item[1]; a = BCA[n]; full = bc_body(n); ex = item[2] if len(item) > 2 else None
        if ex: assert ex in full, ("BC", n, ex)
        body = ex or full; label = f"比利时信条 {a['title']}"; url = a['url']
        QUOTES.append(('bc', n, body)); inner = "".join(f'<p>{esc(p)}</p>' for p in body.split('\n\n') if p.strip()); cls = "bc"
    else:
        h, n = item[1], item[2]; a = dort_art(h, n); full = dort_body(h, n); ex = item[3] if len(item) > 3 else None
        if ex: assert ex in full, ("DORT", h, n, ex)
        body = ex or full; label = f"多特信经 {DLAB[h]} {a['title']}"; url = a['url']
        QUOTES.append(('dort', (h, n), body)); inner = "".join(f'<p>{esc(p)}</p>' for p in body.split('\n\n') if p.strip()); cls = "dt"
    part = "（节录）" if len(item) > (3 if kind == 'dort' else 2) else ""
    return (f'<blockquote class="cci {cls}" data-cci="{kind}"><div class="cci-h"><span class="tag">{"📘" if cls=="hc" else "📗" if cls=="bc" else "📕"} {esc(label)}{part}</span>'
            f'<a href="{url}" target="_blank" rel="noopener">CCI 原文 ↗</a></div>{inner}</blockquote>')

VCACHE = {}
def vtext(ref):
    if ref in VCACHE: return VCACHE[ref]
    t = None
    m = re.match(r'^(\D+?)(\d+):(\d+)(?:-(\d+))?$', ref)
    if m:
        try: t = verses(ref)
        except Exception as e: print("VERSE FAIL", ref, e); t = None
    VCACHE[ref] = t; return t

def md(s):
    s = esc(s).replace("&quot;", "\"")
    def vref(m):
        r = H.unescape(m.group(1)); t = vtext(r)
        if t: return f'<button type="button" class="vs" data-t="{esc(t)}">{esc(r)}</button>'
        return f'<span class="vs0">{esc(r)}</span>'
    s = re.sub(r'\{\{(.+?)\}\}', vref, s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b class="key">\1</b>', s)
    s = re.sub(r'!!(.+?)!!', r'<span class="hard">\1</span>', s)
    s = re.sub(r'==(.+?)==', r'<span class="cov">\1</span>', s)
    s = re.sub(r'\[\[(.+?)\]\]', r'<span class="term">\1</span>', s)
    s = re.sub(r'__(.+?)__', r'<mark class="hl">\1</mark>', s)
    s = re.sub(r'~~(.+?)~~', r'<span class="mk-w">\1</span>', s)
    s = re.sub(r'\+\+(.+?)\+\+', r'<span class="mk-d">\1</span>', s)
    return s


def md_rich(s):
    """Like md(), but keep literal HTML (trusted generator content such as speech grids)."""
    def vref(m):
        r = m.group(1); t = vtext(r)
        if t: return f'<button type="button" class="vs" data-t="{esc(t)}">{esc(r)}</button>'
        return f'<span class="vs0">{esc(r)}</span>'
    s = re.sub(r'\{\{(.+?)\}\}', vref, s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b class="key">\1</b>', s)
    s = re.sub(r'!!(.+?)!!', r'<span class="hard">\1</span>', s)
    s = re.sub(r'==(.+?)==', r'<span class="cov">\1</span>', s)
    s = re.sub(r'\[\[(.+?)\]\]', r'<span class="term">\1</span>', s)
    s = re.sub(r'__(.+?)__', r'<mark class="hl">\1</mark>', s)
    s = re.sub(r'~~(.+?)~~', r'<span class="mk-w">\1</span>', s)
    s = re.sub(r'\+\+(.+?)\+\+', r'<span class="mk-d">\1</span>', s)
    return s

def verse_card(ref, cls=""):
    t = vtext(ref); assert t, ref
    return f'<figure class="kv {cls}"><blockquote>{esc(t)}</blockquote><figcaption>— {esc(ref)}（和合本）</figcaption></figure>'

def callout(kind, title, body, hid=None):
    icon={"key":"⭐","hard":"⚠️","doc":"📖","app":"🌱","mem":"🧠"}[kind]
    label={"key":"重点","hard":"难点","doc":"教义","app":"应用","mem":"记忆钩"}[kind]
    ida=f' id="{esc(hid)}"' if hid else ""
    return f'<aside class="co co-{kind}"><h4{ida}>{icon} {label} · {esc(title)}</h4><div>{md(body)}</div></aside>'

NAV = [("index.html","🏠","首页总览"),("bible.html","📜","整本圣经·圣约"),("intro.html","🧭","导论·结构"),("history.html","🗺️","时间·故事·地图"),
       ("culture.html","🏺","地理·历史·文化"),
       ("jerusalem.html","🔥","耶路撒冷 1–7"),("samaria.html","🌊","犹太撒玛利亚 8–12"),("missions.html","⛵","宣教旅行 13–19"),("rome.html","⛓️","往罗马 20–28"),
       ("doctrine.html","📘","改革宗专题"),("creeds.html","✝️","三大信经"),("memory.html","🧠","记忆·自测"),("sources.html","🔖","来源·校验")]

SITE = [
    ("总览与方法", ["index.html","bible.html","intro.html"]),
    ("时间与地理", ["history.html","culture.html"]),
    ("逐章深读", ["jerusalem.html","samaria.html","missions.html","rome.html"]),
    ("教义与记忆", ["doctrine.html","creeds.html","memory.html","sources.html"]),
]
NAV_D = {h:(ic,t) for h,ic,t in NAV}
_CN = "零一二三四五六七八九"
def cn_num(n):
    if n<=0: return str(n)
    if n<10: return _CN[n]
    if n==10: return "十"
    if n<20: return "十"+_CN[n-10]
    if n<100:
        return _CN[n//10]+"十"+(_CN[n%10] if n%10 else "")
    return str(n)

def _htext(t, attrs):
    m=re.search(r'\bdata-toc="([^"]+)"', attrs or "")
    if m: return H.unescape(m.group(1))
    t=re.sub(r'<small[^>]*>.*?</small>','',t,flags=re.S)
    t=re.sub(r'<[^>]+>','',t)
    t=H.unescape(re.sub(r'\s+',' ',t).strip())
    t=re.sub(r'^[一二三四五六七八九十百]+、\s*','',t)
    return t

def _toc_items(body):
    raw=re.findall(r'<h([2-4])([^>]*)>(.*?)</h\1>', body, re.S)
    items=[]
    for lv,attrs,t in raw:
        mid=re.search(r'\bid="([^"]+)"', attrs or "")
        if not mid: continue
        items.append((int(lv), mid.group(1), _htext(t, attrs)))
    while items and items[0][0]>2:
        items.pop(0)
    return items

def _li(level, hid, label, kids_html, num=None):
    has=bool(kids_html)
    tw=(f'<button type="button" class="tw" aria-expanded="true" aria-label="折叠「{esc(label)}」" data-for="{esc(hid)}"></button>'
        if has else '<span class="tw tw-sp" aria-hidden="true"></span>')
    badge=f'<span class="tn">{esc(num)}</span>' if num else ""
    a=f'<a href="#{esc(hid)}" class="t{level}">{badge}{esc(label)}</a>'
    inner=f'<div class="toc-row">{tw}{a}</div>'
    if has:
        return f'<li class="tl{level}" data-id="{esc(hid)}">{inner}<ol class="toc-kids">{kids_html}</ol></li>'
    return f'<li class="tl{level} leaf" data-id="{esc(hid)}">{inner}</li>'

def toc_from(body):
    items=_toc_items(body)
    # nest: list of (lv,id,label,children)
    root=[]; stack=[]
    for lv,hid,lab in items:
        node={"lv":lv,"id":hid,"lab":lab,"ch":[]}
        while stack and stack[-1]["lv"]>=lv:
            stack.pop()
        if not stack:
            root.append(node)
        else:
            stack[-1]["ch"].append(node)
        stack.append(node)
    def render(nodes, level):
        out=[]
        for i,n in enumerate(nodes,1):
            kids=render(n["ch"], level+1) if n["ch"] else ""
            num=cn_num(i) if level==1 else None
            out.append(_li(level, n["id"], n["lab"], kids, num))
        return "".join(out)
    page_ol=render(root,1) or '<li class="leaf"><div class="toc-row"><span class="tw tw-sp"></span><a href="#main">本页</a></div></li>'
    return page_ol

def site_toc(fn):
    out=['<ol class="toc-l toc-site">']
    for i,(g,hs) in enumerate(SITE,1):
        kids=""
        cur=any(h==fn for h in hs)
        for h in hs:
            ic,t=NAV_D[h]
            on=' class="on"' if h==fn else ""
            kids+=f'<li class="tl2 leaf"><div class="toc-row"><span class="tw tw-sp" aria-hidden="true"></span><a href="{h}"{on} class="t2">{ic} {esc(t)}</a></div></li>'
        open_="true" if cur else "true"
        out.append(f'<li class="tl1{" curp" if cur else ""}" data-id="site-{i}"><div class="toc-row">'
                   f'<button type="button" class="tw" aria-expanded="{open_}" aria-label="折叠「{esc(g)}」" data-for="site-{i}"></button>'
                   f'<a href="{hs[0]}" class="t1"><span class="tn">{cn_num(i)}</span>{esc(g)}</a></div>'
                   f'<ol class="toc-kids">{kids}</ol></li>')
    out.append('</ol>')
    return "".join(out)

def page(fn, title, sub, body, hero_cls="", extra_head="", maps=False):
    nav = "".join(f'<a href="{h}" class="{"on" if h==fn else ""}"><span>{i}</span>{t}</a>' for h, i, t in NAV)
    idx = [h for h, _, _ in NAV].index(fn)
    prv = NAV[idx-1] if idx > 0 else None; nxt = NAV[idx+1] if idx < len(NAV)-1 else None
    pn = '<nav class="pn">' + (f'<a href="{prv[0]}">← {prv[1]} {prv[2]}</a>' if prv else '<span></span>') + (f'<a href="{nxt[0]}">{nxt[1]} {nxt[2]} →</a>' if nxt else '<span></span>') + '</nav>'
    maps_js = (f'<script src="assets/maps-data.js?v={ASSET_V}" defer></script><script src="assets/maps.js?v={ASSET_V}" defer></script>' if maps else '')
    return f'''<!doctype html><html lang="zh-CN" data-theme="night"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)+" · 使徒行传深读 GROKstudy" if fn!="index.html" else "使徒行传深读 GROKstudy"}</title><meta name="description" content="{esc(sub)}">
<script>try{{var t=localStorage.getItem('acts-theme');if(t)document.documentElement.dataset.theme=t;if(localStorage.getItem('acts-toc')==='0')document.documentElement.classList.add('toc-off');var w=localStorage.getItem('acts-tocw');if(w){{var n=+w;if(n>=220&&n<=640)document.documentElement.style.setProperty('--tocw',n+'px')}}}}catch(e){{}}</script>
<link rel="stylesheet" href="assets/style.css?v={ASSET_V}">{extra_head}</head><body>
<div class="bg" aria-hidden="true"><i></i><i></i><i></i></div><div id="prog"></div>
<header class="top"><button id="tocbtn" class="ib" aria-label="目录" title="显示/隐藏目录 (T)">☰</button><a class="brand" href="index.html">🔥 使徒行传<b>深读</b></a>
<nav class="mainnav">{nav}</nav><button id="navbtn" class="ib" aria-label="页面菜单">▦</button><button id="themebtn" class="ib" aria-label="切换主题" title="切换明暗">🌗</button></header>
<div class="navdrop" id="navdrop">{nav}</div>
<div id="tocwrap"><aside id="toc" aria-label="目录"><div class="toc-h"><b>📑 目录</b>
<div class="toc-tools"><button type="button" class="btn ghost sm" id="toc-ex" title="展开全部">全部展开</button>
<button type="button" class="btn ghost sm" id="toc-cl" title="收起二级与三级">收起下级</button>
<button class="ib sm" id="tocx" aria-label="收起目录">✕</button></div>
<input id="tocq" type="search" placeholder="筛选目录…" aria-label="筛选目录"></div>
<div class="toc-sec"><h2 class="toc-sh">站内导航</h2>{site_toc(fn)}</div>
<div class="toc-sec"><h2 class="toc-sh">本页目录</h2><ol class="toc-l toc-page">{toc_from(body)}</ol></div>
</aside>
<div id="tocresizer" class="toc-resizer" role="separator" aria-orientation="vertical" aria-valuemin="220" aria-valuemax="640" aria-label="拖动以调整目录宽度，双击恢复默认" tabindex="0"></div>
</div>
<div id="scrim"></div>
<main id="main"><section class="hero {hero_cls}"><div class="hero-in"><p class="eyebrow">使徒行传 · 教会历史 · 欧陆改革宗深读 · {VER}</p><h1>{title}</h1><p class="sub">{sub}</p></div></section>
<div class="legend glass" id="legend"><b class="lg-t">笔记标记</b>
<span class="key">重点</span><span class="hard">难点</span><span class="cov">圣约神学</span><span class="term">术语</span>
<mark class="hl">底纹必记</mark><span class="mk-u">实线强调</span><span class="mk-d">虚线提示</span><span class="mk-w">波浪易错</span>
<button type="button" class="vs" data-t="点按蓝色经文出处，可弹出和合本经文。">经文出处</button>
<span class="lg-cci">📘📗📕 CCI 逐字引文</span>
<span class="lg-co co-key">⭐ 重点框</span><span class="lg-co co-hard">⚠️ 难点框</span><span class="lg-co co-doc">📖 教义框</span><span class="lg-co co-app">🌱 应用框</span><span class="lg-co co-mem">🧠 记忆钩</span>
</div>
{body}
{pn}
<footer class="foot glass"><p>使徒行传深读 · acts-{DATE.replace("-","")}-{VER}-GROKstudy · 信经与信条引文逐字取自 <a href="https://ccifellowship.org/books/book-of-praise" target="_blank" rel="noopener">ccifellowship.org《敬拜手册》</a>（构建时程序核对）；经文为和合本。讲解、图表与口诀为本站学习整理。</p></footer>
</main><button id="totop" class="fab" aria-label="回到顶部">↑</button>
{maps_js}<script src="assets/anim.js?v={ASSET_V}" defer></script><script src="assets/app.js?v={ASSET_V}" defer></script></body></html>'''

_W = json.load(open("/workspace/Westminster-Standards-GROKstudy/generator/data/standards.json"))
def _ws(t): return re.sub(r'⟦\d+⟧', '', t)
def wq(kind, a, b=None, ex=None):
    """威斯敏斯特引文（RTF-USA 简体中文译本，贾少彬 译）。kind: wcf(ch,sec) / wsc(q) / wlc(q)"""
    if kind == 'wcf':
        full = _ws(_W['wcf'][a-1]['secs'][b-1]['text']); label = f"威斯敏斯特信仰告白 {a}.{b}（{_W['wcf'][a-1]['title']}）"
    else:
        it = _W[kind][a-1]; full = _ws(it['ques']) + "　" + _ws(it['ans']); label = ("威斯敏斯特小要理问答" if kind=='wsc' else "威斯敏斯特大要理问答") + f" 第{a}问"
    body = ex or full
    if ex: assert ex in full, (kind, a, b, ex)
    QUOTES.append(('w'+kind, (a, b), body))
    return (f'<blockquote class="cci ws" data-cci="w"><div class="cci-h"><span class="tag">📙 {esc(label)}{"（节录）" if ex else ""}</span>'
            f'<span class="src">RTF-USA 中文译本</span></div><p>{esc(body)}</p></blockquote>')
