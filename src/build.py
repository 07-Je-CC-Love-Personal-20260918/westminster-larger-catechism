# -*- coding: utf-8 -*-
"""装配：把各模块拼成单文件 index.html。"""

import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from css import CSS
from charts import SPRITE
from js import JS
import macro, topics, hc, lc1, lc2, lc3, history, creeds, maps, flows
from unit import render_unit

TOC = []   # (level, anchor, label)


def toc(level, anchor, label):
    TOC.append((level, anchor, label))


def viz(kind, key, caption):
    src = maps.MAPS[key]() if kind == "map" else flows.FLOWS[key]()
    return '<figure id="viz-%s">%s<figcaption>%s</figcaption></figure>' % (key, src, caption)


def part_html(pid, num, title, desc):
    toc(1, pid, title)
    return ('<section class="part" id="%s"><div class="num">%s</div>'
            '<h2>%s</h2><p>%s</p></section>' % (pid, num, title, desc))


def sec_html(sid, title, body, lv=2):
    toc(lv, sid, title)
    return '<h3 id="%s">%s</h3>%s' % (sid, title, body)


def build():
    B = []

    B.append(SPRITE)
    B.append('<div class="waterbg" aria-hidden="true"><span></span><span></span><span></span><b></b><b></b></div>')
    B.append('<div class="progress" aria-hidden="true"><i id="progressBar"></i></div>')

    # ── 顶栏 ──
    B.append('''<div class="topbar">
<button class="btn menu-btn" data-act="menu" aria-label="目录">☰ 目录</button>
<div class="brand">威斯敏斯特<b>大要理问答</b>全解</div>
<div class="spacer"></div>
<button class="btn" id="tocBtn" data-act="toc" aria-pressed="false">隐藏目录</button>
<button class="btn" id="themeBtn" data-act="theme">主题 · 跟随系统</button>
<button class="btn printBtn" data-act="print">打印 / PDF</button>
</div>
<div class="scrim" id="scrim" data-act="scrim"></div>
<div class="shell">
<aside class="sidebar" id="sidebar"><h2>目录 CONTENTS</h2><ul class="toc" id="toc">__TOC__</ul></aside>
<main>''')

    # ── Hero ──
    B.append('''<header class="hero">
<div class="eyebrow">WESTMINSTER LARGER CATECHISM · 1647</div>
<h1>威斯敏斯特大要理问答<br>全解</h1>
<div class="lat">Catechismus Maior Westmonasteriensis</div>
<p class="sub">196 问全覆盖。先跳出框架从整本圣经与神学核心看，再逐组深入；
以欧陆改革宗与正统神学为参照系，交代前因后果、真实论敌、写了什么、如何应用。
含<b>王朝与年代记忆系统</b>（十句口诀 · 十朝互动卡 · 三线并行年表）、<b>三大普世信经对照</b>，
末附<b>海德堡速背引擎</b>——52 主日互动地图、57 张闪卡、21 天计划。</p>
<div class="meta">
<span class="pill c">196 问全覆盖</span><span class="pill">45 个解读单元</span>
<span class="pill n">五重视角逐组剖析</span><span class="pill">24 幅图表图示 · 4 幅地图</span>
<span class="pill c">十朝君王 · 可拖动时间轴</span><span class="pill">流程图 · 思维导图 · 动态图</span>
<span class="pill g">海德堡 52 主日 · 129 问</span><span class="pill">75 张互动闪卡</span>
<span class="pill">纯静态 · 零外部请求</span>
</div>
</header>''')

    # ── 检索条 ──
    B.append('''<div class="searchbar">
<input type="search" id="qsearch" placeholder="检索 196 问：输入关键词，如「称义」「安息日」「贪恋」「代求」……" aria-label="检索问答">
<button class="btn" id="qclear">清除</button>
<button class="btn" data-act="expand" aria-pressed="false">全部展开</button>
<span class="cnt" id="qcount">共 196 问</span>
</div>''')

    # ── 第一至第三部（宏观），并在第二部插入王朝记忆三节 ──
    from charts import figure as _fig
    for blk in macro.BLOCKS:
        if blk["type"] == "part":
            B.append(part_html(blk["id"], blk["num"], blk["title"], blk["desc"]))
        else:
            B.append(sec_html(blk["id"], blk["title"], blk["html"]))
        if blk.get("id") == "p1-2":
            B.append(sec_html("p1-2b", "二·附　196 问思维导图：一张图看完全篇",
                              "<p>先看骨架，再看细节。这张图把 196 问压成<b>一个中心、两大分支、九个挂点</b>——"
                              "背下这九个挂点，你随时能从任意一问倒推回它在全篇中的位置。</p>"
                              + viz("flow", "mind196",
                                    "图二·附　196 问思维导图。中心是问 5（全篇目录），左枝「信什么」，右枝「行什么」。")))
        if blk.get("id") == "p1-7":
            B.append(viz("flow", "which",
                         "图三·附　该用哪一份？三份威敏文件加上大公信经的选择决策树。"))
        if blk.get("id") == "p2-1":
            B.append(viz("map", "britain",
                         "地图一　三个王国与十二年的因果链。整场危机是从<b>苏格兰</b>烧起来的，不是从英格兰。"))
            B.append(sec_html("p2-k1", "二、记不住几个王？先背这十句口诀",
                              history.SEC_WHY + _fig("dynasty",
                              "图四　英格兰十朝，条宽按在位年数真实成比例。关键一眼：威斯敏斯特会议整个发生在查理一世这一朝的六年之内。")))
            B.append(sec_html("p2-k2", "三、十朝互动卡：每一朝做了什么、与威敏有何关系",
                              history.SEC_MONARCH))
            B.append(sec_html("p2-k2b", "三·附　两幅地图：宗教改革的欧洲，与流亡者的路线",
                              "<p>把年代挂到<b>地理</b>上，会记得更牢。第一幅告诉你三项合一信条为什么全部诞生在同一条河谷；"
                              "第二幅告诉你英格兰清教主义的种子是怎么被带回去的。</p>"
                              + viz("map", "reformation",
                                    "地图二　宗教改革的欧洲。日内瓦—海德堡—多特直线距离不到 600 公里，整个欧陆改革宗文献传统在这条窄带上完成。")
                              + viz("map", "exiles",
                                    "地图三　1553–1558 马利亚流亡者的出走与 1559 年的归来。金色流动箭头为出走路线，绿色虚线为归国。")))
            B.append(sec_html("p2-k3", "四、三线并行年表：欧陆 · 英格兰 · 苏格兰",
                              _fig("threelines",
                              "图五　三条线同时在走。两道红色竖虚线是「双生年」：1559（《要义》定版＝伊丽莎白折中）与 1563（海德堡＝三十九条）。")
                              + history.SEC_SCRUB + history.timeline_html()))
            B.append(sec_html("p2-k4", "五、18 张年代与人物闪卡（专治记不住）",
                              history.SEC_HISTCARDS))

    B.append(sec_html("p2-k5", "十一、它后来去了哪里：一幅传播图",
                      "<p>最后一个容易被忽略的事实：<b>写它的国家废了它，接纳它的邻国把它传遍了世界。</b>"
                      "1662 年威敏准则在英格兰失去法定地位，1690 年却被立为苏格兰国教信条；"
                      "此后经苏格兰移民与宣教，进入爱尔兰、北美、澳洲、非洲与亚洲。</p>"
                      + viz("map", "spread",
                            "地图四　威斯敏斯特准则 1648 年至今的传播。今日 OPC、PCA、韩国长老会、华人改革宗教会所持守的，都是 1648 年那一份。")))

    # ── 第四部 三大普世信经 ──
    B.append(part_html("pc", "第四部", "大公坐标：三大普世信经与三项合一信条",
                       "欧陆改革宗先是大公的，然后才是改革宗的。这一部把大要理放回「三大信经 ＋ 三项合一信条」的两层标准里，并补上威敏没有明文处理的那一块。"))
    B.append(sec_html("pc-1", "一、两层标准：比利时信条第9条说了什么", creeds.SEC_WHY))
    B.append(sec_html("pc-2", "二、三大信经的坐标与四大公会议", creeds.SEC_TABLE))
    B.append(sec_html("pc-2b", "二·附　信仰之盾：亚他那修信经的图形版（动态）",
                      "<p>亚他那修信经前半部分的四十四条，可以压缩成一张图、六句话。"
                      "<b>三条外边读「不是」，三条内辐读「是」</b>——这六句就是正统三一论的全部边界。</p>"
                      + viz("flow", "shield",
                            "图七·附　信仰之盾（Scutum Fidei）。线条为动态描绘。右栏给出它与大要理问 9–10、比利时信条第 10 条的对应。")))
    B.append(sec_html("pc-3", "三、威敏为何不用使徒信经作骨架，以及如何补白", creeds.SEC_WHYNOT))
    B.append(sec_html("pc-4", "四、三层对照：大公信经 · 三项合一 · 大要理", creeds.SEC_BRIDGE))

    # ── 第五部 逐问解读 ──
    B.append(part_html("p4", "第五部", "逐问解读：196 问全覆盖",
                       "45 个单元，每单元先列该组全部问答的要义，再从五个镜头剖析：本质核心／为什么写·真实论敌／欧陆对读／不同视角·张力／应用。点击标题条展开或收起。"))

    B.append(sec_html("p4-a", "上篇　人当信关于神的什么（问1–90）",
                      topics.INTRO_A
                      + viz("flow", "ordo",
                            "图十一·附　救恩次序流程图（动态流线）。三条泳道：永恒的谕旨、历史的成就、个人的施行——不可互相压缩。")))
    for u in lc1.UNITS:
        toc(3, u["id"], "%s　%s" % (u["rng"], u["title"].split("：")[0]))
        B.append(render_unit(u, open_default=(u["id"] == "u01")))

    B.append(sec_html("p4-b", "中篇　律法与十诫（问91–152）",
                      viz("flow", "tablets",
                          "图十二·附　两块石版。左块对神（问102 爱神），右块对人（问122 爱人如己）。附十诫分法之争的说明。")
                      + topics.INTRO_B))
    for u in lc2.UNITS:
        toc(3, u["id"], "%s　%s" % (u["rng"], u["title"].split("：")[0]))
        B.append(render_unit(u))

    B.append(sec_html("p4-c", "下篇　蒙恩之道与祷告（问153–196）", topics.INTRO_C))
    for u in lc3.UNITS:
        toc(3, u["id"], "%s　%s" % (u["rng"], u["title"].split("：")[0]))
        B.append(render_unit(u))

    # ── 第五部 跨部专题 ──
    B.append(part_html("p5", "第六部", "跨部专题：把线索横着拉一遍",
                       "逐问解读是纵向的。这一部横向切几刀，把散在各处、但必须放在一起才看得懂的线索并排铺开。"))
    for t in topics.TOPICS:
        B.append(sec_html(t["id"], t["title"], t["html"]))

    # ── 第六部 海德堡速背 ──
    B.append(part_html("p6", "第七部", "海德堡速背引擎",
                       "大要理不是为背诵而写的；欧陆改革宗真正的记忆载体是《海德堡要理问答》。这一部提供把它装进长期记忆的最短路径，并逐处标出与大要理的对应。"))
    B.append(sec_html("p6-1", "一、先记住那根骨头：困苦—拯救—感恩",
                      hc.SEC_FRAME
                      + viz("flow", "mindhc",
                            "图十六　海德堡思维导图：一个入口、三根枝、十个挂点。其余 120 问都是这些挂点的展开。")))
    B.append(sec_html("p6-2", "二、六组记忆钩子", hc.SEC_HOOKS))
    B.append(sec_html("p6-3", "三、52 主日互动全图（含大要理对应）", hc.SEC_MAP))
    B.append(sec_html("p6-4", "四、57 张闪卡：翻面 · 首字提示 · 打乱 · 标记背熟", hc.SEC_CARDS))

    # 21 天计划表
    rows = []
    for d, rng, theme, note in hc.PLAN:
        rows.append('<tr><td class="k c">第 %d 天</td><td class="c">%s</td><td>%s</td><td>%s</td></tr>'
                    % (d, rng, theme, note))
    plan_tbl = ('<div class="tablewrap"><table><caption>21 天背熟海德堡 · 间隔重复计划表</caption>'
                '<thead><tr><th style="width:11%">日程</th><th style="width:13%">范围</th>'
                '<th style="width:26%">主题</th><th>今日重点与提示</th></tr></thead><tbody>'
                + "".join(rows) + '</tbody></table></div>' + hc.SEC_PLAN_NOTE)
    B.append(sec_html("p6-5", "五、21 天计划表", plan_tbl))

    # 129 问全表（由 52 主日数据生成）
    rows = []
    secname = {"g": "困苦", "d": "拯救", "t": "感恩"}
    for n, s, q, t, c, w in hc.LORDSDAYS:
        rows.append('<tr><td class="k c">主日 %d</td><td class="c">%s</td><td class="c">问 %s</td>'
                    '<td>%s</td><td>%s</td><td class="note">%s</td></tr>'
                    % (n, secname[s], q, t, c, w))
    tbl129 = ('<p>下表按 52 个主日列出海德堡全部 129 问的分组、主题、核心内容，并给出<b>大要理对应问数</b>。'
              '可用作逐周教理教学的排程表，也可用作两份文件的互查索引。</p>'
              '<div class="tablewrap"><table><caption>海德堡 129 问 · 52 主日全表（含威敏大要理对应）</caption>'
              '<thead><tr><th style="width:8%">主日</th><th style="width:7%">部分</th><th style="width:9%">问数</th>'
              '<th style="width:20%">主题</th><th style="width:38%">核心内容</th><th>大要理对应</th></tr></thead><tbody>'
              + "".join(rows) + '</tbody></table></div>')
    B.append(sec_html("p6-6", "六、129 问全表（按 52 主日 · 附大要理对应）", tbl129))

    # ── 附录 ──
    B.append(part_html("apx", "附录", "术语表 · 单元索引 · 延伸阅读", "查阅用。"))

    grows = []
    for lat, cn, desc in topics.GLOSSARY:
        grows.append('<tr><td class="lt">%s</td><td class="k">%s</td><td>%s</td></tr>' % (lat, cn, desc))
    B.append(sec_html("apx-1", "一、28 条术语表",
                      '<div class="tablewrap"><table><caption>改革宗关键术语（按大要理出现次序大致排列）</caption>'
                      '<thead><tr><th style="width:22%">拉丁／原文</th><th style="width:14%">中文</th>'
                      '<th>释义与出处</th></tr></thead><tbody>' + "".join(grows) + '</tbody></table></div>'))

    irows = []
    for mod, label in ((lc1, "上篇"), (lc2, "中篇"), (lc3, "下篇")):
        for u in mod.UNITS:
            irows.append('<tr><td class="c">%s</td><td class="k"><a href="#%s">%s</a></td><td>%s</td></tr>'
                         % (label, u["id"], u["rng"], u["title"]))
    B.append(sec_html("apx-2", "二、45 个解读单元索引",
                      '<div class="tablewrap"><table><caption>点击问数可直接跳转</caption>'
                      '<thead><tr><th style="width:10%">篇</th><th style="width:16%">问数</th>'
                      '<th>单元主题</th></tr></thead><tbody>' + "".join(irows) + '</tbody></table></div>'))

    B.append(sec_html("apx-3", "三、延伸阅读四步路径", topics.READING))

    # ── 尾 ──
    B.append('''</main></div>
<footer>
<p>《威斯敏斯特大要理问答》1647 年完成，1648 年苏格兰教会大会接纳。本页所列问答为<b>忠实的要义译述</b>，
保留原答的结构、次序与关键措辞，<em>不能替代正式译本</em>；研读与引用请以所在教会采用的标准译本为准。</p>
<p>问 109 已标明 1788 年美国长老会的删改。解读部分为编者依改革宗正统神学与欧陆三项合一信条所作，
凡属传统内的合法分歧（至上论／堕落后论、六日的解释、安息日的严格程度、确信的地位）均已明确标出，不以正统与异端相判。</p>
<p class="note">纯静态单页 · 无外部字体与脚本请求 · 可离线保存 · 支持浅／深／跟随系统三态主题 · 附 A4 打印样式</p>
</footer>
<button class="toTop" id="toTop" data-act="top" aria-label="回到顶部">↑</button>
<button class="tocFab" data-act="toc" aria-label="显示目录">☰ 目录</button>''')

    body = "".join(B)

    # ── 目录 ──
    tl = []
    for lv, anchor, label in TOC:
        if lv == 1:
            tl.append('<li class="lv1"><a href="#%s">%s</a></li>' % (anchor, label))
        elif lv == 2:
            tl.append('<li><a href="#%s">%s</a></li>' % (anchor, label))
        else:
            tl.append('<li class="lv3"><a href="#%s">%s</a></li>' % (anchor, label))
    body = body.replace("__TOC__", "".join(tl))

    favicon = ("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E"
               "%3Crect width=%2732%27 height=%2732%27 rx=%276%27 fill=%27%231f3a5f%27/%3E"
               "%3Ctext x=%2716%27 y=%2723%27 font-size=%2720%27 text-anchor=%27middle%27 fill=%27%23c9a227%27"
               " font-family=%27serif%27%3E%E5%A4%A7%3C/text%3E%3C/svg%3E")

    html = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>威斯敏斯特大要理问答全解 · 196问 · 欧陆改革宗视角 · 附海德堡速背</title>
<meta name="description" content="《威斯敏斯特大要理问答》196问全覆盖解读：整本圣经视角、历史情境、逐组剖析、欧陆改革宗对读、多重视角与应用；含12幅图表与海德堡要理问答52主日互动地图、57张闪卡与21天背诵计划。">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="%s">
<style>%s</style>
</head>
<body>
%s
%s
<script>%s</script>
</body>
</html>""" % (favicon, CSS, body, hc.data_script(lc2.DECA) + '<script>' + history.monarchs_js() + history.histcards_js() + history.eras_js() + history.events_js() + '</script>', JS)

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site", "index.html")
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("written:", out)
    print("bytes:", len(html.encode("utf-8")))
    cn = sum(1 for ch in html if "\u4e00" <= ch <= "\u9fff")
    print("chinese chars:", cn)
    print("toc entries:", len(TOC))


if __name__ == "__main__":
    build()
