#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site/index.html 静态校验。CI 或本地改完跑一遍，全绿再部署。"""
import collections, io, os, re, sys
from xml.etree import ElementTree as ET

H = io.open(os.path.join(os.path.dirname(__file__), "site", "index.html"), encoding="utf-8").read()
fail = []


def check(name, ok, detail=""):
    print(("  OK   " if ok else "  FAIL ") + name + (("  " + detail) if detail else ""))
    if not ok:
        fail.append(name)


print("== 威斯敏斯特大要理问答全解 · 静态校验 ==")
ids = re.findall(r'\sid="([^"]+)"', H)
dup = [k for k, v in collections.Counter(ids).items() if v > 1]
check("ID 无重复", not dup, "重复: %s" % dup)
missing = sorted(set(re.findall(r'href="#([^"]+)"', H)) - set(ids))
check("锚点全部有效", not missing, "缺失: %s" % missing)

qn = sorted(set(int(x) for x in re.findall(r'<span class="qn">(\d+)</span>', H)))
check("196 问齐全", qn == list(range(1, 197)), "缺: %s" % sorted(set(range(1, 197)) - set(qn)))

bad = []
for t in ("div", "details", "summary", "table", "tr", "td", "th", "section", "figure",
          "figcaption", "p", "span", "ul", "li", "h3", "h4", "main", "aside", "footer", "button"):
    o, c = len(re.findall(r"<%s(?=[\s>])" % t, H)), len(re.findall(r"</%s>" % t, H))
    if o != c:
        bad.append("%s %d/%d" % (t, o, c))
check("HTML 标签平衡", not bad, " ".join(bad))

svgs = re.findall(r"<svg[^>]*>.*?</svg>", H, re.S)
nbad = 0
for s in svgs:
    try:
        ET.fromstring(s)
    except ET.ParseError:
        nbad += 1
check("SVG 全部良构（%d 个）" % len(svgs), nbad == 0, "%d 个解析失败" % nbad)

check("零外部请求", not re.findall(r'(?:src|href)="(?:https?:)?//', H))
check("无乱码", "\ufffd" not in H)
check("模板占位已替换", "__TOC__" not in H)
check("图 25 幅", H.count("<figure") == 25, "实际 %d" % H.count("<figure"))
check("表 18 张", H.count("<table") == 18, "实际 %d" % H.count("<table"))

kb = len(H.encode("utf-8")) / 1024.0
cn = sum(1 for ch in H if "\u4e00" <= ch <= "\u9fff")
print("  ---- %.0f KB · %d 中文字符 · %d 个 ID" % (kb, cn, len(ids)))
print(("全部通过" if not fail else "失败 %d 项：%s" % (len(fail), fail)))
sys.exit(1 if fail else 0)
