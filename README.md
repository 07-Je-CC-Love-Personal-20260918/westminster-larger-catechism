# 威斯敏斯特大要理问答全解

**当前版本 v1.0.0**（2026-09-18）　·　线上：https://westminster-larger-catechism.netlify.app

196 问全覆盖的静态单页站，及其 Python 生成器。欧陆改革宗视角（三项合一信条）＋ 三大普世信经坐标。
零外部请求、自适应、可离线保存、附 A4 打印样式。

## 快速上手
```bash
./build.sh          # 重建 site/index.html 并跑静态校验
python3 verify.py   # 只校验，不重建
```
构建无第三方依赖，Python 3 标准库即可。版本号见 `VERSION`，变更见 `CHANGELOG.md`。

## 发布流程
1. 改 `src/` 下对应模块
2. `./build.sh` —— 校验必须全绿
3. 更新 `VERSION` 与 `CHANGELOG.md`
4. `git commit` → `git tag -a vX.Y.Z -m "..."` → `git push && git push --tags`
5. 部署（见下「四、重新部署」）

---


## 一、交付物
- 线上地址：https://westminster-larger-catechism.netlify.app
- Netlify 项目名：`westminster-larger-catechism`
- site id：`bfe3f817-5144-49c3-8899-8abd8bf99662`
- Netlify 账号：Wei Nie / yb77448@um.edu.mo（slug `Abner199`，GitHub 登录 Abner199）
- team / account id：`689f69a8bdbf45296d9073cb`
- 管理后台：https://app.netlify.com/projects/westminster-larger-catechism
- 最近一次 deploy id：`6aab85a9721b0d4077eabfec`（state=ready，2026-09-17）

## 二、目录结构
```
wlc-site/
├── src/                 ← Python 生成器（真正的源码）
│   ├── build.py         装配入口：python3 build.py
│   ├── css.py           全站样式（house style + 水波 + 地图 + 动画）
│   ├── js.py            交互（主题/目录/检索/闪卡×2/君王/十诫/主日/时间轴拖动器/涟漪）
│   ├── charts.py        12 幅基础 SVG 图 + SPRITE（箭头 marker）
│   ├── maps.py          4 幅地图（真实经纬度投影）
│   ├── flows.py         流程图 / 思维导图 / 信仰之盾 / 两块石版
│   ├── macro.py         第一至三部：全景 · 情境 · 结构
│   ├── history.py       王朝口诀 · 十朝数据 · 三线年表 · 时间轴拖动器 · 18 张史卡
│   ├── creeds.py        第四部：三大普世信经
│   ├── lc1/lc2/lc3.py   第五部逐问解读，45 单元覆盖 196 问（含 DECA 十诫数据）
│   ├── topics.py        第六部跨部专题 + 附录（术语表/索引/延伸阅读）
│   ├── hc.py            第七部海德堡速背（52 主日 · 57 闪卡 · 21 天计划 · 129 问全表）
│   └── unit.py          问答单元的数据结构与渲染
└── site/
    ├── index.html       ← 构建产物，单文件约 498 KB，可直接双击打开
    └── netlify.toml     publish = "."
```

## 三、重新构建
```bash
cd src && python3 build.py      # 输出 ../site/index.html
```
无第三方依赖，Python 3 标准库即可。

## 四、重新部署（同一 site，URL 不变）
```bash
cd site
npx -y @netlify/mcp@latest --site-id bfe3f817-5144-49c3-8899-8abd8bf99662 --proxy-path "<deploy-site 工具返回的一次性 proxy 链接>"
```
或直接在 Netlify 后台把 `site/` 目录拖拽上传。

## 五、技术备忘（下次同类任务直接复用）
- 字体：**不引用 Google Fonts**，纯本地字体栈回退（用户在珠海，fonts.googleapis.com 不可达）；全站零外部请求。
- 目录滚动高亮用 **rAF + getBoundingClientRect**，不要用 IntersectionObserver。
- Playwright 测高亮必须 `scrollIntoView({behavior:'instant'})`，页面有 `scroll-behavior:smooth`，否则误报全失败。
- 闪卡「已背熟」集合必须 `Array.from(set)`，`[].slice.call(Set)` 返回空数组。
- SVG 箭头 marker 用**文档级单例 sprite**（`<svg width=0>` + defs），避免每图重复 id。
- 长页面性能：对 `details.unit` / `figure` / `.tablewrap` 加 `content-visibility:auto`，FCP 从约 500ms 降到 420ms。
- 沙箱出网代理封禁 `*.netlify.app`：**线上校验只能靠 `get-deploy-for-site`（state/published_at/screenshot_url）＋ 本地同一份文件实测**，curl / Playwright / WebFetch 直连均不可用。

## 六、内容备忘
- 问答文字为**要义译述**，非正式译本，引用须以所在教会标准译本为准。
- 问 109 已标明 1788 年美国长老会删去「容忍假宗教」；问 142 depopulations→depredation。
- 传统内合法分歧一律标出不作正统/异端之判：至上论/堕落后论、六日解释、安息日严格程度、确信是否属信心本质。
- 欧陆与威敏的实质差异只标三处：安息日、确信的地位、得儿子名分是否单列。
