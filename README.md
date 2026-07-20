# daily-stock-report v3.0

一句话：给 AI 助手发一段话，每天自动出股票报告。**K 线图 + 主题定制 + AI 纹理 + 自动质检**，PDF 输出。

支持三个 AI 编程助手：Claude Code · Codex · Codebuddy
覆盖四个市场：美股 · 港股 · A股 · 通用 / 加密货币

---

## v3.0 新功能

| 功能 | 说明 |
|---|---|
| **K 线图** | OHLC 蜡烛图 + MA5 均线，matplotlib 渲染，自动识别涨跌 |
| **5 套主题** | default-light / warm-cream / cool-slate / ink-blue / dark，一键切换 |
| **AI 背景纹理** | Seedream / DALL-E / Stability 自动生成报告背景纹理，磨砂/纸张质感 |
| **图片 API 入口** | 首次使用主动询问配置，支持任意图片生成 API，改 3 个字段即可切换 |
| **Playwright 渲染** | 替代 wkhtmltopdf，完整支持现代 CSS、背景纹理、SVG |
| **8 种颜色高亮** | 红/绿/蓝/琥珀/紫 重点标识，五维归因徽章，顶部渐变摘要条 |
| **自动质检** | 每次生成报告后自动检测乱码、缺失章节、图表引用、CSS 完整性 |
| **GitHub Actions CI** | push/PR 自动运行配置校验 + 模板检查 + 渲染链路测试 |

---

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

---

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

```
/cron "0 18 * * 1-5" /daily-stock-report 美股   # 工作日 6 PM 自动出美股报告
```

---

## 报告内容（v3.0）

每份 PDF 报告含 10 个板块：

| # | 板块 | 类型 | 说明 |
|---|---|---|---|
| 一 | 三大指数概览 | CSS 数据表 + 卡片 | 红涨绿跌，带驱动分析 |
| 二 | 指数近一月走势 | K 线图 / 折线图 | OHLC 蜡烛 + MA5，matplotlib PNG |
| 三 | 纳斯达克深度分析 | 纯文字 | 走势/板块贡献/明星股/情绪 |
| 四 | 涨跌幅最大个股 | 数据表 | 5 只，涨跌原因 |
| 五 | 五大维度涨跌归因 | 判定表 + 徽章 | 政策/资金/情绪/技术/基本面 |
| 六 | 板块轮动 | CSS 柱状图 | 5 涨 5 跌，轮动逻辑 |
| 七 | 宏观环境 | 指标卡片 | 利率/CPI/VIX/非农 |
| 八 | 下周关注 | 纯文字 | 财报/技术位/政策/央行 |
| 九 | 今日知识点 | 知识卡片 | 金融 + 股市，4 周轮换 |
| 十 | 自选股追踪 | 数据表 | watchlist.md 驱动（可选） |

### 视觉亮点

- **顶部渐变摘要条** — 今日核心：芯片熊市 | VIX 18.77 | 资金轮动
- **8 种颜色标记** — 红(跌/利空)、绿(涨/利好)、蓝(日期/概率)、琥珀(油价/异常)、紫(洞察)
- **五维归因徽章** — 利空/净流出/偏恐慌 等带框标识
- **AI 背景纹理** — 磨砂纸张质感或几何纹路，极淡叠底，打印后不抢眼但比纯白有质感

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

## 技术说明

### 渲染管线

```
数据采集 (WebSearch)
  → HTML 生成 (CSS + SVG + matplotlib PNG)
  → 报告质检 (tests/check_report.py)
  → PDF 渲染 (Playwright Chromium)
  → 输出 + 追踪器更新
```

### 技术栈

| 组件 | 技术 |
|---|---|
| AI 引擎 | Claude Code / Codex / Codebuddy (Agent Skills 标准) |
| 图表生成 | matplotlib (K线/折线) + CSS (柱状图) |
| PDF 渲染 | Playwright + Chromium (默认) / wkhtmltopdf (降级) |
| 图片生成 | Seedream 5.0 Pro / DALL-E 3 / Stability AI (可选) |
| 字体 | Microsoft YaHei / SimHei / PingFang SC |
| 测试 | Python check scripts + GitHub Actions CI |

### 颜色规范

| 角色 | 色值 | 用途 |
|---|---|---|
| 涨绿 | `#16a34a` | 涨幅、利好、阳线 |
| 跌红 | `#dc2626` | 跌幅、利空、阴线 |
| 强调蓝 | `#1e40af` (默认) | 标题、分隔线、卡片边框 |
| 警告琥珀 | `#f59e0b` | 异常数据、油价、VIX 警戒 |
| 洞察紫 | `#7c3aed` | 图表解读、额外洞察 |

---

## 更新

```bash
cd ~/.claude/skills/daily-stock-report
./setup.sh --update
```

---

## 文件结构

```
daily-stock-report/
├── SKILL.md                       # Skill 主文件 (1070+ 行)
├── theme.json                     # 主题 + 图片 API 配置
├── VERSION                        # 3.0.0
├── README.md
├── INSTALL.md
├── setup.sh
├── watchlist.md                   # 自选股列表
├── codebuddy/SKILL.md             # Codebuddy 入口
├── templates/                     # 4 个市场模板
│   ├── us-stock.md                # 美股（10 板块）
│   ├── hk-stock.md                # 港股
│   ├── a-stock.md                 # A股
│   └── generic.md                 # 通用 / 加密货币
├── trackers/                      # 知识追踪（5 个文件）
├── tests/                         # 测试套件
│   ├── run_all.sh                 # 一键测试入口
│   ├── check_config.py            # 配置 & 模板校验
│   ├── check_render.py            # HTML→PDF 渲染链路
│   └── check_report.py            # 报告质量检查（乱码/格式/完整性）
├── assets/decorations/            # AI 生成的装饰素材
└── .github/workflows/
    └── test.yml                   # GitHub Actions CI
```

## License

MIT
