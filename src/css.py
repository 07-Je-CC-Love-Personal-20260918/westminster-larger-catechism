# -*- coding: utf-8 -*-
"""全站样式：沿用本项目 HTML house style（羊皮纸／深蓝／绛红／金，无外部字体请求）。"""

CSS = r"""
:root{
  --ink:#1d1a16; --ink-2:#4a423a; --ink-3:#6f6458;
  --bg:#f6f1e4; --bg-2:#fbf8f0; --card:#fffdf7; --line:#ded1b6; --line-2:#eadfc7;
  --navy:#1f3a5f; --navy-2:#2d5183; --navy-soft:#e7edf5;
  --crimson:#8c2f39; --crimson-soft:#f7e9e9;
  --gold:#a9812f; --gold-2:#c9a227; --gold-soft:#f6eed8;
  --green:#2f5d4a; --green-soft:#e6efe9;
  --shadow:0 1px 2px rgba(60,45,20,.06),0 8px 24px rgba(60,45,20,.07);
  --radius:10px;
  --serif:"EB Garamond","Cormorant Garamond",Garamond,"Times New Roman",Georgia,serif;
  --display:"Cinzel","Trajan Pro","EB Garamond",Georgia,serif;
  --cn:"Noto Serif SC","Source Han Serif SC","Songti SC",SimSun,"Segoe UI",serif;
  --mono:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace;
  --maxw:1320px; --sbw:306px;
}
html[data-theme="dark"]{
  --ink:#e9e2d4; --ink-2:#c5bba7; --ink-3:#9a9081;
  --bg:#15171c; --bg-2:#1a1d23; --card:#1e2229; --line:#343a45; --line-2:#2a2f38;
  --navy:#9dc0ea; --navy-2:#b7d2f3; --navy-soft:#1c2634;
  --crimson:#e59aa2; --crimson-soft:#2c1d20;
  --gold:#dbb45c; --gold-2:#e9c977; --gold-soft:#2b2519;
  --green:#8fc6ac; --green-soft:#18241f;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 26px rgba(0,0,0,.32);
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:78px;-webkit-text-size-adjust:100%}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}
body{
  margin:0;background:var(--bg);color:var(--ink);
  font-family:var(--cn);font-size:16.5px;line-height:1.95;
  overflow-x:hidden;
  background-image:
    radial-gradient(circle at 12% 8%, rgba(169,129,47,.055), transparent 42%),
    radial-gradient(circle at 88% 22%, rgba(31,58,95,.05), transparent 46%),
    radial-gradient(circle at 50% 92%, rgba(140,47,57,.04), transparent 52%);
  background-attachment:fixed;
}
img,svg{max-width:100%}
a{color:var(--navy-2);text-decoration:none;border-bottom:1px solid rgba(45,81,131,.3)}
a:hover{border-bottom-color:var(--navy-2)}
:focus-visible{outline:2.5px solid var(--gold-2);outline-offset:2px;border-radius:3px}

/* ---------- 顶栏 ---------- */
.topbar{
  position:sticky;top:0;z-index:60;display:flex;align-items:center;gap:.6rem;
  padding:.5rem clamp(.7rem,2vw,1.4rem);
  background:color-mix(in srgb,var(--bg) 88%,transparent);
  backdrop-filter:saturate(1.3) blur(9px);
  border-bottom:1px solid var(--line);
}
.topbar .brand{font-family:var(--display);letter-spacing:.06em;font-size:.93rem;color:var(--navy);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.topbar .brand b{color:var(--crimson);font-weight:600}
.spacer{flex:1}
.btn{
  font-family:var(--cn);font-size:.8rem;line-height:1;padding:.5rem .7rem;cursor:pointer;
  background:var(--card);color:var(--ink-2);border:1px solid var(--line);border-radius:7px;
  transition:background .15s,color .15s,border-color .15s;white-space:nowrap;
}
.btn:hover{border-color:var(--gold);color:var(--ink)}
.btn[aria-pressed="true"]{background:var(--gold-soft);border-color:var(--gold);color:var(--ink)}
.menu-btn{display:none}

/* ---------- 布局 ---------- */
.shell{max-width:var(--maxw);margin:0 auto;display:grid;grid-template-columns:var(--sbw) minmax(0,1fr);gap:clamp(1rem,2.4vw,2.4rem);padding:0 clamp(.8rem,2vw,1.6rem) 5rem}
.sidebar{position:sticky;top:60px;align-self:start;max-height:calc(100vh - 72px);overflow-y:auto;padding:1.1rem .4rem 2rem 0;scrollbar-width:thin}
.sidebar h2{font-family:var(--display);font-size:.74rem;letter-spacing:.16em;color:var(--ink-3);margin:.2rem 0 .7rem;font-weight:600}
.toc{list-style:none;margin:0;padding:0;font-size:.845rem;line-height:1.55}
.toc li{margin:.06rem 0}
.toc a{display:block;padding:.3rem .55rem;border-radius:6px;color:var(--ink-2);border:0;border-left:2.5px solid transparent}
.toc a:hover{background:var(--bg-2);color:var(--ink)}
.toc a.active{background:var(--navy-soft);color:var(--navy);border-left-color:var(--gold-2);font-weight:600}
.toc .lv1{margin-top:.85rem;border-top:1px solid var(--line-2);padding-top:.5rem}
.toc .lv1>a{font-family:var(--display);letter-spacing:.05em;font-size:.79rem;color:var(--crimson);font-weight:600;padding:.28rem .55rem}
.toc .lv1>a:hover{background:var(--crimson-soft)}
.toc .lv1>a.active{background:var(--crimson-soft);color:var(--crimson);border-left-color:var(--crimson)}
.toc .lv3 a{padding-left:1.35rem;font-size:.8rem;color:var(--ink-3)}
main{min-width:0;padding-top:1.3rem}

/* ---------- 标题与排版 ---------- */
.hero{text-align:center;padding:3.2rem 1rem 2.2rem;border-bottom:2px solid var(--line);margin-bottom:2.2rem;position:relative}
.hero::after{content:"";position:absolute;left:50%;bottom:-6px;transform:translateX(-50%);width:86px;height:10px;background:var(--bg);
  border-left:1px solid var(--line);border-right:1px solid var(--line);border-bottom:2px solid var(--line)}
.hero .eyebrow{font-family:var(--display);font-size:.72rem;letter-spacing:.3em;color:var(--gold);margin-bottom:1rem}
.hero h1{font-family:var(--cn);font-weight:700;font-size:clamp(1.75rem,5.2vw,3rem);line-height:1.32;margin:.2rem 0 .5rem;color:var(--navy);letter-spacing:.03em}
.hero .lat{font-family:var(--display);font-size:clamp(.72rem,2vw,.92rem);letter-spacing:.13em;color:var(--crimson);margin-bottom:1.1rem}
.hero .sub{max-width:44rem;margin:0 auto;color:var(--ink-2);font-size:.96rem}
.hero .meta{margin-top:1.4rem;display:flex;flex-wrap:wrap;gap:.45rem;justify-content:center}
.pill{font-size:.73rem;padding:.26rem .66rem;border-radius:999px;background:var(--card);border:1px solid var(--line);color:var(--ink-3)}
.pill.g{background:var(--gold-soft);border-color:var(--gold);color:var(--gold)}
.pill.n{background:var(--navy-soft);border-color:var(--navy-2);color:var(--navy)}
.pill.c{background:var(--crimson-soft);border-color:var(--crimson);color:var(--crimson)}

.part{margin:3.6rem 0 1.6rem;padding:1.5rem 0 .9rem;border-top:3px double var(--line);border-bottom:1px solid var(--line-2)}
.part .num{font-family:var(--display);font-size:.73rem;letter-spacing:.3em;color:var(--gold)}
.part h2{font-size:clamp(1.35rem,3.6vw,1.9rem);margin:.35rem 0 .45rem;color:var(--crimson);font-weight:700;letter-spacing:.02em}
.part p{margin:0;color:var(--ink-3);font-size:.9rem}
h3{font-size:clamp(1.08rem,2.6vw,1.32rem);margin:2.3rem 0 .75rem;color:var(--navy);font-weight:700;padding-left:.7rem;border-left:4px solid var(--gold-2);line-height:1.5}
h4{font-size:1rem;margin:1.5rem 0 .5rem;color:var(--ink);font-weight:700}
p{margin:.72rem 0}
ul,ol{padding-left:1.3rem;margin:.6rem 0}
li{margin:.3rem 0}
b,strong{color:var(--crimson);font-weight:700}
em{font-style:normal;color:var(--navy);font-weight:600}
.lt{font-family:var(--serif);font-style:italic;color:var(--navy-2);letter-spacing:.01em}
.note{font-size:.87rem;color:var(--ink-3)}
hr{border:0;border-top:1px solid var(--line-2);margin:2rem 0}

/* ---------- 卡片／方框 ---------- */
.box{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--navy);border-radius:var(--radius);padding:1rem 1.15rem;margin:1.1rem 0;box-shadow:var(--shadow)}
.box.gold{border-left-color:var(--gold-2);background:var(--gold-soft)}
.box.crim{border-left-color:var(--crimson);background:var(--crimson-soft)}
.box.green{border-left-color:var(--green);background:var(--green-soft)}
.box .lbl{font-family:var(--display);font-size:.68rem;letter-spacing:.2em;color:var(--ink-3);display:block;margin-bottom:.35rem}
.box p:first-of-type{margin-top:0}.box p:last-child{margin-bottom:0}
.grid{display:grid;gap:.9rem;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));margin:1.1rem 0}
.grid.tri{grid-template-columns:repeat(auto-fit,minmax(min(220px,100%),1fr))}
.mini{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:.85rem 1rem;box-shadow:var(--shadow)}
.mini h5{margin:0 0 .35rem;font-size:.93rem;color:var(--navy);font-weight:700}
.mini p{margin:.25rem 0;font-size:.875rem;color:var(--ink-2)}
.quote{font-family:var(--cn);border-left:3px solid var(--gold-2);padding:.15rem 0 .15rem .95rem;margin:1rem 0;color:var(--ink-2);font-size:.93rem}
.quote cite{display:block;font-style:normal;font-size:.79rem;color:var(--ink-3);margin-top:.3rem}

/* ---------- 表格 ---------- */
.tablewrap{overflow-x:auto;margin:1.2rem 0;border:1px solid var(--line);border-radius:var(--radius);background:var(--card);box-shadow:var(--shadow);-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;min-width:520px;font-size:.855rem}
caption{caption-side:top;text-align:left;padding:.7rem .9rem .1rem;font-size:.82rem;color:var(--ink-3)}
th,td{padding:.55rem .7rem;border-bottom:1px solid var(--line-2);text-align:left;vertical-align:top;line-height:1.6}
thead th{background:var(--navy);color:#fdfaf2;font-weight:600;font-size:.8rem;letter-spacing:.03em;position:sticky;top:0}
html[data-theme="dark"] thead th{background:#22304a;color:#e9f0fb}
tbody tr:nth-child(even){background:color-mix(in srgb,var(--bg-2) 70%,transparent)}
tbody tr:hover{background:var(--gold-soft)}
td.k{font-weight:700;color:var(--crimson);white-space:nowrap}
td.c,th.c{text-align:center}

/* ---------- 图 ---------- */
figure{margin:1.5rem 0;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:1rem .8rem .6rem;box-shadow:var(--shadow);overflow:hidden}
figure svg{display:block;width:100%;height:auto}
figcaption{font-size:.8rem;color:var(--ink-3);text-align:center;margin-top:.5rem;padding:0 .4rem}

/* ---------- 问答单元 ---------- */
.unit{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);margin:1.5rem 0;box-shadow:var(--shadow);overflow:hidden}
.unit>summary{list-style:none;cursor:pointer;padding:.85rem 1rem;display:flex;gap:.7rem;align-items:baseline;
  background:linear-gradient(to right,var(--navy-soft),transparent);border-bottom:1px solid transparent}
.unit>summary::-webkit-details-marker{display:none}
.unit[open]>summary{border-bottom-color:var(--line-2)}
.unit>summary:hover{background:linear-gradient(to right,var(--gold-soft),transparent)}
.unit .qr{font-family:var(--display);font-size:.76rem;letter-spacing:.06em;color:var(--gold);border:1px solid var(--gold);border-radius:5px;padding:.12rem .42rem;white-space:nowrap;flex:none}
.unit .ut{font-weight:700;color:var(--navy);font-size:1rem;line-height:1.5}
.unit .body{padding:.3rem 1rem 1.1rem}
.qa{border-top:1px dashed var(--line-2);padding:.62rem 0}
.qa:first-child{border-top:0}
.qa .qn{display:inline-block;min-width:2.7rem;font-family:var(--display);font-size:.75rem;color:#fff;background:var(--crimson);border-radius:4px;text-align:center;padding:.08rem .28rem;margin-right:.4rem;vertical-align:.08rem}
.qa .q{font-weight:700;color:var(--ink)}
.qa .a{display:block;margin-top:.2rem;padding-left:.2rem;color:var(--ink-2);font-size:.93rem}
.qa .a::before{content:"答 ";font-family:var(--display);font-size:.72rem;letter-spacing:.12em;color:var(--gold)}
.qa mark{background:var(--gold-2);color:#1d1a16;border-radius:2px;padding:0 .1em}
.lens{margin-top:1rem;display:grid;gap:.7rem;grid-template-columns:repeat(auto-fit,minmax(min(330px,100%),1fr))}
.lens .l{border:1px solid var(--line-2);border-radius:8px;padding:.7rem .85rem;background:var(--bg-2)}
.lens .l .t{font-family:var(--display);font-size:.67rem;letter-spacing:.17em;display:block;margin-bottom:.25rem}
.lens .l.core{border-left:3px solid var(--crimson)} .lens .l.core .t{color:var(--crimson)}
.lens .l.why{border-left:3px solid var(--navy)} .lens .l.why .t{color:var(--navy)}
.lens .l.cont{border-left:3px solid var(--gold-2)} .lens .l.cont .t{color:var(--gold)}
.lens .l.view{border-left:3px solid var(--green)} .lens .l.view .t{color:var(--green)}
.lens .l.app{border-left:3px solid var(--ink-3)} .lens .l.app .t{color:var(--ink-3)}
.lens .l p{margin:.2rem 0;font-size:.9rem;color:var(--ink-2)}
.keys{margin-top:.75rem;font-size:.81rem;color:var(--ink-3);border-top:1px solid var(--line-2);padding-top:.5rem}
.keys span{font-family:var(--display);letter-spacing:.14em;font-size:.66rem;color:var(--gold);margin-right:.4rem}

/* ---------- 搜索条 ---------- */
.searchbar{display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;margin:1.2rem 0;padding:.7rem .8rem;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);position:sticky;top:52px;z-index:20}
.searchbar input[type=search]{flex:1 1 200px;min-width:0;font-family:var(--cn);font-size:.9rem;padding:.5rem .7rem;border:1px solid var(--line);border-radius:7px;background:var(--bg-2);color:var(--ink)}
.searchbar .cnt{font-size:.78rem;color:var(--ink-3);white-space:nowrap}

/* ---------- 十诫互动 ---------- */
.deca{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(140px,100%),1fr));gap:.5rem;margin:1.1rem 0}
.deca button{font-family:var(--cn);text-align:left;padding:.55rem .7rem;border-radius:8px;border:1px solid var(--line);background:var(--card);cursor:pointer;color:var(--ink-2);font-size:.85rem;line-height:1.45;transition:border-color .15s,background .15s}
.deca button:hover{border-color:var(--gold)}
.deca button[aria-pressed="true"]{background:var(--navy-soft);border-color:var(--navy-2);color:var(--navy);font-weight:600}
.deca button i{display:block;font-style:normal;font-family:var(--display);font-size:.68rem;letter-spacing:.14em;color:var(--gold)}
#decaPanel{min-height:120px}

/* ---------- 52 主日地图 ---------- */
.lds{display:grid;grid-template-columns:repeat(auto-fill,minmax(52px,1fr));gap:5px;margin:1rem 0}
.lds button{font-family:var(--display);font-size:.72rem;padding:.42rem .1rem;border-radius:6px;border:1px solid var(--line);background:var(--card);color:var(--ink-2);cursor:pointer;transition:transform .12s,border-color .15s}
.lds button:hover{border-color:var(--gold);transform:translateY(-1px)}
.lds button[aria-pressed="true"]{background:var(--crimson);border-color:var(--crimson);color:#fff}
.lds button[data-sec="g"]{box-shadow:inset 0 -3px 0 var(--crimson)}
.lds button[data-sec="d"]{box-shadow:inset 0 -3px 0 var(--navy-2)}
.lds button[data-sec="t"]{box-shadow:inset 0 -3px 0 var(--green)}
#ldPanel{min-height:150px}
.legend{display:flex;gap:1rem;flex-wrap:wrap;font-size:.79rem;color:var(--ink-3);margin:.5rem 0}
.legend i{display:inline-block;width:15px;height:4px;border-radius:2px;margin-right:.3rem;vertical-align:.18rem}

/* ---------- 闪卡 ---------- */
.fc-wrap{margin:1.2rem 0}
.fc{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--gold-2);border-radius:var(--radius);padding:1.4rem 1.2rem;min-height:220px;display:flex;flex-direction:column;justify-content:center;box-shadow:var(--shadow);cursor:pointer;text-align:center}
.fc .tag{font-family:var(--display);font-size:.68rem;letter-spacing:.18em;color:var(--gold);margin-bottom:.6rem}
.fc .q{font-weight:700;font-size:1.04rem;color:var(--navy);line-height:1.65}
.fc .a{margin-top:.9rem;padding-top:.8rem;border-top:1px dashed var(--line);color:var(--ink-2);font-size:.94rem;line-height:1.85;text-align:left}
.fc .a.hidden{filter:blur(6px);opacity:.55;user-select:none}
.fc .hint{margin-top:.8rem;font-size:.9rem;color:var(--crimson);letter-spacing:.12em;text-align:left}
.fc.done{border-top-color:var(--green)}
.fc-bar{display:flex;gap:.45rem;flex-wrap:wrap;align-items:center;margin-top:.8rem}
.fc-bar .prog{font-size:.79rem;color:var(--ink-3);margin-left:auto}
.fc-filter{display:flex;gap:.4rem;flex-wrap:wrap;margin:.7rem 0}

/* ---------- 时间轴 ---------- */
.tl{list-style:none;padding:0;margin:1.2rem 0;border-left:2px solid var(--line);padding-left:1.1rem}
.tl li{position:relative;margin:.75rem 0;font-size:.9rem;color:var(--ink-2)}
.tl li::before{content:"";position:absolute;left:-1.48rem;top:.62rem;width:8px;height:8px;border-radius:50%;background:var(--gold-2);border:2px solid var(--bg)}
.tl li b{color:var(--navy);font-family:var(--display);font-size:.85rem;letter-spacing:.04em;margin-right:.45rem}
.tl li.hi::before{background:var(--crimson)}

/* ---------- 底部 ---------- */
footer{max-width:var(--maxw);margin:0 auto;padding:2.5rem clamp(.8rem,2vw,1.6rem) 4rem;border-top:1px solid var(--line);color:var(--ink-3);font-size:.84rem;text-align:center}
.toTop{position:fixed;right:16px;bottom:16px;z-index:50;width:42px;height:42px;border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--ink-2);cursor:pointer;box-shadow:var(--shadow);display:none;font-size:1rem}
.toTop.show{display:block}

/* ---------- 移动端 ---------- */
@media (max-width:1000px){
  .shell{grid-template-columns:1fr}
  .menu-btn{display:inline-block}
  .sidebar{position:fixed;inset:0 auto 0 0;width:min(86vw,320px);max-height:none;height:100%;
    background:var(--bg-2);border-right:1px solid var(--line);z-index:70;transform:translateX(-102%);
    transition:transform .22s ease;padding:1rem .8rem 3rem;overflow-y:auto;box-shadow:var(--shadow)}
  .sidebar.open{transform:none}
  .scrim{position:fixed;inset:0;background:rgba(20,16,10,.44);z-index:65;display:none}
  .scrim.show{display:block}
  .searchbar{position:static}
  html{scroll-padding-top:64px}
}
@media (max-width:560px){
  body{font-size:16px;line-height:1.88}
  .hero{padding:2.2rem .4rem 1.7rem}
  .unit .body{padding:.3rem .7rem 1rem}
  .printBtn{display:none}
  .lds{grid-template-columns:repeat(auto-fill,minmax(44px,1fr))}
}

/* ---------- SVG 图内文字 ---------- */
.sv{font-family:var(--cn);font-size:13px;fill:var(--ink-2)}
.sv .t{font-weight:700;fill:var(--navy);font-size:14px}
.sv .sm{font-size:11px;fill:var(--ink-3)}
.sv .xs{font-size:10px;fill:var(--ink-3);letter-spacing:.06em}
.sv .k{font-weight:700;fill:var(--crimson)}
.sv .w{fill:#fffdf7;font-weight:700}
.sv .bx{fill:var(--card);stroke:var(--line);stroke-width:1.2}
.sv .bxn{fill:var(--navy-soft);stroke:var(--navy-2);stroke-width:1.2}
.sv .bxg{fill:var(--gold-soft);stroke:var(--gold);stroke-width:1.2}
.sv .bxc{fill:var(--crimson-soft);stroke:var(--crimson);stroke-width:1.2}
.sv .bxe{fill:var(--green-soft);stroke:var(--green);stroke-width:1.2}
.sv .ln{stroke:var(--line);stroke-width:1.2;fill:none}
.sv .ar{stroke:var(--gold);stroke-width:1.6;fill:none;marker-end:url(#ah)}
.sv .arn{stroke:var(--navy-2);stroke-width:1.6;fill:none;marker-end:url(#ahn)}
.sv .dash{stroke:var(--line);stroke-width:1.2;fill:none;stroke-dasharray:5 4}
.sv .fn{fill:var(--navy)}.sv .fc{fill:var(--crimson)}.sv .fg{fill:var(--gold)}.sv .fe{fill:var(--green)}

/* ══════════ 水波背景（高级感 · 低成本 · 尊重减弱动效） ══════════ */
.waterbg{position:fixed;inset:0;z-index:-2;pointer-events:none;overflow:hidden;opacity:.85}
.waterbg span{position:absolute;border-radius:50%;filter:blur(46px);will-change:transform}
.waterbg span:nth-child(1){width:52vw;height:52vw;left:-12vw;top:-10vw;
  background:radial-gradient(circle,rgba(31,58,95,.16),transparent 66%);animation:drift1 52s ease-in-out infinite}
.waterbg span:nth-child(2){width:46vw;height:46vw;right:-10vw;top:22vh;
  background:radial-gradient(circle,rgba(169,129,47,.15),transparent 66%);animation:drift2 64s ease-in-out infinite}
.waterbg span:nth-child(3){width:44vw;height:44vw;left:24vw;bottom:-14vw;
  background:radial-gradient(circle,rgba(140,47,57,.12),transparent 66%);animation:drift3 74s ease-in-out infinite}
html[data-theme="dark"] .waterbg{opacity:.6}
@keyframes drift1{0%,100%{transform:translate3d(0,0,0) scale(1)}33%{transform:translate3d(7vw,5vh,0) scale(1.1)}66%{transform:translate3d(-4vw,9vh,0) scale(.95)}}
@keyframes drift2{0%,100%{transform:translate3d(0,0,0) scale(1)}40%{transform:translate3d(-8vw,-6vh,0) scale(1.08)}75%{transform:translate3d(3vw,7vh,0) scale(.94)}}
@keyframes drift3{0%,100%{transform:translate3d(0,0,0) scale(1)}45%{transform:translate3d(6vw,-7vh,0) scale(1.06)}80%{transform:translate3d(-7vw,-3vh,0) scale(.97)}}

/* 细腻的水纹层：两道极淡的斜向波纹缓慢推移 */
.waterbg b{position:absolute;inset:-20%;display:block;
  background:repeating-linear-gradient(112deg,transparent 0 46px,rgba(31,58,95,.028) 46px 50px,transparent 50px 96px);
  animation:wave 34s linear infinite}
.waterbg b+b{background:repeating-linear-gradient(-104deg,transparent 0 62px,rgba(169,129,47,.024) 62px 66px,transparent 66px 128px);
  animation:wave2 47s linear infinite}
@keyframes wave{from{transform:translate3d(0,0,0)}to{transform:translate3d(96px,54px,0)}}
@keyframes wave2{from{transform:translate3d(0,0,0)}to{transform:translate3d(-128px,42px,0)}}

/* 点击涟漪 */
.rippleHost{position:relative;overflow:hidden}
.rp{position:absolute;border-radius:50%;pointer-events:none;transform:translate(-50%,-50%) scale(0);
  background:radial-gradient(circle,rgba(201,162,39,.42),rgba(201,162,39,.14) 45%,transparent 72%);
  animation:rp .62s cubic-bezier(.22,.61,.36,1) forwards}
@keyframes rp{to{transform:translate(-50%,-50%) scale(1);opacity:0}}
/* 页面水面涟漪（点击正文空白处） */
.wave-ring{position:fixed;z-index:1;pointer-events:none;border-radius:50%;
  border:1.5px solid rgba(169,129,47,.5);transform:translate(-50%,-50%) scale(0);
  animation:ring 1.15s cubic-bezier(.16,.84,.44,1) forwards}
.wave-ring.b{animation-delay:.13s;border-color:rgba(31,58,95,.38)}
@keyframes ring{0%{transform:translate(-50%,-50%) scale(0);opacity:.85}
  100%{transform:translate(-50%,-50%) scale(1);opacity:0}}
@media (prefers-reduced-motion:reduce){
  .waterbg span,.waterbg b{animation:none!important}
  .rp,.wave-ring{display:none!important}
}

/* ══════════ 阅读进度条 ══════════ */
.progress{position:fixed;left:0;top:0;height:2.5px;z-index:80;width:100%;background:transparent;pointer-events:none}
.progress i{display:block;height:100%;width:0;
  background:linear-gradient(90deg,var(--navy-2),var(--gold-2));transition:width .12s linear}

/* ══════════ 目录可隐藏 ══════════ */
body.tocOff .sidebar{display:none}
body.tocOff .shell{grid-template-columns:minmax(0,1fr)}
body.tocOff main{max-width:min(78ch,100%);margin:0 auto}
.tocFab{position:fixed;left:14px;bottom:16px;z-index:55;display:none;
  padding:.55rem .8rem;border-radius:999px;border:1px solid var(--line);background:var(--card);
  color:var(--ink-2);cursor:pointer;box-shadow:var(--shadow);font-family:var(--cn);font-size:.8rem}
body.tocOff .tocFab{display:block}
@media (max-width:1000px){body.tocOff .tocFab{display:none}body.tocOff .shell{grid-template-columns:1fr}
  body.tocOff .sidebar{display:block}}

/* ══════════ 平滑与质感 ══════════ */
.box,.mini,.unit,figure,.tablewrap,.fc{transition:box-shadow .3s ease,transform .3s ease,border-color .25s ease}
.mini:hover,.box:hover{box-shadow:0 2px 4px rgba(60,45,20,.06),0 14px 34px rgba(60,45,20,.11)}
html[data-theme="dark"] .mini:hover,html[data-theme="dark"] .box:hover{box-shadow:0 2px 6px rgba(0,0,0,.35),0 16px 38px rgba(0,0,0,.4)}
.unit>summary,.btn,.lds button,.deca button,.mon button{-webkit-tap-highlight-color:transparent}
.topbar{box-shadow:0 1px 0 rgba(0,0,0,.02),0 6px 22px rgba(60,45,20,.05)}

/* ══════════ 口诀 ══════════ */
.poem{display:grid;gap:.3rem;margin:.8rem 0}
.poem div{display:flex;align-items:baseline;gap:.8rem;padding:.4rem .6rem;border-radius:7px;
  background:color-mix(in srgb,var(--card) 70%,transparent);border-left:3px solid var(--gold-2)}
.poem span{font-family:var(--cn);font-weight:700;font-size:1.06rem;letter-spacing:.22em;color:var(--crimson);white-space:nowrap}
.poem i{font-style:normal;font-size:.8rem;color:var(--ink-3);letter-spacing:.02em}
@media (max-width:480px){.poem div{flex-direction:column;gap:.15rem}.poem span{font-size:1rem;letter-spacing:.16em}}

/* ══════════ 君王面板 ══════════ */
.mon{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(128px,100%),1fr));gap:.5rem;margin:1.1rem 0}
.mon button{font-family:var(--cn);text-align:left;padding:.55rem .65rem;border-radius:8px;border:1px solid var(--line);
  background:var(--card);cursor:pointer;color:var(--ink-2);font-size:.86rem;line-height:1.45;
  border-bottom-width:3px;transition:transform .16s ease,border-color .16s}
.mon button:hover{transform:translateY(-2px);border-color:var(--gold)}
.mon button[aria-pressed="true"]{background:var(--navy-soft);color:var(--navy);font-weight:600}
.mon button i{display:block;font-style:normal;font-size:.68rem;color:var(--ink-3);letter-spacing:.04em}
.mon button[data-c="r"]{border-bottom-color:var(--crimson)}
.mon button[data-c="p"]{border-bottom-color:var(--green)}
.mon button[data-c="m"]{border-bottom-color:var(--gold-2)}
.mon button[data-c="h"]{border-bottom-color:var(--navy-2)}
.mon button[data-c="i"]{border-bottom-color:var(--ink-3)}
#monPanel{min-height:180px}

/* ══════════ 三线年表 ══════════ */
table.tl3 td.yr{font-family:var(--display);font-weight:700;color:var(--navy);white-space:nowrap}
table.tl3 td.ln{white-space:nowrap;font-size:.78rem}
table.tl3 td.ln.c{color:var(--gold)}
table.tl3 td.ln.e{color:var(--navy-2)}
table.tl3 td.ln.s{color:var(--green)}
table.tl3 tr.mile td{background:color-mix(in srgb,var(--gold-soft) 60%,transparent)}
table.tl3 tr.mile td.yr{color:var(--crimson)}

/* ══════════ 地图 ══════════ */
.sv .sea{fill:color-mix(in srgb,var(--navy-soft) 55%,transparent)}
html[data-theme="dark"] .sv .sea{fill:color-mix(in srgb,var(--navy-soft) 70%,transparent)}
.sv .mp.land{fill:var(--card);stroke:var(--line);stroke-width:1.4;stroke-linejoin:round}
.sv .mborder{stroke:var(--line);stroke-width:1.4;stroke-dasharray:6 4;fill:none}
.sv .mreg{font-size:11px;fill:var(--ink-3);letter-spacing:.22em}
.sv .mlab{font-size:11.5px;font-weight:700;fill:var(--navy)}
.sv .mnote{font-size:9.5px;fill:var(--ink-3)}
.sv .mleg{fill:var(--card);stroke:var(--line);stroke-width:1;opacity:.95}
.sv .mchain{stroke:var(--gold);stroke-width:1.4}
.sv .river{fill:none;stroke:var(--navy-2);stroke-width:2.2;opacity:.75;stroke-linejoin:round;stroke-linecap:round}
.sv .mriver{font-size:10px;fill:var(--navy-2);letter-spacing:.14em;opacity:.9}
.sv .mpt{stroke:var(--card);stroke-width:1.4}
.sv .mpt.c1{fill:var(--crimson)} .sv .mpt.c2{fill:var(--gold-2)} .sv .mpt.c3{fill:var(--navy-2)}
.sv .mpt.c4{fill:var(--green)}  .sv .mpt.c5{fill:var(--ink-3)}
.sv .marr{fill:none;stroke-width:1.7;marker-end:url(#ah)}
.sv .marr.out{stroke:var(--gold)}
.sv .marr.back{stroke:var(--green);stroke-dasharray:6 5;marker-end:url(#ahg)}
.sv .lane{stroke:var(--line-2);stroke-width:1;stroke-dasharray:3 5}
.sv .mind{fill:none;stroke:var(--gold);stroke-width:1.3;opacity:.7}
.sv .shield{fill:none;stroke:var(--navy-2);stroke-width:2}

/* 动态：流动虚线 · 脉冲 · 描线 */
.sv .flow{stroke-dasharray:9 7;animation:dashmove 1.5s linear infinite}
@keyframes dashmove{to{stroke-dashoffset:-32}}
.sv .pulse{transform-box:fill-box;transform-origin:center;animation:mpulse 2.6s ease-in-out infinite}
@keyframes mpulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.45);opacity:.6}}
.sv .draw{stroke-dasharray:900;stroke-dashoffset:900;animation:drawln 2.6s ease forwards}
@keyframes drawln{to{stroke-dashoffset:0}}
@media (prefers-reduced-motion:reduce){
  .sv .flow,.sv .pulse{animation:none!important}
  .sv .draw{animation:none!important;stroke-dashoffset:0!important}
}

/* ══════════ 时间轴拖动器 ══════════ */
.scrub{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:1rem 1.1rem;box-shadow:var(--shadow);margin:1.2rem 0}
.scrub-top{display:flex;align-items:baseline;gap:.8rem;flex-wrap:wrap;margin-bottom:.6rem}
.scrub-year{font-family:var(--display);font-size:2rem;font-weight:700;color:var(--crimson);
  line-height:1;min-width:4.6rem;font-variant-numeric:tabular-nums}
.scrub-era{font-size:.86rem;color:var(--ink-2)}
.scrub-era b{color:var(--navy)}
.scrub input[type=range]{width:100%;accent-color:var(--gold-2);margin:.5rem 0 .2rem;height:26px}
.scrub-ticks{display:flex;justify-content:space-between;font-size:.7rem;color:var(--ink-3);
  font-family:var(--display);letter-spacing:.04em}
.scrub-out{margin-top:.7rem;display:grid;gap:.4rem;min-height:104px}
.scrub-out .ev{display:flex;gap:.6rem;align-items:baseline;padding:.34rem .55rem;border-radius:6px;
  background:var(--bg-2);border-left:3px solid var(--line);font-size:.86rem;
  animation:evin .32s ease both}
@keyframes evin{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
.scrub-out .ev.c{border-left-color:var(--gold)} .scrub-out .ev.e{border-left-color:var(--navy-2)}
.scrub-out .ev.s{border-left-color:var(--green)}
.scrub-out .ev .y{font-family:var(--display);font-weight:700;color:var(--navy);min-width:2.6rem}
.scrub-out .ev .l{font-size:.7rem;color:var(--ink-3);min-width:2.6rem}
.scrub-out .none{font-size:.85rem;color:var(--ink-3);padding:.4rem .55rem}
.scrub-bar{position:relative;height:16px;margin-top:.2rem}
.scrub-bar i{position:absolute;top:5px;width:2px;height:7px;background:var(--line);border-radius:1px}
.scrub-bar i.m{background:var(--gold-2);height:11px;top:2px;width:2.5px}

/* ══════════ 性能：长页面分块渲染 ══════════ */
details.unit{content-visibility:auto;contain-intrinsic-size:auto 120px}
figure{content-visibility:auto;contain-intrinsic-size:auto 420px}
.tablewrap{content-visibility:auto;contain-intrinsic-size:auto 320px}
@media print{details.unit,figure,.tablewrap{content-visibility:visible!important}}

/* ---------- 打印 ---------- */
@media print{
  .topbar,.sidebar,.scrim,.toTop,.searchbar,.fc-bar,.fc-filter,.deca,.lds,.mon,.btn,.waterbg,.progress,.tocFab,.scrub input,.scrub-bar{display:none!important}
  body.tocOff .shell{grid-template-columns:1fr}
  body{background:#fff;color:#000;font-size:10.5pt;line-height:1.6}
  .shell{display:block;max-width:none;padding:0}
  .part{break-before:page;border-top:2px solid #999}
  .unit{break-inside:avoid;box-shadow:none;border-color:#bbb}
  details{display:block!important}
  details>*{display:block!important}
  .fc .a.hidden{filter:none!important;opacity:1!important}
  figure,table,.box{break-inside:avoid;box-shadow:none}
  a{color:#000;border:0}
  @page{size:A4;margin:16mm 14mm}
}
"""
