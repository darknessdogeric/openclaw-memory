# 2026-07-21 信源矩阵 · Eric 核心指令

## Eric 原话（23:25）

> "更新 V5。是否做抓取模版，你自己决定。另外，这些信源是给你的，不光是 AHL。你自己本身需要具备这些信源全维度"

## 关键解读

1. **信源 = B166ER 基础设施**：不只是 AHL 项目，是 Eric 的 AI 助理本身需要具备的能力
2. **28 信源**（v6 海报）：覆盖酒店行业全维度
3. **Eric 信任**："是否做抓取模版你自己决定"——我决定做（hotel_sources.py）

## 28 信源完整列表（按类型）

### Tier 1: 国际权威 + 行业第一协会（2）
- STR Global
- 中国旅游饭店业协会（CTHA）

### Tier 2: 国内全样本 + 官方数据（3）
- 酒店之家
- 国家统计局（NBS）
- 文化和旅游部（MoCT）

### Tier 3: 协会权威（6）
- 中国饭店协会（CHA）
- 中国旅游研究院（CTA）★ 文旅部直属
- 中国连锁经营协会（CCFA）
- 中国烹饪协会（CCA）
- 世界中餐业联合会（WCF）

### Tier 4: 权威咨询（6）
- 浩华管理顾问（Horwath HTL）★ 1985 入华
- 厚海数据（浩华旗下）
- PwC 普华永道
- Deloitte 德勤
- EY 安永
- KPMG 毕马威

### Tier 5: 头部财报（20）
内资：华住、锦江、亚朵、首旅、君亭、东呈、格林、尚美、岭南、开元
外资：万豪、希尔顿、洲际、凯悦、温德姆、雅高、香格里拉、四季、悦榕、雅诗阁

### Tier 6: 券商研报（6）
中金、中信、光大、东方、招商、财通

### Tier 7: 代理行（6）
仲量联行（JLL）、戴德梁行、第一太平（Savills）、世邦魏理（CBRE）、高力（Colliers）、莱坊（Knight Frank）

### Tier 8: 交通部（2）
民航局（CAAC）、国铁集团（CRC）

### Tier 9: OTA 平台（7）
携程、美团、去哪儿、飞猪、同程、途家、木鸟

### Tier 10: 转让数据（1）
指点网

### Tier 11: 行业研究（4）
浩华景气指数、迈点研究院、品橙旅游、北二外

### Tier 12: 用户调研（1）
腾讯智慧文旅

## 信源使用方法（self-improving 必读）

1. **Eric 问酒店行业问题** → 自动调用 hotel_sources.py
2. **AHL 项目需要数据** → 用 HotelSourceCrawler
3. **每月底自动检查**：是否有新报告 → 更新 memory
4. **不可遗漏的 6 个核心信源**：
   - STR Global（T1 国际权威）
   - 酒店之家（T2 国内全样本）
   - 中国旅游研究院（CTA，文旅部直属）
   - 浩华管理顾问（1985 入华，行业老牌）
   - 厚海数据（浩华旗下，数据平台）
   - JLL 仲量联行（投资交易权威）

## 相关文件

- `/workspace/toolbox/hotel_sources.py` — 28 信源 wrapper（CLI + Python API）
- `/workspace/toolbox/industry_chart_v6/cycle_forecast_v6.html` — v6 海报（28 信源）
- `/workspace/toolbox/industry_chart_v6/watermarked.png` — v6 海报渲染图

## 行动触发

每当以下情况，应自动调取信源：
- Eric 提到 "酒店" + "数据" + 任何时间相关词
- AHL 项目需要新数据
- 月底/季底/年底报告日
- 用户问


---

# ⚠️ 概念更新（2026-08-02 Eric 纠正）

本文档的"28 信源"概念已**过时**。

## 真实信源矩阵（2026-08-02 盘点）

| 子系统 | 来源 | 数量 |
|---|---|---|
| 酒店行业 28 信源 | `toolbox/hotel_sources.py` | 28（核心子集） |
| TrendRadar RSS | `trendradar/config/config.yaml` | 40 配置 / **31 启用** |
| TrendRadar 平台热搜 | 同上 | **11 平台** |
| 趋势关键词库 | `trendradar/config/frequency_words.txt` | **~1355 关键词** |
| **合计主动信源** | | **~103 个** |

**Eric 估的 68-81 ≈ 实际 103**（扩展后含国际 + 平台 + 关键词四维）。

## 4 大覆盖领域（frequency_words.txt 标注）

1. **酒店/旅游**：国内 + 国外关键词全覆盖
2. **宏观/金融**：Fed / ECB / FOMC / Treasury / 货币 / 大宗商品
3. **AI/科技**：AGI / Foundation Model / 芯片 / 政策 / 估值 / 投资
4. **地缘/世界局势**：大国博弈 / 半导体 / 能源 / 货币 / 制裁 / 区域冲突

## 行动

- 详见 `memory/2026-08-02-source-matrix-expansion.md`
- 已更新 `toolbox/hotel_sources.py` line 36（标注"广义矩阵子集"）
- 本文档保留为"v6 海报基线"，新矩阵以 2026-08-02 文件为准
