# -*- coding: utf-8 -*-
"""交互脚本：主题三态、目录滚动高亮（rAF + getBoundingClientRect）、检索、十诫面板、
52 主日地图、闪卡（遮答／首字／打乱／标记／筛选）。"""

JS = r"""
(function(){
'use strict';
var $=function(s,r){return (r||document).querySelector(s)};
var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var LS={get:function(k,d){try{var v=localStorage.getItem(k);return v===null?d:v}catch(e){return d}},
        set:function(k,v){try{localStorage.setItem(k,v)}catch(e){}}};

/* ---------- 主题三态 ---------- */
var THEMES=['auto','light','dark'], THLABEL={auto:'主题 · 跟随系统',light:'主题 · 浅色',dark:'主题 · 深色'};
function applyTheme(t){
  var mq=window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches;
  var eff=(t==='auto')?(mq?'dark':'light'):t;
  document.documentElement.setAttribute('data-theme',eff);
  document.documentElement.setAttribute('data-theme-mode',t);
  var b=$('#themeBtn'); if(b){b.textContent=THLABEL[t]}
}
var curTheme=LS.get('wlc-theme','auto');
applyTheme(curTheme);
if(LS.get('wlc-toc','on')==='off'){
  document.addEventListener('DOMContentLoaded',function(){
    document.body.classList.add('tocOff');
    var tb=document.getElementById('tocBtn');
    if(tb){tb.textContent='显示目录';tb.setAttribute('aria-pressed','true')}
  });
}
if(window.matchMedia){try{window.matchMedia('(prefers-color-scheme: dark)')
  .addEventListener('change',function(){if(curTheme==='auto')applyTheme('auto')})}catch(e){}}

/* ---------- 目录滚动高亮 ---------- */
var links=$$('.toc a[href^="#"]'), targets=[];
links.forEach(function(a){var el=document.getElementById(a.getAttribute('href').slice(1)); if(el)targets.push({a:a,el:el})});
var ticking=false,lastActive=null;
function spy(){
  ticking=false;
  var best=null,bestTop=-1e9,probe=90;
  for(var i=0;i<targets.length;i++){
    var t=targets[i].el.getBoundingClientRect().top;
    if(t<=probe && t>bestTop){bestTop=t;best=targets[i]}
  }
  if(!best && targets.length)best=targets[0];
  if(best && best.a!==lastActive){
    if(lastActive)lastActive.classList.remove('active');
    best.a.classList.add('active');lastActive=best.a;
    var sb=$('#sidebar');
    if(sb && sb.scrollHeight>sb.clientHeight && window.innerWidth>1000){
      var r=best.a.getBoundingClientRect(), sr=sb.getBoundingClientRect();
      if(r.top<sr.top+30||r.bottom>sr.bottom-30){sb.scrollTop+=r.top-sr.top-sb.clientHeight/2.6}
    }
  }
}
function onScroll(){if(!ticking){ticking=true;requestAnimationFrame(spy)}}
window.addEventListener('scroll',onScroll,{passive:true});
window.addEventListener('resize',onScroll,{passive:true});

/* ---------- 抽屉目录 ---------- */
function closeDrawer(){var s=$('#sidebar'),c=$('#scrim');if(s)s.classList.remove('open');if(c)c.classList.remove('show')}
document.addEventListener('click',function(e){
  var t=e.target.closest?e.target.closest('[data-act]'):null;
  if(!t)return;
  var act=t.getAttribute('data-act');
  if(act==='menu'){var s=$('#sidebar'),c=$('#scrim');s.classList.toggle('open');c.classList.toggle('show')}
  else if(act==='scrim'){closeDrawer()}
  else if(act==='theme'){var i=THEMES.indexOf(curTheme);curTheme=THEMES[(i+1)%3];LS.set('wlc-theme',curTheme);applyTheme(curTheme)}
  else if(act==='print'){window.print()}
  else if(act==='expand'){var on=t.getAttribute('aria-pressed')!=='true';
    $$('details.unit').forEach(function(d){d.open=on});t.setAttribute('aria-pressed',String(on));
    t.textContent=on?'全部收起':'全部展开'}
  else if(act==='top'){window.scrollTo({top:0,behavior:'smooth'})}
  else if(act==='toc'){
    var off=!document.body.classList.contains('tocOff');
    document.body.classList.toggle('tocOff',off);
    LS.set('wlc-toc',off?'off':'on');
    var tb=$('#tocBtn'); if(tb){tb.textContent=off?'显示目录':'隐藏目录';tb.setAttribute('aria-pressed',String(off))}
    setTimeout(onScroll,60);
  }
});
$$('.toc a').forEach(function(a){a.addEventListener('click',function(){if(window.innerWidth<=1000)closeDrawer()})});

/* ---------- 回到顶部 ---------- */
var tt=$('#toTop');
window.addEventListener('scroll',function(){if(tt){tt.classList.toggle('show',window.scrollY>700)}},{passive:true});

/* ---------- 196 问检索 ---------- */
var qaNodes=null;
function initSearch(){
  var inp=$('#qsearch'); if(!inp)return;
  qaNodes=$$('.qa').map(function(n){return {n:n,t:n.textContent,html:n.innerHTML}});
  var cnt=$('#qcount');
  function esc(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}
  function run(){
    var v=inp.value.trim();
    if(!v){qaNodes.forEach(function(o){o.n.innerHTML=o.html;o.n.style.display=''});
      $$('details.unit').forEach(function(d){d.style.display=''});
      cnt.textContent='共 196 问';return}
    var re=new RegExp(esc(v),'gi'),hit=0;
    qaNodes.forEach(function(o){
      if(re.test(o.t)){o.n.style.display='';hit++;
        o.n.innerHTML=o.html.replace(new RegExp('(?![^<]*>)'+esc(v),'gi'),function(m){return '<mark>'+m+'</mark>'});
      } else {o.n.style.display='none';o.n.innerHTML=o.html}
      re.lastIndex=0;
    });
    $$('details.unit').forEach(function(d){
      var any=$$('.qa',d).some(function(x){return x.style.display!=='none'});
      d.style.display=any?'':'none'; if(any)d.open=true;
    });
    cnt.textContent='命中 '+hit+' 问';
  }
  inp.addEventListener('input',run);
  var clr=$('#qclear'); if(clr)clr.addEventListener('click',function(){inp.value='';run();inp.focus()});
}

/* ---------- 十诫面板 ---------- */
function initDeca(){
  var wrap=$('#decaBtns'),panel=$('#decaPanel'); if(!wrap||!panel||!window.DECA)return;
  function render(i){
    var d=window.DECA[i];
    panel.innerHTML='<div class="box gold"><span class="lbl">第 '+d.no+' 诫 · 问 '+d.q+'</span>'+
      '<p><b>诫命</b>　'+d.text+'</p>'+
      '<p><b>所要求的</b>　'+d.req+'</p>'+
      '<p><b>所禁止的</b>　'+d.forb+'</p>'+
      (d.why?'<p><b>加重的理由</b>　'+d.why+'</p>':'')+
      '<p><b>欧陆对读</b>　'+d.hc+'</p></div>';
    $$('button',wrap).forEach(function(b,j){b.setAttribute('aria-pressed',String(j===i))});
  }
  window.DECA.forEach(function(d,i){
    var b=document.createElement('button');
    b.innerHTML='<i>'+d.no+'　问 '+d.q+'</i>'+d.name;
    b.setAttribute('aria-pressed','false');
    b.addEventListener('click',function(){render(i)});
    wrap.appendChild(b);
  });
  render(0);
}

/* ---------- 52 主日地图 ---------- */
function initLD(){
  var wrap=$('#ldBtns'),panel=$('#ldPanel'); if(!wrap||!panel||!window.LORDSDAYS)return;
  function render(i){
    var d=window.LORDSDAYS[i],sec={g:'苦',d:'救',t:'谢'}[d.s];
    var cls=d.s==='g'?'crim':(d.s==='d'?'':'green');
    panel.innerHTML='<div class="box '+cls+'"><span class="lbl">主日 '+d.n+' · 问 '+d.q+' · '+
      ({g:'第一部分　人的困苦',d:'第二部分　人的拯救',t:'第三部分　人的感恩'}[d.s])+'</span>'+
      '<p><b>'+d.t+'</b></p><p>'+d.c+'</p>'+
      (d.w?'<p class="note">威敏对应：'+d.w+'</p>':'')+'</div>';
    $$('button',wrap).forEach(function(b,j){b.setAttribute('aria-pressed',String(j===i))});
  }
  window.LORDSDAYS.forEach(function(d,i){
    var b=document.createElement('button');
    b.textContent=d.n; b.title='主日'+d.n+'：'+d.t; b.setAttribute('data-sec',d.s);
    b.setAttribute('aria-pressed','false');
    b.addEventListener('click',function(){render(i)});
    wrap.appendChild(b);
  });
  render(0);
}

/* ---------- 闪卡引擎（支持多副牌） ---------- */
function initFC(prefix, deckData, storeKey){
  var host=$('#'+prefix+'Card'); if(!host||!deckData)return;
  var all=deckData.slice(), deck=all.slice(), idx=0, revealed=false, hinted=false;
  var doneSet={}; try{doneSet=JSON.parse(LS.get(storeKey,'{}'))||{}}catch(e){doneSet={}}
  var filter='all';
  function firstChars(s){
    var plain=s.replace(/<[^>]*>/g,'');
    return plain.split(/[，。；：、？！…\s]+/).filter(Boolean).map(function(seg){
      return seg.charAt(0)+'○'.repeat(Math.max(0,Math.min(seg.length-1,6)));
    }).join(' · ');
  }
  function applyFilter(){
    deck=all.filter(function(c){
      if(filter==='all')return true;
      if(filter==='todo')return !doneSet[c.id];
      return c.g===filter;
    });
    if(!deck.length)deck=all.slice();
    idx=0;revealed=false;hinted=false;draw();
  }
  function draw(){
    var c=deck[idx]; if(!c)return;
    host.className='fc rippleHost'+(doneSet[c.id]?' done':'');
    host.innerHTML='<div class="tag">'+c.tag+'</div><div class="q">'+c.q+'</div>'+
      '<div class="a'+(revealed?'':' hidden')+'">'+c.a+'</div>'+
      (hinted&&!revealed?'<div class="hint">'+firstChars(c.a)+'</div>':'');
    var p=$('#'+prefix+'Prog'); if(p){
      var done=deck.filter(function(x){return doneSet[x.id]}).length;
      p.textContent=(idx+1)+' / '+deck.length+'　已标记背熟 '+done+' 张';
    }
    var mk=$('#'+prefix+'Mark'); if(mk)mk.textContent=doneSet[c.id]?'取消背熟':'标记背熟';
  }
  function go(d){idx=(idx+d+deck.length)%deck.length;revealed=false;hinted=false;draw()}
  host.addEventListener('click',function(){revealed=!revealed;draw()});
  $('#'+prefix+'Prev').addEventListener('click',function(){go(-1)});
  $('#'+prefix+'Next').addEventListener('click',function(){go(1)});
  $('#'+prefix+'Flip').addEventListener('click',function(){revealed=!revealed;draw()});
  $('#'+prefix+'Hint').addEventListener('click',function(){hinted=!hinted;draw()});
  $('#'+prefix+'Shuffle').addEventListener('click',function(){
    for(var i=deck.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=deck[i];deck[i]=deck[j];deck[j]=t}
    idx=0;revealed=false;hinted=false;draw();
  });
  $('#'+prefix+'Mark').addEventListener('click',function(){
    var c=deck[idx]; if(doneSet[c.id])delete doneSet[c.id]; else doneSet[c.id]=1;
    LS.set(storeKey,JSON.stringify(doneSet));draw();
  });
  $$('#'+prefix+'Filter button').forEach(function(b){
    b.addEventListener('click',function(){
      filter=b.getAttribute('data-f');
      $$('#'+prefix+'Filter button').forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});
      applyFilter();
    });
  });
  document.addEventListener('keydown',function(e){
    if(/input|textarea|select/i.test((e.target.tagName||'')))return;
    var r=host.getBoundingClientRect();
    if(r.top>window.innerHeight-60||r.bottom<60)return;
    if(e.key==='ArrowRight'){go(1)}
    else if(e.key==='ArrowLeft'){go(-1)}
    else if(e.key===' '){e.preventDefault();revealed=!revealed;draw()}
  });
  applyFilter();
}

/* ---------- 君王面板 ---------- */
function initMon(){
  var wrap=$('#monBtns'),panel=$('#monPanel'); if(!wrap||!panel||!window.MONARCHS)return;
  var CL={r:'crim',p:'green',m:'gold',h:'',i:''};
  function render(i){
    var m=window.MONARCHS[i];
    panel.innerHTML='<div class="box '+CL[m.c]+'"><span class="lbl">第 '+m.n+' 朝 · '+m.house+' · '+m.a+'–'+m.b+'</span>'+
      '<p style="font-size:1.05rem"><b>'+m.name+'</b>　<span class="lt">'+m.en+'</span>　<span class="pill g">'+m.hook+'</span></p>'+
      '<p><b>教会政策</b>　'+m.policy+'</p>'+
      '<p><b>关键事件</b>　'+m.event+'</p>'+
      '<p><b>与威敏准则的关系</b>　'+m.wlc+'</p></div>';
    $$('button',wrap).forEach(function(b,j){b.setAttribute('aria-pressed',String(j===i))});
  }
  window.MONARCHS.forEach(function(m,i){
    var b=document.createElement('button');
    b.className='rippleHost';
    b.setAttribute('data-c',m.c); b.setAttribute('aria-pressed','false');
    b.innerHTML='<i>'+m.a+'–'+m.b+'</i>'+m.name;
    b.addEventListener('click',function(){render(i)});
    wrap.appendChild(b);
  });
  render(0);
}

/* ---------- 时间轴拖动器 ---------- */
function initScrub(){
  var rg=$('#scRange'),ye=$('#scYear'),er=$('#scEra'),ou=$('#scOut'),bar=$('#scBar');
  if(!rg||!window.EVENTS||!window.ERAS)return;
  var LN={c:['欧陆','c'],e:['英格兰','e'],s:['苏格兰','s']};
  var MIN=1517,MAX=1800;
  window.EVENTS.forEach(function(v){
    if(!v.m)return;
    var i=document.createElement('i'); i.className='m';
    i.style.left=((v.y-MIN)/(MAX-MIN)*100)+'%'; i.title=v.y+' '+v.t; bar.appendChild(i);
  });
  function render(){
    var y=parseInt(rg.value,10);
    ye.textContent=y;
    var e=null;
    for(var i=0;i<window.ERAS.length;i++){var x=window.ERAS[i]; if(y>=x.a&&y<=x.b){e=x;break}}
    er.innerHTML=e?('<b>'+e.t+'</b>　'+e.d):'';
    var near=window.EVENTS.filter(function(v){return Math.abs(v.y-y)<=4})
                          .sort(function(a,b){return a.y-b.y||a.l.localeCompare(b.l)});
    if(!near.length){ou.innerHTML='<div class="none">这四年前后没有记录在案的节点——把滑块拖向金色刻度试试。</div>';return}
    ou.innerHTML=near.slice(0,7).map(function(v){
      return '<div class="ev '+v.l+'"><span class="y">'+v.y+'</span><span class="l">'+LN[v.l][0]+
             '</span><span>'+v.t+'</span></div>';
    }).join('');
  }
  rg.addEventListener('input',render);
  render();
}

/* ---------- 阅读进度条 ---------- */
function initProgress(){
  var bar=$('#progressBar'); if(!bar)return;
  function upd(){
    var h=document.documentElement.scrollHeight-window.innerHeight;
    bar.style.width=(h>0?Math.min(100,window.scrollY/h*100):0)+'%';
  }
  window.addEventListener('scroll',upd,{passive:true});
  window.addEventListener('resize',upd,{passive:true});
  upd();
}

/* ---------- 水波涟漪 ---------- */
function initRipple(){
  if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var RIPPLE_SEL='.btn,.fc,.lds button,.deca button,.mon button,.unit>summary,.mini,.tocFab,.toTop';
  document.addEventListener('pointerdown',function(e){
    var t=e.target.closest?e.target.closest(RIPPLE_SEL):null;
    if(t){
      t.classList.add('rippleHost');
      var r=t.getBoundingClientRect(), d=Math.max(r.width,r.height)*2.1;
      var s=document.createElement('span');
      s.className='rp';
      s.style.cssText='width:'+d+'px;height:'+d+'px;left:'+(e.clientX-r.left)+'px;top:'+(e.clientY-r.top)+'px';
      t.appendChild(s);
      setTimeout(function(){s.remove()},640);
      return;
    }
    // 正文空白处：水面扩散环
    if(!e.target.closest('main')&&!e.target.closest('header'))return;
    if(e.target.closest('a,input,table,svg'))return;
    for(var k=0;k<2;k++){
      var ring=document.createElement('div');
      ring.className='wave-ring'+(k?' b':'');
      var size=k?300:210;
      ring.style.cssText='width:'+size+'px;height:'+size+'px;left:'+e.clientX+'px;top:'+e.clientY+'px';
      document.body.appendChild(ring);
      (function(el){setTimeout(function(){el.remove()},1350)})(ring);
    }
  },{passive:true});
}

function boot(){
  initSearch();initDeca();initLD();initMon();initScrub();initProgress();initRipple();
  initFC('fc',window.CARDS,'wlc-fc-done');
  initFC('hc',window.HCARDS,'wlc-hc-done');
  spy();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
"""
