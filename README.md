# 📊 daily-stock-report

**一句话：给 AI 助手发一段话，每天自动出股票报告。含图表，PDF 输出。**

支持三个 AI 编程助手：Claude Code · Codex · Codebuddy
覆盖四个市场：🇺🇸 美股 · 🇭🇰 港股 · 🇨🇳 A股 · 🌍 通用 / 加密货币

---

## 安装

打开你的 AI 助手（Claude Code / Codex / Codebuddy），把下面这段话贴进去：

> 请帮我安装 daily-stock-report skill。
>
> 仓库地址：https://github.com/<your-username>/daily-stock-report.git
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

每次出报告时自动追踪这些股票的走势，追加到报告末尾。

### 每日定时

```
/cron "0 18 * * 1-5" /daily-stock-report 美股   # 工作日 6 PM 自动出美股报告
```

---

## 报告内容

每份 PDF 报告含：

- 📊 指数快照（含 CSS 数据表）
- 📈 板块热力图（CSS 柱状图，领涨绿 / 领跌红）
- 💰 资金流向图（南北向资金）
- 📋 自选股仪表盘（需配置 watchlist.md）
- 📡 宏观分析
- ⏳ 明日关注

## 更新

```bash
cd ~/.claude/skills/daily-stock-report
./setup.sh --update
```

---

## 文件结构

```
daily-stock-report/
├── SKILL.md                   ← Claude Code / Codex 入口
├── codebuddy/SKILL.md         ← Codebuddy 入口
├── templates/                 ← 4 个市场模板（含 chart 标签）
├── trackers/                  ← 4 个市场知识追踪
├── watchlist.md               ← 自选股列表
├── setup.sh                   ← 一键安装 / 更新
├── VERSION
└── README.md
```

## License

MIT
