---
name: hotel-feasibility-report
description: 酒店/民宿投资可行性研究报告方法论与工具链：地区级→单店逐层下钻（10 章 5 维结构），依据弥勒 v1-v4 与 PDF 实战经验。触发：酒店投资可行性、民宿可研、物业可研报告、改造投资测算。
---

# 酒店/民宿投资可行性研究报告 - Skill

> **版本**: v1.0
> **创建**: 2026-07-23
> **作者**: B166ER
> **依据**: 弥勒 v1-v4 + PDF 实战经验
> **状态**: Active

## Overview

本 skill 提供**酒店/民宿投资可行性研究报告**的完整方法论和工具链。覆盖：
- **地区级分析**（如：云南红河州弥勒市）
- **单店深度分析**（如：某具体物业可行性）
- **宏观→项目逐层下钻**（10 章+5 维结构）

**核心价值**：
- ✅ 把 4-6 小时手工任务压缩到 1-2 小时
- ✅ 强制 34 维度信源审计，告别"信息覆盖不全"
- ✅ 强制 10 章+5 维标准结构，告别"v3 缺宏观"式结构性错误
- ✅ 一键生成 9 张图表 + PDF（合并交付）
- ✅ 7 项质量校验，保证每份报告都达标

## When to Use

当用户提出以下请求时使用：
- 分析某地区/城市的酒店或民宿市场环境
- 给具体物业做投资可行性研究
- 对比多个地区的酒店投资机会
- 输出 PDF 格式的市场报告
- 任何"酒店/民宿投资"相关深度分析

## Features

### 报告结构（10 章 + 5 维）
1. **行业总览**（Executive Summary + 4 数据点 + 1 警示）
2. **宏观环境**（PEST：经济/政策/社会/技术）
3. **行业供给**（全国 + 区域 + 民宿）
4. **行业需求**（消费端 + 旅居 + 民宿细分）
5. **运营表现**（OCC/ADR/RevPAR + 同梯次对标）
6. **竞争格局**（外资 + 内资 + 标杆案例）
7. **营销与渠道**（OTA + 短视频 + 私域）
8. **AI + PMS + 收益管理**
9. **资本市场**（JLL / 投融资 / 退出）
10. **政策与法规**（办证 + 土地 + 创业担保）
11. **项目可行性**（5 维矩阵 + 财务模型 + 三档决策）

### 工具链
- `gen_market_analysis.py`（一键生成地区报告）
- `gen_single_store.py`（一键生成单店报告，待开发）
- `gen_charts.py`（生成 9 张标准图表）
- `build_pdf.py`（PDF 构建）
- `call_deepseek.py`（DeepSeek API 封装）
- `quality_check.py`（7 项校验）

### 34 维度信源强制审计
A 行业协会 5 + B 国际研究 6 + C 国内研究 5 + D OTA 6 + E 官方统计 5 + F 学术智库 3 + G 财经媒体 4 = 34 个

## Usage

### Quick Start

```bash
# 一键生成地区报告
python scripts/gen_market_analysis.py --region "弥勒" --preference "稳"

# 7 项质量校验
python scripts/quality_check.py --pdf "reports/弥勒民宿可行性研究报告.pdf"
```

### 输出文件

每个项目交付：
```
reports/
├── {region}_feasibility_report.pdf   ← 主交付（PDF）
├── {region}_feasibility_report.md    ← Markdown 源
├── {region}_deepseek_summary.txt     ← AI 生成摘要
├── {region}_raw_data.json            ← 原始数据
├── charts/                            ← 9 张图表 PNG
│   ├── 01_2024_groups_compare.png
│   ├── ...
│   └── 09_policy_timeline.png
└── quality_check_report.txt            ← 7 项校验结果
```

## SOPs

### 地区级 SOP（5 步）
1. **信源审计** → 34 维度覆盖率 ≥70%
2. **数据采集** → 并行抓取
3. **报告填充** → 按 10 章+5 维结构
4. **图表+PDF** → 一键生成
5. **质量校验** → 7 项必查

### 单店级 SOP（6 步）
1. **物业尽职调查**（权属/物理/政策/工程）
2. **投资测算**（财务模型 + 3 档场景）
3. **客群与产品定位**
4. **运营手册**（组织/SOP/营销/收益）
5. **合规+融资**（办证 + 创业担保）
6. **退出+风险预案**

详见：
- `methodology/sop-region-analysis.md`
- `methodology/sop-single-store-analysis.md`

## Required Tools

### 必备工具
- **STR 数据访问**（行业基准）
- **浩华景气指数**（季度报告）
- **DeepSeek API**（执行摘要生成）
- **Python 3.14** + matplotlib + reportlab
- **OTA 抓取工具**（scrapling/scrape_matrix）

### 推荐工具
- **仲量联行 JLL**（资本市场报告）
- **Fastdata 极数**（民宿行业报告）
- **迈点研究院**（区域投资报告）

## Quality Standards

### 7 项必查
1. ✅ 34 维度信源覆盖率 ≥70%
2. ✅ 10 章宏观 + 5 维可行性完整
3. ✅ OCC/ADR/RevPAR 推算有 Eric ADR 估算方法支撑
4. ✅ 政策合规（办证流程 + 土地红线）
5. ✅ 财务模型 3 档场景 + 修正路径
6. ✅ 图表 ≥6 张 + PDF 完整
7. ✅ 数据来源可追溯（≥8 类权威信源）

**任何 1 项不达标 = 不准交付**

## Files

```
skills/hotel-feasibility-report/
├── SKILL.md                          # 本文件
├── references/
│   ├── schema.md                     # 10 章+5 维结构
│   ├── sop-region.md                 # 地区级 SOP
│   ├── sop-single-store.md           # 单店级 SOP
│   ├── data-source-34-dimensions.md  # 34 维度信源规范
│   ├── decision-tree.md              # 决策树
│   └── quality-checklist.md          # 7 项质量校验
├── scripts/
│   ├── gen_market_analysis.py        # 一键地区报告生成
│   ├── gen_single_store.py           # 一键单店报告生成（待开发）
│   ├── gen_charts.py                 # 图表生成
│   ├── build_pdf.py                  # PDF 构建
│   ├── call_deepseek.py              # DeepSeek 封装
│   └── quality_check.py              # 7 项校验
├── assets/
│   └── template.pdf                  # 标准 PDF 模板
└── examples/
    └── 弥勒民宿可行性研究报告.pdf   # 第一例
```

## Examples

### 第一例：弥勒 v4
**输入**：
- 地区：云南红河州弥勒市
- 类型：综合可行性研究报告
- 风险偏好：稳
- 时间：2026-07-23

**输出**：
- PDF 报告（1.4 MB，22 页）
- 9 张图表
- 5 维可行性矩阵（市场 8.5 / 政策 7.5 / 财务 6.5 / 运营 6.5 / 退出 5.5）
- 三档决策建议：极稳/稳/积极
- 7/7 质量校验通过

**关键结论**：
- 有条件可行（5 约束满足时）
- 推荐：280 万投资湖泉周边 12 间中端精品
- 修正后 5-6 年回收

## Roadmap

### Phase 1（当前）
- [x] 地区级 SOP + 工具链
- [x] 弥勒案例验证
- [x] PDF 报告生成
- [x] 7 项质量校验

### Phase 2（2 周内）
- [ ] 单店级 SOP 完整开发
- [ ] gen_single_store.py 工具
- [ ] 多区域对比 SOP
- [ ] 历史案例库（A 股年报、并购案例）

### Phase 3（1 月内）
- [ ] 跨地区对比模板
- [ ] 风险概率模型（基于 STR 月报）
- [ ] AI Agent 自治分析
- [ ] 自动更新数据源（如 STR 月报）

### Phase 4（长期）
- [ ] 实时数据接入
- [ ] AI 投资决策建议
- [ ] 完整行业 SaaS 平台

## License

MIT License - 见 LICENSE 文件

## Acknowledgments

本 skill 借鉴：
- **迈点研究院**标准报告结构
- **STR China** OCC/ADR/RevPAR 基准
- **浩华 Horwath HTL** 行业景气指数
- **仲量联行 JLL** 资本市场框架
- **Fastdata 极数**民宿行业报告
- **Eric** 34 维度信源规范 + ADR 估算方法

## Contact

- B166ER（自动化 + 行业研究 Agent）
- Eric（项目总控 / 战略方向）
