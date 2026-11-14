# Playwright QA: overflow, clipping, header overlap, interactions, console errors
# widths: 390, 768, 1024, 1440, plus landscape phone 844x390
import asyncio, json, os, sys, subprocess, time, socket
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=os.path.join(ROOT,"docs"); OUT=os.path.join(ROOT,"build","qa"); os.makedirs(OUT,exist_ok=True)
PAGES=[f for f in sorted(os.listdir(D)) if f.endswith(".html")]
CHROME="/usr/bin/google-chrome"
JS=r"""()=>{const de=document.documentElement,vw=de.clientWidth,res={sw:de.scrollWidth,vw:vw,off:[],clip:[],hdr:[]};
const scrollers=n=>{for(let p=n.parentElement;p;p=p.parentElement){const s=getComputedStyle(p);if(/(auto|scroll|hidden)/.test(s.overflowX)&&p!==document.body&&p!==de)return true;if(p.id==='toc'||p.id==='navdrop'||p.classList.contains('lmap')||p.classList.contains('leaflet-container'))return true}return false};
document.querySelectorAll('main *').forEach(n=>{const r=n.getBoundingClientRect();if(!r.width||getComputedStyle(n).position==='fixed')return;
 if((r.right>vw+2||r.left<-2)&&!scrollers(n))res.off.push((n.className||n.tagName)+' '+Math.round(r.left)+'→'+Math.round(r.right));
 const s=getComputedStyle(n);if(['P','LI','TD','B','SPAN','A','H2','H3','H4','SMALL'].includes(n.tagName)&&s.overflowX==='visible'&&n.scrollWidth>n.clientWidth+3&&n.clientWidth>0&&s.display!=='inline'&&!scrollers(n))res.clip.push(n.tagName+'.'+n.className+':'+n.textContent.slice(0,20))});
const hs=[...document.querySelectorAll('.top > *')].filter(e=>getComputedStyle(e).display!=='none').map(e=>e.getBoundingClientRect());
for(let i=0;i<hs.length;i++)for(let j=i+1;j<hs.length;j++){const a=hs[i],b=hs[j];if(a.right>b.left+1&&b.right>a.left+1&&a.bottom>b.top&&b.bottom>a.top)res.hdr.push(i+'x'+j)}
res.off=res.off.slice(0,8);res.clip=res.clip.slice(0,8);return res}"""

async def interact(pg):
    # TOC toggle
    btn=await pg.query_selector("#tocbtn")
    if btn:
        await btn.click(); await pg.wait_for_timeout(200)
        await btn.click(); await pg.wait_for_timeout(200)
    # expand hard questions / details
    for i,el in enumerate(await pg.query_selector_all("details.hardq, details.intro, details")):
        if i>8: break
        try:
            await el.evaluate("e=>{if(!e.open)e.open=true}")
        except Exception:
            pass
    # flip a card
    fl=await pg.query_selector(".flip")
    if fl:
        try: await fl.click(); await pg.wait_for_timeout(150)
        except Exception: pass
    # map source buttons (do not wait for tiles)
    btns=await pg.query_selector_all(".srcs button")
    for b in btns[:3]:
        try:
            await b.click(); await pg.wait_for_timeout(120)
        except Exception:
            pass
    # SVG layer toggles if present
    lbs=await pg.query_selector_all(".maptools .lb[data-l]")
    for b in lbs[:2]:
        try: await b.click(); await pg.wait_for_timeout(80)
        except Exception: pass
    await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
    await pg.wait_for_timeout(200)

async def main():
    so=socket.socket(); so.bind(("127.0.0.1",0)); PORT=so.getsockname()[1]; so.close()
    srv=subprocess.Popen([sys.executable,"-m","http.server",str(PORT),"--bind","127.0.0.1","-d",D],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(0.6)
    rep={}; bad=0
    views=[(390,844,"phone"),(844,390,"phone-land"),(768,1024,"tablet"),(1024,768,"tablet-land"),(1440,900,"desktop")]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=CHROME, args=["--no-sandbox","--disable-gpu"])
        for w,h,tag in views:
            ctx=await b.new_context(viewport={"width":w,"height":h},device_scale_factor=1)
            pg=await ctx.new_page(); errs=[]
            pg.on("pageerror",lambda e:errs.append(str(e)))
            for f in PAGES:
                errs.clear()
                await pg.goto(f"http://127.0.0.1:{PORT}/{f}",wait_until="load",timeout=30000)
                await pg.wait_for_timeout(180)
                title=await pg.title()
                assert "使徒行传" in title, (f,title)
                await interact(pg)
                r=await pg.evaluate(JS); r["errs"]=errs[:]; r["title"]=title; r["view"]=tag
                ok = r["sw"]<=r["vw"]+2 and not r["off"] and not r["clip"] and not r["hdr"] and not r["errs"]
                bad += (not ok); rep[f"{w}x{h}/{f}"]=r
                print(("OK " if ok else "BAD"),f"{w}x{h}",f,"sw",r["sw"],"vw",r["vw"],r["off"][:3],r["clip"][:3],r["hdr"],r["errs"][:2])
                if tag in ("phone","desktop") or not ok:
                    await pg.screenshot(path=os.path.join(OUT,f"{tag}-{w}-{f[:-5]}.png"),full_page=False)
            await ctx.close()
        await b.close()
    srv.terminate(); json.dump(rep,open(os.path.join(OUT,"qa.json"),"w"),ensure_ascii=False,indent=1); print("BAD PAGES",bad)
asyncio.run(main())
