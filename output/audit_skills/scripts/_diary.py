# -*- coding: utf-8 -*-
import io, sys, os, re, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
SI = os.path.join(HOME,"self-improving")
MD = os.path.join(ROOT,"memory","2026-11-18.md")

DIARY = """# 2026-11-18 日记

## 主题：技能库与范式库深度审计（承接 2026-11-17 自我进化重构）

### 一、这次做成了什么

**全量清点**：物理 `SKILL.md` 271 份 → 去重 185 命名 → **按真实技能边界（排除技能内部嵌套的 `examples/`、`variants/`）重算后为 134 个**。79 组"同名"里 76 组只是 CRLF/LF 差异，3 组"真冲突"实为嵌套副本误判。

**完整性修复**：8 个无 `description` 的技能（cad-batch-processing／cost-governor／hotel-feasibility-report／interior-fullplan／officecli／en／zh-CN／skill-vetter）已补可路由描述；11 处跨技能路径错引已指向真实所在（如 `ppt-visual-editor` 的 7 个配套件实际在 `ppt-deck-builder-pro`）。

**GitHub 补装**（只装已证实缺口，非堆叠）：`writing-evals`（21 文件）、`autoreview`（1 文件）、`technical-documentation`（13 文件），全部来自 `openclaw/clawhub`（MIT，commit bf198e62），台账见 `output/audit_skills/GITHUB_INSTALL_LEDGER.json`。

**固定工作流**：建 `SKILL_REGISTRY.json`（134 条）＋ `WORKFLOWS.json`（19 条）＋ `TOOL_INDEX.json`（698 个工具），并把 `toolbox/skill_router.py` 升级为注册表驱动（含 `--check` 自建前查重）。**路由已写进 AGENTS.md**，不再是纸面索引。

**同源治理**：md→docx 家族 16 套 → 正本 1 套（`skills/docx-md-bridge`）＋ 1 个有明确分工的研判报告变体（`toolbox/md2docx.py`）。旧克隆 6 件先合并唯一内容（编号列表、分页标记）再归档到 `toolbox/_archive/legacy_docx_variants_2026-11-18/`，留清单可回滚。

**断言**：selfcheck 从 12 条增至 **18 条**（C13–C18 新增），**18/18 全绿，退出码 0**。

### 二、我今天犯的错（写进日记，不写进日志）

**错 1（判断）：绕过既有轮子造第 9 个变体。**
`skills/docx-md-bridge/scripts/md_to_docx.py` 一直可用且完全正常，我今天却手搓 `toolbox/md2docx.py`。更讽刺的是：**我在新轮子里修的那个"表格被吞"bug，正本里根本不存在** —— 实测两个转换器输出完全一致（6 段／1 表 3 行）。我在自己造的轮子里修一个不存在的问题。
→ 这就是用户说的"有工具不用"的活证据。

**错 2（执行）：检测器口径错 → 结论错，连撞三次。**
① 把技能内部的 `examples/`、`variants/` 嵌套副本数成独立技能 → 185 虚高，实为 134
② 特征正则只认 `List Bullet`，没认正本自己的 `• ` 实现 → 误判"列表"是旧克隆独有
③ "目录域"命中的是 `print('1. 桌面根目录')` 里的"目录"二字 → 正本与克隆都没有真 TOC 域
**共同病根**：把检测器的判断当成了事实的权威。正确次序永远是：**先怀疑检查器 → 修检查器 → 再看结论**。

**错 3（执行）：grep 在 Windows 上不存在**（`WinError 2`），全盘扫描还把 anyi-ops-kb／.chroma_db 读进来拖到超时。改成纯 Python 定向扫描才拿到可信数据。

**错 4（路径）**：`ROOT\..\skills` 指向 `D:\\B166ER-openclaw\skills`（不存在），真实位置是 `ROOT\skills`。这个路径错让我把 docx-md-bridge 排除在能力并集之外，直接导致"独有能力"整张表是假的。

### 三、收尾三问

1. **今天有没有错？错在判断还是执行？** —— 四处错：**一处判断**（绕过既有轮子，判断错）、**三处执行**（检测器口径、工具不可用、路径错）。判断错最贵。
2. **有没有更好的做法？有没有更好的传感器？** —— 做法：**注册表驱动**（`SKILL_REGISTRY.json` 由程序生成，不手写不漂移）。传感器：新增 **C13–C18 六条断言** —— 注册表存在且每个技能有 description、注册表与磁盘不漂移、GitHub 安装有台账、md→docx 正本唯一、归档不回潮、工作流表非空。**纯文字不算进化。**
3. **有没有新规律？** —— **"库里有 ≠ 能路由到 ≠ 会被调用"是三件事。** 审计技能库必须同时查：存在、完整、可路由、被真实调用、形成工作流。只查文件数，必然得出"装备完善"的假结论。

### 四、明天接着做

- `toolbox` 根目录仍有 698 个非临时 .py ＋ 1229 个非 .py 文件 —— 工具层还没做完治理，缺"每个工具归属哪个技能"的强制约束
- 范式库（`anyi-ops-kb/04_方法论/`）已有报告范式／经营分析范式／方法论书籍内化／设计内化／配色／版式／服务设计，但**缺"技能—范式—工作流"三者对齐表**
- `~/skills` 是 `workspace/skills` 的 Junction（52/80 文件逐字节相同）—— 本质是同一套的第二个入口，仍算"同一技能出现在两处"，待确认是否应改为单一目录
"""
os.makedirs(os.path.dirname(MD), exist_ok=True)
open(MD,"w",encoding="utf-8",newline="\n").write(DIARY)
print("✔ 日记已写:", os.path.basename(MD), os.path.getsize(MD), "B")

# ---------- corrections.md 追加 ----------
CP = os.path.join(SI,"corrections.md")
c = open(CP, encoding="utf-8", errors="replace").read()
ENTRY = """

## 2026-11-18 · 技能库审计：库里有 ≠ 能路由到 ≠ 会被调用

**症状**：全量审计 271 份 SKILL.md / 134 个真实技能，79 组同名散在三处；而系统提示里的技能清单**被截断（115/155，藏了 40 个）**。路由靠"扫提示"→ 扫不全 → 技能存在但发现不了。

**★ 活证据（我自己的）**：`skills/docx-md-bridge/scripts/md_to_docx.py` 一直可用且完全正常，我今天却绕过它手搓 `toolbox/md2docx.py`（第 9 个变体）。**更讽刺：我在新轮子里修的"表格被吞"bug，正本里根本不存在** —— 实测两轮子输出完全一致（6 段／1 表 3 行）。**我在自己造的轮子里修一个不存在的问题。**

**正解**：
1. **注册表驱动**：`output/audit_skills/SKILL_REGISTRY.json`（程序生成，含 description／脚本数／三处位置）+ `WORKFLOWS.json`（19 条固定工作流）+ `TOOL_INDEX.json`（698 工具）
2. **路由写进 AGENTS.md**：动手前 `python toolbox/skill_router.py --task "..."`；自建前 `--check "<拟造名>"`
3. **description 必须含触发词**（用户会怎么说），不能只写功能 —— 这是路由能否命中的唯一依据
4. **新工具三件事缺一不算完成**：写 `skills/<name>/SKILL.md` ＋ 登记注册表 ＋ 加一条 selfcheck 断言

**★ 检测器口径错 → 结论错（今天连撞三次）**：
① 技能内部 `examples/`、`variants/` 嵌套副本被数成独立技能 → 185 虚高，实为 134
② 特征正则只认 `List Bullet`，没认正本自己的 `• ` 实现 → 误判"列表"为旧克隆独有
③ "目录域"命中的是 `print('1. 桌面根目录')` 里的"目录"二字 → 两者都没有真 TOC 域

**★★ 通用规则**：**先怀疑检查器 → 修检查器 → 再看结论。** 把检测器的判断当成事实的权威，就会为了保住一个错误结论去改口径 —— 这比漏检更危险。

**★★ 同源治理顺序不可颠倒**：先合并唯一内容 → 再归档 → 后删除；删除前留清单可回滚（本次归档 6 件 md→docx 旧克隆，先把编号列表与分页标记并入正本）。
"""
if "2026-11-18 · 技能库审计" not in c:
    open(CP,"w",encoding="utf-8",newline="\n").write(c.rstrip() + ENTRY + "\n")
print("✔ corrections.md 已追加 → %d B" % os.path.getsize(CP))

# ---------- 域级文件：代码与工具链 ----------
DP = os.path.join(SI,"domains","代码与工具链.md")
d = open(DP, encoding="utf-8", errors="replace").read()
DADD = """

## 技能与工具路由（2026-11-18）

**正本四件套**（程序生成，勿手改）：
- `output/audit_skills/SKILL_REGISTRY.json` —— 134 个技能，**以"真实技能边界"为准（排除技能内部嵌套的 `examples/`、`variants/`、`references/`）**
- `output/audit_skills/WORKFLOWS.json` —— 19 条固定工作流（任务 → 技能 → 依据）
- `output/audit_skills/TOOL_INDEX.json` —— 698 个工具，含 `skill_equivalent` 与边界说明
- `output/audit_skills/GITHUB_INSTALL_LEDGER.json` —— GitHub 安装台账（来源／MIT／commit／回滚）

**调用纪律**：动手前 `python toolbox/skill_router.py --task "..."`；自建前 `--check "<拟造名>"`。**命中即用，不得自建同类工具。**

**md→docx 正本唯一**：`skills/docx-md-bridge/scripts/md_to_docx.py`（通用）｜`skills/gongwen-docx-cn/scripts/md2docx_gongwen.py`（公文 GB/T 9704）｜`toolbox/md2docx.py`（研判报告版式）。旧克隆 6 件已归档至 `toolbox/_archive/legacy_docx_variants_2026-11-18/`。

**★ 教训**：**库里有 ≠ 能路由到 ≠ 会被调用**，这是三件事。审计必须同时查存在／完整／可路由／被真实调用／形成工作流五个层面 —— 只查文件数必然得出"装备完善"的假结论。
"""
if "技能与工具路由（2026-11-18）" not in d:
    open(DP,"w",encoding="utf-8",newline="\n").write(d.rstrip() + DADD + "\n")
print("✔ domains/代码与工具链.md 已更新 → %d B" % os.path.getsize(DP))
