# -*- coding: utf-8 -*-
import io, sys, os, re, ast
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
SC = os.path.join(ROOT,"toolbox","selfcheck.py")
t = open(SC, encoding="utf-8", errors="replace").read()
assert "C13" not in t, "已存在 C13，勿重复插入"

NEW = '''# ---------------- C13 技能注册表完备（2026-11-18 技能库审计新增） ----------------
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
    for base in (os.path.join(ROOT,"skills"), os.path.join(HOME,"skills"), os.path.join(HOME,".claude","skills")):
        if not os.path.isdir(base):
            continue
        for f in glob.glob(os.path.join(base,"*","SKILL.md")):
            d = os.path.basename(os.path.dirname(f))
            if d.startswith("_"): continue
            tx = open(f, encoding="utf-8", errors="replace").read()
            m = re.search(r"^name:\\s*(.+)$", tx, re.M)
            disk.add((m.group(1).strip() if m else d).strip('"\\''))
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

'''

anchor = "def run(as_json=False):"
assert anchor in t
t2 = t.replace(anchor, NEW + anchor, 1)
ast.parse(t2)
open(SC,"w",encoding="utf-8",newline="\n").write(t2)
print("✔ 已插入 C13-C18 六条断言，selfcheck.py %d B → %d B" % (len(t), len(t2)))
