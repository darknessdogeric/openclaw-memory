# 地区级市场分析 SOP v1.0

> **适用任务**：分析某个地区（城市/州/省）酒店/民宿市场环境
> **第一例**：云南红河州弥勒市（2026-07-23）
> **编订**：B166ER | 2026-07-23

---

## 启动检查清单

接收到任务后，先填这个清单再开干：

```markdown
## 任务定义
- 目标地区：[如 弥勒市 / 大理 / 西双版纳 / 莫干山]
- 任务类型：[地区全景 / 项目可行性 / 单店深度]
- 风险偏好：[稳 / 积极 / 极稳]（默认稳）
- 客群视角：[投资者 / 政府 / 业主本人 / 战略顾问]
- 交付要求：[PDF / Word / Markdown / PPT]

## 信源审计
- 必查 34 维度（参见 data-source-34-dimensions.md）
- 当地融媒体/政府公报
- 当地民宿/酒店协会

## 期望产出
- [PDF 报告 + Markdown 源 + 图表 PNG]
```

---

## 5 步标准流程

### Step 1：信源审计（强制）

```bash
# 工具调用
python scripts/audit_34_dimensions.py --region "弥勒" --output "audit.md"
```

**审计标准**：
- 覆盖率 ≥70% 才能继续
- 缺失的关键信源必须在 Step 2 补救

**审计产出**（示例）：
```
A 类：3/5 已用（60%）
B 类：0/6 ⚠ 必须补足
C 类：1/5（20%）
D 类：2/6（33%）
E 类：5/5（100%）✅
F 类：0/3
G 类：0/4
─────────────────
总计：11/34 = 32% ⚠ 待补
必须补足：STR/浩华/JLL/Fastdata/迈点
```

---

### Step 2：数据采集（并行）

**并行抓取清单**：

| 优先级 | 数据类型 | 工具 |
|--------|---------|------|
| 🥇 | STR 全国酒店业绩 | web_search + 行业报告 |
| 🥇 | 浩华景气指数 | web_search |
| 🥇 | 上市公司财报 | web_search |
| 🥇 | 迈点/京东/Fastdata 行业报告 | web_fetch |
| 🥇 | OTA 实测价格 | scrapling / scrape_matrix |
| 🥇 | 当地政府公报 | web_search |
| 🥇 | 项目方访谈 | 直接对话 |
| 🥈 | 财经媒体报道 | web_search + 微博/搜狐 |
| 🥈 | 法规/政策文件 | 文库 + 各省政府网 |
| 🥉 | 学术论文 | 知网 + Google Scholar |

**输出**：`reports/<地区>_raw_data.json`（结构化数据）

---

### Step 3：报告框架填充（按 schema）

按 10 章+5 维结构填充：

```markdown
## Part 1: 宏观全景（10 章）
- Ch 1 行业总览（基于 STR/浩华）
- Ch 2 宏观环境（基于 PEST）
- Ch 3 行业供给（基于集团财报 + OTA 数据）
- Ch 4 行业需求（基于消费端报告）
- Ch 5 运营表现（基于 ADR/OCC 推算）
- Ch 6 竞争格局（基于标杆案例）
- Ch 7 营销渠道（基于 OTA 抓取）
- Ch 8 AI+PMS（基于行业 KB）
- Ch 9 资本市场（基于 JLL/CBRE）
- Ch 10 政策（基于政府文件）

## Part 2: 项目可行性（第 11 章）
- 5 维可行性矩阵
- 财务模型
- 三档决策
- 投资必查清单
```

**每个章节必须包含**：导入段 + 3-5 个数据点 + 对比表/图 + 关键判断 + 下章过渡

---

### Step 4：图表 + PDF 生成（一键）

```bash
# Step 4a: 生成图表（9 张标准）
python scripts/gen_charts.py --data "reports/<地区>_raw_data.json" --output "reports/<地区>/charts/"

# Step 4b: 生成 PDF
python scripts/build_pdf.py --markdown "reports/<地区>_report.md" --charts "reports/<地区>/charts/" --output "reports/<地区>_report.pdf"
```

**图表 9 张**：
1. 上市公司核心指标对比
2. 外资/区域 RevPAR 变化
3. 民宿/旅居行业增长
4. 旅居康养爆发
5. 5 维对标雷达
6. 财务模型三档
7. 客群结构饼图
8. 5 维可行性矩阵
9. 政策时间线

**PDF 配置**：reportlab + 中文字体 + 10 章 + 5 维可行性 + 执行摘要（DeepSeek 生成）

---

### Step 5：质量校验（强制）

```bash
python scripts/quality_check.py --report "reports/<地区>_report.pdf"
```

**7 项必查**（详见 quality-checklist.md）：
1. ✅ 34 维度覆盖率 ≥70%
2. ✅ 10 章宏观 + 5 维可行性完整
3. ✅ OCC/ADR/RevPAR 推算有 Eric ADR 估算方法支撑
4. ✅ 政策合规（办证流程 + 土地红线）
5. ✅ 财务模型 3 档场景 + 修正路径
6. ✅ 图表 ≥6 张 + PDF 完整
7. ✅ 数据来源可追溯（≥8 类权威信源）

**任何 1 项不达标 = 返回修改**

---

## 工具调用链

```python
# 1. 信源审计
audit_34_dimensions(region_name)

# 2. 数据采集
fetch_data([
    sources=['STR', '浩华', '迈点', 'Fastdata', 'JLL', ...],
    region=region_name,
    output=f"{region_name}_raw_data.json"
])

# 3. 报告填充（模板）
fill_schema(
    raw_data=...,
    schema="methodology/schema.md",
    output=f"{region_name}_report.md"
)

# 4. 图表 + PDF
gen_charts(raw_data, charts_dir)
build_pdf(markdown, charts_dir, output_pdf)

# 5. 质量校验
quality_check(pdf_path)
```

---

## 实战应用：弥勒案例

```bash
# Step 1: 审计
python scripts/audit_34_dimensions.py --region "弥勒"
# 输出：覆盖率 15% → 必须补足

# Step 2: 抓取
python scripts/fetch_data.py --region "弥勒" --targets STR,浩华,JLL,Fastdata,迈点
# 输出：reports/mile_raw_data.json

# Step 3: 填充（10 章+5 维）
python scripts/fill_schema.py --data reports/mile_raw_data.json --output reports/mile_report.md

# Step 4: 图表+PDF
python scripts/gen_charts.py --data reports/mile_raw_data.json
python scripts/build_pdf.py --markdown reports/mile_report.md --output 弥勒民宿可行性研究报告.pdf

# Step 5: 自检
python scripts/quality_check.py 弥勒民宿可行性研究报告.pdf
# ✅ 7/7 全部达标 → 发布
```

---

## 预期效果

| 指标 | v1-v4 手动 | 方法论 + SOP 后 |
|------|---------|---------------|
| 时间 | 4-6 小时 | **1-2 小时** |
| 质量 | 不可复现 | **7 项校验保证** |
| 复用度 | 0 | **100%（下次直接套）** |
| 学习成本 | 每次重新学 | **0（流程已固化）** |

---

## 下一步行动

1. ⏳ 创建 `sop-single-store-analysis.md`（单店深度）
2. ⏳ 创建 `decision-tree.md`（什么时候选哪条路径）
3. ⏳ 创建 `quality-checklist.md`
4. ⏳ 创建 `scripts/audit_34_dimensions.py`
5. ⏳ 创建 `scripts/gen_market_analysis.py`（一键生成报告）