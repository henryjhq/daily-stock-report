# daily-stock-report v2.0

一句话：给 AI 助手发一段话，每天自动出股票报告。含图表 + 知识卡片，PDF 输出。

支持三个 AI 编程助手：Claude Code · Codex · Codebuddy
覆盖四个市场：美股 · 港股 · A股 · 通用 / 加密货币

新功能：
- 8+1 板块完整日报
- 全中文界面（修复 wkhtmltopdf emoji 乱码）
- 每日金融 + 股市知识点，4 周轮换体系
- 纳斯达克深度分析 + 五大维度涨跌归因
- 自选股自动追踪

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

### 自选股

编辑 `watchlist.md`，加上你关注的股票：

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

## 报告内容（v2.0）

每份 PDF 报告含 9 个板块：

| # | 板块 | 类型 |
|---|---|---|
| 一 | 三大指数概览 | CSS 数据表 |
| 二 | 纳斯达克深度分析 | 走势/板块/明星股/情绪 |
| 三 | 涨跌幅最大个股 | 5 只 + 涨跌原因 |
| 四 | 五大维度涨跌归因 | 政策/资金/情绪/技术/基本面 |
| 五 | 板块轮动 | CSS 柱状图（5 涨 5 跌） |
| 六 | 宏观环境 | 国债/VIX/DXY/Fed/地缘 |
| 七 | 今日关注前瞻 | 财报/数据/技术位 |
| 八 | 今日知识点 | 金融概念 + 股市实操，4 周轮换 |
| 九 | 自选股追踪（可选） | watchlist.md 驱动 |

## 知识体系

每天自动出两条投资知识，4 周循环覆盖 8 个领域：

| 周次 | 金融知识 | 股市知识 |
|---|---|---|
| 第 1 周 | 宏观经济指标 | 大盘分析基础 |
| 第 2 周 | 货币政策工具 | 板块轮动 |
| 第 3 周 | 固定收益 | 个股分析 |
| 第 4 周 | 衍生品 | 资金面 |

## 技术说明

- wkhtmltopdf 使用 QtWebKit，不支持 emoji 和 Unicode 符号（会显示空白）
- 报告 HTML 已做全中文适配，字体栈为 Windows / macOS 中文系统字体
- 颜色规范：涨绿 #16a34a / 跌红 #dc2626

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
├── SKILL.md                       # Claude Code / Codex 入口
├── codebuddy/SKILL.md             # Codebuddy 入口
├── templates/                     # 4 个市场模板（含 chart 标签）
│   ├── us-stock.md                # 美股（9 板块结构）
│   ├── hk-stock.md                # 港股
│   ├── a-stock.md                 # A股
│   └── generic.md                 # 通用 / 加密货币
├── trackers/                      # 追踪文件
│   ├── us-stock-tracker.md
│   ├── hk-stock-tracker.md
│   ├── a-stock-tracker.md
│   ├── generic-tracker.md
│   └── knowledge-tracker.md       # 知识进度追踪
├── watchlist.md                   # 自选股列表
├── setup.sh                       # 一键安装 / 更新
├── VERSION
└── README.md
```

## License

MIT
