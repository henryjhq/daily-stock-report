# US Stock Daily Report Template

## 排版一致性要求（每次生成前必读）

每天的报告排版必须与往期报告保持基本一致。生成 HTML 前，**先读取工作目录或
`output/` 目录下最近一份历史报告 HTML**（如 `美股日报_*.html` 或 `report_*.html`），
对齐其板块顺序与 HTML 结构。下方为 2026-08 系列报告的标准版式基准，后续报告严格沿用。

**标准页面骨架（自上而下顺序）：**

```
report-header（标题 + meta）
metric-row（四张指标卡：三大指数 + VIX）
pull-quote（一句话主题）
一、三大指数概览
二、指数近一月K线图
三、纳斯达克深度分析
四、涨跌幅最大个股
五、五大维度涨跌归因
六、板块轮动
七、宏观环境
八、今日关注前瞻
九、今日知识点
（十、自选股追踪，仅当 watchlist 有该市场条目）
report-footer
```

**颜色规则（与 theme.json 一致，红涨绿跌）：**
- 上涨 = `theme.gain`（默认 `#dc2626` 红），CSS 类 `.up`
- 下跌 = `theme.loss`（默认 `#16a34a` 绿），CSS 类 `.down`
- 阳线实体/影线用 gain 红，阴线实体/影线用 loss 绿

---

## Report Header

```html
<div class="report-header">
  <h1>美股市场日报</h1>
  <p class="meta">报告日期：{{GEN_DATE}} | 行情数据：{{DATA_DATE}} 收盘 | 数据来源：网络实时搜索</p>
</div>
```

标题固定为「美股市场日报」，日期只写进 meta，不写进 h1。

## KEY METRICS ROW（标题后、pull-quote 前）

四张并排指标卡（`.metric-row` + `.metric-card`），顺序：S&P 500 / NASDAQ / 道琼斯 / VIX。
每张卡含：`metric-value`（收盘点位）+ `metric-label`（名称）+ `metric-label`（涨跌点与涨跌幅，套 `.up`/`.down`）。

```html
<div class="metric-row">
  <div class="metric-card">
    <div class="metric-value">7,785.76</div>
    <div class="metric-label">S&P 500</div>
    <div class="metric-label"><span class="down">-13.23 (-0.17%)</span></div>
  </div>
  <!-- NASDAQ / 道琼斯 / VIX 同理 -->
</div>
```

## PULL QUOTE（一句话主题）

```html
<div class="pull-quote">一句话概括当日市场主线（涨跌原因 + 领涨方向）。</div>
```

---

## Sections

### 1. 三大指数概览
**chart: table**

按顺序包含四层结构（缺一不可）：

1. **导语段** `<p>`：当日大盘定调，用 `<span class="focus-number">关键词</span>` 高亮核心事件。
2. **summary-box 卡片概览**：三列并排，每列含 `slabel`（指数名）+ `svalue`（收盘点位）+ `schange`（涨跌幅，套 `.up`/`.down`）+ 一行副标题 `slabel`（如「创新高后小幅回吐」）。
3. **data-table 明细表**：5 列 `指数 | 收盘点位 | 涨跌点 | 涨跌幅 | 驱动因素`，指数名套 `<strong>`，涨跌点/涨跌幅套 `.up`/`.down`。
4. **note 段**：周度表现补充 + 板块涨跌家数等补充信息。

```html
<h2>一、三大指数概览</h2>
<p>…定调描述，<span class="focus-number">关键词</span>…</p>
<div class="summary-box"><table class="summary-table"><tr>
  <td><div class="slabel">S&P 500</div><div class="svalue">7,785.76</div><div class="schange down">-0.17%</div><div class="slabel">创新高后小幅回吐</div></td>
  <td>…纳斯达克…</td>
  <td>…道琼斯…</td>
</tr></table></div>
<table class="data-table striped">
  <tr><th>指数</th><th>收盘点位</th><th>涨跌点</th><th>涨跌幅</th><th>驱动因素</th></tr>
  <tr><td><strong>S&P 500</strong></td><td>7,785.76</td><td class="down">-13.23</td><td class="down">-0.17%</td><td>驱动因素一句话</td></tr>
  <!-- 纳斯达克 / 道琼斯 同理 -->
</table>
<p class="note">* 周度表现补充…</p>
```

指数顺序统一为：S&P 500 → 纳斯达克 → 道琼斯。

### 2. 指数近一月K线图
**chart: kline**（首选；仅当 OHLC 完全不可得时才退化为 chart: line）

三大指数各自一张 K 线卡片（`.kline-charts-grid` + `.kline-chart-card`），15-20 个交易日 OHLC 蜡烛图。

- 卡片顺序与概览一致：S&P 500 → 纳斯达克 → 道琼斯。
- 每张卡 subtitle 格式：`{{起始日}} - {{结束日}} · N个交易日 · 开盘 X · 收盘 Y · 涨/跌 Z%`（涨跌套 `.up`/`.down`，Z% 为区间涨跌幅 = 首开 vs 末收）。
- 蜡烛颜色：阳线（收盘≥开盘）用 gain 红，阴线用 loss 绿；影线同色。
- 末尾 `note`：`* K线图中，红实体为收盘高于开盘（阳线），绿实体为收盘低于开盘（阴线），影线为当日最高最低价。部分交易日数据为估算值。`

```html
<h2>二、指数近一月K线图</h2>
<div class="kline-section"><div class="kline-charts-grid">
  <div class="kline-chart-card">
    <div class="chart-title">S&P 500 指数</div>
    <div class="chart-subtitle">07/18 - 08/14 · 20个交易日 · 开盘 7,723 · 收盘 7,786 · <span class="up">涨 +0.8%</span></div>
    <svg viewBox="0 0 580 210" style="width:100%; height:auto; display:block;">…蜡烛…</svg>
  </div>
  <!-- 纳斯达克 / 道琼斯 同理 -->
</div></div>
<p class="note">* K线图中，红实体…（红涨绿跌注释）</p>
```

### 3. 纳斯达克深度分析
**chart: none**

四段纯文字，每段 `<p><strong>小标题：</strong>…</p>`：
**走势分析 / 板块贡献 / 明星个股 / 市场情绪**。

### 4. 涨跌幅最大个股
**chart: table**

单表 5 只混合（涨的在前、跌的在后，约 3 涨 2 跌），代码加粗 + 中文名。
列：`代码 | 最新价 | 涨跌幅 | 涨跌原因`。涨跌幅套 `.up`/`.down`。末尾 `note` 说明。

```html
<table class="data-table striped">
  <tr><th>代码</th><th>最新价</th><th>涨跌幅</th><th>涨跌原因</th></tr>
  <tr><td><strong>RDDT</strong> Reddit</td><td>—</td><td class="up">+12.60%</td><td>获纳入标普 500 指数</td></tr>
  <!-- 其余 4 只 -->
</table>
<p class="note">* 个股最新价随盘中实时波动，此处聚焦当日涨跌幅与驱动因素。</p>
```

### 5. 五大维度涨跌归因
**chart: table**

列：`维度 | 今日判断 | 依据`。**「今日判断」列必须按语义着色**：
- 利好 / 乐观 / 偏多 / 改善 / 净流入 → `.up`（红）
- 利空 / 恐慌 / 偏空 / 恶化 / 净流出 → `.down`（绿）
- 中性 / 平衡 / 平稳 / 震荡 → 默认无颜色

### 6. 板块轮动
**chart: bar**

结构：**导语段 `<p>`**（板块涨跌家数 + 轮动主线）→ `.bar-section`（领涨 5 个 + 领跌 5 个柱）→ **轮动逻辑段**（资金流向 + 事件驱动）。
柱宽公式 `width = abs(change%) / max_abs_change% * 100`，领涨柱套 `.bar-fill up`，领跌柱套 `.bar-fill down`。

### 7. 宏观环境
**chart: none**

`<ul>` 列表，固定 6 项：国债收益率 / 美元指数 DXY / VIX / 美联储动态 / 经济数据 / 地缘政治。

### 8. 今日关注前瞻
**chart: none**

`<ul>` 列表 4-5 项：经济数据 / 财报 / 政策事件 / 关键技术位 / 地缘进展。

### 9. 今日知识点
**chart: none**

两个 `.knowledge-card`，各含 `<h4>` 标题 + `<p>` 正文：
- **金融知识 #N**：延续 knowledge-tracker 编号。
- **股市知识 #N**：延续 knowledge-tracker 编号，尽量与当日盘面关联。

### 10. 自选股追踪（如有）
**chart: table**

仅当 `watchlist.md` 该市场下有未注释条目时生成。列：`代码 | 最新价 | 当日涨跌 | 近期关键事件`。

---

## Report Footer

```html
<div class="report-footer">本报告由 AI 自动生成，数据来源于公开市场信息，仅供学习参考，不构成任何投资建议。</div>
```

---

## Tracker Entry Format

```
| {{YYYY-MM-DD}} | S&P 500 {{change%}} | {{top mover ticker}} {{%}} | {{5-word theme}} |
```

## Knowledge Tracker Entry Format

```
| {{YYYY-MM-DD}} | 金融: {{topic}} (#{{N}}) | 股市: {{topic}} (#{{M}}) |
```

知识领域轮换表（每 4 周一个循环）：

| 周次 | 金融知识方向 | 股市知识方向 |
|---|---|---|
| 第 1 周 | 宏观经济指标 (CPI/PCE/GDP/PMI) | 大盘分析基础 (指数/成交量/技术位) |
| 第 2 周 | 货币政策工具 (利率/准备金/公开市场操作) | 板块轮动 (行业分类/轮动规律/产业链) |
| 第 3 周 | 固定收益 (国债/企业债/收益率曲线) | 个股分析 (财报/估值/技术指标) |
| 第 4 周 | 衍生品 (期货/期权/波动率) | 资金面 (北向/融资融券/机构持仓) |
