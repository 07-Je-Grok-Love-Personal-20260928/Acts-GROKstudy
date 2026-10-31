# -*- coding: utf-8 -*-
from common import md, esc, cq, verse_card, VER, DATE, CREEDS
from chap import SEC, mindtree
def index(chs):
    b=['<div class="intro2 glass reveal"><p>'+md("使徒行传是**教会历史的第一章**：复活升天的基督藉着圣灵与圣道，把福音从耶路撒冷带到罗马。本站先从**整本圣经与圣约**看它的位置，再看**导论结构**与**时间、故事、地图、文化**，然后逐章深读 28 章（故事线、真实背景、前因后果、圣经神学、==圣约神学==、!!难点!!、信条对照、应用），最后用**改革宗专题**、**三大信经**与**记忆自测**把它们收拢。")+'</p></div>']
    b.append('<h2 id="i1">📚 28 章一览</h2><div class="bgrid">'+"".join(f'<a class="bk glass reveal" href="{SEC[c["sec"]][2]}#c{c["no"]}" style="--gc:{SEC[c["sec"]][1]}"><span class="bi">{c["ic"]}</span><b>{c["no"]} · {c["t"]}</b><small>{c["kw"]}</small></a>' for c in chs)+'</div>')
    b.append('<div class="glegend">'+"".join(f'<span style="--gc:{c}">{n}</span>' for n,c,_ in SEC.values())+'</div>')
    b.append('<h2 id="i2">🧭 学习路线</h2><div class="flow">'+"".join(f'<a class="fstep" href="{h}"><span class="n">{k+1}</span>{t}</a>'+('<i class="farr">➜</i>' if k<6 else '') for k,(h,t) in enumerate([("bible.html","整本圣经与圣约：先看全景"),("intro.html","导论：作者、目的、结构、讲道"),("history.html","时间线、故事线、地图与文化"),("jerusalem.html","逐章深读（四段 28 章）"),("doctrine.html","十二个改革宗专题 · 信条对照"),("creeds.html","三大信经背诵与比较"),("memory.html","口诀、记忆卡、小考")]))+'</div>')
    b.append('<h2 id="i3">🌳 全书思维导图</h2>'+mindtree("🔥 使徒行传 28 章",chs))
    b.append('<h2 id="i4">✨ 一节总纲</h2>'+verse_card("徒1:8")+'<p class="note">全书照这节经文展开：圣灵降临（2 章）→ 耶路撒冷（1–7）→ 犹太与撒马利亚（8–12）→ 直到地极（13–28）。</p>')
    b.append('<h2 id="i5">🎨 颜色与标记</h2><div class="tbl"><table><tbody><tr><td><b class="key">金色粗体</b></td><td>重点：必须掌握的核心事件、教义与钥句</td></tr><tr><td><span class="hard">珊瑚红底</span></td><td>难点：历来争议或容易误解之处（附改革宗解答）</td></tr><tr><td><span class="cov">紫色下划线</span></td><td>圣约神学：恩典之约、应许、记号与印证</td></tr><tr><td><span class="term">青色虚线</span></td><td>术语与历史名词</td></tr><tr><td><button type="button" class="vs" data-t="例：“但圣灵降临在你们身上，你们就必得着能力……”（徒1:8）">徒1:8</button></td><td>经文出处，点按弹出和合本经文</td></tr><tr><td>📘📗📕📙</td><td>海德堡要理问答 · 比利时信条 · 多特信经（CCI 中译，逐字）· 威斯敏斯特标准（比较用）</td></tr></tbody></table></div>')
    return "".join(b)
def sources(stats):
    S=[("信经与信条（逐字引用来源）",[("CCI 使徒信经",CREEDS["apostles"]["url"]),("CCI 尼西亚信经",CREEDS["nicene"]["url"]),("CCI 亚他那修信经",CREEDS["athanasian"]["url"]),("CCI 海德堡要理问答","https://ccifellowship.org/books/book-of-praise/confessions/heidelberg-catechism"),("CCI 比利时信条","https://ccifellowship.org/books/book-of-praise/confessions/the-belgic-confession"),("CCI 多特信经","https://ccifellowship.org/books/book-of-praise/confessions/canons-of-dort")]),
       ("经文与地图",[("和合本（CUV）经文：getBible API","https://api.getbible.net/v2/cus/44/1.json"),("Natural Earth 地图数据（公有领域）","https://www.naturalearthdata.com/")]),
       ("改革宗参考（未直接引用原文，仅供延伸）",[("ccreformed.org","https://www.ccreformed.org/"),("reformedbeginner.net","https://reformedbeginner.net/"),("加拿大改革宗教会 CanRC","https://canrc.org/"),("北美联合改革宗教会 URCNA","https://www.urcna.org/"),("传承改革宗教会 HRC","https://heritagereformed.com/"),("基督教改革宗教会 PRCA","https://prca.org/"),("正统长老会 OPC","https://opc.org/"),("Mid-America Reformed Seminary","https://www.midamerica.edu/"),("Canadian Reformed Theological Seminary","https://crts.ca/"),("Puritan Reformed Theological Seminary","https://prts.edu/"),("Westminster Theological Seminary（Gaffin 等）","https://www.wts.edu/")]),
       ("威斯敏斯特标准（比较用）",[("RTF-USA 简体中文译本（贾少彬 译），本站引文取自其数据","https://rtf-usa.org/")])]
    b=['<h2 id="s1">🔖 来源</h2>']
    for k,(t,L) in enumerate(S): b.append(f'<h3 id="s1-{k}">{t}</h3><ul class="src">'+"".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n,u in L)+'</ul>')
    b.append('<h2 id="s2">✅ 校验结果（构建时自动生成）</h2><div class="tbl"><table><tbody>'+"".join(f'<tr><td><b>{k}</b></td><td>{v}</td></tr>' for k,v in stats)+'</tbody></table></div>')
    b.append('<h2 id="s3">⚠️ 说明与局限</h2><ul class="src"><li>信条引文逐字取自 ccifellowship.org 的中文译本；其他译本措辞可能不同。</li><li>年代多为近似值（保守学者常见观点），学界有其他看法。</li><li>地图路线为依据使徒行传地名连成的示意线，不代表精确的古代道路。</li><li>讲解、口诀与图表为本站学习整理，不是任何教会的正式文件；权威在圣经，其次在教会公认的信条。</li><li>“🔊 朗读”使用浏览器内置语音合成（Web Speech API），音色因设备而异。</li></ul>')
    b.append(f'<h2 id="s4">🗂️ 版本</h2><div class="tbl"><table><thead><tr><th>版本</th><th>日期</th><th>说明</th></tr></thead><tbody><tr><td>{VER}</td><td>{DATE}（台北时间）</td><td>首次发布：28 章逐章深读、整本圣经与圣约、导论、时间线与动画地图、十二个改革宗专题、三大信经背诵（含朗读）与比较、三项联合信条比较、记忆自测。</td></tr></tbody></table></div>')
    return "".join(b)
