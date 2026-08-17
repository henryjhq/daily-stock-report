# 更新日志

本文件的版本号遵循「语义化版本」原则。重要说明：仓库此前存在一个误标为 `v2.0` 的版本，
经复核该次更新为向下兼容的功能增强，并非破坏性改动，不应跳到重大版本。故本版统一
**更名为 v1.5**，与 v1.0.0 共同构成 v1.x 版本线。此前误标的 `v2.0` / `v2.0.0` 标识已废弃。

---

## v1.5 (2026-08-17)

相对 v1.0.0 的一次功能增强。核心变化：**主题系统 + K线图 + Playwright 渲染**三件套，辅以 AI 装饰、定时任务、自动化测试。

### 新增功能

- **主题定制系统**
  - 新增 `theme.json` 配置文件，支持 5 套预设主题：default-light / warm-cream / cool-slate / ink-blue / dark。
  - 可自定义背景、表面、边框、文字、强调色、涨跌色、字体大小、表格斑马纹、卡片阴影。
  - 新增「主题颜色强制映射」规则：`gain`（涨）/ `loss`（跌）颜色全局生效，覆盖 CSS 类、柱状图、折线图、K线图、区域填充、Callout 边框。

- **K线图渲染（chart: kline）**
  - 新增 `chart: kline` 图表类型：OHLC 蜡烛图 + 5 日均线，覆盖美股 / 港股 / A股 / 通用四大市场模板。
  - 蜡烛颜色随主题涨跌色自动映射（红涨绿跌 / 绿涨红跌可切换）。

- **Playwright 渲染器**
  - 弃用 wkhtmltopdf（QtWebKit 2016 老引擎），改用 Playwright + Chromium。
  - 完整支持现代 CSS（flexbox）、SVG（polyline/polygon/rect）、背景纹理与背景混合模式，解决了旧引擎下图表渲染缺失的问题。

- **AI 装饰元素生成**
  - `theme.json` 新增 `imageApi` 配置，可接入 Seedream（火山引擎）/ DALL-E / Stability 等图片生成 API。
  - 自动生成报告背景纹理等装饰元素（无 API 时自动回退纯色背景）。

- **每日定时任务**
  - `theme.json` 新增 `schedule` 配置（`enabled` / `market` / `time` / `days`），支持按市场、时间、工作日自动生成日报。
  - 新增 `SCHEDULE.md` 说明文档。

- **自动化测试**
  - 新增 `tests/` 目录：`check_config.py`（配置检查）、`check_render.py`（渲染检查）、`check_report.py`（报告结构检查）、`run_all.sh`（一键运行）。

### 改进

- **排版一致性规范**：`templates/us-stock.md` 固化标准版式（metric-row 指标卡 + summary-box 卡片概览 + data-table 明细表 + K线图），并在 SKILL.md 中新增强制规则，生成前对齐往期报告，避免每日排版漂移。
- **颜色规范修正**：README 原「涨绿跌红」表述有误，现统一为「红涨绿跌」（涨 `#dc2626` / 跌 `#16a34a`），与 `theme.json` 一致。

### 其他

- 更新 `.gitignore`，忽略 `output/` 与 `report_*.html` 等生成产物。
- tracker 文件追加 2026-07 ~ 2026-08 期间的每日记录。

---

## v1.0.0 (2026-07)

初始版本。

- 8+1 板块完整日报（三大指数概览、纳斯达克深度分析、涨跌幅个股、五大维度归因、板块轮动、宏观环境、关注前瞻、知识点、自选股追踪）。
- 全中文界面，修复 wkhtmltopdf emoji 乱码。
- 每日金融 + 股市知识点，4 周轮换体系。
- 四大市场模板（美股 / 港股 / A股 / 通用）。

> 注：v1.0.0 发布后，仓库曾出现 `v2.0.0` 标签与提交信息，本次已统一更正为 v1.5 语义。
