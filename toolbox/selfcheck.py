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
