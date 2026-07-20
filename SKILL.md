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

### Prerequisite: Read theme.json

Before generating the HTML, read `theme.json` from the skill directory.
If it doesn't exist, create it using the default values below.
Use the theme values to populate all CSS. The colors below are the
**default theme** — substitute with theme.json values when available.

**Default colors (from theme.json):**
- Background: `#ffffff`
- Surface (card/table header bg): `#f8fafc`
- Surface border: `#e2e8f0`
- Text primary: `#0f172a` | Text body: `#334155` | Text muted: `#64748b`
- Accent: `#2563eb` | Accent light: `#eff6ff`
- Gain green: `#16a34a` | Loss red: `#dc2626`
- Warn: `#f59e0b` | Warn light: `#fffbeb`

**Font stack (Chinese-friendly, works in wkhtmltopdf QtWebKit):**
```css
font-family: "Microsoft YaHei", "SimHei", "PingFang SC", "Hiragino Sans GB", sans-serif;
```

**Core CSS (include verbatim in every report, substituting theme values):**

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: "Microsoft YaHei", "SimHei", "PingFang SC", "Hiragino Sans GB", sans-serif;
  color: #334155; background: #ffffff; max-width: 800px;
  margin: 0 auto; padding: 48px 40px; line-height: 1.8;
  /* AI-generated background texture (4% opacity, barely visible when printed) */
  background-image: url('../assets/decorations/bg-texture.png');
  background-repeat: repeat;
  background-size: 400px 400px;
  background-blend-mode: multiply;
}

/* ===== Header ===== */
.report-header { margin-bottom: 40px; padding-bottom: 24px;
                 border-bottom: 1px solid #e2e8f0; }
.report-header h1 { font-size: 28px; margin-bottom: 6px; color: #0f172a;
                    letter-spacing: -0.5px; }
.report-header .meta { font-size: 13px; color: #64748b; }

/* ===== Section headings ===== */
h2 { font-size: 20px; margin: 44px 0 16px 0; padding-bottom: 8px;
     border-bottom: 3px solid #2563eb; color: #0f172a; }
h3 { font-size: 16px; margin: 20px 0 10px 0; color: #334155; }
p { margin: 8px 0 12px 0; font-size: 15px; color: #334155; }
ul { margin: 8px 0 12px 0; padding-left: 20px; }
li { font-size: 15px; color: #334155; margin: 4px 0; }
strong { color: #0f172a; }

/* ===== Tables (with optional stripe) ===== */
.data-table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }
.data-table th { background: #f8fafc; text-align: left; padding: 10px 12px;
                 border-bottom: 2px solid #e2e8f0; font-weight: 700; font-size: 14px; color: #334155; }
.data-table td { padding: 9px 12px; border-bottom: 1px solid #e2e8f0; font-size: 14px; }
/* Alternating row stripe (when tableStripe: true) */
.data-table.striped tr:nth-child(even) td { background: #f8fafc; }

/* ===== Color indicators ===== */
.up { color: #16a34a; font-weight: 700; }
.down { color: #dc2626; font-weight: 700; }
.note { font-size: 13px; color: #64748b; }

/* ===== Focus number (highlight the day's key metric) ===== */
.focus-number { display: inline-block; background: #eff6ff; color: #2563eb;
                padding: 2px 10px; border-radius: 4px; font-weight: 700; }

/* ===== Bar charts (sector performance) ===== */
.bar-section { margin: 20px 0; }
.bar-chart { margin: 8px 0 18px 0; }
.bar-row { display: flex; align-items: center; margin: 5px 0; }
.bar-label { width: 120px; font-weight: 600; font-size: 14px;
             text-align: right; padding-right: 12px; color: #334155; }
.bar-track { flex: 1; background: #f8fafc; border-radius: 4px; height: 26px; }
.bar-fill { height: 26px; border-radius: 4px; color: #fff; font-size: 12px;
            line-height: 26px; padding: 0 10px; font-weight: 700; white-space: nowrap; }
.bar-fill.up { background: #16a34a; }
.bar-fill.down { background: #dc2626; }

/* ===== Line & K-line charts (SVG) ===== */
.line-section, .kline-section { margin: 20px 0; }
.line-charts-grid, .kline-charts-grid { display: flex; flex-wrap: wrap; gap: 16px; margin: 16px 0; }
.line-chart-card, .kline-chart-card { flex: 1; min-width: 220px; background: #f8fafc;
                                      border: 1px solid #e2e8f0; border-radius: 8px;
                                      padding: 14px 12px 8px 12px; }
.line-chart-card .chart-title, .kline-chart-card .chart-title { font-size: 14px;
    font-weight: 700; color: #0f172a; margin-bottom: 2px; text-align: center; }
.line-chart-card .chart-subtitle, .kline-chart-card .chart-subtitle { font-size: 11px;
    color: #64748b; text-align: center; margin-bottom: 6px; }
.line-chart-svg { width: 100%; height: auto; display: block; }

/* ===== Metric cards (key numbers) ===== */
.metric-row { display: flex; gap: 16px; margin: 20px 0; flex-wrap: wrap; }
.metric-card { flex: 1; min-width: 140px; background: #f8fafc;
               border: 1px solid #e2e8f0; border-radius: 8px;
               padding: 18px 14px; text-align: center; }
.metric-card .metric-value { font-size: 28px; font-weight: 700; color: #0f172a; line-height: 1.2; }
.metric-card .metric-label { font-size: 12px; color: #64748b; margin-top: 4px; }

/* ===== Pull quote (key insight highlight) ===== */
.pull-quote { font-size: 17px; font-weight: 600; color: #2563eb; text-align: center;
              padding: 18px 28px; margin: 24px 0;
              border-top: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; }

/* ===== Knowledge cards ===== */
.knowledge-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;
                  padding: 16px 20px; margin: 16px 0; }
.knowledge-card h4 { font-size: 15px; color: #2563eb; margin-bottom: 6px; }
.knowledge-card p { font-size: 14px; }

/* ===== Callout boxes ===== */
.callout { background: #eff6ff; border-left: 4px solid #2563eb;
           padding: 14px 18px; margin: 18px 0; border-radius: 0 6px 6px 0;
           font-size: 14px; color: #1e40af; line-height: 1.7; }
.callout.warn { background: #fffbeb; border-left-color: #f59e0b; color: #92400e; }
.callout.bullish { background: #f0fdf4; border-left-color: #16a34a; color: #166534; }
.callout.bearish { background: #fef2f2; border-left-color: #dc2626; color: #991b1b; }

/* ===== Section divider ===== */
.section-divider { width: 100%; height: 1px; background: #e2e8f0; margin: 36px 0 20px 0; }
.section-divider.accent { height: 3px; background: #2563eb; }
.section-divider.fade { height: 1px; background: linear-gradient(
  90deg, transparent 0%, #e2e8f0 20%, #e2e8f0 80%, transparent 100%); }

/* ===== Page layout ===== */
.page-break { page-break-before: always; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 40px 0 16px 0; }

/* ===== Footer ===== */
.report-footer { margin-top: 48px; padding-top: 16px;
                 border-top: 1px solid #e2e8f0; font-size: 11px;
                 color: #94a3b8; text-align: center; }

/* ===== Index summary cards ===== */
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

**SVG line chart template (use when template says `chart: line`):**

For each index, render a card with an SVG line chart showing ~20 trading days.

SVG coordinate calculation:
```
chart_width = 520 (plot area), chart_height = 150 (plot area)
margin_left = 45, margin_top = 10
points = 20-22 data items

x_spacing = chart_width / (points - 1)
min_price = min(all closes) * 0.995
max_price = max(all closes) * 1.005
price_range = max_price - min_price

For data point i:
  x = margin_left + i * x_spacing
  y = margin_top + (1 - (close[i] - min_price) / price_range) * chart_height
```

Line color rule:
- If last close >= first close: green (#16a34a)
- If last close < first close: red (#dc2626)

```html
<div class="line-section">
  <h3>指数近一月走势</h3>
  <div class="line-charts-grid">
    <!-- One card per index. Repeat for each index (usually 3). -->
    <div class="line-chart-card">
      <div class="chart-title">S&P 500</div>
      <div class="chart-subtitle">近20个交易日 · [涨/跌] X.X%</div>
      <svg viewBox="0 0 580 200" class="line-chart-svg">
        <!--
        SVG STRUCTURE (from back to front):
        1. Horizontal grid lines (4 lines, y evenly spaced)
        2. Y-axis labels (price values, right-aligned at x=38)
        3. Area fill: <polygon> from first point down to bottom-right then bottom-left, back to first
           - fill="rgba(22,163,74,0.08)" for up, "rgba(220,38,38,0.08)" for down
        4. Price line: <polyline> through all data points
           - fill="none", stroke="#16a34a" or "#dc2626", stroke-width="2", stroke-linejoin="round"
        5. First and last data dots: <circle> r="3", plus a label
           - First dot: <circle cx="x0" cy="y0" r="3" fill="#64748b"/>
           - Last dot: <circle cx="xN" cy="yN" r="4" fill="same as line color"/>
        6. X-axis date labels: every ~5th date, y=192, text-anchor="middle", font-size="9", fill="#94a3b8"
        -->
      </svg>
    </div>
    <!-- ... more index cards ... -->
  </div>
  <p class="note">* 数据来源：公开市场数据，每日收盘价。折线仅反映收盘价变化，不含盘中波动。</p>
</div>
```

**SVG construction rules:**

1. **Grid lines**: 4 horizontal `<line>` elements at y = margin_top + 0%, 33%, 66%, 100% of chart_height.
   Stroke: `#e2e8f0`, stroke-width: 1.

2. **Y-axis labels**: 4 `<text>` elements at each grid line. Use `text-anchor="end"`, x=38.
   Show rounded price values. Font: 10px, fill: `#64748b`.

3. **Area fill**: `<polygon>` with `points="x0,y0 x1,y1 ... xN,yN xN,bottom y_bottom,bottom x0,bottom"`.
   The bottom is margin_top + chart_height.

4. **Price line**: `<polyline>` with `points="x0,y0 x1,y1 ... xN,yN"`.
   Use `stroke-linejoin="round"` and `stroke-linecap="round"`.

5. **Data dots**: Only mark the first and last point.
   First: r="3", fill="#64748b". Last: r="4", fill=line color.

6. **X-axis labels**: Pick indices 0, 4, 9, 14, 19 (roughly every 5th). Show MM-DD format.
   y = margin_top + chart_height + 18. Font: 9px, fill: `#94a3b8`.

7. **Chart subtitle**: Show date range and net change (e.g. "06/20 - 07/18 · 涨 +3.2%").
   Use `.up` / `.down` class for the change.

8. **Card layout**: 3 cards per row on desktop (flex-wrap wraps to new row).
   If only 2 indices, 2 cards. If 4 indices, 2 rows of 2.

**Multi-index layering (optional variant):**

For markets where all indices share similar scale (e.g., US: all 3 are index points),
render all lines on ONE chart with a legend:

```html
<svg viewBox="0 0 580 220" class="line-chart-svg">
  <!-- Same grid, but 3 polylines with different colors: -->
  <!-- S&P 500: #2563eb (blue) -->
  <!-- NASDAQ: #16a34a (green) -->
  <!-- Dow Jones: #f59e0b (amber) -->
  <!-- Legend at top-right: colored line + index name -->
</svg>
```

Use this variant only for US stocks (indices are comparable: S&P ~5800, NASDAQ ~19000, Dow ~42000).
For HK and A-shares, use separate cards (indices have very different scales).

**SVG K-line (candlestick) chart template (use when template says `chart: kline`):**

K-line charts show OHLC (Open/High/Low/Close) for each trading day, giving richer
information than line charts. Each "candle" shows the day's price range and direction.

Color convention (match report colors):
- Yang (close >= open): green body `#16a34a`
- Yin (close < open): red body `#dc2626`

SVG coordinate calculation:
```
chart_width = 520 (plot area), chart_height = 145 (plot area)
margin_left = 50, margin_top = 10
candles = 15-20 OHLC data points

candle_spacing = chart_width / candles.length
candle_body_width = Math.min(candle_spacing * 0.65, 12)

min_price = min(all lows) * 0.995
max_price = max(all highs) * 1.005
price_range = max_price - min_price

For candle i:
  center_x = margin_left + i * candle_spacing + candle_spacing / 2
  open_y  = margin_top + (1 - (open[i]  - min_price) / price_range) * chart_height
  close_y = margin_top + (1 - (close[i] - min_price) / price_range) * chart_height
  high_y  = margin_top + (1 - (high[i]  - min_price) / price_range) * chart_height
  low_y   = margin_top + (1 - (low[i]   - min_price) / price_range) * chart_height

  body_top = Math.min(open_y, close_y)
  body_h = Math.max(Math.abs(close_y - open_y), 1)  // minimum 1px for doji
  is_yang = close[i] >= open[i]
  color = is_yang ? "#16a34a" : "#dc2626"
```

```html
<div class="kline-section">
  <h3>指数近一月K线图</h3>
  <div class="kline-charts-grid">
    <div class="kline-chart-card">
      <div class="chart-title">S&P 500</div>
      <div class="chart-subtitle">
        近{{N}}个交易日 · 开盘 {{open[0]}} · 收盘 {{close[last]}} ·
        <span class="[up|down]">[涨|跌] X.X%</span>
      </div>
      <svg viewBox="0 0 580 210" class="line-chart-svg">
        <!--
        SVG STRUCTURE (back to front):
        1. Horizontal grid lines (4 lines)
           <line x1="50" y1="y" x2="570" y2="y" stroke="#e2e8f0" stroke-width="1"/>
        2. Y-axis labels (4 price labels, right-aligned at x=45)
           <text x="45" y="y+4" text-anchor="end" font-size="10" fill="#64748b">price</text>
        3. For each candle (loop i from 0 to N-1):
           a. Wick: <line x1="cx" y1="high_y" x2="cx" y2="low_y"
                          stroke="color" stroke-width="1"/>
           b. Body: <rect x="cx - bw/2" y="body_top"
                          width="bw" height="body_h"
                          fill="color"/>
        4. 5-day moving average line (optional but recommended):
           <polyline points="..." fill="none" stroke="#f59e0b" stroke-width="1.5"
                     stroke-dasharray="4,2" opacity="0.7"/>
           With a legend label: "MA5"
        5. X-axis date labels: every ~4th candle, y=190, text-anchor="middle",
           font-size="9", fill="#94a3b8"
        -->
      </svg>
    </div>
    <!-- ... more index cards ... -->
  </div>
  <p class="note">* K线图中，实体为当日开盘至收盘价区间，影线为当日最高最低价。绿涨红跌。虚线为5日均线。</p>
</div>
```

**K-line rendering notes:**

1. **Minimum body height**: Always clamp `body_h` to at least 1px so doji (flat) candles are visible as a thin line.

2. **Wick line**: Always draw from `high_y` to `low_y`. The body rect draws on top, covering the middle portion.

3. **MA5 line (5-day moving average)**: Calculate 5-day SMA of close prices. Plot as a dashed polyline in amber (#f59e0b). This adds valuable context. Skip MA5 if fewer than 10 candles.

4. **Grid lines**: 4 horizontal lines covering the price range from min_price to max_price. Label each with a rounded price value.

5. **X-axis**: Show every 4th date label to avoid crowding. With 15-20 candles, this gives 4-5 labels.

6. **Chart card layout**: Same card grid as line charts — `.kline-charts-grid` uses flex-wrap.

7. **When to use K-line vs line chart**:
   - `chart: kline` — primary choice for the monthly trend section (richer info)
   - `chart: line` — fallback when OHLC data is unavailable
   - Both can be shown side-by-side if space permits

**Combined K-line + line chart card CSS:**

```css
/* K-line charts */
.kline-section { margin: 20px 0; }
.kline-charts-grid { display: flex; flex-wrap: wrap; gap: 16px; margin: 16px 0; }
.kline-chart-card { flex: 1; min-width: 220px; background: #f8fafc;
                    border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 12px 8px 12px; }
.kline-chart-card .chart-title { font-size: 14px; font-weight: 700; color: #0f172a;
                                  margin-bottom: 2px; text-align: center; }
.kline-chart-card .chart-subtitle { font-size: 11px; color: #64748b;
                                    text-align: center; margin-bottom: 6px; }
```

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

**Read theme.json:**

After market resolution, read `theme.json` from the skill directory.
If it doesn't exist, create it with default values (see "Theme File Quick-Start").
Use the theme values to populate all CSS colors and styles in the report.

If the user says things like "换个暖色背景", "用深色主题", "字体大一点",
update the corresponding key in `theme.json` before proceeding.

**Check AI decorations — ask user if not configured:**

Before Phase 1, check the decoration status:

- If `aiDecorations` is `true` AND `imageApi.apiKey` is a real key (not placeholder): proceed to generate.
- If `aiDecorations` is `false` OR `imageApi.apiKey` is `"YOUR_API_KEY_HERE"`: ask the user ONCE per session:

  > 想让报告更好看吗？接入图片生成 API（Seedream / DALL-E / Stability）可以自动生成报告背景纹理和装饰元素，让 PDF 更有质感。
  >
  > 选项：
  > - A) 我有火山引擎 Seedream API Key（推荐，500 次免费）
  > - B) 我有 OpenAI DALL-E API Key
  > - C) 我有其他图片生成 API
  > - D) 跳过，纯白背景就挺好

  - If A: guide user to get Seedream key from https://console.volcengine.com/ark/ → paste into `theme.json` → `imageApi.apiKey`. Set `"provider": "seedream"`, update endpoint/model if needed.
  - If B: set `"provider": "openai"`, `"endpoint": "https://api.openai.com/v1/images/generations"`, `"model": "dall-e-3"`, ask user for key.
  - If C: ask user for endpoint, model, and key. Fill `imageApi` accordingly.
  - If D: set `"aiDecorations": false`, proceed without decorations.

  After user configures: set `"aiDecorations": true`, save `theme.json`, then proceed to generate decoration assets below.

**Generate decoration assets (run once, skip if already exist):**

If `aiDecorations` is `true` and `imageApi` is configured:

1. Check if `assets/decorations/bg-texture.png` exists. If yes, skip generation.
2. Call the configured image API:
   - Endpoint: `imageApi.endpoint` (POST)
   - Authorization: `imageApi.headers.Authorization` (replace `{{apiKey}}` with `imageApi.apiKey`)
   - Body: `{"model": "<imageApi.model>", "prompt": "<decorationPrompt>", "size": "<imageApi.size>", "response_format": "<imageApi.responseFormat>", ...<imageApi.extraBody>}`
3. If `responseFormat` is `b64_json`: decode base64 and save as PNG to `assets/decorations/bg-texture.png`.
   If `responseFormat` is `url`: download the URL and save.
4. Report: "Generated background texture via {provider} — saved to assets/decorations/"

**Image API configuration (for users):**

Users can plug in ANY image generation API by editing `theme.json` → `imageApi`:

| Provider | Example config |
|---|---|
| **Seedream (火山引擎)** | `"endpoint": "https://ark.cn-beijing.volces.com/api/v3/images/generations"`, `"model": "doubao-seedream-5-0-pro-260628"` |
| **OpenAI DALL-E** | `"endpoint": "https://api.openai.com/v1/images/generations"`, `"model": "dall-e-3"`, `"size": "1024x1024"` |
| **Stability AI** | `"endpoint": "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"`, customize headers/body |
| **Custom / 其他** | Any OpenAI-compatible or custom endpoint — just set `endpoint`, `headers`, and `extraBody` |

To switch providers, the user only needs to change:
- `imageApi.provider` — label (for display)
- `imageApi.endpoint` — API URL
- `imageApi.model` — model ID
- `imageApi.apiKey` — their API key
- `imageApi.extraBody` — any provider-specific parameters (e.g., `"quality": "hd"` for DALL-E)

The skill auto-adapts: `Authorization` header + JSON body with `prompt`/`model`/`size` from config.
No code changes needed when switching image API providers.

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

**Historical data for monthly line charts (all markets):**
Search for each index's past-month closing prices. Target: 20-22 trading days.

US:
1. `S&P 500 index daily close prices last 30 days history`
2. `NASDAQ composite daily prices last month 2026`
3. `Dow Jones Industrial Average daily close past 30 days`

HK:
1. `Hang Seng Index HSI daily close prices last 30 days`
2. `Hang Seng TECH Index historical prices past month`
3. `HSCEI China Enterprises Index daily data last 30 days`

A-Share:
1. `上证指数 每日收盘价 近30天 历史数据`
2. `深证成指 近一个月 每日收盘点位`
3. `创业板指 过去30天 收盘价历史`

Generic:
1. `<TICKER> historical daily prices last 30 days`

From search results, extract for each index:
- Start date and end date (last ~20 trading days)
- **For line charts:** daily closing prices (at minimum: start, end, high, low, and 5-8 intermediate points)
- **For K-line charts:** daily OHLC (Open, High, Low, Close) — at least 10-15 trading days with all 4 prices
- Overall trend direction (up/down/sideways)

If exact daily prices are unavailable, interpolate reasonably between known points.
Prefer OHLC data when available — it enables both K-line and line chart rendering.

Store as:
- Line chart: `[{date: "MM-DD", close: NNNNN}, ...]` for each index.
- K-line chart: `[{date: "MM-DD", open: NNNN, high: NNNN, low: NNNN, close: NNNN}, ...]` for each index.

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
Index monthly data: <index>: [{date: "MM-DD", close: NNNNN}, ...] (20-22 data points each)
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
| `chart: line` | Inline SVG line chart (monthly index trend, 20-22 close prices) |
| `chart: kline` | Inline SVG candlestick chart (monthly OHLC, 15-20 candles + MA5) |
| `chart: none` | Prose analysis paragraph only |

Generate a **self-contained HTML file** using the exact CSS specification above.

Report structure (follow template section order):

1. **三大指数概览** (chart: table) -- Summary cards + detailed table
2. **指数近一月走势** (chart: kline) -- SVG candlestick chart per index, 15-20 trading days, green/red candles + MA5 line. Fall back to `chart: line` if OHLC data unavailable.
3. **纳斯达克深度分析** (chart: none) -- Trend, sector contributions, star stocks, sentiment
4. **涨跌幅最大个股** (chart: table) -- 5 stocks with reasons
5. **五大维度涨跌归因** (chart: table) -- Policy, capital, sentiment, technical, fundamental
6. **板块轮动** (chart: bar) -- 5 leading + 5 lagging sectors
7. **宏观环境** (chart: none) -- Yields, DXY, VIX, Fed, geopolitics
8. **今日关注前瞻** (chart: none) -- Earnings, data, technical levels
9. **今日知识点** (chart: none) -- 1 finance concept + 1 stock market tip
10. **自选股追踪** (chart: table, optional) -- Only if watchlist has entries

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

**Step 1: Ensure Playwright + Chromium are available.**

Default PDF renderer: Playwright with headless Chromium (supports modern CSS,
background-images, web fonts, SVG, and AI-generated textures).

Check with:
```bash
python -c "from playwright.sync_api import sync_playwright; print('ok')" 2>&1
```

If not installed:
```bash
pip install playwright
python -m playwright install chromium
```

**Fallback: wkhtmltopdf** (legacy, limited CSS support):

If Playwright is unavailable, use wkhtmltopdf:
```bash
wkhtmltopdf --encoding UTF-8 --page-size A4 --margin-top 15mm --margin-bottom 15mm --margin-left 12mm --margin-right 12mm --enable-local-file-access report.html report.pdf
```

**Reason for switching to Playwright:**
wkhtmltopdf uses QtWebKit (2016 engine) which does NOT support:
- `background-blend-mode`, `background-image` with local files
- Modern CSS Grid/Flexbox properly
- SVG elements like `<polyline>`, `<polygon>`
- `opacity` and CSS filters
- Web fonts loaded via `@font-face`

Playwright + Chromium supports ALL of the above, making AI-generated
background textures, SVG charts, and modern CSS layouts work correctly.

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
2. Ordered sections with `chart:` tags (`table`, `bar`, `flow`, `line`, `kline`, `none`)
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

## Visual Customization & Report Aesthetics

### Philosophy

Financial reports should be: professional, scannable, and visually calm.
The goal is NOT to be flashy — it's to make data easy to read and key
information jump out instantly.

### Customization: Theme Config

Before generating a report, read `theme.json` from the skill directory.
If it doesn't exist, create it with defaults. Users edit this file to
customize their report look.

**`theme.json` format:**

```json
{
  "name": "default-light",
  "background": "#ffffff",
  "surface": "#f8fafc",
  "surfaceBorder": "#e2e8f0",
  "textPrimary": "#0f172a",
  "textBody": "#334155",
  "textMuted": "#64748b",
  "accent": "#2563eb",
  "accentLight": "#eff6ff",
  "gain": "#16a34a",
  "loss": "#dc2626",
  "warn": "#f59e0b",
  "warnLight": "#fffbeb",
  "dividerStyle": "line",
  "headerAccent": "bar",
  "tableStripe": true,
  "cardShadow": false,
  "fontSize": "normal",
  "aiDecorations": false,
  "decorationPrompt": "abstract geometric financial pattern, subtle, light gray, professional, clean lines, suitable for printed report background"
}
```

| Key | Values | Effect |
|---|---|---|
| `background` | Any hex | Page background color |
| `surface` | Any hex | Card/table header background |
| `accent` | Any hex | Section borders, highlights, callout borders |
| `dividerStyle` | `"line"` / `"dot"` / `"thick"` | Section divider appearance |
| `headerAccent` | `"bar"` / `"none"` / `"underline"` | H2 header decoration style |
| `tableStripe` | `true` / `false` | Alternating row colors in tables |
| `cardShadow` | `true` / `false` | Drop shadow on index cards (off for print) |
| `fontSize` | `"small"` / `"normal"` / `"large"` | Base font size scaling |
| `aiDecorations` | `true` / `false` | Enable AI-generated decorative images |
| `decorationPrompt` | string | Prompt used when generating decoration assets |

**Theme presets (quick-switch by changing `name`):**

| Preset | Background | Accent | Vibe |
|---|---|---|---|
| `default-light` | `#ffffff` | `#2563eb` | Clean professional |
| `warm-cream` | `#fefcf5` | `#b45309` | Warm, paper-like |
| `cool-slate` | `#f8fafc` | `#475569` | Minimal, cool tone |
| `ink-blue` | `#f0f4ff` | `#1e40af` | Deep blue professional |
| `dark` | `#1e293b` | `#60a5fa` | Dark mode (screen only — wastes ink for print) |

When the user says "换个暖色背景" or "用深色主题", update `theme.json` `name` and apply the corresponding preset.

### AI-Generated Decorative Elements

**What AI image generation IS good for in reports:**

| Use | Example | When to generate |
|---|---|---|
| Background texture | Subtle geometric pattern, 5% opacity, behind entire page | Once per theme, reused indefinitely |
| Section divider ornament | Small inline SVG/PNG between sections | Once per theme |
| Header accent image | Abstract stock chart / candle pattern behind H1 | Once per theme |
| Cover page illustration | Minimalist financial-themed art for page 1 | Once per theme |
| Pull-quote mark | Decorative quotation mark for key takeaways | Once per theme |

**What AI image generation is NOT for:**
- Data charts (K-line, line, bar) — use SVG
- Tables with numbers — use HTML tables
- Any element where accuracy matters

**Decoration generation workflow (run once, not per report):**

When `aiDecorations` is `true` and assets don't exist yet:

1. Generate background texture image:
   - Prompt: `theme.decorationPrompt` (from theme.json)
   - Size: 400x400px tileable seamless pattern
   - Save: `assets/decorations/bg-texture.png`
   - Apply in HTML: `body { background-image: url('assets/decorations/bg-texture.png'); background-repeat: repeat; }`

2. Generate section divider ornament:
   - Prompt: "minimalist horizontal section divider ornament, single color {accent}, thin line with small geometric accent, transparent background, 600x20px"
   - Save: `assets/decorations/divider.png`
   - Apply in HTML: `<img src="assets/decorations/divider.png" class="section-divider">`

3. Generate header accent:
   - Prompt: "abstract minimalist stock market chart line pattern, {accent} color on transparent background, very faint, professional, 800x80px"
   - Save: `assets/decorations/header-accent.png`
   - Apply in HTML: as background behind report title

**How to generate the images (choose one):**

Option A — DALL-E via OpenAI API (requires API key):
```bash
curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "dall-e-3",
    "prompt": "...",
    "size": "1024x1024",
    "quality": "standard",
    "n": 1
  }'
```
Then crop/resize to needed dimensions.

Option B — Use `/design-html` skill to generate CSS-only decorative elements.
No API key needed, works offline, and produces smaller file sizes.
This is the preferred approach for wkhtmltopdf reports.

Option C — Stock image services (Unsplash, Pexels) for abstract financial
backgrounds. Free, no generation needed.

**Applying decorations in HTML:**

```html
<!-- Background texture (very subtle, 3-5% opacity) -->
<style>
  body {
    background-color: {{theme.background}};
    background-image: url('assets/decorations/bg-texture.png');
    background-repeat: repeat;
    background-blend-mode: overlay;
    background-opacity: 0.04;
  }
</style>

<!-- Section divider -->
<img src="assets/decorations/divider.png"
     style="width:100%; height:12px; margin: 24px 0; opacity:0.6;"
     alt="">

<!-- Header accent bar (pure CSS fallback, always works) -->
<div style="height: 4px; background: linear-gradient(
  90deg, {{theme.accent}} 0%, {{theme.accent}} 40%,
  transparent 40%, transparent 100%
); margin-bottom: 24px;"></div>
```

**Important: Always provide pure CSS fallbacks.** AI-generated images may fail
to generate, may not load in wkhtmltopdf, or the user may not have API access.
The report must look acceptable without any AI-generated assets.

### Enhanced Visual Hierarchy

Beyond color customization, these CSS techniques improve readability:

**1. Section differentiation — accent bar on H2:**
```css
h2 {
  border-bottom: 3px solid {{theme.accent}};
  padding-bottom: 8px;
}
/* Alternative: left accent bar */
h2.accent-left {
  border-bottom: none;
  border-left: 4px solid {{theme.accent}};
  padding-left: 12px;
}
```

**2. Key metric cards (for index summary):**
```css
.metric-card {
  background: {{theme.surface}};
  border: 1px solid {{theme.surfaceBorder}};
  border-radius: 8px;
  padding: 20px 16px;
  text-align: center;
}
.metric-card .metric-value {
  font-size: 28px;
  font-weight: 700;
  color: {{theme.textPrimary}};
  line-height: 1.2;
}
.metric-card .metric-label {
  font-size: 12px;
  color: {{theme.textMuted}};
  text-transform: uppercase;
  letter-spacing: 1px;
}
```

**3. Alternating table rows (when `tableStripe: true`):**
```css
.data-table tr:nth-child(even) td {
  background: {{theme.surface}};
}
```

**4. Callout with icon substitute (no emoji):**
```css
.callout { border-left: 4px solid {{theme.accent}}; }
.callout.warn { border-left: 4px solid {{theme.warn}}; }
.callout.bullish { border-left: 4px solid {{theme.gain}}; }
.callout.bearish { border-left: 4px solid {{theme.loss}}; }
```

**5. Pull quote for key insight:**
```css
.pull-quote {
  font-size: 18px;
  font-weight: 600;
  color: {{theme.accent}};
  text-align: center;
  padding: 20px 32px;
  margin: 24px 0;
  border-top: 1px solid {{theme.surfaceBorder}};
  border-bottom: 1px solid {{theme.surfaceBorder}};
}
```

**6. Focus indicator for the day's most important number:**
```css
.focus-number {
  display: inline-block;
  background: {{theme.accentLight}};
  color: {{theme.accent}};
  padding: 2px 10px;
  border-radius: 4px;
  font-weight: 700;
  font-size: 1.1em;
}
```

### Page Layout Enhancement

```css
/* Better spacing rhythm */
body { max-width: 800px; margin: 0 auto; padding: 48px 40px; }

/* Top header area */
.report-header {
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 1px solid {{theme.surfaceBorder}};
}
.report-header h1 { font-size: 28px; letter-spacing: -0.5px; }

/* Section spacing */
h2 { margin-top: 44px; margin-bottom: 16px; }

/* Footer */
.report-footer {
  margin-top: 48px;
  padding-top: 16px;
  border-top: 1px solid {{theme.surfaceBorder}};
  font-size: 11px;
  color: {{theme.textMuted}};
  text-align: center;
}
```

### QuickChart Integration (Optional, for richer data charts)

When more chart types are needed (radar charts, heatmaps, etc.),
use QuickChart.io as an image source:

```html
<img src="https://quickchart.io/chart?width=600&amp;height=250&amp;c=...URL-encoded JSON..."
     style="width:100%; max-width:600px;" alt="Chart">
```

QuickChart is free, open-source, and renders Chart.js configurations server-side.
Use `&format=svg` for sharper PDF output.

### Summary: How to make reports beautiful

| Priority | Action | Cost | Status |
|---|---|---|---|
| 1 | Use the enhanced CSS — section bars, metric cards, pull quotes | Free, immediate | ✅ Built-in |
| 2 | Customize `theme.json` — pick colors that match your taste | Free, 30 seconds | ✅ 5 presets |
| 3 | Set `aiDecorations: true` + configure `imageApi` — auto-generate background texture once | ~$0.01 once | ✅ Seedream integrated |
| 4 | Switch to Playwright renderer for modern CSS support | +300MB, +3s per PDF | Optional |
| 5 | Integrate QuickChart for more chart variety | Free, network-dependent | Optional |

Do priority 1-3. With the image API configured, every report automatically gets
a subtle background texture that makes it look professionally printed rather than
flat white. Change `decorationPrompt` in theme.json to customize the texture style.

### Theme File Quick-Start

To generate a default `theme.json`:

```bash
cat > theme.json << 'EOF'
{
  "name": "default-light",
  "background": "#ffffff",
  "surface": "#f8fafc",
  "surfaceBorder": "#e2e8f0",
  "textPrimary": "#0f172a",
  "textBody": "#334155",
  "textMuted": "#64748b",
  "accent": "#2563eb",
  "accentLight": "#eff6ff",
  "gain": "#16a34a",
  "loss": "#dc2626",
  "warn": "#f59e0b",
  "warnLight": "#fffbeb",
  "dividerStyle": "line",
  "headerAccent": "bar",
  "tableStripe": true,
  "cardShadow": false,
  "fontSize": "normal",
  "aiDecorations": false,
  "decorationPrompt": "abstract geometric pattern, subtle, light gray, clean simple lines, tileable, minimal, financial report background, 5% visible"
}
EOF
```

When the skill runs, read this file first. Use its values to populate the CSS
variables in the report HTML. If the file doesn't exist, create it with defaults
and proceed.
