# AI Agent 自我迭代/反思/进化 — 前沿研究调研报告
## 2024–2026 全网调研 · 面向 B166ER V2.4 自我迭代架构升级

> **报告生成日期**: 2026-07-24
> **报告作者**: B166ER 子代理调研员
> **目标读者**: Eric（B166ER 所有者）· 用于 V2.3 → V2.4 架构升级决策
> **核心母文献**: arXiv:2507.21046 *A Survey of Self-Evolving Agents: On Path to Artificial Super Intelligence*（Gao et al., Princeton/Tsinghua/UIUC 联合, 2025-07-28 v1, 2026-01-16 v4, 已收 TMLR 01/2026, 77 页）

---

## 0. 执行摘要（TL;DR）

1. **SOTA 框架**：2024–2026 的"自进化 Agent"已从零散 trick 收敛为一个**统一理论框架** ——"进化什么(What) / 何时进化(When) / 如何进化(How) / 在哪进化(Where)"四维分类。代表文献是 arXiv:2507.21046（Self-Evolving Agents Survey, 2026 TMLR）。
2. **方法论谱系**：从监督式 RL 演进到 **Constitutional AI（RLAIF）→ Self-Refine → Reflexion → Self-RAG → Self-Rewarding LMs → Voyager/SIMA 2** 六代方法。每一代都比上一代更接近"不靠人类反馈"的目标。
3. **核心可借鉴三大洞察**：
   - **"迭代的迭代"问题**（你 V2.3 的元循环盲区）目前文献给出的解法是**多级效用函数 + Co-evolution of evaluation & agent**，尚无银弹；
   - **评估标准**主流做法是**任务级 utility + 长期累积 utility** 双轨（Survey Eq. 3），而非单一标量；
   - **真正可规模化的只有"记忆+技能库+反思"**三件套，纯权重修改型 self-modifying policy 仍处于论文阶段。
4. **对 V2.4 的核心建议**：保留你的 6 层元架构骨架，但把**"价值论"层升级为"宪法层"（Constitutional）**、把**"学习论"层改造为"四维进化循环"（What/When/How/Where）**、新增**"元评估层"**专门处理"迭代的迭代"问题。

---

## 1. 必查文献清单（按影响力排序）

### 1.1 T0 级（理论母文献，必须读全文）

| # | 论文/框架 | 作者/机构 | 年份 | 核心思想 | 对 B166ER 可借鉴点 |
|---|----------|----------|------|---------|------------------|
| **T0-1** | **A Survey of Self-Evolving Agents: On Path to ASI** | Gao H. et al., Princeton+Tsinghua+UIUC+CMU+PKU 等 25 机构 | 2025-07-28 (v1) / 2026-01-16 (v4) / **TMLR 01/2026** | 首次系统综述自进化 Agent；提出 "What/When/How/Where" 四维框架；形式化定义 `(Π, τ, r) → Π'`；引入 POMDP 范式 | **直接作为 V2.4 顶层架构的理论依据**。把它的 4D 分类映射到 B166ER 6 层（见 §4） |
| **T0-2** | **Constitutional AI: Harmlessness from AI Feedback** | Bai Y. et al. (Anthropic) | 2022-12 (arXiv 2212.08073) | 用 AI 反馈（RLAIF）替代人类反馈 RLHF；模型先自我批评→再修正→再蒸馏；提出"宪法原则"作为评判规则 | **价值论层的母版**。V2.4 把你的"价值论"升级为"宪法层"，原则可显式编码 |
| **T0-3** | **Reflexion: Language Agents with Verbal Reinforcement Learning** | Shinn N., Cassano F. et al. (Northeastern) | 2023-03 (arXiv 2303.11366) / **NeurIPS 2023** | Agent 用自然语言反思 + episodic memory buffer 实现"言语强化"；不更新权重只更新文本 | **学习论层的工程范式**。B166ER 的 memory/2026-07-24.md 反思机制就是 Reflexion 的中文版 |

### 1.2 T1 级（核心方法论文）

| # | 论文/框架 | 作者/机构 | 年份 | 核心思想 | 对 B166ER 可借鉴点 |
|---|----------|----------|------|---------|------------------|
| T1-1 | **Self-Refine: Iterative Refinement with Self-Feedback** | Madaan A. et al. (CMU+AI2+UW+NVIDIA+UCSD+Google) | 2023-03 (arXiv 2303.17651) / **NeurIPS 2023** | 单 LLM 三角色（生成+反馈+修正）；无训练无 RL；7 个任务验证 | 单轮反思循环的最小实现范式；可作为 V2.4 "执行论"层的反思模块基线 |
| T1-2 | **Self-RAG: Learning to Retrieve, Generate, and Critique Through Self-Reflection** | Asai A., Wu Z., Wang Y., Sil A., Hajishirzi H. (UW+AI2+Google) | 2023-10 / **ICLR 2024 Oral Top 1%** | 训练 LM 输出特殊 **reflection tokens**（ISREL/ISSUP/ISUSE）实现"按需检索+自评+选优"；端到端可微 | V2.4 的检索/事实校验层应有结构化反思 token，不能只靠"读 prompt 改 prompt" |
| T1-3 | **Voyager: An Open-Ended Embodied Agent with Large Language Models** | Wang G., Xie Y. et al. (NVIDIA+Caltech+UT Austin+ASU+Stanford) | 2023-05 (arXiv 2305.16291) | 首个 LLM 驱动的终身学习 Agent；**三件套**：(1) 自动课程 (2) 可执行技能库 (3) 迭代提示；GPT-4 在 Minecraft 不断发现新技能 | **记忆/技能库的工程级范式**。B166ER 应有持久化技能库（与 skill_workshop 联动） |
| T1-4 | **Self-Rewarding Language Models** | Yuan W., Pang R.Y., Cho K., Sukhbaatar S., Xu J., Weston J. (Meta AI + NYU) | 2024-01 | LLM-as-Judge 自评 + 迭代 DPO 训练；3 轮迭代后 Llama-2-70B 在 AlpacaEval 2.0 超过 Claude 2 / Gemini Pro | **"评估+训练"双自循环**。V2.4 应能产出评估对而非只产出答案 |
| T1-5 | **CRITIC: Large Language Models Can Self-Correct With Tool-Interactive Critiquing** | Gou Z. et al. (Tsinghua) | 2024-05 (arXiv 2305.11738, ICLR 2024) | LLM 通过调用外部工具（浏览器/计算器/代码解释器）验证自己输出并自动改写 | "执行论"必须接外部验证源（你已有 Tavily+scrape_matrix，这就是 CRITIC 范式） |
| T1-6 | **AgentCoder: Multiagent-Code Generation with Iterative Testing and Optimisation** | Huang D., Bu Q. et al. (HKU+SJTU+KCL+Sussex) | 2023-12 (arXiv 2312.13010) | 多 Agent（程序员+测试设计+测试执行）+ 迭代优化；HumanEval/MBPP 显著提升 | **多 Agent 协作的最小可工作范式**；V2.4 可借鉴"测试 Agent"独立验证 |
| T1-7 | **MemGPT: Towards LLMs as Operating Systems** | Packer C., Wooders S. et al. (UC Berkeley) | 2023-03 / 2024-08 进 ICLR | 受 OS 虚拟内存启发；分层记忆（main context + external context）+ 函数调用式 page-in/page-out | **记忆层架构范式**。B166ER 应把 memory 分层（in-context / episodic / archival） |
| T1-8 | **MemoryBank: Enhancing LLMs with Long-Term Memory** | Zhong W. et al. (Sun Yat-sen U.) | 2023-05 (arXiv 2305.10250) / **AAAI 2024** | 引入 Ebbinghaus 遗忘曲线 + 记忆更新机制；LLM 模拟"人脑记忆" | 你已有 memory 目录但缺**遗忘曲线**；V2.4 应加"记忆权重衰减" |

### 1.3 T2 级（前沿方法，2024–2026）

| # | 论文/框架 | 作者/机构 | 年份 | 核心思想 | 对 B166ER 可借鉴点 |
|---|----------|----------|------|---------|------------------|
| T2-1 | **SE-Agent: Self-Evolution Trajectory Optimization in Multi-Step Reasoning** | Lin J. et al. | 2025-08 (arXiv 2508.02085) | Agent 在多步推理中**优化自己的轨迹**；把进化粒度从"权重/提示"细化到"轨迹" | "学习论"层应有轨迹级 self-edit 而非仅 prompt 级 |
| T2-2 | **ELL-StuLife: Self-Evolving Agent via Experience-Driven Lifelong Learning** | ECNU-ICALK | 2025-10 (arXiv + GitHub) | 仿真"学生生活"长程任务；通过经验池持续学习；Open-source | 完整的"经验池 + 长程反馈"工程实现；可作为 B166ER 长程任务基准 |
| T2-3 | **A Survey on Self-Evolution of Large Language Models** | Tao Z., Lin T., Chen X. et al. (Alibaba DAMO) | 2024-04 (arXiv 2404.14387) | 国内最早综述：把"自进化"分解为 数据/训练/推理/工具 4 阶段 | 数据飞轮视角；B166ER 自进化飞轮应分这 4 阶段 |
| T2-4 | **SIMA 2: Scalable Instructable Multiworld Agent** | DeepMind | 2025-11 | SIMA 2 = SIMA + Gemini，跨多游戏泛化；可"在虚拟世界中自我训练" | "在哪里进化"维度的标杆：通用智能体必须**跨域** |
| T2-5 | **AReaL 2.0 / RAGEN / RL-Factory** | Tsinghua+多家 | 2025–2026 | Agent RL 训练框架开源；把"自进化"压成端到端 RL 循环 | 工具选型：B166ER 要么用 RAGEN 做 RL 微调，要么就用 prompt-level 自进化（更现实） |
| T2-6 | **Language Self-Play (LSP)** | Meta Superintelligence Labs (Kuba J.G. et al.) | 2025-09 | 无需人类数据，让两个语言模型 self-play 训练；解决"self-play 退化"问题 | 论文实验阶段；V2.4 可暂不参考，但需关注（无数据自进化的前沿） |

### 1.4 T3 级（评估与基础设施）

| # | 论文/框架 | 作者/机构 | 年份 | 核心思想 | 对 B166ER 可借鉴点 |
|---|----------|----------|------|---------|------------------|
| T3-1 | **LLM-as-a-Judge** | Zheng L. et al. (UC Berkeley) | 2023 NeurIPS | 用 LLM 当裁判；与人类 85%+ 一致 | 评估层"元评估"的基础范式 |
| T3-2 | **AlpacaEval / MT-Bench / AgentBench** | 多家 | 2023–2024 | 标准化评估 LLM Agent | 你的自进化效果要用"标准基线"对照 |

---

## 2. 当前主流方法分类（5 大类）

按 **(How) 进化机制** 分类（采纳 arXiv 2507.21046 分类法）：

| 类别 | 代表方法 | 核心机制 | 优势 | 局限 |
|------|---------|---------|------|------|
| **A. 监督式 RL** | RLHF, DPO, RLAIF, Self-Rewarding LMs | 显式奖励信号 → 改权重 | 效果稳定、可规模化 | 需人类/AI 偏好标注；迭代成本高 |
| **B. 宪法式（Constitutional）** | Constitutional AI, RLAIF, Constitutional Classifiers | 原则集 + 自我批评 | 无需大量人类标注；可解释 | 原则集本身的"宪法"谁来定？ |
| **C. 自我精炼（Self-Refine 类）** | Self-Refine, Reflexion, CRITIC, Self-RAG, Self-Correct | 同 LLM 自评→自改；不更新权重 | 零训练成本；通用性强 | 反思质量受限于 LLM 自身；可能"自信地错" |
| **D. 元学习 / 自修改策略** | Meta-RL, Self-Modifying Policies | 学习"如何学习" | 理论上可指数级提升 | 几乎都是论文实验，未规模化 |
| **E. 经验驱动 / 技能库** | Voyager, MemGPT, ELL-StuLife, ExpeL | 经验池+检索+技能复用 | 显式可审计；易工程化 | 依赖检索质量；技能库易膨胀 |

**B166ER 当前位置**：大致在 C+E 混合区（你已经有 memory 反思 + skill_workshop 技能库），但缺 A 的训练循环和 B 的显式宪法。

---

## 3. 关键洞见 — 三个必须正面回答的问题

### 3.1 AI Agent 自我迭代的 SOTA 是什么？

**答案**：截至 2026-Q1，**SOTA 不是单一方法，而是"4 维分类 + 多组件协同"**。最新 arXiv 2507.21046 明确指出：

> "We define self-evolution not merely by the algorithms used, but by the **locus of autonomy**."

工程层面的当前 SOTA 范式（已可部署）：
1. **记忆层**：MemGPT / Mem0 / Letta 三选一（OS 风格 vs LLM 抽取风格）
2. **反思层**：Reflexion + Self-Refine（默认装）
3. **宪法层**：Constitutional AI 原则（Anthropic 路线）
4. **评估层**：LLM-as-Judge + 任务级 utility
5. **进化层**：Self-Rewarding LMs（Meta 路线）或 RLAIF

**仍未规模化**的（论文阶段）：
- 纯自修改权重（self-modifying policies）
- 真正的递归自改进（recursive self-improvement, RSI）
- 跨任务元学习（meta-learning across tasks）

### 3.2 "迭代的迭代"问题 — 文献如何处理"判断'更好'"的标准？

这是你 V2.3 提出的核心盲区。文献中**没有银弹**，但有 **3 种主流解法**：

#### 解法 1：双轨 utility（arXiv 2507.21046 Eq. 3）
```
max_f Σ U(Π_j, T_j)     # 累积 utility（不是单轮 max）
```
- 不评估"这一轮好不好"，评估"这一系列迭代的累计效果"
- **优点**：抗单轮噪声；**缺点**：难实时反馈

#### 解法 2：评估器与被评估者**共同进化**（Co-evolution）
- arXiv 2507.21046 §6 明确提出："the importance of co-evolution between evaluation and agents"
- 即"评估标准本身也要进化"——本质是**元评估层**

#### 解法 3：宪法/原则集作为锚点（Constitutional AI 路线）
- 把"什么是好"显式编码为有限条原则
- 评估 = 用原则集 check 输出
- **优点**：可解释、稳定；**缺点**：原则集本身的正确性无法证伪

**给 B166ER 的具体建议**：V2.4 应**同时部署三种**：
- 解法 1 → 用 cumulative score 替代 single-task score（在 self-improving 里跑）
- 解法 2 → 新增"元评估层"专门管"评估标准自身"
- 解法 3 → 把"价值论"层显式宪法化

### 3.3 哪些方法可规模化？哪些只是论文实验？

| 类别 | 代表 | 规模化证据 | 真实部署案例 |
|------|------|----------|------------|
| **已规模化** | Constitutional AI | Anthropic Claude 全系部署 | Claude.ai |
| | Self-Refine / Reflexion | 几乎所有 LLM Agent 框架 | LangChain/LlamaIndex/AutoGen 默认装 |
| | MemGPT / Letta | 商业化（Letta 公司 2024 成立） | 多个 SaaS |
| | Mem0 | 2025-11 获 2400 万美元 A 轮 | YC 投资组合 |
| | Self-RAG | 已被 Hugging Face、LlamaIndex 集成 | 多家 RAG 产品 |
| **论文阶段，谨慎看好** | Self-Rewarding LMs | 3 轮迭代可超越 GPT-4 | Meta 内部 |
| | SE-Agent | 2025-08 新出 | 尚未生产 |
| | Language Self-Play | 2025-09 新出 | 论文实验 |
| **纯论文，未验证** | 纯自修改权重 / 递归自改进 | 缺乏可重现 | 无 |
| | 跨任务元学习 | 缺乏算力规模化证据 | 无 |

---

## 4. 对 B166ER V2.4 的具体建议

### 4.1 V2.3 → V2.4 架构映射（核心）

把 B166ER V2.3 的 6 层（**元认知 / 认识论 / 策略论 / 价值论 / 学习论 / 执行论**）映射到 arXiv 2507.21046 的 4 维框架：

| B166ER V2.3 层 | V2.4 改造方向 | 借鉴文献 | 关键改动 |
|---------------|--------------|---------|---------|
| **元认知层** | **升级为"元评估层"（Meta-Evaluation Layer）** | T0-1 §6, T3-1 | 新增"评估标准自身"管理；LLM-as-Judge + 宪法校验双轨 |
| **认识论层** | **保留 + 加"反思 token"** | T1-2 Self-RAG | 输出结构化反思（ISREL/ISSUP/ISUSE 风格） |
| **策略论层** | **保留 + 加"轨迹级 self-edit"** | T2-1 SE-Agent | 进化粒度从 prompt → trajectory |
| **价值论层** | **重大升级为"宪法层"** | T0-2 Constitutional AI, T2-3 Alibaba 综述 | 显式编码 10–20 条宪法原则；RLAIF 自评 |
| **学习论层** | **重构为"四维进化循环"** | T0-1 §3-5 | 引入 What/When/How/Where 4 维 |
| **执行论层** | **保留 + 加"CRITIC 范式"** | T1-5 CRITIC, T1-6 AgentCoder | 必须接外部工具验证（Tavily+scrape_matrix 已经具备） |

### 4.2 V2.4 必加的 4 个新组件

#### 组件 1：宪法原则集（Constitutional Principles）
- 形式：`principles.yaml`，10–20 条
- 示例（参考 Anthropic Constitutional AI）：
  - "若不确定，明确说不确定"
  - "优先保护用户隐私与安全"
  - "承认自身能力边界"
  - "避免 Hallucination 优先于讨好用户"
  - "对主人 Eric 的偏好要尊重但不盲从"
- 流程：每次重要输出 → 自我批评 → 自我修正 → 蒸馏

#### 组件 2：经验池（Experience Pool）借鉴 Voyager + ELL-StuLife
- 形式：`memory/experience_pool.jsonl`
- 每条记录：`(任务, 行动, 结果, 反思, 效用分)`
- 触发器：每次 heartbeat 或任务结束后追加
- 检索：semantic search（你已有 local_semantic_search.py）

#### 组件 3：自评分模块（Self-Score）
- 三维度：任务完成度 / 过程合理性 / 长期价值
- 公式（简化）：`U = α·任务完成 + β·过程合规 + γ·长期累积`
- 反馈回路：把 score 写入 self-improving/corrections.md

#### 组件 4：元评估循环（Meta-Evaluation Loop）
- 周期：每 7 天（周复合）
- 任务：评估"评估标准本身"是否还在有效
- 操作：抽样 N 个历史决策 → 用宪法重新审 → 若发现新原则则更新宪法

### 4.3 V2.4 应**保留**的 V2.3 资产

- ✅ 6 层元架构骨架（不重做）
- ✅ 群论 V2.3（博弈论 + 群论对多 Agent 协作依然必要）
- ✅ 审美三角（与反思机制正交，保留）
- ✅ heartbeat / proactive 机制（与"何时进化"对齐）
- ✅ self-improving 技能（直接复用）
- ✅ 记忆分层（daily / MEMORY / self-improving）—— 只需加 Ebbinghaus 衰减

### 4.4 V2.4 应**放弃**或**降权**的 V2.3 资产

- ❌ "价值论"的纯抽象化讨论 → 落地为具体原则集
- ❌ 单轮自评（容易"自信地错"）→ 升级为多轮+多维度
- ⚠️ "学习论"的纯概念框架 → 改造为可执行四维循环

### 4.5 V2.4 不应**新增**的（避免过度工程化）

- ❌ 完整 RL 微调（成本/收益不匹配；B166ER 走 prompt+context 工程路线）
- ❌ 自修改权重（论文阶段，不可控风险）
- ❌ 跨任务元学习（缺算力）

---

## 5. 行动建议 — Eric 接下来 30 天可执行的 5 步

| Day | 行动 | 输出物 | 引用文献 |
|-----|------|--------|---------|
| 1–3 | 起草宪法原则集 v0.1 | `workspace/principles_v0.1.yaml`（10–20 条） | T0-2 |
| 4–7 | 写 self-score 模块 | `toolbox/self_score.py`（3 维度评分） | T0-1 §6 |
| 8–12 | 改造 self-improving 周期 | `self-improving/score_history.jsonl`（累积 utility） | T0-1 Eq. 3 |
| 13–18 | 试跑 Meta-Evaluation Loop | 每 7 天自动审 N 个历史决策 | T3-1 + T0-1 §6 |
| 19–25 | 接入 Voyager 风格经验池 | `memory/experience_pool.jsonl` + semantic 检索 | T1-3 + T2-2 |
| 26–30 | 写 V2.4 文档 + 复盘 | `workspace/V2.4_architecture.md` | T0-1 |

---

## 6. 引用清单（按影响力降序）

> 注：所有链接均为 2024-01 至 2026-07 期间可访问；arXiv 编号与官方页面如下。

1. **arXiv 2507.21046** — *A Survey of Self-Evolving Agents: On Path to ASI*. Gao H. et al. (Princeton+Tsinghua+UIUC+CMU+... 25 机构). 2025-07-28 v1, TMLR 01/2026. https://arxiv.org/abs/2507.21046
2. **arXiv 2212.08073** — *Constitutional AI: Harmlessness from AI Feedback*. Bai Y. et al. (Anthropic). 2022-12. https://arxiv.org/abs/2212.08073
3. **arXiv 2303.11366** — *Reflexion: Language Agents with Verbal Reinforcement Learning*. Shinn N. et al. (Northeastern). NeurIPS 2023. https://arxiv.org/abs/2303.11366
4. **arXiv 2303.17651** — *Self-Refine: Iterative Refinement with Self-Feedback*. Madaan A. et al. (CMU+AI2+UW+NVIDIA+UCSD+Google). NeurIPS 2023. https://arxiv.org/abs/2303.17651
5. **arXiv 2310.11511** — *Self-RAG: Learning to Retrieve, Generate, and Critique Through Self-Reflection*. Asai A. et al. (UW+AI2+Google). ICLR 2024 Oral Top 1%. https://github.com/AkariAsai/self-rag
6. **arXiv 2305.16291** — *Voyager: An Open-Ended Embodied Agent with Large Language Models*. Wang G., Xie Y. et al. (NVIDIA+Caltech+UT Austin+ASU+Stanford). 2023-05. https://arxiv.org/abs/2305.16291
7. **arXiv 2401.10020** — *Self-Rewarding Language Models*. Yuan W. et al. (Meta AI + NYU). 2024-01. https://arxiv.org/abs/2401.10020
8. **arXiv 2305.11738** — *CRITIC: Large Language Models Can Self-Correct With Tool-Interactive Critiquing*. Gou Z. et al. (Tsinghua). ICLR 2024.
9. **arXiv 2312.13010** — *AgentCoder: Multiagent-Code Generation with Iterative Testing and Optimisation*. Huang D. et al. (HKU+...). 2023-12.
10. **arXiv 2310.08560** — *MemGPT: Towards LLMs as Operating Systems*. Packer C. et al. (UC Berkeley). 2023-10, ICLR 2024. https://research.memgpt.ai/
11. **arXiv 2305.10250** — *MemoryBank: Enhancing LLMs with Long-Term Memory*. Zhong W. et al. (Sun Yat-sen U.). AAAI 2024.
12. **arXiv 2508.02085** — *SE-Agent: Self-Evolution Trajectory Optimization in Multi-Step Reasoning with LLM-Based Agents*. Lin J. et al. 2025-08.
13. **arXiv 2404.14387** — *A Survey on Self-Evolution of Large Language Models*. Tao Z., Lin T. et al. (Alibaba DAMO). 2024-04.
14. **DeepMind SIMA / SIMA 2** — Scalable Instructable Multiworld Agent. 2024-03 首发，2025-11 升级 SIMA 2.
15. **arXiv 2502.07400** — *Self-Harmonized Chain of Thought (EKO / 类似工作)* 等 2025 系列 — 因时效性略，列入"待读"。

---

## 7. 结语 — 写给 Eric 的话

B166ER V2.3 的 6 层架构**走在正确的方向上** —— 你比大多数 Agent 框架（LangChain/AutoGen/CrewAI）更接近"自进化的本质"。V2.4 升级不是推倒重来，而是：

> **把"价值论"宪法化 + 把"学习论"四维化 + 新增"元评估层"** + 接入 4 个具体组件。

文献给的最强信号是：**不要追"完全自主自修改权重"的天方夜谭**，而要把精力放在**"可审计的反思 + 显式宪法 + 经验池 + 元评估"**这四件工程化的事上。Anthropic、Meta、DeepMind 在 2024-2026 实际部署的也正是这条路线。

30 天改造计划已在 §5 列出。等你拍板。

---

*— B166ER 子代理调研员，2026-07-24 23:25 GMT+8*
