# -*- coding: utf-8 -*-
import json, re
from common import md, esc, vtext
from chap import SEC
def plain(s): return re.sub(r'\{\{(.+?)\}\}',r'\1',re.sub(r'(\*\*|!!|==|\[\[|\]\])','',s))
def data(chs):
    return [dict(id=f'c{c["no"]}',n=f'第 {c["no"]} 章 · {c["t"]}',ab=str(c["no"]),ic=c["ic"],kw=c["kw"],kv=c["kv"],kvt=vtext(c["kv"]),place=plain(c["place"]).split("（")[0][:30],date=plain(c["date"]),mn=plain(c["mn"]),g=c["sec"],c=SEC[c["sec"]][1],ch=1,pg=SEC[c["sec"]][2]+f'#c{c["no"]}') for c in chs]
MN=[("jer","1–7","升 灵 瘸 审 亚 七 司","升天 · 圣灵降临 · 医治瘸腿 · 公会审问 · 亚拿尼亚 · 选立七人 · 司提反"),
    ("sam","8–12","腓 扫 哥 安 希","腓利 · 扫罗归信 · 哥尼流 · 安提阿 · 希律之死"),
    ("mis","13–19","差 路 会 腓 雅 哥 以","差派 · 路司得 · 耶路撒冷会议 · 腓立比 · 雅典 · 哥林多 · 以弗所"),
    ("rom","20–28","米 捕 辩 谋 腓 非 亚 船 罗","米利都 · 被捕 · 台阶自辩 · 密谋 · 腓力斯 · 非斯都 · 亚基帕 · 船难 · 罗马")]
def build(chs):
    D=data(chs)
    b=['<h2 id="m1">一、28 章口诀（四段）</h2><div class="mnem glass reveal">'+"".join(f'<p class="big" style="color:{SEC[g][1]}"><small>{r} 章</small> {t}</p><p class="note">{d}</p>' for g,r,t,d in MN)+'<p class="note">总口诀：<b class="key">“京 · 犹撒 · 旅 · 罗”</b>——耶路撒冷（7 章）、犹太撒马利亚（5 章）、宣教旅行（7 章）、往罗马（9 章）：7-5-7-9，合 28 章。</p></div>']
    b.append('<div class="chips">'+"".join(f'<a class="chip" href="{d["pg"]}" style="--c:{d["c"]}"><span>{d["ic"]}</span>{d["ab"]}<small>{d["kw"]}</small></a>' for d in D)+'</div>')
    b.append('<h3 id="m1b">🔢 数字记忆</h3><div class="tbl"><table><tbody>'+"".join(f'<tr><td><b class="key">{a}</b></td><td>{md(c)}</td></tr>' for a,c in [("1:8","全书大纲：耶路撒冷 → 犹太 → 撒马利亚 → 地极"),("40","复活后显现四十天（{{徒1:3}}）"),("120","楼上祷告的人数（{{徒1:15}}）"),("3000 / 5000","五旬节受洗三千（2:41）；男丁约五千（4:4）"),("7","选立七位执事（6:3）"),("3","保罗归信讲述三次（9、22、26）；三次宣教旅行；三位官员宣告无罪"),("6","六个进展报告：6:7 · 9:31 · 12:24 · 16:5 · 19:20 · 28:31"),("276","船上的人数（{{徒27:37}}）"),("2","在凯撒利亚两年（24:27）、在罗马两年（28:30）")])+'</tbody></table></div>')
    b.append('<h2 id="m2">二、28 章钥字 + 钥节 + 记忆钩</h2><div class="tbl"><table><thead><tr><th>章</th><th>钥字</th><th>钥节</th><th>记忆钩</th><th>何时 · 何地</th></tr></thead><tbody>'+"".join(f'<tr style="--c:{d["c"]}"><td class="bk"><a href="{d["pg"]}">{d["ic"]} {d["n"]}</a></td><td><b class="key">{d["kw"]}</b></td><td><button type="button" class="vs" data-t="{esc(d["kvt"])}">{d["kv"]}</button></td><td>{esc(d["mn"])}</td><td><small>{esc(d["date"])} · {esc(d["place"])}</small></td></tr>' for d in D)+'</tbody></table></div>')
    b.append('<h2 id="m3">三、记忆卡（点按翻转）</h2><div class="fc-tools"><button id="fcshuf" class="btn">🔀 打乱</button><button id="fcall" class="btn">🔁 全部翻回</button></div><div class="cards" id="fcards">'+"".join(f'<div class="flip sm" tabindex="0" role="button" style="--gc:{d["c"]}"><div class="fi-in"><div class="ff"><span>{d["ic"]}</span><b>{d["n"]}</b><em>钥字？钥节？</em></div><div class="fb"><b class="key">{d["kw"]}</b><p>{esc(d["kvt"])}</p><small>— {d["kv"]}</small></div></div></div>' for d in D)+'</div>')
    b.append('<h2 id="m4">四、钥节填空</h2><div class="cloze" id="cloze"></div><p class="note">随机挖去钥节中的一个词，点按“显示”核对。刷新页面换一组。</p>')
    b.append('<h2 id="m5">五、自测小考</h2><div class="quiz glass" id="quiz"><div class="qz-h"><span id="qzn">第 1 题</span><span id="qzs">得分 0</span></div><p class="qz-q" id="qzq"></p><div class="qz-o" id="qzo"></div><p class="qz-f" id="qzf" aria-live="polite"></p><div class="qz-b"><button class="btn" id="qznext">下一题 ➜</button><button class="btn ghost" id="qzre">重新开始</button></div></div>')
    pal=[("🚪","大门","1–2","门口一朵云（升天）+ 门框着了火（五旬节）"),("🛋️","客厅","3–5","沙发上坐着跳起来的瘸子；墙上贴“顺从神不顺从人”"),("🍽️","餐厅","6–7","七个服事饭桌的人；窗外飞来石头（司提反）"),("🚗","车库","8","一辆马车，太监在读以赛亚书"),("⚡","走廊","9","一道强光，地上跌倒一个人"),("🛏️","屋顶","10–11","大布从天降下，里面有各样走兽"),("🔓","地下室","12","铁门自己开了，锁链掉在地上"),
         ("🗺️","书房","13–14","墙上挂着第一次旅行地图"),("⚖️","会议室","15","圆桌会议：“我们得救乃是因主耶稣的恩”"),("🎵","浴室","16","半夜唱歌，地震了"),("🏛️","阳台","17","对着城里的祭坛：“未识之神”"),("⛺","工作间","18","织帐棚的工具"),("🔥","壁炉","19","在烧邪术书"),
         ("👋","前院","20","米利都码头的拥抱告别"),("⛓️","大门外","21–26","锁链、法庭、王座"),("🌊","泳池","27","船难：木板漂浮"),("🏠","客房","28","租来的房子，门开着，人来人往")]
    b.append('<h2 id="m6">六、记忆宫殿：走一遍你的家</h2><div class="palace">'+"".join(f'<div class="pl glass reveal"><span>{a}</span><b>{c}</b><i>徒 {d}</i><p>{e}</p></div>' for a,c,d,e in pal)+'</div>')
    plan=[(i,f"徒{i}") for i in range(1,29)]
    b.append('<h2 id="m7">七、28 天通读计划（一天一章）</h2><div class="plan" id="plan">'+"".join(f'<label class="pd glass"><input type="checkbox" data-d="{d}"><b>第 {d} 天</b><span>{t} · {D[d-1]["kw"]}</span></label>' for d,t in plan)+'</div><p class="note">勾选会保存在本机浏览器（localStorage）。读完后复习：口诀 + 小考 + 三大信经背诵。</p>')
    b.append(f'<script id="epdata" type="application/json">{json.dumps(D,ensure_ascii=False).replace("</","<\\/")}</script>')
    return "".join(b)
