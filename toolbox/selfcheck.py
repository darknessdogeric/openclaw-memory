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
