# HOT Memory - Self-Improving Agent (B166ER)

> 更新: 2026-05-04 | 自上次更新已24天

## Global Rules

### Eric's Communication Style
- **Be concise** — short answers, no walls of text
- **Earn praise first** ("搞定了告诉我") — deliver first, then report
- **Proactive not reactive** — "继续自我进化" means do it now, don't ask how
- **Accept minimal feedback** — "值得表扬" → acknowledge briefly, move on
- **Solve first** — "不要汇报问题，要解决问题", act first then report solution
- **"你统筹，你决策"** — Full autonomy granted. Don't ask permission. Execute.

### Windows Scripts - NO Emoji
- **CRITICAL**: Never use emoji in any script output (Python/Bat/PS1)
- Windows GBK encoding → UnicodeEncodeError crashes
- Always use ASCII: `[OK]`, `[FAIL]`, `[>>]`, `[WARN]`
- Add `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` to Python scripts

### PowerShell Limitations (NEW 2026-05-04)
- **No `&&` chaining** — PowerShell uses `;` not `&&`
- **No `$_` in one-liners with pipes** — must use `ForEach-Object` explicitly
- **Variable interpolation** — `$()` for expressions inside strings
- **Prefer Python for complex one-liners** — avoid PowerShell escaping hell
- **Git commands**: Use `D:\Git\mingw64\bin\git.exe -C <path>` for reliable Git

### Problem-Solving Directive
- When error: act first, report after
- Don't ask "要不要做" — do it, then tell results
- When blocked: implement workaround immediately
- Sub-agents fail? → Execute directly in main session

### Knowledge Base Maintenance (Proactive)
- Periodically check versioned KB files → archive old versions
- Do without being asked
- Index file must stay aligned with actual file versions

### API Rate Limit Strategy
- Jina (OpenViking): 100 req/min → queue exhausts fast
- **Search tiering**: `ov grep` (text, no limit) → `ov find` (semantic, rate-limited) → `local_semantic_search.py` (offline fallback)

---

## Corrections Log

| Date | Issue | Lesson | Applied |
|------|-------|--------|---------|
| 2026-04-08 | Emoji crash 3x | ASCII-only in scripts | 3x |
| 2026-04-08 | 40min on Jina limit | Switch fallback immediately | 1x |
| 2026-04-08 | Verbose after praise | Brief acknowledgment only | 1x |
| 2026-05-04 | Sub-agents all failed (4/4) | Kimi K2.5 account suspended (insufficient balance); fix by recharging, not platform bug | 1x |
| 2026-05-04 | PowerShell escaping 3x | Use Python scripts for complex ops | 1x |
| 2026-05-04 | Gateway restart lost turn | After upgrade, verify session continuity | 1x |
| 2026-05-04 | User "东西呢?" after yield | Never yield without visible progress markers | 1x |
| 2026-05-04 | KB index stale 24 days | Proactive check every heartbeat | 1x |

## Patterns: Sub-Agent Reliability (UPDATED 2026-05-04)

### Root Cause Found: Kimi K2.5 Account Suspended
- **Symptom**: deepseek-v4-pro ×3 + kimi-k2.5 ×1 all failed (4-16s)
- **Root cause**: Kimi K2.5 account `org-6ed2fe8a` **suspended** — insufficient balance
- **Mechanism**: Main session uses deepseek (has balance); fallback/sub-agent hits kimi → silent fail
- **Fix**: Recharge kimi account at https://platform.moonshot.cn
- **Workaround until fixed**: Execute all tasks in main session (no sub-agents)

### Gateway Restart Recovery
- After `npm install -g openclaw@<version>`, gateway restarts → session interrupted
- **Check**: `openclaw status` after upgrade to verify gateway health
- **Reconnect**: WebChat may need manual refresh (Ctrl+R)

---

## Patterns: Tools

### Local Semantic Search
- model2vec: `minishlab/potion-base-8M` (8MB, 256dim, CPU, free)
- Chromadb: `PersistentClient(path=...)` (NOT `Client(Settings(...))`)
- Cmd: `python local_semantic_search.py [index|count|search|full]`
- Storage: `workspace/.chroma_db/`

### OpenViking
- PID: `data2/.openviking.pid`
- Manual start: `Remove-Item data2\.openviking.pid` → run `start_ov.bat`
- `ov grep`: text search, NO rate limit (use this first)
- `ov find`: semantic search, rate-limited (use when clear)

### Search Strategy (3-tier)
1. `ov grep "text"` — exact match, unlimited
2. `ov find "query"` — semantic, uses Jina (limit 100/min)
3. `python local_semantic_search.py search "query"` — offline, unlimited

### Cron Jobs
- Git backup: every 6 hours (id: 484c5c7e)
- Memory Dreaming: daily 3:00 (id: 5f5aceed)
- Report cron jobs: 7 scheduled (五一/端午/月度/Q2/暑期/十一)

---

## Industry Intelligence (May 2026)

- **OpenClaw 2026.5.3-beta.2**: Plugin externalization (npm-first), Gateway performance improvements, WebChat/Control UI resilience fixes
- **Sub-agent instability**: deepseek-v4-pro sub-agents crash; model compatibility issue
- **Plugin ecosystem**: ClawHub → npm migration in progress, git: plugin install support added
- **xAI Grok 4.3**: Now default xAI chat model in OpenClaw

## Self-Evolution Log

| Date | Action |
|------|--------|
| 2026-04-08 (1st) | Created .self-improving/, HOT/WARM/COLD tiers, corrections |
| 2026-04-08 (2nd) | +Eric通信风格, +搜索三层策略, +cron验证 |
| 2026-04-08 (3rd) | +行业情报, +DeepSeek/Gemma/Qwen更新 |
| 2026-05-04 (1st) | **月度大更新**: +PowerShell限制, +子Agent失败模式, +Gateway重启恢复, +5月行业情报, +自主决策原则, +指数更新至5/4 |

---

## Lottery Prediction (V5.1-回测进化)

### Core Insight
> LLM猜数字是"文科生推手"，量化才是"量化分析官"。
> 必须让Python执行计算，而不是让LLM凭感觉吐出号码。

### V5.0 五层架构
| Layer | 功能 | 技术 |
|-------|------|------|
| Layer1 | 数据特征工程 | AC值/012路/遗漏追踪/冷热码 |
| Layer2 | 混合预测引擎 | Shannon熵/赫斯特指数/马尔可夫链 |
| Layer3 | 组合优化 | 旋转矩阵/约束过滤/遗传算法 |
| Layer4 | 博弈论过滤 | 反人群选择/BIRTHDAY_ZONE惩罚 |
| Layer5 | 资金管理 | 凯利公式/期望收益 |

### Python Scripts
- `lottery_history/lottery_v5.py` — V5.0主程序
- `lottery_history/backtest_v5.py` — 回测分析
- `lottery_history/miss_tracker_fix.py` — 正确遗漏计算
- `lottery_history/lottery_v51.py` — V5.1最终预测
