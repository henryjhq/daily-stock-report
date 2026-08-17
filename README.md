# daily-stock-report v1.5

一句话：给 AI 助手发一段话，每天自动出股票报告。**K 线图 + 主题定制 + AI 纹理 + 自动质检**，PDF 输出。

支持三个 AI 编程助手：Claude Code · Codex · Codebuddy
覆盖四个市场：美股 · 港股 · A股 · 通用 / 加密货币

> 版本线：v1.1 → v1.2 → v1.3 → v1.4 → **v1.5**（当前）。

## 功能特性

| 特性 | 说明 |
|---|---|
| **主题定制系统** | `theme.json` 一键切换 5 套主题（default-light / warm-cream / cool-slate / ink-blue / dark），可自定义颜色、字体大小、斑马纹、卡片阴影 |
| **红涨绿跌规范** | gain/loss 颜色全局强制映射，可适配 A股「红涨绿跌」与美股「绿涨红跌」两种习惯 |
| **K线图渲染** | 新增 `chart: kline`，OHLC 蜡烛图 + 5 日均线，覆盖四大市场 |
| **Playwright 渲染器** | 弃用 wkhtmltopdf（QtWebKit 老引擎），改用 Chromium，完整支持现代 CSS / SVG / 背景纹理 |
| **AI 装饰元素** | 接入 Seedream / DALL-E / Stability 图片 API，自动生成报告背景纹理 |
| **每日定时任务** | `theme.json` 的 `schedule` 配置，按市场 / 时间 / 工作日自动生成 |
| **自动化测试** | `tests/` 提供配置检查、渲染检查、报告结构检查脚本 |
| **排版一致性** | 模板固化标准版式（指标卡 + 卡片概览 + K线图），确保每日报告排版统一 |

## 安装

打开你的 AI 助手（Claude Code / Codex / Codebuddy），把下面这段话贴进去：

> 请帮我安装 daily-stock-report skill。
>
> 仓库地址：https://github.com/henryjhq/daily-stock-report.git
>
> 1. 判断你自己是什么 agent：
>    - Claude Code → 克隆到 ~/.claude/skills/daily-stock-report/
>    - Codex → 克隆到 ~/.codex/skills/daily-stock-report/
>    - Codebuddy → 克隆到 ~/.codebuddy/skills-marketplace/skills/daily-stock-report/
> 2. git clone 到对应目录，cd 进去
> 3. 运行 chmod +x setup.sh && ./setup.sh
> 4. 装好之后告诉我

详细安装说明见 [INSTALL.md](INSTALL.md)。

## 使用

| 命令 | 效果 |
|---|---|
| `/daily-stock-report` | 弹菜单选市场 → 生成 PDF 报告 |
| `/daily-stock-report 美股` | 直接出美股报告（S&P 500 / NASDAQ / Dow） |
| `/daily-stock-report 港股` | 直接出港股报告（HSI / 南北向资金） |
| `/daily-stock-report A股` | 直接出 A 股报告（上证 / 深证 / 北向资金） |
| `/daily-stock-report 比特币` | 不匹配前三类，走通用模板 |

### 主题切换

```bash
# 编辑 theme.json 的 name 字段即可换主题
vim theme.json   # 支持: default-light | warm-cream | cool-slate | ink-blue | dark
```

### 图片 API 配置

首次生成报告时会自动询问是否接入图片生成 API。也可以手动编辑 `theme.json` 的 `imageApi` 块：

```json
"imageApi": {
    "provider": "seedream",              // 或 openai / stability / custom
    "endpoint": "https://...api/v3/images/generations",
    "model": "doubao-seedream-5-0-pro-260628",
    "apiKey": "YOUR_API_KEY_HERE"
}
```

支持 Seedream (火山引擎) / DALL-E (OpenAI) / Stability AI / 自定义 API。

### 自选股

编辑 `watchlist.md`：

```markdown
## 美股
- AAPL (苹果)
- NVDA (英伟达)

## 港股
- 9988 (阿里巴巴)
```

### 每日定时

```bash
/cron "0 18 * * 1-5" /daily-stock-report 美股   # 工作日 6 PM 自动出美股报告
```

也可编辑 `theme.json` 的 `schedule` 字段（`enabled` / `market` / `time` / `days`）开启内置定时任务。

## 报告内容

每份 PDF 报告含 10 个板块：

| # | 板块 | 类型 |
|---|---|---|
| 一 | 三大指数概览 | 指标卡 + 卡片概览 + 明细表 |
| 二 | 指数近一月K线图 | SVG 蜡烛图（OHLC + 5 日均线） |
| 三 | 纳斯达克深度分析 | 走势/板块/明星股/情绪 |
| 四 | 涨跌幅最大个股 | 5 只 + 涨跌原因 |
| 五 | 五大维度涨跌归因 | 政策/资金/情绪/技术/基本面 |
| 六 | 板块轮动 | CSS 柱状图（5 涨 5 跌） |
| 七 | 宏观环境 | 国债/VIX/DXY/Fed/地缘 |
| 八 | 今日关注前瞻 | 财报/数据/技术位 |
| 九 | 今日知识点 | 金融概念 + 股市实操，4 周轮换 |
| 十 | 自选股追踪（可选） | watchlist.md 驱动 |

### 视觉亮点

- **AI 背景纹理** — 磨砂纸张质感或几何纹路，极淡叠底，打印后不抢眼但比纯白有质感
- **K 线图竖向堆叠** — 每张图独占一行，蜡烛清晰可辨
- **指标卡片** — 关键宏观数据（收益率/VIX/DXY/油价）以卡片展示
- **引语金句** — 每日核心洞察以居中醒目文字呈现

---

## 测试 & 质量保障

### 自动质检（每次生成报告后）

每次报告生成后自动运行 `tests/check_report.py`，检查：

| 检查项 | 说明 |
|---|---|
| 乱码检测 | 扫描 6 个 wkhtmltopdf 不支持的 Unicode 范围（emoji/symbols/arrows） |
| HTML 结构 | DOCTYPE、charset、head/body 标签完整性 |
| 章节完整性 | 7 个必需章节是否全部存在 |
| 图表引用 | 所有 `<img src>` 指向的文件是否真实存在 |
| 表格质量 | open/close 标签匹配、涨跌颜色标注计数 |
| 关键数据 | 数字数量、日期、指数名称 |
| CSS 质量 | 颜色规范（涨绿/跌红/强调蓝）、中文字体栈 |

### CI 自动测试（GitHub Actions）

每次 push/PR 到 master 自动运行：

```bash
python tests/check_config.py    # theme.json + 模板 + SKILL.md 结构
python tests/check_render.py    # Playwright HTML→PDF 渲染链路
bash tests/run_all.sh           # 文件完整性 + Git 状态
```

👉 [Actions 面板](https://github.com/henryjhq/daily-stock-report/actions)

### 本地测试

```bash
bash tests/run_all.sh                 # 完整测试（5 步，含渲染）
bash tests/run_all.sh --skip-render   # 快速测试（跳过渲染，2 秒）
python tests/check_report.py <报告.html>   # 单独检查某份报告
```

---

## 主题定制

编辑 `theme.json` 即可自定义报告外观：

- **预设主题**：`default-light` / `warm-cream` / `cool-slate` / `ink-blue` / `dark`
- **涨跌颜色**：`gain`（涨）/ `loss`（跌），默认「红涨绿跌」（涨 `#dc2626` / 跌 `#16a34a`）
- **AI 装饰**：`aiDecorations: true` + 配置 `imageApi`，自动生成背景纹理

> 注意：`imageApi.apiKey` 若填入真实密钥，请勿提交到仓库。

## 技术说明

- PDF 由 Playwright + Chromium 渲染，支持现代 CSS、SVG 图表与背景纹理
- 报告 HTML 全中文适配，字体栈为 Windows / macOS 中文系统字体
- 颜色规范：涨红 `#dc2626` / 跌绿 `#16a34a`（可经 `theme.json` 反转）

## 更新

```bash
cd ~/.claude/skills/daily-stock-report
./setup.sh --update
```

## 文件结构

```
daily-stock-report/
├── SKILL.md                       # Claude Code / Codex 入口
├── codebuddy/SKILL.md             # Codebuddy 入口
├── templates/                     # 4 个市场模板（含 chart 标签）
│   ├── us-stock.md                # 美股（10 板块结构 + 排版规范）
│   ├── hk-stock.md                # 港股
│   ├── a-stock.md                 # A股
│   └── generic.md                 # 通用 / 加密货币
├── trackers/                      # 追踪文件（追加式知识日志）
│   ├── us-stock-tracker.md
│   ├── hk-stock-tracker.md
│   ├── a-stock-tracker.md
│   ├── generic-tracker.md
│   └── knowledge-tracker.md       # 知识进度追踪
├── theme.json                     # 主题 + 定时任务 + 图片 API 配置
├── SCHEDULE.md                    # 定时任务说明
├── watchlist.md                   # 自选股列表
├── assets/                        # 装饰资源（背景纹理）
├── tests/                         # 自动化测试脚本
├── setup.sh                       # 一键安装 / 更新
├── CHANGELOG.md                   # 更新日志
├── VERSION
└── README.md
```

## License

MIT
