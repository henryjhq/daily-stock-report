---
name: daily-stock-report
description: Generate a parameterized daily financial report for US stocks, HK stocks, A-shares, or any market. Outputs a styled PDF with charts.
triggers:
  - daily stock report
  - daily-stock-report
  - stock report
  - market report
  - 每日股评
  - 股票报告
  - 市场报告
  - 美股报告
  - 港股报告
  - A股报告
allowed-tools:
  - Bash
  - Read
  - Write
  - WebSearch
  - AskUserQuestion
  - Glob
---

# /daily-stock-report

Generate a parameterized daily financial market report. Output is **PDF with embedded charts**.
Supports US stocks, HK stocks, A-shares, and a generic/crypto fallback.

## When to invoke

- User asks for a daily stock/market report
- User mentions "美股", "港股", "A股", "股票", "市场报告"
- User invokes `/daily-stock-report` directly

## Workflow

### Phase 0 — Parameter Resolution

Parse user input:

| User input | Market | Template |
|---|---|---|
| `美股` / `us` / `US` | US stocks | `templates/us-stock.md` |
| `港股` / `hk` / `HK` | HK stocks | `templates/hk-stock.md` |
| `A股` / `a-stock` / `CN` | A-shares | `templates/a-stock.md` |
| Anything else / empty | Ask user | — |

If no parameter, use AskUserQuestion:

> Which market do you want a daily report for?

Options:
- US Stocks (美股) — S&P 500, NASDAQ, Dow Jones
- HK Stocks (港股) — Hang Seng Index, Southbound flow
- A-Shares (A股) — Shanghai Composite, Shenzhen Component
- Other / Crypto — Generic market template

### Phase 1 — Data Collection

Use **WebSearch** to gather real-time data. Run 2-3 parallel searches:

**US Stocks:**
1. `S&P 500 NASDAQ Dow Jones today market summary`
2. `US stock market top movers gainers losers today`
3. `Federal Reserve interest rate outlook latest`

**HK Stocks:**
1. `Hang Seng Index today market summary`
2. `Southbound northbound stock connect flow today`
3. `Hong Kong stock market top movers today`

**A-Shares:**
1. `上证指数 深证成指 今日行情 summary`
2. `A股板块轮动 领涨领跌板块 今日`
3. `北向资金 今日流向`

**Generic / Crypto:**
1. Detect tickers; search each: `<TICKER> price today market cap`
2. `global market macro overview today`

**Watchlist (if watchlist.md exists and has entries for this market):**
Read `watchlist.md`, find entries under the matching market heading.
For each non-commented ticker, search: `<TICKER> stock price today news`

Compile into structured context:

```
Market: <name>
Date: <today>
Indices: <name>: <close> (<change%>)
Top movers: <3-5 names with % change>
Macro: <1-2 sentences on rates/policy>
Sectors: <leading/lagging>
Flows: <net inflow/outflow>
Watchlist: <ticker: price, change%, headline> (if any)
```

### Phase 2 — HTML Report Generation

Read the template file from `templates/`. Each section has a `chart:` tag
that determines the output format:

| Tag | Output |
|---|---|
| `chart: table` | CSS-styled data table, red/green color coding |
| `chart: bar` | Pure CSS horizontal bar chart (sector performance) |
| `chart: flow` | Flow comparison bar chart (northbound/southbound) |
| `chart: none` | Prose analysis paragraph only |

Generate a **self-contained HTML file**. Requirements:
- All CSS in a single `<style>` block — no external files
- No JavaScript, no external fonts
- Red/green color coding: gains in `#22c55e` (green), losses in `#ef4444` (red)
- Professional report typography: system font stack, clear hierarchy
- Page-break hints so each section starts on a new PDF page

**CSS bar chart template** (use when template says `chart: bar`):

```html
<div class="bar-section">
  <h3>领涨板块 ▲</h3>
  <div class="bar-chart">
    <div class="bar-row"><span class="bar-label">科技</span><div class="bar-track"><div class="bar-fill up" style="width:64%">+3.2%</div></div></div>
    <div class="bar-row"><span class="bar-label">通信</span><div class="bar-track"><div class="bar-fill up" style="width:56%">+2.8%</div></div></div>
    <div class="bar-row"><span class="bar-label">消费</span><div class="bar-track"><div class="bar-fill up" style="width:38%">+1.9%</div></div></div>
  </div>
  <h3>领跌板块 ▼</h3>
  <div class="bar-chart">
    <div class="bar-row"><span class="bar-label">公用</span><div class="bar-track"><div class="bar-fill down" style="width:24%">-1.2%</div></div></div>
    <div class="bar-row"><span class="bar-label">能源</span><div class="bar-track"><div class="bar-fill down" style="width:42%">-2.1%</div></div></div>
  </div>
</div>
```

**CSS for bar charts** (include in `<style>` block):

```css
.bar-section { margin: 24px 0; }
.bar-chart { margin: 8px 0 16px 0; }
.bar-row { display: flex; align-items: center; margin: 4px 0; }
.bar-label { width: 80px; font-weight: 600; text-align: right; padding-right: 12px; }
.bar-track { flex: 1; background: #f3f4f6; border-radius: 4px; height: 24px; }
.bar-fill { height: 24px; border-radius: 4px; color: white; font-size: 12px; line-height: 24px; padding: 0 8px; font-weight: 600; white-space: nowrap; }
.bar-fill.up { background: #22c55e; }
.bar-fill.down { background: #ef4444; }
```

**CSS for tables** (include in `<style>` block):

```css
.data-table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }
.data-table th { background: #f8fafc; text-align: left; padding: 10px 12px; border-bottom: 2px solid #e2e8f0; font-weight: 700; }
.data-table td { padding: 8px 12px; border-bottom: 1px solid #f1f5f9; }
.data-table .up { color: #22c55e; font-weight: 600; }
.data-table .down { color: #ef4444; font-weight: 600; }
```

**Report HTML structure:**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>Daily Stock Report — {{MARKET}} — {{DATE}}</title>
<style>
  /* all styles here */
</style>
</head>
<body>
  <h1>{{REPORT TITLE}}</h1>
  <p class="meta">Generated: {{DATE}} | Data: WebSearch real-time</p>
  <!-- Sections in template order -->
</body>
</html>
```

Fill each section with Phase 1 data. The report should be:
- **Data-driven**: cite numbers, not vague adjectives
- **Concise**: 4-6 sections, each 3-5 sentences of analysis + a chart
- **Actionable**: end with a "What to watch tomorrow" section

### Phase 3 — PDF Output & Record

**Step 1: Ensure wkhtmltopdf is available.**

Check with `which wkhtmltopdf || where wkhtmltopdf`. If missing, auto-install:

| Platform | Install command |
|---|---|
| Windows | `winget install wkhtmltopdf` |
| macOS | `brew install wkhtmltopdf` |
| Linux | `sudo apt-get install -y wkhtmltopdf` |

Tell the user: "Installing PDF tool (one-time)…"

**Step 2: Save HTML.**

```
~/.claude/daily-stock-reports/<market>-report-<YYYY-MM-DD>.html
```

**Step 3: Convert to PDF.**

```bash
wkhtmltopdf --encoding UTF-8 \
  --page-size A4 \
  --margin-top 15mm --margin-bottom 15mm \
  --margin-left 12mm --margin-right 12mm \
  report.html report.pdf
```

Output: `<market>-report-<YYYY-MM-DD>.pdf` in the same directory.

**Step 4: Print summary in conversation.**

Show: market, date, key index moves, top mover, PDF path.

**Step 5: Update tracker.**

Append one line to `trackers/<market>-tracker.md`:

```
| <YYYY-MM-DD> | <index change%> | <top mover> | <key theme> |
```

### Market auto-detection (no parameter)

- 4-digit code (9988, 0700) → HK stock
- 6-digit code (600519, 000858) → A-share
- 1-5 letters (AAPL, TSLA) → US stock
- Otherwise → ask user

## Templates

Each template in `templates/` defines:
1. Report header format
2. Ordered sections with `chart:` tags (`table`, `bar`, `flow`, `none`)
3. Tracker entry format

Users can edit templates to customize report structure without touching SKILL.md.

## Trackers

Each tracker in `trackers/` is a running knowledge log:
- Markdown table with daily entries
- Progressive curriculum (week 1: basic indices, week 2: sector rotation, week 3: fund flows, week 4: derivatives/options)
- Append-only — the skill never deletes entries
