# 威斯敏斯特大要理问答全解

**当前版本 v1.1.1**（2026-09-18）

线上（双镜像，内容一致）
- Netlify：https://westminster-larger-catechism.netlify.app
- GitHub Pages：https://07-je-cc-love-personal-20260918.github.io/westminster-larger-catechism/

196 问全覆盖的静态单页站，及其 Python 生成器。欧陆改革宗视角（三项合一信条）＋ 三大普世信经坐标。
零外部请求、自适应、可离线保存、附 A4 打印样式。

## 快速上手
```bash
./build.sh           # 重建 + 静态校验 + SVG 版面校验
python3 verify.py    # 只跑静态校验（ID/锚点/196问/标签/SVG良构/零外链）
python3 svgcheck.py  # 只跑 SVG 版面校验（出框 / 文字重叠 / 被遮 / 撑出色块）
```

> **为什么单独有 svgcheck**：`figure{overflow:hidden}` 会把出框的 SVG 文字裁掉，
> 普通 DOM 溢出检测量不到，页面看着「零溢出」实则文字被切、被压。
> 必须逐个 `<text>` 实测。v1.1.0 靠它一次查出 19 幅图的问题。
>
> v1.1.1 又补了两条规则：**文字被后绘制的图形遮盖**（SVG 按文档顺序绘制，
> 后出现的方框会压住先画的文字，DOM 层面同样测不到），以及**文字撑出所在色块**。
> 画新图时凡是「方框 + 标签」的结构，务必先排布再绘制，不要写死坐标。
构建无第三方依赖，Python 3 标准库即可。版本号见 `VERSION`，变更见 `CHANGELOG.md`。

## 持续部署

推到 `main` 即自动上线，无需任何手动操作：

```
push main ──► GitHub Actions
                ├─ setup-python 3.11
                ├─ cd src && python3 build.py      构建，约 0.1 秒
                ├─ python3 verify.py               10 项静态校验，不过则中止
                ├─ netlify deploy --prod           站点 id 取自 .netlify/state.json
                ├─ upload-pages-artifact ─► deploy-pages    第二镜像
                └─ 回写 site/index.html 到仓库      保证仓库内 == 线上
push tag v* ──► 以上全部 + 自动建 GitHub Release 并附上 index.html
pull request ──► 只构建校验，不部署
```

**凭据**：仅需组织级 Secret `NETLIFY_AUTH_TOKEN`，配置一次，组织内所有仓库继承。
站点 id 不是密钥，直接提交在 `.netlify/state.json`，因此新项目零配置。

**两个坑**：
1. 提交信息中不要出现跳过 CI 的方括号标记（GitHub 会据此跳过整次运行）。
   自动回写的那条提交会带该标记，用于防止递归触发。
2. tag 必须打在**已包含本工作流文件的提交**上。GitHub 在 tag 推送时读取的是
   该 tag 所指提交上的工作流；指向旧提交的 tag 不会触发任何运行。
3. `github-pages` 环境默认只允许受保护分支部署，**tag 推送会被环境保护规则拒绝**。
   因此 Pages 相关步骤只在 `main` 上执行；tag 路径只做 Netlify 部署与 Release 归档。

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
