/* 使徒行传深读 GROKstudy v3.0.0 */
(function(){
"use strict";
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var html=document.documentElement,wide=function(){return innerWidth>1100};
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){}}
/* TOC: 3-level collapse, resize, scroll-spy, persist */
var toc=$('#toc');
var TOC_MIN=220, TOC_MAX=640, TOC_DEF=300;
function tocWide(){return innerWidth>1100}
function tocToggle(force){
  if(tocWide()){var off=force!==undefined?!force:!html.classList.contains('toc-off');html.classList.toggle('toc-off',off);store('acts-toc',off?'0':'1')}
  else{html.classList.toggle('toc-open',force!==undefined?force:!html.classList.contains('toc-open'))}
}
$('#tocbtn').addEventListener('click',function(){tocToggle()});
$('#tocx').addEventListener('click',function(){tocToggle(false)});
$('#scrim').addEventListener('click',function(){html.classList.remove('toc-open')});
$$('#toc a[href^="#"]').forEach(function(a){a.addEventListener('click',function(){if(!tocWide())html.classList.remove('toc-open')})});
document.addEventListener('keydown',function(e){
  if(/INPUT|TEXTAREA/.test(e.target.tagName))return;
  if(e.key==='t'||e.key==='T'){tocToggle()}
  if(e.key==='Escape'){html.classList.remove('toc-open');hidePop();var nd=$('#navdrop');if(nd)nd.classList.remove('open')}
});
function tocPageKey(){return 'acts-toc-fold:'+location.pathname.split('/').pop()}
function saveFold(){
  var o={};
  $$('#toc li[data-id]').forEach(function(li){if(li.classList.contains('is-collapsed'))o[li.dataset.id]=1});
  store(tocPageKey(),JSON.stringify(o));
}
function loadFold(){
  var raw=store(tocPageKey()), o=null;
  try{o=raw?JSON.parse(raw):null}catch(e){o=null}
  $$('#toc li[data-id]').forEach(function(li){
    var tw=$('.tw[data-for="'+li.dataset.id+'"]',li);
    if(!tw)return;
    var col;
    if(o) col=!!o[li.dataset.id];
    else col=li.classList.contains('tl2')&&!!li.closest('.toc-page')&&!!li.querySelector('.toc-kids');
    li.classList.toggle('is-collapsed',col);
    tw.setAttribute('aria-expanded',col?'false':'true');
  });
}
loadFold();
toc.addEventListener('click',function(e){
  var b=e.target.closest('.tw'); if(!b||!b.dataset.for)return;
  e.preventDefault();
  var li=toc.querySelector('li[data-id="'+b.dataset.for+'"]'); if(!li)return;
  var col=!li.classList.contains('is-collapsed');
  li.classList.toggle('is-collapsed',col);
  b.setAttribute('aria-expanded',col?'false':'true');
  saveFold();
});
function tocSetAll(expand, onlyLower){
  $$('#toc li[data-id]').forEach(function(li){
    if(onlyLower&&li.classList.contains('tl1')&&li.closest('.toc-page'))return;
    var tw=$('.tw[data-for="'+li.dataset.id+'"]',li); if(!tw)return;
    li.classList.toggle('is-collapsed',!expand);
    tw.setAttribute('aria-expanded',expand?'true':'false');
  });
  saveFold();
}
var ex=$('#toc-ex'),cl=$('#toc-cl');
if(ex)ex.addEventListener('click',function(){tocSetAll(true,false)});
if(cl)cl.addEventListener('click',function(){tocSetAll(false,true)});
$('#tocq').addEventListener('input',function(){
  var q=this.value.trim().toLowerCase();
  $$('#toc li[data-id], #toc li.leaf').forEach(function(li){
    if(!q){li.classList.remove('hid');return;}
    var child=li.textContent.toLowerCase().indexOf(q)>=0;
    li.classList.toggle('hid',!child);
    if(child){li.classList.remove('is-collapsed'); var tw=$('.tw[data-for]',li); if(tw)tw.setAttribute('aria-expanded','true');}
  });
});
function clampW(w){
  var cap=tocWide()?TOC_MAX:Math.min(TOC_MAX, Math.floor(innerWidth*0.9));
  return Math.max(TOC_MIN, Math.min(cap, Math.round(w)));
}
function applyW(w,persist){
  w=clampW(w); html.style.setProperty('--tocw',w+'px');
  var rz=$('#tocresizer'); if(rz)rz.setAttribute('aria-valuenow',String(w));
  if(persist!==false) store('acts-tocw',String(w));
  return w;
}
(function(){var w=store('acts-tocw'); if(w) applyW(+w,false);})();
(function bindResize(){
  var rz=$('#tocresizer'); if(!rz||!toc)return;
  var shell=$('#tocwrap')||toc;
  var startX=0,startW=0,dragging=false,pid=null;
  function widthNow(){return shell.getBoundingClientRect().width}
  function down(e){
    if(e.pointerType==='mouse'&&e.button!==0)return;
    e.preventDefault();
    dragging=true; pid=e.pointerId; startX=e.clientX; startW=widthNow();
    html.classList.add('toc-dragging');
    try{rz.setPointerCapture(e.pointerId)}catch(err){}
  }
  function move(e){ if(!dragging||(pid!==null&&e.pointerId!==pid))return; applyW(startW+(e.clientX-startX),false); }
  function up(e){ if(!dragging||(pid!==null&&e.pointerId!==pid))return; dragging=false; pid=null; html.classList.remove('toc-dragging'); applyW(widthNow(),true); try{rz.releasePointerCapture(e.pointerId)}catch(err){} }
  rz.addEventListener('pointerdown',down);
  rz.addEventListener('pointermove',move);
  rz.addEventListener('pointerup',up);
  rz.addEventListener('pointercancel',up);
  rz.addEventListener('dblclick',function(){applyW(TOC_DEF,true)});
  var lastTap=0;
  rz.addEventListener('pointerup',function(e){
    if(e.pointerType==='touch'||e.pointerType==='pen'){
      var now=Date.now(); if(now-lastTap<350){applyW(TOC_DEF,true); e.preventDefault();} lastTap=now;
    }
  });
  rz.addEventListener('keydown',function(e){
    var w=widthNow();
    if(e.key==='ArrowLeft'){e.preventDefault();applyW(w-16,true)}
    if(e.key==='ArrowRight'){e.preventDefault();applyW(w+16,true)}
    if(e.key==='Home'){e.preventDefault();applyW(TOC_MIN,true)}
    if(e.key==='End'){e.preventDefault();applyW(TOC_MAX,true)}
    if(e.key==='0'||e.key==='Enter'){e.preventDefault();applyW(TOC_DEF,true)}
  });
})();
/* scroll-spy via IntersectionObserver + light rAF for progress */
var pageLinks=$$('.toc-page a[href^="#"]'), prog=$('#prog'), topBtn=$('#totop'), ticking=false;
function expandAncestors(a){
  var li=a.closest('li[data-id]');
  while(li){
    if(li.classList.contains('is-collapsed')){
      li.classList.remove('is-collapsed');
      var tw=$('.tw[data-for="'+li.dataset.id+'"]',li);
      if(tw) tw.setAttribute('aria-expanded','true');
    }
    li=li.parentElement && li.parentElement.closest('li[data-id]');
  }
}
var currentAct=null;
function setAct(a){
  if(currentAct===a)return;
  if(currentAct)currentAct.classList.remove('act');
  currentAct=a;
  if(!a)return;
  a.classList.add('act');
  expandAncestors(a);
  if(tocWide()){
    var tr=toc.getBoundingClientRect(),ar=a.getBoundingClientRect();
    if(ar.top<tr.top+80||ar.bottom>tr.bottom-24) toc.scrollTop+=ar.top-tr.top-tr.height/3;
  }
}
if('IntersectionObserver' in window && pageLinks.length){
  var vis={};
  var ioSpy=new IntersectionObserver(function(es){
    es.forEach(function(en){vis[en.target.id]=en.isIntersecting?en.boundingClientRect.top:1e9;});
    var best=null,bestTop=1e9;
    pageLinks.forEach(function(a){
      var id=a.getAttribute('href').slice(1), el=document.getElementById(id);
      if(!el)return;
      var top=vis[id];
      if(top===undefined){var r=el.getBoundingClientRect(); top=r.top;}
      if(top<140 && 140-top<=bestTop){bestTop=140-top;best=a;}
    });
    if(!best){
      for(var i=0;i<pageLinks.length;i++){
        var el=document.getElementById(pageLinks[i].getAttribute('href').slice(1));
        if(el&&el.getBoundingClientRect().top>=0){best=pageLinks[i];break;}
      }
    }
    if(best)setAct(best);
  },{rootMargin:'-80px 0px -55% 0px',threshold:[0,.1,1]});
  pageLinks.forEach(function(a){var el=document.getElementById(a.getAttribute('href').slice(1)); if(el)ioSpy.observe(el);});
}
function onScrollLite(){
  var h=document.documentElement,sc=h.scrollTop||document.body.scrollTop,max=h.scrollHeight-h.clientHeight;
  if(prog)prog.style.width=(max>0?sc/max*100:0)+'%';
  if(topBtn)topBtn.classList.toggle('show',sc>600);
  ticking=false;
}
addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScrollLite)}},{passive:true});
onScrollLite();
if(topBtn)topBtn.addEventListener('click',function(){scrollTo({top:0,behavior:'smooth'})});

/* nav dropdown + theme */
$('#navbtn').addEventListener('click',function(e){e.stopPropagation();$('#navdrop').classList.toggle('open')});
document.addEventListener('click',function(e){if(!e.target.closest('#navdrop'))$('#navdrop').classList.remove('open')});
$('#themebtn').addEventListener('click',function(){var t=html.dataset.theme==='light'?'night':'light';html.dataset.theme=t;store('acts-theme',t)});
/* progress, scrollspy, totop */
var links=$$('#toc a'),heads=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))}),prog=$('#prog'),top=$('#totop'),ticking=false;
function onScroll(){
  var h=document.documentElement,sc=h.scrollTop||document.body.scrollTop,max=h.scrollHeight-h.clientHeight;
  prog.style.width=(max>0?sc/max*100:0)+'%';top.classList.toggle('show',sc>600);
  var cur=-1;for(var i=0;i<heads.length;i++){if(heads[i]&&heads[i].getBoundingClientRect().top<120)cur=i;else if(heads[i])break}
  links.forEach(function(a,i){a.classList.toggle('act',i===cur)});
  if(cur>=0&&wide()){var a=links[cur],tr=toc.getBoundingClientRect(),ar=a.getBoundingClientRect();if(ar.top<tr.top+60||ar.bottom>tr.bottom-20)toc.scrollTop+=ar.top-tr.top-tr.height/3}
  ticking=false;
}
addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScroll)}},{passive:true});onScroll();
top.addEventListener('click',function(){scrollTo({top:0,behavior:'smooth'})});
/* reveal */
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});
  $$('.reveal').forEach(function(el){io.observe(el)});
}else $$('.reveal').forEach(function(el){el.classList.add('in')});
/* verse popover */
var pop=null;
function hidePop(){if(pop){pop.remove();pop=null}}
document.addEventListener('click',function(e){
  var b=e.target.closest('.vs');
  if(!b){if(!e.target.closest('#pop'))hidePop();return}
  e.preventDefault();var same=pop&&pop._src===b;hidePop();if(same)return;
  pop=document.createElement('div');pop.id='pop';pop._src=b;pop.setAttribute('role','dialog');
  pop.textContent=b.dataset.t;var sm=document.createElement('small');sm.textContent='— '+b.textContent+'（和合本）';pop.appendChild(sm);
  document.body.appendChild(pop);
  var r=b.getBoundingClientRect(),pw=pop.offsetWidth,x=Math.min(Math.max(8,r.left+scrollX),scrollX+document.documentElement.clientWidth-pw-8),y=r.bottom+scrollY+8;
  if(r.bottom+pop.offsetHeight+16>innerHeight&&r.top>pop.offsetHeight+16)y=r.top+scrollY-pop.offsetHeight-8;
  pop.style.left=x+'px';pop.style.top=y+'px';
});
addEventListener('resize',hidePop);
/* flip cards */
document.addEventListener('click',function(e){var f=e.target.closest('.flip');if(f&&!e.target.closest('.vs'))f.classList.toggle('on')});
document.addEventListener('keydown',function(e){var f=e.target.closest&&e.target.closest('.flip');if(f&&(e.key==='Enter'||e.key===' ')){e.preventDefault();f.classList.toggle('on')}});
/* timeline filter */
$$('.tlf button').forEach(function(b){b.addEventListener('click',function(){
  $$('.tlf button').forEach(function(x){x.classList.toggle('on',x===b)});var f=b.dataset.f;
  $$('.tli').forEach(function(li){var show=f==='all'||(f==='ep'?li.classList.contains('ep'):li.classList.contains('c-'+f));li.classList.toggle('hid',!show);if(show)li.classList.add('in')});
})});
/* map */
var gm=$('.gmap');
if(gm){
  $$('.maptools .lb[data-l]').forEach(function(b){b.addEventListener('click',function(){b.classList.toggle('on');$$('.lyr[data-l="'+b.dataset.l+'"]',gm).forEach(function(g){g.classList.toggle('off',!b.classList.contains('on'))})})});
  var pl=$('#playroutes');if(pl)pl.addEventListener('click',function(){gm.classList.remove('playing');void gm.getBoundingClientRect();gm.classList.add('playing')});
  var info=$('#cityinfo');
  $$('.city[data-n]',gm).forEach(function(c){
    function sel(){$$('.city.sel',gm).forEach(function(x){x.classList.remove('sel')});c.classList.add('sel');var i=c.dataset.i;info.innerHTML='';var b=document.createElement('b');b.textContent='📍 '+c.dataset.n+'：';info.appendChild(b);info.appendChild(document.createTextNode(i?i:'与书信写作/收信无直接关系，是行程中的城市。'))}
    c.addEventListener('click',sel);c.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();sel()}});
  });
}
/* creed recite modes */
$$('.recite').forEach(function(r){
  var body=$('.rbody',r);
  $$('.rmodes button',r).forEach(function(b){b.addEventListener('click',function(){
    var m=b.dataset.m;
    if(m==='big'){b.classList.toggle('on');body.classList.toggle('big');return}
    if(m==='tts'){var ss=window.speechSynthesis;if(!ss){b.textContent='🔇 不支持朗读';return}
      if(ss.speaking){ss.cancel();b.classList.remove('on');b.textContent='🔊 朗读';return}
      var txt=$$('.rt',body).map(function(x){return x.dataset.o||x.textContent}).join('');var u=new SpeechSynthesisUtterance(txt);u.lang='zh-CN';u.rate=.9;
      var v=ss.getVoices().filter(function(x){return /zh/i.test(x.lang)})[0];if(v)u.voice=v;
      u.onend=u.onerror=function(){b.classList.remove('on');b.textContent='🔊 朗读'};b.classList.add('on');b.textContent='⏹ 停止';ss.speak(u);return}
    $$('.rmodes button:not([data-m=big]):not([data-m=tts])',r).forEach(function(x){x.classList.toggle('on',x===b)});
    body.classList.remove('hint','hide');$$('.rt.show',body).forEach(function(x){x.classList.remove('show')});
    $$('.rt',body).forEach(function(x){if(x.dataset.o){x.textContent=x.dataset.o;delete x.dataset.o}});
    if(m==='hint'){body.classList.add('hint');$$('.rt',body).forEach(function(x){var t=x.textContent;x.dataset.o=t;var k=t.replace(/^\d+\)\s*/,'');var pre=t.slice(0,t.length-k.length);x.innerHTML='';x.appendChild(document.createTextNode(pre));var s=document.createElement('b');s.className='hint1';s.textContent=k.charAt(0);x.appendChild(s);x.appendChild(document.createTextNode(k.slice(1)))})}
    if(m==='hide')body.classList.add('hide');
  })});
  body.addEventListener('click',function(e){var t=e.target.closest('.rt');if(t&&(body.classList.contains('hint')||body.classList.contains('hide')))t.classList.toggle('show')});
});
/* memory page */
var dEl=$('#epdata');
if(dEl){
  var D=JSON.parse(dEl.textContent);
  var shuffle=function(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a};
  var fc=$('#fcards');
  $('#fcshuf').addEventListener('click',function(){shuffle($$('.flip',fc)).forEach(function(c){fc.appendChild(c)})});
  $('#fcall').addEventListener('click',function(){$$('.flip.on',fc).forEach(function(c){c.classList.remove('on')})});
  /* cloze */
  var cz=$('#cloze');
  shuffle(D).slice(0,6).forEach(function(d){
    var t=d.kvt,cands=['圣灵','耶稣','神','主','见证','罗马','耶路撒冷','外邦人','教会','道','复活','恩','光明','异象','放心','锁链','百姓','救恩','能力','悔改'].filter(function(w){return t.indexOf(w)>=0});
    var w=cands.length?cands[Math.floor(Math.random()*cands.length)]:t.slice(2,4),i=t.indexOf(w);
    var row=document.createElement('div');row.className='cz2';var p=document.createElement('p');
    p.appendChild(document.createTextNode(t.slice(0,i)));var g=document.createElement('span');g.className='gap';g.textContent=w;p.appendChild(g);p.appendChild(document.createTextNode(t.slice(i+w.length)));
    var s=document.createElement('small');s.textContent='— '+d.kv;var b=document.createElement('button');b.className='btn';b.textContent='显示';b.addEventListener('click',function(){row.classList.toggle('rev')});
    row.appendChild(p);row.appendChild(s);row.appendChild(b);cz.appendChild(row);
  });
  /* quiz */
  var kinds=[
    function(d){return{q:'使徒行传'+d.n+'的钥字是？',a:d.kw,o:D.map(function(x){return x.kw})}},
    function(d){return{q:'“'+d.kvt.slice(0,40)+(d.kvt.length>40?'……':'')+'” 出自使徒行传哪一章？',a:d.n,o:D.map(function(x){return x.n})}},
    function(d){return{q:d.n+'：主要发生在哪里？',a:d.place,o:D.map(function(x){return x.place}),p:1}},
    function(d){return{q:'记忆钩“'+d.mn.slice(0,34)+(d.mn.length>34?'……':'')+'”对应哪一章？',a:d.n,o:D.map(function(x){return x.n})}}
  ];
  var qi=0,sc=0,cur=null,done=false,ord=[];
  function newQ(){
    if(!ord.length)ord=shuffle(D);var d=ord.pop();var k=kinds[Math.floor(Math.random()*kinds.length)](d);
    var opts=shuffle(k.o.filter(function(x,i,a){return x!==k.a&&a.indexOf(x)===i&&!(k.p&&x.slice(0,2)===k.a.slice(0,2))})).slice(0,3);opts.push(k.a);cur=k;done=false;
    $('#qzn').textContent='第 '+(++qi)+' 题';$('#qzq').textContent=k.q;$('#qzf').textContent='';var o=$('#qzo');o.innerHTML='';
    shuffle(opts).forEach(function(t){var b=document.createElement('button');b.textContent=t;b.addEventListener('click',function(){if(done)return;done=true;var ok=t===k.a;if(ok)sc++;b.classList.add(ok?'ok':'no');$$('button',o).forEach(function(x){if(x.textContent===k.a)x.classList.add('ok')});$('#qzs').textContent='得分 '+sc+' / '+qi;$('#qzf').textContent=ok?'✅ 正确！':'❌ 正确答案：'+k.a});o.appendChild(b)});
  }
  $('#qznext').addEventListener('click',newQ);$('#qzre').addEventListener('click',function(){qi=0;sc=0;ord=[];$('#qzs').textContent='得分 0';newQ()});newQ();
  /* plan */
  var saved={};try{saved=JSON.parse(store('acts-plan')||'{}')}catch(e){}
  $$('#plan input').forEach(function(c){c.checked=!!saved[c.dataset.d];c.addEventListener('change',function(){saved[c.dataset.d]=c.checked;store('acts-plan',JSON.stringify(saved))})});
}
/* draw svg in twoage */
$$('.twoage').forEach(function(f){var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){$$('.draw',f).forEach(function(d){d.classList.add('in')});o.disconnect()}})});o.observe(f)});
/* prefetch next pages on hover/idle for snappy switches */
function prefetch(href){
  if(!href||href.charAt(0)==='#'||/^(https?:|mailto:|javascript:)/i.test(href))return;
  href=href.split('#')[0]; if(!href)return;
  if(document.querySelector('link[rel="prefetch"][href="'+href+'"]'))return;
  var l=document.createElement('link'); l.rel='prefetch'; l.as='document'; l.href=href; document.head.appendChild(l);
}
document.addEventListener('pointerover',function(e){
  var a=e.target.closest&&e.target.closest('a[href]'); if(a)prefetch(a.getAttribute('href'));
},true);
(function(){
  var idle=window.requestIdleCallback||function(f){setTimeout(f,400)};
  idle(function(){ $$('.pn a, .toc-site a, .mainnav a').forEach(function(a){prefetch(a.getAttribute('href'))}); });
})();
})();
