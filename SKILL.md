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

## Important: wkhtmltopdf Rendering Limitations

wkhtmltopdf uses QtWebKit (an old browser engine). The following characters **DO NOT render**
and will appear as blank boxes (tofu) in the PDF:

- All emoji: U+1F300-U+1F9FF range
- All flag emoji: U+1F1E6-U+1F1FF range
- Geometric dingbats: U+2700-U+27BF range
- Miscellaneous symbols: U+2600-U+26FF range
- Arrows: U+2190-U+21FF range
- Triangles and blocks: U+25A0-U+25FF range

**Rule: Never use any of the above character ranges in report HTML.**
Use plain Chinese/English text instead. For example:
- Use "[涨]" instead of green arrow up
- Use "[跌]" instead of red arrow down
- Use section numbers instead of emoji icons
- Use the word "上涨" / "下跌" instead of triangles

## CSS & Font Specification

Always use these exact colors and fonts in every report:

**Colors:**
- Gain green: `#16a34a`
- Loss red: `#dc2626`
- Background: `#ffffff`
- Table header bg: `#f1f5f9`
- Table header border: `#cbd5e1`
- Row border: `#e2e8f0`
- Callout bg (info): `#eff6ff`, border: `#2563eb`
- Callout bg (warn): `#fffbeb`, border: `#f59e0b`

**Font stack (Chinese-friendly, works in wkhtmltopdf QtWebKit):**
```css
font-family: "Microsoft YaHei", "SimHei", "PingFang SC", "Hiragino Sans GB", sans-serif;
```

**Core CSS (include verbatim in every report):**

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: "Microsoft YaHei", "SimHei", "PingFang SC", "Hiragino Sans GB", sans-serif;
  color: #1e293b; background: #fff; max-width: 800px;
  margin: 0 auto; padding: 40px 32px; line-height: 1.8;
}
h1 { font-size: 26px; margin-bottom: 4px; color: #0f172a; }
.meta { font-size: 13px; color: #64748b; margin-bottom: 28px; }
h2 { font-size: 20px; margin: 36px 0 12px 0; padding-bottom: 6px;
     border-bottom: 3px solid #2563eb; color: #0f172a; }
h3 { font-size: 16px; margin: 18px 0 8px 0; color: #334155; }
p { margin: 6px 0 10px 0; font-size: 15px; color: #334155; }
ul { margin: 8px 0 12px 0; padding-left: 20px; }
li { font-size: 15px; color: #334155; margin: 4px 0; }
strong { color: #0f172a; }

/* Tables */
.data-table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }
.data-table th { background: #f1f5f9; text-align: left; padding: 10px 12px;
                 border-bottom: 2px solid #cbd5e1; font-weight: 700; font-size: 14px; color: #334155; }
.data-table td { padding: 9px 12px; border-bottom: 1px solid #e2e8f0; font-size: 14px; }
.up { color: #16a34a; font-weight: 700; }
.down { color: #dc2626; font-weight: 700; }
.note { font-size: 13px; color: #64748b; }

/* Bar charts */
.bar-section { margin: 20px 0; }
.bar-chart { margin: 8px 0 18px 0; }
.bar-row { display: flex; align-items: center; margin: 5px 0; }
.bar-label { width: 120px; font-weight: 600; font-size: 14px;
             text-align: right; padding-right: 12px; color: #334155; }
.bar-track { flex: 1; background: #f1f5f9; border-radius: 4px; height: 26px; }
.bar-fill { height: 26px; border-radius: 4px; color: #fff; font-size: 12px;
            line-height: 26px; padding: 0 10px; font-weight: 700; white-space: nowrap; }
.bar-fill.up { background: #16a34a; }
.bar-fill.down { background: #dc2626; }

/* Knowledge cards */
.knowledge-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;
                  padding: 16px 20px; margin: 16px 0; }
.knowledge-card h4 { font-size: 15px; color: #2563eb; margin-bottom: 6px; }
.knowledge-card p { font-size: 14px; }

/* Callout boxes */
.callout { background: #eff6ff; border-left: 4px solid #2563eb;
           padding: 14px 18px; margin: 18px 0; border-radius: 0 6px 6px 0;
           font-size: 14px; color: #1e40af; line-height: 1.7; }
.callout.warn { background: #fffbeb; border-left-color: #f59e0b; color: #92400e; }

.page-break { page-break-before: always; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 40px 0 16px 0; }
.footer { font-size: 12px; color: #94a3b8; text-align: center; }

/* Index summary cards */
.summary-box { width: 100%; margin: 20px 0; }
.summary-table { width: 100%; border-collapse: collapse; }
.summary-table td { width: 33%; padding: 16px 10px; text-align: center;
                    border: 1px solid #e2e8f0; background: #f8fafc; }
.summary-table .slabel { font-size: 13px; color: #64748b; }
.summary-table .svalue { font-size: 22px; font-weight: 700; color: #0f172a; margin: 4px 0; }
.summary-table .schange { font-size: 15px; font-weight: 700; }
```

**Bar chart HTML template (use when template says `chart: bar`):**

```html
<div class="bar-section">
  <h3>领涨板块</h3>
  <div class="bar-chart">
    <div class="bar-row"><span class="bar-label">板块名</span><div class="bar-track"><div class="bar-fill up" style="width:64%">+3.2%</div></div></div>
    <!-- repeat for 5 sectors -->
  </div>
  <h3>领跌板块</h3>
  <div class="bar-chart">
    <div class="bar-row"><span class="bar-label">板块名</span><div class="bar-track"><div class="bar-fill down" style="width:42%">-2.1%</div></div></div>
    <!-- repeat for 5 sectors -->
  </div>
</div>
```

Bar width formula: `width = (abs(change%) / max_abs_change%) * 100`, capped at 100%.
For example, if the largest sector gain is +2.0%, set `max_abs_change%` to 2.0.

## Workflow

### Phase 0 -- Parameter Resolution

Parse user input:

| User input | Market | Template |
|---|---|---|
| `美股` / `us` / `US` | US stocks | `templates/us-stock.md` |
| `港股` / `hk` / `HK` | HK stocks | `templates/hk-stock.md` |
| `A股` / `a-stock` / `CN` | A-shares | `templates/a-stock.md` |
| Anything else / empty | Ask user | -- |

If no parameter, use AskUserQuestion:

> Which market do you want a daily report for?

Options:
- US Stocks (美股) -- S&P 500, NASDAQ, Dow Jones
- HK Stocks (港股) -- Hang Seng Index, Southbound flow
- A-Shares (A股) -- Shanghai Composite, Shenzhen Component
- Other / Crypto -- Generic market template

### Phase 1 -- Data Collection

Use **WebSearch** to gather real-time data. Run searches in parallel based on market:

**US Stocks:**
1. `S&P 500 NASDAQ Dow Jones today market summary`
2. `US stock market top movers gainers losers today`
3. `Federal Reserve interest rate outlook latest`
4. `US Treasury yields 2Y 10Y VIX dollar index today`
5. `NASDAQ sector performance technology stocks sentiment today`

**HK Stocks:**
1. `Hang Seng Index today market summary`
2. `Southbound northbound stock connect flow today`
3. `Hong Kong stock market top movers today`
4. `Hang Seng sector rotation leading lagging today`
5. `Hong Kong monetary policy HIBOR today`

**A-Shares:**
1. `上证指数 深证成指 今日行情 summary`
2. `A股板块轮动 领涨领跌板块 今日`
3. `北向资金 今日流向`
4. `A股市场情绪 成交量 涨跌比 今日`
5. `中国央行货币政策 宏观政策 最新`

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
Sectors: <leading/lagging, 5 each>
Flows: <net inflow/outflow>
Sentiment: <VIX level, advance/decline ratio, volume>
Watchlist: <ticker: price, change%, headline> (if any)
```

### Phase 2 -- HTML Report Generation

Read the template file from `templates/`. Each section has a `chart:` tag
that determines the output format:

| Tag | Output |
|---|---|
| `chart: table` | CSS-styled data table, red/green color coding |
| `chart: bar` | Pure CSS horizontal bar chart (sector performance) |
| `chart: flow` | Flow comparison bar chart (northbound/southbound) |
| `chart: none` | Prose analysis paragraph only |

Generate a **self-contained HTML file** using the exact CSS specification above.

Report structure (follow template section order):

1. **三大指数概览** (chart: table) -- Summary cards + detailed table
2. **纳斯达克深度分析** (chart: none) -- Trend, sector contributions, star stocks, sentiment
3. **涨跌幅最大个股** (chart: table) -- 5 stocks with reasons
4. **五大维度涨跌归因** (chart: table) -- Policy, capital, sentiment, technical, fundamental
5. **板块轮动** (chart: bar) -- 5 leading + 5 lagging sectors
6. **宏观环境** (chart: none) -- Yields, DXY, VIX, Fed, geopolitics
7. **今日关注前瞻** (chart: none) -- Earnings, data, technical levels
8. **今日知识点** (chart: none) -- 1 finance concept + 1 stock market tip
9. **自选股追踪** (chart: table, optional) -- Only if watchlist has entries

The report should be:
- **Data-driven**: cite numbers, not vague adjectives
- **Comprehensive**: 8-9 sections covering all dimensions
- **Actionable**: end with "今日关注前瞻" and knowledge takeaways
- **All Chinese**: section titles, analysis text, table headers -- all in Chinese. Only ticker symbols (AAPL, TSLA) and standard abbreviations (CPI, PCE, VIX, DXY, FOMC) may stay in English

**Five dimensions analysis (Section 4) details:**

Each dimension gets a 1-sentence verdict and 1-2 sentence rationale:

| Dimension | Verdict options | Data sources |
|---|---|---|
| 政策面 | 利好 / 中性 / 利空 | Fed speak, fiscal policy, regulations |
| 资金面 | 净流入 / 平衡 / 净流出 | Volume, capital flows, margin debt |
| 情绪面 | 乐观 / 中性 / 恐慌 | VIX, advance/decline, safe haven demand |
| 技术面 | 偏多 / 震荡 / 偏空 | Moving averages, support/resistance, RSI |
| 基本面 | 改善 / 平稳 / 恶化 | Earnings, economic data, guidance |

**Knowledge tips (Section 8) details:**

Follow the weekly rotation:

| Week | Finance topic area | Stock topic area |
|---|---|---|
| Week 1 | Macro indicators (CPI/PCE/GDP/PMI) | Market basics (indices/volume/technicals) |
| Week 2 | Monetary policy tools | Sector rotation |
| Week 3 | Fixed income | Stock analysis (earnings/valuation) |
| Week 4 | Derivatives | Capital flows |

Refer to `trackers/knowledge-tracker.md` to find the last topic covered, then pick the next one in sequence. Each knowledge tip must include:
- Topic number (e.g., #1, #2) for continuity
- 3-5 sentence explanation in plain Chinese
- Connection to current market context when possible

### Phase 3 -- PDF Output & Record

**Step 1: Ensure wkhtmltopdf is available.**

Check with `which wkhtmltopdf || where wkhtmltopdf`. On Windows, look in
`/c/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe`. If missing, auto-install:

| Platform | Install command |
|---|---|
| Windows | `winget install wkhtmltopdf` |
| macOS | `brew install wkhtmltopdf` |
| Linux | `sudo apt-get install -y wkhtmltopdf` |

Tell the user: "Installing PDF tool (one-time)..."

**Step 2: Save HTML.**

Save to the project's `reports/daily-stock/` directory:

```
<project-root>/reports/daily-stock/<market>-report-<YYYY-MM-DD>.html
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

Show: market, date, key index moves, top mover, knowledge tips given, PDF path.

**Step 5: Update trackers.**

Append one line to `trackers/<market>-tracker.md`:

```
| <YYYY-MM-DD> | <index change%> | <top mover ticker> <%> | <5-word theme> |
```

Append one line to `trackers/knowledge-tracker.md`:

```
| <YYYY-MM-DD> | 金融: <concept> (#<N>) | 股市: <tip> (#<M>) |
```

### Market auto-detection (no parameter)

- 4-digit code (9988, 0700) -> HK stock
- 6-digit code (600519, 000858) -> A-share
- 1-5 letters (AAPL, TSLA) -> US stock
- Otherwise -> ask user

## Templates

Each template in `templates/` defines:
1. Report header format
2. Ordered sections with `chart:` tags (`table`, `bar`, `flow`, `none`)
3. Tracker entry format

Users can edit templates to customize report structure without touching SKILL.md.

## Trackers

Each tracker in `trackers/` is a running knowledge log:

**Market tracker (`<market>-tracker.md`):**
- Markdown table with daily entries
- Progressive curriculum: week 1 (indices), week 2 (sectors), week 3 (flows), week 4 (derivatives/options)
- Append-only -- the skill never deletes entries

**Knowledge tracker (`knowledge-tracker.md`):**
- Markdown table with daily knowledge entries
- Tracks which finance and stock topics have been covered
- Ensures progressive knowledge building without repetition
- 4-week rotation cycle across 8 knowledge areas
- Append-only -- never deletes entries
