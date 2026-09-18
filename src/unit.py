# -*- coding: utf-8 -*-
"""问答单元的数据结构与渲染。"""


def U(uid, rng, title, qas, core="", why="", cont="", view="", app="", keys=""):
    return {"type": "unit", "id": uid, "rng": rng, "title": title, "qas": qas,
            "core": core, "why": why, "cont": cont, "view": view, "app": app, "keys": keys}


def render_unit(u, open_default=False):
    h = ['<details class="unit" id="%s"%s>' % (u["id"], " open" if open_default else "")]
    h.append('<summary><span class="qr">%s</span><span class="ut">%s</span></summary>' % (u["rng"], u["title"]))
    h.append('<div class="body">')
    for n, q, a in u["qas"]:
        h.append('<div class="qa"><span class="qn">%s</span><span class="q">%s</span>'
                 '<span class="a">%s</span></div>' % (n, q, a))
    lens = []
    for key, cls, label in (("core", "core", "本质核心"), ("why", "why", "为什么写 · 真实论敌"),
                            ("cont", "cont", "欧陆对读"), ("view", "view", "不同视角 · 张力"),
                            ("app", "app", "应用")):
        if u.get(key):
            lens.append('<div class="l %s"><span class="t">%s</span><p>%s</p></div>' % (cls, label, u[key]))
    if lens:
        h.append('<div class="lens">' + "".join(lens) + '</div>')
    if u.get("keys"):
        h.append('<div class="keys"><span>关键经文</span>%s</div>' % u["keys"])
    h.append('</div></details>')
    return "".join(h)
