# -*- coding: utf-8 -*-
"""可播放、暂停、拖动的动画块（仅 transform / opacity / stroke-dashoffset）。"""
from common import md, esc

CTRL = '''<div class="anim-ctrl" data-anim="{aid}"><button type="button" class="btn sm anim-play" aria-label="播放或暂停">▶ 播放</button>
<input type="range" class="anim-scrub" min="0" max="100" value="0" aria-label="动画进度"><span class="anim-pct">0%</span></div>'''

def _box(aid, title, hid, svg, cap):
    return f'''<section class="animbox glass" id="{hid}" data-anim="{aid}">
<h3 id="{hid}-t">{esc(title)}</h3>
<figure class="animfig">{svg}{CTRL.format(aid=aid)}<figcaption>{esc(cap)}</figcaption></figure>
</section>'''

def growth_chart():
    # Acts progress reports
    rows=[
        (0.05,"徒2:41","三千人","五旬节受洗"),
        (0.18,"徒4:4","男人约五千","美门之后"),
        (0.32,"徒6:7","道兴旺 · 祭司多归信","第一次进展报告"),
        (0.46,"徒9:31","教会建立，人数增加","扫罗归信之后"),
        (0.58,"徒12:24","神的道日见兴旺、越发广传","希律死后"),
        (0.70,"徒16:5","信心越发坚固，人数天天加增","第二次旅行"),
        (0.84,"徒19:20","主的道大大兴旺，而且得胜","以弗所"),
        (1.00,"徒28:31","放胆传讲，没有人禁止","罗马，开放的结尾"),
    ]
    bars=""
    for i,(at,ref,lab,note) in enumerate(rows):
        y=48+i*36
        w=80+at*520
        bars+=f'''<g class="sn grow" data-at="{at:.2f}">
          <rect class="gbar" x="180" y="{y}" width="{w}" height="22" rx="6" fill="#f5b942" style="transform-origin:180px {y+11}px"/>
          <text x="172" y="{y+16}" text-anchor="end" fill="#ffd36b" font-size="12">{esc(ref)}</text>
          <text x="{180+w+8}" y="{y+16}" fill="#e8ecf6" font-size="13" font-weight="700">{esc(lab)}</text>
          <text x="180" y="{y-2}" fill="#a5b0c8" font-size="10">{esc(note)}</text>
        </g>'''
    svg=f'''<svg class="cmo anim-svg growth" viewBox="0 0 860 360" role="img" aria-label="福音扩展进展图">
      <rect width="860" height="360" fill="#152445"/>
      <text x="16" y="26" fill="#ffd36b" font-size="16" font-weight="700">福音怎样「长大」：八次进展报告</text>
      {bars}
    </svg>'''
    return _box("growth","福音扩展：八次进展报告","an-growth",svg,
                "路加用重复的进展句，而不是统计年报，来显明道自己在生长。播放时柱体按时间依次升起。")

def pentecost_spread():
    # simple rings + nations fade; can also be the map schematic but this is dedicated
    from maps_extra import pentecost_schematic
    return _box("pentecost","五旬节：乡谈传开的动画","an-pentecost", pentecost_schematic(),
                "火舌落下之后，十五个地名按徒2:9-11的顺序亮起。这是一次性的救赎历史事件，不是每个信徒必须重复的模式。")

def council_flow():
    nodes=[
        (0.00,80,50,"问题","有人从犹太下来：「必须受割礼才能得救」（15:1）","#ff6b8b"),
        (0.15,300,50,"安提阿辩论","保罗、巴拿巴与他们大大地纷争辩论（15:2）","#f5b942"),
        (0.30,520,50,"上耶路撒冷","教会派他们去见使徒和长老（15:2-3）","#4fb3ff"),
        (0.45,80,180,"彼得见证","神赐外邦人圣灵，如同赐给我们（15:7-11）","#3fd39a"),
        (0.60,300,180,"巴拿巴·保罗","述说神在外邦人中所行的神迹（15:12）","#67e8f9"),
        (0.75,520,180,"雅各裁决","引阿摩司 9：重建大卫的帐幕（15:13-21）","#b794ff"),
        (0.90,300,310,"公函发出","不把难担的轭放在外邦门徒颈上（15:22-29）","#f5b942"),
    ]
    boxes=""
    for at,x,y,t,d,c in nodes:
        boxes+=f'''<g class="sn" data-at="{at:.2f}">
          <rect x="{x}" y="{y}" width="200" height="70" rx="12" fill="{c}" fill-opacity=".18" stroke="{c}" stroke-width="2"/>
          <text x="{x+100}" y="{y+24}" text-anchor="middle" fill="{c}" font-size="14" font-weight="700">{esc(t)}</text>
          <text x="{x+100}" y="{y+48}" text-anchor="middle" fill="#e8ecf6" font-size="11">{esc(d[:28])}</text>
        </g>'''
    # arrows as paths
    arrows='''
    <path class="draw" d="M280,85 L300,85" stroke="#94a3b8" stroke-width="2" fill="none"/>
    <path class="draw" d="M500,85 L520,85" stroke="#94a3b8" stroke-width="2" fill="none"/>
    <path class="draw" d="M620,120 L180,180" stroke="#94a3b8" stroke-width="2" fill="none"/>
    <path class="draw" d="M280,215 L300,215" stroke="#94a3b8" stroke-width="2" fill="none"/>
    <path class="draw" d="M500,215 L520,215" stroke="#94a3b8" stroke-width="2" fill="none"/>
    <path class="draw" d="M620,250 L400,310" stroke="#94a3b8" stroke-width="2" fill="none"/>
    '''
    svg=f'''<svg class="cmo anim-svg" viewBox="0 0 760 400" role="img" aria-label="耶路撒冷会议流程图">
      <rect width="760" height="400" fill="#152445"/>
      <text x="16" y="28" fill="#ffd36b" font-size="16" font-weight="700">耶路撒冷会议：问题 → 见证 → 圣经 → 公函</text>
      {arrows}{boxes}
    </svg>'''
    return _box("council","耶路撒冷会议：决策流程","an-council",svg,
                "次序要记牢：先是福音事实（神已经把圣灵赐给外邦人），再是经文裁决（阿摩司 9），最后是牧养性的公函。不是多数表决另立新律。")

def trials_flow():
    nodes=[
        (0.00,40,70,"圣殿暴动","徒21:27-36","#ff6b8b"),
        (0.14,220,70,"台阶上自辩","徒22","#f5b942"),
        (0.28,400,70,"公会分裂","徒23:1-10","#4fb3ff"),
        (0.42,580,70,"夜送凯撒利亚","徒23:23-33","#3fd39a"),
        (0.56,40,200,"腓力斯前","徒24","#67e8f9"),
        (0.70,220,200,"非斯都 · 上诉","徒25:1-12","#b794ff"),
        (0.84,400,200,"亚基帕前","徒26","#fb7185"),
        (1.00,580,200,"无罪却往罗马","徒26:32；27–28","#f5b942"),
    ]
    boxes=""
    for at,x,y,t,d,c in nodes:
        boxes+=f'''<g class="sn" data-at="{at:.2f}">
          <rect x="{x}" y="{y}" width="160" height="64" rx="12" fill="{c}" fill-opacity=".2" stroke="{c}" stroke-width="2"/>
          <text x="{x+80}" y="{y+26}" text-anchor="middle" fill="#e8ecf6" font-size="13" font-weight="700">{esc(t)}</text>
          <text x="{x+80}" y="{y+46}" text-anchor="middle" fill="{c}" font-size="11">{esc(d)}</text>
        </g>'''
    svg=f'''<svg class="cmo anim-svg" viewBox="0 0 800 300" role="img" aria-label="五次辩护流程">
      <rect width="800" height="300" fill="#152445"/>
      <text x="16" y="28" fill="#ffd36b" font-size="16" font-weight="700">从暴动到上诉凯撒：五次辩护</text>
      <path class="draw" d="M200,102 L220,102 M380,102 L400,102 M560,102 L580,102 M120,134 L120,200 M200,232 L220,232 M380,232 L400,232 M560,232 L580,232" stroke="#94a3b8" stroke-width="2" fill="none"/>
      {boxes}
    </svg>'''
    return _box("trials","受审序列：五次辩护","an-trials",svg,
                "路加要读者看见：暴民、公会、巡抚、君王都不能找出死罪。上诉凯撒不是投机，是主在徒23:11的应许正在兑现。")

def storm_seq():
    stages=[
        (0.00,"启航","凯撒利亚 → 西顿 → 每拉，换上亚历山大粮船","#67e8f9"),
        (0.18,"逆风","沿岸难行，到革哩底佳澳；保罗劝告勿再开船","#4fb3ff"),
        (0.36,"暴风","优罗革罗从东北刮起；捆船、丢下货物","#ff6b8b"),
        (0.54,"黑暗","十四昼夜不见日月；神的使者应许全船必生","#b794ff"),
        (0.72,"测深","二十丈、十五丈；抛锚等天亮；砍断小船","#f5b942"),
        (0.90,"搁浅","两水夹流，船尾被浪撞碎；276 人上岸","#3fd39a"),
    ]
    g=""
    for i,(at,t,d,c) in enumerate(stages):
        x=30+i*140
        g+=f'''<g class="sn" data-at="{at:.2f}">
          <circle cx="{x+50}" cy="120" r="28" fill="{c}" fill-opacity=".25" stroke="{c}" stroke-width="3"/>
          <text x="{x+50}" y="125" text-anchor="middle" fill="{c}" font-size="13" font-weight="700">{i+1}</text>
          <text x="{x+50}" y="170" text-anchor="middle" fill="#e8ecf6" font-size="13" font-weight="700">{esc(t)}</text>
          <text x="{x+50}" y="190" text-anchor="middle" fill="#a5b0c8" font-size="11">{esc(d[:18])}</text>
          <text x="{x+50}" y="206" text-anchor="middle" fill="#a5b0c8" font-size="11">{esc(d[18:36])}</text>
        </g>'''
    # waves drawn
    waves='<path class="draw" d="M20,70 C80,50 140,90 200,70 S320,50 400,70 S560,90 640,70 S760,50 840,70" fill="none" stroke="#7dd3fc" stroke-width="2"/>'
    svg=f'''<svg class="cmo anim-svg" viewBox="0 0 880 280" role="img" aria-label="船难风暴序列">
      <rect width="880" height="280" fill="#0b2740"/>
      <text x="16" y="28" fill="#ffd36b" font-size="16" font-weight="700">船难六幕：从逆风到全船得救（徒27）</text>
      {waves}{g}
    </svg>'''
    return _box("storm","船难风暴序列","an-storm",svg,
                "路加以航海细节写下护理：暴风、测深、抛锚、砍缆，每一步都没有取消「你必站在凯撒面前」的应许。")

def timeline_play(items):
    """items: (year, label, detail) — a scrubbable playhead along a track."""
    n=len(items)
    w=max(720, n*70)
    dots=""
    for i,(y,lab,det) in enumerate(items):
        x=40+i*((w-80)/max(1,n-1))
        at=i/max(1,n-1)
        dots+=f'''<g class="sn" data-at="{at:.2f}">
          <circle cx="{x:.1f}" cy="90" r="7" fill="#f5b942" stroke="#fff" stroke-width="2"/>
          <text x="{x:.1f}" y="70" text-anchor="middle" fill="#ffd36b" font-size="11">{y}</text>
          <text x="{x:.1f}" y="118" text-anchor="middle" fill="#e8ecf6" font-size="11">{esc(lab)}</text>
        </g>'''
    svg=f'''<svg class="cmo anim-svg tlplay" viewBox="0 0 {w} 160" role="img" aria-label="时间线回放">
      <rect width="{w}" height="160" fill="#152445"/>
      <text x="16" y="24" fill="#ffd36b" font-size="15" font-weight="700">时间线回放（主后 30–62，选点）</text>
      <path class="draw sch-route" d="M40,90 L{w-40},90" fill="none" stroke="#4fb3ff" stroke-width="3"/>
      <circle class="anim-dot" r="9" fill="#ff6b8b" stroke="#fff" stroke-width="2"/>
      {dots}
    </svg>'''
    return _box("tlplay","时间线回放","an-tlplay",svg,
                "播放时沿时间轴向右移动。详细条目与罗马官员对照见本页下方列表。")

REGISTRY={
    "growth": growth_chart,
    "pentecost": pentecost_spread,
    "council": council_flow,
    "trials": trials_flow,
    "storm": storm_seq,
}

def render_anim(aid, **kw):
    if aid=="tlplay":
        return timeline_play(kw["items"])
    return REGISTRY[aid]()
