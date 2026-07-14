# US Stock Daily Report Template

## Report Header

```
# 🇺🇸 US Stock Market Daily Report — {{DATE}}
```

> **Data as of:** market close {{DATE}} · Sources: WebSearch
> **Indices:** S&P 500 · NASDAQ Composite · Dow Jones Industrial Average

---

## Sections

### 1. Index Snapshot 📊
**chart: table**

Report the day's performance for all three major indices in a styled table.
Red/green color coding: green for gains, red for losses.

Columns: Index | Close | Change | % Change

One-line driver for each index (e.g., "tech rallied on AI earnings").

### 2. Top Movers 🚀
**chart: table**

3-5 stocks that moved the most today in a table.
Columns: Ticker | Price | Change % | Reason (one sentence)

Prioritize well-known names.

### 3. Sector Rotation 🔄
**chart: bar**

Top 5 gaining GICS sectors as green bars, bottom 5 losing sectors as red bars.
CSS bar chart: `.bar-fill.up` for leaders, `.bar-fill.down` for laggards.

Mention 1-2 sentences on what's driving the rotation.

### 4. Macro Pulse 📡
**chart: none**

Key macro signals (prose only):
- Treasury yields (2Y, 10Y) — direction
- US Dollar Index (DXY) — direction
- VIX — level and direction
- Fed speak or data releases

### 5. What to Watch ⏳
**chart: none**

2-3 concrete events for the next trading day (prose only):
- Earnings reports after close / before open
- Economic data releases
- Technical levels (S&P 500 support/resistance)

---

## Tracker Entry Format

```
| {{YYYY-MM-DD}} | S&P 500 {{change%}} | {{top mover ticker}} {{%}} | {{5-word theme}} |
```
