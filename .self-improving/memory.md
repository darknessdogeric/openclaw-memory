# HOT Memory - Self-Improving Agent (B166ER)

## Global Rules

### Eric's Communication Style
- **Be concise** — short answers, no walls of text
- **Earn praise first** ("搞定了告诉我") — deliver first, then report
- **Proactive not reactive** — "继续自我进化" means do it now, don't ask how
- **Accept minimal feedback** — "值得表扬" → acknowledge briefly, move on
- **Solve first** — "不要汇报问题，要解决问题", act first then report solution

### Windows Scripts - NO Emoji
- **CRITICAL**: Never use emoji in any script output (Python/Bat/PS1)
- Windows GBK encoding → UnicodeEncodeError crashes
- Always use ASCII: `[OK]`, `[FAIL]`, `[>>]`, `[WARN]`
- Add `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` to Python scripts

### Problem-Solving Directive
- When error: act first, report after
- Don't ask "要不要做" — do it, then tell results
- When blocked: implement workaround immediately

### Knowledge Base Maintenance (Proactive)
- Periodically check versioned KB files → archive old versions
- Do without being asked

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

---

## Patterns: Tools

### Local Semantic Search ✅
- model2vec: `minishlab/potion-base-8M` (8MB, 256dim, CPU, free)
- Chromadb: `PersistentClient(path=...)` (NOT `Client(Settings(...))`)
- Cmd: `python local_semantic_search.py [index|count|search|full]`
- Storage: `workspace/.chroma_db/`

### OpenViking ✅
- PID: `data2/.openviking.pid`
- Manual start: `Remove-Item data2\.openviking.pid` → run `start_ov.bat`
- `ov grep`: text search, NO rate limit (use this first)
- `ov find`: semantic search, rate-limited (use when clear)

### Search Strategy (3-tier)
1. `ov grep "text"` — exact match, unlimited
2. `ov find "query"` — semantic, uses Jina (limit 100/min)
3. `python local_semantic_search.py search "query"` — offline, unlimited

### Cron Jobs
- Git backup: every 6 hours
- Data acquisition: 8:00 and 20:00 daily
- Check: `openclaw cron list` (may hang — try `openclaw status` instead)

---

## Industry Intelligence (April 2026)

- **DeepSeek V4 on Huawei chips** — China AI decoupling from Nvidia accelerating
- **Gemma 4 / Qwen 3 / Llama 4** — Open models getting very capable, good for AHL integration
- **Nvidia Agent Platform** — Enterprise AI agent wave, aligns with AHL direction
- **Energy crisis** — AI cos building gas plants for data centers, constraint approaching
- **Prompt injection** — Top security threat in deployed LLM systems

## Self-Evolution Log

| Date | Action |
|------|--------|
| 2026-04-08 (1st) | Created .self-improving/, HOT/WARM/COLD tiers, corrections |
| 2026-04-08 (2nd) | +Eric通信风格, +搜索三层策略, +cron验证 |
| 2026-04-08 (3rd) | +行业情报(April 2026), +DeepSeek/Gemma/Qwen更新, +能源/安全趋势 |
| 2026-04-08 (4th) | +博弈论过滤层彩票V4.2, +彩票宝典.docx, +SOP更新 |
| 2026-04-08 (5th) | **+V5.0 Gemini量化重构**: lottery_v5.py(五层架构), 信息论+马尔可夫+凯利公式 |
| 2026-04-08 (6th) | **+V5.1回测发现**: MissTracker修正, 极冷号20(29期), 热号策略20%命中率, 改为热号托底+极冷反弹策略 |

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

### Key Metrics (Current)
- 赫斯特指数: ~0 (强均值回归, 和值趋向84)
- **前区极冷: 20(29期), 31(17期), 1(16期), 23(16期), 14(15期)**
- **后区大遗漏: 4(15期), 6(14期), 9(12期), 3(11期)**
- 前区最热: 26(9次), 3(8次), 5(7次)
- 热号策略回测命中率: 仅20%

### V5.1 Strategy: 热号托底 + 极冷反弹
| 策略 | 原理 |
|------|------|
| 热号26托底 | 30期出现9次，必然延续 |
| 极冷20/31反弹 | 20号29期未出，统计必然回归 |
| 后区4/6/9大遗漏 | 遗漏超10期，跟踪 |
| 博弈论过滤 | 避开生日区(01-12) |

### Python Scripts
- `lottery_history/lottery_v5.py` — V5.0主程序
- `lottery_history/backtest_v5.py` — 回测分析
- `lottery_history/miss_tracker_fix.py` — 正确遗漏计算
- `lottery_history/lottery_v51.py` — V5.1最终预测

### Output Files
- `lottery_history/prediction_26037_v51.json` — V5.1最终预测 |
