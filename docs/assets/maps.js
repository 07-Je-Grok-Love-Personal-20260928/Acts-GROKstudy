/* 使徒行传深读 v2：自托管 Leaflet + 多源底图 + 自动回退；仅在进入视口时初始化 */
(function(){
"use strict";
var SRC=[
  {id:"osm",name:"OpenStreetMap",url:"https://tile.openstreetmap.org/{z}/{x}/{y}.png",sub:"",attr:"© OpenStreetMap",max:19},
  {id:"esri-topo",name:"Esri 地形",url:"https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",sub:"",attr:"Tiles © Esri",max:19},
  {id:"esri-img",name:"Esri 卫星",url:"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",sub:"",attr:"Tiles © Esri",max:18},
  {id:"esri-st",name:"Esri 街道",url:"https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",sub:"",attr:"Tiles © Esri",max:19},
  {id:"esri-shade",name:"Esri 地貌阴影",url:"https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}",sub:"",attr:"Tiles © Esri",max:13},
  {id:"otm",name:"OpenTopoMap",url:"https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",sub:"abc",attr:"© OpenTopoMap (CC-BY-SA) © OSM",max:17},
  {id:"hot",name:"OSM Humanitarian",url:"https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",sub:"abc",attr:"© OSM France · HOT",max:19},
  {id:"osm-de",name:"OSM Deutschland",url:"https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png",sub:"abc",attr:"© OpenStreetMap",max:18}
];
var CHAIN=SRC.map(function(s){return s.id});
var BEST={};
var $ = function(s,r){return (r||document).querySelector(s)};
var $$ = function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};

function note(box,t,bad){
  var el=$(".mstat",box); if(!el) return;
  el.textContent=t; el.classList.toggle("bad",!!bad);
}
function srcOf(id){for(var i=0;i<SRC.length;i++) if(SRC[i].id===id) return SRC[i]; return SRC[0];}

var lp=null;
function needL(){
  if(window.L&&L.map) return Promise.resolve();
  if(lp) return lp;
  if(!document.querySelector('link[href*="leaflet.css"]')){
    var l=document.createElement("link"); l.rel="stylesheet"; l.href="assets/vendor/leaflet/leaflet.css"; document.head.appendChild(l);
  }
  lp=new Promise(function(ok,no){
    var s=document.createElement("script"); s.src="assets/vendor/leaflet/leaflet.js"; s.onload=ok; s.onerror=no; document.head.appendChild(s);
  });
  return lp;
}

function tiles(map,box,start){
  if(map._tl){map.removeLayer(map._tl); map._tl=null;}
  clearTimeout(map._wd);
  var order=CHAIN.slice();
  var pref=start||order[0];
  var ix=order.indexOf(pref); if(ix>0){order.splice(ix,1); order.unshift(pref);}
  if(BEST.id&&BEST.id!==pref){var j=order.indexOf(BEST.id); if(j>0){order.splice(j,1); order.splice(1,0,BEST.id);}}
  var i=0;
  function next(why){
    if(map._tl){map.removeLayer(map._tl); map._tl=null;}
    clearTimeout(map._wd);
    if(i>=order.length){
      note(box,"在线底图均不可达。上方／左侧示意图与地点标记仍可阅读（离线可用）。",1);
      box.classList.add("mtfail");
      return;
    }
    var s=srcOf(order[i]);
    var t=L.tileLayer(s.url,{subdomains:s.sub||"abc",maxZoom:s.max,maxNativeZoom:s.max,attribution:s.attr,keepBuffer:1,updateWhenIdle:true,crossOrigin:false});
    var ok=0,er=0;
    var adv=function(){if(map._tl!==t)return; i++; next();};
    t.on("tileload",function(){
      if(!ok){BEST.id=s.id; note(box,"实景底图 · "+s.name+"（失败时自动切换）"); box.classList.remove("mtfail");
        $$(".srcs button",box).forEach(function(b){b.classList.toggle("on",b.dataset.src===s.id);});
      }
      ok++;
    });
    t.on("tileerror",function(){er++; if((er>=3&&ok===0)||er>ok*2+8) adv();});
    map._tl=t; t.addTo(map);
    var ms=window.__tileTimeout||4500;
    map._wd=setTimeout(function(){if(!ok) adv();},ms);
    note(box,"正在连接 "+s.name+"…");
  }
  box.classList.remove("mtfail");
  next();
}

function listFb(el,cfg){
  var pts=cfg.points||[];
  el.innerHTML='<div class="mapfb"><b>地图脚本未加载（离线或被拦截）。地点列表：</b><ul>'+
    pts.map(function(p){return "<li>"+p.n+(p.d?"："+p.d:"")+"</li>";}).join("")+"</ul></div>";
}

function build(box){
  var id=box.dataset.map, cfg=(window.ACTS_MAPS||{})[id];
  var el=$(".lmap",box);
  if(!el) return;
  if(!(window.L&&L.map)){listFb(el,cfg||{}); return;}
  if(!cfg){el.innerHTML='<div class="mapfb">没有这幅地图的数据。</div>'; return;}
  el.innerHTML="";
  var map=L.map(el,{scrollWheelZoom:false,zoomSnap:.25,attributionControl:true,preferCanvas:true});
  map.attributionControl.setPrefix("Leaflet · 示意图始终离线可用");
  box._map=map;
  (cfg.regions||[]).forEach(function(r){
    if(r.poly) L.polygon(r.poly,{color:r.c,weight:1.4,fillColor:r.c,fillOpacity:.22,dashArray:r.dash||null}).bindPopup("<b>"+r.n+"</b><br>"+(r.d||"")).addTo(map);
    if(r.circle) L.circle(r.circle,{radius:r.rad,color:r.c,weight:1.4,fillColor:r.c,fillOpacity:.2}).bindPopup("<b>"+r.n+"</b>").addTo(map);
  });
  (cfg.routes||[]).forEach(function(r){
    var pl=L.polyline(r.path,{color:r.c,weight:r.w||4,opacity:.92,dashArray:r.dash||null}).addTo(map);
    pl.bindTooltip(r.n,{sticky:true});
    map._routes=(map._routes||[]).concat([r]);
  });
  (cfg.points||[]).forEach(function(p){
    var c=L.circleMarker(p.ll,{radius:p.r||7,color:"#fff",weight:1.6,fillColor:p.c||cfg.color||"#f5b942",fillOpacity:1}).addTo(map);
    c.bindTooltip(p.n,{permanent:innerWidth>=720&&p.perm!==false,direction:p.dir||"right",className:"mlab",offset:[8,0]});
    if(p.d) c.bindPopup("<b>"+p.n+"</b><br>"+p.d);
  });
  var b=cfg.bounds;
  if(b) map.fitBounds(b,{padding:[24,24],maxZoom:cfg.maxZoom||8});
  else {
    var all=[];
    (cfg.points||[]).forEach(function(p){all.push(p.ll);});
    (cfg.routes||[]).forEach(function(r){r.path.forEach(function(x){all.push(x);});});
    if(all.length) map.fitBounds(L.latLngBounds(all).pad(.18),{padding:[24,24],maxZoom:cfg.maxZoom||8});
    else map.setView([36.2,28],5);
  }
  var start=(function(){try{return localStorage.getItem("acts-tiles")||"osm";}catch(e){return "carto-v";}})();
  if(navigator.onLine===false){note(box,"目前离线：请使用示意图。打开网络后可点选底图来源。",1);}
  else tiles(map,box,start);
  $$(".srcs button",box).forEach(function(btn){
    btn.addEventListener("click",function(){
      $$(".srcs button",box).forEach(function(x){x.classList.remove("on");});
      btn.classList.add("on");
      try{localStorage.setItem("acts-tiles",btn.dataset.src);}catch(e){}
      tiles(map,box,btn.dataset.src);
    });
  });
  var play=$(".play-live",box);
  if(play) play.addEventListener("click",function(){runPlay(map,box);});
  setTimeout(function(){map.invalidateSize();},200);
}

function runPlay(map,box){
  var routes=map._routes||[];
  if(!routes.length){note(box,"这幅图没有可播放的路线。");return;}
  if(map._mover){map.removeLayer(map._mover); map._mover=null; if(map._raf) cancelAnimationFrame(map._raf);}
  var pts=[]; routes.forEach(function(r){pts=pts.concat(r.path);});
  var m=L.circleMarker(pts[0],{radius:9,color:"#fff",weight:2,fillColor:"#ff6b8b",fillOpacity:1}).addTo(map);
  map._mover=m;
  var i=0, t0=null, dur=Math.max(6000, pts.length*380);
  function segLen(){
    var Ltot=0, acc=[0];
    for(var k=1;k<pts.length;k++){
      var a=L.latLng(pts[k-1]), b=L.latLng(pts[k]);
      Ltot+=a.distanceTo(b); acc.push(Ltot);
    }
    return {Ltot:Ltot||1,acc:acc};
  }
  var S=segLen();
  function at(p){
    var d=p*S.Ltot;
    for(var k=1;k<S.acc.length;k++) if(S.acc[k]>=d){
      var t=(d-S.acc[k-1])/Math.max(1,S.acc[k]-S.acc[k-1]);
      var a=pts[k-1], b=pts[k];
      return [a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t];
    }
    return pts[pts.length-1];
  }
  function step(ts){
    if(!t0)t0=ts;
    var p=Math.min(1,(ts-t0)/dur);
    m.setLatLng(at(p));
    if(p<1) map._raf=requestAnimationFrame(step);
  }
  map._raf=requestAnimationFrame(step);
}

function safe(box){
  if(box._built) return;
  box._built=1;
  needL().then(function(){try{build(box);}catch(e){console.warn(e); var el=$(".lmap",box); if(el) el.innerHTML='<div class="mapfb">地图加载失败，请使用示意图。</div>';}})
    .catch(function(){var el=$(".lmap",box), cfg=(window.ACTS_MAPS||{})[box.dataset.map]; if(el) listFb(el,cfg||{}); note(box,"Leaflet 未加载，示意图仍可阅读。",1);});
}

/* 示意图动画仅在进入视口时运行 */
var cio=window.IntersectionObserver?new IntersectionObserver(function(es){
  es.forEach(function(en){
    var f=en.target, s=f.querySelector("svg");
    f.classList.toggle("run",en.isIntersecting);
    if(s&&s.pauseAnimations){en.isIntersecting?s.unpauseAnimations():s.pauseAnimations();}
  });
},{rootMargin:"40px 0px"}):null;

function init(){
  $$(".schematic svg").forEach(function(s){if(s.pauseAnimations)s.pauseAnimations();});
  if(cio) $$(".schematic").forEach(function(f){cio.observe(f);});
  var boxes=$$(".livebox[data-map]");
  if(!boxes.length) return;
  if(!("IntersectionObserver" in window)){boxes.forEach(safe);return;}
  var lastS=0,qT=0,q=[];
  addEventListener("scroll",function(){lastS=performance.now();},{passive:true});
  var pump=function(){
    qT=0; if(!q.length) return;
    var idle=performance.now()-lastS;
    if(idle<280){qT=setTimeout(pump,300-idle);return;}
    safe(q.shift());
    if(q.length) qT=setTimeout(pump,80);
  };
  var io=new IntersectionObserver(function(es){
    es.forEach(function(en){if(en.isIntersecting){io.unobserve(en.target);q.push(en.target);if(!qT)qT=setTimeout(pump,40);}});
  },{rootMargin:"240px 0px"});
  boxes.forEach(function(el){io.observe(el);});
}
window.__actsMapsInit=function(){$$(".livebox[data-map]").forEach(safe);};
if(document.readyState!=="loading") init(); else document.addEventListener("DOMContentLoaded",init);
var rz=0;
addEventListener("resize",function(){
  clearTimeout(rz); rz=setTimeout(function(){$$(".livebox").forEach(function(b){if(b._map)b._map.invalidateSize();});},200);
},{passive:true});
})();
