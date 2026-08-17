# 更新日志

版本线：v1.1 → v1.2 → v1.3 → v1.4 → **v1.5**

## v1.5 (2026-08-17)

### 新增功能

- **主题定制系统**：`theme.json` 一键切换 5 套预设主题（default-light / warm-cream / cool-slate / ink-blue / dark），支持自定义涨跌色、字体大小、斑马纹、卡片阴影
- **K线图渲染**：新增 `chart: kline`，OHLC 蜡烛图 + 5 日均线，覆盖美股 / 港股 / A股 / 通用四大市场
- **Playwright 渲染器**：弃用 wkhtmltopdf，完整支持现代 CSS / SVG / 背景纹理
- **AI 装饰元素**：接入 Seedream / DALL-E / Stability 图片 API 生成背景纹理
- **每日定时任务**：`theme.json` 的 `schedule` 配置 + `SCHEDULE.md` 说明
- **自动化测试**：`tests/` 提供配置 / 渲染 / 结构检查脚本

### 改进

- **排版一致性规范**：`SKILL.md` 与 `templates/us-stock.md` 固化标准版式，确保每日报告排版与往期一致
- 修正 README 颜色规范（红涨绿跌：涨 `#dc2626` / 跌 `#16a34a`）
- 新增本更新日志（CHANGELOG.md）
- 更新 `.gitignore`，排除 `output/` 与 `report_*.html` 等生成产物

## v1.4 (2026-07-23)

红涨绿跌配色 + CSS 页面优化 + 输出目录规则。

## v1.3 (2026-07-23)

K线图渲染 + 主题系统 + AI 装饰元素 + Playwright 渲染器。

## v1.2 (2026-07-23)

全面升级：9 板块报告 + 中文适配 + 知识体系。

## v1.1 (2026-07-23)

初始版本。
