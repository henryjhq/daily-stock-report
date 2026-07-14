---
name: daily-stock-report
display_name: 每日股评
display_name_en: Daily Stock Report
version: 1.0.0
description: 生成参数化的每日金融报告，支持美股/港股/A股/通用四种模板，含图表，输出 PDF。用户说「每日股评」「股票报告」「美股报告」「market report」时触发。
description_zh: 生成参数化的每日金融报告，支持美股/港股/A股/通用四种模板，含图表，输出 PDF。
description_en: Generate a parameterized daily financial report for US stocks, HK stocks, A-shares, or any market. Includes charts and PDF output.
allowed-tools: Bash,Read,Write,WebSearch,AskUserQuestion,Glob
---

# /daily-stock-report

生成参数化的每日金融市场报告。支持四种模板：美股、港股、A股、通用/加密货币。

## When to invoke

- 用户要求每日股票/市场报告
- 用户提到「美股」「港股」「A股」「股票」「市场报告」
- 用户调用 `/daily-stock-report`

## Workflow

### Phase 0 — 参数解析

如果用户提供了市场关键词，直接映射：

| 用户输入 | 市场 | 模板 |
|---|---|---|
| `美股` / `us` / `US` | 美股 | `templates/us-stock.md` |
| `港股` / `hk` / `HK` | 港股 | `templates/hk-stock.md` |
| `A股` / `a-stock` / `CN` | A股 | `templates/a-stock.md` |
| 其他 / 空 | 询问用户 | — |

无参数时用 AskUserQuestion：

> 你要哪个市场的每日报告？

选项：
- 美股 (US Stocks)
- 港股 (HK Stocks)
- A股 (A-Shares)
- 其他 / 加密货币

### Phase 1 — 数据采集

用 **WebSearch** 收集实时数据。每个市场跑 2-3 次并行搜索。

**美股：**
1. `S&P 500 NASDAQ Dow Jones today market summary`
2. `US stock market top movers gainers losers today`
3. `Federal Reserve interest rate outlook latest`

**港股：**
1. `Hang Seng Index today market summary`
2. `southbound northbound stock connect flow today`
3. `Hong Kong stock market top movers today`

**A股：**
1. `上证指数 深证成指 今日行情`
2. `A股板块轮动 领涨领跌板块 今日`
3. `北向资金 南向资金 今日流向`

**自选股（如有）：**
读取 `watchlist.md`，如果当前市场有自选股，逐个搜索：
`<TICKER> stock price today news`

收集到的数据整理成结构化上下文：

```
Market: <市场名称>
Date: <今天日期>
指数表现: <指数名>: <收盘价> (<涨跌幅%>)
领涨/领跌: <3-5 只股票及涨跌幅>
宏观要点: <利率/政策 1-2 句>
板块轮动: <领涨板块 / 领跌板块>
资金流向: <净流入/流出>
```

### Phase 2 — 生成 HTML 报告

读取对应模板 `templates/<market>.md`。模板的每个 section 带有 `chart:` 标签，
skill 按标签生成对应格式：

| chart 标签 | 输出 |
|---|---|
| `chart: table` | CSS 美化数据表格，涨跌红绿色标 |
| `chart: bar` | 纯 CSS 横向柱状图（领涨/领跌板块） |
| `chart: flow` | 资金流向对比柱状图 |
| `chart: none` | 纯文字分析段落 |

生成一个**自包含 HTML 文件**，内部包含：
- `<style>` 块：专业报告排版，表格红绿色标，柱状图 CSS
- 数据表格和图表直接嵌入 HTML
- 无需外部 CSS/JS/字体

CSS 柱状图模式（放在有 `chart: bar` 标签的 section）：
```html
<div class="bar-chart">
  <div class="bar-label">领涨 ▲</div>
  <div class="bar up" style="width:64%"><span>科技 +3.2%</span></div>
  <div class="bar up" style="width:56%"><span>通信 +2.8%</span></div>
  <div class="bar-label">领跌 ▼</div>
  <div class="bar down" style="width:24%"><span>公用 -1.2%</span></div>
  <div class="bar down" style="width:42%"><span>能源 -2.1%</span></div>
</div>
```

报告结构（4-6 个 section，按模板顺序）：
1. 指数快照（chart: table）
2. 领涨领跌（chart: bar）
3. 板块轮动（chart: bar）
4. 宏观脉搏（chart: none）
5. 自选股仪表盘（chart: table，仅 watchlist 有内容时）
6. 明日关注（chart: none）

### Phase 3 — 输出 & 记录

1. **保存 HTML** → `~/.claude/daily-stock-reports/<market>-report-<YYYY-MM-DD>.html`

2. **转 PDF**（自动）：
   - 检测 `wkhtmltopdf` 是否可用
   - 没装就自动装：`winget install wkhtmltopdf` / `brew install wkhtmltopdf` / `sudo apt install wkhtmltopdf`
   - 一条命令转换：`wkhtmltopdf report.html report.pdf`
   - 即使转换失败，HTML 已经完整可用，浏览器打开即报告

3. **对话中输出**：文字摘要 + PDF 路径

4. **更新 tracker**：追加每日一行摘要到 `trackers/<market>-tracker.md`

### 市场自动检测（无参数时）

- 4 位数字代码（9988, 0700）→ 港股
- 6 位数字代码（600519, 000858）→ A股
- 1-5 字母（AAPL, TSLA, BABA）→ 美股
- 其他 → 询问用户

## 模板

`templates/` 下的每个模板定义：
1. 报告标题格式
2. 有序 section 列表，每个带 `chart:` 标签
3. Tracker 条目格式

skill 在生成时读取模板，用户可自定义模板，无需改 SKILL.md。

## Tracker

`trackers/` 下的每日知识日志：
- 每日条目的 markdown 表格
- 渐进式 curriculum（第一周基础指数，第二周板块轮动，第三周资金流向，第四周期权/衍生品）
- 只追加不删除
