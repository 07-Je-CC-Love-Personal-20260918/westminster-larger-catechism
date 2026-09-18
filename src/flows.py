# -*- coding: utf-8 -*-
"""流程图 · 思维导图 · 动态图。"""

from charts import _svg


# ═════════════ 救恩次序流程图（动态流线）═════════════
def flow_ordo():
    b = ['<text class="t" x="16" y="24">救恩次序流程图 · 问57–90　（箭头为动态流线）</text>',
         '<text class="xs" x="16" y="42">左侧＝永恒中的谕旨；中间＝历史中的成就；右侧＝个人身上的施行。三段之间不可颠倒。</text>']
    # 三个泳道
    lanes = [("永恒　谕旨", 58, "bxg"), ("历史　成就", 128, "bxn"), ("个人　施行", 198, "bxe")]
    for t, y, cls in lanes:
        b.append('<rect x="14" y="%d" width="88" height="56" rx="7" class="%s"/>' % (y, cls))
        b.append('<text x="58" y="%d" class="xs" text-anchor="middle">%s</text>' % (y + 26, t.split("　")[0]))
        b.append('<text x="58" y="%d" class="xs" text-anchor="middle">%s</text>' % (y + 40, t.split("　")[1]))
        b.append('<line x1="108" y1="%d" x2="706" y2="%d" class="lane"/>' % (y + 28, y + 28))
    def node(x, y, w, t, sub, cls):
        o = ['<rect x="%d" y="%d" width="%d" height="42" rx="7" class="%s"/>' % (x, y, w, cls)]
        o.append('<text x="%d" y="%d" class="k" text-anchor="middle" font-size="12">%s</text>' % (x + w / 2, y + 18, t))
        o.append('<text x="%d" y="%d" class="xs" text-anchor="middle">%s</text>' % (x + w / 2, y + 33, sub))
        return "".join(o)
    # 永恒
    b.append(node(120, 65, 130, "拣选", "问13", "bxg"))
    b.append(node(276, 65, 150, "恩典之约", "问30–32", "bxg"))
    b.append(node(452, 65, 150, "指定中保", "问36", "bxg"))
    # 历史
    b.append(node(120, 135, 130, "道成肉身", "问37", "bxn"))
    b.append(node(276, 135, 150, "顺服与代赎", "问48–49", "bxn"))
    b.append(node(452, 135, 150, "复活升天代求", "问52–55", "bxn"))
    # 个人
    for i, (t, s) in enumerate([("有效恩召", "问67"), ("与基督联合", "问66"), ("称义", "问70"),
                                ("收纳", "问74"), ("成圣", "问75")]):
        b.append(node(120 + i * 118, 205, 108, t, s, "bxe"))
    # 竖向流线
    for x in (185, 351, 527):
        b.append('<path class="ar flow" d="M%d,109 L%d,131"/>' % (x, x))
    b.append('<path class="ar flow" d="M185,179 L185,201"/>')
    # 横向流线
    for x in (252, 428):
        b.append('<path class="ar flow" d="M%d,86 L%d,86"/>' % (x, x + 20))
        b.append('<path class="ar flow" d="M%d,156 L%d,156"/>' % (x, x + 20))
    for i in range(4):
        b.append('<path class="ar flow" d="M%d,226 L%d,226"/>' % (230 + i * 118, 234 + i * 118))
    # 终点
    b.append('<rect x="120" y="272" width="582" height="40" rx="7" class="bxc"/>')
    b.append('<text x="411" y="290" class="k" text-anchor="middle">坚忍（问79） → 死时成全为圣（问86） → 身体复活（问87） → 公开称义与荣耀（问90）</text>')
    b.append('<text x="411" y="305" class="xs" text-anchor="middle">这一整条线的起点与终点，都在问1：荣耀神，并完全以祂为乐，直到永远</text>')
    b.append('<path class="ar flow" d="M411,249 L411,269"/>')
    b.append('<text class="sm" x="16" y="336">读法提醒：<tspan class="k">三条泳道不可压缩成一条。</tspan>'
             '把「永恒」塌进「个人」，就成了宿命论；把「历史」塌进「个人」，就成了普救论；'
             '把「个人」塌进「历史」，就取消了有效恩召。大要理问 57 那一问，正是这三层之间的接榫。</text>')
    return _svg("0 0 720 350", "".join(b))


# ═════════════ 196 问思维导图 ═════════════
def mind_196():
    b = ['<text class="t" x="16" y="24">196 问思维导图 · 中心是问 5</text>']
    b.append('<rect x="272" y="196" width="176" height="52" rx="26" class="bxc"/>')
    b.append('<text x="360" y="218" class="k" text-anchor="middle">问 5 · 全篇目录</text>')
    b.append('<text x="360" y="234" class="xs" text-anchor="middle">信什么　／　行什么</text>')
    L = [("问1–5　根基", ["问1 目的：荣耀神并以祂为乐", "问3 准则：唯独圣经"], 56),
         ("问6–35　神与约", ["问6–11 神与三一", "问12–14 谕旨", "问15–20 创造·护理·行为之约", "问21–29 堕落与刑罚", "问30–35 恩典之约"], 96),
         ("问36–56　中保", ["问36–42 位格", "问43–45 三职", "问46–56 二态"], 216),
         ("问57–90　施行", ["问57–65 范围与教会", "问66–78 联合·称义·成圣", "问79–90 坚忍·死·末世"], 300)]
    R = [("问91–100　律法总论", ["问93–97 律法三用", "问99 解经八规则"], 56),
         ("问101–148　十诫", ["问101–121 前四诫（对神）", "问122–148 后六诫（对人）"], 120),
         ("问149–152　罪与刑罚", ["问149 无人能守全", "问150–151 罪有轻重"], 196),
         ("问153–177　蒙恩之道", ["问153–160 圣道", "问161–167 洗礼", "问168–177 圣餐"], 252),
         ("问178–196　祷告", ["问178–185 祷告总论", "问186–196 主祷文"], 340)]
    def branch(items, side):
        o = []
        for t, subs, y in items:
            if side < 0:
                x, w = 40, 190
                bx = x + w
                ctl = 252
            else:
                x, w = 490, 190
                bx = x
                ctl = 468
            o.append('<rect x="%d" y="%d" width="%d" height="30" rx="7" class="%s"/>'
                     % (x, y, w, "bxn" if side < 0 else "bxg"))
            o.append('<text x="%d" y="%d" class="k" text-anchor="middle" font-size="12">%s</text>'
                     % (x + w / 2, y + 20, t))
            o.append('<path class="mind" d="M%d,%d C%d,%d %d,%d %d,222"/>'
                     % (bx, y + 15, ctl, y + 15, ctl, 222, 360 + side * 90))
            for j, s in enumerate(subs):
                sy = y + 42 + j * 15
                sx = x + (12 if side < 0 else w - 12)
                o.append('<circle cx="%d" cy="%d" r="2.6" class="%s"/>' % (sx, sy - 4, "fn" if side < 0 else "fg"))
                o.append('<text x="%d" y="%d" class="xs" text-anchor="%s">%s</text>'
                         % (sx + (8 if side < 0 else -8), sy, "start" if side < 0 else "end", s))
        return "".join(o)
    b.append(branch(L, -1))
    b.append(branch(R, 1))
    b.append('<text x="164" y="44" class="k" text-anchor="middle">人当信关于神的什么　问6–90</text>')
    b.append('<text x="576" y="44" class="k" text-anchor="middle">神向人所要求的本分　问91–196</text>')
    return _svg("0 0 720 400", "".join(b))


# ═════════════ 海德堡思维导图 ═════════════
def mind_hc():
    b = ['<text class="t" x="16" y="24">海德堡 129 问思维导图 · 一根三叉的骨头</text>']
    b.append('<rect x="20" y="88" width="132" height="54" rx="10" class="bxc"/>')
    b.append('<text x="86" y="110" class="k" text-anchor="middle">问1–2</text>')
    b.append('<text x="86" y="128" class="xs" text-anchor="middle">安慰 ＋ 三件事</text>')
    arms = [("一、困苦", "问3–11（9问）", ["问3 从律法知罪", "问8 全然败坏，除非重生", "问11 神慈爱，也公义"], 30, "bxc"),
            ("二、拯救", "问12–85（74问）", ["问21 真信心「连我也」", "问31–32 三职，也在我身上",
                                          "问60–61 唯独因信称义", "问65–82 圣礼：洗礼与圣餐"], 122, "bxn"),
            ("三、感恩", "问86–129（44问）", ["问86 为何还要行善", "问92–115 十诫（在感恩之下）",
                                          "问116–129 祷告与主祷文", "问129 阿们：这是真的"], 246, "bxe")]
    for i, (t, rng, subs, y, cls) in enumerate(arms):
        b.append('<rect x="206" y="%d" width="150" height="40" rx="8" class="%s"/>' % (y, cls))
        b.append('<text x="281" y="%d" class="k" text-anchor="middle">%s</text>' % (y + 18, t))
        b.append('<text x="281" y="%d" class="xs" text-anchor="middle">%s</text>' % (y + 32, rng))
        b.append('<path class="mind" d="M152,115 C180,115 180,%d 204,%d"/>' % (y + 20, y + 20))
        for j, s in enumerate(subs):
            sy = y + 14 + j * 17
            b.append('<rect x="392" y="%d" width="306" height="15" rx="4" class="bx"/>' % (sy - 11))
            b.append('<text x="400" y="%d" class="xs">%s</text>' % (sy, s))
            b.append('<path class="mind" d="M358,%d C374,%d 376,%d 390,%d"/>' % (y + 20, y + 20, sy - 4, sy - 4))
    b.append('<text class="sm" x="16" y="336">把这张图记住，海德堡就再也丢不了：'
             '<tspan class="k">一个入口（安慰），三根枝（困苦·拯救·感恩），九到十个挂点。</tspan>'
             '其余 120 问都是这些挂点的展开。</text>')
    return _svg("0 0 720 350", "".join(b))


# ═════════════ 读法决策树 ═════════════
def flow_which():
    b = ['<text class="t" x="16" y="24">该用哪一份？· 决策树</text>']
    b.append('<rect x="252" y="42" width="216" height="38" rx="19" class="bxc"/>')
    b.append('<text x="360" y="66" class="k" text-anchor="middle">你现在要做什么？</text>')
    opts = [("我要背诵", "小要理 107 问\n或海德堡 129 问", 20, "bxe"),
            ("我要查教义界线", "威斯敏斯特信条\n33 章 172 节", 196, "bxn"),
            ("我要讲道 / 逐条省察", "大要理 196 问\n（本站）", 372, "bxg"),
            ("我要大公根基", "三大普世信经\n＋比利时信条", 548, "bxc")]
    for t, r, x, cls in opts:
        b.append('<path class="ar" d="M360,82 C360,104 %d,104 %d,120"/>' % (x + 76, x + 76))
        b.append('<rect x="%d" y="122" width="152" height="34" rx="7" class="bx"/>' % x)
        b.append('<text x="%d" y="144" class="k" text-anchor="middle" font-size="12">%s</text>' % (x + 76, t))
        b.append('<rect x="%d" y="170" width="152" height="50" rx="7" class="%s"/>' % (x, cls))
        for j, line in enumerate(r.split("\n")):
            b.append('<text x="%d" y="%d" class="xs" text-anchor="middle">%s</text>' % (x + 76, 190 + j * 15, line))
        b.append('<path class="ar" d="M%d,158 L%d,168"/>' % (x + 76, x + 76))
    b.append('<text class="sm" x="16" y="248">三份文件内容不冲突，用途完全不同。'
             '<tspan class="k">拿大要理去教七岁孩子，是工具用错了，不是文件写差了。</tspan></text>')
    return _svg("0 0 720 262", "".join(b))


# ═════════════ 信仰之盾（动态描线）═════════════
def fig_shield():
    b = ['<text class="t" x="16" y="24">信仰之盾 <tspan class="lt">Scutum Fidei</tspan> · 亚他那修信经的图形版</text>',
         '<text class="xs" x="16" y="42">三条外边读「不是」（non est），三条内辐读「是」（est）。六句话，正统三一论的全部边界。</text>']
    cx, cy, R = 250, 176, 104
    pts = {"父": (cx, cy - R), "子": (cx - R * 0.87, cy + R * 0.5), "灵": (cx + R * 0.87, cy + R * 0.5)}
    # 外三角：不是
    tri = " ".join("%.0f,%.0f" % pts[k] for k in ("父", "子", "灵"))
    b.append('<polygon points="%s" class="shield draw"/>' % tri)
    for a, bq, lab, dx, dy, rot in (("父", "子", "不是", -66, -30, -60), ("子", "灵", "不是", 0, 34, 0), ("父", "灵", "不是", 66, -30, 60)):
        x1, y1 = pts[a]; x2, y2 = pts[bq]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        b.append('<rect x="%.0f" y="%.0f" width="40" height="20" rx="5" class="bx"/>' % (mx - 20, my - 10))
        b.append('<text x="%.0f" y="%.0f" class="xs" text-anchor="middle">不是</text>' % (mx, my + 4))
    b.append('<circle cx="%d" cy="%d" r="34" class="bxc"/>' % (cx, cy))
    b.append('<text x="%d" y="%d" class="k" text-anchor="middle">神</text>' % (cx, cy + 5))
    for k, (x, y) in pts.items():
        b.append('<line x1="%d" y1="%d" x2="%.0f" y2="%.0f" class="shield draw"/>' % (cx, cy, x, y))
        mx, my = (cx + x) / 2, (cy + y) / 2
        b.append('<rect x="%.0f" y="%.0f" width="28" height="18" rx="5" class="bxg"/>' % (mx - 14, my - 9))
        b.append('<text x="%.0f" y="%.0f" class="xs" text-anchor="middle">是</text>' % (mx, my + 4))
        b.append('<circle cx="%.0f" cy="%.0f" r="28" class="bxn"/>' % (x, y))
        b.append('<text x="%.0f" y="%.0f" class="k" text-anchor="middle">%s</text>' % (x, y + 5, k))
    # 右侧释义
    lines = [("父不是子，子不是灵，灵不是父", "位格的真实分别——反撒伯流（形态论）"),
             ("父是神，子是神，灵是神", "本质的完全同一——反亚流（次位论）"),
             ("然而不是三位神，乃是一位神", "亚他那修信经第 15–16 条"),
             ("大要理问 9", "「三位是同一位神，同一本质，同等权能与荣耀，虽在位格特性上有别」"),
             ("大要理问 10", "父生子；子被父所生；圣灵从父与子而出——自亘古永远如此"),
             ("比利时信条第 10 条", "子按其神性是「自有的神」（autotheos）——加尔文守住的那条线")]
    for i, (t, d) in enumerate(lines):
        y = 74 + i * 46
        b.append('<rect x="392" y="%d" width="310" height="38" rx="7" class="%s"/>' % (y, "bxg" if i < 3 else "bx"))
        b.append('<text x="404" y="%d" class="k" font-size="12">%s</text>' % (y + 16, t))
        b.append('<text x="404" y="%d" class="xs">%s</text>' % (y + 31, d))
    return _svg("0 0 720 358", "".join(b))


# ═════════════ 十诫两块石版 ═════════════
def fig_tablets():
    b = ['<text class="t" x="16" y="24">两块石版 · 问98：前四诫对神，后六诫对人</text>']
    left = [("一", "除了我以外，不可有别的神", "问103–106", "敬拜的对象"),
            ("二", "不可为自己雕刻偶像", "问107–110", "敬拜的方式"),
            ("三", "不可妄称神的名", "问111–114", "神名的使用"),
            ("四", "当记念安息日", "问115–121", "时间的归属")]
    right = [("五", "当孝敬父母", "问122–133", "权柄关系"), ("六", "不可杀人", "问134–136", "生命"),
             ("七", "不可奸淫", "问137–139", "贞洁"), ("八", "不可偷盗", "问140–142", "财产"),
             ("九", "不可作假见证", "问143–145", "真理与名誉"), ("十", "不可贪恋", "问146–148", "心的方向")]
    def tablet(x, w, title, sub, rows, cls):
        o = ['<path d="M%d,64 Q%d,28 %d,64 L%d,318 Q%d,332 %d,318 Z" class="%s"/>'
             % (x, x + w / 2, x + w, x + w, x + w / 2, x, cls)]
        o.append('<text x="%d" y="86" class="k" text-anchor="middle">%s</text>' % (x + w / 2, title))
        o.append('<text x="%d" y="102" class="xs" text-anchor="middle">%s</text>' % (x + w / 2, sub))
        for i, (n, t, q, k) in enumerate(rows):
            y = 122 + i * (188.0 / max(len(rows), 1))
            o.append('<text x="%d" y="%.0f" class="k" font-size="13">%s</text>' % (x + 16, y, n))
            o.append('<text x="%d" y="%.0f" class="xs">%s</text>' % (x + 36, y, t))
            o.append('<text x="%d" y="%.0f" class="xs" text-anchor="end">%s · %s</text>' % (x + w - 14, y, k, q))
        return "".join(o)
    b.append(tablet(20, 330, "第一块　对神的本分", "爱主你的神（问102）", left, "bxn"))
    b.append(tablet(370, 330, "第二块　对人的本分", "爱人如己（问122）", right, "bxg"))
    b.append('<text class="sm" x="20" y="344">分法之争：改革宗与东正教以「不可有别的神」为第一诫、「不可雕刻偶像」为第二诫；'
             '<tspan class="k">罗马天主教与路德宗把两者合并，再把第十诫拆成两条</tspan>——后果是「不可雕刻偶像」在其要理问答中常被省略。</text>')
    return _svg("0 0 720 356", "".join(b))


FLOWS = {"ordo": flow_ordo, "mind196": mind_196, "mindhc": mind_hc,
         "which": flow_which, "shield": fig_shield, "tablets": fig_tablets}
