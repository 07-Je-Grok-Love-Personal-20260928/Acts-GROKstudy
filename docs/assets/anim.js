/* 使徒行传深读 v3.1：路线/图表动画——仅 dashoffset、opacity、transform；视口内才跑；尊重 reduced-motion */
(function(){
"use strict";
var reduce = false;
try{ reduce = matchMedia("(prefers-reduced-motion: reduce)").matches; }catch(e){}
var $ = function(s,r){return (r||document).querySelector(s)};
var $$ = function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};

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
function apply(box, t){ /* t in 0..1 */
  var svg=box._svg; if(!svg) return;
  var paths=box._paths||[];
  paths.forEach(function(p,i){
    var L=p._L||0; if(!L) return;
    /* rays can appear in sequence */
    var delay=0;
    if(p.classList.contains("draw-ray")){
      var g=p.closest("[data-at]"); delay=g?parseFloat(g.getAttribute("data-at"))||0:0;
      var local=t<delay?0: Math.min(1,(t-delay)/Math.max(0.08,1-delay));
      p.style.strokeDashoffset=String(L*(1-local));
      return;
    }
    p.style.strokeDashoffset=String(L*(1-t));
  });
  $$("[data-at]", svg).forEach(function(el){
    var a=parseFloat(el.getAttribute("data-at"))||0;
    var on=t+0.02>=a;
    el.style.opacity=on?"1":"0";
  });
  $$(".gbar", svg).forEach(function(el){
    var g=el.closest("[data-at]"); var a=g?parseFloat(g.getAttribute("data-at"))||0:0;
    var local=t<a?0:1;
    el.style.transform="scaleX("+local+")";
  });
  var dot=$(".anim-dot", svg);
  if(dot){
    var route=$("path.sch-route, path.draw", svg);
    if(route && route._L){
      var pt=route.getPointAtLength(route._L * Math.max(0,Math.min(1,t)));
      if(dot.tagName==="circle"){ dot.setAttribute("cx", pt.x); dot.setAttribute("cy", pt.y); }
      else dot.setAttribute("transform", "translate("+pt.x+","+pt.y+")");
    }
  }
  var pct=$(".anim-pct", box);
  if(pct) pct.textContent=Math.round(t*100)+"%";
  var scrub=$(".anim-scrub", box);
  if(scrub && !box._scrubbing) scrub.value=String(Math.round(t*100));
  box._t=t;
}

function bind(box){
  if(box._bound) return;
  var svg=box.matches("svg")?box: $("svg", box);
  if(!svg) return;
  box._svg=svg;
  box._paths=readyPaths(svg);
  $$("[data-at]", svg).forEach(function(el){ el.style.opacity="0"; el.style.transition="opacity .25s linear"; });
  $$(".gbar", svg).forEach(function(el){ el.style.transform="scaleX(0)"; el.style.transition="transform .3s linear"; });
  var play=$(".anim-play", box);
  var scrub=$(".anim-scrub", box);
  box._t=0; box._playing=false; box._raf=0; box._t0=0; box._dur=Math.max(4200, (box._paths.length||8)*500);
  function stop(){ box._playing=false; if(box._raf) cancelAnimationFrame(box._raf); box._raf=0; if(play) play.textContent="▶ 播放"; }
  function start(){
    if(reduce){ apply(box,1); return; }
    box._playing=true; if(play) play.textContent="⏸ 暂停";
    if(box._t>=0.995) box._t=0;
    var startT=performance.now() - box._t*box._dur;
    function step(now){
      if(!box._playing) return;
      var t=Math.min(1,(now-startT)/box._dur);
      apply(box,t);
      if(t<1) box._raf=requestAnimationFrame(step);
      else stop();
    }
    box._raf=requestAnimationFrame(step);
  }
  if(play) play.addEventListener("click", function(){
    if(box._playing) stop(); else start();
  });
  if(scrub){
    var seek=function(){ stop(); apply(box, (+scrub.value)/100); };
    scrub.addEventListener("pointerdown", function(){ box._scrubbing=1; });
    scrub.addEventListener("input", seek);
    scrub.addEventListener("change", function(){ box._scrubbing=0; seek(); });
  }
  box._bound=1;
  if(reduce) apply(box,1);
  else apply(box,0);
  box._start=start;
}

function maybeStart(box){
  bind(box);
  if(reduce) return;
  if(box._auto) return;
  box._auto=1;
  /* slight delay so layout settles */
  setTimeout(function(){ if(!box._playing && box._t===0) box._start(); }, 120);
}

function init(){
  var boxes=$$(".schematic, .animbox");
  if(!boxes.length) return;
  if(!("IntersectionObserver" in window)){ boxes.forEach(function(b){ bind(b); if(!reduce) maybeStart(b); }); return; }
  var io=new IntersectionObserver(function(es){
    es.forEach(function(en){
      if(en.isIntersecting){ maybeStart(en.target); }
      else if(en.target._playing){ /* pause offscreen */
        en.target._playing=false; if(en.target._raf) cancelAnimationFrame(en.target._raf);
        var p=$(".anim-play", en.target); if(p) p.textContent="▶ 播放";
      }
    });
  },{rootMargin:"80px 0px", threshold:0.15});
  boxes.forEach(function(b){ io.observe(b); });
}
if(document.readyState!=="loading") init();
else document.addEventListener("DOMContentLoaded", init);
})();
