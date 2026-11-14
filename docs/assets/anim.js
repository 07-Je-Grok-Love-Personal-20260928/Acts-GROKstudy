/* 使徒行传深读 v3.1：路线/图表动画——仅 dashoffset、opacity、transform；视口内才跑；尊重 reduced-motion */
(function(){
"use strict";
var reduce = false;
try{ reduce = matchMedia("(prefers-reduced-motion: reduce)").matches; }catch(e){}
var $ = function(s,r){return (r||document).querySelector(s)};
var $$ = function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};

var lastS = 0, pumpT = 0, waiting = [], active = null;
function markScroll(){ lastS = performance.now(); }
addEventListener("scroll", markScroll, {passive:true});
addEventListener("wheel", markScroll, {passive:true});
addEventListener("touchmove", markScroll, {passive:true});

function lenOf(p){
  try{ return p.getTotalLength(); }catch(e){ return 0; }
}
function readyPaths(svg){
  var paths=$$("path.draw, path.sch-route, line.draw-ray", svg);
  paths.forEach(function(p){
    var L=lenOf(p); if(!L) return;
    p._L=L;
    p.style.strokeDasharray=String(L);
    p.style.strokeDashoffset=String(L);
  });
  return paths;
}
function apply(box, t){
  var svg=box._svg; if(!svg) return;
  var paths=box._paths||[];
  var i, p, L, delay, local, g, a, on, el;
  for(i=0;i<paths.length;i++){
    p=paths[i]; L=p._L||0; if(!L) continue;
    if(p.classList.contains("draw-ray")){
      g=p.closest("[data-at]"); delay=g?parseFloat(g.getAttribute("data-at"))||0:0;
      local=t<delay?0: Math.min(1,(t-delay)/Math.max(0.08,1-delay));
      p.style.strokeDashoffset=String(L*(1-local));
    } else {
      p.style.strokeDashoffset=String(L*(1-t));
    }
  }
  var ats=box._ats||[];
  for(i=0;i<ats.length;i++){
    el=ats[i]; a=el._at; if(a==null){ a=el._at=parseFloat(el.getAttribute("data-at"))||0; }
    on=t+0.02>=a;
    if(el._on!==on){ el._on=on; el.style.opacity=on?"1":"0"; }
  }
  var bars=box._bars||[];
  for(i=0;i<bars.length;i++){
    el=bars[i]; g=el.closest("[data-at]"); a=g?g._at:0; if(a==null) a=0;
    local=t<a?0:1;
    if(el._sc!==local){ el._sc=local; el.style.transform="scaleX("+local+")"; }
  }
  var dot=box._dot, route=box._route;
  if(dot && route && route._L){
    var pt=route.getPointAtLength(route._L * Math.max(0,Math.min(1,t)));
    if(dot.tagName==="circle"){ dot.setAttribute("cx", pt.x); dot.setAttribute("cy", pt.y); }
    else dot.setAttribute("transform", "translate("+pt.x+","+pt.y+")");
  }
  if(box._pct) box._pct.textContent=Math.round(t*100)+"%";
  if(box._scrubEl && !box._scrubbing) box._scrubEl.value=String(Math.round(t*100));
  box._t=t;
}

function bind(box){
  if(box._bound) return;
  var svg=box.matches("svg")?box: $("svg", box);
  if(!svg) return;
  box._svg=svg;
  box._paths=readyPaths(svg);
  box._ats=$$("[data-at]", svg);
  box._bars=$$(".gbar", svg);
  box._dot=$(".anim-dot", svg);
  box._pct=$(".anim-pct", box);
  box._scrubEl=$(".anim-scrub", box);
  box._route=$("path.sch-route, path.draw", svg);
  (box._ats||[]).forEach(function(el){
    el._at=parseFloat(el.getAttribute("data-at"))||0;
    el.style.opacity="0"; el.style.transition="opacity .25s linear";
  });
  (box._bars||[]).forEach(function(el){ el.style.transform="scaleX(0)"; el.style.transition="transform .3s linear"; });
  box._t=0; box._playing=false; box._raf=0; box._dur=Math.max(4200, (box._paths.length||8)*500);
  if(reduce) apply(box,1);
  else apply(box,0);
  box._bound=1;
}

function stop(box){
  if(!box) return;
  box._playing=false;
  if(box._raf) cancelAnimationFrame(box._raf);
  box._raf=0;
  var play=$(".anim-play", box);
  if(play) play.textContent="▶ 播放";
  if(active===box) active=null;
}

function start(box){
  bind(box);
  if(reduce){ apply(box,1); return; }
  if(active && active!==box) stop(active);
  box._playing=true; active=box;
  var play=$(".anim-play", box);
  if(play) play.textContent="⏸ 暂停";
  if(box._t>=0.995) box._t=0;
  var startT=performance.now() - box._t*box._dur;
  function step(now){
    if(!box._playing) return;
    var t=Math.min(1,(now-startT)/box._dur);
    apply(box,t);
    if(t<1) box._raf=requestAnimationFrame(step);
    else stop(box);
  }
  box._raf=requestAnimationFrame(step);
}

function wire(box){
  if(box._wired) return;
  box._wired=1;
  var play=$(".anim-play", box);
  var scrub=$(".anim-scrub", box);
  if(play) play.addEventListener("click", function(){
    bind(box);
    if(box._playing) stop(box); else start(box);
  });
  if(scrub){
    var seek=function(){ bind(box); stop(box); apply(box, (+scrub.value)/100); };
    scrub.addEventListener("pointerdown", function(){ box._scrubbing=1; });
    scrub.addEventListener("input", seek);
    scrub.addEventListener("change", function(){ box._scrubbing=0; seek(); });
  }
}

function maybeStart(box){
  if(reduce){ bind(box); return; }
  if(box._auto) return;
  box._auto=1;
  if(waiting.indexOf(box)<0) waiting.push(box);
  schedulePump();
}

function schedulePump(){
  if(pumpT) return;
  pumpT=setTimeout(pump, 40);
}
function pump(){
  pumpT=0;
  if(!waiting.length) return;
  var idle=performance.now()-lastS;
  if(idle<280){ pumpT=setTimeout(pump, Math.max(40, 300-idle)); return; }
  var box;
  while(waiting.length){
    box=waiting.shift();
    if(!box._inView){ box._auto=0; continue; }
    bind(box);
    if(!box._playing && box._t===0) start(box);
    break;
  }
  if(waiting.length) pumpT=setTimeout(pump, 120);
}

function init(){
  var boxes=$$(".schematic, .animbox");
  if(!boxes.length) return;
  boxes.forEach(wire);
  if(!("IntersectionObserver" in window)){
    boxes.forEach(function(b){ bind(b); if(!reduce) maybeStart(b); });
    return;
  }
  var io=new IntersectionObserver(function(es){
    es.forEach(function(en){
      var box=en.target;
      if(en.isIntersecting){ box._inView=1; maybeStart(box); }
      else {
        box._inView=0;
        if(box._playing) stop(box);
      }
    });
  },{rootMargin:"80px 0px", threshold:0.15});
  boxes.forEach(function(b){ io.observe(b); });
}
if(document.readyState!=="loading") init();
else document.addEventListener("DOMContentLoaded", init);
})();
