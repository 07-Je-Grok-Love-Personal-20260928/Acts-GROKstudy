# -*- coding: utf-8 -*-
from common import md, esc, cq, wq, verse_card, vtext, callout
from geo import chmap
from maps_ui import chapter_pair
SEC = {"jer":("耶路撒冷 · 1–7 章","#f5b942","jerusalem.html"),"sam":("犹太 · 撒马利亚 · 8–12 章","#3fd39a","samaria.html"),
       "mis":("宣教旅行 · 13–19 章","#4fb3ff","missions.html"),"rom":("往罗马 · 20–28 章","#ff6b8b","rome.html")}
def flow(steps, end):
    s='<div class="flow">'
    for i,t in enumerate(steps): s+=f'<div class="fstep"><span class="n">{i+1}</span>{md(t)}</div><i class="farr">➜</i>'
    return s+f'<div class="fstep end">📖 {md(end)}</div></div>'
def sbar(ol):
    seg="".join(f'<div class="seg" style="flex:1" title="{esc(r)} {esc(t)}"><b>{esc(r)}</b><span>{esc(t)}</span></div>' for r,t in ol)
    return f'<div class="sbar">{seg}</div>'
def conf(c):
    return wq(*c[1:]) if c[0]=='w' else cq(c)
def chapter(c):
    i=f'c{c["no"]}'; sname,col,_=SEC[c["sec"]]
    facts=[("📅","时间",c["date"]),("📍","地点",c["place"]),("👥","主要人物",c["who"]),("🧭","1:8 进程",sname)]
    fx="".join(f'<div class="fact"><span class="fi">{a}</span><b>{b}</b><p>{md(t)}</p></div>' for a,b,t in facts)
    ol="".join(f'<li><b>{esc(r)}</b> {md(t)}</li>' for r,t in c["ol"])
    hards="".join(f'<details class="hardq"><summary>⚠️ {md(q)}</summary><p>{md(a)}</p></details>' for q,a in c.get("hard",[]))
    confs="".join(conf(x) for x in c.get("conf",[]))
    apps="".join(f'<li>{md(a)}</li>' for a in c["app"])
    hard_blk=f'<aside class="co co-hard"><h4 id="{i}-hd">⚠️ 难点 · 点开看改革宗解答</h4>{hards}</aside>' if hards else ''
    return f'''<section class="ep" id="{i}" style="--gc:{col}">
<h2 id="{i}-t" class="ep-h" data-toc="第 {c["no"]} 章 · {c["t"]}"><span class="ei">{c["ic"]}</span>第 {c["no"]} 章 · {c["t"]} <small>{c["ref"]} · {sname}</small></h2>
<div class="ep-banner glass reveal"><div class="kwbox"><span class="kwl">钥字</span><span class="kw">{c["kw"]}</span></div><p class="core">💎 {md(c["core"])}</p>{verse_card(c["kv"])}</div>
<div class="facts">{fx}</div>
{chapter_pair(c)}
<h3 id="{i}-st">📖 故事线：发生了什么</h3><div class="card glass"><p>{md(c["story"])}</p></div>{sbar(c["ol"])}<ol class="outline">{ol}</ol>
<h3 id="{i}-bg">🏺 真实背景与文化</h3><div class="card glass culture"><p>{md(c["bg"])}</p></div>
<h3 id="{i}-why">🔗 前因后果</h3>{flow(c["why"], c["res"])}
<h3 id="{i}-bt">📜 圣经神学 · 圣约神学</h3><div class="two"><aside class="co co-doc"><h4 id="{i}-btd">📖 教义 · 在整本圣经中</h4><div>{md(c["bt"])}</div></aside><aside class="co co-doc ct"><h4 id="{i}-ct">🤝 圣约视角</h4><div>{md(c["ct"])}</div></aside></div>
<h3 id="{i}-rf">🌷 欧陆改革宗要点</h3><div class="two"><aside class="co co-key"><h4 id="{i}-core">⭐ 重点 · 本质核心</h4><div>{md(c["rf"])}</div></aside>{hard_blk}</div>
{f'<div class="confs">{confs}</div>' if confs else ''}
<h3 id="{i}-ap">🌱 应用与记忆</h3>
<aside class="co co-app"><h4 id="{i}-appx">🌱 应用 · 今天怎样活</h4><ul class="apps">{apps}</ul></aside>
<aside class="co co-mem"><h4 id="{i}-mn">🧠 记忆钩 · 第 {c["no"]} 章</h4><div>{md(c["mn"])}</div></aside>
<div class="flip" tabindex="0" role="button" aria-label="翻转记忆卡"><div class="fi-in"><div class="ff"><span>🧠 记忆钩</span><b>第 {c["no"]} 章 · {c["kw"]}</b><em>点按翻转</em></div><div class="fb"><p>{md(c["mn"])}</p></div></div></div>
</section>'''
def mindtree(title, chs):
    br="".join(f'<li style="--gc:{SEC[c["sec"]][1]}"><a href="#c{c["no"]}" class="mt-b">{c["ic"]} {c["no"]} · <b>{c["kw"]}</b></a><ul>'+"".join(f'<li><span>{t}</span></li>' for _,t in c["ol"][:3])+'</ul></li>' for c in chs)
    return f'<div class="mtree glass reveal"><div class="mt-root">{title}</div><ul class="mt-l1">{br}</ul></div>'
def gtable(chs):
    rows="".join(f'<tr style="--gc:{SEC[c["sec"]][1]}"><td><a href="#c{c["no"]}">{c["ic"]} 第 {c["no"]} 章</a></td><td><b class="kwt">{c["kw"]}</b></td><td>{md(c["date"])}</td><td>{md(c["place"])}</td><td>{md(c["core"])}</td></tr>' for c in chs)
    return f'<div class="tbl"><table><thead><tr><th>章</th><th>钥字</th><th>时间</th><th>地点</th><th>一句话核心</th></tr></thead><tbody>{rows}</tbody></table></div>'
