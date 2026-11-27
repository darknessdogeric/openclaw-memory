# -*- coding: utf-8 -*-
"""_addchk20.py - 为工具层新增断言 C20/C21/C22 并重跑自检"""
import io
import sys
import os
import re
import ast
import json
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
SC = os.path.join(ROOT, "toolbox", "selfcheck.py")

NEW = '''# ---------------- C20 工具索引完备（2026-11-18 工具层治理新增） ----------------
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

'''

t = open(SC, encoding="utf-8", errors="replace").read()
if "C20" not in t:
    anchor = "def run(as_json=False):"
    assert anchor in t
    t = t.replace(anchor, NEW + anchor, 1)
    ast.parse(t)
    open(SC, "w", encoding="utf-8", newline="\n").write(t)
    print("✔ 已插入 C20/C21/C22，selfcheck.py %d B" % len(t))
else:
    print("· C20 已存在，跳过插入")

print()
print("=" * 96)
print("路由实测（三层：工作流 / 技能 / 工具）")
print("=" * 96)
r = subprocess.run([sys.executable, os.path.join(ROOT, "toolbox", "skill_router.py"),
                    "--task", "把 md 转成带表格的 docx"], capture_output=True, timeout=150)
print(r.stdout.decode("utf-8", "replace"))

print()
print("=" * 96)
print("自建前查重实测 --check")
print("=" * 96)
r2 = subprocess.run([sys.executable, os.path.join(ROOT, "toolbox", "skill_router.py"),
                     "--check", "md_to_docx.py"], capture_output=True, timeout=150)
print(r2.stdout.decode("utf-8", "replace"))

print()
print("=" * 96)
print("全量自检")
print("=" * 96)
r3 = subprocess.run([sys.executable, SC], capture_output=True, timeout=400)
print(r3.stdout.decode("utf-8", "replace"))
print("退出码:", r3.returncode)
