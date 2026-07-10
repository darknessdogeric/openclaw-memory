# 8 阶段生命周期主决策树

> **用途**：Eric 1v1 咨询时跟业主**白板画**用的核心决策图
> **形式**：Mermaid（可渲染为 SVG/PNG，或直接看代码）
> **深度**：每个决策节点都有"分叉判断标准"
> **配合**：`lifecycle-index.md` 8 阶段说明

---

## 主决策树（Mermaid）

```mermaid
graph TD
    Start([业主来咨询]) --> A1{业主类型?}
    A1 -->|国央企| Path_SOE[路径 A: 国央企]
    A1 -->|民营/私营| Path_PVT[路径 B: 民营]
    A1 -->|其他| Path_Other[路径 C: 混合]

    Path_SOE --> B1{项目过三重一大?}
    B1 -->|否| B1No[先合规评估]
    B1 -->|是| B2[阶段 1-3 评估]

    Path_PVT --> B2

    B2 --> Stage1[阶段 1: 物业资产评估]
    Stage1 --> S1Check{总分 ≥ 30?}
    S1Check -->|< 20| S1Fail[❌ 不建议改造<br/>建议转让]
    S1Check -->|20-30| S1Warn[⚠️ 需深度分析]
    S1Check -->|≥ 30| Stage2[阶段 2: 项目重新定位]

    S1Warn --> Stage2

    Stage2 --> S2Check{定位清晰?}
    S2Check -->|否| S2Refine[先做定位<br/>再用 stage 1 评估]
    S2Check -->|是| Stage3[阶段 3: 经营模式选择]

    S2Refine --> Stage2

    Stage3 --> S3Check{业主类型}
    S3Check -->|国央企| S3SOE[→ 全委/集团品牌<br/>(几乎不加盟)]
    S3Check -->|民营/私营| S3PVT[→ 自营/加盟品牌<br/>(东呈业绩对赌)]
    S3Check --> S3Any[继续]

    S3SOE --> Stage4
    S3PVT --> Stage4
    S3Any --> Stage4

    Stage4[阶段 4: 改造方式选择]
    Stage4 --> S4Check{物业状态}
    S4Check -->|< 5 年未翻新| S4Light[→ 轻改<br/>1-2 个月]
    S4Check -->|5-10 年| S4Mid[→ 中改<br/>3-6 个月 + 装配式]
    S4Check -->|> 10 年| S4Heavy[→ 重改<br/>6-12 个月]

    S4Light --> Stage5
    S4Mid --> Stage5
    S4Heavy --> Stage5

    Stage5[阶段 5: 投资匡算]
    Stage5 --> S5Check{业主类型}
    S5Check -->|国央企| S5SOECalc[+30-50% 成本]
    S5Check -->|民营/私营| S5PVTCalc[基线成本]

    S5SOECalc --> S5NPV
    S5PVTCalc --> S5NPV{NPV > 0?}

    S5NPV -->|否| S5Stop[❌ 投资不可行<br/>考虑择机/转让]
    S5NPV -->|是| Stage6

    Stage6[阶段 6: 供应商选择]
    Stage6 --> S6Check{业主类型}
    S6Check -->|国央企| S6SOE[→ 公开招标<br/>不可选朋友推荐]
    S6Check -->|民营/私营| S6PVT[→ 商业谈判<br/>可选朋友推荐]

    S6SOE --> Stage7
    S6PVT --> Stage7

    Stage7[阶段 7: 团队去留]
    Stage7 --> S7Check{业主类型}
    S7Check -->|国央企| S7SOE[→ 稳岗不裁<br/>+ 党建/工会]
    S7Check -->|民营/私营| S7PVT[→ 灵活调整<br/>+ 业绩对赌]

    S7SOE --> Stage8
    S7PVT --> Stage8

    Stage8[阶段 8: 运营 + 投后 + 退出]
    Stage8 --> S8Check{退出意向}
    S8Check -->|< 5 年| S8Short[→ 5 年计划<br/>3-6 个月退出]
    S8Check -->|5-10 年| S8Mid[→ 10 年计划<br/>市场化退出]
    S8Check -->|10-20 年| S8Long[→ 长期持有<br/>多次软改]

    S8Short --> End([交付方案])
    S8Mid --> End
    S8Long --> End

    %% 样式（按业主类型）
    classDef soeNode fill:#E8F0FE,stroke:#4285F4,color:#000
    classDef pvtNode fill:#FFF3E0,stroke:#FB8C00,color:#000
    classDef failNode fill:#FFEBEE,stroke:#EA4335,color:#000
    classDef successNode fill:#E8F5E9,stroke:#34A853,color:#000

    class Path_SOE,B1,B1No,B2SOECalc,S6SOE,S7SOE soeNode
    class Path_PVT,S3PVT,S5PVTCalc,S6PVT,S7PVT pvtNode
    class S1Fail,S5Stop failNode
    class S8Short,S8Mid,S8Long,End successNode
```

---

## 决策树使用说明

### 1. 何时用
- ✅ 1v1 咨询**白板**画给业主看
- ✅ 业主**首次**来咨询时的"全局图"
- ✅ 业主**迷失**在某个阶段时回看整体
- ❌ 不是 PPT 详细方案（那是诊断报告）

### 2. 怎么用
- **Step 1**：确认业主类型（国央企/民营）→ 路径分流
- **Step 2**：从 Stage 1 依次往下走
- **Step 3**：每个 Stage 都有"分叉判断"（总分 / 定位 / 业主类型）
- **Step 4**：不同业主类型走不同路径（国央企 vs 民营）

### 3. 关键节点判断标准

| 节点 | 判断标准 |
|------|----------|
| **A1 业主类型** | 5 问清单（见 ownership-types.md 第 6 节）|
| **B1 双重一大** | 国央企必查；项目 ≥ 500 万 = 必上党委会 |
| **S1Check 总分** | 5 大维度各 10 分，合计 ≥ 30 分 = 建议改造 |
| **S2Check 定位** | 业主能 1 句话说清 = 定位 OK |
| **S3Check 业主类型** | 国央企→全委；民营→加盟（业绩对赌）|
| **S4Check 物业状态** | 上次翻新 + 当前 OCC |
| **S5Check NPV** | 折现率 10%，5 年/10 年视角 |
| **S6Check 业主类型** | 国央企=公开招标；民营=商业谈判 |
| **S7Check 业主类型** | 国央企=稳岗；民营=灵活 |
| **S8Check 退出意向** | 业主自述 + 资金压力 |

### 4. 失败节点处理

| 失败 | 处理 |
|------|------|
| **S1Fail 总分 < 20** | 不建议改造 → 建议转让或退出（不浪费时间）|
| **S5Stop NPV < 0** | 数学上不可行 → 重新评估或择机 |

### 5. 输出物（决策树后）

| 节点 | 输出物 |
|------|--------|
| Stage 1 评估 | 5 大维度自评（总分）|
| Stage 2 定位 | 定位声明 + 客群画像 |
| Stage 3 模式 | 自营/加盟/全委 决策 |
| Stage 4 模式 | 轻改/中改/重改 决策 + 装配式 |
| Stage 5 匡算 | 3 场景回本 + NPV + 敏感性 |
| Stage 6 供应商 | 4 支柱选定 |
| Stage 7 团队 | 4 类人去留 + 激励方案 |
| Stage 8 投后退出 | 5/10/20 年计划 |

**完整输出 = 诊断报告**（见 `outputs/2026-06-12-diagnosis-report-template.md`）

---

## Mermaid 渲染

### 方法 1：VS Code + Markdown Preview
- 安装 `Markdown Preview Mermaid Support` 扩展
- 直接打开本文件，预览即可看到图

### 方法 2：在线渲染
- 访问 https://mermaid.live/
- 粘贴 Mermaid 代码
- 导出 PNG/SVG

### 方法 3：命令行
```bash
# 安装 mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# 渲染
mmdc -i 8-stage-master-tree.md -o 8-stage-master-tree.svg
```

### 方法 4：嵌入 HTML
```html
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>mermaid.initialize({ startOnLoad: true });</script>
<div class="mermaid">
  [mermaid 代码]
</div>
```

---

## 决策树的"不变量"原则

无论业主类型/物业状态/预算怎么变，**8 阶段顺序不变**：
```
1 → 2 → 3 → 4 → 5 → 6 → 7 → 8
```

但**每个阶段的具体行动**会随业主类型变化（国央企 vs 民营）。

**这个"不变量 + 变量"结构** = 决策树的设计哲学。

---

## 决策树 vs 诊断报告

| 维度 | 决策树（本文件）| 诊断报告 |
|------|--------------|----------|
| 用途 | 1v1 白板画 | 交付业主 |
| 长度 | 1 张图 | 20-30 页 |
| 形式 | 视觉化 | 文字 + 表格 |
| 详细度 | 粗（决策点）| 细（数据 + 测算）|
| 时机 | 咨询开始 | 咨询结束 |
| 受众 | 业主+Eric 同看 | 业主拿走 |

**配合使用**：决策树是"看地图"，诊断报告是"具体路线 + 时间表"。

---

## 相关文件

- `lifecycle-index.md` - 8 阶段说明
- `stage-1-asset-assessment.md` 到 `stage-8-exit-strategy.md` - 8 个阶段文件
- `decision-framework.md` - 基础决策框架
- `decision-tree-extended.md` - 多场景决策树
- `ownership-types.md` - 国央企 vs 民营
- `sov-private-differences.md` - 详细对比
- `outputs/2026-06-12-diagnosis-report-template.md` - 诊断报告

---

## 标签

`#决策树` `#8阶段` `#可视化` `#Eric白板工具` `#2026-06-12`
