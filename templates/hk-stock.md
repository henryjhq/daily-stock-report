# HK Stock Daily Report Template

## Report Header

```
# 🇭🇰 Hong Kong Stock Market Daily Report — {{DATE}}
```

> **Data as of:** market close {{DATE}} · Sources: WebSearch
> **Indices:** Hang Seng Index (HSI) · Hang Seng TECH Index · China Enterprises Index (HSCEI)

---

## Sections

### 1. Index Snapshot 📊
**chart: table**

HSI, HSTECH, HSCEI in a styled table with red/green color coding.

Columns: Index | Close | Change | % Change

One-line driver per index.

### 2. 指数近一月走势
**chart: kline** (fallback: chart: line)

三大指数（恒生指数、恒生科技、国企指数）过去约 15-20 个交易日的 OHLC K 线图，
叠加 5 日均线。每个指数独立 SVG 卡片（价格区间差异较大，不适合叠加）。

K 线颜色：绿涨红跌。如 OHLC 数据不足，退化为折线图。

### 3. Connect Flows 🔗
**chart: flow**

Southbound (mainland → HK) and Northbound (HK → mainland) net flows as a CSS bar chart.
Green bars for inflow, red for outflow. RMB billions.

1-2 sentences on what the flow direction signals.

### 4. Top Movers 🚀
**chart: table**

3-5 HK-listed names that moved the most. Mix of TECH (9988, 0700, 9618, 3690) and traditional names.

Columns: Code | Name | Change % | Reason

### 5. Sector & Theme 🧭
**chart: bar**

Key themes driving HK markets as a CSS bar chart (sector performance):
- Tech, property, financials, consumer, energy

Prose on: China policy signals, property sector updates, tech regulation, CNH/USD impact.

### 6. What to Watch ⏳
**chart: none**

2-3 concrete events for the next trading day (prose only):
- China economic data (CPI, PMI, trade data)
- Key earnings from HK-listed companies
- HSI technical levels
- US market overnight impact (ADR performance)

---

## Tracker Entry Format

```
| {{YYYY-MM-DD}} | HSI {{change%}} / HSTECH {{change%}} | Southbound {{net Rmb B}} | {{5-word theme}} |
```
