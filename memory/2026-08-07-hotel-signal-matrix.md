# 酒店行业信源全景 · B166ER 信源矩阵 v1.0

> 生成日期：2026-08-07 08:21 GMT+8
> 已落地工具为底，**不包含**规划中 / 概念阶段。

## Layer 1 · 📰 舆情情报（Sentiment）
- **TrendRadar MCP** ✅ — 跨平台新闻聚合（10+ 平台）/情感分析/热点话题
- **RSS 订阅** ✅ — hacker-news / 36kr（Agent-Reach 内置）

## Layer 2 · 💰 价格数据（Price Data）
- **Booking Price Extractor** ✅ 生产就绪 — 28 房型/酒店验证通过（JPY/CNY/USD）
- **invisible_playwright** ✅ — 跨境 OTA（Bypass reCAPTCHA 0.9 vs Chromium 0.3-0.5）

## Layer 3 · 🔍 行业洞察（Insight）
- **Tavily** ✅ — AI 搜索 + 综合答案（1000/月）
- **web_search / web_fetch** ✅ — 通用网页（OpenClaw 内置）

## Layer 4 · 👥 社交与用户信号（Social Signal）
- **Agent-Reach** ✅ — 17 平台路由：V2EX / 雪球 / B 站 / RSS / Jina
- **Obscura** ✅ — 国内强反爬：携程 / 美团 / 小红书 / 飞猪
- **scrap_tools (Playwright)** — 复杂动态交互

## Layer 5 · 🤖 智能解析（AI Parsing）
- **Skyvern Vision LLM** ✅ — Planner-Actor-Validator 三智能体
- **Vision LLM（图片直读）** — 截图/海报直接 OCR

## Layer 6 · 📊 行业人才信号（Talent Signal）
- **career-ops wrapper** ✅ — 14 模式 / 9 阶段 Pipeline；offer 流动 = 行业温度计

---

## 不变量识别（V2.4 群论视域）
**什么在变**：具体酒店、价格、新闻话题、社交声音。
**什么不变**：信源矩阵的六层结构 —— **供需匹配 × 信任** 决定一切酒店价值。

## 当前覆盖盲点
- 携程/美团**实时价格**大规模抓取尚未跑通（Obscura 验证达 1 家级别）
- Booking 价格 GraphQL 化未做（仍是 DOM 选择器）
- 国内 OTA 评论反爬未系统化
- 雪球 / 慧博等**二级市场酒店股**信号未接入
