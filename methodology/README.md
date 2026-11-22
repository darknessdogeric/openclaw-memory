# 酒店/民宿投资可行性研究 · 方法论体系 v1.0

> **目的**：把"地区/单店市场环境分析 + 策略措施"的每次重复任务，固化为可复用 SOP
> **第一例**：云南红河州弥勒市（2026-07-23）
> **编订**：B166ER | 2026-07-23
> **服务对象**：Eric + 未来所有类似任务

---

## 一、为什么需要方法论体系

每次任务我们都走过这条路径：
```
v1 全景报告 → v2 深度全景 → v3 项目可行性（缺宏观）→ v4 完整版 → PDF
```

**核心教训**（5 个）：
1. ❌ **第一版永远残缺**——缺宏观/缺可行性/缺图表/缺信源
2. ❌ **每次都重新走一遍教训**——浪费 30-50% 时间
3. ❌ **方法论未固化**——下次同类任务还是从零开始
4. ❌ **工具零散**——DeepSeek 调用/图表生成/PDF 构建各管一段
5. ❌ **质量不可复现**——同样问题，下一个人做出来的可能不一样

**目标**：把这 5 个教训转化为 **5 个固化机制**。

---

## 二、方法论体系核心结构

```
methodology/
├── README.md                                  ← 本文件（体系总览）
├── data-source-34-dimensions.md              ← 34 维度信源规范
├── schema.md                                  ← 报告结构框架（10 章 + 5 维）
├── sop-region-analysis.md                     ← 地区分析 SOP（弥勒/大理/西双版纳 等）
├── sop-single-store-analysis.md               ← 单店深度 SOP（一家酒店可行性）
├── decision-tree.md                           ← 决策树（什么时候选哪条路径）
├── output-templates/                          ← 输出模板
│   ├── region-report.md                      
│   ├── single-store-report.md                
│   └── decision-matrix.md                    ← 5 维评分表
└── quality-checklist.md                       ← 质量校验清单
```

```
scripts/                                        ← 工具链
├── gen_market_analysis.py                     ← 一键生成地区报告
├── gen_single_store.py                        ← 一键生成单店报告
├── gen_charts.py                              ← 图表生成（已存在）
├── build_pdf.py                               ← PDF 构建（已存在）
└── call_deepseek.py                           ← DeepSeek 调用封装
```

```
skills/hotel-feasibility-report/               ← 完整 Skill 封装
├── SKILL.md                                   ← Skill 主入口
├── references/
│   ├── schema.md                              
│   ├── sop-region.md
│   ├── sop-single-store.md
│   └── 34-dimensions.md
├── scripts/                                   ← 上述 scripts 的子集
└── assets/
    └── template.pdf                           
```

---

## 三、5 个固化机制（对应 5 个教训）

### 机制 1：34 维度信源强制审计

**目的**：杜绝"用了 30% 信源就以为覆盖了"（v1 的教训）

**实现**：
- `data-source-34-dimensions.md` 列出全部 34 个权威信源
- 每个报告 v1/v2/v3 必须对照审计
- 输出覆盖率（%）+ 缺失清单
- **审计未达 70% 不准发报告**

### 机制 2：报告标准结构（10 章 + 5 维）

**目的**：杜绝"v3 缺宏观"这种结构性缺失

**实现**：
- `schema.md` 强制 10 章宏观全景 + 5 维可行性矩阵
- 每个章节有固定模板（如"行业总览"必须有 4 个数据点 + 1 个警示）
- **缺任何章节 = 报告未完成**

### 机制 3：SOP 流程（输入-处理-输出）

**目的**：让任意"小助手"接手都能跑通流程

**实现**：
- `sop-region-analysis.md`：地区分析 SOP（5 步）
  1. 数据采集（信源 + 工具）
  2. 结构填充（10 章）
  3. 可行性矩阵（5 维）
  4. 风险/机会清单
  5. 决策建议 + 交付
- `sop-single-store-analysis.md`：单店深度 SOP（6 步）

### 机制 4：工具链自动化

**目的**：用代码代替手工（30 分钟任务 → 3 分钟）

**实现**：
- `gen_market_analysis.py`：输入地区名 → 输出 Markdown 报告骨架
- `gen_charts.py`（已存在）：输入数据 → 输出 9 张图表
- `build_pdf.py`（已存在）：输入内容 + 图表 → 输出 PDF
- `call_deepseek.py`：执行摘要智能生成

### 机制 5：质量校验

**目的**：确保输出可复现、达到一定标准

**实现**：
- `quality-checklist.md` 包含 7 项必查：
  1. 34 维度信源覆盖率 ≥70%
  2. 10 章宏观全景 + 5 维可行性矩阵完整
  3. OCC/ADR/RevPAR 推算有 Eric ADR 估算方法支撑
  4. 政策合规（办证流程 + 土地红线）
  5. 财务模型有 3 档场景 + 修正路径
  6. 图表 ≥6 张 + PDF 完整
  7. 数据来源可追溯（≥8 类权威信源）
- **任何 1 项不达标 = 不准发给 Eric**

---

## 四、从弥勒案例看方法论的诞生（演进路径）

| 版本 | 教训 | 启发的方法论要素 |
|------|------|----------------|
| **v1 全景** | 18 次搜索但没用知识库/图表 | **知识库优先 + 工具链** |
| **v2 深度** | 用了 5 份知识库但缺专业信源 | **34 维度审计机制** |
| **v3 可行性** | 跳过宏观直达项目级 | **10 章+5 维结构强制** |
| **v4 完整** | 终于结构对了，但需 4 小时 | **SOP + 工具链自动化** |
| **PDF** | 用户还要图表 | **图表+PDF一体化模板** |

**核心方法论升级**：v1-v4 不是"版本号"，而是 **5 个独立但互补的方法论要素**。

---

## 五、未来同类任务的标准路径

```
Step 1: 接收任务（如"分析西双版纳酒店市场"）
    ↓
Step 2: 调取 methodology/README.md（本次任务）
    ↓
Step 3: 执行 data-source-34-dimensions.md 信源审计
    ↓
Step 4: 按 sop-region-analysis.md 跑流程
    ↓
Step 5: 用 schema.md 填 10 章 + 5 维
    ↓
Step 6: 用 scripts/ 生成图表 + PDF
    ↓
Step 7: 用 quality-checklist.md 自检
    ↓
Step 8: 交付（PDF + Markdown）
```

**预期效果**：
- 时间：3-4 小时（v1-v4 的 1/3）
- 质量：每次一致（不再 v1→v4 反复）
- 可复现：Eric 给新地区，方法论直接套用

---

## 六、下一步行动

1. ✅ 完成方法论 README（当前）
2. ⏳ 完成 34 维度信源规范文档
3. ⏳ 完成 SOP 文档（地区 + 单店）
4. ⏳ 完成 schema.md 和模板文件
5. ⏳ 封装 tools（gen_market_analysis.py + call_deepseek.py）
6. ⏳ 创建完整 skill（hotel-feasibility-report）

请 Eric 检阅本方法论体系。

