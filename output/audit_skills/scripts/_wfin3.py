# -*- coding: utf-8 -*-
import io, sys, os, re, glob, shutil, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HOME = os.path.expanduser("~")
ROOT = r"D:\B166ER-openclaw\workspace"
D = os.path.join(HOME, "self-improving")
OUT = os.path.join(ROOT, "output", "infra_experience")
DESK = os.path.join(HOME, "Desktop", "认知拓扑_朋友圈图")
os.makedirs(DESK, exist_ok=True)

# ---------- 1. 交付 ----------
files = ["self_evolution_topology_9x16.png", "self_evolution_topology_9x16.html",
         "self_evolution_topology_v1.png", "self_evolution_topology_v1.html"]
print("=== 交付到桌面 认知拓扑_朋友圈图/ ===")
for f in files:
    s = os.path.join(OUT, f)
    if not os.path.exists(s):
        print("   ★ 缺", f); continue
    shutil.copy2(s, os.path.join(DESK, f))
    print("   %9d B  %s" % (os.path.getsize(os.path.join(DESK,f)), f))
# 缩略图清理
th = os.path.join(OUT, "_th9x16.png")
if os.path.exists(th): os.remove(th)

# ---------- 2. corrections：信息图三层质检 ----------
cp = os.path.join(D, "corrections.md")
ct = open(cp, encoding="utf-8", errors="replace").read()
ADD = """

---

## 2026-11-17 · ★★ 信息图质检必须三层 —— 程序化体检过了，图仍然可能是错的

**背景**：做「自我进化信息拓扑图」（9:16 手机版）。

**错在哪**：第一版跑完程序化体检，我看到「溢出 0 / 越界 0 / 裁切 0」就以为没问题。**但那个体检只查了 HTML 盒模型，完全没查 SVG 内部。** 补上 SVG 元素级检测后，抓出：

| 缺陷 | 程序化体检是否报 | 视觉核验是否报 |
|---|---|---|
| 3 处 SVG 文字重叠（边标压在节点文字上）| ❌ 不报（都在各自元素盒内）| ✅ 报 |
| 1 处 SVG 文本越出 viewBox 边界 | ❌ 不报 | ✅ 报 |
| **226px 垂直死白**（卡片底 1620 → 页脚 1846）| ❌ 不报 | ✅ 报 |
| 连线语义错误（边标压在竖箭头上、重复标注）| ❌ 不报 | ✅ 报 |

**根因**：★ **"程序化体检通过"被我自己当成了"视觉正确"的证据 —— 这正是我今天批评 naive self-critique 的同一个病（读起来通顺 ≠ 真对）。**

**规则（已落 `domains/代码与工具链.md`）**：
1. **信息图/拓扑图必须过三层质检**：
   - **L1 盒模型**：溢出 / 越界 / 裁切（已有）
   - **L2 SVG 元素级**：**文本两两包围盒重叠** ＋ **文本越出 viewBox** ＋ **死白区检测**（版块间最大空隙）
   - **L3 视觉核验**：缩略图看连线语义、标签压线、信息层级
2. **★ 体检脚本要按输出类型分**：HTML 与 SVG 的检查项不同，**不能拿 HTML 的检查覆盖 SVG**。
3. **★ 死白也算缺陷** —— 手机竖版上每一行都是稀缺资源。
4. **★ 修法优先改版面逻辑，不是挪字**：删重复标注、把边标移到"节点之间的空带"、加高 SVG 把间距拉开。挪字只会把冲突推到别处。
"""
if "信息图质检必须三层" not in ct:
    ct = ct.rstrip() + ADD
    with open(cp, "w", encoding="utf-8", newline="\n") as f: f.write(ct)
print()
print("corrections.md:", os.path.getsize(cp), "B | 今日条目", len(re.findall(r"^## 2026-11-17", ct, re.M)))

# ---------- 3. domains/代码与工具链.md 追加质检三层 ----------
dp = os.path.join(D, "domains", "代码与工具链.md")
dt = open(dp, encoding="utf-8", errors="replace").read()
DADD = """
## 8. 信息图 / 拓扑图质检必须三层

**★ 教训来源**：2026-11-17 自我进化信息拓扑图（9:16）—— 第一版程序化体检"溢出 0 / 越界 0 / 裁切 0"全过，但补上 SVG 元素级检测后抓出 3 处文字重叠、1 处越出 viewBox、226px 死白。

| 层 | 查什么 | 工具 |
|---|---|---|
| **L1 盒模型** | 溢出 / 越界 / 裁切 | `getBoundingClientRect` + scrollHeight |
| **L2 SVG 元素级** | ★ **文本两两包围盒重叠**、★ **文本越出 viewBox**、★ **版块间死白** | 两两相交判定 + viewBox 边界 + 版块间距 |
| **L3 视觉核验** | 连线语义、标签压线、信息层级、可读性 | 缩略图目视 |

**纪律**：
1. **★ 体检脚本按输出类型分**：HTML 与 SVG 检查项不同，**不能拿 HTML 的检查覆盖 SVG**。
2. **★ 死白也算缺陷** —— 手机竖版每一行都是稀缺资源；卡片底到页脚的空隙 > 120px 即为版式缺陷。
3. **★ 修法优先改版面逻辑**：删重复标注 → 边标移到节点间空带 → 加高 SVG 拉开间距 → 最后才挪字。
4. **★ 手机版字号基准**：1080 宽图在 390pt 手机上缩到 **0.36 倍** —— 正文不得 < 15px（等效 5.4pt 不可读）；关键数字与标题需 ≥ 20px。
"""
if "信息图 / 拓扑图质检必须三层" not in dt:
    dt = dt.rstrip() + "\n" + DADD
    with open(dp, "w", encoding="utf-8", newline="\n") as f: f.write(dt)
print("domains/代码与工具链.md:", os.path.getsize(dp), "B")

# ---------- 4. index.md 重生成 ----------
rt = open(os.path.join(D,"rules.md"), encoding="utf-8", errors="replace").read()
defs = set(re.findall(r"^#{1,4}\s*(R\d{2,4})\b", rt, re.M))
allref = set(re.findall(r"\b(R\d{2,4})\b", rt))
defs_map = {}
for f in glob.glob(os.path.join(D,"rules","*.md")):
    m = re.match(r"R(\d{2,4})", os.path.basename(f))
    if m: defs_map["R"+m.group(1)] = os.path.basename(f)
ghost = allref - defs
resolved = {g: defs_map[g] for g in ghost if g in defs_map}
undefined = sorted(ghost - set(defs_map), key=lambda x:int(x[1:]))
def lf(sub):
    out = []
    for f in sorted(glob.glob(os.path.join(D,sub,"**","*"), recursive=True)):
        if not os.path.isfile(f): continue
        rel = os.path.relpath(f, D).replace(os.sep,"/")
        if "_backup_" in rel: continue
        t = open(f, encoding="utf-8", errors="replace").read()
        ttl = next((l.lstrip("# ").strip() for l in t.split("\n") if l.startswith("#")), "")
        out.append((rel, os.path.getsize(f), ttl[:48]))
    return out
dom = lf("domains"); prj = lf("projects")
topics = []
for f in sorted(glob.glob(os.path.join(D,"rules_*.md"))):
    t = open(f, encoding="utf-8", errors="replace").read()
    ttl = next((l.lstrip("# ").strip() for l in t.split("\n") if l.startswith("#")), "")
    topics.append(("rules_"+os.path.basename(f)[6:], os.path.getsize(f), ttl[:48]))
nf = lambda s: len([f for f in glob.glob(os.path.join(D,s,"**","*"), recursive=True) if os.path.isfile(f)])
ct2 = open(cp, encoding="utf-8", errors="replace").read()
hm = open(os.path.join(D,"memory.md"), encoding="utf-8", errors="replace").read()
ej = json.load(open(os.path.join(D,"eval","encoding_baseline_2026-11-17.json"), encoding="utf-8")) if False else None
IDX = """# B166ER 自进化记忆 · 实时索引 v3.6

> **由正文程序生成（2026-11-17 第四轮收口），不手写维护。** 规则正文 `rules.md`｜逐条规则 `rules/`｜专题 `rules_*.md`｜纠错日志 `corrections.md`
> **正本唯一**：`~/self-improving/`（三个副本已于 2026-11-17 全部删除，见 `CANONICAL.md`）｜**分层定义**：`skills/self-improving/SKILL.md` v1.2.9

---

## 状态看板（2026-11-17 实测）

| 指标 | 值 |
|---|---|
| HOT `memory.md` | **{hl} 行 / {hc} 字符**（上限 100 行）｜含 R-断言 / R-读回 |
| WARM `domains/` | **{nd}** ｜ `projects/` | **{np}** ｜ `rules/` | **{nrule}** ｜ `archive/` | **{na}** ｜ `eval/` | **{ne}** |
| 专题 `rules_*.md` | **{ntop}** 份（含 R-AUTO-01～14 自动化踩坑）|
| `rules.md` | {rs} B / {rc} 字符 / 纯 UTF-8 ｜ 标题级定义 **{rn}** 条 ｜ 引用 {ra} 个 R 号 |
| `corrections.md` | {cs} 字符 / {cl} 行 ｜ **2026-11-17 单日补登 {ncorr} 条** |
| **执行器** | `toolbox/selfcheck.py` **12 断言**｜`skill_router.py`｜`fix_mixed_encoding.py`｜`evolution_scan.py`｜`evolution_watch.py`｜`evolution_watch_trigger2.js`｜`evolution_scan_payload.js` |
| **自动化** | **B166ER-自进化扫描**（每周一 09:00，`script` 负载不调模型）＋ **B166ER-自进化缺席告警**（每日 08:30，`trigger` 零子进程 ＋ `agentTurn`）→ **eval 从 56 天空档恢复为制度保证** |
| **交付物** | `self_evolution_topology_9x16.png`（2160×3840 手机竖版）＋ `self_evolution_topology_v1.png`（2160×2880 3:4 版）→ 桌面 `认知拓扑_朋友圈图/` |

---

## ★ 幽灵引用登记（正本引用但未内联定义）

**背景**：正本 `rules.md` 内联定义 {rn} 条，却引用 {ra} 个 R 号 → **{nghost} 个幽灵引用**。2026-11-17 全域比对：

- **已由 `rules/` 逐条文件补齐 {nres} 个**：
{resolved}
- **★ 全域确认无定义（真孤儿）{nund} 个** —— 保留引用作为历史痕迹，**不臆造正文**：
{undefined}

---

## 三层加载规则

| 层 | 位置 | 何时加载 | 写入时机 |
|---|---|---|---|
| **HOT** | `memory.md` | **常驻**（每次会话）| 只放今天仍成立的事实；易失效事实迁 `archive/` |
| **WARM** | `domains/` · `projects/` · `rules/` | 任务匹配时 | 同一主题第 2 次出现 → 建域级文件；**规则正文写 `rules/Rxxx.md`** |
| **COLD** | `archive/` | 显式查询 | 失效条目、历史备份、评估 JSON、已删副本保全 |
| **执行器** | `toolbox/selfcheck.py` 等 | 交付前强制 | **不存内容，只执行断言** |

---

## HOT 层当前条目（`memory.md`，常驻）

- **Preferences**：沟通零委婉／先给逻辑；文档中文优先+给 explorer 命令；执行先做后问；自进化须落成可检索规则；给选项不给单解
- **Patterns**：先扫本地资产再设计框架；信源分层+四档置信度；OCR 优先且专名交叉核；**程序化体检是下限、视觉核验不可省**；改公式先反推口径并用原件验证
- **Rules**：R-公文／R-工具／R-自检／**R-断言**／**R-读回**／**R-发布**／**R-榜单**／R-口径／**R-编码**／R-工具探底／R-子任务

---

## WARM · 域级文件（`domains/`）

{doms}

## WARM · 项目级文件（`projects/`）

{prjs}

## WARM · 专题规则文件（`rules_*.md`）

{topics}

---

## R 体系

- 标题级唯一编号 **{rn}**（最高 R{maxid}）；全文交叉引用 {ra} 个
- 逐条规则正文：`rules/`（{nrule} 份）
- 分层：L0 宪法 / L1 元规则 / L2 工作流 / L3 情境
- ★ **2026-11-17 新增**：`rules.md` 末尾「R-AUTO 专题索引」把 R-AUTO-01～14 挂进主文件 —— **此前 14 条规则不在会被看到的位置，因此当天被逐条重犯**

---

## 纠错日志（`corrections.md`）

- 格式：`## YYYY-MM-DD · 标题` → 错在哪 / 根因 / 代价 / 规则
- 最近日期：{recent}

---

## 体检清单（每季度执行一次）

1. `domains/` `projects/` `rules/` 是否仍非空？
2. index 的 R 编号数是否等于 `rules.md` **标题级**实际唯一编号数？
3. `memory.md` 是否含已过期事实？
4. 近一月纠错是否已按域归入 `domains/`？
5. **★ 是否存在第二个自进化目录？**（应恒为 0）
6. **★ 全域 .md 是否纯 UTF-8？**（相对 `eval/encoding_baseline` 比对，只报新增）
7. **★ `selfcheck.py` 12 条断言是否仍全绿？**
8. **★ eval 是否恢复周期运行？**（查 `eval/` 最近一份扫描记录日期）
9. **★ 建完 automation 是否回读过 `deliveryPreview`？**（出现 `no route` = 产出你看不到）
10. **★ 信息图是否过了三层质检？**（盒模型 / SVG 元素级 / 视觉核验）

---

*索引由正文自动生成 · 2026-11-17 · 分层可用性优先于条目数量*
"""
IDX = IDX.format(hl=hm.count("\n")+1, hc=len(hm), nd=len(dom), np=len(prj),
  nrule=len(glob.glob(os.path.join(D,"rules","*.md"))), na=nf("archive"), ne=nf("eval"), ntop=len(topics),
  rs=os.path.getsize(os.path.join(D,"rules.md")), rc=len(rt), rn=len(defs),
  maxid=max(int(x[1:]) for x in defs if x[1:].isdigit()), ra=len(allref),
  cs=len(ct2), cl=ct2.count("\n")+1, ncorr=len(re.findall(r"^## 2026-11-17", ct2, re.M)),
  nghost=len(ghost), nres=len(resolved), nund=len(undefined),
  resolved="\n".join("  - `%s` → `rules/%s`" % (g,v) for g,v in sorted(resolved.items(), key=lambda x:int(x[0][1:]))),
  undefined="  - " + ", ".join(undefined),
  doms="\n".join("| `%s` | %d B | %s |" % r for r in dom),
  prjs="\n".join("| `%s` | %d B | %s |" % r for r in prj),
  topics="\n".join("| `%s` | %d B | %s |" % r for r in topics),
  recent=" · ".join(sorted(set(re.findall(r"^##\s*(\d{4}-\d{2}-\d{2})", ct2, re.M)))[-8:]))
print("index.md:", len(IDX), "chars")

# ---------- 5. 今日日记 ----------
dp = os.path.join(ROOT, "memory", "2026-11-17.md")
note = """
### 2026-11-17 第四轮 · 自我进化信息拓扑图（9:16 手机版）

- **触发**：Eric「把你自我进化做成一张信息拓扑图」→「9:16的手机图」
- **★ 拓扑设计逻辑**：不画"我有哪些文件"，画**「信息怎么流、在哪断了」**。主体＝四层记忆（HOT/WARM/COLD ＋ ★执行器层）＋ 两条自动化链（产出链/告警链）＋ 终点「Eric 看得见」；**两条回流边**（执行器→HOT 当场改／COLD→HOT 3次重复升回）＋ **一条红色虚线断边**（告警链→Eric，56天空档）**与修复后的金色实线并置** → 一眼看出"这条边曾经是断的，今天接上了"。**这是把"故障史"画出来，不是功能清单。**
- **★ 9:16 的硬约束（已算清）**：1080 宽图在手机全屏 390pt 视口下缩到 **0.36 倍** → 正文不得 < 15px（等效 5.4pt 不可读）。故字号整体上调（SVG 正文 12.5→16.5px、标题 43→53px、节点 16.5→22px），并把纵向空间让给**「断链与闭合」时间轴**（09-22 最后一次 eval → 10-26 才发现缺席一个月 → 11-17 体检两链建成 → 此后每周扫描·每日探测）
- **交付**：`self_evolution_topology_9x16.png`（**2160×3840**，手机竖版）＋ `self_evolution_topology_v1.png`（2160×2880 3:4 版）＋ 两份 HTML → 桌面 `认知拓扑_朋友圈图/`
- **★ 本轮又暴露一个变体病（新规则已落）**：**"程序化体检通过"被我自己当成了"视觉正确"的证据** —— 第一版体检「溢出0/越界0/裁切0」全过，但补 **SVG 元素级检测**（文本两两包围盒重叠 / 文本越出 viewBox / 版块间死白）后抓出 **3 处文字重叠 + 1 处越界 + 226px 死白**。**这正是我今天批评 naive self-critique 的同一个病：读起来通顺 ≠ 真对。**
- **★ 新规则（`domains/代码与工具链.md` §8）**：信息图质检必须三层 —— **L1 盒模型 / L2 SVG 元素级 / L3 视觉核验**；体检脚本按输出类型分（**不能拿 HTML 的检查覆盖 SVG**）；**死白也算缺陷**（手机竖版每行都稀缺）；修法优先改版面逻辑而非挪字。
"""
cur = open(dp, encoding="utf-8", errors="replace").read() if os.path.exists(dp) else ""
if "第四轮 · 自我进化信息拓扑图" not in cur:
    with open(dp, "a", encoding="utf-8", newline="\n") as f: f.write(note)
print("日记:", os.path.getsize(dp), "B")
