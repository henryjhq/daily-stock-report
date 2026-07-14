# Generic Market Daily Report Template

## Report Header

```
# 📊 Market Daily Report — {{TICKERS/MARKET}} — {{DATE}}
```

> **Data as of:** {{DATE}} · Sources: WebSearch
> **Coverage:** {{user-specified tickers or market description}}

---

## Sections

### 1. Price Snapshot 📊
**chart: table**

Styled table for each ticker/asset:

Columns: Asset | Price | 1D Δ% | 7D Δ% | YTD Δ%

Red/green color coding.

### 2. Market Context 🌍
**chart: none**

Broader macro context (prose only):
- Relevant index performance
- Sector trends
- Key macro driver (rates, currency, commodity)
- Cross-asset signals

### 3. News & Catalysts 📰
**chart: none**

2-4 recent news items or catalysts (prose only):
- Earnings, regulations, macro data, geopolitics, industry news

### 4. Sentiment Check 🧭
**chart: bar**

CSS bar chart showing sentiment signals if data available:
- Social sentiment, analyst ratings, fund flows

If insufficient data, fall back to prose.

### 5. What to Watch ⏳
**chart: none**

2-3 concrete events to monitor (prose only):
- Key price levels (support/resistance/breakout)
- Upcoming catalysts
- Correlation risks

---

## Tracker Entry Format

```
| {{YYYY-MM-DD}} | {{primary ticker}} {{change%}} | {{key catalyst}} | {{5-word theme}} |
```
