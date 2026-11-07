# 技能市场扫描 2026-10-20（12:23 第二次运行）

> 本文件重写并修复了今日早前一次扫描的乱码（GBK 写入 UTF-8 造成）。
> 根因：PowerShell `Out-String` / `Set-Content` 未显式 `-Encoding utf8`。
> **规则**：以后所有 memory 写入走 `Write` 工具，不用 `>>` 重定向。

## 1. ClawHub 新技能搜索

`clawhub search ""` **报 `missing required argument 'query'`** —— 空查询不被接受，
无法做「全量新技能」扫描，只能做关键词定向搜索。这是长期限制，不是故障。

### hotel（酒店 · Eric 主战场）
| slug | 评分 | 评估 |
|------|------|------|
| hotel | 6120 | 泛化占位名，低价值 |
| hotel-lobby-ai-prompt-director | 5095 | 大堂 AI 提示词导演，**已在待 inspect 清单** |
| china-hotel-price-compare | 5095 | 酒店比价 v4.1.7，**已在待 inspect 清单** |
| rollinggo-hotel-skill-cn-new | 5095 | RollingGo 全球预订 v1.1.1，备用 |
| booking-com-hotel-data | 5095 | Booking.com 实时价/评论 API，**对存量翻新竞品调研有用** |

### AI agent
sales-ai-agent-starter / production-agent-builder / ai-agent-builder-zh /
emailautomationskill / agent-maker-2 —— 通用套壳，评分仅 1000 档，**无差异化价值，跳过**。

**本次无新增高价值技能。** hotel 赛道命中项全部已在累计待 inspect 清单中，无新面孔。

## 2. 已有技能 git 更新（本次实际执行了升级）

7 个技能带 `.git`：evolver / open-design-skill / ponytail / ppt-generator /
scholar-skill / wenjuan-survey / wewrite

| 技能 | 状态 | 本次动作 |
|------|------|----------|
| **wewrite** | **落后 141 commits** | ✅ **已 fast-forward 到 v4.2.1** |
| evolver | 76 落后 / 312 领先，MERGE_HEAD 存在 | ⛔ 冲突未解，未动 |
| ponytail | 0/0 已是最新 | tag 引用冲突属噪音，无实质更新 |
| open-design-skill / ppt-generator / scholar-skill | 0/0 已是最新 | 无需动作 |

### ⚠️ wewrite v4.2.1 是破坏性重构（184 文件，+6883 / −14969）

单体 skill 拆成 **10 个子技能**：
`wewrite` / `wewrite-write` / `wewrite-review` / `wewrite-rewrite` / `wewrite-visual` /
`wewrite-style` / `wewrite-topic` / `wewrite-stats` / `wewrite-publish` / `wewrite-learn`

同时 `scripts/` → `src/wewrite/` Python 包，`dist/openclaw/` 目录整体删除。

**已验证**：`openclaw skills check` 仍能发现 `wewrite`（递归发现机制生效），根目录
`SKILL.md` 虽被删除但技能未失效。**无需修复动作**，但注意引用路径若指向
`scripts/` 或 `dist/openclaw/` 会失效。

## 3. 阻塞项：evolver 合并冲突（需 Eric 手动）

`skills/evolver` 处于 **未完成的 merge 状态**（`.git/MERGE_HEAD` 存在）：
- `UU` 未合并文件 20+：`SKILL.md` / `README.md` / `index.js` / `package.json` / `src/gep/*`
- `AA` 双方新增：hubSearch.js / reflection.js / strategy.js / signalDistiller.js 等
- 分歧极大：本地 312 commits vs 远程 76 commits

**不能无人值守自动解**——冲突涉及 40+ 文件核心逻辑，自动 `ours/theirs` 可能毁掉本地演进。
建议：Eric 有空时 `git -C skills/evolver merge --abort` 后重新拉取，或决定以哪一侧为准。

## 4. 工具链问题（持续）

- `clawhub search` 不接受空 query → **无法自动发现「真正的新技能」**，只能关键词扫。
- `git pull` 在 tag 同名不同指向的仓库（ponytail/wewrite）会整体失败；
  解法：`git fetch --force --prune --tags` + `git merge --ff-only origin/main`（绕开 pull）。
- `skills/wenjuan-survey-skill/wenjuan-survey` 的 `git -C` **实际解析到了 workspace 主仓库**
  （ahead 27 / behind 9）。**绝对不能在 cron 里 merge/rebase**，否则污染主仓库。

---

_扫描者: B166ER | 触发: cron 332ec6e6 | 模型: minimax/MiniMax-M3 | 当日第 2 次扫描_
_实际变更: wewrite v→4.2.1（唯一执行成功的升级）_