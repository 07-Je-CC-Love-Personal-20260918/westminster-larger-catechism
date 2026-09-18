#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SVG 版面校验：检出图内文字出框与互相重叠。

为什么需要它：figure{overflow:hidden} 会把出框的 SVG 文字裁掉，
普通的 DOM 溢出检测量不到，页面看着「没溢出」实则文字被切、被压。
必须用 getBoundingClientRect 逐个 <text> 实测。
需要 playwright；CI 中若未安装则跳过（不阻断构建）。
"""
import os, subprocess, sys, threading, http.server, socketserver, functools

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
PORT = 8977

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("== SVG 版面校验 ==\n  skip  未安装 playwright，跳过")
    sys.exit(0)

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", PORT), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()

JS = """()=>{const out=[];
 document.querySelectorAll('svg.sv').forEach(svg=>{
  const fig=svg.closest('figure'); const id=fig?fig.id:'(未命名)';
  const sr=svg.getBoundingClientRect(); if(sr.width<10)return;
  const vb=(svg.getAttribute('viewBox')||'').split(/\\s+/).map(Number);
  const sc=sr.width/(vb[2]||1);
  const ts=[...svg.querySelectorAll('text')];
  let ox=0,oy=0; const ovl=[];
  ts.forEach(t=>{const r=t.getBoundingClientRect(); if(r.width<0.5)return;
   ox=Math.max(ox,(Math.max(sr.left-r.left,r.right-sr.right))/sc);
   oy=Math.max(oy,(Math.max(sr.top-r.top,r.bottom-sr.bottom))/sc);});
  for(let i=0;i<ts.length;i++){const a=ts[i].getBoundingClientRect(); if(a.width<0.5)continue;
   for(let j=i+1;j<ts.length;j++){const c=ts[j].getBoundingClientRect(); if(c.width<0.5)continue;
    if(Math.min(a.right,c.right)-Math.max(a.left,c.left)>2 &&
       Math.min(a.bottom,c.bottom)-Math.max(a.top,c.top)>2)
      ovl.push([(ts[i].textContent||'').slice(0,18),(ts[j].textContent||'').slice(0,18)]);}}
  if(ox>1.5||oy>1.5||ovl.length) out.push({id,ox:Math.round(ox),oy:Math.round(oy),ovl:ovl.slice(0,4),n:ovl.length});
 });return out}"""

print("== SVG 版面校验（出框 · 重叠）==")
bad = []
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
    print("  FAIL %s  出框X=%s 出框Y=%s 重叠=%s" % (r["id"], r["ox"], r["oy"], r["n"]))
    for a, b in r["ovl"]:
        print("         「%s」 压住 「%s」" % (a, b))
print("  共 %d 个 SVG，%s" % (n_svg, "全部零出框零重叠" if not bad else "%d 个有问题" % len(bad)))
sys.exit(1 if bad else 0)
