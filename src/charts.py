# -*- coding: utf-8 -*-
"""手写 SVG 图示。全部用 CSS 变量着色，自动适配浅／深主题。"""

import re

SPRITE = """<svg width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute"><defs>
<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
  <path d="M0,0 L10,5 L0,10 z" fill="var(--gold)"/></marker>
<marker id="ahn" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
  <path d="M0,0 L10,5 L0,10 z" fill="var(--navy-2)"/></marker>
<marker id="ahg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
  <path d="M0,0 L10,5 L0,10 z" fill="var(--green)"/></marker>
</defs></svg>"""


def _cw(ch):
    """粗略字宽（font-size 11px）。"""
    if "\u4e00" <= ch <= "\u9fff" or ch in "，。：；、（）「」《》·？！…—　“”":
        return 11.2
    if ch in "0123456789":
        return 6.2
    return 5.8


def _wrap_sm(body, vw=720.0, pad=16.0, lh=15.0):
    """把 <text class="sm"> 的长句按可用宽度折成多行 tspan，返回 (新body, 额外高度)。
    SVG 的 text 不会自动换行，长注释必须在生成期折行，否则出框被 figure 裁掉。"""
    pat = re.compile(r'<text class="sm" x="([\d.]+)" y="([\d.]+)">(.*?)</text>', re.S)
    extra = [0.0]

    def repl(m):
        x, y, inner = float(m.group(1)), m.group(2), m.group(3)
        avail = vw - x - pad
        # 切成 (字符, tspan属性) 序列，保留内嵌 <tspan class="k"> 标记
        toks, runs = re.split(r'(<tspan[^>]*>.*?</tspan>)', inner, flags=re.S), []
        for t in toks:
            if not t:
                continue
            mm = re.match(r'<tspan([^>]*)>(.*?)</tspan>', t, re.S)
            if mm:
                for ch in mm.group(2):
                    runs.append((ch, mm.group(1)))
            else:
                for ch in t:
                    runs.append((ch, None))
        # 贪心折行
        lines, cur, w = [], [], 0.0
        for ch, attr in runs:
            cwi = _cw(ch)
            if w + cwi > avail and cur:
                lines.append(cur); cur, w = [], 0.0
            cur.append((ch, attr)); w += cwi
        if cur:
            lines.append(cur)
        if len(lines) <= 1:
            return m.group(0)
        extra[0] = max(extra[0], (len(lines) - 1) * lh)
        out = ['<text class="sm" x="%s" y="%s">' % (m.group(1), y)]
        for i, ln in enumerate(lines):
            out.append('<tspan x="%s" dy="%s">' % (m.group(1), 0 if i == 0 else lh))
            buf, cattr = [], "###"
            for ch, attr in ln:
                if attr != cattr:
                    if buf:
                        out.append(('<tspan%s>%s</tspan>' % (cattr, "".join(buf))) if cattr else "".join(buf))
                    buf, cattr = [], attr
                buf.append(ch)
            if buf:
                out.append(('<tspan%s>%s</tspan>' % (cattr, "".join(buf))) if cattr else "".join(buf))
            out.append('</tspan>')
        out.append('</text>')
        return "".join(out)

    return pat.sub(repl, body), extra[0]


_KEY = {"cur": "x"}


def _svg(vb, body, h=None):
    body, extra = _wrap_sm(body)
    if extra:
        a, bb, c, d = [float(v) for v in vb.split()]
        vb = "%g %g %g %g" % (a, bb, c, d + extra)
    return ('<svg class="sv" viewBox="%s" xmlns="http://www.w3.org/2000/svg" role="img">'
            '%s</svg>') % (vb, body)


def fig_bible():
    """整本圣经一条主线，并标出大要理落在哪一格。"""
    steps = [
        ("创造", "神照自己形像造人，立行为之约", "问15–20", "bxn"),
        ("堕落", "始祖违约，全人类在亚当里沉沦", "问21–29", "bxc"),
        ("应许", "恩典之约：一位中保被应许", "问30–35", "bxg"),
        ("道成肉身", "中保基督：二性一位，三职二态", "问36–56", "bxn"),
        ("施行", "有效恩召·称义·收纳·成圣·坚忍", "问57–90", "bxe"),
        ("回应", "律法·蒙恩之道·祷告，感恩的生活", "问91–196", "bxg"),
        ("成全", "身体复活，公开宣判，永远荣耀", "问86–90", "bxn"),
    ]
    b = ['<text class="t" x="16" y="24">整本圣经一条主线　·　大要理 196 问在这条线上的位置</text>']
    b.append('<line class="ln" x1="20" y1="58" x2="700" y2="58"/>')
    x = 20
    w = 92
    for i, (name, desc, rng, cls) in enumerate(steps):
        b.append('<circle cx="%d" cy="58" r="7" class="%s"/>' % (x + w // 2, cls))
        b.append('<rect x="%d" y="76" width="%d" height="72" rx="7" class="%s"/>' % (x, w - 8, cls))
        b.append('<text class="k" x="%d" y="96" text-anchor="middle">%s</text>' % (x + (w - 8) // 2, name))
        b.append('<text class="xs" x="%d" y="112" text-anchor="middle">%s</text>' % (x + (w - 8) // 2, rng))
        for j, line in enumerate(_wrap(desc, 7)):
            b.append('<text class="xs" x="%d" y="%d" text-anchor="middle">%s</text>'
                     % (x + (w - 8) // 2, 128 + j * 13, line))
        if i < len(steps) - 1:
            b.append('<path class="ar" d="M%d,58 L%d,58"/>' % (x + w - 4, x + w + 6))
        x += w + 5
    b.append('<text class="sm" x="20" y="176">大要理不是从「我的需要」起步，而是从「神的荣耀」起步；'
             '它把人放回这条历史线上，先问「你信谁」，再问「你当如何活」。</text>')
    return _svg("0 0 720 190", "".join(b))


def _wrap(s, n):
    return [s[i:i + n] for i in range(0, len(s), n)]


def fig_structure():
    """196 问的两大部比例与十三个分组。"""
    groups = [
        ("问1–5", 5, "根基：目的与准则", "bxg"),
        ("问6–20", 15, "神·谕旨·创造·护理", "bxn"),
        ("问21–29", 9, "堕落与罪的刑罚", "bxc"),
        ("问30–35", 6, "恩典之约", "bxg"),
        ("问36–56", 21, "中保基督", "bxn"),
        ("问57–90", 34, "救赎的施行", "bxe"),
        ("问91–100", 10, "律法总论", "bxg"),
        ("问101–148", 48, "十诫逐诫", "bxc"),
        ("问149–152", 4, "罪与刑罚", "bxc"),
        ("问153–177", 25, "蒙恩之道", "bxe"),
        ("问178–196", 19, "祷告与主祷文", "bxn"),
    ]
    total = sum(g[1] for g in groups)
    b = ['<text class="t" x="16" y="22">196 问的骨架比例　·　为什么说大要理是「教理讲章的纲目」</text>']
    b.append('<text class="xs" x="16" y="42">上条＝两大部；下条＝十一个分组，宽度按问数真实成比例</text>')
    # 两大部
    w1 = int(680 * 90 / 196.0)
    b.append('<rect x="20" y="56" width="%d" height="30" rx="5" class="bxn"/>' % w1)
    b.append('<rect x="%d" y="56" width="%d" height="30" rx="5" class="bxg"/>' % (20 + w1 + 3, 680 - w1 - 3))
    b.append('<text class="k" x="%d" y="76" text-anchor="middle">人当信神什么（问6–90，85问）</text>' % (20 + w1 // 2))
    b.append('<text class="k" x="%d" y="76" text-anchor="middle">神向人要求什么本分（问91–196，106问）</text>'
             % (20 + w1 + 3 + (680 - w1 - 3) // 2))
    # 分组
    x = 20.0
    for rng, n, name, cls in groups:
        w = 680.0 * n / total
        b.append('<rect x="%.1f" y="102" width="%.1f" height="34" rx="4" class="%s"/>' % (x, max(w - 2, 4), cls))
        if w > 42:
            b.append('<text class="xs" x="%.1f" y="117" text-anchor="middle">%s</text>' % (x + w / 2, rng))
            b.append('<text class="xs" x="%.1f" y="130" text-anchor="middle">%s</text>'
                     % (x + w / 2, name if len(name) <= 7 else name[:6] + "…"))
        x += w
    b.append('<text class="sm" x="20" y="160">十诫一段独占 48 问（占全篇四分之一），蒙恩之道与祷告合占 44 问。'
             '这个比例本身就是宣告：正统不是思辨的陈列，而是要落在良心与生活上。</text>')
    return _svg("0 0 720 175", "".join(b))


def fig_purpose():
    """Q1 目的论的推论链。"""
    b = ['<text class="t" x="16" y="22">问1 的一根链条：为什么「荣耀神」必然带出「以祂为乐」</text>']
    nodes = [("神是自有永有", "祂的荣耀不能增添", 20),
             ("人是受造的形像", "人的存在为反照祂", 190),
             ("荣耀祂＝作祂所造之用", "本分", 360),
             ("作祂所造之用＝人的至福", "享受", 530)]
    for i, (t1, t2, x) in enumerate(nodes):
        cls = "bxn" if i % 2 == 0 else "bxg"
        b.append('<rect x="%d" y="44" width="160" height="58" rx="7" class="%s"/>' % (x, cls))
        b.append('<text class="k" x="%d" y="66" text-anchor="middle" font-size="12">%s</text>' % (x + 80, t1))
        b.append('<text class="xs" x="%d" y="84" text-anchor="middle">%s</text>' % (x + 80, t2))
        if i < 3:
            b.append('<path class="ar" d="M%d,73 L%d,73"/>' % (x + 162, x + 178))
    b.append('<rect x="150" y="122" width="420" height="42" rx="7" class="bxc"/>')
    b.append('<text class="k" x="360" y="140" text-anchor="middle">'
             '结论：本分与幸福不是两件事，而是一件事的两面</text>')
    b.append('<text class="xs" x="360" y="156" text-anchor="middle">'
             '海德堡问1 从「安慰」进，大要理问1 从「目的」进——同一扇门的两侧把手</text>')
    b.append('<path class="dash" d="M360,104 L360,120"/>')
    return _svg("0 0 720 178", "".join(b))


def fig_mediator():
    """中保推论链 问36–45。"""
    b = ['<text class="t" x="16" y="22">中保的推论链　·　问36–45 为何必须是「神而人」</text>']
    chain = [("必须是人", "才能受苦、顺服、代表人", "问39", "bxg", 20, 50),
             ("必须是神", "才能担当神的忿怒、赋无限价值", "问38", "bxn", 20, 122),
             ("必须是一位", "两性合于一位，作为才归于全体", "问40–41", "bxc", 250, 86)]
    for t1, t2, q, cls, x, y in chain:
        b.append('<rect x="%d" y="%d" width="200" height="58" rx="7" class="%s"/>' % (x, y, cls))
        b.append('<text class="k" x="%d" y="%d" text-anchor="middle">%s　<tspan class="xs">%s</tspan></text>'
                 % (x + 100, y + 23, t1, q))
        b.append('<text class="xs" x="%d" y="%d" text-anchor="middle">%s</text>' % (x + 100, y + 42, t2))
    b.append('<path class="ar" d="M222,79 L246,105"/>')
    b.append('<path class="ar" d="M222,151 L246,125"/>')
    b.append('<path class="ar" d="M452,115 L482,115"/>')
    offices = [("先知", "以言语与灵启示神的旨意", "问43"),
               ("祭司", "一次献己为祭，常作代求", "问44"),
               ("君王", "召聚、治理、护卫、审判", "问45")]
    for i, (n, d, q) in enumerate(offices):
        b.append('<rect x="488" y="%d" width="212" height="48" rx="7" class="bxe"/>' % (46 + i * 58))
        b.append('<text class="k" x="500" y="%d">%s　<tspan class="xs">%s</tspan></text>' % (66 + i * 58, n, q))
        b.append('<text class="xs" x="500" y="%d">%s</text>' % (82 + i * 58, d))
    b.append('<text class="sm" x="20" y="216">大要理不把「基督论」当抽象位格学：它先问「我们需要怎样一位中保」，'
             '再由需要推出位格，由位格推出三职——救恩论倒逼出基督论，而不是相反。</text>')
    return _svg("0 0 720 228", "".join(b))


def fig_states():
    """基督二态阶梯 问46–56。"""
    b = ['<text class="t" x="16" y="22">二态的阶梯　·　问46–56：降卑与升高各四级</text>']
    down = ["成孕降生（问47）", "生在律法下，受今生苦难（问48）", "受死（问49）", "死后葬、居于死权之下至第三日（问50）"]
    up = ["复活（问52）", "升天（问53）", "坐在神右边（问54）", "再来审判（问56）"]
    for i, t in enumerate(down):
        y = 46 + i * 34
        b.append('<rect x="20" y="%d" width="300" height="28" rx="5" class="bxc"/>' % y)
        b.append('<text class="xs" x="34" y="%d">%s</text>' % (y + 18, t))
        b.append('<path class="ln" d="M%d,%d L%d,%d"/>' % (26 + i * 6, y + 28, 26 + i * 6, y + 34))
    for i, t in enumerate(up):
        y = 148 - i * 34
        b.append('<rect x="400" y="%d" width="300" height="28" rx="5" class="bxn"/>' % y)
        b.append('<text class="xs" x="414" y="%d">%s</text>' % (y + 18, t))
    b.append('<path class="ar" d="M330,166 Q360,180 394,166"/>')
    b.append('<text class="xs" x="360" y="196" text-anchor="middle">同一位中保　同一条路</text>')
    b.append('<text class="sm" x="20" y="218">降卑之末即升高之始。大要理把「降在阴间」处理为「死的权下、至第三日」'
             '（问50），刻意避开中世纪「地狱之游」的想像——与海德堡问44 把它解为十架上的极苦，路线不同、用意相通。</text>')
    return _svg("0 0 720 232", "".join(b))


def fig_union():
    """与基督联合为轴心的恩惠辐射。"""
    b = ['<text class="t" x="16" y="22">恩惠的轴心　·　问65–90：一切益处都从「与基督联合」辐射出来</text>']
    b.append('<circle cx="360" cy="128" r="56" class="bxc"/>')
    b.append('<text class="k" x="360" y="122" text-anchor="middle">与基督联合</text>')
    b.append('<text class="xs" x="360" y="140" text-anchor="middle">问66　unio cum Christo</text>')
    ring = [("有效恩召", "问67–68", 360, 40), ("称义", "问70–73", 596, 78),
            ("收纳", "问74", 640, 160), ("成圣", "问75–78", 500, 214),
            ("坚忍", "问79", 220, 214), ("确信", "问80–81", 80, 160),
            ("死时得释", "问85–86", 124, 78)]
    for n, q, x, y in ring:
        b.append('<rect x="%d" y="%d" width="98" height="40" rx="7" class="bxn"/>' % (x - 49, y - 20))
        b.append('<text class="k" x="%d" y="%d" text-anchor="middle" font-size="12">%s</text>' % (x, y - 2, n))
        b.append('<text class="xs" x="%d" y="%d" text-anchor="middle">%s</text>' % (x, y + 13, q))
        b.append('<path class="dash" d="M360,128 L%d,%d"/>' % (x, y))
    b.append('<text class="sm" x="16" y="258">这是欧陆改革宗读威敏最愿意认领的一段：称义与成圣不是先后两笔交易，'
             '而是同一个联合的两个不可分的面向——避免了律法主义，也避免了反律主义。</text>')
    return _svg("0 0 720 272", "".join(b))


def fig_law3():
    """律法三用。"""
    uses = [("第一用　镜子", "显明罪，夺去自义", "usus elenchticus", "问95", "bxc"),
            ("第二用　缰绳", "约束外在的恶，护卫社会", "usus politicus", "问95", "bxg"),
            ("第三用　规范", "指引已得救者感恩而行", "usus normativus", "问97", "bxe")]
    b = ['<text class="t" x="16" y="22">律法的三种用处　·　问93–97 与海德堡问115 的同一条路</text>']
    for i, (n, d, lat, q, cls) in enumerate(uses):
        x = 20 + i * 234
        b.append('<rect x="%d" y="42" width="216" height="96" rx="8" class="%s"/>' % (x, cls))
        b.append('<text class="k" x="%d" y="66" text-anchor="middle">%s</text>' % (x + 108, n))
        b.append('<text class="xs" x="%d" y="86" text-anchor="middle">%s</text>' % (x + 108, d))
        b.append('<text class="xs" x="%d" y="104" text-anchor="middle" font-style="italic">%s</text>' % (x + 108, lat))
        b.append('<text class="xs" x="%d" y="124" text-anchor="middle">%s</text>' % (x + 108, q))
    b.append('<text class="sm" x="20" y="162">威敏把十诫放在「本分」部，海德堡把十诫放在「感恩」部——'
             '位置不同，第三用的实质相同：律法对重生者不再是定罪的法庭，而是父家的家规。</text>')
    return _svg("0 0 720 176", "".join(b))


def fig_means():
    """蒙恩之道三管道。"""
    b = ['<text class="t" x="16" y="22">蒙恩之道　·　问154：圣道、圣礼、祷告，外在而普通的管道</text>']
    cols = [("圣道", "读·听·信·行", "问155–160", "bxn", 20),
            ("圣礼", "洗礼·圣餐", "问161–177", "bxg", 253),
            ("祷告", "主祷文为范本", "问178–196", "bxe", 486)]
    for n, d, q, cls, x in cols:
        b.append('<rect x="%d" y="70" width="214" height="74" rx="8" class="%s"/>' % (x, cls))
        b.append('<text class="k" x="%d" y="96" text-anchor="middle">%s</text>' % (x + 107, n))
        b.append('<text class="xs" x="%d" y="114" text-anchor="middle">%s</text>' % (x + 107, d))
        b.append('<text class="xs" x="%d" y="132" text-anchor="middle">%s</text>' % (x + 107, q))
        b.append('<path class="ar" d="M%d,58 L%d,68"/>' % (x + 107, x + 107))
    b.append('<rect x="220" y="34" width="280" height="26" rx="6" class="bxc"/>')
    b.append('<text class="k" x="360" y="52" text-anchor="middle">圣灵藉着这些，使救赎在选民身上生效</text>')
    b.append('<text class="sm" x="20" y="170">「外在」（external）指可见可用的手段，「普通」（ordinary）指神常规的行事方式。'
             '大要理不否认神能例外行事，只是否认人可以绕过管道而自订捷径。</text>')
    return _svg("0 0 720 184", "".join(b))


def fig_prayer():
    """主祷文六求结构。"""
    b = ['<text class="t" x="16" y="22">主祷文的骨架　·　问186–196：先三求为神，后三求为己</text>']
    b.append('<rect x="180" y="38" width="360" height="30" rx="6" class="bxc"/>')
    b.append('<text class="k" x="360" y="58" text-anchor="middle">序言：我们在天上的父（问189）——近与高同时成立</text>')
    left = [("愿人都尊你的名为圣", "问190", "神的荣耀"), ("愿你的国降临", "问191", "神的国度"),
            ("愿你的旨意行在地上", "问192", "神的旨意")]
    right = [("我们日用的饮食", "问193", "身体的需用"), ("免我们的债", "问194", "罪债的赦免"),
             ("不叫我们遇见试探", "问195", "试探中的保守")]
    for i, (t, q, k) in enumerate(left):
        y = 84 + i * 42
        b.append('<rect x="20" y="%d" width="320" height="34" rx="6" class="bxn"/>' % y)
        b.append('<text class="k" x="34" y="%d" font-size="12">%s</text>' % (y + 15, t))
        b.append('<text class="xs" x="34" y="%d">%s　·　%s</text>' % (y + 29, q, k))
    for i, (t, q, k) in enumerate(right):
        y = 84 + i * 42
        b.append('<rect x="380" y="%d" width="320" height="34" rx="6" class="bxg"/>' % y)
        b.append('<text class="k" x="394" y="%d" font-size="12">%s</text>' % (y + 15, t))
        b.append('<text class="xs" x="394" y="%d">%s　·　%s</text>' % (y + 29, q, k))
    b.append('<rect x="180" y="216" width="360" height="30" rx="6" class="bxe"/>')
    b.append('<text class="k" x="360" y="236" text-anchor="middle">结语：国度、权柄、荣耀全是你的（问196）</text>')
    b.append('<text class="sm" x="20" y="270">次序即神学：先求神的名、国、旨，再求己的粮、赦、保守。'
             '祷告的语法本身就在纠正以自我为圆心的敬虔。</text>')
    return _svg("0 0 720 284", "".join(b))


def fig_two_covenants():
    """两约对比。"""
    rows = [("对象", "无罪的亚当，作全人类的公共代表", "在基督里的选民"),
            ("条件", "完全、亲身、持续的顺服", "信心——本身也是神所赐"),
            ("应许", "生命", "生命、圣灵、永远的荣耀"),
            ("刑罚", "死", "基督已代受"),
            ("中保", "无", "有：神人二性的基督")]
    b = ['<text class="t" x="16" y="22">两约的分水岭　·　问20 与 问30–32</text>']
    b.append('<rect x="200" y="36" width="248" height="26" rx="5" class="bxc"/>')
    b.append('<text class="k" x="324" y="54" text-anchor="middle">行为之约</text>')
    b.append('<rect x="456" y="36" width="248" height="26" rx="5" class="bxe"/>')
    b.append('<text class="k" x="580" y="54" text-anchor="middle">恩典之约</text>')
    for i, (k, a, bcell) in enumerate(rows):
        y = 70 + i * 36
        b.append('<rect x="20" y="%d" width="172" height="30" rx="5" class="bxg"/>' % y)
        b.append('<text class="xs" x="106" y="%d" text-anchor="middle">%s</text>' % (y + 19, k))
        b.append('<rect x="200" y="%d" width="248" height="30" rx="5" class="bx"/>' % y)
        b.append('<text class="xs" x="324" y="%d" text-anchor="middle">%s</text>' % (y + 19, a))
        b.append('<rect x="456" y="%d" width="248" height="30" rx="5" class="bx"/>' % y)
        b.append('<text class="xs" x="580" y="%d" text-anchor="middle">%s</text>' % (y + 19, bcell))
    b.append('<text class="sm" x="20" y="272">两约的对比不是「律法对恩典」的对立，而是「在谁里面」的对立：'
             '第一个亚当代表我们失败，末后的亚当代表我们成全。归算的逻辑两边完全对称。</text>')
    return _svg("0 0 720 286", "".join(b))


def fig_wlc_hc():
    """两条并行柱，柱高严格按问数成比例。过薄的段（<20px）不塞字，改在图下以色块标注。"""
    b = ['<text class="t" x="16" y="22">两种编排，一套福音　·　大要理 196 问 vs 海德堡 129 问</text>',
         '<text class="xs" x="16" y="40">柱高按问数严格成比例；两柱绘图区等高，可直接目测各段占比</text>']
    left = [("问1–5", "目的与准则", "bxg", 5), ("问6–90", "人当信神什么", "bxn", 85),
            ("问91–152", "律法与本分", "bxc", 62), ("问153–196", "蒙恩之道与祷告", "bxe", 44)]
    right = [("问1–2", "安慰与三件要知道的事", "bxg", 2), ("问3–11", "人的困苦", "bxc", 9),
             ("问12–85", "人的拯救", "bxn", 74), ("问86–129", "感恩（十诫·主祷文）", "bxe", 44)]
    TOP, BOT, GAP = 78.0, 342.0, 3.0
    b.append('<text class="k" x="180" y="68" text-anchor="middle">威斯敏斯特大要理　1647　·　196 问</text>')
    b.append('<text class="k" x="540" y="68" text-anchor="middle">海德堡要理问答　1563　·　129 问</text>')
    thin = []

    def column(items, x0, total):
        H = BOT - TOP - GAP * (len(items) - 1)
        y = TOP
        for rng, name, cls, n in items:
            h = H * n / float(total)
            b.append('<rect x="%d" y="%.1f" width="320" height="%.1f" rx="5" class="%s"/>' % (x0, y, h, cls))
            cy = y + h / 2
            if h >= 38:
                b.append('<text class="k" x="%d" y="%.1f" text-anchor="middle" font-size="12">%s</text>'
                         % (x0 + 160, cy - 3, rng))
                b.append('<text class="xs" x="%d" y="%.1f" text-anchor="middle">%s　（%d 问）</text>'
                         % (x0 + 160, cy + 12, name, n))
            elif h >= 17:
                b.append('<text class="xs" x="%d" y="%.1f" text-anchor="middle">%s　%s（%d 问）</text>'
                         % (x0 + 160, cy + 4, rng, name, n))
            else:
                # 过薄：不塞字，改到图下以色块标注，同时画一条引线指向该段
                b.append('<line class="ln" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>'
                         % (x0 + 320, cy, x0 + 332, cy))
                thin.append((cls, rng, name, n))
            y += h + GAP

    column(left, 20, 196)
    column(right, 380, 129)
    b.append('<text class="xs" x="16" y="364">过薄而无法容字的段（按比例仅数像素高，已用短引线标出）：</text>')
    for i, (cls, rng, name, n) in enumerate(thin):
        x = 16 + i * 232
        b.append('<rect x="%d" y="374" width="14" height="12" rx="3" class="%s"/>' % (x, cls))
        b.append('<text class="xs" x="%d" y="384">%s　%s（%d 问）</text>' % (x + 20, rng, name, n))
    b.append('<text class="sm" x="16" y="410">两柱的「感恩／本分」一段几乎同长（44 问对 44 问）——'
             '这是两大谱系最深的共鸣：<tspan class="k">顺服的位置与动机完全一致</tspan>。'
             '差别在前段：海德堡把困苦压到 9 问、拯救放到 74 问，重心在「为我成就了什么」；'
             '大要理把神论与谕旨展开得更早也更长，重心在「祂是谁」。</text>')
    return _svg("0 0 720 428", "".join(b))


def fig_sins():
    """罪的轻重（问150–151）四个加重维度。"""
    dims = [("从犯罪的人", "身分、年龄、恩赐、职责、榜样的影响"),
            ("从所干犯的对象", "直接冒犯神？冒犯尊长？冒犯公众？"),
            ("从罪行本身", "违犯何诫、是否累犯、是否公开、是否引人同犯"),
            ("从时间地点", "主日、公共敬拜中、蒙警戒之后仍犯")]
    b = ['<text class="t" x="16" y="22">「罪有轻重」的四把尺　·　问150–151</text>']
    b.append('<text class="xs" x="16" y="40">一切罪本身都可憎、都当受刑罚；但在神眼前，它们的加重程度并不相同。</text>')
    for i, (k, d) in enumerate(dims):
        x = 20 + (i % 2) * 350
        y = 54 + (i // 2) * 74
        b.append('<rect x="%d" y="%d" width="330" height="62" rx="8" class="%s"/>' % (x, y, "bxn" if i % 2 == 0 else "bxg"))
        b.append('<text class="k" x="%d" y="%d">%s</text>' % (x + 16, y + 24, k))
        b.append('<text class="xs" x="%d" y="%d">%s</text>' % (x + 16, y + 44, d))
    b.append('<text class="sm" x="20" y="216">这一段常被误读为「有些罪无关紧要」。大要理的原意恰好相反：'
             '既然罪有加重，就更该逐一省察；它是牧养的分辨工具，不是自我宽免的滑梯。</text>')
    return _svg("0 0 720 230", "".join(b))


ALL = {
    "bible": fig_bible, "structure": fig_structure, "purpose": fig_purpose,
    "mediator": fig_mediator, "states": fig_states, "union": fig_union,
    "law3": fig_law3, "means": fig_means, "prayer": fig_prayer,
    "covenants": fig_two_covenants, "wlchc": fig_wlc_hc, "sins": fig_sins,
}


def figure(key, caption):
    _KEY["cur"] = key
    return '<figure id="fig-%s">%s<figcaption>%s</figcaption></figure>' % (key, ALL[key](), caption)


def fig_dynasty():
    """英格兰十朝条带图，宽度按在位年数成比例。"""
    reigns = [("亨八", 1509, 1547, "bxc"), ("爱六", 1547, 1553, "bxe"), ("玛丽", 1553, 1558, "bxc"),
              ("伊莉", 1558, 1603, "bxg"), ("詹一", 1603, 1625, "bxg"), ("查一", 1625, 1649, "bxn"),
              ("空位", 1649, 1660, "bx"), ("查二", 1660, 1685, "bxn"), ("詹二", 1685, 1688, "bxc"),
              ("威玛", 1689, 1702, "bxe")]
    T0, T1, X0, W = 1509, 1702, 20, 680
    b = ['<text class="t" x="16" y="18">英格兰十朝 · 1509–1702　（条宽＝在位年数，真实比例）</text>']
    # 图例移到图底，把顶部空间让给窄条的挑标

    def X(y):
        return X0 + W * (y - T0) / float(T1 - T0)
    narrow = 0
    for name, a, bb, cls in reigns:
        x, w = X(a), X(bb) - X(a)
        b.append('<rect x="%.1f" y="58" width="%.1f" height="40" rx="5" class="%s"/>' % (x, max(w - 2, 5), cls))
        if w > 34:
            b.append('<text class="k" x="%.1f" y="83" text-anchor="middle" font-size="12">%s</text>' % (x + w / 2, name))
        else:
            # 窄条：名称挑到条上方；相邻窄条必须上下错开两层，否则标签互压
            ly = 50 if narrow % 2 == 0 else 36
            narrow += 1
            b.append('<line class="ln" x1="%.1f" y1="58" x2="%.1f" y2="%d" stroke-dasharray="2 2"/>'
                     % (x + w / 2, x + w / 2, ly + 4))
            b.append('<text class="xs" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (x + w / 2, ly, name))
    for i, y in enumerate((1509, 1547, 1558, 1603, 1625, 1649, 1660, 1688, 1702)):
        yy = 112 if i % 2 == 0 else 126          # 交错两行，彻底避开相邻年份互相压字
        b.append('<line class="dash" x1="%.1f" y1="98" x2="%.1f" y2="%d"/>' % (X(y), X(y), yy - 10))
        b.append('<text class="xs" x="%.1f" y="%d" text-anchor="middle">%d</text>' % (X(y), yy, y))
    marks = [(1534, "断罗马"), (1552, "公祷书"), (1559, "折中"), (1611, "钦定本"),
             (1638, "国民圣约"), (1643, "威敏开议"), (1647, "大要理"), (1662, "大逐"), (1690, "苏格兰定案")]
    for i, (y, t) in enumerate(marks):
        yy = 152 + (i % 3) * 22
        b.append('<line class="ln" x1="%.1f" y1="58" x2="%.1f" y2="%d" stroke-dasharray="3 3"/>' % (X(y), X(y), yy - 10))
        b.append('<circle cx="%.1f" cy="%d" r="3" class="fg"/>' % (X(y), yy - 6))
        b.append('<text class="xs" x="%.1f" y="%d" text-anchor="middle">%d %s</text>' % (X(y), yy + 6, y, t))
    b.append('<text class="xs" x="16" y="222">红＝倾向罗马　绿＝推行改革宗　金＝折中　蓝＝高派主教制　灰＝无王</text>')
    b.append('<text class="sm" x="20" y="244">看清一件事：<tspan class="k">威斯敏斯特会议整个发生在查理一世这一条</tspan>——'
             '开议、信条、大要理全在 1643–1647 的六年内；四年后他被处决，十三年后准则在英格兰被废。</text>')
    return _svg("0 0 720 258", "".join(b))


def fig_threelines():
    """欧陆／英格兰／苏格兰三线并行。"""
    T0, T1, X0, W = 1517, 1700, 68, 630
    lanes = [("欧陆", 76, "bxg", "fg"), ("英格兰", 124, "bxn", "fn"), ("苏格兰", 172, "bxe", "fe")]
    pts = {
        "欧陆": [(1517, "路德"), (1536, "要义"), (1561, "比利时"), (1563, "海德堡"), (1610, "抗辩五条"), (1619, "多特")],
        "英格兰": [(1534, "断罗马"), (1552, "公祷书"), (1559, "折中"), (1611, "钦定本"), (1643, "开议"), (1647, "大要理"), (1662, "大逐")],
        "苏格兰": [(1560, "改教"), (1618, "珀斯"), (1638, "圣约"), (1648, "接纳"), (1690, "定案")],
    }
    b = ['<text class="t" x="16" y="22">三线并行 · 1517–1700</text>',
         '<text class="xs" x="16" y="38">同一段年代，三条线同时在走。竖虚线标出两个「双生年」。</text>']

    def X(y):
        return X0 + W * (y - T0) / float(T1 - T0)
    for i, y in enumerate((1559, 1563)):
        b.append('<line class="dash" x1="%.1f" y1="66" x2="%.1f" y2="200" stroke="var(--crimson)"/>' % (X(y), X(y)))
        # 两年仅差 4 年，标签必须一上一下错开
        b.append('<text class="xs" x="%.1f" y="%d" text-anchor="%s" fill="var(--crimson)">%d 双生年</text>'
                 % (X(y) + (-4 if i == 0 else 4), 214 if i == 0 else 227, "end" if i == 0 else "start", y))
    for name, yy, cls, fcls in lanes:
        b.append('<rect x="10" y="%d" width="52" height="24" rx="5" class="%s"/>' % (yy - 12, cls))
        b.append('<text class="xs" x="36" y="%d" text-anchor="middle">%s</text>' % (yy + 4, name))
        b.append('<line class="ln" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (X0, yy, X0 + W, yy))
        for i, (y, t) in enumerate(pts[name]):
            b.append('<circle cx="%.1f" cy="%d" r="4.5" class="%s"/>' % (X(y), yy, fcls))
            dy = -10 if i % 2 == 0 else 16
            b.append('<text class="xs" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (X(y), yy + dy, t))
    for y in range(1520, 1701, 20):
        b.append('<text class="xs" x="%.1f" y="252" text-anchor="middle">%d</text>' % (X(y), y))
    b.append('<line class="ln" x1="%d" y1="240" x2="%d" y2="240"/>' % (X0, X0 + W))
    return _svg("0 0 720 264", "".join(b))


def fig_creeds():
    """两层标准：三大信经 ＋ 三项合一信条。"""
    b = ['<text class="t" x="16" y="22">欧陆改革宗的两层标准</text>']
    b.append('<rect x="20" y="40" width="680" height="82" rx="8" class="bxn"/>')
    b.append('<text class="k" x="36" y="62">第一层　大公遗产：三大普世信经</text>')
    for i, (t, d) in enumerate([("使徒信经", "约8世纪定型 · 三段骨架"), ("尼西亚信经", "325/381 · 同质 homoousios"),
                                ("亚他那修信经", "约5–6世纪 · 三一＋道成肉身")]):
        x = 36 + i * 222
        b.append('<rect x="%d" y="72" width="208" height="40" rx="6" class="bx"/>' % x)
        b.append('<text class="k" x="%d" y="90" text-anchor="middle" font-size="12">%s</text>' % (x + 104, t))
        b.append('<text class="xs" x="%d" y="105" text-anchor="middle">%s</text>' % (x + 104, d))
    b.append('<rect x="20" y="136" width="680" height="82" rx="8" class="bxg"/>')
    b.append('<text class="k" x="36" y="158">第二层　改革宗判决：三项合一信条</text>')
    for i, (t, d) in enumerate([("比利时信条", "1561 · 37条 · 教义总纲"), ("海德堡要理", "1563 · 129问 · 牧养教导"),
                                ("多特信经", "1619 · 五项 · 恩典的性质")]):
        x = 36 + i * 222
        b.append('<rect x="%d" y="168" width="208" height="40" rx="6" class="bx"/>' % x)
        b.append('<text class="k" x="%d" y="186" text-anchor="middle" font-size="12">%s</text>' % (x + 104, t))
        b.append('<text class="xs" x="%d" y="201" text-anchor="middle">%s</text>' % (x + 104, d))
    b.append('<path class="ar" d="M360,124 L360,134"/>')
    b.append('<rect x="150" y="232" width="420" height="34" rx="7" class="bxc"/>')
    b.append('<text class="k" x="360" y="248" text-anchor="middle">威斯敏斯特大要理问答（1647）</text>')
    b.append('<text class="xs" x="360" y="262" text-anchor="middle">内容横跨两层，却只在第二层有明文归属——这一块需要主动补上</text>')
    b.append('<path class="dash" d="M360,220 L360,230"/>')
    b.append('<text class="sm" x="20" y="288">比利时信条第9条：「我们乐意接受三大信经，就是使徒信经、尼西亚信经与亚他那修信经。」'
             '——欧陆改革宗<tspan class="k">先是大公的，然后才是改革宗的</tspan>。</text>')
    return _svg("0 0 720 300", "".join(b))


ALL["dynasty"] = fig_dynasty
ALL["threelines"] = fig_threelines
ALL["creeds"] = fig_creeds
