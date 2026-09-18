# -*- coding: utf-8 -*-
"""地图模块：四幅手绘示意地图，纯 SVG、CSS 变量着色、零外部请求。
坐标由经纬度线性投影而来，轮廓为简化示意，不作测绘用途。"""

from charts import _svg


def P(lon, lat):
    """经纬度 → 画布坐标。x=(lon+10.5)*23.5，y=(59.5-lat)*24+50（近似等距圆柱）。"""
    return ((lon + 10.5) * 23.5, (59.5 - lat) * 24.0 + 50.0)


def _path(pts, close=True):
    d = "M%.1f,%.1f " % P(*pts[0]) + " ".join("L%.1f,%.1f" % P(*q) for q in pts[1:])
    return d + (" Z" if close else "")


def _pt(lon, lat):
    x, y = P(lon, lat)
    return "%.1f,%.1f" % (x, y)


# ── 简化轮廓 ───────────────────────────────────────────────────
GB = [(-5.0, 58.6), (-3.0, 58.64), (-2.1, 57.15), (-2.5, 56.05), (-2.0, 55.77), (-1.6, 55.0),
      (-0.08, 54.1), (0.3, 52.9), (1.75, 52.48), (1.4, 51.4), (0.25, 50.74), (-1.3, 50.6),
      (-4.1, 50.37), (-5.7, 50.07), (-4.5, 51.3), (-5.3, 51.9), (-4.4, 52.4), (-4.5, 53.35),
      (-3.0, 53.4), (-3.6, 54.9), (-5.8, 55.3), (-6.3, 55.85), (-6.2, 57.35)]
IE = [(-7.4, 55.4), (-5.9, 54.6), (-6.26, 53.35), (-6.4, 52.3), (-8.5, 51.9), (-9.9, 52.1),
      (-9.1, 53.3), (-8.6, 54.3)]
FR = [(1.9, 50.96), (3.06, 50.6), (6.1, 49.6), (7.75, 48.57), (7.59, 47.56), (6.14, 46.20),
      (7.3, 43.7), (5.4, 43.3), (3.0, 42.7), (-1.5, 43.5), (-0.6, 44.8), (-1.6, 47.2),
      (-4.5, 48.4), (-1.6, 49.7), (0.1, 49.5)]
LC = [(2.9, 51.2), (4.35, 50.85), (5.7, 50.85), (5.9, 52.0), (6.57, 53.22), (4.8, 53.1),
      (4.9, 52.37), (4.4, 51.9), (4.4, 51.22)]
DE = [(6.57, 53.22), (7.21, 53.37), (10.0, 53.55), (10.7, 53.87), (14.55, 53.43), (17.0, 51.1),
      (16.4, 48.2), (11.6, 48.14), (8.54, 47.37), (7.59, 47.56), (7.75, 48.57), (6.1, 49.6),
      (5.7, 50.85), (5.9, 52.0)]
CH = [(7.59, 47.56), (8.54, 47.37), (9.5, 46.85), (9.0, 46.0), (6.14, 46.20), (6.9, 47.0)]
IT = [(7.7, 45.07), (9.2, 45.46), (12.3, 45.44), (13.8, 45.65), (13.5, 43.6), (14.6, 41.9),
      (12.5, 41.9), (10.4, 43.7), (8.9, 44.4)]
IB = [(-2.9, 43.3), (2.2, 41.4), (-1.0, 41.0), (-6.0, 41.0), (-8.6, 41.1), (-8.4, 43.4)]
DK = [(8.1, 56.3), (8.5, 57.6), (10.6, 57.5), (10.8, 56.2), (9.9, 54.9), (8.6, 55.3)]
RHINE = [(7.59, 47.56), (7.75, 48.57), (8.43, 49.32), (8.27, 50.0), (7.6, 50.36), (6.96, 50.94),
         (5.9, 52.0), (4.67, 51.81)]


def _base(full=True):
    parts = [GB, IE, FR, LC, DE, CH, DK] + ([IT, IB] if full else [])
    return "".join('<path d="%s" class="mp land"/>' % _path(q) for q in parts)


def _city(lon, lat, name, note="", cls="c1", dx=7, dy=-7, anchor="start", r=4.2, pulse=False):
    x, y = P(lon, lat)
    o = ['<circle cx="%.1f" cy="%.1f" r="%.1f" class="mpt %s%s"/>' % (x, y, r, cls, " pulse" if pulse else "")]
    o.append('<text x="%.1f" y="%.1f" class="mlab" text-anchor="%s">%s</text>'
             % (x + dx, y + dy, anchor, name))
    if note:
        o.append('<text x="%.1f" y="%.1f" class="mnote" text-anchor="%s">%s</text>'
                 % (x + dx, y + dy + 12, anchor, note))
    return "".join(o)


def _arc(a, b, cls="marr", bend=0.22, flow=False):
    x1, y1 = P(*a)
    x2, y2 = P(*b)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    cx, cy = mx - dy * bend, my + dx * bend
    return '<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" class="%s%s"/>' % (
        x1, y1, cx, cy, x2, y2, cls, " flow" if flow else "")


# ═════════════ 图 1：宗教改革的欧洲 ═════════════
def map_reformation():
    b = ['<text class="t" x="16" y="24">宗教改革的欧洲 · 1517–1648　（示意图）</text>',
         '<text class="xs" x="16" y="42">蓝线为莱茵河。三项合一信条全部诞生在这条河的沿线与它的入海口三角洲。</text>',
         '<rect x="0" y="52" width="720" height="448" class="sea"/>', _base()]
    b.append('<path d="%s" class="river"/>' % _path(RHINE, close=False))
    rx, ry = P(6.5, 51.2)
    b.append('<text x="%.1f" y="%.1f" class="mriver" transform="rotate(-64 %.1f %.1f)">莱 茵 河</text>'
             % (rx + 6, ry, rx + 6, ry))
    for lon, lat, t in ((14.8, 49.6, "德意志诸邦"), (1.2, 46.6, "法兰西"), (-1.5, 53.0, "英格兰"),
                        (-4.4, 57.5, "苏格兰"), (-8.3, 54.6, "爱尔兰"), (5.6, 52.9, "低地国家"),
                        (-4.8, 41.6, "西班牙"), (12.4, 43.0, "意大利"), (10.6, 45.8, "瑞士"),
                        (9.5, 56.5, "丹麦")):
        px, py = P(lon, lat)
        b.append('<text x="%.1f" y="%.1f" class="mreg" text-anchor="middle">%s</text>' % (px, py, t))
    b.append(_city(12.65, 51.87, "威登堡", "1517 九十五条", "c4"))
    b.append(_city(6.14, 46.20, "日内瓦", "加尔文 · 1536/1559《要义》", "c2", dx=-9, anchor="end", pulse=True))
    b.append(_city(8.68, 49.41, "海德堡", "1563 海德堡要理问答", "c2", dx=9, dy=6, pulse=True))
    b.append(_city(4.67, 51.81, "多特", "1618–19 多特会议", "c2", dx=-9, dy=-8, anchor="end", pulse=True))
    b.append(_city(3.39, 50.60, "图尔奈", "1561 比利时信条 · 德布莱", "c2", dx=-9, dy=18, anchor="end", pulse=True))
    b.append(_city(7.21, 53.37, "埃姆登", "1571 会议：两文件成为标准", "c2", dy=-9))
    b.append(_city(7.75, 48.57, "斯特拉斯堡", "布塞", "c3", dx=-10, dy=-6, anchor="end"))
    b.append(_city(8.54, 47.37, "苏黎世", "慈运理 · 布灵格", "c3", dx=10, dy=10))
    b.append(_city(-0.13, 51.51, "伦敦 · 威斯敏斯特", "1643–49 会议", "c1", dx=-9, dy=-9, anchor="end", r=5.8, pulse=True))
    b.append(_city(-3.19, 55.95, "爱丁堡", "1638 国民圣约", "c1", dx=10, dy=-6))
    b.append(_city(-6.26, 53.35, "都柏林", "", "c1", dx=9, dy=14))
    b.append(_city(11.12, 46.07, "特伦特", "1545–63 天主教会议", "c5", dx=10, dy=6))
    b.append(_city(12.50, 41.90, "罗马", "", "c5"))
    b.append(_city(2.35, 48.86, "巴黎", "1559 法国改革宗信条", "c3", dx=-9, dy=16, anchor="end"))
    b.append('<rect x="14" y="510" width="692" height="26" rx="7" class="mleg"/>')
    for i, (cls, t) in enumerate((("c2", "三项合一信条的诞生地"), ("c1", "威斯敏斯特一系"),
                                  ("c4", "路德宗源头"), ("c3", "其他改革宗中心"), ("c5", "罗马天主教"))):
        x = 30 + i * 138
        b.append('<circle cx="%d" cy="523" r="4.2" class="mpt %s"/>' % (x, cls))
        b.append('<text x="%d" y="527" class="mnote">%s</text>' % (x + 11, t))
    b.append('<text class="sm" x="16" y="558">日内瓦→海德堡→多特，直线距离不到 600 公里。'
             '<tspan class="k">整个欧陆改革宗的文献传统，是沿着莱茵河这一条窄带完成的</tspan>——而威敏在海峡对岸。</text>')
    return _svg("0 0 720 570", "".join(b))


# ═════════════ 图 2：马利亚流亡者 ═════════════
def map_exiles():
    b = ['<text class="t" x="16" y="24">马利亚流亡者的出走与归来 · 1553–1559　（示意图）</text>',
         '<text class="xs" x="16" y="42">这是英格兰清教主义真正的种子：数百人去看过日内瓦，回来就再也不满足于「折中」。</text>',
         '<rect x="0" y="52" width="720" height="356" class="sea"/>', _base(full=False)]
    dests = [((7.75, 48.57), "斯特拉斯堡", 16), ((8.68, 50.11), "法兰克福", -9),
             ((8.54, 47.37), "苏黎世", 6), ((7.59, 47.56), "巴塞尔", 22),
             ((6.14, 46.20), "日内瓦", -9), ((7.21, 53.37), "埃姆登", -9)]
    for (lon, lat), nm, dy in dests:
        b.append(_arc((-0.13, 51.51), (lon, lat), "marr out", 0.15, flow=True))
    b.append(_arc((6.14, 46.20), (-0.13, 51.51), "marr back", -0.3))
    b.append(_city(-0.13, 51.51, "伦敦", "1553 玛丽登基，约三百人被烧", "c5", dx=-9, dy=-10, anchor="end", r=6))
    for (lon, lat), nm, dy in dests:
        big = nm == "日内瓦"
        b.append(_city(lon, lat, nm, "《日内瓦圣经》1560" if big else "",
                       "c2" if big else "c3", dx=10, dy=dy, r=5.8 if big else 4.2, pulse=big))
    px, py = P(1.4, 47.6)
    b.append('<text x="%.1f" y="%.1f" class="mnote fe">1559 伊丽莎白登基后陆续归国</text>' % (px, py))
    b.append('<text class="sm" x="16" y="434">在日内瓦，他们亲眼看见一间<tspan class="k">按圣经治理与敬拜</tspan>的教会：'
             '长老治会、惩戒、诗篇歌唱、以讲道为中心。八十四年后，这些人的属灵后裔坐在了威斯敏斯特礼拜堂里。</text>')
    return _svg("0 0 720 446", "".join(b))


# ═════════════ 图 3：三个王国 ═════════════
def map_britain():
    def Q(lon, lat):
        return ((lon + 11) * 38.0, (59.5 - lat) * 38.0 + 30.0)

    def qpath(pts):
        return "M%.1f,%.1f " % Q(*pts[0]) + " ".join("L%.1f,%.1f" % Q(*q) for q in pts[1:]) + " Z"

    def city(lon, lat, nm, note="", cls="c1", dx=9, dy=-7, anchor="start", r=4.6, pulse=False):
        x, y = Q(lon, lat)
        o = ['<circle cx="%.1f" cy="%.1f" r="%.1f" class="mpt %s%s"/>' % (x, y, r, cls, " pulse" if pulse else "")]
        o.append('<text x="%.1f" y="%.1f" class="mlab" text-anchor="%s">%s</text>' % (x + dx, y + dy, anchor, nm))
        if note:
            o.append('<text x="%.1f" y="%.1f" class="mnote" text-anchor="%s">%s</text>' % (x + dx, y + dy + 12, anchor, note))
        return "".join(o)

    b = ['<text class="t" x="16" y="24">三个王国，一场危机 · 1637–1649　（示意图）</text>',
         '<text class="xs" x="16" y="42">《庄严同盟与圣约》要求三国教会在教义、敬拜、纪律、治理上归于一致——威斯敏斯特会议就是执行这一条的机构。</text>',
         '<rect x="0" y="52" width="512" height="400" class="sea"/>']
    b.append('<path d="%s" class="mp land"/>' % qpath(GB))
    b.append('<path d="%s" class="mp land"/>' % qpath(IE))
    x1, y1 = Q(-3.6, 54.9); x2, y2 = Q(-2.0, 55.77)
    b.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="mborder"/>' % (x1, y1, x2, y2))
    for lon, lat, t in ((-4.5, 57.1, "苏格兰"), (-1.4, 53.35, "英格兰"), (-8.2, 53.6, "爱尔兰"), (-3.9, 52.45, "威尔士")):
        px, py = Q(lon, lat)
        b.append('<text x="%.1f" y="%.1f" class="mreg" text-anchor="middle">%s</text>' % (px, py, t))
    b.append(city(-3.19, 55.95, "爱丁堡", "1637 祈祷书暴动 · 1638 国民圣约", "c2", dx=10, dy=-8, r=6.2, pulse=True))
    b.append(city(-4.25, 55.86, "格拉斯哥", "1638 大会废除主教制", "c2", dx=-10, dy=16, anchor="end"))
    b.append(city(-1.60, 55.00, "纽卡斯尔", "1640 苏格兰军南下", "c2", dx=10, dy=-4))
    b.append(city(-1.20, 53.97, "马斯顿荒原", "1644 议会军决定性胜利", "c4", dx=10, dy=2))
    b.append(city(-0.99, 52.40, "纳西比", "1645 保王党主力覆灭", "c4", dx=-10, dy=-6, anchor="end"))
    b.append(city(-1.26, 51.75, "牛津", "1642–46 保王党首都", "c5", dx=-10, dy=8, anchor="end"))
    b.append(city(0.12, 52.21, "剑桥", "塔克尼：大要理主笔", "c3", dx=10, dy=-6))
    b.append(city(-0.13, 51.51, "伦敦 · 威斯敏斯特", "1643–49 会议开了千余次", "c1", dx=10, dy=20, r=6.8, pulse=True))
    b.append(city(-6.26, 53.35, "都柏林", "1641 爱尔兰起义", "c5", dx=-10, anchor="end"))
    b.append('<rect x="520" y="60" width="192" height="236" rx="9" class="mleg"/>')
    b.append('<text x="534" y="82" class="mlab fc">因果链 · 十二年</text>')
    chain = ["1637 强推祈祷书（爱丁堡）", "1638 国民圣约（苏格兰）", "1639/40 主教战争",
             "1640 被迫召长期议会", "1642 内战爆发", "1643 庄严同盟与圣约",
             "1643 威斯敏斯特会议开议", "1646 信条完成", "1647 大要理完成", "1649 查理一世被处决"]
    for i, t in enumerate(chain):
        y = 104 + i * 19
        b.append('<circle cx="540" cy="%d" r="3.2" class="mpt c1"/>' % (y - 4))
        b.append('<text x="551" y="%d" class="mnote">%s</text>' % (y, t))
        if i < len(chain) - 1:
            b.append('<line x1="540" y1="%d" x2="540" y2="%d" class="mchain"/>' % (y - 1, y + 12))
    b.append('<text class="sm" x="16" y="476">一条最容易被忽略的线索：'
             '<tspan class="k">整场危机是从苏格兰烧起来的，不是从英格兰。</tspan>'
             '查理若不强推祈祷书，就没有国民圣约；没有圣约，议会就没有筹码换取苏格兰出兵；没有那笔交易，就没有威斯敏斯特会议。</text>')
    return _svg("0 0 720 488", "".join(b))


# ═════════════ 图 4：全球传播 ═════════════
def map_spread():
    b = ['<text class="t" x="16" y="24">威斯敏斯特准则的传播 · 1648 至今　（示意图）</text>',
         '<text class="xs" x="16" y="42">它在英格兰被废（1662），却经苏格兰走向了全世界。今日全球长老宗的信条根源都在这条线上。</text>']
    b.append('<rect x="0" y="52" width="720" height="372" class="sea"/>')
    # 极简世界陆块
    blobs = [
        ("M60,150 L150,120 L215,132 L240,178 L205,214 L150,236 L96,220 L62,186 Z", "北美"),
        ("M170,250 L215,238 L236,282 L222,344 L188,376 L162,336 L156,288 Z", "南美"),
        ("M300,120 L372,104 L420,124 L432,166 L400,190 L340,186 L300,160 Z", "欧洲"),
        ("M320,196 L400,190 L436,230 L424,300 L380,344 L336,316 L310,252 Z", "非洲"),
        ("M436,110 L560,96 L640,124 L648,180 L592,208 L500,196 L444,162 Z", "亚洲"),
        ("M566,278 L640,268 L668,300 L650,336 L590,340 L560,312 Z", "澳洲"),
    ]
    for d, nm in blobs:
        b.append('<path d="%s" class="mp land"/>' % d)
    def node(x, y, nm, note, cls="c3", dx=8, dy=-6, anchor="start", r=4.4, pulse=False):
        o = ['<circle cx="%d" cy="%d" r="%.1f" class="mpt %s%s"/>' % (x, y, r, cls, " pulse" if pulse else "")]
        o.append('<text x="%d" y="%d" class="mlab" text-anchor="%s">%s</text>' % (x + dx, y + dy, anchor, nm))
        o.append('<text x="%d" y="%d" class="mnote" text-anchor="%s">%s</text>' % (x + dx, y + dy + 12, anchor, note))
        return "".join(o)
    SRC = (352, 130)
    targets = [(200, 170, "北美殖民地", "1729 采纳 · 1788 修订", "c2", 8, -6, "start", 5.4, True),
               (330, 138, "爱尔兰", "长老会", "c3", -8, 24, "end", 4, False),
               (612, 300, "澳洲 · 新西兰", "19 世纪移民带入", "c3", -8, -6, "end", 4, False),
               (372, 300, "非洲南部", "宣教与移民", "c3", 8, -6, "start", 4, False),
               (600, 150, "韩国 · 印尼 · 华人教会", "20 世纪宣教果实", "c3", -8, 26, "end", 4.6, False),
               (192, 300, "巴西 · 墨西哥", "拉美长老会", "c3", 8, -6, "start", 4, False)]
    for x, y, nm, note, cls, dx, dy, an, r, pu in targets:
        mx, my = (SRC[0] + x) / 2, (SRC[1] + y) / 2
        b.append('<path d="M%d,%d Q%.0f,%.0f %d,%d" class="marr out flow"/>'
                 % (SRC[0], SRC[1], mx, my - 46, x, y))
        b.append(node(x, y, nm, note, cls, dx, dy, an, r, pu))
    b.append(node(SRC[0], SRC[1], "苏格兰", "1648 接纳 · 1690 立为国教信条", "c1", -8, -8, "end", 6.4, True))
    b.append('<text class="sm" x="16" y="404">一个值得记住的反讽：'
             '<tspan class="k">写它的国家废了它，接纳它的邻国把它传遍了世界。</tspan>'
             '今日 OPC、PCA、韩国长老会、华人改革宗教会所持守的，都是 1648 年那一份。</text>')
    return _svg("0 0 720 418", "".join(b))


MAPS = {"reformation": map_reformation, "exiles": map_exiles,
        "britain": map_britain, "spread": map_spread}
