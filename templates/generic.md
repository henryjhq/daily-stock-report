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

### 2. 价格近一月走势
**chart: kline** (fallback: chart: line)

各交易标的过去约 15-20 个交易日的 OHLC K 线图，叠加 5 日均线。
每个标独立 SVG 卡片。K 线颜色：绿涨红跌。如 OHLC 数据不足，退化为折线图。

### 3. Market Context 🌍
**chart: none**

Broader macro context (prose only):
- Relevant index performance
- Sector trends
- Key macro driver (rates, currency, commodity)
- Cross-asset signals

### 4. News & Catalysts 📰
**chart: none**

2-4 recent news items or catalysts (prose only):
- Earnings, regulations, macro data, geopolitics, industry news

### 5. Sentiment Check 🧭
**chart: bar**

CSS bar chart showing sentiment signals if data available:
- Social sentiment, analyst ratings, fund flows

If insufficient data, fall back to prose.

### 6. What to Watch ⏳
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
