# -*- coding: utf-8 -*-
"""_reg_pat.py - 纹样内化收口：登记注册表 / 入范式库 / 加断言 / 入册 / 终检"""
import io
import sys
import os
import re
import json
import glob
import ast
import shutil
import tempfile
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
SI = os.path.join(HOME, "self-improving")
AUD = os.path.join(ROOT, "output", "audit_skills")
KB4 = os.path.join(ROOT, "anyi-ops-kb", "04_方法论")
NOTE = os.path.join(KB4, "方法论书籍内化", "《纹样设计速查手册》核心内化笔记_v1.0_2026-11-19.md")
PY = sys.executable


def jwrite(p, o):
    d = os.path.dirname(p)
    os.makedirs(d, exist_ok=True)
    fd, t = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(o, f, ensure_ascii=False, indent=1)
    os.replace(t, p)


# ---------- 1. 内化笔记入范式库（它是范式，必须可被路由） ----------
P = json.load(open(os.path.join(AUD, "PARADIGM_REGISTRY.json"), encoding="utf-8"))
rel = "anyi-ops-kb/04_方法论/方法论书籍内化/《纹样设计速查手册》核心内化笔记_v1.0_2026-11-19.md"
if not any(x["file"] == rel for x in P):
    t = open(NOTE, encoding="utf-8").read()
    ttl = next((l.lstrip("# ").strip() for l in t.split("\n") if l.startswith("#")), "纹样设计速查手册")
    kw = ["纹样", "纹样选型", "纹样检索", "纹样编号", "传统纹样", "纹样设计", "纹样应用",
          "装饰纹", "团花", "缠枝", "卷草", "宝相花", "云纹", "水纹", "水涡", "朝代分期",
          "寓意", "文物出处", "溯源", "授权", "国潮纹样", "视觉系统", "布艺纹样", "文创纹样",
          "构图", "连续", "骨架词", "母题", "组合校验"]
    P.append({"src": "KB_04_方法论", "file": rel, "title": ttl[:80],
              "when": "触发：" + " / ".join(kw[:14]),
              "trigger_source": "explicit", "keywords": kw,
              "bytes": len(t.encode("utf-8"))})
    jwrite(os.path.join(AUD, "PARADIGM_REGISTRY.json"), P)
    print("1) 内化笔记已入范式库（%d 条）" % len(P))
else:
    print("1) 范式库已含该笔记")

# ---------- 2. 工作流新增（绑定范式） ----------
WFP = os.path.join(AUD, "WORKFLOWS.json")
W = json.load(open(WFP, encoding="utf-8"))
ADD = {"纹样选型与视觉系统": ("pattern-design-cn",
                            "★ 纹样选型／检索／组合校验；朝代一致＋寓意适配＋溯源可授权三约束")}
added = 0
for task, (sk, note) in ADD.items():
    if any(w["task"] == task for w in W):
        continue
    if sk not in [r["name"] for r in json.load(open(os.path.join(AUD, "SKILL_REGISTRY.json"), encoding="utf-8"))]:
        print("   ★ %s 尚未入注册表，先重建" % sk)
    W.append({"task": task, "skills": sk, "note": note,
              "paradigms": [rel], "source": "2026-11-19 纹样内化"})
    added += 1
    print("2) 工作流 + %s → %s" % (task, sk))
jwrite(WFP, W)
print("   工作流 %d 条" % len(W))

# ---------- 3. 重建技能注册表（收录 pattern-design-cn） ----------
r = subprocess.run([PY, os.path.join(ROOT, "skills", "skill-registry-builder", "scripts", "build_skill_registry.py")],
                   capture_output=True, timeout=300)
print("3) " + r.stdout.decode("utf-8", "replace").strip().replace("\n", " ｜ "))

# ---------- 4. 新增断言 C23（纹样底库可检索且技能在册） ----------
SC = os.path.join(ROOT, "toolbox", "selfcheck.py")
C23 = '''# ---------------- C23 纹样底库可检索（2026-11-19 纹样内化新增） ----------------
@check("C23", "纹样底库须存在、可检索、且技能已入注册表", "《纹样设计速查手册》内化后必须能被路由调用，否则等于没吸收")
def c23():
    idx = os.path.join(ROOT, "output", "book_纹样设计速查手册", "纹样索引.json")
    sk = os.path.join(ROOT, "skills", "pattern-design-cn", "SKILL.md")
    if not os.path.exists(idx):
        return False, "缺纹样索引", []
    if not os.path.exists(sk):
        return False, "缺 pattern-design-cn 技能", []
    try:
        P = json.load(open(idx, encoding="utf-8"))
    except Exception as e:
        return False, "索引解析失败 %s" % str(e)[:50], []
    n = len(P.get("index_meihua", [])) + len(P.get("numbered_4722198", []))
    if n < 100:
        return False, "底库条目仅 %d 条，覆盖不足" % n, []
    reg = os.path.join(ROOT, "output", "audit_skills", "SKILL_REGISTRY.json")
    if not os.path.exists(reg):
        return False, "缺技能注册表", []
    names = {x["name"] for x in json.load(open(reg, encoding="utf-8"))}
    if "pattern-design-cn" not in names:
        return False, "pattern-design-cn 未入注册表（路由不到）", []
    # 实跑检索器
    try:
        out = subprocess.run([sys.executable,
                              os.path.join(ROOT, "skills", "pattern-design-cn", "scripts", "pattern_index.py"),
                              "search", "水"], capture_output=True, timeout=90)
        o = out.stdout.decode("utf-8", "replace")
    except Exception as e:
        return False, "检索器执行失败 %s" % str(e)[:40], []
    if "命中" not in o:
        return False, "检索器无输出", []
    return True, "纹样底库 %d 条 ｜ 技能已入册 ｜ 检索器可执行" % n, []

'''
t = open(SC, encoding="utf-8", errors="replace").read()
if "C23" not in t:
    anchor = "def run(as_json=False):"
    t = t.replace(anchor, C23 + anchor, 1)
    ast.parse(t)
    open(SC, "w", encoding="utf-8", newline="\n").write(t)
    print("4) 已插入 C23")
else:
    print("4) C23 已存在")

# ---------- 5. 入册：corrections / domains / 日记 / MEMORY ----------
def append_once(path, marker, text):
    tt = open(path, encoding="utf-8", errors="replace").read()
    if marker in tt:
        return False
    open(path, "w", encoding="utf-8", newline="\n").write(tt.rstrip() + "\n" + text + "\n")
    return True


CORR = """

## 2026-11-19 · 书籍内化的正确起点：先确认书在不在，再决定能不能写

**症状**：Eric 指令「《纹样设计速查手册》这本书吸纳一下。全面吸收内化。」而**本机没有这本书**（扫描 679,398 个文件 + 13,621 个 WPS 云盘文件 + 全部接收目录 + 近 14 天新增，零命中）。

**★ Bug 1｜差点凭标题编内容**
- 风险：若直接写"内化笔记"，会凭空造出书的内容、寓意、文物出处 —— **那是伪造证据**
- 正解：**★ 先查书在不在 → 查它是不是公开出版物 → 取公开原文（官方书目/目录/出版社介绍）→ 明确标注哪层是源、哪层是我的推论、哪层未取得**

**★ Bug 2｜只做转述不算内化**
- 正解：**★ 内化 = 从真实数据里做分析，产出可推演的规则。** 本次从 503 条真实纹样名做构词法分析 → 得到「结构骨架 × 题材母题」的生成规则（结构词 20 ＋ 母题 30 即可自创合规纹样名）＋ 命名长度规律（5 字占 49%）＋ 寓意线索占比（27%）。**这才是数据才能支撑、书上没明说的增量。**

**★ Bug 3｜底库边界必须如实报告**
- 本次底库检索「葫芦」命中 **0 条** —— 已如实写进内化笔记与国堰选型清单（"需查原书，不得凭想象配"），**不拿"福禄纹"糊弄过去**

**★ Bug 4｜信源分层必须显式**
- 本次采用 **【源】/【判】/【问】** 三层标注，并如实记录 **3 处口径差异**：编辑推荐写"飞鸟纹"vs 权威目录"鸟纹"（以目录为准）／1200 多个 vs 1210 个（取保守）／团队 13 年 vs 14 年（取 13+）

**★ 通用规则**：**内化一本书的产出应该是「可检索的底库 ＋ 可执行的规则 ＋ 可落地的场景清单」三件套**，而不是一篇读后感。落到具体项目才叫内化 —— 本次直接产出了国堰纹样选型清单（编号级条目 0015/0017/0022）。
"""
print("5) corrections:", append_once(os.path.join(SI, "corrections.md"), "2026-11-19 · 书籍内化的正确起点", CORR))

DOM = """

### 纹样（《纹样设计速查手册》内化）· 2026-11-19

- **技能**：`skills/pattern-design-cn/`（SKILL.md ＋ `scripts/pattern_index.py` ＋ `data/`）—— 触发：纹样选型／检索／编号／组合校验
- **底库**：`output/book_纹样设计速查手册/纹样索引.json`（**503 条**：纹样之美目录 422 ＋ 速查手册编号表 81），含章、页码、原书编号
- **方法三约束**：**① 朝代一致 ② 寓意适配 ③ 溯源可授权**；顺序不可颠倒（先定朝代 → 再选母题 → 最后调形式）
- **构词法（本次增量）**：纹样名 = **结构骨架 × 题材母题**；结构词 Top（缠枝35 如意34 团花28 卷草26 折枝18 四合14 龟背11 盘肠10 方胜10）＋ 母题 Top（花128 云121 枝53 龙35 莲34 宝相21 凤20 牡丹20）→ 掌握约 20 骨架 ＋ 30 母题即可自创合规命名
- **命名长度规律**：5 字占 49%｜7 字占 17%｜3–4 字占 21%（名字长度＝复杂度读数）
- **寓意线索**：132 条（27%）含明确吉祥语义（如意35 万18 寿11 仙9 八仙8 祥6 福5 吉3）→ 酒店语境需防误配
- **★ 边界**：底库是**目录不是内页** —— 逐条寓意、文物出处、图像形态未收录；`compose` 只在**命名层**给合规判断
"""
print("5) domains/代码与工具链:", append_once(os.path.join(SI, "domains", "代码与工具链.md"), "### 纹样（《纹样设计速查手册》内化）", DOM))

# 日记
D19 = os.path.join(ROOT, "memory", "2026-11-19.md")
if not os.path.exists(D19):
    open(D19, "w", encoding="utf-8", newline="\n").write("""# 2026-11-19 日记

## 主题：《纹样设计速查手册》全面吸收内化

### 一、书不在本机 —— 先查证再动手
扫描 679,398 个文件（C 用户域 ＋ D 盘深 5 层）＋ 13,621 个 WPS 企业云盘文件 ＋ 全部接收目录（Downloads／企业微信／微信／OneDrive／Documents／Desktop）＋ 近 14 天新增 —— **零命中**。
文本里出现的"纹样"是**文漾都江 88 款纹样 IP 库**（都江堰文创），不是这本书。

→ 决定：不凭空写。转而确认它是公开出版物，取官方书目与目录原文作为证据基础。

### 二、书的真实身份（国家出版发行信息公共服务平台）
**《纹样设计速查手册》｜红糖美学 著｜人民邮电出版社（绘客）｜2024-08｜ISBN 9787115643353｜328 页｜32 开全彩铜版｜¥129｜中图 J51-62**
1200+ 中国传统纹样 · 13 大类 · 每纹样独立编号 · 标注文物来源与藏品出处 · 按先秦→明清分期以**避免时代搭配错误**。
姊妹版《纹样之美》（北京大学出版社 2024，239 页）目录更细且带页码 —— 本次底库取自此书。

### 三、做了什么
1. **信源分层**：官方书目（cppinfo）＋ 出版社宣传页 ＋ 三民網路書店目录原文 ＋ 越秀外国语学院 MARC 目录
2. **底库**：503 条可检索纹样（章 ＋ 页码 ＋ 原书编号），落 `output/book_纹样设计速查手册/纹样索引.json`
3. **构词法分析**（本次增量，非转述）：纹样名 = **结构骨架 × 题材母题**；结构词 Top20 ＋ 母题 Top30 ＋ 实存共现组合；命名长度规律（5 字 49%）；寓意线索占比 27%
4. **内化笔记**：`anyi-ops-kb/04_方法论/方法论书籍内化/《纹样设计速查手册》核心内化笔记_v1.0_2026-11-19.md`（七段式，含【源】/【判】/【问】分层 ＋ 3 处口径差异 ＋ 7 条失败模式）
5. **技能**：`skills/pattern-design-cn/`（SKILL.md ＋ `pattern_index.py` ＋ `data/`）—— search / chapter / compose / motifs / structures / stats
6. **落地到在跑的项目**：国堰宾馆纹样选型清单 v1.0 → 桌面 `产业发展部/旗下酒店/国堰宾馆/文创改造/`（三源并用：文漾都江 88 款授权 ＋ 水利纹样骨架 ＋ 葫芦专供文创）＋ 已回写国堰文件索引
7. **断言**：新增 C23（底库存在＋技能在册＋检索器可执行）

### 四、这次的关键判断
**★ 「全面吸收」不是写一篇读后感，是产出「可检索底库 ＋ 可执行规则 ＋ 可落地场景清单」三件套。**
**★ 底库检索「葫芦」命中 0 条 —— 如实写进笔记与清单（"需查原书，不得凭想象配"），不拿"福禄纹"糊弄。**
**★ 内化笔记里必须写清哪层是书里的、哪层是我推的、哪层没拿到 —— 否则就是伪造证据。**

### 五、收尾三问
1. **今天有没有错？错在判断还是执行？** —— 一处判断失误被自己拦下：**差点凭标题编内容**（拦在动手前，靠"先查书在不在"这一步）；执行层面两次小错（`relpath` 跨卷异常、繁简映射不全）都已修。
2. **有没有更好的做法？有没有更好的传感器？** —— 做法：**信源分层 + 底库边界如实报告**；传感器：**C23 断言**（底库在不在、技能在不在册、检索器能不能跑 —— 三者缺一即 FAIL）。
3. **有没有新规律？** —— **书籍内化的产出必须是可执行资产，不是感想；且必须显式声明"哪部分我没拿到"。** 落 `corrections.md` ＋ 域级文件。

### 六、明天接着做
- 补全 1200 条完整编号表（购书或取电子版）→ 当前 503 条
- 补《纹样之美》第一章「纹样简史」正文（各朝代特点）→ 当前只有目录条目
- 逐条寓意与文物出处（需原书内页）
- 核「葫芦纹」是否在原书内 —— 直接决定国堰文创线的符号策略
- 文漾都江 88 款图册与授权流程索取后，做主视觉 3 选 1
""")
    print("5) 日记已建: memory/2026-11-19.md")
else:
    print("5) 日记已存在")

# MEMORY
MM = os.path.join(ROOT, "MEMORY.md")
MADD = """
## ★ 《纹样设计速查手册》全面内化（2026-11-19）

- **★ 书不在本机**（扫 679,398 文件 ＋ 13,621 个 WPS 云盘文件 ＋ 全部接收目录 ＋ 近 14 天新增，零命中）→ **不凭空写，转而取公开原文**。真实身份：红糖美学著｜人民邮电出版社·绘客｜2024-08｜ISBN 9787115643353｜328 页 32 开全彩铜版｜¥129｜中图 J51-62｜**1200+ 纹样 · 13 大类 · 逐条编号 · 标文物出处 · 按先秦→明清分期以避免时代搭配错误**。
- **★ 底库 503 条**（`output/book_纹样设计速查手册/纹样索引.json`）：《纹样之美》姊妹版目录 422 条（章＋页码）＋ 速查手册编号表 81 条（0001–0081）。
- **★ 本次增量（不是转述，是从真实数据做的分析）**：**纹样名 = 结构骨架 × 题材母题**。结构词 Top（缠枝35 如意34 团花28 卷草26 折枝18 四合14 龟背11 盘肠10 方胜10 锁子8 八仙8）＋ 母题 Top（花128 云121 枝53 龙35 莲34 宝相21 凤20 牡丹20 鸟16 蝶15）＋ 实存共现组合（如意×云11、缠枝×花11、四合×云10）→ **掌握约 20 骨架 ＋ 30 母题即可自创结构合规的纹样名**。命名长度：5 字占 49%｜7 字 17%｜3–4 字 21%（名字长度＝复杂度读数）。寓意线索 132 条（27%：如意35 万18 寿11 仙9 八仙8 祥6 福5 吉3）。
- **★ 方法三约束**：**① 朝代一致 ② 寓意适配 ③ 溯源可授权**；顺序不可颠倒（先定朝代 → 再选母题 → 最后调形式）。13 类中前 4 类（云/几何/莲/牡丹）是可无限衍生的骨架类，第 8–13 类（龙/凤/兽面/鸟/蝶/人物）是**带权力象征的具象图腾，公共空间慎用**。
- **★ 交付三件套**：① 内化笔记 `anyi-ops-kb/04_方法论/方法论书籍内化/《纹样设计速查手册》核心内化笔记_v1.0_2026-11-19.md`（12.8 KB，七段式，**【源】/【判】/【问】分层**，如实记 3 处口径差异：飞鸟纹 vs 鸟纹以目录为准／1200+ vs 1210 取保守／团队 13 年 vs 14 年取 13+）② **技能 `skills/pattern-design-cn/`**（SKILL.md ＋ `scripts/pattern_index.py`：search／chapter／compose／motifs／structures／stats，**compose 是组合校验器**）③ **落地清单**：桌面 `产业发展部/旗下酒店/国堰宾馆/文创改造/2026-11-19_国堰纹样选型清单_v1.0_据《纹样设计速查手册》.md`（三源并用：**文漾都江 88 款授权纹样 ＋ 水利纹样骨架（涡形水云纹 #0015／水涡云纹 #0017／水云纹 #0022）＋ 葫芦专供文创不进主视觉**）＋ 已回写国堰文件索引。
- **★ ★ 底库边界如实报告**：检索「**葫芦命中 0 条**」—— 已写进笔记与清单（"需查原书全文，不得凭想象配"）。底库是**目录不是内页**，逐条寓意／文物出处／图像形态未收录；`compose` 只在**命名层**给合规判断。**这四问未闭前不能宣称"已全面吸收"。**
- **★ 通用规则**：**内化一本书的产出必须是「可检索底库 ＋ 可执行规则 ＋ 可落地场景清单」三件套，而不是读后感；且必须显式声明哪部分没拿到 —— 否则就是伪造证据。**
- **★ 新断言 C23**：底库存在 ＋ 技能入注册表 ＋ 检索器可执行，三者缺一即 FAIL。
- **关联**：`skills/pattern-design-cn/`｜`output/book_纹样设计速查手册/`（索引／构词法／抓取原文存证）｜`anyi-ops-kb/04_方法论/方法论书籍内化/《纹样设计速查手册》核心内化笔记_v1.0_2026-11-19.md`｜桌面 `产业发展部/旗下酒店/国堰宾馆/文创改造/`
<!-- project: github.com/darknessdogeric/openclaw-memory -->
"""
print("5) MEMORY:", append_once(MM, "《纹样设计速查手册》全面内化（2026-11-19）", MADD))

# ---------- 6. 终检 ----------
print()
print("=" * 96)
r = subprocess.run([PY, os.path.join(ROOT, "toolbox", "selfcheck.py")], capture_output=True, timeout=400)
print(r.stdout.decode("utf-8", "replace"))
print("退出码:", r.returncode)
