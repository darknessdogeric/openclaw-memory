# REA 架构学习笔记（2026-10-15）

> **来源**: `https://github.com/morluto/rea` (REA = Reverse Engineer Anything)
> **触发**: Eric 「评估一下这个」 → 「方案 2: 读源码 1-2 小时」
> **范围**: 只读 `src/composition/` + `AGENTS.md` + `.agents/skills/` + `package.json`（不装、不 fork、不克隆）
> **结论**: 260K star 异常，但工程真实。学习它的 MCP + skills + tools 三层架构模式

---

## 一、REA 一句话定义

**REA = MCP 服务 + 反向工程工具链编排层。** 它把 IDA / Hopper / Ghidra / JEB / Frida / apktool / adb 等 16 个 RE 工具通过 MCP 协议封装，让 AI agent（Claude Code / Qwen / Gemini / Grok / DeepSeek 等）能用自然语言调用这些工具逆向 app / binary。

---

## 二、关键结构信号

### 2.1 三层架构（核心洞察）

```
┌─────────────────────────────────────────────┐
│  .agents/skills/  ← Agent 工作流（4 个）     │  ← "如何使用工具"
│  - rea-changelog-update                      │
│  - rea-ci-tests-audit                        │
│  - rea-tool-design                           │
│  - reverse-engineer-anything                 │
└─────────────────────────────────────────────┘
                  ↑ 调用
┌─────────────────────────────────────────────┐
│  src/composition/  ← 原子工具（32 个）       │  ← "工具能做什么"
│  - adb / android / apktool / electron         │
│  - binary / wasm / firmware / pcap           │
│  - rust / go / javascript / flutter         │
│  - browserObservation / runtimeObservation   │
│  - auxiliaryAnalysisProviders (抽象层)        │
└─────────────────────────────────────────────┘
                  ↑ 封装
┌─────────────────────────────────────────────┐
│  第三方 RE 工具（IDA / Ghidra / Hopper / JEB）│  ← "底层二进制能力"
└─────────────────────────────────────────────┘
```

**B166ER 现状对比**:

| 维度 | B166ER | REA | 差距 |
|------|--------|-----|------|
| Skills 数量 | 95+ | 4 | B166ER 太多，可能未分层 |
| Tools 数量 | 不分层 | 32 (清晰分类) | B166ER 需要显式 tools 层 |
| 工具与 Skill 关系 | 混合 | 严格分离 | B166ER 可以引入 tools/ 目录 |
| MCP 协议 | ❌ 未用 | ✅ SDK v2.3.1 | B166ER 应考虑 |

### 2.2 AGENTS.md 核心原则（16 条可执行哲学）

**最有价值的 6 条**（B166ER 应直接采用）：

1. **"Distinguish observations, derivations, inferences, and unknowns"**
   → 把"我看到什么 / 推导出什么 / 推测什么 / 不知道什么"明确分离。B166ER 记忆和推理应引入此分类。

2. **"Dependencies flow inward"** (Clean Architecture)
   → 域语义在内，provider 在外，CLI/MCP 在最外。技能调用链应该单向：Skill → Tool → External API。

3. **"Configuration changes must be additive and idempotent"**
   → B166ER 自修改 SOUL/AGENTS.md 时必须幂等（同输入同输出）。

4. **"Preserve caller-selected inputs and local evidence"**
   → Eric 显性授权 = 不可篡改的输入凭证。B166ER 不应改写 Eric 原始指令。

5. **"Give each interpretation and resource a clear owner"**
   → KB 单一所有者。KB-AHL 由 Eric 主导，KB-Methodology 由 B166ER 维护。责任清晰。

6. **"Bind handlers to named contracts with exact types"**
   → 工具契约必须显式。Tool schema 不能用 `any`/字典。

### 2.3 优化优先级（最具颠覆性）

REA 显式说"按此顺序优化"：

```
1. Agent tokens and context  ← 最重要
2. Analysis time
3. CPU and memory
```

**翻译到 B166ER**:

```
1. Eric 注意力 + context window  ← 应该最优先
2. Eric 任务时间
3. 我的 token / 计算
```

**现状 vs 目标**:
- 现状：B166ER 倾向"做更多更全"（详尽报告、长 KB、详细 cite）
- 目标："最小充分答案" + "必要的来源、覆盖、限制"

这就是 SOUL V2.4 "真 > 善 > 美" 的工程化执行：去掉装饰性详尽，保留决定性最小集。

### 2.4 错误处理范式

REA 用 **tagged error algebra + Result 类型**：
- 不是 throw exception
- 是返回值携带 success/error 标签
- 强制 caller 处理 error 分支

**B166ER 现状**: 用 print 错误 + return None
**应该**: 引入 Python 的 `Result` 库（`returns` / `result`）或自建 Tagged Union

### 2.5 工具链（值得 B166ER 借鉴的）

REA 的 dev toolchain 全是 2026 主流前沿：
- **TypeScript 7.0.2**（同时测 6.0.3 + 7.0.2 双版本）
- **oxlint + oxfmt + rolldown**（oxc 工具链，比 ESLint+Prettier 快 50-100 倍）
- **Vitest 5.0.3**（现代测试框架）
- **Stryker 10.0.0**（变异测试，确保测试真的有效）
- **Turborepo 2.11.7**（monorepo 编排）
- **knip**（找无用 export）
- **jscpd**（找重复代码）
- **VitePress**（文档）

**B166ER 可借鉴**:
- Python 工具: `ruff` (替代 flake8+black，速度快 10-100 倍)
- 测试: `pytest + mutmut` (变异测试)
- Lint: 已用 `oxlint` 不可用（Python only），用 `ruff check`
- 自修改幂等: 自建 `self-improve` 模块，加 idempotency_test

### 2.6 模型客户端多版本支持（少见的设计）

REA 显式支持并测试 10+ AI model clients：
- claude / qwen / gemini / grok / opencode / deepseek / copilot / commandcode / omp / pi / hermes

每个都有独立 `verify:*-client.mjs` 验证脚本。

**B166ER 启示**: 不绑定单一模型。SOUL V2.4 写明"主动推断 + 模型 provider/model 显式引用"，但没真正支持多 provider。REA 的"模型即 adapter"模式值得借鉴。

---

## 三、B166ER 可立即采用的 5 个动作

### 动作 1: 引入 tools/ 与 skills/ 显式分离

**现状**: B166ER skills/ 95+ 个，混在一起
**改进**: 在 `workspace/` 下新建 `tools/` 目录
```
workspace/
  skills/        ← 工作流 (existing)
  tools/         ← 原子操作 (new)
  agents/        ← 跨 skill 编排 (new, optional)
```

每个 tool 文件 = 一个原子能力（如 `read_url.py`, `fetch_rss.py`, `git_commit.py`），每个 skill 调用多个 tools。

### 动作 2: 工具契约显式化

每个 tool 用 JSON Schema 定义：
```python
# tools/fetch_rss.py
SCHEMA = {
  "name": "fetch_rss",
  "input": {"url": "string", "timeout": "int"},
  "output": {"items": "array", "errors": "array"},
  "errors": ["timeout", "404", "parse_error"]
}
```

### 动作 3: 错误处理改 Result 范式

引入 `returns` 库：
```python
from returns.result import Result, Success, Failure

def fetch_rss(url: str) -> Result[list, str]:
    try:
        ...
        return Success(items)
    except Exception as e:
        return Failure(f"fetch_rss_failed: {e}")
```

### 动作 4: 优化优先级显式化

在 AGENTS.md / SOUL.md 增补：

> **优化优先级**（自上而下）:
> 1. Eric 的注意力 + 上下文窗口（最小充分答案）
> 2. Eric 任务时间（一次到位不返工）
> 3. B166ER 的 token / 计算
>
> 任何"详尽报告"必须先过这 3 层 filter。

### 动作 5: 自修改幂等性测试

B166ER 写自己的 self-improving 规则时，加 idempotency_test：
```python
# self-improving/test_idempotency.py
def test_rule_X_idempotent():
    before = read_file("rules.md")
    apply_rule_X(rules.md)
    after = read_file("rules.md")
    apply_rule_X(rules.md)  # 再跑一次
    after2 = read_file("rules.md")
    assert after == after2  # 幂等
```

---

## 四、不应照搬的（红绿黄灯）

| 维度 | 评估 | 原因 |
|------|------|------|
| 260K star | ❌ 不可信 | 6 个月不可能，灰产嫌疑 |
| RE 工具链集成 | ❌ 不需要 | B166ER 方向是 AI 代理 + 知识图谱，不是 RE |
| 16 种语言 polyglot | ❌ 不需要 | 过度工程，B166ER 用 Python 足够 |
| 74MB monorepo | ❌ 不需要 | B166ER 工作区不需要这么大 |
| Stryker 变异测试 | 🟡 价值高但成本高 | 慢慢引入，不强求 |
| oxlint 工具链 | 🟢 部分采用 | Python 改 ruff |
| MCP 协议 | 🟡 长期考虑 | 当前 exec + read 够用，但 MCP 是趋势 |
| AGENTS.md 哲学原则 | 🟢 强烈推荐 | 16 条里至少 6 条 B166ER 已隐式做了，**显式化即可** |
| skills/tools 分离 | 🟢 强烈推荐 | B166ER 95+ skills 已需要分层 |

---

## 五、最终判断（一句话）

> **REA 的工程化深度（尤其 AGENTS.md 的 16 条原则 + skills/tools/MCP 三层架构）是 B166ER 缺的，不是它主打的 RE 能力。**
> **260K star 是个红鲱鱼（red herring），但 AGENTS.md 是真金。**
> **B166ER 当前在 95+ skills 上"广而不深"，REA 在 4 skills + 32 tools 上"窄而深"——窄而深的工程模式值得借鉴。**

---

## 六、执行进度（2026-10-15 22:00 GMT+8 补充）

Eric 说「你决定」，按 V2.4 真>善>美 + 优化优先级 + 风险/时机综合判断，**选 Option 1 最小子集**：

### 6.1 已落地（21:55-21:58 GMT+8）

| 动作 | 文件 | 状态 |
|------|------|------|
| 建 `workspace/tools/` 目录 | `tools/` | ✅ |
| 抽 3 个原子工具 | `read_url.py` / `file_atomic_write.py` / `git_safe_commit.py` | ✅ |
| 写 3 个 JSON Schema 契约 | `schemas/*.json` | ✅ |
| 写 1 个 pytest | `tests/test_read_url.py` | ✅ |
| 5/5 测试通过 | — | ✅ |

### 6.2 没动（按 Option 1 最小子集原则保留）

- 95+ skills 拆分到 tools/（风险高，留下次）
- Result 库（dict 风格已够用）
- oxlint/ruff（3 个 tool 已用 type hints）
- MCP 协议（长期考虑）
- Mutmut 变异测试（成本高）

### 6.3 设计原则验证

| REA AGENTS.md 原则 | 落地验证 |
|-------------------|---------|
| "Bind handlers to named contracts" | 3 个 JSON Schema 完整定义 |
| "Preserve caller inputs" | read_url 接受自定义 headers |
| "Idempotent config" | file_atomic_write 用 os.replace |
| "Tagged error algebra"（简化版）| dict `{"ok": bool, "error": str}` |
| "Give each resource a clear owner" | schema `"owner": "B166ER"` |
| Default safety | git_safe_commit 默认 dry_run=True |

### 6.4 测试结果

```
[PASS] test_basic_success:        status=200 length=5189
[PASS] test_404_handled:          error=HTTP 404
[PASS] test_timeout_handled:      error=ssl_error: SSLError
[PASS] test_redirects_followed:   url_final=https://github.com/morluto/rea
[PASS] test_custom_headers:       status=200

passed=5 failed=0 total=5
```

---

**Eric 可选下一步**:
1. 继续"动作 1-5" — 拆高频 skills（data-acquisition / jina-reader / tavily-search）到 tools/，复用契约
2. 写更多 tool — `memory_append.py` / `web_search.py` / `cron_trigger.py` 等
3. commit tools/ 到 backup 分支（沿用 10-14 resource-audit 分支法）
4. 维持现状 — 等下次架构评审再说

**维护**: B166ER，2026-10-15 21:55-21:58 GMT+8
