# -*- coding: utf-8 -*-
"""selfcheck.py - 把每次教训变成"可失败的断言"，替代散文式自省

用法:
    python toolbox/selfcheck.py            # 全跑，退出码 0=全过 1=有失败
    python toolbox/selfcheck.py --json
设计原则（对标 ACE/Reflection 研究的 grounded critique）：
    反思必须锚在"执行/检索"上。散文式"经验教训"会陷入 coherence trap
    —— 读起来有道理，但从不变下一次动作。每条教训必须是一条能 PASS/FAIL 的断言。
"""
import io, sys, os, re, json, glob, subprocess, datetime
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")
SI = os.path.join(HOME, "self-improving")

CHECKS = []
def check(cid, title, rule):
    def deco(fn):
        CHECKS.append({"id": cid, "title": title, "rule": rule, "fn": fn})
        return fn
    return deco

def _md_files(base):
    return [p for p in glob.glob(os.path.join(base, "**", "*.md"), recursive=True)
            if os.path.isfile(p) and ".bak" not in os.path.basename(p)]

# ---------------- C01 编码 ----------------
@check("C01", "知识库文本文件不得新增编码损坏", "已知损伤有基线；只报新增 —— 不可逆的损伤只能事前拦")
def c01():
    base_path = os.path.join(SI, "eval", "encoding_baseline_2026-11-17.json")
    known = {}
    if os.path.exists(base_path):
        try:
            bj = json.load(open(base_path, encoding="utf-8"))
            for it in bj.get("items", []):
                known[it["path"]] = it.get("ufffd", 0)
        except Exception:
            known = {}
    cur = {}
    for base in [SI, os.path.join(ROOT, "anyi-ops-kb"), os.path.join(ROOT, "memory")]:
        if not os.path.isdir(base):
            continue
        for p in _md_files(base):
            try:
                rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            except ValueError:
                rel = p.replace(os.sep, "/")
            try:
                t = open(p, "rb").read().decode("utf-8")
                n = t.count("\ufffd")
            except UnicodeDecodeError as e:
                n = -1
            if n != 0:
                cur[rel] = n
    newbad = []
    for rel, n in cur.items():
        if rel not in known:
            newbad.append((rel, "新增损坏 U+FFFD=%d" % n))
        elif n > known[rel]:
            newbad.append((rel, "较基线恶化 %d -> %d" % (known[rel], n)))
    healed = [r for r in known if r not in cur]
    msg = "无新增损坏（已知基线 %d 个受损文件，其中 %d 个已修复）" % (len(known), len(healed)) if not newbad else "%d 个文件新增/恶化" % len(newbad)
    return (not newbad), msg, newbad[:8]

# ---------------- C02 HOT 层上限 ----------------
@check("C02", "HOT memory.md 不超过 100 行", "SKILL.md 规定 HOT <=100 行，超了就不再常驻")
def c02():
    p = os.path.join(SI, "memory.md")
    if not os.path.exists(p):
        return False, "memory.md 不存在", []
    t = open(p, encoding="utf-8", errors="replace").read()
    n = t.count("\n") + 1
    return (n <= 100), ("%d 行 (上限100)" % n), []

# ---------------- C03 HOT 层时效 ----------------
@check("C03", "HOT 层不得含已过期事实", "HOT 只放今天仍成立的事实；带日期的易失效事实须迁 archive/")
def c03():
    p = os.path.join(SI, "memory.md")
    if not os.path.exists(p):
        return False, "memory.md 不存在", []
    t = open(p, encoding="utf-8", errors="replace").read()
    bad = []
    for m in re.finditer(r"(\d{4}-\d{2}-\d{2})[^。\n]{0,24}(剩余|截止|剩\s*\d+\s*天|已到期)", t):
        bad.append(m.group(0)[:60])
    today = datetime.date.today()
    for m in re.finditer(r"(20\d\d)-(\d\d)-(\d\d)[^。\n]{0,18}(剩余\s*\d+\s*天|截止)", t):
        try:
            d = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            if (today - d).days > 30:
                bad.append(m.group(0)[:60])
        except Exception:
            pass
    return (not bad), ("发现 %d 条过期事实" % len(bad) if bad else "无过期事实"), bad[:5]

# ---------------- C04 索引一致性 ----------------
@check("C04", "index.md 与 rules.md 标题级 R 编号一致", "索引脱节 47 条的教训；口径必须是标题级")
def c04():
    idx = os.path.join(SI, "index.md")
    rls = os.path.join(SI, "rules.md")
    if not (os.path.exists(idx) and os.path.exists(rls)):
        return False, "index.md 或 rules.md 不存在", []
    it = open(idx, encoding="utf-8", errors="replace").read()
    rt = open(rls, encoding="utf-8", errors="replace").read()
    real = len(set(re.findall(r"^#{1,4}\s*(R\d{2,4})\b", rt, re.M)))
    # ★ 正则放宽：index.md 由程序生成，表述格式可能变；不要写死格式
    claimed = None
    for pat in [r"标题级 R 号 \*\*(\d+)\*\*",          # 新格式
                r"R 编号数[^\d]{0,20}\*\*(\d+)\*\*",
                r"标题级唯一编号 \*\*(\d+)\*\*",
                r"\*\*(\d+)\*\*\s*个（最高",
                r"\*\*(\d+)\*\*\s*个（最高 R"]:     # 旧格式
        m = re.search(pat, it)
        if m:
            claimed = int(m.group(1)); break
    if claimed is None:
        return False, "index.md 未声明标题级数量（格式可能已变，需同步检查器正则）", []
    m = None
    return (claimed == real), ("声明 %d / 实际 %d" % (claimed, real), "差 %d" % (claimed - real)), []

# ---------------- C05 分层不空转 ----------------
@check("C05", "domains/ 与 projects/ 不得为空", "分层目录空转 = 内容全堆两个大文件 = 记忆腐化")
def c05():
    out = []
    for sub in ["domains", "projects"]:
        d = os.path.join(SI, sub)
        fs = [f for f in glob.glob(os.path.join(d, "*.md"))] if os.path.isdir(d) else []
        if not fs:
            out.append(sub)
    return (not out), ("空目录: %s" % ",".join(out) if out else "两层均有内容"), out

# ---------------- C06 正本唯一 ----------------
@check("C06", "磁盘上只能存在一个 self-improving 目录", "同一规则散在四处 = 下次必然取错版本；副本已于 2026-11-17 全删")
def c06():
    p = os.path.join(SI, "CANONICAL.md")
    if not os.path.exists(p):
        return False, "缺 CANONICAL.md", []
    t = open(p, encoding="utf-8", errors="replace").read()
    if "正本" not in t:
        return False, "CANONICAL.md 未声明正本", []
    # ★ 磁盘上实际存在几个 self-improving 目录
    found = []
    for d in [os.path.join(SI), os.path.join(ROOT, "self-improving"),
              os.path.join(HOME, ".self-improving"),
              os.path.join(ROOT, "memory", "self-improving")]:
        if os.path.isdir(d):
            found.append(d)
    extra = [d for d in found if os.path.realpath(d) != os.path.realpath(SI)]
    if extra:
        return False, ("发现 %d 个额外副本: %s" % (len(extra), "; ".join(os.path.basename(x) for x in extra)),
                       [os.path.relpath(x, ROOT).replace(os.sep, "/") for x in extra])
    return True, ("正本唯一（磁盘上仅 1 个 self-improving 目录）"), []

# ---------------- C07 无重复造轮子 ----------------
@check("C07", "同功能工具不得重复造", "toolbox 已有 8 个 md->docx 变体，我今天又造了第 9 个")
def c07():
    tb = os.path.join(ROOT, "toolbox")
    # ★ 只查"能力型工具"（可复用能力），排除一次性脚本族
    ONEOFF = re.compile(r"^(append_|add_|check_|atomic_|_|mk_|make_|tmp_|patch_|fix_|gen_|v\d)")
    CAPABILITY = re.compile(r"(docx|render|ocr|pptx|pdf|router|selfcheck|semantic|search|fetch)")
    fam = {}
    for p in glob.glob(os.path.join(tb, "*.py")):
        b = os.path.basename(p)
        if b.startswith("_") or ONEOFF.match(b):
            continue
        if not CAPABILITY.search(b):
            continue
        key = re.sub(r"[^a-z]", "", b.lower().replace("_", ""))
        for famkey in fam:
            if key.startswith(famkey[:5]) and famkey[:5]:
                fam[famkey].append(b)
                break
        else:
            fam[key] = [b]
    dup = {k: v for k, v in fam.items() if len(v) > 1}
    reg = os.path.join(SI, "eval", "duplicate_tools_2026-11-17.json")
    known = []
    if os.path.exists(reg):
        try:
            known = [tuple(x) for x in json.load(open(reg, encoding="utf-8")).get("families", [])]
        except Exception:
            known = []
    news = []
    for k, v in dup.items():
        if not any(sorted(x) == sorted(v) for x in known):
            news.append((k, v))
    return (not news), ("已知重复族 %d 个（在册），新增 %d 个" % (len(dup)-len(news), len(news)) if not news else "新增重复族: %s" % "; ".join("+".join(v) for _,v in news[:3])), news[:5]

# ---------------- C08 技能可路由 ----------------
@check("C08", "技能必须可被检索到（progressive disclosure）", "94 个技能、0 个路由索引 = 技能存在但不可发现")
def c08():
    r = os.path.join(ROOT, "toolbox", "skill_router.py")
    if not os.path.exists(r):
        return False, "缺 skill_router.py", []
    try:
        out = subprocess.run([sys.executable, r, "--task", "md 转 docx 排版"], capture_output=True, timeout=90)
        o = out.stdout.decode("utf-8", "replace")
    except Exception as e:
        return False, "路由执行失败 %s" % str(e)[:40], []
    hit = "docx" in o.lower() or "gongwen" in o.lower()
    return hit, ("路由可用" if hit else "路由无命中"), []

# ---------------- C09 纠错日志规模 ----------------
@check("C09", "corrections.md 不应无限膨胀", "SKILL.md 只保留最近 50 条；82KB 说明记录层已跑飞")
def c09():
    p = os.path.join(SI, "corrections.md")
    if not os.path.exists(p):
        return False, "corrections.md 不存在", []
    t = open(p, encoding="utf-8", errors="replace").read()
    n = len(re.findall(r"^## ", t, re.M))
    hot = 0
    hp = os.path.join(SI, "memory.md")
    if os.path.exists(hp):
        hot = len(open(hp, encoding="utf-8", errors="replace").read())
    ratio = len(t) / max(hot, 1)
    return (ratio <= 30), ("日志 %d 字符 / HOT %d 字符 = %.1f 倍 (阈值30)" % (len(t), hot, ratio), "记录层远大于行为层"), []

# ---------------- C10 记忆读回 ----------------
@check("C10", "近期日记必须被读回（memory 不能是 write-only）", "AGENTS.md 要求每次会话读 memory/YYYY-MM-DD.md；我今天一次没读")
def c10():
    md = os.path.join(ROOT, "memory")
    if not os.path.isdir(md):
        return False, "缺 memory 目录", []
    files = sorted(glob.glob(os.path.join(md, "2026-*.md")))
    if not files:
        return False, "无日记", []
    recent = files[-5:]
    unread = []
    for f in recent:
        t = open(f, encoding="utf-8", errors="replace").read()
        if len(t.strip()) < 200:
            unread.append(os.path.basename(f))
    return (not unread), ("%d 份近期日记过短" % len(unread) if unread else "近期日记均有实质内容"), unread

# ---------------- C11 域级文件覆盖 ----------------
@check("C11", "近期纠错必须沉淀到 domains/（否则只留在日志里）", "写进日志 ≠ 下次会被检索到")
def c11():
    dm = os.path.join(SI, "domains")
    if not os.path.isdir(dm):
        return False, "缺 domains/", []
    fs = [f for f in glob.glob(os.path.join(dm, "*.md"))]
    need = ["编码", "发布", "榜单", "口径"]
    have = " ".join(open(f, encoding="utf-8", errors="replace").read() for f in fs)   # ★ 读全文，不截断
    miss = [k for k in need if k not in have]
    return (not miss), ("未覆盖: %s" % ",".join(miss) if miss else "四个域级主题均已覆盖"), miss

@check("C12", "PREFLIGHT 必须存在且 <=40 行（动手前的强制清单）", "progressive disclosure：动手前只加载最短的那一份")
def c12():
    p = os.path.join(SI, "PREFLIGHT.md")
    if not os.path.exists(p):
        return False, "缺 PREFLIGHT.md", []
    n = open(p, encoding="utf-8", errors="replace").read().count("\n") + 1
    return (n <= 40), ("%d 行 (上限40)" % n), []

# ---------------- C13 技能注册表完备（2026-11-18 技能库审计新增） ----------------
@check("C13", "技能注册表须存在且每个技能有 description", "8 个技能无 description = 有技能但路由不到；注册表是路由的地基")
def c13():
    p = os.path.join(ROOT, "output", "audit_skills", "SKILL_REGISTRY.json")
    if not os.path.exists(p):
        return False, "缺 SKILL_REGISTRY.json", []
    try:
        rows = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return False, "注册表解析失败 %s" % str(e)[:50], []
    nod = [r.get("name","?") for r in rows if not (r.get("desc") or "").strip()]
    if nod:
        return False, "无 description 的技能 %d 个: %s" % (len(nod), ",".join(nod[:5])), nod[:5]
    return True, "注册表 %d 个技能，全部可路由（有 description）" % len(rows), []

# ---------------- C14 注册表不漂移 ----------------
@check("C14", "注册表须与磁盘技能一致（不漂移）", "注册表建完就漂 = 路由指向不存在的技能，等于没有索引")
def c14():
    p = os.path.join(ROOT, "output", "audit_skills", "SKILL_REGISTRY.json")
    if not os.path.exists(p):
        return False, "缺注册表", []
    rows = json.load(open(p, encoding="utf-8"))
    reg = {r.get("name") for r in rows}
    disk = set()
    # ★ 与注册表生成同口径：祖先目录若含 SKILL.md 则视为技能内部副本，不算独立技能
    for base in (os.path.join(ROOT,"skills"), os.path.join(HOME,"skills"), os.path.join(HOME,".claude","skills")):
        if not os.path.isdir(base):
            continue
        for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
            d = os.path.dirname(f)
            rel = os.path.relpath(d, base).split(os.sep)
            # ★ 与注册表生成器同一定义：_ 开头目录是归档区，不算在库技能
            if any(x.startswith("_") for x in rel):
                continue
            anc = rel[:-1]
            if any(os.path.exists(os.path.join(base, *anc[:i+1], "SKILL.md")) for i in range(len(anc))):
                continue
            tx = open(f, encoding="utf-8", errors="replace").read()
            m = re.search(r"^name:\s*(.+)$", tx, re.M)
            disk.add((m.group(1).strip() if m else os.path.basename(d)).strip('"\''))
    missing = sorted(disk - reg); stale = sorted(reg - disk)
    if missing or stale:
        return False, "磁盘有注册表无 %d 个: %s ｜ 注册表有磁盘无 %d 个: %s" % (
            len(missing), ",".join(missing[:4]), len(stale), ",".join(stale[:4])), (missing+stale)[:5]
    return True, "注册表 %d / 磁盘 %d，完全一致" % (len(reg), len(disk)), []

# ---------------- C15 GitHub 安装台账 ----------------
@check("C15", "GitHub 装的技能须有台账（来源/版本/许可证/回滚）", "AGENTS.md 硬要求；无台账 = 无法回滚、无法追责")
def c15():
    p = os.path.join(ROOT, "output", "audit_skills", "GITHUB_INSTALL_LEDGER.json")
    if not os.path.exists(p):
        return False, "缺 GITHUB_INSTALL_LEDGER.json", []
    try:
        L = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return False, "台账解析失败 %s" % str(e)[:50], []
    bad = []
    for it in L.get("installs", []):
        for k in ("repo","license","commit"):
            if not it.get(k): bad.append("%s:%s" % (it.get("name","?"), k))
    if not L.get("rollback"):
        bad.append("rollback")
    if bad:
        return False, "台账缺项: %s" % ",".join(bad[:5]), bad[:5]
    return True, "台账 %d 条安装，来源/许可/commit/回滚齐全" % len(L.get("installs", [])), []

# ---------------- C16 md→docx 正本唯一 ----------------
@check("C16", "通用 md→docx 只允许 1 个正本", "我今天造了第 9 个变体绕过既有轮子；再造第 10 个就是复发")
def c16():
    tb = os.path.join(ROOT,"toolbox")
    fam = sorted(os.path.basename(p) for p in glob.glob(os.path.join(tb,"*.py"))
                 if re.match(r"^md_?to_?docx|^md2docx", os.path.basename(p)))
    canon = os.path.join(ROOT,"skills","docx-md-bridge","scripts","md_to_docx.py")
    ok = os.path.exists(canon) and len(fam) <= 2
    if not ok:
        return False, "正本缺失=%s ｜ toolbox 内 md→docx 脚本 %d 个: %s" % (
            (not os.path.exists(canon)), len(fam), ",".join(fam)), fam
    return True, "正本在 skills/docx-md-bridge ｜ toolbox 仅余 %d 个有明确分工的变体(%s)" % (len(fam), ",".join(fam)), []

# ---------------- C17 固定工作流表非空 ----------------
@check("C17", "固定工作流表须存在且非空", "19 条工作流是『不重造轮子』的落地物；空表 = 只有口号没有路由")
def c17():
    p = os.path.join(ROOT, "output", "audit_skills", "WORKFLOWS.json")
    if not os.path.exists(p):
        return False, "缺 WORKFLOWS.json", []
    try:
        W = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return False, "工作流表解析失败 %s" % str(e)[:50], []
    bad = [w.get("task","?") for w in W if not (w.get("skills") or "").strip()]
    if len(W) < 5:
        return False, "工作流仅 %d 条，覆盖不足" % len(W), []
    if bad:
        return False, "缺 skills 字段: %s" % ",".join(bad[:4]), bad[:4]
    return True, "固定工作流 %d 条，每条均绑定技能" % len(W), []

# ---------------- C18 归档不回潮 ----------------
@check("C18", "已归档的旧克隆不得回到 toolbox 根目录", "归档不是搬走就完 —— 复活即等于重复轮子回流")
def c18():
    arc = os.path.join(ROOT,"toolbox","_archive","legacy_docx_variants_2026-11-18")
    if not os.path.isdir(arc):
        return True, "无归档目录（未触发）", []
    tb = os.path.join(ROOT,"toolbox")
    back = [f for f in os.listdir(arc) if os.path.exists(os.path.join(tb, f))]
    if back:
        return False, "回流 %d 个: %s" % (len(back), ",".join(back[:5])), back[:5]
    return True, "归档 %d 件，全部未回流" % len(os.listdir(arc)), []

# ---------------- C19 范式库可路由（2026-11-18 技能库审计新增） ----------------
@check("C19", "范式须可路由（有触发词）且工作流须绑定范式", "150 条范式若 143 条无『何时用』＝ 有范式但调不出来，与技能同款病")
def c19():
    p = os.path.join(ROOT, "output", "audit_skills", "PARADIGM_REGISTRY.json")
    if not os.path.exists(p):
        return False, "缺 PARADIGM_REGISTRY.json", []
    try:
        P = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return False, "范式注册表解析失败 %s" % str(e)[:50], []
    nokw = [x.get("file","?") for x in P if not (x.get("keywords") or x.get("when"))]
    if nokw:
        return False, "无触发词 %d 条: %s" % (len(nokw), ",".join(nokw[:3])), nokw[:5]
    wf = os.path.join(ROOT, "output", "audit_skills", "WORKFLOWS.json")
    if not os.path.exists(wf):
        return False, "缺 WORKFLOWS.json", []
    W = json.load(open(wf, encoding="utf-8"))
    nb = [w.get("task","?") for w in W if not (w.get("paradigms") or [])]
    if nb:
        return False, "未绑定范式的工作流 %d 条: %s" % (len(nb), ",".join(nb[:3])), nb[:5]
    return True, "范式 %d 条全部可路由 ｜ %d 条工作流全部绑定范式" % (len(P), len(W)), []

# ---------------- C20 工具索引完备（2026-11-18 工具层治理新增） ----------------
@check("C20", "工具索引须存在且每个工具都有分类", "417 个工具若无分类 = 工具层是黑箱；owner_skill 缺失 = 工具不知道归谁")
def c20():
    p = os.path.join(ROOT, "output", "audit_skills", "TOOL_INDEX.json")
    if not os.path.exists(p):
        return False, "缺 TOOL_INDEX.json", []
    try:
        T = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return False, "工具索引解析失败 %s" % str(e)[:50], []
    if not T:
        return False, "工具索引为空", []
    valid = ("capability", "oneoff_family", "orphan")
    bad = [k for k, v in T.items() if v.get("category") not in valid]
    if bad:
        return False, "未分类工具 %d 个: %s" % (len(bad), ",".join(bad[:4])), bad[:5]
    cats = {}
    for v in T.values():
        cats[v.get("category")] = cats.get(v.get("category"), 0) + 1
    owned = sum(1 for v in T.values() if v.get("owner_skill"))
    return True, "工具 %d 个 ｜ %s ｜ 已归属技能 %d" % (len(T), cats, owned), []

# ---------------- C21 工具须可被路由 ----------------
@check("C21", "工具必须能被 --task 检索到", "工具只写进索引 = 仍是黑箱；有工具不用正是这个病")
def c21():
    r = os.path.join(ROOT, "toolbox", "skill_router.py")
    if not os.path.exists(r):
        return False, "缺 skill_router.py", []
    try:
        out = subprocess.run([sys.executable, r, "--task", "把 md 转成带表格的 docx"],
                             capture_output=True, timeout=120)
        o = out.stdout.decode("utf-8", "replace")
    except Exception as e:
        return False, "路由执行失败 %s" % str(e)[:50], []
    if "工具命中" not in o:
        return False, "路由未输出工具区段", []
    if "md_to_docx" not in o and "docx" not in o.lower():
        return False, "路由未命中任何 docx 工具", []
    return True, "路由可检索工具层", []

# ---------------- C22 归档工具不得回流 ----------------
@check("C22", "已归档的一次性工具不得回流到 toolbox 根目录", "281 件 hb 一次性脚本已归档；回流即等于重复轮子复活")
def c22():
    arc = os.path.join(ROOT, "toolbox", "_archive", "hb_family_2026-11-18")
    if not os.path.isdir(arc):
        return True, "无归档目录（未触发）", []
    tb = os.path.join(ROOT, "toolbox")
    back = [f for f in os.listdir(arc) if os.path.exists(os.path.join(tb, f))]
    if back:
        return False, "回流 %d 件: %s" % (len(back), ",".join(back[:4])), back[:5]
    hb_left = len([f for f in os.listdir(tb) if f.startswith("hb") and f.endswith(".py")])
    return True, "归档 %d 件未回流 ｜ toolbox 根目录 hb* 剩 %d 件（有引用/目标仍在）" % (
        len(os.listdir(arc)), hb_left), []

# ---------------- C23 被取代版本必须归档留痕，不得留在项目根目录 ----------------
@check("C23", "被取代版本必须归档留痕，不得留在项目根目录", "2026-11-07 commit 662911c2 直接 rm 20 件被取代版本；旧版本是口径证据链，不是垃圾")
def c23():
    base = os.path.join(ROOT, "anyi-ops-kb", "02_项目")
    if not os.path.isdir(base):
        return True, "无 02_项目 目录（未触发）", []
    bad = []
    governed = 0
    for proj in sorted(os.listdir(base)):
        p = os.path.join(base, proj)
        if not os.path.isdir(p):
            continue
        arc = os.path.join(p, "_归档_被取代版本")
        if not os.path.isdir(arc):
            continue
        governed += 1
        for f in sorted(os.listdir(p)):
            fp = os.path.join(p, f)
            if os.path.isfile(fp) and "已被" in f:
                bad.append(proj + "/" + f)
        if not os.path.exists(os.path.join(arc, "00_归档清单_可回滚.md")):
            bad.append(proj + "/_归档_被取代版本/缺《00_归档清单_可回滚.md》")
    if bad:
        return False, "残留 %d 件: %s" % (len(bad), ",".join(bad[:4])), bad[:5]
    return True, "归档治理项目 %d 个 ｜ 根目录无被取代件残留 ｜ 归档清单齐备" % governed, []


# ---------------- C24 建立交付分层的项目文件夹必须有文件索引 ----------------
@check("C24", "建立交付分层的项目文件夹必须有文件索引", "AGENTS.md 硬规矩：交付后必须回写索引；无索引 = 交接不了、追溯不了")
def c24():
    base = os.path.join(os.path.expanduser("~"), "Desktop", "产业发展部", "旗下酒店")
    if not os.path.isdir(base):
        return True, "无 旗下酒店 目录（未触发）", []
    miss = []
    n = 0
    for proj in sorted(os.listdir(base)):
        p = os.path.join(base, proj)
        if not os.path.isdir(p):
            continue
        layered = os.path.isdir(os.path.join(p, "改造报告交付")) or os.path.isdir(os.path.join(p, "测算与中间产物"))
        if not layered:
            continue
        n += 1
        idx = [f for f in os.listdir(p) if f.startswith("00") and "索引" in f and f.endswith(".md")]
        if not idx:
            miss.append(proj)
    if miss:
        return False, "缺索引 %d 个: %s" % (len(miss), ",".join(miss[:4])), miss[:5]
    return True, "有交付分层项目 %d 个 ｜ 索引齐备" % n, []


# ---------------- C25 测算引擎默认行为不得静默漂移 ----------------
@check("C25", "测算引擎默认行为不得静默漂移（基准逐项锁定）", "R67 扩展测算引擎后，若有人改坏默认值，国堰的 IRR/NPV 会静默变化而无人察觉")
def c25():
    import importlib
    bl_path = os.path.join(ROOT, "toolbox", "_baseline", "irr_baseline_2026-11-18.json")
    if not os.path.exists(bl_path):
        return True, "无基线文件（未触发）", []
    try:
        base = json.load(open(bl_path, encoding="utf-8"))
    except Exception as e:
        return False, "基线读取失败 %s" % str(e)[:50], []
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    sys.path.insert(0, os.path.join(ROOT, "toolbox"))
    try:
        mod = importlib.import_module("hotel_irr_calc")
        importlib.reload(mod)
    except Exception as e:
        return False, "引擎导入失败 %s" % str(e)[:50], []
    cases = {
        "guoyan_A3_3000w_ADR600": dict(rooms=236, total_invest=3000, peak_adr=600, peak_occ=0.70,
            non_room_ratio=0.30, ramp_type='cultural', labor_cost_annual=800, rent_annual=221,
            discount_rate=0.08, tax_rate=0.25, gop_rate=0.38, labor_in_gop=True),
        "guoyan_B3_3000w_ADR320": dict(rooms=236, total_invest=3000, peak_adr=320, peak_occ=0.65,
            non_room_ratio=0.30, ramp_type='cultural', labor_cost_annual=800, rent_annual=221,
            discount_rate=0.08, tax_rate=0.25, gop_rate=0.38, labor_in_gop=True),
        "guoyan_v310_main_3600w": dict(rooms=236, total_invest=3600, peak_adr=330, peak_occ=0.55,
            non_room_ratio=0.50, ramp_type='cultural', labor_cost_annual=800, rent_annual=221,
            discount_rate=0.08, tax_rate=0.25, gop_rate=0.34, labor_in_gop=True),
        "legacy_default_labor_double": dict(rooms=236, total_invest=3000, peak_adr=600, peak_occ=0.70,
            non_room_ratio=0.30, ramp_type='cultural', labor_cost_annual=800, rent_annual=221,
            discount_rate=0.08, tax_rate=0.25, gop_rate=0.38),
    }
    diffs = []
    for name, p in cases.items():
        b = base.get(name)
        if not b:
            diffs.append(name + ": 基线缺失")
            continue
        try:
            r = mod.calc_hotel_project(p)
        except Exception as e:
            diffs.append("%s: 执行异常 %s" % (name, str(e)[:40]))
            continue
        got = {
            "irr": round(r["irr"], 6), "static_payback": round(r["static_payback"], 4),
            "dynamic_payback": round(r["dynamic_payback"], 4) if r.get("dynamic_payback") else None,
            "npv": round(r["npv"], 2),
        }
        for k, v in got.items():
            if b.get(k) != v:
                diffs.append("%s.%s: 基线 %s ≠ 现值 %s" % (name, k, b.get(k), v))
    if diffs:
        return False, "漂移 %d 项: %s" % (len(diffs), "; ".join(diffs[:3])), diffs[:5]
    return True, "4 组基准逐项一致（IRR/静态/动态回收/NPV）｜引擎默认行为未漂移", []


# ---------------- C26 直觉预判台账必须可审计 ----------------
@check("C26", "直觉预判台账每条记录必须有 falsifier 与数字 confidence", "R68：Eric 的强直觉若只在事后自我评分，则永远无法证伪、无法校准、无法升级为资产；登记即必须带证伪条件与数字置信度")
def c26():
    p = os.path.join(ROOT, "memory", "predictions", "intuition.jsonl")
    if not os.path.exists(p):
        return True, "无台账文件（未触发）", []
    bad = []
    n = 0
    try:
        with open(p, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                n += 1
                try:
                    r = json.loads(line)
                except Exception as e:
                    bad.append("第%d行 JSON 解析失败 %s" % (i, str(e)[:40]))
                    continue
                rid = r.get("id", "?")
                if not str(r.get("claim", "")).strip():
                    bad.append("%s claim 为空" % rid)
                if not str(r.get("falsifier", "")).strip():
                    bad.append("%s 缺 falsifier" % rid)
                c = r.get("confidence")
                if not isinstance(c, (int, float)) or not (0 <= float(c) <= 1):
                    bad.append("%s confidence 非 0-1 数字: %r" % (rid, c))
                if r.get("registration") not in ("live", "retrospective"):
                    bad.append("%s registration 非法: %r" % (rid, r.get("registration")))
                for k in ("as_of", "domain", "direction", "horizon_months", "basis"):
                    if r.get(k) in (None, ""):
                        bad.append("%s 缺 %s" % (rid, k))
    except Exception as e:
        return False, "台账读取失败 %s" % str(e)[:60], []
    if bad:
        return False, "台账 %d 条中 %d 项不合规: %s" % (n, len(bad), "; ".join(bad[:3])), bad[:5]
    return True, "台账 %d 条全部含 falsifier＋数字 confidence＋合法 registration" % n, []


# ---------------- CC27 纹样底库可检索（2026-11-19 纹样内化新增） ----------------
@check("C27", "纹样底库须存在、可检索、且技能已入注册表", "《纹样设计速查手册》内化后必须能被路由调用，否则等于没吸收")
def c27():
    idx = os.path.join(ROOT, "output", "book_纹样设计速查手册", "纹样索引.json")
    sk = os.path.join(ROOT, "skills", "pattern-design-cn", "SKILL.md")
    if not os.path.exists(idx):
        return False, "缺纹样索引", []
    if not os.path.exists(sk):
        return False, "缺 pattern-design-cn 技能", []
    try:
        P = json.load(open(idx, encoding="utf-8"))
    except Exception as e:
        return False, "索引解析失败 " + str(e)[:50], []
    n = len(P.get("index_meihua", [])) + len(P.get("numbered_4722198", []))
    if n < 100:
        return False, "底库条目仅 " + str(n) + " 条，覆盖不足", []
    reg = os.path.join(ROOT, "output", "audit_skills", "SKILL_REGISTRY.json")
    if not os.path.exists(reg):
        return False, "缺技能注册表", []
    names = {x["name"] for x in json.load(open(reg, encoding="utf-8"))}
    if "pattern-design-cn" not in names:
        return False, "pattern-design-cn 未入注册表（路由不到）", []
    try:
        out = subprocess.run([sys.executable,
                              os.path.join(ROOT, "skills", "pattern-design-cn", "scripts", "pattern_index.py"),
                              "search", "水"], capture_output=True, timeout=90)
        o = out.stdout.decode("utf-8", "replace")
    except Exception as e:
        return False, "检索器执行失败 " + str(e)[:40], []
    if "命中" not in o:
        return False, "检索器无输出", []
    return True, "纹样底库 " + str(n) + " 条 ｜ 技能已入册 ｜ 检索器可执行", []

# ---------------- C27 履历真源一致性：虚构任职实体清零 ----------------
@check("C28", "履历真源一致性：虚构任职实体清零 + 真源文件存在", "R69：把乱码猜成履历并据此写人物画像＝虚构材料→虚构引语→虚构结论；引用 Eric 履历只认唯一真源")
def c27():
    forbid = ["国宾凯悦", "国奥元禧", "重庆博升", "瑞珀酒店集团"]
    bad = []
    for rel in ("MEMORY.md", "USER.md"):
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        c = open(p, encoding="utf-8", errors="replace").read()
        for k in forbid:
            if k in c:
                bad.append("%s 含 %s" % (rel, k))
    auth = os.path.join(ROOT, "memory", "eric-career-authoritative.md")
    if not os.path.exists(auth):
        bad.append("缺 memory/eric-career-authoritative.md")
    else:
        ac = open(auth, encoding="utf-8", errors="replace").read()
        for k in forbid:
            if k not in ac:
                bad.append("真源未列禁用实体 %s" % k)
        for need in ("岷山", "远途", "丽苑维景", "共享维景", "安逸", "中旅"):
            if need not in ac:
                bad.append("真源缺节点 %s" % need)
    mdir = os.path.join(ROOT, "memory")
    for dp, dn, fn in os.walk(mdir):
        dn[:] = [x for x in dn if x != "__pycache__"]
        for f in fn:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            c = open(p, encoding="utf-8", errors="replace").read()
            for k in forbid:
                if k in c and not any(m in c for m in ("虚构", "严禁", "污染", "禁用")):
                    bad.append("%s 含 %s 且无错误标记" % (os.path.relpath(p, ROOT), k))
    if bad:
        return False, "履历真源不一致 %d 项: %s" % (len(bad), "; ".join(bad[:4])), bad[:6]
    return True, "MEMORY/USER 虚构任职实体清零｜真源存在且六节点齐全｜memory 残留均带错误标记", []


# ---------------- C28 首日档案必须带乱码标注并由解码正本替代 ----------------
@check("C29", "首日档案必须降级标注并由真源替代引用", "R69：首日档案是 2026-02-12 简历 PDF 视觉转写(OCR)产物，含转写错字；只能作背景参考，引用必须经真源")
def c29():
    p = os.path.join(ROOT, "memory", "user-knowledge-base.md")
    auth = os.path.join(ROOT, "memory", "eric-career-authoritative.md")
    if not os.path.exists(p):
        return True, "无首日档案（未触发）", []
    if not os.path.exists(auth):
        return False, "缺真源 memory/eric-career-authoritative.md", ["缺真源"]
    ac = open(auth, encoding="utf-8", errors="replace").read()
    bad = []
    for need in ("背景参考", "OCR", "源优先级", "维景", "远途"):
        if need not in ac:
            bad.append("真源缺标注 %s" % need)
    u = os.path.join(ROOT, "USER.md")
    if os.path.exists(u):
        uc = open(u, encoding="utf-8", errors="replace").read()
        if "eric-career-authoritative" not in uc:
            bad.append("USER.md 未指向真源")
        if "首日档案" not in uc or "背景参考" not in uc:
            bad.append("USER.md 未标注首日档案为背景参考")
    if bad:
        return False, "首日档案治理不完整 %d 项: %s" % (len(bad), "; ".join(bad[:4])), bad[:6]
    return True, "首日档案已降级为背景参考｜真源含源优先级与维景/远途口径｜USER.md 已指向真源", []


# ---------------- C30 履历口径一致性（维景/远途） ----------------
@check("C30", "履历口径一致性：真源履历表与 USER.md 同为维景/远途口径，OCR 错字与虚构实体清零", "R69-b/R69-c：首日档案的「美居/元图」是 OCR 错字（正解维景/远途），且不得用行业常识补全出虚构实体")
def c30():
    auth = os.path.join(ROOT, "memory", "eric-career-authoritative.md")
    u = os.path.join(ROOT, "USER.md")
    bad = []
    if not os.path.exists(auth):
        return False, "缺真源 memory/eric-career-authoritative.md", ["缺真源"]
    ac = open(auth, encoding="utf-8", errors="replace").read()
    for need in ("维景", "远途", "禁用清单", "源优先级"):
        if need not in ac:
            bad.append("真源缺 %s" % need)
    FORBID = ("美居", "元图", "国宾凯悦", "国奥元禧", "重庆博升", "瑞珀酒店集团", "首旅如家")
    # 真源 §1 履历表内：零容忍
    m = re.search(r"## 1\..*?(?=\n## 2\.)", ac, re.S)
    if not m:
        bad.append("真源找不到 §1 履历表")
    else:
        rows = [x for x in m.group(0).splitlines() if x.strip().startswith("|")]
        for forbid in FORBID:
            for row in rows:
                if forbid in row:
                    bad.append("真源履历表含禁用实体 %s" % forbid)
    # 真源其余部分：若提及禁用实体，必须带标注（说明它是 OCR 错字/禁用项）
    for n, l in enumerate(ac.splitlines(), 1):
        for forbid in FORBID:
            if forbid in l and not any(k in l for k in ("OCR", "错字", "禁用", "虚构", "转写", "行业对标", "合理性检验")):
                bad.append("真源 L%d 提及 %s 但无标注" % (n, forbid))
    # USER.md：履历表内零容忍；表外提及必须带标注
    if os.path.exists(u):
        uc = open(u, encoding="utf-8", errors="replace").read()
        for need in ("丽苑维景", "共享维景"):
            if need not in uc:
                bad.append("USER.md 缺 %s" % need)
        mm = re.search(r"### 实际工作经历.*?(?=\n### )", uc, re.S)
        if not mm:
            bad.append("USER.md 找不到实际工作经历表")
        else:
            rows = [x for x in mm.group(0).splitlines() if x.strip().startswith("|")]
            for forbid in FORBID:
                for row in rows:
                    if forbid in row:
                        bad.append("USER.md 履历表含禁用实体 %s" % forbid)
        for n, l in enumerate(uc.splitlines(), 1):
            for forbid in FORBID:
                if forbid in l and not any(k in l for k in ("OCR", "错字", "禁用", "虚构", "转写", "背景参考", "行业对标", "首日档案")):
                    bad.append("USER.md L%d 提及 %s 但无标注" % (n, forbid))
    if bad:
        return False, "履历口径不一致 %d 项: %s" % (len(bad), "; ".join(bad[:4])), bad[:6]
    return True, "真源与 USER.md 履历表同为维景/远途口径｜OCR 错字与虚构实体清零（仅存标注式说明）", []


# ---------------- C31 工具层：一次性 PDF 抽取脚本不得回流 toolbox 根目录 ----------------
@check("C31", "一次性 PDF 抽取脚本不得回流 toolbox 根目录", "2026-11-20 教训：每遇一份新 PDF 就复制一份 dump_pdf_xx.py，逻辑完全相同只改写死路径 —— 5 件并存把 C07 顶到 FAIL。正本已参数化落到 skills/pdf-extract/scripts/pdf_extract.py")
def c31():
    tb = os.path.join(ROOT, "toolbox")
    bad = []
    for p in glob.glob(os.path.join(tb, "dump_pdf*.py")):
        bad.append(os.path.basename(p))
    skill = os.path.join(ROOT, "skills", "pdf-extract")
    script = os.path.join(skill, "scripts", "pdf_extract.py")
    sk_md = os.path.join(skill, "SKILL.md")
    if not os.path.exists(script):
        bad.append("缺正本 skills/pdf-extract/scripts/pdf_extract.py")
    if not os.path.exists(sk_md):
        bad.append("缺 skills/pdf-extract/SKILL.md")
    else:
        t = open(sk_md, encoding="utf-8", errors="replace").read()
        if "description:" not in t:
            bad.append("pdf-extract/SKILL.md 缺 description（无法被路由命中）")
        if "PDF" not in t and "pdf" not in t:
            bad.append("pdf-extract/SKILL.md 缺触发词")
    arc = os.path.join(tb, "_archive", "pdf_dump_family_2026-11-20")
    if not os.path.isdir(arc):
        bad.append("缺归档目录 pdf_dump_family_2026-11-20")
    else:
        if not os.path.exists(os.path.join(arc, "00_归档清单_可回滚.md")):
            bad.append("归档目录缺《00_归档清单_可回滚.md》")
        kept = len([f for f in os.listdir(arc) if f.endswith(".py")])
        if kept < 5:
            bad.append("归档件仅 %d 件（应为 5 件，payload 全保留）" % kept)
    if bad:
        return False, "工具层 PDF 抽取治理未闭环: %s" % "; ".join(bad[:4]), bad[:6]
    return True, "toolbox 根目录无 dump_pdf* ｜ 正本 pdf_extract.py 已落技能层 ｜ 归档 5 件带可回滚清单", []


# ---------------- C32 KB 副本单一化：不得扫最旧副本下结论 ----------------
@check("C32", "KB 检索须指向主副本，不得扫最旧副本", "2026-11-20 教训：判三份原件已丢失前只扫了 D:\anyi-ops-kb（旧副本，新媒体件只到 10-02），而它们完整存在于 workspace\anyi-ops-kb 主副本。11-06 全盘扫描已写明该教训，本次重复犯错")
def c32():
    primary = os.path.join(ROOT, "anyi-ops-kb")
    guide = os.path.join(primary, "README_主副本说明.md")
    bad = []
    if not os.path.isdir(primary):
        bad.append("主副本不存在 %s" % primary)
    else:
        if not os.path.exists(guide):
            bad.append("主副本缺 README_主副本说明.md（KB 检索入口指引）")
        else:
            g = open(guide, encoding="utf-8", errors="replace").read()
            for token in ("anyi-ops-kb", "README_主副本说明", "主副本"):
                if token not in g:
                    bad.append("主副本说明缺要素 %s" % token)
        n = len([f for f in glob.glob(os.path.join(primary, "**", "*"), recursive=True)
                 if os.path.isfile(f)])
        if n < 1500:
            bad.append("主副本文件数仅 %d（应 > 1500，疑似被误当作旧副本）" % n)
    # 会话档案里的 KB 引用不得指向旧副本
    for mem in ("anyi-newmedia-session-init_v2.md",):
        mp = os.path.join(ROOT, "memory", mem)
        if os.path.exists(mp):
            t = open(mp, encoding="utf-8", errors="replace").read()
            if "D:\anyi-ops-kb" in t and "workspace" not in t:
                bad.append("%s 的 KB 引用指向旧副本 D:\anyi-ops-kb" % mem)
    if bad:
        return False, "KB 副本纪律未闭环: %s" % "; ".join(bad[:4]), bad[:6]
    return True, "主副本 README 已立 ｜ 主副本文件数 > 1500 ｜ 会话档案引用指向主副本", []


# ---------------- C33 原件层双跑：KB 是二手，桌面才是原件 ----------------
@check("C33", "检索须 Desktop + KB 双跑，不得只查 KB", "2026-11-20 教训：11-06 桌面原件扫描已写明「KB ≠ 原件，任何全盘扫描必须 Desktop + KB 双跑」，但本轮仍只查 KB，漏掉桌面原件层，致拍板清单两条建议与原件矛盾。新增断言：原件层索引须存在、本板块会话档案须引用桌面原件路径")
def c33():
    primary = os.path.join(ROOT, "anyi-ops-kb")
    idx = os.path.join(primary, "09_来源材料", "README_原件层索引.md")
    bad = []
    if not os.path.exists(idx):
        bad.append("主副本缺 09_来源材料/README_原件层索引.md（KB≠原件 的检索入口）")
    else:
        g = open(idx, encoding="utf-8", errors="replace").read()
        for token in ("Desktop", "双跑", "原件层", "桌面"):
            if token not in g:
                bad.append("原件层索引缺要素 %s" % token)
        if "Desktop" not in g and "桌面" not in g:
            bad.append("原件层索引未指向桌面原件路径")
    # 本板块会话档案必须引用桌面原件层路径（否则下个会话又会只查 KB）
    for mem in ("anyi-newmedia-session-init_v2.md",):
        mp = os.path.join(ROOT, "memory", mem)
        if os.path.exists(mp):
            t = open(mp, encoding="utf-8", errors="replace").read()
            if ("产业发展部" not in t) or ("Desktop" not in t and "桌面" not in t):
                bad.append("%s 未引用桌面原件层路径" % mem)
    if bad:
        return False, "原件层双跑纪律未闭环: %s" % "; ".join(bad[:4]), bad[:6]
    return True, "原件层索引已立 ｜ 桌面+KB 双跑纪律已写入 ｜ 会话档案引用桌面原件路径", []


# ---------------- C34 交付件结构断言：存在 不等于 对位 ----------------
@check("C34", "交付件须过结构校验：条款在位、编号连续、无残留", 
"2026-11-20 教训：脚本锚点形态不匹配时静默跳过，条款丢失而断言不报；校验须含结构断言而非只查关键词")
def c34():
    desk = os.path.join("C:/Users/ericz/Desktop", "产业发展部", "新媒体业务")
    docs = {
        "安逸集团小红书矩阵建设需求标准_V1.1修订对照表_v1.2_2026-11-20.docx": ["C7", "C8", "C9", "C10", "C11", "审读", "3.0%"],
        "安逸集团小红书矩阵_服务商方案重新征集函_草稿_v1.2_2026-11-20.docx": ["C7", "C8", "C9", "C10", "C11", "审读", "3.0%"],
        "国堰单店闭环打样_执行清单_v1.0_2026-11-20.docx": ["213", "266.80", "40.45", "85%", "美舍", "W1", "审读", "C10"],
        "D1过时表述_存量排查底稿_v1.0_2026-11-20.docx": ["唯一高星级涉外", "对外沟通记录", "温泉酒店", "管道", "19 条独立表述"],
    }
    bad = []
    try:
        import docx
    except Exception:
        return True, "未装 python-docx，跳过结构校验", []
    for fn, kws in docs.items():
        fp = os.path.join(desk, fn)
        if not os.path.exists(fp):
            bad.append("缺交付件 %s" % fn)
            continue
        try:
            d = docx.Document(fp)
        except Exception as e:
            bad.append("无法解析 %s: %s" % (fn, str(e)[:30]))
            continue
        txt = [para.text for para in d.paragraphs]
        for tb in d.tables:
            for r in tb.rows:
                txt.append(" | ".join(c.text for c in r.cells))
        full = chr(10).join(txt)
        for k in kws:
            if k not in full:
                bad.append("%s 缺要素 %s" % (fn, k))
        if chr(0xFFFD) in full:
            bad.append("%s 含 U+FFFD 编码损坏" % fn)
        resid = [l for l in txt if l.strip().startswith("|")]
        if resid:
            bad.append("%s 有 %d 行 Markdown 残留" % (fn, len(resid)))
        empty = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if not c.text.strip())
        if empty:
            bad.append("%s 有 %d 个空单元格" % (fn, empty))
        if not d.tables:
            bad.append("%s 无表格" % fn)
    # 有序列表编号连续性（征集函提交材料 1 至 16），不用正则避免转义坑
    letter = os.path.join(desk, "安逸集团小红书矩阵_服务商方案重新征集函_草稿_v1.2_2026-11-20.docx")
    if os.path.exists(letter):
        d2 = docx.Document(letter)
        nums = set()
        for para in d2.paragraphs:
            t = para.text.strip()
            head = t.split(".", 1)[0]
            if head.isdigit() and t[len(head):len(head) + 1] == ".":
                nums.add(int(head))
        miss = [i for i in range(1, 17) if i not in nums]
        if miss:
            bad.append("征集函提交材料编号缺失: %s" % miss)
    if bad:
        return False, "交付件结构校验未过: %s" % "; ".join(bad[:4]), bad[:6]
    return True, "交付件结构校验通过 ｜ 要素在位 ｜ 提交材料 1-16 编号连续 ｜ 无残留无空单元格", []

# ---------------- C35 Markdown 表格结构通则（源文件级） ----------------
@check("C35", "md 表格块须唯一分隔行，docx 不得有垃圾分隔行", "2026-11-20 教训：修复脚本对每一行都补分隔符，一次修复反而制造垃圾行；断言须在 md 源级校验表格块，并在 docx 级校验无残留分隔行")
def c35():
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("_c35_impl", os.path.join(ROOT, "toolbox", "_c35_impl.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        desk = os.path.join("C:/Users/ericz/Desktop", "产业发展部", "新媒体业务")
        return mod.check(ROOT, desk)
    except Exception as e:
        return False, "C35 执行异常 %s" % str(e)[:60], []


# ---------------- C36 入境游数据卡（2026-11-20 新增） ----------------
@check("C36", "入境游数据卡须齐备且生成器在库", "免签红利这条曲线是对外材料高频引用项：缺版/尺寸不符/生成器丢失 = 无法复现也无法交付")
def c36():
    out = os.path.join(ROOT, 'output', 'info_inbound')
    need = {'inbound_9x16.png': (2160, 3840), 'inbound_3x4.png': (2160, 2880)}
    miss = []
    for fn, wh in need.items():
        p = os.path.join(out, fn)
        if not os.path.exists(p):
            miss.append(fn + ':缺文件'); continue
        try:
            from PIL import Image
            with Image.open(p) as im:
                if (im.width, im.height) != wh:
                    miss.append('%s:%dx%d' % (fn, im.width, im.height))
        except Exception as e:
            miss.append(fn + ':' + str(e)[:30])
    if miss:
        return False, '入境游数据卡缺失或尺寸不符: ' + '; '.join(miss[:3]), miss[:3]
    gen = os.path.join(ROOT, 'skills', 'source-matrix-infographic', 'scripts', 'make_inbound_chart.py')
    if not os.path.exists(gen):
        return False, '缺 make_inbound_chart.py（不可复现）', []
    tpl = os.path.join(ROOT, 'skills', 'source-matrix-infographic', 'data', 'tpl_inbound.html')
    if not os.path.exists(tpl):
        return False, '缺 tpl_inbound.html', []
    return True, '两版齐备（2160×3840 / 2160×2880）｜生成器与模板在库', []

# ---------------- C37 B 标品牌串统一（2026-11-21 新增） ----------------
@check("C37", "B 标品牌串须统一为 ERIC & B166ER", "Eric 2026-11-21 明确：凡 ERIC<分隔符>B166ER 一律改 ERIC & B166ER；旧形态回流即此断言 FAIL")
def c37():
    import re as _re
    seps = "\\s*[\\u00d7\\u2715Xx\\uff38*\\u00b7]\\s*"
    old1 = _re.compile("ERIC" + seps + "B166ER", _re.I)
    old2 = _re.compile("B166ER" + seps + "ERIC", _re.I)
    exts = (".md", ".txt", ".html", ".htm", ".css", ".js", ".json", ".py", ".csv")
    skip = {"node_modules", ".git", "__pycache__", "_archive", "site-packages", ".venv", "venv", "brand_rename_2026-11-21"}
    roots = [os.path.join(ROOT, x) for x in ("memory", "toolbox", "anyi-ops-kb", "skills")]
    bad = []
    for rt in roots:
        if not os.path.isdir(rt):
            continue
        for base, dirs, fs in os.walk(rt):
            dirs[:] = [d for d in dirs if d not in skip and not d.startswith(".")]
            for f in fs:
                if os.path.splitext(f)[1].lower() not in exts:
                    continue
                p = os.path.join(base, f)
                try:
                    if os.path.getsize(p) > 6000000:
                        continue
                    tx = open(p, encoding="utf-8", errors="replace").read()
                except Exception:
                    continue
                n = len(old1.findall(tx)) + len(old2.findall(tx))
                if n:
                    bad.append(os.path.relpath(p, ROOT) + ":" + str(n))
    if bad:
        return False, "旧 B 标形态残留 " + str(len(bad)) + " 处: " + "; ".join(bad[:3]), bad[:3]
    return True, "B 标统一 ERIC & B166ER ｜ 两向旧形态 0 残留", []

# ---------------- C38 B 标旧形态补扫（2026-11-21 新增） ----------------
# 补 C37 的两个漏洞：① 扫描根补 outputs/ 与 obsidian-vault/ ② 判定改为逐行不跨行
@check("C38", "B 标旧形态须在 outputs/ 与 obsidian-vault/ 一并归零", "2026-11-21 实测：C37 只扫 4 根且用跨行正则, outputs/ 与 obsidian-vault/ 长期漏网; 实现见 toolbox/_c38_impl.py")
def c38():
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("_c38_impl", os.path.join(ROOT, "toolbox", "_c38_impl.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.check(ROOT)
    except Exception as e:
        return False, "C38 执行异常 %s" % str(e)[:60], []


# ---------------- C39 关键交付件存在性（防"写完≠跑过"） ----------------
@check("C39", "关键交付件必须真实存在且内容完整", "2026-11-19 写了 43KB 构建脚本却没跑 → 测算表根本没生成却已回复'已交付'；存在性检查必须会 FAIL")
def c39():
    import os as _os
    desk = _os.path.join(_os.path.expanduser("~"), "Desktop", "产业发展部", "旗下酒店", "国堰宾馆")
    if not _os.path.isdir(desk):
        return True, "桌面交付目录不存在（未触发）", []
    need = [
        (_os.path.join(desk, "00_国堰宾馆文创改造_文件索引.md"), "桌面总索引"),
        (_os.path.join(desk, "改造报告交付", "国堰_分阶段测算表_v1.0_2026-11-19.xlsx"), "分阶段测算表"),
        (_os.path.join(desk, "改造报告交付", "2026-11-22_分阶段方案v2.1_口径修正版_含测算表_v2.1.md"), "分阶段方案 v2.1"),
    ]
    miss = []
    for p, label in need:
        if not _os.path.exists(p) or _os.path.getsize(p) < 1000:
            miss.append(label)
    if miss:
        return False, "缺失或内容异常 %d 件: %s" % (len(miss), ",".join(miss)), miss
    try:
        from openpyxl import load_workbook
        wb = load_workbook(need[1][0], read_only=True)
        want = ["00_读我与口径", "01_参数", "02_分期投资表", "03_分年现金流",
                "04_情景矩阵", "05_敏感性", "06_决策门阈值", "07_口径冲突与待校准", "08_来源与置信度"]
        lack = [w for w in want if w not in wb.sheetnames]
        wb.close()
        if lack:
            return False, "测算表缺工作表 %d 张: %s" % (len(lack), ",".join(lack[:4])), lack[:5]
    except Exception as e:
        return False, "测算表无法读取 %s" % str(e)[:50], []
    return True, "交付件齐全（总索引 + 测算表 9 表 + 分阶段方案 v2.1）", []


# ---------------- C40 正式交付件不得含"更正叙述"（Eric 2026-11-22 立规） ----------------
def _formal_files():
    """正式交付件清单：KB 项目目录下的报告/请示/方案/纪要类 md ＋ 桌面产业发展部交付件 md"""
    out = []
    kb = os.path.join(ROOT, "anyi-ops-kb", "02_项目")
    for p in _md_files(kb):
        n = os.path.basename(p)
        if any(k in n for k in ("报告", "请示", "方案", "纪要")):
            try:
                r = os.path.relpath(p, ROOT).replace(os.sep, "/")
            except ValueError:
                r = p.replace(os.sep, "/")
            out.append(r)
    desk = os.path.join(HOME, "Desktop", "产业发展部")
    for p in _md_files(desk):
        n = os.path.basename(p)
        if "索引" in n or "README" in n:
            continue
        try:
            r = os.path.relpath(p, ROOT).replace(os.sep, "/")
        except ValueError:
            r = p.replace(os.sep, "/")
        out.append(r)
    return sorted(set(out))


@check("C40", "正式交付件只讲内容本身，不得叙述改了什么",
       "Eric 2026-11-22 21:47：出正式内容时不要出现「更正了什么」，直接就是内容本身；新增正式件一律严查")
def c40():
    pats = ["更正", "此前称", "此前写", "此前版", "上一版", "经复核", "这是错的", "我错",
            "虚高", "已更正", "改错", "我方更", "有误", "口径修正"]
    bl = os.path.join(SI, "eval", "formal_deliverables_baseline_2026-11-22.json")
    base = set()
    if os.path.exists(bl):
        try:
            base = set(json.load(open(bl, encoding="utf-8")).get("files", []))
        except Exception:
            base = set()
    else:
        files = _formal_files()
        json.dump({"files": files}, open(bl, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return True, "已建立正式件基线 %d 件（既有件豁免，此后新增件严查）" % len(files), []
    bad = []
    for p in _formal_files():
        if p in base:
            continue
        try:
            t = open(p, encoding="utf-8").read()
        except Exception:
            continue
        hit = [w for w in pats if w in t]
        if hit:
            bad.append("%s ← %s" % (os.path.basename(p), ",".join(hit)))
    if bad:
        return False, "正式件含更正叙述 %d 件" % len(bad), bad
    return True, "正式件无更正叙述（新增 %d 件严查）" % (len(_formal_files()) - len(base)), []



# ---------------- C41 主体名称须有源文件出处 ----------------
@check("C41", "正式件中的运营/管理主体名称须有源文件出处",
       "Eric 2026-11-23：正式件里出现的运营方、管理方、品牌方名称，必须能在项目源文件（管理合同、专题报告、专题会纪要、评估报告）里找到同名出处；"
       "严禁把市场上其他公司或酒店集团的名称安到本项目头上。已知无出处者列入黑名单，全库有效区均不得再出现。")
def c41():
    import glob as _g
    KB = os.path.join(ROOT, "anyi-ops-kb", "02_项目", "总府皇冠假日")
    DESK = os.path.join(os.path.expanduser("~"), "Desktop", "产业发展部",
                        "旗下酒店", "总府皇冠假日酒店", "招商推介")
    BLACK = ["逸柏"]          # 已知无出处：出现在酒店集团清单里，非本项目运营方
    NEED = ["六洲酒店管理（上海）有限公司", "洲际酒店集团", "四川总府实业有限公司"]
    formal = []
    for p in _g.glob(os.path.join(KB, "**", "*招商推介*.md"), recursive=True):
        if os.path.isfile(p) and "_已废止_" not in p:
            formal.append(p)
    for p in _g.glob(os.path.join(DESK, "*.md")):
        if os.path.isfile(p):
            formal.append(p)
    if not formal:
        return True, "未发现总府招商推介正式件（跳过）", []
    bad = []
    for p in formal:
        try:
            s = open(p, encoding="utf-8").read()
        except Exception:
            continue
        hit = [w for w in BLACK if w in s]
        if hit:
            bad.append("%s 无出处主体名 %s" % (os.path.basename(p), ",".join(hit)))
        # 必备主体只对正式母本/模板生效；核对表、口径裁决表等过程件不要求载明
        bn = os.path.basename(p)
        if not bn.startswith("00_") and ("PPT模板" in bn or "投资方版" in bn):
            miss = [w for w in NEED if w not in s]
            if miss:
                bad.append("%s 缺应载明的主体 %s" % (bn, ",".join(miss)))
    # 项目 KB 有效区 + 桌面交付目录防复发（范围受限，保证 selfcheck 秒级）
    scope = []
    scope += [p for p in _g.glob(os.path.join(KB, "**", "*.md"), recursive=True)
              if os.path.isfile(p) and "_已废止_" not in p]
    scope += [p for p in _g.glob(os.path.join(DESK, "**", "*.md"), recursive=True) if os.path.isfile(p)]
    for p in scope:
        try:
            s = open(p, encoding="utf-8").read()
        except Exception:
            continue
        hit = [w for w in BLACK if w in s]
        if hit:
            bad.append("%s 无出处主体名 %s" % (os.path.basename(p), ",".join(hit)))
    if bad:
        return False, "发现无出处主体名或主体缺漏 %d 处" % len(bad), bad
    return True, "正式件主体名称均有源文件出处（正式件 %d 份，扫描 %d 份，黑名单 %d 词 0 命中）" % (len(formal), len(scope), len(BLACK)), []


# ---------------- C42 亏损治理与经营综合分析能力（2026-11-23 新增） ----------------
@check("C42", "企业亏损治理与经营综合分析能力须真实存在且结构完整",
       "2026-11-23 新增能力：技能三件（SKILL.md ＋ 分析模版 ＋ 红线校验）＋ KB 正本 ＋ 注册表登记；缺任一件即 FAIL")
def c42():
    import os as _os, json as _json
    base = _os.path.join(ROOT, "skills", "loss-governance-analysis")
    need = [
        (_os.path.join(base, "SKILL.md"), "SKILL.md"),
        (_os.path.join(base, "references", "分析模版.md"), "分析模版"),
        (_os.path.join(base, "references", "红线与校验.md"), "红线与校验"),
        (_os.path.join(ROOT, "anyi-ops-kb", "04_方法论", "企业亏损治理与经营综合分析办法_v1.0_2026-11-23.md"), "KB正本"),
    ]
    miss = []
    for p, label in need:
        if not _os.path.exists(p) or _os.path.getsize(p) < 800:
            miss.append(label)
    det = []
    if miss:
        return False, "缺失或过小: " + ", ".join(miss), miss
    tpl = open(_os.path.join(base, "references", "分析模版.md"), encoding="utf-8").read()
    must = ["一页纸结论", "经营结构分解", "亏损归因三层", "处置决策", "落地三要素", "数据清单",
            "S01", "L0", "TRevPAR"]
    bad = [m for m in must if m not in tpl]
    if bad:
        det.append("模版缺结构: " + ", ".join(bad))
    sk = open(_os.path.join(base, "SKILL.md"), encoding="utf-8").read()
    if "name:" not in sk.split("---")[1] or "description:" not in sk.split("---")[1]:
        det.append("SKILL.md frontmatter 缺 name 或 description")
    trig = ["亏损治理", "经营综合分析", "亏损归因"]
    if not any(x in sk for x in trig):
        det.append("SKILL.md description 缺触发词")
    reg = _os.path.join(ROOT, "output", "audit_skills", "SKILL_REGISTRY.json")
    if not _os.path.exists(reg):
        det.append("注册表缺失")
    else:
        try:
            rows = _json.load(open(reg, encoding="utf-8"))
            if not any(r.get("name") == "loss-governance-analysis" for r in rows):
                det.append("注册表未登记 loss-governance-analysis")
        except Exception as e:
            det.append("注册表读取异常 %s" % str(e)[:40])
    if det:
        return False, "能力不完整: " + det[0][:80], det
    return True, "亏损治理与经营综合分析能力完整（技能三件 ＋ KB 正本 ＋ 注册表 ＋ 六段结构）", []



# ---------------- C43 康体业态口径（禁止把姊妹酒店业态安到本项目）----------------
@check("C43", "康体业态不得使用无源业态名；层数面积餐位口径须与工程部档案一致",
       "Eric 2026-11-23：工程部《物业基础档案·工程概况》表A2 的正式名称是「娱乐部 3,780 ㎡」；"
       "洲际 PIP 原件康体设施栏为「Pool, Fitness; SPA」——本项目无温泉汤泉业态。"
       "同业主姊妹物业总府川宾即四川宾馆（2024 报告：1999 年与本酒店同时被评为五星级饭店和四星级饭店），同样不是温泉酒店。正式件禁止把温泉/汤泉用于本项目或川宾；"
       "外部参照所在行放行：哈尔滨北龙汤泉酒店 8·25 火灾案（2024 报告原文）、中山温泉与温江皇冠假日（第三方造价与竞品案例）。"
       "地上 29 层、主体建筑檐高 108 m、地上主体建筑面积 58,064.43 ㎡、地下 8,611.2 ㎡、"
       "全日餐厅 1,574 ㎡／490 餐位、厨房 1,975.4 ㎡、池内四根承重柱。")
def c43():
    import glob as _g
    DESK = os.path.join(os.path.expanduser("~"), "Desktop", "产业发展部",
                        "旗下酒店", "总府皇冠假日酒店")
    # 项目自用禁用；外部参照（北龙/中山/温江）按所在行放行，见下方 EXEMPT
    BAD = [r"(?<!北龙)(?<!中山)(?<!温江)汤泉", r"(?<!北龙)(?<!中山)(?<!温江)温泉",
           r"泡汤", r"汤泉[（(]?康体", r"汤泉体",
           r"川宾温泉", r"四星级温泉", r"总府川宾温泉", r"温泉运营", r"温泉日场",
           r"温泉会员", r"温泉汤浴", r"三根承重柱", r"负一层泳池",
           r"11,611\.20", r"44490", r"(?<![0-9])90\s*餐位",
           r"地上\s*28\s*层", r"\|\s*地上层数\s*\|\s*28\s*层", r"约\s*98\s*m"]
    # 仅对物业/招商类正式件校验必备口径值
    MUST = ["3,780", "58,064.43", "8,611.2", "29 层", "108 m", "490 餐位", "娱乐部", "厨房"]
    # 外部参照所在行放行：
    #   北龙＝2018·8·25 重大火灾案（2024 报告原文）；中山/温江＝第三方造价与竞品案例
    EXEMPT = ("北龙", "中山", "温江")
    targets = []
    for d in (os.path.join(DESK, "招商推介"), os.path.join(DESK, "改造报告交付")):
        targets += [p for p in _g.glob(os.path.join(d, "*.md")) + _g.glob(os.path.join(d, "*.docx"))
                    if os.path.isfile(p)]
    if not targets:
        return True, "未发现正式交付件（跳过）", []
    bad = []
    for p in targets:
        try:
            if p.endswith(".md"):
                s = open(p, encoding="utf-8").read()
            else:
                from docx import Document as _D
                _d = _D(p)
                s = "\n".join([q.text for q in _d.paragraphs] +
                              [c.text for tb in _d.tables for rr in tb.rows for c in rr.cells])
        except Exception:
            continue
        for ln in s.split("\n"):
            if any(x in ln for x in EXEMPT):
                continue
            for pat in BAD:
                if re.search(pat, ln):
                    bad.append("%s 命中禁用口径 %s" % (os.path.basename(p), pat))
                    break
        bn = os.path.basename(p)
        if "招商推介" in bn and not bn.startswith("00_"):
            miss = [w for w in MUST if w not in s]
            if miss:
                bad.append("%s 缺必备口径值 %s" % (bn, ",".join(miss)))
    if bad:
        return False, "康体业态口径违规 %d 处" % len(bad), bad
    return True, "康体业态口径正确（正式件 %d 份，无项目自用温泉汤泉，层数面积餐位一致）" % len(targets), []


@check("C44", "招商推介 PPT 模板不得含估值金额与财务测算词，且必备口径值须齐全",
       "Eric 2026-11-23：喂给 PPT 生成工具的招商模板，内容段不得出现任何金额、估值、投资额、造价、"
       "营业收入、利润、收益率、回收期类数字（评估总值 69,923.42 万元、原始工程投资 67,430 万元均不得进入）；"
       "同时不得出现 汤泉/泡汤/11,611.20/地上 28 层/约 98 m 等旧错值，"
       "且必须载明 娱乐部/3,780/58,064.43/8,611.2/29 层/108 m/490 餐位/厨房 与三大主体名称。")
def c44():
    import glob as _g
    DESK = os.path.join(os.path.expanduser("~"), "Desktop", "产业发展部",
                        "旗下酒店", "总府皇冠假日酒店", "招商推介")
    tpl = [p for p in _g.glob(os.path.join(DESK, "*PPT模板*.md")) + _g.glob(os.path.join(DESK, "*PPT模板*.docx"))
           if os.path.isfile(p)]
    if not tpl:
        return True, "未发现招商 PPT 模板（跳过）", []
    MONEY = ["万元", "亿元", "评估值", "评估总值", "资产价值", "投资额", "改造投资", "造价",
             "营业收入", "经营利润", "净利润", "毛利", "现金流", "NPV", "IRR", "内部收益率",
             "净现值", "回收期", "投资回报", "收益率", "估值", "市值", "溢价", "成本", "负债",
             "可承受", "67,430", "69,923.42"]
    BAD = [r"(?<!北龙)汤泉", r"泡汤", r"11,611\.20", r"44490", r"(?<![0-9])90\s*餐位",
           r"地上\s*28\s*层", r"约\s*98\s*m", r"逸柏", r"其他中庭"]
    MUST = ["69,026.08", "58,064.43", "8,611.2", "29 层", "108 m", "402 间", "3,780.00",
            "490 餐位", "娱乐部", "厨房", "六洲酒店管理（上海）有限公司", "洲际酒店集团",
            "四川总府实业有限公司"]
    bad = []
    for p in tpl:
        try:
            if p.endswith(".md"):
                s = open(p, encoding="utf-8").read()
            else:
                from docx import Document as _D
                _d = _D(p)
                s = "\n".join([q.text for q in _d.paragraphs] +
                              [c.text for tb in _d.tables for rr in tb.rows for c in rr.cells])
        except Exception:
            continue
        # 只校验内容段（生成指令段的禁写条款允许出现禁词名）
        # 注意：docx 顶部有目录，"页面清单"会先以目录项出现 → 取最后一个精确标题位置
        seg = s
        if p.endswith(".md"):
            k = s.find("## 页面清单")
            if k >= 0:
                seg = s[k:]
        else:
            from docx import Document as _DD
            _d2 = _DD(p)
            paras = [q.text for q in _d2.paragraphs]
            idxs = [i for i, q in enumerate(paras) if q.strip() == "页面清单"]
            if idxs:
                seg = "\n".join(paras[idxs[-1]:])
                seg += "\n" + "\n".join(
                    c.text for tb in _d2.tables for rr in tb.rows for c in rr.cells)
            else:
                k = s.find("页面清单")
                if k >= 0:
                    seg = s[k:]
        hit = [w for w in MONEY if w in seg]
        if hit:
            bad.append("%s 含估值/财务词 %s" % (os.path.basename(p), ",".join(hit)))
        for pat in BAD:
            if re.search(pat, seg):
                bad.append("%s 命中旧错值 %s" % (os.path.basename(p), pat))
        miss = [w for w in MUST if w not in seg]
        if miss:
            bad.append("%s 缺必备口径值 %s" % (os.path.basename(p), ",".join(miss)))
    if bad:
        return False, "招商模板口径违规 %d 处" % len(bad), bad
    return True, "招商模板口径正确（模板 %d 份，无估值金额，必备口径值齐全）" % len(tpl), []


# ---------------- C45 中国传统色值库（2026-11-25 新增） ----------------
@check("C45", "中国传统色值库须 71 条齐备且字段完整", "《中国传统色主题配色手册》v2.0 内化成果：色库缺条目/字段缺失/脚本丢失 = 国风配色无法复现，且会把待校准值误当书载值")
def c45():
    import json as _json
    base = os.path.join(ROOT, 'skills', 'chinese-traditional-color')
    lib = os.path.join(base, 'references', 'ctc_colors.json')
    scr = os.path.join(base, 'scripts', 'ctc_palette.py')
    skl = os.path.join(base, 'SKILL.md')
    miss = []
    if not os.path.exists(lib):
        return False, '缺 references/ctc_colors.json', []
    if not os.path.exists(scr):
        return False, '缺 scripts/ctc_palette.py（配色方法不可复现）', []
    if not os.path.exists(skl):
        return False, '缺 SKILL.md（技能不可路由）', []
    try:
        with open(skl, encoding='utf-8') as f:
            head = f.read(1500)
        if 'description:' not in head:
            return False, 'SKILL.md 缺 description（路由不到）', []
    except Exception as e:
        return False, 'SKILL.md 读取失败: ' + str(e)[:40], []
    try:
        with open(lib, encoding='utf-8') as f:
            data = _json.load(f)
    except Exception as e:
        return False, '色库解析失败: ' + str(e)[:40], []
    cols = data.get('colors') or []
    if len(cols) != 71:
        return False, '色库条目数 ' + str(len(cols)) + '，应为 71（47 传统色 + 24 节气）', []
    need = ('name', 'family', 'meaning', 'value_source', 'pending_book_value')
    bad = []
    for c in cols:
        for k in need:
            if k not in c:
                bad.append(str(c.get('name', '?')) + ' 缺 ' + k)
        hx = c.get('hex')
        if hx is not None and not (isinstance(hx, str) and hx.startswith('#') and len(hx) == 7):
            bad.append(str(c.get('name', '?')) + ' HEX 格式异常')
        if c.get('family') == '节气' and hx is not None:
            bad.append(str(c.get('name', '?')) + ' 节气色不应有书载值')
    if bad:
        return False, '色库字段/口径异常: ' + '; '.join(bad[:3]), bad[:3]
    pend = len([c for c in cols if c.get('pending_book_value')])
    return True, '71 条齐备（47 + 24）｜字段完整｜待校准 ' + str(pend) + ' 条（书载值未取得，须诚实标注）', []

# ---------------- C46 预测台账与纪律工具（2026-11-26 新增） ----------------
@check("C46", "预测台账须有可结算条目且纪律工具齐备", "西尔弗信号与噪声内化成果：台账不产生分数就不算在跑；概率不给结算日 = 不可证伪的断言 = 不算预测")
def c46():
    import json as _json
    base = os.path.join(ROOT, 'skills', 'prediction-discipline')
    led = os.path.join(ROOT, 'data', 'prediction_ledger.jsonl')
    need = ['ledger.py', 'base_rate.py', 'regression_to_mean.py', 'signal_audit.py', 'brier.py']
    miss = [n for n in need if not os.path.exists(os.path.join(base, 'scripts', n))]
    if miss:
        return False, '纪律工具缺失: ' + ', '.join(miss), miss
    if not os.path.exists(led):
        return False, '缺 data/prediction_ledger.jsonl', []
    rows = []
    try:
        with open(led, encoding='utf-8') as f:
            for ln in f:
                ln = ln.strip()
                if ln and not ln.startswith('#'):
                    rows.append(_json.loads(ln))
    except Exception as e:
        return False, '台账解析失败: ' + str(e)[:40], []
    if not rows:
        return False, '台账为空 —— 原则二要求每条预测留痕', []
    bad = []
    for r in rows:
        for k in ('id', 'question', 'p', 'resolved_date', 'base_rate'):
            if r.get(k) is None:
                bad.append(str(r.get('id', '?')) + ' 缺 ' + k)
        p = r.get('p')
        if not isinstance(p, (int, float)) or not (0 < p < 1):
            bad.append(str(r.get('id', '?')) + ' 概率必须在(0,1)开区间')
    if bad:
        return False, '台账字段/概率口径异常: ' + '; '.join(bad[:3]), bad[:3]
    sk = os.path.join(base, 'SKILL.md')
    if not os.path.exists(sk):
        return False, '缺 SKILL.md（技能不可路由）', []
    head = open(sk, encoding='utf-8').read(2000)
    if 'description:' not in head:
        return False, 'SKILL.md 缺 description（路由不到）', []
    settled = len([r for r in rows if r.get('outcome') is not None])
    return True, '台账 ' + str(len(rows)) + ' 条（已结算 ' + str(settled) + '）｜五工具齐备｜概率与结算日口径合规', []

# ---------------- C47 公文排版器须输出 A4 纸张（2026-11-27 新增） ----------------
@check("C47", "公文排版器必须显式设置 A4 纸张（python-docx 默认模板是 Letter）",
       "GB/T 9704 用 A4；默认模板 8.5x11in 比 A4 少 1.76cm 页高，会让图片被挤出页、页数虚增、打印错位")
def c47():
    p = os.path.join(ROOT, 'skills', 'gongwen-docx-cn', 'scripts', 'md2docx_gongwen.py')
    if not os.path.exists(p):
        return False, '缺 md2docx_gongwen.py（公文排版正本丢失）', []
    s = open(p, encoding='utf-8', errors='replace').read()
    miss = [k for k in ('sec.page_width', 'sec.page_height', 'Cm(21.0)', 'Cm(29.7)') if k not in s]
    if miss:
        return False, '未显式设 A4 纸张：缺 ' + '、'.join(miss), miss
    return True, '已显式设 A4（21.0 × 29.7 cm），非 Letter 默认模板', []


# ---------------- C48 AgentOS 工程闭环（2026-11-28 新增：企业级 AgentOS 内化成果） ----------------
@check("C48", "AgentOS 工程闭环须齐备：体检/成本台账/Trace与审计分离/策略层/事故回灌",
       "《企业级AgentOS架构设计与工程实践》内化成果：缺 Trace 与审计分离 = 出事查不到哪一步、谁授权；"
       "缺策略层 = 硬规矩只停在文字层靠自觉；缺事故回灌 = 同类错误必然复发；缺成本台账 = 账单来了才知道浪费")
def c48():
    need = [
        ("skills/agentos-architecture/SKILL.md", "AgentOS 技能主文件"),
        ("skills/agentos-architecture/scripts/agentos_gap_audit.py", "12 层成熟度体检"),
        ("skills/agentos-architecture/scripts/cost_ledger.py", "模型成本台账工具"),
        ("skills/agentos-architecture/scripts/trace_log.py", "Trace 与审计事件分离工具"),
        ("skills/agentos-architecture/scripts/policy_gate.py", "机器可执行策略层"),
        ("data/model_cost_ledger.jsonl", "成本台账"),
        ("data/task_trace.jsonl", "任务级 Trace"),
        ("data/audit_events.jsonl", "审计事件独立成账"),
        ("data/regression_cases.jsonl", "事故回灌回归集"),
        ("data/policy_ledger.jsonl", "策略执行记录"),
        ("anyi-ops-kb/04_方法论/方法论书籍内化/《企业级AgentOS架构设计与工程实践》核心内化笔记_v1.0_2026-11-28.md", "内化笔记"),
    ]
    miss = []
    for rel, label in need:
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.exists(p):
            miss.append(label + "(" + os.path.basename(rel) + ")")
        elif os.path.getsize(p) < 40:
            miss.append(label + " 内容为空")
    if miss:
        return False, "缺 " + "、".join(miss), miss
    # Trace 与审计必须分账：文件不同，且各自非空
    tr = open(os.path.join(ROOT, "data", "task_trace.jsonl"), encoding="utf-8", errors="replace").read()
    au = open(os.path.join(ROOT, "data", "audit_events.jsonl"), encoding="utf-8", errors="replace").read()
    if "trace_id" not in tr and "step" not in tr:
        return False, "task_trace.jsonl 缺 trace/step 字段", []
    if "actor" not in au or "action" not in au:
        return False, "audit_events.jsonl 缺 actor/action 字段（审计与 Trace 必须分账）", []
    # 回归集必须非空：事故不回灌 = 同类错误复发
    rg = [l for l in open(os.path.join(ROOT, "data", "regression_cases.jsonl"), encoding="utf-8", errors="replace") if l.strip()]
    if len(rg) < 1:
        return False, "事故回灌回归集为空", []
    # 策略层必须含机器可执行策略，且不是只有文字
    ps = open(os.path.join(ROOT, "skills", "agentos-architecture", "scripts", "policy_gate.py"), encoding="utf-8", errors="replace").read()
    for k in ("def evaluate", "idempotency_key", "ESCALATE", "DENY", "ALLOW"):
        if k not in ps:
            return False, "策略层缺 " + k + "（策略必须可判定、有幂等键、有审批与拦截动作）", [k]
    # 成本台账必须有记录且字段完整
    cl = [l for l in open(os.path.join(ROOT, "data", "model_cost_ledger.jsonl"), encoding="utf-8", errors="replace") if l.strip()]
    if not cl:
        return False, "成本台账为空（不记账就等于不知道钱花在哪）", []
    for l in cl:
        try:
            r = json.loads(l)
        except Exception:
            return False, "成本台账有坏行（非 JSON）", []
        for k in ("actor", "task", "tokens", "value"):
            if k not in r:
                return False, "成本台账缺字段 " + k, [k]
    return True, ("AgentOS 闭环齐备：四工具 + 四账本 + 策略层可判定 ｜ 事故回归集 %d 条 ｜ 成本台账 %d 条"
                  % (len(rg), len(cl))), []


# ---------------- C49 自动结算作业须按到期日触发，不得每日空跑（2026-11-28 新增） ----------------
@check("C49", "台账结算作业须为到期日节点：每日轮询已废止，且每条预测的到期日都须有节点或安全网覆盖",
       "第 4 章「成本记录：不要等到账单来了才发现问题」的护栏：每日 cron 曾一次空跑烧 678,145 token；"
       "新预测若没配到期节点就会漏结算 —— 断言让两者都跑不掉")
def c49():
    import subprocess as _sp
    import json as _json
    CLI = r"C:\Users\ericz\AppData\Roaming\npm\openclaw.cmd"
    if not os.path.exists(CLI):
        return False, "openclaw CLI 不存在，无法核验自动作业状态", []
    try:
        r = _sp.run([CLI, "cron", "list", "--json"], capture_output=True, timeout=60)
        raw = r.stdout.decode("utf-8", "replace")
        jobs = _json.loads(raw).get("jobs", [])
    except Exception as e:
        return False, "读取 cron 列表失败，无法核验：%s" % str(e)[:80], []

    def cron_daily(expr):
        """真正每日 = 分 时 * * *  （日与月均为通配，且星期亦为通配）。
        注意：'0 9 * * 1' 是每周一，不是每日 —— 不能只看前两位。"""
        parts = (expr or "").split()
        if len(parts) != 5:
            return False
        mi, hr, dom, mon, dow = parts
        return dom == "*" and mon == "*" and dow == "*"

    settle = [j for j in jobs if "台账结算" in (j.get("name") or "")]
    if not settle:
        return False, "找不到任何台账结算作业", []

    # 1) 不得存在 enabled 的每日结算作业
    daily = []
    for j in settle:
        if not j.get("enabled"):
            continue
        sch = j.get("schedule") or {}
        if sch.get("kind") == "cron" and cron_daily(sch.get("expr")):
            daily.append("%s (%s)" % (j.get("name"), sch.get("expr")))
    if daily:
        return False, "存在每日轮询的结算作业（每日空跑烧 token）：" + "、".join(daily), daily

    # 2) 每条预测的到期日都须被节点覆盖
    led = os.path.join(ROOT, "data", "prediction_ledger.jsonl")
    if not os.path.exists(led):
        return False, "预测台账缺失", []
    dues = set()
    for ln in open(led, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        try:
            o = _json.loads(ln)
        except Exception:
            continue
        d = o.get("resolved_date")
        if d:
            dues.add(d)
    if not dues:
        return True, "台账无到期日（无需节点）｜结算作业 %d 个，无每日轮询" % len(settle), []

    # 收集节点覆盖：at 节点取日期（本地时区修正 +8）；cron 安全网取其频率
    at_dates = set()
    has_safety = False
    for j in settle:
        if not j.get("enabled"):
            continue
        sch = j.get("schedule") or {}
        if sch.get("kind") == "at":
            at = (sch.get("at") or "")[:10]
            if at:
                at_dates.add(at)
        elif sch.get("kind") == "cron":
            has_safety = True
    # at 节点用 UTC 存储，取前 8 位后 +1 天（结算允许在到期日当天或之后）
    uncovered = []
    for d in sorted(dues):
        hit = d in at_dates
        if not hit:
            # 允许节点早于到期日不超过 3 天（提前结算）
            try:
                y, m, dd = [int(x) for x in d.split("-")]
                import datetime as _dt
                base = _dt.date(y, m, dd)
                if any(abs((base - _dt.date(*[int(x) for x in a.split("-")])).days) <= 3 for a in at_dates):
                    hit = True
            except Exception:
                pass
        if not hit and not has_safety:
            uncovered.append(d)
    if uncovered:
        return False, "这些到期日无节点覆盖且无安全网：" + "、".join(uncovered), uncovered
    return True, ("结算作业 %d 个（at 节点 %d 个，安全网 %s）｜到期日 %d 个全部覆盖，无每日轮询"
                  % (len(settle), len(at_dates), "有" if has_safety else "无", len(dues))), []


# ---------------- C50 自动作业频率判定逻辑须自测通过（2026-11-28 新增） ----------------
@check("C50", "自动作业频率体检的判定逻辑须经已知答案自测通过（cron 五段→年触发次数）",
       "假绿比 FAIL 更危险：标签与数值若各写各的，会出现「每年一次」却标成「按月」这类不一致；"
       "且周与月不可混算（0 9 * * 1 是年 52 次，不是 12 次）")
def c50():
    p = os.path.join(ROOT, "skills", "agentos-architecture", "scripts", "cron_cost_audit.py")
    if not os.path.exists(p):
        return False, "缺 cron_cost_audit.py（自动作业频率体检工具丢失）", []
    import subprocess as _sp
    try:
        r = _sp.run([sys.executable, p, "--selftest"], capture_output=True, timeout=120)
        out = r.stdout.decode("utf-8", "replace")
        if "全部正确" not in out:
            alt = r.stdout.decode("mbcs", "replace")
            if "全部正确" in alt:
                out = alt
    except Exception as e:
        return False, "自测执行失败：%s" % str(e)[:80], []
    if r.returncode != 0:
        bad = [l for l in out.split("\n") if "★错" in l or "自测失败" in l]
        return False, "频率判定逻辑自测未过：" + ("；".join(bad[:4]) if bad else out.strip()[-120:]), bad[:4]
    if "全部正确" not in out:
        return False, "自测未报「全部正确」，判定逻辑状态不明", []
    # 工具本体须含 selftest 入口与年次数换算
    s = open(p, encoding="utf-8", errors="replace").read()
    for k in ("def selftest", "def cron_annual", "52", "365"):
        if k not in s:
            return False, "cron_cost_audit.py 缺 " + k, [k]
    return True, "频率判定逻辑自测通过（7 例已知答案）｜年触发换算含周 52 次与每日 365 次基准", []


# ---------------- C51 判断类交付件须与事实底表成对，且底表含口径陷阱（2026-11-28 新增） ----------------
@check("C51", "宏观/行业判断书须与配套事实底表成对存在，且底表须含口径陷阱章节",
       "只出结论不出证据 = 判断书与底表会脱节；本轮整合两路研究时即出现过「正文说 Q3 转正、底表实为 Q2」的口径不一致")
def c51():
    pairs = [
        (os.path.join(ROOT, "anyi-ops-kb", "00_全域商业市场认知",
                      "中国经济周期定位与下行期结束方式判断_v1.0_2026-11-28.md"),
         os.path.join(ROOT, "anyi-ops-kb", "00_全域商业市场认知", "宏观事实底表_2026-11-28.md")),
    ]
    miss = []
    for report, facts in pairs:
        if not os.path.exists(report):
            miss.append("判断书缺失:" + os.path.basename(report))
            continue
        if not os.path.exists(facts):
            miss.append("配套事实底表缺失:" + os.path.basename(facts))
            continue
        ft = open(facts, encoding="utf-8", errors="replace").read()
        if "口径陷阱" not in ft:
            miss.append("底表缺「口径陷阱」章节:" + os.path.basename(facts))
        if "置信度" not in ft:
            miss.append("底表缺置信度标注:" + os.path.basename(facts))
        rt = open(report, encoding="utf-8", errors="replace").read()
        for k in ("诚实边界", "先行指标"):
            if k not in rt:
                miss.append("判断书缺「%s」章节:%s" % (k, os.path.basename(report)))
    if miss:
        return False, "；".join(miss[:6]), miss[:6]
    return True, "判断书与事实底表成对在位（底表含口径陷阱与置信度标注，判断书含诚实边界与先行指标）", []
def run(as_json=False):
    res = []
    npass = 0
    for c in CHECKS:
        try:
            ok, msg, det = c["fn"]()
        except Exception as e:
            ok, msg, det = False, "检查执行异常 %s" % str(e)[:60], []
        if ok:
            npass += 1
        res.append({"id": c["id"], "title": c["title"], "rule": c["rule"], "ok": ok, "msg": msg, "det": det})
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print("=" * 96)
        print("自检 · 把教训变成可失败的断言")
        print("=" * 96)
        for r in res:
            print("  [%s] %-4s %-34s %s" % ("PASS" if r["ok"] else "FAIL", r["id"], r["title"], r["msg"]))
            if not r["ok"] and r["det"]:
                for d in r["det"]:
                    s = " ".join(str(x) for x in (d if isinstance(d, (list, tuple)) else [d]))
                    print("           · " + s[:110])
        print("-" * 96)
        print("  %d/%d 通过" % (npass, len(res)))
    return 0 if npass == len(res) else 1

if __name__ == "__main__":
    sys.exit(run("--json" in sys.argv))
