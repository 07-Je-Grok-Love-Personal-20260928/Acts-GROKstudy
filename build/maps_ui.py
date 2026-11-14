# -*- coding: utf-8 -*-
"""地图对：离线概念示意图（SVG）+ 可切换多源的在线 Leaflet 实景图。"""
import json, math, html as H
from geo import C, WP, JOURNEYS, EARLY, P, W as GW, H as GH, ll, smooth, actsmap, chmap

def esc(s): return H.escape(s, quote=True)

CITY = {
 "jerusalem":"教会诞生、使徒会议、保罗被捕（徒1–7、15、21–23）",
 "samaria":"腓利传道，西门（徒8）","gaza":"往迦萨的路上，埃提阿伯太监（徒8）",
 "joppa":"大比大复活；彼得的异象（徒9–10）","lydda":"以尼雅得医治（徒9）",
 "caesarea":"哥尼流；腓利之家；保罗被囚两年（徒10、21、23–26）",
 "damascus":"扫罗归信（徒9）","antioch":"第一个外邦教会与宣教基地（徒11、13、15、18）",
 "tarsus":"保罗家乡（徒9:11；22:3）","salamis":"在会堂传道（徒13）",
 "paphos":"方伯士求保罗信主（徒13）","perga":"马可离队（徒13）",
 "pantioch":"会堂讲道后转向外邦人（徒13）","iconium":"分裂与逼迫（徒14）",
 "lystra":"被当作神，后被石头打；提摩太的家乡（徒14、16）","derbe":"第一次旅行终点（徒14）",
 "troas":"马其顿异象；犹推古复活（徒16、20）","philippi":"吕底亚、禁卒；欧洲第一个教会（徒16）",
 "thessalonica":"「搅乱天下」的指控（徒17）","berea":"天天考查圣经（徒17）",
 "athens":"亚略巴古讲道（徒17）","corinth":"住一年半；迦流不受理（徒18）",
 "ephesus":"推喇奴学房；亚底米暴动（徒19）","miletus":"对以弗所长老告别（徒20）",
 "tyre":"门徒劝阻保罗（徒21）","sidon":"犹流宽待保罗（徒27）","myra":"换亚历山大粮船（徒27）",
 "crete":"佳澳；不听劝告（徒27）","malta":"毒蛇不伤；部百流（徒28）",
 "syracuse":"停留三天（徒28）","puteoli":"弟兄留住七天（徒28）",
 "rome":"软禁两年，放胆传道（徒28）","alexandria":"亚波罗的家乡；粮船出发地（徒18:24、27:6）",
 "cappadocia":"五旬节听众之一（徒2:9）","pontus":"五旬节听众；亚居拉家乡（徒2:9；18:2）",
 "sidon":"徒27：犹流宽待保罗","myra":"徒27：换船",
 "arabia":"保罗曾往阿拉伯（加1:17）","azotus":"腓利走过亚锁都各城（徒8:40）",
 "sardis":"亚细亚七教会之一（启3:1）","philadelphia":"亚细亚七教会之一（启3:7）",
 "appforum":"亚比亚大道驿站，罗马弟兄来迎（徒28:15）","threetaverns":"亚比亚大道驿站（徒28:15）",
 "dyrrhachium":"厄纳齐亚大道西端（亚得里亚海）"
}

def _ll(k):
    lon,lat=ll(k); return [round(lat,3), round(lon,3)]

def _nm(k):
    if k in C: return C[k][0]
    return {"seleucia":"西流基","attalia":"亚大利","neapolis":"尼亚波利","amphipolis":"暗妃波里",
            "cenchreae":"坚革哩","assos":"亚朔","cos":"哥士","rhodes":"罗底","patara":"帕大喇",
            "ptolemais":"多利买","cnidus":"革尼土","fairhavens":"佳澳","rhegium":"利基翁",
            "sea1":"海路","sea2":"海路","sea3":"海路","crete_s":"革哩底南岸","sea4":"海路",
            "sea5":"海路","sea6":"海路"}.get(k,k)

def pts_of(keys, color="#f5b942"):
    out=[]
    for k in keys:
        if k.startswith("sea") or k in ("crete_s",): continue
        out.append({"n":_nm(k),"ll":_ll(k),"d":CITY.get(k,""),"c":color,"k":k})
    return out

def path_of(keys):
    return [_ll(k) for k in keys]

# ---------- 概念示意图 ----------
IC = {"city":"●","port":"⚓","sea":"🌊","event":"✦","rome":"🏛","jer":"★"}

def _wave_pts(n, W=860, H=210, y0=108, amp=36, pad=48):
    if n<=1: return [(W/2,y0)]
    return [(pad+i*(W-2*pad)/(n-1), y0 + (amp if i%2 else -amp)) for i in range(n)]

def _curve(pts):
    if len(pts)<2: return "M"+" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    d=f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts)-1):
        p0=pts[i-1] if i else pts[i]; p1=pts[i]; p2=pts[i+1]; p3=pts[i+2] if i+2<len(pts) else p2
        c1=(p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        d+=f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d

def path_schematic(title, stops, color="#4fb3ff", kind="land", caption=""):
    """stops: [(name, kind)] kind=city|port|sea|event|rome|jer"""
    n=len(stops); W=max(640, n*92); H=220
    pts=_wave_pts(n,W,H)
    d=_curve(pts)
    uid=abs(hash(title+color))%100000
    nodes=""
    for i,((name,kd),(x,y)) in enumerate(zip(stops,pts)):
        ic={"port":"⚓","sea":"🌊","event":"✦","rome":"🏛","jer":"★"}.get(kd,"")
        lab=f"{ic}{name}" if ic else name
        nodes+=f'<g class="sn"><circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{color}" stroke="#fff" stroke-width="2"/>'
        nodes+=f'<text x="{x:.1f}" y="{y+(28 if i%2 else -18):.1f}" text-anchor="middle" font-size="13">{esc(lab)}</text></g>'
    if kind=="sea":
        sea=f'<rect width="100%" height="100%" fill="url(#sg{uid})"/>'
    else:
        sea=f'<rect width="100%" height="100%" fill="url(#lg{uid})"/>'
    svg=f'''<svg class="cmo" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}" preserveAspectRatio="xMidYMid meet">
<defs>
  <linearGradient id="lg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#152445"/><stop offset="1" stop-color="#1c3358"/></linearGradient>
  <linearGradient id="sg{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d3a5c"/><stop offset="1" stop-color="#12304c"/></linearGradient>
</defs>
{sea}
<text x="16" y="28" fill="#ffd36b" font-size="15" font-weight="700">{esc(title)}</text>
<path class="sch-route draw" d="{d}" fill="none" stroke="{color}" stroke-width="3.4" stroke-linecap="round"/>
<circle r="7" fill="#ff6b8b" stroke="#fff" stroke-width="2"><animateMotion dur="{max(6,n)}s" repeatCount="indefinite" path="{d}"/></circle>
{nodes}
</svg>'''
    return svg

def basin_regions():
    """抽象地中海区域（示意位置，非精确海岸）。用 lon/lat 经 geo.P 投影。"""
    blobs=[
      ("意大利",14.5,42.3,15.5,41.0,"#c08457"),
      ("西西里",14.3,37.5,15.3,37.1,"#d4a574"),
      ("马其顿",22.4,41.2,21.6,40.6,"#5aa9ff"),
      ("亚该亚",22.5,37.6,23.4,38.2,"#7dd3fc"),
      ("亚细亚",28.2,38.3,27.4,37.6,"#3fd39a"),
      ("加拉太",32.6,38.7,33.2,38.2,"#86efac"),
      ("叙利亚",37.0,35.4,36.5,34.6,"#f5b942"),
      ("犹太",35.1,31.6,34.7,31.1,"#fb7185"),
      ("埃及",30.8,30.6,31.6,30.2,"#fbbf24"),
      ("塞浦路斯",33.2,35.1,33.6,34.8,"#67e8f9"),
      ("革哩底",24.9,35.2,25.6,35.0,"#93c5fd"),
    ]
    return blobs

def concept_geo(title, routes, keys, color="#4fb3ff", regions=True):
    """用与实景图同一套经纬度的概念底图（色块区域 + 路线 + 城市）。"""
    s=[f'<svg class="cmo gmap cgeo" viewBox="0 0 {GW} {GH}" role="img" aria-label="{esc(title)}">']
    s.append(f'<rect width="{GW}" height="{GH}" fill="#12304c"/>')
    s.append('<text x="20" y="36" fill="#ffd36b" font-size="28" font-weight="700">'+esc(title)+'</text>')
    if regions:
        for n,lo,la,lo2,la2,c in basin_regions():
            x,y=P(lo,la); x2,y2=P(lo2,la2)
            rx,ry=abs(x2-x)+70, abs(y2-y)+46
            s.append(f'<ellipse class="blob" cx="{(x+x2)/2:.0f}" cy="{(y+y2)/2:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{c}" fill-opacity=".28" stroke="{c}" stroke-opacity=".7" stroke-width="2"/>')
            s.append(f'<text class="rgn" x="{(x+x2)/2:.0f}" y="{(y+y2)/2:.0f}" text-anchor="middle" fill="{c}" font-size="22">{n}</text>')
    # seas label
    for n,lo,la in (("地 中 海",18.8,33.6),("爱琴海",25.0,39.1),("黑 海",33.4,42.4)):
        x,y=P(lo,la); s.append(f'<text class="sea" x="{x:.0f}" y="{y:.0f}" text-anchor="middle" fill="rgba(186,230,253,.45)" font-size="26" letter-spacing=".3em">{n}</text>')
    for i,(nm,col,ks) in enumerate(routes):
        d=smooth([P(*ll(k)) for k in ks])
        dur=max(8,len(ks)//2)
        s.append(f'<g class="lyr"><path d="{d}" fill="none" stroke="{col}" stroke-width="3.6" stroke-linecap="round" stroke-dasharray="11 8" class="sch-route"/><circle r="8" fill="{col}" stroke="#fff" stroke-width="2"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{d}"/></circle></g>')
    for k in keys:
        if k not in C: continue
        n,lon,lat,dx,dy,an=C[k]; x,y=P(lon,lat)
        s.append(f'<g class="city"><circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#fff" stroke="#0b1325" stroke-width="2"/><text x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{an}" font-size="16">{n}</text></g>')
    s.append('</svg>')
    return "".join(s)

def ring_schematic():
    # 1:8 四圈情景图
    return '''<svg class="cmo rings2" viewBox="0 0 560 560" role="img" aria-label="徒1:8 四圈扩展">
      <defs><radialGradient id="rgA" cx="50%" cy="50%"><stop offset="0" stop-color="#f5b942" stop-opacity=".15"/><stop offset="1" stop-color="#3b5bff" stop-opacity=".05"/></radialGradient></defs>
      <rect width="560" height="560" fill="url(#rgA)"/>
      <g text-anchor="middle" font-weight="700">
        <circle class="ring" cx="280" cy="280" r="240" fill="none" stroke="#ff6b8b" stroke-width="3" stroke-dasharray="8 8" style="--d:.1s"/>
        <text x="280" y="36" fill="#ff6b8b" font-size="16">直到地极 · 罗马</text>
        <circle class="ring" cx="280" cy="280" r="175" fill="none" stroke="#4fb3ff" stroke-width="3" stroke-dasharray="8 8" style="--d:.25s"/>
        <text x="280" y="114" fill="#4fb3ff" font-size="16">犹太全地</text>
        <circle class="ring" cx="280" cy="280" r="110" fill="none" stroke="#3fd39a" stroke-width="3" stroke-dasharray="8 8" style="--d:.4s"/>
        <text x="280" y="180" fill="#3fd39a" font-size="16">撒马利亚</text>
        <circle class="ring" cx="280" cy="280" r="48" fill="#f5b942" stroke="#fff" stroke-width="3" class="ring" style="--d:.55s"/>
        <text x="280" y="286" fill="#1a1300" font-size="15">耶路撒冷</text>
      </g>
      <path d="M280,280 C330,200 420,200 500,80" fill="none" stroke="#ffd36b" stroke-width="3" stroke-dasharray="7 6"/>
      <circle r="6" fill="#ff6b8b" stroke="#fff" stroke-width="2"><animateMotion dur="5s" repeatCount="indefinite" path="M280,280 C330,200 420,200 500,80"/></circle>
      <text x="508" y="76" fill="#ffd36b" font-size="14">罗马</text>
    </svg>'''

def diaspora_schematic():
    nations=[
      ("帕提亚",-80,-10),("玛代",-40,-70),("以拦",0,-95),("美索不达米亚",50,-80),
      ("加帕多家",95,-40),("本都",115,10),("亚细亚",100,70),("弗吕家",55,100),
      ("旁非利亚",5,110),("埃及",-50,95),("古利奈",-95,55),("罗马",-120,0),
      ("克里特",-90,-55),("阿拉伯",-20,70),("犹太",40,40)
    ]
    s=['<svg class="cmo" viewBox="0 0 640 440" role="img" aria-label="五旬节万邦示意图">']
    s.append('<rect width="640" height="440" fill="#152445"/><text x="20" y="30" fill="#ffd36b" font-size="16" font-weight="700">五旬节的听众：从耶路撒冷散向万邦（徒2:9-11）</text>')
    cx,cy=320,230
    s.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="#f5b942"/><text x="{cx}" y="{cy+5}" text-anchor="middle" fill="#1a1300" font-size="13" font-weight="700">耶路撒冷</text>')
    for i,(n,dx,dy) in enumerate(nations):
        x,y=cx+dx*1.7,cy+dy*1.35
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#f5b942" stroke-opacity=".45" stroke-dasharray="4 5"/>')
        s.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#4fb3ff"/><text x="{x}" y="{y-10}" text-anchor="middle" fill="#e8ecf6" font-size="12">{n}</text>')
    s.append('<circle r="6" fill="#ff6b8b" stroke="#fff" stroke-width="2"><animateMotion dur="8s" repeatCount="indefinite" path="M320,196 C420,120 500,200 480,300 C400,360 240,360 160,280 C120,200 220,120 320,196"/></circle>')
    s.append('</svg>')
    return "".join(s)

def religion_schematic():
    items=[("耶路撒冷","圣殿 / 公会",280,70,"#f5b942"),("路司得","丢斯与希耳米",80,200,"#fb7185"),
           ("腓立比","巫鬼与帝王",80,80,"#c08457"),("雅典","未识之神 · 哲学",200,330,"#5aa9ff"),
           ("哥林多","偶像与肉市",360,340,"#f472b6"),("以弗所","亚底米大庙",500,200,"#3fd39a"),
           ("罗马","帝王崇拜",520,70,"#ff6b8b")]
    s=['<svg class="cmo" viewBox="0 0 640 420" role="img" aria-label="使徒行传中的宗教世界">']
    s.append('<rect width="640" height="420" fill="#152445"/><text x="16" y="28" fill="#ffd36b" font-size="16" font-weight="700">宗教世界：圣殿、会堂、偶像与帝王崇拜</text>')
    for i,(a,b,x,y,c) in enumerate(items):
        s.append(f'<rect x="{x-70}" y="{y-28}" width="140" height="58" rx="14" fill="{c}" fill-opacity=".2" stroke="{c}" stroke-width="2"/>')
        s.append(f'<text x="{x}" y="{y-2}" text-anchor="middle" fill="#e8ecf6" font-size="15" font-weight="700">{a}</text>')
        s.append(f'<text x="{x}" y="{y+18}" text-anchor="middle" fill="{c}" font-size="12">{b}</text>')
    # connecting dashes to jerusalem
    for a,b,x,y,c in items[1:]:
        s.append(f'<path d="M280,98 Q{(280+x)/2},{(70+y)/2-20} {x},{y-28}" fill="none" stroke="#94a3b8" stroke-dasharray="4 6" stroke-width="1.4"/>')
    s.append('</svg>')
    return "".join(s)

# ---------- 地图对 HTML ----------
SRCS_BTNS = [
 ("osm","OSM"),("esri-topo","地形"),("esri-img","卫星"),("esri-st","街道"),
 ("esri-shade","地貌"),("otm","等高"),("hot","人道"),("osm-de","OSM-DE")
]

def mappair(mid, title, schematic, hist, play=True, caption="概念示意图（离线可用，不依赖网络）"):
    def _btn(i,n):
        on=' class="on"' if i=="osm" else ""
        return f'<button type="button" data-src="{i}"{on}>{esc(n)}</button>'
    btns="".join(_btn(i,n) for i,n in SRCS_BTNS)
    pl='<button type="button" class="btn play-live">▶ 播放路线</button>' if play else ""
    return f'''<section class="mappair" id="mp-{mid}">
<div class="mph"><h3 id="mp-{mid}-t">{esc(title)}</h3></div>
<div class="mpgrid">
<figure class="schematic glass">{schematic}<div class="anim-ctrl" data-anim="route"><button type="button" class="btn sm anim-play" aria-label="播放或暂停路线动画">▶ 播放</button><input type="range" class="anim-scrub" min="0" max="100" value="0" aria-label="路线进度"><span class="anim-pct">0%</span></div><figcaption>{esc(caption)}</figcaption></figure>
<div class="livebox glass" data-map="{esc(mid)}">
  <div class="mapbar"><span class="mapbar-l">在线实景地图</span><div class="srcs" role="group" aria-label="底图来源">{btns}</div>{pl}</div>
  <div class="lmap" role="region" aria-label="{esc(title)} 交互地图"></div>
  <p class="mstat" aria-live="polite">滚动到此处后加载。网络不稳时自动切换底图；若全部失败，示意图与标记仍可阅读。</p>
</div>
</div>
<div class="maphist">{hist}</div>
</section>'''

def bounds_of(keys, pad=1.2):
    lls=[_ll(k) for k in keys if not str(k).startswith("sea")]
    if not lls: return [[31,12],[43,38]]
    lats=[x[0] for x in lls]; lons=[x[1] for x in lls]
    return [[min(lats)-pad, min(lons)-pad],[max(lats)+pad, max(lons)+pad]]

def cfg_route(mid, name, keys, color, extra_pts=None, dash=None):
    pts=pts_of([k for k in (extra_pts or keys) if k in C or k in WP], color)
    return mid, {"color":color,"maxZoom":8,"bounds":bounds_of(keys),"points":pts,
                 "routes":[{"n":name,"c":color,"path":path_of(keys),"dash":dash}]}

def chapter_schematic(c):
    keys=c.get("route") or c["map"]
    stops=[]
    seen=set()
    for k in keys:
        if k.startswith("sea") or k=="crete_s":
            lab="海路"; kd="sea"
        else:
            lab=_nm(k); kd="jer" if k=="jerusalem" else ("rome" if k=="rome" else ("port" if k in ("paphos","caesarea","troas","puteoli","malta","myra","sidon","tyre") else "city"))
        if (lab in seen) and kd!="sea": continue
        seen.add(lab); stops.append((lab,kd))
    if len(stops)<1: stops=[(_nm(c["map"][0]) if c.get("map") else "地点","city")]
    col={"jer":"#f5b942","sam":"#3fd39a","mis":"#4fb3ff","rom":"#ff6b8b"}[c["sec"]]
    return path_schematic(f'第 {c["no"]} 章 · {c["t"]}', stops, col, "sea" if c["no"] in (27,28) else "land")

def chapter_cfg(c):
    col={"jer":"#f5b942","sam":"#3fd39a","mis":"#4fb3ff","rom":"#ff6b8b"}[c["sec"]]
    keys=c.get("route") or c["map"]
    show=[k for k in (c["map"]+ (c.get("route") or [])) if k in C]
    # unique preserve
    u=[]; 
    for k in show:
        if k not in u: u.append(k)
    mid=f"ch{c['no']}"
    routes=[]
    if c.get("route"):
        routes=[{"n":f"徒{c['no']} 路线","c":col,"path":path_of(c["route"])}]
    return mid, {"color":col,"maxZoom":9,"bounds":bounds_of(keys,.8),"points":pts_of(u,col),"routes":routes}

def chapter_pair(c):
    hist=f'<p class="note">本章地点：{"、".join(_nm(k) for k in c["map"] if k in C)}。示意图按故事顺序排列；右侧／下方为可缩放的真实地图（多源底图，失败自动切换）。</p>'
    return mappair(f"ch{c['no']}", f"第 {c['no']} 章地图 · {c['t']}", chapter_schematic(c), hist, play=bool(c.get("route")))

# ---------- 全局地图配置 ----------
def all_cfgs(chapters):
    cfgs={}
    def add(mid, cfg): cfgs[mid]=cfg
    # overview
    rts=[{"n":"早期扩展（徒1–12）","c":"#2dd4bf","path":path_of(ks)} for ks in EARLY]
    for jid,name,col,ks in JOURNEYS:
        rts.append({"n":name,"c":col,"path":path_of(ks)})
    keys=["jerusalem","samaria","caesarea","damascus","antioch","tarsus","salamis","paphos","pantioch","iconium","lystra","derbe",
          "troas","philippi","thessalonica","berea","athens","corinth","ephesus","miletus","tyre","crete","malta","syracuse","puteoli","rome"]
    add("overview",{"color":"#f5b942","maxZoom":7,"bounds":[[30.5,10.5],[43.2,38.5]],"points":pts_of(keys),"routes":rts})
    add("early",{"color":"#2dd4bf","maxZoom":8,"bounds":[[31.2,33.8],[37.0,37.2]],
                 "points":pts_of(["jerusalem","samaria","gaza","joppa","lydda","caesarea","damascus","antioch","tarsus","tyre","sidon"]),
                 "routes":[{"n":"早期扩展","c":"#2dd4bf","path":path_of(ks)} for ks in EARLY]})
    for jid,name,col,ks in JOURNEYS:
        add(jid,{"color":col,"maxZoom":8,"bounds":bounds_of(ks),"points":pts_of([k for k in ks if k in C],col),"routes":[{"n":name,"c":col,"path":path_of(ks)}]})
    # provinces
    REG=[
      ("犹太",[[31.2,34.2],[31.2,35.6],[32.9,35.6],[32.9,34.2]],"#fb7185","罗马行省（巡抚驻凯撒利亚）；圣殿在耶路撒冷。"),
      ("叙利亚",[[33.0,35.6],[33.0,37.2],[36.8,37.2],[36.8,35.6]],"#f5b942","安提阿为省会，帝国第三大城。"),
      ("加拉太",[[37.4,30.5],[37.4,35.0],[39.8,35.0],[39.8,30.5]],"#86efac","南加拉太：彼西底安提阿、以哥念、路司得、特庇。"),
      ("亚细亚",[[36.8,26.0],[36.8,29.8],[39.6,29.8],[39.6,26.0]],"#3fd39a","省会以弗所；亚底米崇拜中心。"),
      ("马其顿",[[39.8,20.8],[39.8,24.8],[41.8,24.8],[41.8,20.8]],"#5aa9ff","腓立比是罗马殖民地；厄纳齐亚大道横贯。"),
      ("亚该亚",[[36.4,21.2],[36.4,24.2],[38.6,24.2],[38.6,21.2]],"#7dd3fc","省会哥林多；雅典为文化旧都。"),
      ("塞浦路斯",[[34.5,32.2],[34.5,34.6],[35.7,34.6],[35.7,32.2]],"#67e8f9","方伯驻帕弗；士求保罗（徒13）。"),
      ("意大利",[[40.4,12.0],[40.4,15.5],[42.6,15.5],[42.6,12.0]],"#c08457","罗马为帝国首都；部丢利为港口。"),
    ]
    regs=[{"n":n,"poly":poly,"c":c,"d":d} for n,poly,c,d in REG]
    add("provinces",{"color":"#f5b942","maxZoom":6,"bounds":[[30.2,10.8],[43.4,38.6]],
        "points":pts_of(["jerusalem","caesarea","antioch","pantioch","ephesus","philippi","corinth","athens","paphos","rome"]),
        "regions":regs,"routes":[]})
    # roads and sea
    via_e= path_of(["neapolis","philippi","amphipolis","thessalonica","berea"]) if True else []
    # neapolis-philippi is Via Egnatia start in the narrative
    via_a=[[40.82,14.12],[41.30,13.83],[41.50,13.25],[41.76,12.62],[41.89,12.48]]  # Puteoli approx to Rome along Appia corridor
    via_s=path_of(["perga","pantioch","iconium","lystra","derbe"])
    sea_g=path_of(["alexandria","myra","cnidus","fairhavens","malta","syracuse","rhegium","puteoli"])
    add("roads",{"color":"#f5b942","maxZoom":6,"bounds":[[31,10.8],[43,34]],
        "points":pts_of(["philippi","thessalonica","pantioch","iconium","puteoli","rome","myra","malta","alexandria","ephesus","corinth"]),
        "routes":[
          {"n":"厄纳齐亚大道（Via Egnatia）","c":"#5aa9ff","path":via_e},
          {"n":"亚比亚大道一带（Via Appia；徒28:15）","c":"#c08457","path":via_a},
          {"n":"塞巴斯特大道一带（南加拉太）","c":"#3fd39a","path":via_s},
          {"n":"亚历山大粮船航线（示意）","c":"#67e8f9","path":sea_g,"dash":"8 8"},
        ]})
    # diaspora Acts 2
    dia=[
      ("帕提亚",35.7,51.4),("玛代",35.0,48.0),("以拦",32.0,48.5),("美索不达米亚",33.4,44.4),
      ("犹太",31.78,35.23),("加帕多家",38.7,35.5),("本都",41.3,36.3),("亚细亚",37.94,27.34),
      ("弗吕家",38.5,30.0),("旁非利亚",36.9,30.7),("埃及",31.2,29.9),("古利奈",32.1,21.6),
      ("罗马",41.89,12.48),("克里特",35.2,24.95),("阿拉伯",29.0,36.0)
    ]
    add("diaspora",{"color":"#f5b942","maxZoom":5,"bounds":[[24,8],[45,54]],
        "points":[{"n":n,"ll":[lat,lon],"c":"#4fb3ff" if n!="犹太" else "#f5b942","d":"五旬节听众（徒2:9-11）","r":8 if n in ("犹太","罗马") else 6} for n,lat,lon in dia],
        "routes":[]})
    # religion
    rel=[
      ("jerusalem","圣殿与公会：犹太敬拜的中心；司提反与保罗都被控「糟蹋圣殿」。","#f5b942"),
      ("lystra","土人认巴拿巴为丢斯、保罗为希耳米（徒14）。","#fb7185"),
      ("philippi","巫鬼的使女；罗马殖民地的帝王崇拜背景（徒16）。","#c08457"),
      ("athens","斯多亚与伊壁鸠鲁；亚略巴古；未识之神的坛（徒17）。","#5aa9ff"),
      ("corinth","偶像之城；祭偶像之物的肉市；迦流座（徒18）。","#f472b6"),
      ("ephesus","亚底米大庙（古代世界七大奇迹之一）；邪术书卷；银匠行会（徒19）。","#3fd39a"),
      ("rome","帝王崇拜的首都；「另有一个王耶稣」在此听来尤为刺耳。","#ff6b8b"),
    ]
    add("religion",{"color":"#b794ff","maxZoom":6,"bounds":[[30.5,10.8],[43,38]],
        "points":[{"n":C[k][0],"ll":_ll(k),"d":d,"c":c} for k,d,c in rel],"routes":[]})
    add("cities",{"color":"#f5b942","maxZoom":6,"bounds":[[30.8,10.8],[43,38]],
        "points":pts_of(["jerusalem","caesarea","antioch","philippi","athens","corinth","ephesus","rome","malta","paphos"]),
        "routes":[]})
    for c in chapters:
        mid,cfg=chapter_cfg(c); add(mid,cfg)
    return cfgs

def dump_js(path, chapters):
    cfgs=all_cfgs(chapters)
    from maps_extra import extra_cfgs
    cfgs.update(extra_cfgs())
    open(path,"w",encoding="utf-8").write("window.ACTS_MAPS="+json.dumps(cfgs,ensure_ascii=False,separators=(",",":"))+";\n")
    return len(cfgs)

def thematic_pair(mid):
    from maps_extra import thematic_pair as _tp
    return _tp(mid)
