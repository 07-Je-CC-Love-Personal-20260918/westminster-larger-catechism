#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SVG 版面校验：检出图内文字出框、文字互相重叠、文字被后绘制图形遮盖、文字撑出所在色块。

为什么需要它：
1. figure{overflow:hidden} 会把出框的 SVG 文字裁掉，普通 DOM 溢出检测量不到，
   页面看着「零溢出」实则文字被切。
2. SVG 按文档顺序绘制，后出现的填充图形会压在先画的文字上。这类「被盖住」
   在 DOM 层面也完全测不到，必须比对绘制次序 + 包围盒。
需要 playwright；CI 中若未安装则跳过（不阻断构建）。
"""
import functools
import http.server
import os
import socketserver
import sys
import threading

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
PORT = 8977

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("== SVG 版面校验 ==\n  skip  未安装 playwright，跳过")
    sys.exit(0)

JS = r"""()=>{const out=[];
 document.querySelectorAll('svg.sv').forEach(svg=>{
  const fig=svg.closest('figure'); const id=fig?fig.id:'(未命名)';
  const sr=svg.getBoundingClientRect(); if(sr.width<10)return;
  const vb=(svg.getAttribute('viewBox')||'').split(/\s+/).map(Number);
  const sc=sr.width/(vb[2]||1);
  const all=[...svg.querySelectorAll('text,rect,circle,polygon,path')];
  const ts=[], sh=[];
  all.forEach((e,idx)=>{
   const r=e.getBoundingClientRect(); if(r.width<0.5||r.height<0.5)return;
   if(e.tagName.toLowerCase()==='text'){ts.push({e,r,idx});}
   else{const f=getComputedStyle(e).fill;
        if(f&&f!=='none'&&f!=='rgba(0, 0, 0, 0)') sh.push({e,r,idx});}
  });
  let ox=0,oy=0; const ovl=[], cov=[];
  ts.forEach(t=>{
   ox=Math.max(ox,(Math.max(sr.left-t.r.left,t.r.right-sr.right))/sc);
   oy=Math.max(oy,(Math.max(sr.top-t.r.top,t.r.bottom-sr.bottom))/sc);});
  for(let i=0;i<ts.length;i++)for(let j=i+1;j<ts.length;j++){
   const a=ts[i].r,c=ts[j].r;
   if(Math.min(a.right,c.right)-Math.max(a.left,c.left)>2 &&
      Math.min(a.bottom,c.bottom)-Math.max(a.top,c.top)>2)
     ovl.push([(ts[i].e.textContent||'').slice(0,18),(ts[j].e.textContent||'').slice(0,18)]);}
  // 文字撑出自己所在的色块（色块先画、文字后画，"被遮"规则抓不到）
  const spill=[];
  ts.forEach(t=>{
   let host=null;
   const cx=(t.r.left+t.r.right)/2, cyy=(t.r.top+t.r.bottom)/2;
   sh.forEach(s=>{
    if(s.idx>t.idx) return;                       // 只看在文字之前画的
    const tag=s.e.tagName.toLowerCase();
    if(tag!=='rect'&&tag!=='circle') return;      // 地图国界是 path，不是标签容器，排除以免误报
    if(s.r.width*s.r.height > sr.width*sr.height*0.45) return;    // 排除海面/整幅底板
    if(s.r.width<14||s.r.height<12) return;       // 忽略小圆点/色标
    if(cx>=s.r.left&&cx<=s.r.right&&cyy>=s.r.top&&cyy<=s.r.bottom)
      if(!host||s.idx>host.idx) host=s;           // 取最近的那个
   });
   if(host){
    const ovr=Math.max(host.r.left-t.r.left, t.r.right-host.r.right,
                       host.r.top-t.r.top, t.r.bottom-host.r.bottom);
    if(ovr>2.5) spill.push([(t.e.textContent||'').slice(0,20),
                            host.e.tagName+'.'+(host.e.getAttribute('class')||''),
                            Math.round(ovr/sc)]);
   }});
  ts.forEach(t=>{
   sh.forEach(s=>{
    if(s.idx<t.idx) return;
    if(s.e.contains(t.e)||t.e.contains(s.e)) return;
    const w=Math.min(t.r.right,s.r.right)-Math.max(t.r.left,s.r.left);
    const h=Math.min(t.r.bottom,s.r.bottom)-Math.max(t.r.top,s.r.top);
    if(w>2&&h>2 && w*h > t.r.width*t.r.height*0.18)
      cov.push([(t.e.textContent||'').slice(0,20), s.e.tagName+'.'+(s.e.getAttribute('class')||'')]);});});
  if(ox>1.5||oy>1.5||ovl.length||cov.length||spill.length)
    out.push({id,ox:Math.round(ox),oy:Math.round(oy),ovl:ovl.slice(0,4),n:ovl.length,
              cov:cov.slice(0,5),cn:cov.length,spill:spill.slice(0,6),sn:spill.length});
 });return out}"""

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", PORT), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()

print("== SVG 版面校验（出框 · 文字重叠 · 文字被遮）==")
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": 1440, "height": 1000})
    pg.goto("http://127.0.0.1:%d/index.html" % PORT, wait_until="load")
    pg.wait_for_timeout(1200)
    pg.evaluate("()=>{document.querySelectorAll('details').forEach(d=>d.open=true);"
                "document.querySelectorAll('figure').forEach(e=>e.style.contentVisibility='visible')}")
    pg.wait_for_timeout(800)
    n_svg = pg.locator("svg.sv").count()
    bad = pg.evaluate(JS)
    br.close()
srv.shutdown()

for r in bad:
    print("  FAIL %s  出框X=%s 出框Y=%s 文字重叠=%s 文字被遮=%s 撑出色块=%s"
          % (r["id"], r["ox"], r["oy"], r["n"], r["cn"], r.get("sn", 0)))
    for a, b in r["ovl"]:
        print("         重叠：「%s」 ↔ 「%s」" % (a, b))
    for a, b in r["cov"]:
        print("         被遮：「%s」 被 %s 盖住" % (a, b))
    for a, b, n in r.get("spill", []):
        print("         撑出：「%s」 超出所在 %s 约 %s 单位" % (a, b, n))
print("  共 %d 个 SVG，%s" % (n_svg, "全部通过" if not bad else "%d 个有问题" % len(bad)))
sys.exit(1 if bad else 0)
