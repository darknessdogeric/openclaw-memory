# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, shutil, tempfile, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
SI = os.path.join(HOME,"self-improving")
def jwrite(p,o):
    d=os.path.dirname(p); os.makedirs(d,exist_ok=True)
    fd,t=tempfile.mkstemp(dir=d,suffix=".tmp")
    with os.fdopen(fd,"w",encoding="utf-8") as f: json.dump(o,f,ensure_ascii=False,indent=1)
    os.replace(t,p)

# ============ 1. corrections.md 追加（排版器改动 + 检查器假阴性） ============
CP = os.path.join(SI,"corrections.md")
c = open(CP, encoding="utf-8", errors="replace").read()
ENTRY = """

## 2026-11-18 · 报告回读校验：排版器缺列表分支 ＋ 检查器漏取表格

**症状**：审计报告 Word 回读，Markdown 残留检出 3 段（`- ` 列表标记留在正文里），同时关键数字 "134" 报缺失——但该数字明明在表格里。

**Bug 1｜排版器 `toolbox/md2docx.py` 没有列表分支（真缺陷）**
- 根因：分支链只处理 `### `／`## `／`# `／`> `／`*强调*`，**`- ` 开头的行落到兜底分支，原样当普通段落输出** → 公文范式要求"列表为纯文字段落、无项目符号"
- 正解：**★ 排版器必须有列表分支**：剥符号 ＋ 缩进 2 字符 ＋ 纯文字段落（不生成项目符号、不生成编号）
- ★ 这类缺陷只有**回读校验**能抓到，程序化体检看不出来

**Bug 2｜我的检查器漏取表格文本（假阴性）**
- 根因：`alltxt = "\\n".join(ps)` **只取段落**、不取表格单元格；而关键数字大多写在表里 → **报"缺失"是假的**
- 正解：**★ 回读取文本必须"正文段落 ＋ 全部表格单元格"合并**，否则校验器自己在骗我
- ★★ 这是今天**第三次**同款病：① 把嵌套副本数成独立技能 ② 特征正则漏认正本实现 ③ 检查器不取表格。**共同病根不变：先怀疑检查器 → 修检查器 → 再看结论。**

**★ 通用规则**：**渲染管线要回读校验，检查器本身也要回读校验（拿已知真值测它）。** 一个只测渲染结果、却用假阴性检查器把关的流程，等于没关。
"""
if "2026-11-18 · 报告回读校验" not in c:
    open(CP,"w",encoding="utf-8",newline="\n").write(c.rstrip()+ENTRY+"\n")
print("✔ corrections.md 已追加 → %d B" % os.path.getsize(CP))

# ============ 2. domains/代码与工具链.md 追加（排版器改动） ============
DP = os.path.join(SI,"domains","代码与工具链.md")
d = open(DP, encoding="utf-8", errors="replace").read()
DADD = """

### 排版器 `toolbox/md2docx.py`（研判报告版式）· 2026-11-18

- 补 **列表分支**：`- `／`• ` 开头行 → 剥符号 ＋ 缩进 2 字符 ＋ 纯文字段落（公文范式：列表无项目符号）
- 用法：`python toolbox/md2docx.py <in.md> <out.docx> [--title T] [--subtitle S]`；支持表格／分隔线／多级标题／内联加粗／引用块
- ★ 字体（已核实本机全在）：宋体（正文 10.5pt）、黑体（标题）、楷体（副标题）、等线；缺字体须如实声明，不得擅自替换
- ★ **回读校验六项必查**：Markdown 残留（全文数 `*` 与 `#`，含表格）／emoji／骨架序列／关键数字（正文＋表格全量取文本）／分隔行是否误入数据行／列表符号残留
"""
if "排版器 `toolbox/md2docx.py`（研判报告版式）" not in d:
    open(DP,"w",encoding="utf-8",newline="\n").write(d.rstrip()+DADD+"\n")
print("✔ domains/代码与工具链.md 已追加 → %d B" % os.path.getsize(DP))

# ============ 3. MEMORY.md 追加 ============
MM = os.path.join(ROOT,"MEMORY.md")
m = open(MM, encoding="utf-8", errors="replace").read()
MADD = """
## ★★★ 技能库与范式库深度审计（2026-11-18）· 从「有工具不用」到「命中即用」

- **★ 一句话结论**：**库里有 ≠ 能路由到 ≠ 会被调用** —— 这是三件事，过去被当成一件，于是"装备完善"的假结论与"每次重新造轮子"的真症状同时存在。
- **★ 活证据（我自己）**：`skills/docx-md-bridge/scripts/md_to_docx.py` 一直可用且完全正常，我当天却绕过它手搓第 9 个 md→docx 变体；**更讽刺：我在新变体里修的"表格被吞"缺陷，正本里根本不存在**（实测两轮子输出完全一致：6 段 1 表 3 行）——**在自己造的轮子里修一个不存在的问题**。
- **★ 审计结果**：物理 `SKILL.md` 271 份 / 去重 185 命名 / **79 组同名**（其中 76 组仅 CRLF 差异，真冲突仅 3 组且实为嵌套副本）→ **按祖先判据的真实技能数 150**（`workspace/skills` 119 ／ `~/skills` 73 ／ `~/.claude/skills` 32）。**编码损损 0**；**无 description 8 个 → 已补 0**；**跨技能路径错引 11 处 → 已修 0**。
- **★ 三个正本（程序生成，勿手改）**：`output/audit_skills/SKILL_REGISTRY.json`（150 技能，含 status 活跃/待装/受保护）｜`WORKFLOWS.json`（**25 条**「任务→技能→范式→依据」）｜`PARADIGM_REGISTRY.json`（**150 条**范式，全部带触发词）｜`TOOL_INDEX.json`（698 工具）｜`GITHUB_INSTALL_LEDGER.json`（3 条安装：来源/MIT/commit/回滚）。
- **★ 范式库同款病**：150 条范式里原有 **143 条无「何时用」**＝有范式但调不出来 → 已补关键词（显式 3 条 / 自动派生 147 条）。
- **★ GitHub 补装（只补已证实缺口）**：`openclaw/clawhub`（MIT，commit bf198e62）装 `writing-evals`(21 文件)／`autoreview`(1)／`technical-documentation`(13)；**`VoltAgent/awesome-openclaw-skills` 仅作缺口发现目录，未安装任何条目**。本机 `clawhub` CLI 不可用（配置库版本不兼容），走 GitHub 直连。
- **★ 闲置裁决 42 个**：归档 1（wayfinding-signage）／同族不拆散保留 5（ponytail 家族）／保留待装 28（**真缺只有 `arkcli` 与 `gstack`**）／纳入工作流激活 6。**★ pip 不在 PATH 但 `python -m pip` 可用（26.0.1）；brew 是 macOS 专属、本机 Windows → 平台不适用 ≠ 缺依赖**（按粗口径会误伤 19 个可用技能）。
- **★ 重复造轮子治理**：md→docx 16 套 → **1 正本（skills/docx-md-bridge）＋ 1 有分工变体（toolbox/md2docx.py，研判报告版式）**；旧克隆 6 件先合并唯一内容（编号列表＋分页标记）再归档至 `toolbox/_archive/legacy_docx_variants_2026-11-18/`。
- **★ 断言 12 → 19（C13–C19），19/19 全绿、退出码 0**：注册表存在且每个技能有 description／注册表不漂移／GitHub 装件有台账／md→docx 正本唯一／工作流表非空／归档不回潮／范式可路由且工作流绑定范式。
- **★ ★ 我今天犯的错（教训比结论值钱）**：① **绕过既有轮子造第 9 个变体**（判断错，最贵）② **检测器口径错连撞四次** —— 嵌套副本数成独立技能 / 特征正则漏认正本实现 / "目录域"命中"根目录"二字 / **检查器不取表格文本导致假阴性**（共同病根：把检测器的判断当事实的权威；正解永远是先怀疑检查器 → 修检查器 → 再看结论）③ `grep` 本机不存在（Windows）＋全盘扫描误入大目录超时 ④ 路径多退一层目录致整张"独有能力"表作废 ⑤ **差点把当日刚建的 4 个技能当"纯说明文档"归档**（判据只扫 `scripts/` 子目录，漏掉技能根目录下的可执行件）→ 已加**受保护集合 ＋ 家族不拆散规则**。
- **★ 调用纪律已写进 AGENTS.md 强制关卡**：动手前 `python toolbox/skill_router.py --task "…"`；自建前 `--check "…"`；**命中即用不得自建同类工具**；新工具三件事缺一不算完成（写 `skills/<name>/SKILL.md` 含触发词 ＋ 登记注册表 ＋ 加一条 selfcheck 断言）。
- **★ 交付**：`anyi-ops-kb/04_方法论/B166ER_技能库与范式库深度审计报告_v1.0_2026-11-18.md/.docx`（回读六项全过：Markdown 残留 0／emoji 0／骨架 10/10／关键数字 9/9／分隔行误入 0／列表符号残留 0）。
- **★ 尚未解决**：toolbox 仍有 **698 个非临时 .py ＋ 1229 个非 .py 文件**，工具层缺"每个工具归属哪个技能"的强制约束（下一段工作）；范式与工作流对齐仍偏粗（约 6 条匹配精度不高，需人工确认）；arkcli/gstack 26 个技能待装；ponytail 家族是否整体降级待定；注册表生成脚本尚未纳入技能层。
- **关联**：`output/audit_skills/`（注册表/工作流/范式/台账/闲置裁决/归档清单）｜`toolbox/skill_router.py`｜`toolbox/selfcheck.py`（19 条断言）｜`skills/docx-md-bridge/`｜`~/self-improving/corrections.md`｜`~/self-improving/domains/代码与工具链.md`
<!-- project: github.com/darknessdogeric/openclaw-memory -->
"""
if "技能库与范式库深度审计（2026-11-18）" not in m:
    open(MM,"w",encoding="utf-8",newline="\n").write(m.rstrip()+MADD+"\n")
print("✔ MEMORY.md 已追加 → %d B" % os.path.getsize(MM))

# ============ 4. 临时脚本归档（不删，移入 output/audit_skills/scripts/） ============
MDIR = os.path.join(ROOT,"memory")
SCR = os.path.join(ROOT,"output","audit_skills","scripts")
os.makedirs(SCR, exist_ok=True)
tmp = [p for p in glob.glob(os.path.join(MDIR,"_*.py"))]
moved=[]
for p in tmp:
    b = os.path.basename(p)
    if b in ("_md2d.py","_chk.py","_chk2.py","_fmt.py","_readskill.py"): continue  # 保留少量可复现取样脚本
    dst = os.path.join(SCR,b)
    if os.path.exists(dst): continue
    shutil.move(p,dst); moved.append(b)
print("✔ 临时脚本归档 %d 个 → output/audit_skills/scripts/（保留 %d 个可复现取样）" % (len(moved), len([p for p in glob.glob(os.path.join(MDIR,'_*.py'))])))

print()
print("="*100); print("最终自检"); print("="*100)
r = subprocess.run([sys.executable, os.path.join(ROOT,"toolbox","selfcheck.py")], capture_output=True, timeout=400)
print(r.stdout.decode("utf-8","replace"))
print("退出码:", r.returncode)
