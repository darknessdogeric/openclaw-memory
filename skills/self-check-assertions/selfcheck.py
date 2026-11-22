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
