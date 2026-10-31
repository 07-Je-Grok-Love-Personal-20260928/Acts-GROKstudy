# -*- coding: utf-8 -*-
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from common import page, QUOTES, VER, DATE, md
from acts_a import CH_A; from acts_b import CH_B; from acts_c import CH_C; from acts_d import CH_D
from chap import chapter, mindtree, gtable
import geo, p_whole, p_intro, p_hist, p_doc, p_creed, p_mem, p_misc
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, "docs")
os.makedirs(os.path.join(D, "assets", "geo"), exist_ok=True)
geo.base_svg(os.path.join(D, "assets", "geo", "med.svg"))
CH = CH_A + CH_B + CH_C + CH_D
assert [c["no"] for c in CH] == list(range(1, 29))
def W(fn, html):
    open(os.path.join(D, fn), "w", encoding="utf-8").write(html); print("wrote", fn, len(html)//1024, "KB")
def grp(fn, title, sub, chs, intro):
    body = f'<h2 id="ov">🗂️ 本段总览</h2><div class="card glass"><p>{md(intro)}</p></div>' + mindtree(title, chs) + gtable(chs) + "".join(chapter(c) for c in chs)
    W(fn, page(fn, title, sub, body))
W("index.html", page("index.html", "使徒行传深读", "教会历史的第一章 · 28 章逐章 · 整本圣经与圣约 · 时间故事地图 · 欧陆改革宗 · 三项联合信条与三大信经逐字对照", p_misc.index(CH), "home"))
W("bible.html", page("bible.html", "整本圣经与圣约", "先看全景：使徒行传在创造—堕落—救赎—成全的救赎历史与恩典之约中的位置", p_whole.build()))
W("intro.html", page("intro.html", "导论 · 结构", "作者、读者、年代、写作目的；1:8 大纲；六个进展报告；讲道一览；路加福音与彼得/保罗平行", p_intro.build()))
W("history.html", page("history.html", "时间 · 故事 · 地图", "主后 30–70 年：时间线、16 个场景、动画路线地图、文化区域、罗马官员与真实世界", p_hist.build()))
grp("jerusalem.html", "耶路撒冷 · 1–7 章", "升天 · 五旬节 · 使徒教训 · 逼迫 · 司提反殉道", CH[0:7],
    "主后约 30–34 年。圣灵降临，教会在耶路撒冷诞生，**使徒的教训、交接、擘饼、祈祷**成为教会的生命。逼迫从外面来（公会），罪从里面来（亚拿尼亚），纷争在中间（寡妇被忽略）——道却一直兴旺（{{徒6:7}}）。以司提反殉道作结。")
grp("samaria.html", "犹太 · 撒马利亚 · 8–12 章", "腓利 · 扫罗归信 · 彼得与哥尼流 · 安提阿 · 希律之死", CH[7:12],
    "主后约 34–44 年。逼迫使门徒分散，福音**跨越种族与宗教的边界**：撒马利亚人、埃提阿伯太监、外邦人哥尼流、安提阿的希腊人。最大的逼迫者扫罗成为外邦人的使徒。以暴君希律之死与“神的道日见兴旺”（{{徒12:24}}）作结。")
grp("missions.html", "宣教旅行 · 13–19 章", "安提阿差派 · 第一、二、三次宣教旅行 · 耶路撒冷会议 · 以弗所", CH[12:19],
    "主后约 46–57 年。安提阿教会按圣灵的吩咐差派巴拿巴与保罗；福音进入小亚细亚、欧洲与亚细亚省。耶路撒冷会议确认**因恩典得救，不必受割礼**。以“主的道大大兴旺，而且得胜”（{{徒19:20}}）作结。")
grp("rome.html", "往罗马 · 20–28 章", "米利都告别 · 耶路撒冷被捕 · 五次辩护 · 船难 · 罗马", CH[19:28],
    "主后约 57–62 年。保罗像他的主一样定意上耶路撒冷，被捕、受审、上诉凯撒，经船难到罗马。罗马官员一再宣告他无罪；主的应许“也必怎样在罗马为我作见证”（{{徒23:11}}）一一成就。全书以“放胆传讲神国的道……并没有人禁止”（{{徒28:31}}）开放作结。")
W("doctrine.html", page("doctrine.html", "改革宗专题", "十二个主题：从使徒行传经文到三项联合信条（CCI 逐字）与威斯敏斯特标准", p_doc.build()))
W("creeds.html", page("creeds.html", "三大普世信经", "使徒信经 · 尼西亚信经 · 亚他那修信经：干净背诵版（可朗读）、深度对比、为何有三份；三项联合信条比较", p_creed.build()))
W("memory.html", page("memory.html", "记忆 · 自测", "口诀、数字、钥字、记忆卡、钥节填空、小考、记忆宫殿与 28 天计划", p_mem.build(CH)))
json.dump([[k, str(a), b] for k, a, b in QUOTES], open(os.path.join(ROOT, "build", "quotes.json"), "w"), ensure_ascii=False, indent=0)
stats_f = os.path.join(ROOT, "build", "verify_stats.json")
stats = json.load(open(stats_f)) if os.path.exists(stats_f) else [["状态", "尚未运行 verify.py"]]
W("sources.html", page("sources.html", "来源 · 校验", "引用来源、逐字校验结果、局限说明与版本记录", p_misc.sources(stats)))
open(os.path.join(D, ".nojekyll"), "w").write("")
print("quotes:", len(QUOTES))
