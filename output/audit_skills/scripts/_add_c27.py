# -*- coding: utf-8 -*-
"""_add_c27.py - 以 C27 安装纹样底库断言

★ ★ 用 @@TOKEN@@ + .replace()，不用 %/format（遵守 2026-11-18 立下的模板纪律）
★ ★ 并行会话正在改同一个 selfcheck.py —— 写入后必须验：原有断言一条不少、只多 1 条
"""
import io
import sys
import os
import re
import ast
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
SC = os.path.join(ROOT, "toolbox", "selfcheck.py")

t = open(SC, encoding="utf-8", errors="replace").read()

if "纹样底库须存在" in t:
    print("· 纹样断言已存在，跳过")
    raise SystemExit(0)

before_ids = re.findall(r'@check\(\s*"(C\d+)"', t)
nxt = max(int(x[1:]) for x in before_ids) + 1
CID = "C" + str(nxt).zfill(2)
NUM = str(nxt)
print("原有 %d 条 ｜ 新增编号 %s" % (len(before_ids), CID))

BLOCK = '''# ---------------- C@CID@ 纹样底库可检索（2026-11-19 纹样内化新增） ----------------
@check("@CID@", "纹样底库须存在、可检索、且技能已入注册表", "《纹样设计速查手册》内化后必须能被路由调用，否则等于没吸收")
def c@NUM@():
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

'''
BLOCK = BLOCK.replace("@CID@", CID).replace("@NUM@", NUM)

anchor = "def run(as_json=False):"
if anchor not in t:
    print("★ 锚点未命中（并行会话可能改了该文件）")
    raise SystemExit(1)
t2 = t.replace(anchor, BLOCK + anchor, 1)
ast.parse(t2)
open(SC, "w", encoding="utf-8", newline="\n").write(t2)

after_ids = re.findall(r'@check\(\s*"(C\d+)"', t2)
lost = [x for x in before_ids if x not in after_ids]
print("✔ 已插入 %s ｜ 写后 %d 条（原 %d）" % (CID, len(after_ids), len(before_ids)))
if lost:
    print("  ★★★ 原有断言丢失: %s —— 并行会话的改动被我覆盖了！" % lost)
    print("  → 立即回滚: git checkout 不可用时，从备份恢复")
    raise SystemExit(2)
print("  ✔ 原有 %d 条断言全部保留，无覆盖" % len(before_ids))

print()
print("=" * 96)
r = subprocess.run([sys.executable, SC], capture_output=True, timeout=400)
print(r.stdout.decode("utf-8", "replace"))
print("退出码:", r.returncode)
