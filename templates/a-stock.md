# A-Share Daily Report Template

## Report Header

```
# 🇨🇳 A-Share Market Daily Report — {{DATE}}
```

> **Data as of:** market close {{DATE}} · Sources: WebSearch
> **Indices:** 上证综指 · 深证成指 · 创业板指 · 科创50

---

## Sections

### 1. Index Snapshot 📊
**chart: table**

Shanghai Composite, Shenzhen Component, ChiNext, STAR 50 in a styled table.

Columns: 指数 | 收盘 | 涨跌 | 涨跌幅

One-line driver per index.

### 2. 指数近一月走势
**chart: kline** (fallback: chart: line)

四大指数（上证综指、深证成指、创业板指、科创50）过去约 15-20 个交易日的 OHLC K 线图，
叠加 5 日均线。每个指数独立 SVG 卡片（价格区间差异较大）。

K 线颜色：红涨绿跌（A 股习惯），或统一绿涨红跌。如 OHLC 数据不足，退化为折线图。

### 3. Market Microstructure 📈
**chart: flow**

Key microstructure data as a flow comparison chart:
- Combined turnover (RMB billions) vs 20-day average
- Northbound flow (北向资金): net inflow/outflow
- Limit-up / limit-down count (涨停/跌停家数)

### 4. Sector & Concept Rotation 🔄
**chart: bar**

CSS bar chart: top 5 Shenwan sectors (green) and bottom 5 (red).

Prose on leading/lagging sectors and hot concepts (AI, new energy, semiconductor, SOE reform).

### 5. Policy & Macro 📡
**chart: none**

China macro and policy signals (prose only):
- PBOC liquidity operations (OMO, MLF, LPR)
- Key policy announcements (State Council, CSRC, SASAC)
- RMB fixing and CNH/CNY movement
- 10Y CGB yield direction

### 6. What to Watch ⏳
**chart: none**

2-3 concrete events (prose only):
- Upcoming economic data (CPI, PPI, PMI, 社融)
- Key earnings from A-share companies
- Technical levels for Shanghai Composite
- Policy window events

---

## Tracker Entry Format

```
| {{YYYY-MM-DD}} | 上证 {{change%}} / 深证 {{change%}} | 北向 {{net Rmb B}} | {{5-word theme}} |
```
