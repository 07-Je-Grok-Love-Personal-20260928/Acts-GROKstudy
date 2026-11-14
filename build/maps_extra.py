# -*- coding: utf-8 -*-
"""v3.1 新增专题地图：编号路线示意图 + 实景 Leaflet 配置。"""
import html as H
from geo import C, WP, JOURNEYS, P, W as GW, H as GH, ll, smooth
from maps_ui import (esc, mappair, concept_geo, path_schematic, pts_of, path_of,
                     bounds_of, CITY, _nm, _ll, _curve, _wave_pts)

def note(ps):
    return "<div class='maphist'>" + "".join(f"<p class='note'>{p}</p>" for p in ps) + "</div>"

# ---------- numbered path schematic (stops: name, kind, ref) ----------
def numbered_schematic(title, stops, color="#4fb3ff", kind="land"):
    n=len(stops); W=max(720, n*100); Ht=240
    pts=_wave_pts(n, W, Ht, y0=118, amp=40, pad=52)
    d=_curve(pts)
    uid=abs(hash(title+color+"n"))%100000
    nodes=""
    for i,((name,kd,ref),(x,y)) in enumerate(zip(stops,pts),1):
        ic={"port":"⚓","sea":"🌊","event":"✦","rome":"🏛","jer":"★","wind":"💨"}.get(kd,"")
        lab=f"{ic}{name}" if ic else name
        ty=y+(32 if i%2 else -22)
        ry=ty+14 if i%2 else ty-14
        nodes+=f'<g class="sn" data-at="{(i-1)/max(1,n-1):.2f}">'
        nodes+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="{color}" stroke="#fff" stroke-width="2"/>'
        nodes+=f'<text x="{x:.1f}" y="{y+4:.1f}" text-anchor="middle" font-size="11" font-weight="800" fill="#1a1300">{i}</text>'
        nodes+=f'<text x="{x:.1f}" y="{ty:.1f}" text-anchor="middle" font-size="13" fill="#e8ecf6">{esc(lab)}</text>'
        if ref:
            nodes+=f'<text x="{x:.1f}" y="{ry:.1f}" text-anchor="middle" font-size="11" fill="#ffd36b">{esc(ref)}</text>'
        nodes+='</g>'
    fill=f'url(#sg{uid})' if kind=="sea" else f'url(#lg{uid})'
    return f'''<svg class="cmo anim-svg" viewBox="0 0 {W} {Ht}" role="img" aria-label="{esc(title)}" preserveAspectRatio="xMidYMid meet">
<defs>
  <linearGradient id="lg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#152445"/><stop offset="1" stop-color="#1c3358"/></linearGradient>
  <linearGradient id="sg{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d3a5c"/><stop offset="1" stop-color="#12304c"/></linearGradient>
</defs>
<rect width="100%" height="100%" fill="{fill}"/>
<text x="16" y="26" fill="#ffd36b" font-size="15" font-weight="700">{esc(title)}</text>
<path class="sch-route draw" d="{d}" fill="none" stroke="{color}" stroke-width="3.4" stroke-linecap="round"/>
<circle class="anim-dot" r="7" fill="#ff6b8b" stroke="#fff" stroke-width="2"/>
{nodes}
</svg>'''

def jerusalem_plan():
    # Schematic city plan (not to scale). Temple courts + Antonia + gates.
    return '''<svg class="cmo anim-svg jplan" viewBox="0 0 720 520" role="img" aria-label="耶路撒冷圣城平面示意图">
  <rect width="720" height="520" fill="#1a2744"/>
  <text x="16" y="26" fill="#ffd36b" font-size="16" font-weight="700">耶路撒冷圣城平面（示意，非精确测绘图）</text>
  <!-- Kidron / Olives -->
  <rect x="600" y="60" width="110" height="430" rx="8" fill="#0d3a2a" opacity=".7"/>
  <text x="655" y="80" text-anchor="middle" fill="#86efac" font-size="12">汲沦溪 · 橄榄山</text>
  <text x="655" y="250" text-anchor="middle" fill="#86efac" font-size="12" transform="rotate(90 655 250)">客西马尼一带</text>
  <!-- Lower / Upper city blocks -->
  <rect x="40" y="300" width="250" height="180" rx="12" fill="#2a3348" stroke="#94a3b8" stroke-dasharray="5 5"/>
  <text x="165" y="330" text-anchor="middle" fill="#cbd5e1" font-size="13">上城（传统楼房方向）</text>
  <text x="165" y="350" text-anchor="middle" fill="#a5b0c8" font-size="11">徒1:13 所住的一间楼房</text>
  <rect x="40" y="80" width="160" height="120" rx="12" fill="#2a3348" stroke="#94a3b8" stroke-dasharray="5 5"/>
  <text x="120" y="130" text-anchor="middle" fill="#cbd5e1" font-size="13">贝塞大池一带</text>
  <text x="120" y="150" text-anchor="middle" fill="#a5b0c8" font-size="11">北墙外</text>
  <!-- Temple complex -->
  <g class="sn" data-at="0">
    <rect x="280" y="140" width="300" height="280" rx="8" fill="#3a2f16" stroke="#f5b942" stroke-width="2"/>
    <text x="430" y="162" text-anchor="middle" fill="#f5b942" font-size="13" font-weight="700">外邦人院</text>
    <!-- Women's / Israel / Priests -->
    <rect x="330" y="210" width="200" height="160" rx="6" fill="#5a4a20" stroke="#ffd36b"/>
    <text x="430" y="230" text-anchor="middle" fill="#ffd36b" font-size="12">妇女院 / 以色列院</text>
    <rect x="365" y="255" width="130" height="90" rx="4" fill="#7a6230" stroke="#fff4c2"/>
    <text x="430" y="280" text-anchor="middle" fill="#fff" font-size="12">圣所</text>
    <rect x="400" y="300" width="60" height="30" rx="3" fill="#f5b942"/>
    <text x="430" y="320" text-anchor="middle" fill="#1a1300" font-size="11" font-weight="700">至圣所</text>
  </g>
  <!-- Beautiful Gate (east, toward Kidron) -->
  <g class="sn" data-at=".25">
    <rect x="575" y="255" width="18" height="50" fill="#4fb3ff"/>
    <text x="610" y="250" fill="#4fb3ff" font-size="12" font-weight="700">美门</text>
    <text x="610" y="266" fill="#7dd3fc" font-size="11">徒3:2</text>
  </g>
  <!-- Solomon portico east inside -->
  <g class="sn" data-at=".35">
    <rect x="548" y="155" width="14" height="250" fill="#67e8f9" opacity=".8"/>
    <text x="520" y="430" text-anchor="middle" fill="#67e8f9" font-size="12">所罗门廊 · 徒3:11; 5:12</text>
  </g>
  <!-- Antonia north -->
  <g class="sn" data-at=".55">
    <rect x="300" y="70" width="220" height="70" rx="6" fill="#7f1d1d" stroke="#ff6b8b" stroke-width="2"/>
    <text x="410" y="100" text-anchor="middle" fill="#fecaca" font-size="14" font-weight="700">🏛 安东尼堡</text>
    <text x="410" y="118" text-anchor="middle" fill="#ffb4b4" font-size="11">驻军 · 徒21:34 保罗被带上台阶</text>
  </g>
  <!-- path arrest -->
  <path class="sch-route draw" d="M584,280 L540,280 L430,200 L410,140" fill="none" stroke="#ff6b8b" stroke-width="3"/>
  <circle class="anim-dot" r="6" fill="#ff6b8b" stroke="#fff" stroke-width="2"/>
  <text x="16" y="500" fill="#a5b0c8" font-size="11">位置为教学示意：圣殿北侧为安东尼堡，东侧为美门与所罗门廊，城东为橄榄山。</text>
</svg>'''

def shipwreck_schematic():
    return '''<svg class="cmo anim-svg" viewBox="0 0 860 300" role="img" aria-label="船难与风势示意图">
  <defs>
    <linearGradient id="seaSW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a3a5c"/><stop offset="1" stop-color="#0b2740"/></linearGradient>
  </defs>
  <rect width="860" height="300" fill="url(#seaSW)"/>
  <text x="16" y="26" fill="#ffd36b" font-size="15" font-weight="700">徒27：优罗革罗（东北暴风）与米利大船难</text>
  <!-- Crete block -->
  <ellipse cx="340" cy="90" rx="130" ry="36" fill="#3a4a3a" stroke="#a8c49a"/>
  <text x="340" y="86" text-anchor="middle" fill="#e8ecf6" font-size="13" font-weight="700">革哩底</text>
  <text x="260" y="108" text-anchor="middle" fill="#ffd36b" font-size="11">佳澳 徒27:8</text>
  <text x="420" y="108" text-anchor="middle" fill="#94a3b8" font-size="11">非尼基（拟开往）</text>
  <ellipse cx="300" cy="150" rx="28" ry="12" fill="#4a5a4a"/>
  <text x="300" y="172" text-anchor="middle" fill="#a8c49a" font-size="11">高大岛</text>
  <!-- Malta -->
  <ellipse cx="760" cy="210" rx="40" ry="18" fill="#3a4a3a" stroke="#a8c49a"/>
  <text x="760" y="214" text-anchor="middle" fill="#e8ecf6" font-size="12">米利大</text>
  <!-- Syrtis warning -->
  <text x="560" y="270" fill="#fb7185" font-size="12">⚠️ 怕搁浅赛耳底沙滩（徒27:17）</text>
  <!-- wind arrows -->
  <g class="sn" data-at=".2" fill="none" stroke="#7dd3fc" stroke-width="2">
    <path d="M500,40 l40,28"/><path d="M530,48 l40,28"/><path d="M560,56 l40,28"/>
    <text x="620" y="50" fill="#7dd3fc" font-size="13" font-weight="700">💨 优罗革罗（东北暴风）</text>
  </g>
  <path class="sch-route draw" d="M80,70 C180,80 240,100 290,110 C330,140 360,180 430,200 C520,220 640,230 760,210" fill="none" stroke="#67e8f9" stroke-width="3.4"/>
  <circle class="anim-dot" r="7" fill="#ff6b8b" stroke="#fff" stroke-width="2"/>
  <g font-size="11" fill="#ffd36b">
    <text x="70" y="58">① 凯撒利亚出发</text>
    <text x="200" y="60">② 每拉换粮船</text>
    <text x="430" y="188">③ 十四昼夜漂流</text>
    <text x="700" y="188">④ 船搁浅，276 人得救</text>
  </g>
</svg>'''

def asia7_schematic():
    # circuit around Ephesus, numbered
    stops=[("以弗所","city","徒19 · 启2:1"),("士每拿","city","启2:8"),("别迦摩","city","启2:12"),
           ("推雅推喇","city","启2:18"),("撒狄","city","启3:1"),("非拉铁非","city","启3:7"),("老底嘉","city","启3:14")]
    return numbered_schematic("亚细亚七教会：以弗所三年，全亚细亚听见这道（徒19:10）", stops, "#3fd39a")

def pentecost_schematic():
    # Geographic-ish fan from Jerusalem (reuse style of diaspora but with data-at for anim)
    nations=[
      ("帕提亚",480,80,"徒2:9"),("玛代",540,120,""),("以拦",560,170,""),("美索不达米亚",500,200,""),
      ("犹太",360,260,"中心"),("加帕多家",430,70,""),("本都",400,40,""),("亚细亚",300,70,""),
      ("弗吕家",320,110,""),("旁非利亚",300,150,""),("埃及",280,320,""),("古利奈",200,300,""),
      ("罗马",80,120,"徒2:10"),("克里特",180,200,""),("阿拉伯",420,340,"徒2:11")
    ]
    cx,cy=360,240
    s=['<svg class="cmo anim-svg" viewBox="0 0 640 440" role="img" aria-label="五旬节万邦示意图">']
    s.append('<rect width="640" height="440" fill="#152445"/><text x="16" y="28" fill="#ffd36b" font-size="15" font-weight="700">五旬节听众：从耶路撒冷听见自己的乡谈（徒2:9-11）</text>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="28" fill="#f5b942"/><text x="{cx}" y="{cy+5}" text-anchor="middle" fill="#1a1300" font-size="12" font-weight="700">耶路撒冷</text>')
    n=len(nations)
    for i,(name,x,y,ref) in enumerate(nations):
        at=i/max(1,n-1)
        s.append(f'<g class="sn" data-at="{at:.2f}">')
        s.append(f'<line class="draw-ray" x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#f5b942" stroke-opacity=".7" stroke-width="1.6"/>')
        s.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#4fb3ff"/>')
        s.append(f'<text x="{x}" y="{y-10}" text-anchor="middle" fill="#e8ecf6" font-size="12">{name}</text>')
        if ref:
            s.append(f'<text x="{x}" y="{y+16}" text-anchor="middle" fill="#ffd36b" font-size="10">{ref}</text>')
        s.append('</g>')
    s.append('<circle class="anim-dot" r="6" fill="#ff6b8b" stroke="#fff" stroke-width="2"/>')
    s.append('</svg>')
    return "".join(s)

# Journey numbered stop lists (name, kind, ref)
J1_STOPS=[
 ("安提阿","city","徒13:1-3"),("西流基","port","13:4"),("撒拉米","city","13:5"),("帕弗","port","13:6-12"),
 ("别加","city","13:13"),("彼西底安提阿","city","13:14-52"),("以哥念","city","14:1-6"),("路司得","city","14:8-20"),
 ("特庇","city","14:20-21"),("原路返回","city","14:21-23"),("亚大利","port","14:25"),("安提阿","city","14:26-28"),
]
J2_STOPS=[
 ("安提阿","city","15:36-41"),("特庇·路司得","city","16:1-5"),("特罗亚","port","16:8-10"),("腓立比","city","16:11-40"),
 ("帖撒罗尼迦","city","17:1-9"),("庇哩亚","city","17:10-15"),("雅典","city","17:16-34"),("哥林多","city","18:1-17"),
 ("以弗所","city","18:19-21"),("凯撒利亚","port","18:22"),("安提阿","city","18:22"),
]
J3_STOPS=[
 ("安提阿","city","18:23"),("加拉太·弗吕家","city","18:23"),("以弗所","city","19:1-41"),("马其顿·希腊","city","20:1-3"),
 ("特罗亚","port","20:6-12"),("米利都","port","20:17-38"),("推罗","port","21:3-6"),("凯撒利亚","port","21:8-14"),
 ("耶路撒冷","jer","21:17"),
]

def _hist(ps):
    return "".join(f"<p>{p}</p>" for p in ps)

# keys used in live maps
PHILIP_KS=["samaria","jerusalem","gaza","azotus","caesarea"]
SAUL_KS=["jerusalem","damascus","arabia","damascus","jerusalem","caesarea","tarsus"]
PETER_KS=["jerusalem","lydda","joppa","caesarea","jerusalem"]
SCATTER_KS=["jerusalem","tyre","sidon","salamis","antioch"]
TRIAL_KS=["jerusalem","caesarea"]
SHIP_KS=["caesarea","sidon","myra","cnidus","fairhavens","cauda","sea3","malta"]
EGN_KS=["dyrrhachium","neapolis","philippi","amphipolis","apollonia_mac","thessalonica","berea"]
ASIA_KS=["ephesus","smyrna","pergamum","thyatira","sardis","philadelphia","laodicea","colossae"]
APPIA_KS=["puteoli","appforum","threetaverns","rome"]

def extra_cfgs():
    """Return {mid: leaflet cfg}."""
    cfgs={}
    def add(mid,**kw): cfgs[mid]=kw
    add("pentecost", color="#f5b942", maxZoom=5, bounds=[[24,8],[45,54]],
        points=[{"n":n,"ll":[lat,lon],"c":"#4fb3ff" if n!="犹太" else "#f5b942","d":"五旬节听众（徒2:9-11）","r":8 if n in ("犹太","罗马") else 6}
                for n,lat,lon in [
      ("帕提亚",35.7,51.4),("玛代",35.0,48.0),("以拦",32.0,48.5),("美索不达米亚",33.4,44.4),
      ("犹太",31.78,35.23),("加帕多家",38.7,35.5),("本都",41.3,36.3),("亚细亚",37.94,27.34),
      ("弗吕家",38.5,30.0),("旁非利亚",36.9,30.7),("埃及",31.2,29.9),("古利奈",32.1,21.6),
      ("罗马",41.89,12.48),("克里特",35.2,24.95),("阿拉伯",29.0,36.0)]],
        routes=[])
    add("philip", color="#3fd39a", maxZoom=9, bounds=bounds_of(PHILIP_KS,.5),
        points=pts_of(PHILIP_KS,"#3fd39a"),
        routes=[{"n":"腓利：撒马利亚 → 迦萨路 → 亚锁都 → 凯撒利亚（徒8）","c":"#3fd39a","path":path_of(PHILIP_KS)}])
    add("saul", color="#f5b942", maxZoom=8, bounds=bounds_of(["jerusalem","damascus","arabia","tarsus","caesarea"],.7),
        points=pts_of(["jerusalem","damascus","arabia","tarsus","caesarea"],"#f5b942"),
        routes=[{"n":"扫罗：耶路撒冷 → 大马士革 → 阿拉伯（加1:17）→ 大数（徒9）","c":"#f5b942","path":path_of(SAUL_KS)}])
    add("peter", color="#4fb3ff", maxZoom=10, bounds=bounds_of(PETER_KS,.4),
        points=pts_of(["jerusalem","lydda","joppa","caesarea"],"#4fb3ff"),
        routes=[{"n":"彼得：吕大 → 约帕 → 凯撒利亚（徒9:32–10）","c":"#4fb3ff","path":path_of(PETER_KS)}])
    add("scatter", color="#fb7185", maxZoom=8, bounds=bounds_of(SCATTER_KS,.8),
        points=pts_of(SCATTER_KS,"#fb7185"),
        routes=[{"n":"分散：腓尼基、居比路、安提阿（徒11:19）","c":"#fb7185","path":path_of(SCATTER_KS)}])
    add("trials", color="#ff6b8b", maxZoom=9, bounds=bounds_of(TRIAL_KS,.6),
        points=pts_of(TRIAL_KS,"#ff6b8b")+[{"n":"安东尼堡（示意）","ll":[31.7805,35.2368],"d":"徒21:34 保罗被带上营楼","c":"#ffd36b","r":8}],
        routes=[{"n":"夜送凯撒利亚（徒23:23-33）","c":"#ff6b8b","path":path_of(["jerusalem","caesarea"])}])
    add("shipwreck", color="#67e8f9", maxZoom=7, bounds=[[31.5,10],[42,36]],
        points=pts_of(["caesarea","sidon","myra","crete","malta"],"#67e8f9")+
               [{"n":"佳澳","ll":[34.93,24.80],"d":"徒27:8 不宜过冬","c":"#ffd36b"},
                {"n":"高大岛","ll":[34.85,23.96],"d":"徒27:16 小船难拉上","c":"#94a3b8"}],
        routes=[{"n":"粮船航线与漂流（徒27）","c":"#67e8f9","path":path_of(SHIP_KS),"dash":"8 8"}])
    add("egnatia", color="#5aa9ff", maxZoom=8, bounds=bounds_of(EGN_KS,1.0),
        points=pts_of(["dyrrhachium","neapolis","philippi","thessalonica","berea"],"#5aa9ff"),
        routes=[{"n":"厄纳齐亚大道（Via Egnatia）","c":"#5aa9ff","path":path_of(EGN_KS)}])
    add("asia7", color="#3fd39a", maxZoom=9, bounds=bounds_of(ASIA_KS,.6),
        points=pts_of(ASIA_KS,"#3fd39a"),
        routes=[{"n":"七教会环线（以弗所为中心，徒19:10）","c":"#3fd39a","path":path_of(["ephesus","smyrna","pergamum","thyatira","sardis","philadelphia","laodicea","ephesus"])}])
    add("jercity", color="#f5b942", maxZoom=18, minZoom=14, bounds=[[31.772,35.226],[31.785,35.246]],
        points=[
          {"n":"圣殿山","ll":[31.7780,35.2354],"d":"外邦人院、妇女院、圣所：教会初期每日在此（徒2:46；3:1）。位置示意。","c":"#f5b942","r":9},
          {"n":"安东尼堡（示意）","ll":[31.7806,35.2369],"d":"圣殿北侧营楼。徒21:34 保罗被带上台阶，对百姓讲话。","c":"#ff6b8b","r":8},
          {"n":"美门（示意）","ll":[31.7778,35.2374],"d":"徒3:2 生来瘸腿的人在此乞讨。","c":"#4fb3ff","r":7},
          {"n":"所罗门廊（示意）","ll":[31.7776,35.2368],"d":"徒3:11；5:12 使徒聚集讲道。","c":"#67e8f9","r":7},
          {"n":"传统楼房方向","ll":[31.7715,35.2305],"d":"徒1:13 所住的一间楼房（传统地点，仅供参照）。","c":"#c08457","r":6},
        ],
        routes=[])
    add("appia", color="#c08457", maxZoom=10, bounds=bounds_of(APPIA_KS,.4),
        points=pts_of(APPIA_KS,"#c08457"),
        routes=[{"n":"部丢利 → 亚比乌市 → 三馆 → 罗马（徒28:13-16）","c":"#c08457","path":path_of(APPIA_KS)}])
    # enhanced numbered journeys reuse same mid j1/j2/j3 (cfg already in all_cfgs)
    return cfgs

THEME = {
 "pentecost":("五旬节的万邦（徒2:9-11）", pentecost_schematic, [
    "名单从东（帕提亚、玛代、以拦——被掳之地）到西（罗马），是一幅「离散犹太人」的世界图。",
    "后期犹太传统把五旬节与西奈颁律法相连；路加则写成「万民听见同一福音」——巴别的反转。",
    "「古利奈」后来出现在安提阿的传道人中（徒11:20；13:1），罗马则有亚居拉、百基拉（徒18:2）。",
 ], True),
 "philip":("腓利：撒马利亚、迦萨路与埃提阿伯太监（徒8）", lambda: numbered_schematic("腓利的路线（徒8）",[
    ("撒马利亚","city","8:5-25"),("迦萨路","event","8:26"),("太监受洗","event","8:36-39"),("亚锁都","city","8:40"),("凯撒利亚","port","8:40")
 ],"#3fd39a"), [
    "撒马利亚人与犹太人有七百年裂痕（只认摩西五经、敬拜在基利心山）。腓利过了这道墙，彼得、约翰随后按手。",
    "「从耶路撒冷下迦萨的路」是南下沿海驿道；太监是埃提阿伯女王干大基的总管，读的是七十士译本以赛亚书。",
    "腓利后来定居凯撒利亚（徒21:8），家中有四个说预言的女儿——福音在行政首府扎根。",
 ], True),
 "saul":("扫罗：大马士革路、阿拉伯与大数（徒9；加1）", lambda: numbered_schematic("扫罗归信之路",[
    ("耶路撒冷","jer","9:1-2"),("大马士革路","event","9:3-9"),("大马士革","city","9:10-25"),
    ("阿拉伯","city","加1:17"),("再回圣城","jer","9:26-29"),("大数","city","9:30")
 ],"#f5b942"), [
    "大马士革是十城联盟中的大城，有会堂网络；「直街」至今仍可对照古城轴线。",
    "加拉太书 1:17 说他曾往阿拉伯（纳巴泰一带）再回大马士革——路加从略，保罗强调福音不是人传授的。",
    "巴拿巴带他见使徒后，因性命危险被送到大数；数年后再被巴拿巴接到安提阿（徒11:25）。",
 ], True),
 "peter":("彼得：吕大、约帕、凯撒利亚（徒9:32–10）", lambda: numbered_schematic("彼得沿海之行",[
    ("耶路撒冷","jer","9:32"),("吕大","city","9:32-35"),("约帕","port","9:36-43"),("凯撒利亚","port","10:1-48"),("回报圣城","jer","11:1-18")
 ],"#4fb3ff"), [
    "吕大（罗 Lod）、约帕（雅法）是沿海平原的犹太市镇；约帕是约拿上船逃往他施之地——如今彼得从这里走向外邦。",
    "凯撒利亚是罗马巡抚驻地、深水港与驻军城，由希律所建，向凯撒致敬。哥尼流是意大利营的百夫长。",
    "异象中的布与不洁之物，不是在讨论食谱，而是拆掉「圣俗隔离」的墙，为外邦人入约开门。",
 ], True),
 "scatter":("分散到安提阿（徒11:19-26）", lambda: numbered_schematic("因司提反而分散的人",[
    ("耶路撒冷","jer","8:1; 11:19"),("腓尼基","port","11:19"),("居比路","city","11:19"),("安提阿","city","11:20-26")
 ],"#fb7185"), [
    "逼迫使门徒散开，福音却沿腓尼基海岸（推罗、西顿）、海路到塞浦路斯，并北上帝国第三大城安提阿。",
    "只对犹太人讲论的人，与「塞浦路斯和古利奈人向希腊人传主耶稣」的人，在安提阿分成两条线——后者成为外邦宣教的起点。",
    "「基督徒」这名首先在安提阿出现（徒11:26）。巴拿巴从耶路撒冷来，又去大数找扫罗，两人在此教导一年。",
 ], True),
 "trials":("被捕与受审：耶路撒冷到凯撒利亚（徒21–26）", lambda: numbered_schematic("五次辩护的地理",[
    ("圣殿暴动","jer","21:27-36"),("安东尼堡","event","21:37–22"),("公会","event","23:1-10"),
    ("夜送海岸","event","23:23-33"),("腓力斯","city","24"),("非斯都·亚基帕","city","25–26")
 ],"#ff6b8b"), [
    "安东尼堡紧贴圣殿北侧，有台阶通向下院，正合徒21:34-40「站在台阶上」对百姓讲话的场景。",
    "七十名骑兵、二百步兵连夜送往凯撒利亚，说明罗马要防止保罗在路上被杀，也说明巡抚府不在耶路撒冷。",
    "腓力斯、非斯都、亚基帕二世三次听审，路加反复记下「没有该死的罪」——为罗马读者，也为福音的公开性。",
 ], True),
 "shipwreck":("航海与船难：佳澳、暴风、米利大（徒27–28）", shipwreck_schematic, [
    "秋季地中海「禁航期」将至（徒27:9 的禁食节多指赎罪日）。佳澳（Fair Havens）避风不佳，船上多数人想去西边的非尼基过冬。",
    "「优罗革罗」是东北暴风。他们在高大岛（Cauda）南面放下小船、用缆绳捆船，又怕被吹到北非赛耳底沙滩。",
    "连续十四昼夜不见日月；第十四夜水手测深，从二十丈到十五丈。船在两水夹流处搁浅，276 人全部上岸。米利大（马耳他）土人「有情分」，部百流是「岛长」。",
 ], True),
 "egnatia":("罗马大道：厄纳齐亚与福音入欧洲", lambda: numbered_schematic("厄纳齐亚大道（Via Egnatia）",[
    ("都拉基乌","port","西端·亚得里亚"),("尼亚波利","port","徒16:11"),("腓立比","city","16:12"),
    ("暗妃波里","city","17:1"),("帖撒罗尼迦","city","17:1"),("庇哩亚","city","17:10 偏南")
 ],"#5aa9ff"), [
    "厄纳齐亚大道横贯马其顿，西起亚得里亚海的都拉基乌，东到拜占庭，是罗马军政主干道。",
    "保罗从特罗亚海路到尼亚波利，立刻走上这条大道：腓立比（罗马殖民地）→ 暗妃波里 → 帖撒罗尼迦（省会、有会堂）。",
    "庇哩亚不在主干道正线上，弟兄夜间送保罗走这条「偏路」，避开帖撒罗尼迦的追逼——地理本身在讲述护理。",
 ], True),
 "asia7":("亚细亚七教会与以弗所三年（徒19；启示录2–3）", asia7_schematic, [
    "保罗在以弗所推喇奴学房辩论两年，「叫一切住在亚细亚的……都听见这道」（徒19:10）。启示录的七教会正在这同一行省的环形驿道上。",
    "以弗所是省会与亚底米大庙所在；士每拿、别迦摩、推雅推喇、撒狄、非拉铁非、老底嘉沿官道顺时针分布，老底嘉邻近歌罗西。",
    "亚底米神庙与银匠行会构成城市经济；「这道」一兴旺，偶像生意就受冲击（徒19:23-27）。启示录对以弗所说「把起初的爱心离弃了」，是同一座教会稍后的诊断。",
 ], True),
 "jercity":("耶路撒冷圣城：圣殿、美门、安东尼堡", jerusalem_plan, [
    "圣殿由外邦人院、妇女院、以色列院、祭司院层层向内。残疾者不能进内院事奉，所以生来瘸腿的人被放在「美门」乞讨（徒3:2）。",
    "所罗门廊在圣殿东侧，是公众讲论之处（约10:23；徒3:11；5:12）。使徒没有离开圣殿敬拜，直到司提反的讲章把「圣殿」重新指向基督。",
    "安东尼堡在圣殿北侧，由希律所建、驻罗马军。暴动时千夫长「带着兵丁跑下去」，又把保罗「带上营楼台阶」——平面图与叙事咬合。",
 ], False),
 "appia":("亚比亚大道：部丢利、亚比乌市、三馆、罗马（徒28）", lambda: numbered_schematic("上罗马的最后一段",[
    ("部丢利","port","28:13-14"),("亚比乌市","city","28:15"),("三馆","city","28:15"),("罗马","rome","28:16")
 ],"#c08457"), [
    "部丢利（Puteoli）是意大利的深水港，亚历山大粮船常在此卸货。保罗遇着弟兄，住了七天。",
    "亚比乌市（Forum Appii）与三馆（Tres Tabernae）是亚比亚大道（Via Appia）上的驿站。罗马的弟兄远道来迎，保罗「感谢神，放心壮胆」。",
    "他以囚犯身份进首都，却能「自己租的房子」接待来访，放胆传神国的道——地极不是地图的终点，是见证的新起点。",
 ], True),
}

# numbered replacements for existing journey mids
JOURNEY_SCH={
 "j1": lambda: numbered_schematic("第一次宣教旅行（徒13–14）", J1_STOPS, "#f5b942"),
 "j2": lambda: numbered_schematic("第二次宣教旅行（徒15:36–18:22）", J2_STOPS, "#4fb3ff"),
 "j3": lambda: numbered_schematic("第三次宣教旅行（徒18:23–21:17）", J3_STOPS, "#3fd39a"),
}

JOURNEY_THEME_NOTES={
 "j1":["第一次旅行（约 46–48）：塞浦路斯到南加拉太，站次与经文编号见图。","方伯士求保罗信主，是路加第一次记下罗马官员归信。路司得的丢斯—希耳米呼声，显出本地神庙仍活着。"],
 "j2":["第二次旅行（约 49–52）：福音首次进入欧洲，沿厄纳齐亚大道到腓立比、帖撒罗尼迦，再到雅典、哥林多。","迦流任亚该亚方伯（约 51–52，德尔斐铭文）是全书最硬的外证年锚。"],
 "j3":["第三次旅行（约 52–57）：以弗所约两年零三个月，「叫一切住在亚细亚的……都听见这道」（徒19:10）。","米利都对长老的嘱咐，是改革宗教会论的关键经文（徒20:28）。"],
 "j4":["被押往罗马（约 59–60）：粮船、佳澳、优罗革罗、米利大、部丢利。","亚比乌市与三馆在亚比亚大道上，罗马弟兄到此迎接。"],
}

def thematic_pair(mid):
    if mid in THEME:
        title, sch, notes, play = THEME[mid]
        svg = sch() if callable(sch) else sch
        hist=_hist(notes)
        cap="概念示意图（离线可用）。可用下方按钮播放、暂停或拖动进度；路线按故事顺序画出。"
        return mappair(mid, title, svg, hist, play=play, caption=cap)
    if mid in JOURNEY_SCH:
        from geo import JOURNEYS
        name=next(n for j,n,c,k in JOURNEYS if j==mid)
        svg=JOURNEY_SCH[mid]()
        return mappair(mid, name, svg, _hist(JOURNEY_THEME_NOTES[mid]), play=True,
                       caption="编号站点示意图（离线可用）。可播放、暂停或拖动进度。")
    raise KeyError("unknown map id: "+mid)
