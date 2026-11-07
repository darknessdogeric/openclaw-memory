"""安装 diagram-design skill (仅取 skills/diagram-design/, 不拉 37MB 全仓)
安装路径: workspace/skills/diagram-design/
验证: 文件数 / frontmatter / 无第三方依赖 / self_check.py 可跑 / 无网络调用
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = "cathrynlavery/diagram-design"
WORK = Path(r"D:\B166ER-openclaw\workspace")
SKILLS = WORK / "skills"
DEST = SKILLS / "diagram-design"
GIT = r"C:\Program Files\Git\cmd\git.exe" if Path(r"C:\Program Files\Git\cmd\git.exe").exists() else "git"
TMP = Path(r"D:\B166ER-openclaw\workspace\memory\_dd_clone")

print("=" * 74)
print("一、ClawHub 是否有官方收录")
print("=" * 74)
r = subprocess.run([r"C:\Users\ericz\AppData\Roaming\npm\clawhub.cmd", "search", "diagram-design"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
out = "\n".join(l for l in (r.stdout or "").splitlines()
                if l.strip() and "node.exe" not in l and "所在位置" not in l
                and "CategoryInfo" not in l and "FullyQualifiedErrorId" not in l
                and not l.startswith("  + "))
print(out[:600] or "  (ClawHub 无收录 → 走 GitHub 直接安装)")

print()
print("=" * 74)
print("二、稀疏克隆 (只取 skills/diagram-design/)")
print("=" * 74)
if TMP.exists():
    shutil.rmtree(TMP, ignore_errors=True)
TMP.mkdir(parents=True, exist_ok=True)
cmds = [
    ["clone", "--filter=blob:none", "--no-checkout", "--depth", "1",
     f"https://github.com/{REPO}.git", str(TMP)],
    ["-C", str(TMP), "sparse-checkout", "init", "--cone"],
    ["-C", str(TMP), "sparse-checkout", "set", "skills/diagram-design"],
    ["-C", str(TMP), "checkout"],
]
for c in cmds:
    p = subprocess.run([GIT] + c,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print("  ❌", " ".join(c[:4]), "->", (p.stderr or "")[:200])
        sys.exit(1)
print("  ✅ 克隆完成")

src = TMP / "skills" / "diagram-design"
if not src.exists():
    print("  ❌ 未取到 skills/diagram-design")
    sys.exit(1)

files = [p for p in src.rglob("*") if p.is_file()]
total_kb = sum(p.stat().st_size for p in files) / 1024
print(f"  源: {len(files)} 文件, {total_kb:,.0f} KB")

print()
print("=" * 74)
print("三、安装到 workspace/skills/diagram-design/")
print("=" * 74)
if DEST.exists():
    shutil.rmtree(DEST, ignore_errors=True)
shutil.copytree(src, DEST, ignore=shutil.ignore_patterns(".git"))
inst = [p for p in DEST.rglob("*") if p.is_file()]
print(f"  ✅ 已安装: {DEST}")
print(f"     {len(inst)} 文件, {sum(p.stat().st_size for p in inst)/1024:,.0f} KB")
for sub in ("references", "assets", "scripts"):
    d = DEST / sub
    n = len(list(d.rglob("*"))) if d.exists() else 0
    print(f"     {sub+'/':<12} {n} 项")

print()
print("=" * 74)
print("四、安装后验证")
print("=" * 74)
sk = (DEST / "SKILL.md").read_text(encoding="utf-8")
m = re.search(r"^---\s*\n(.*?)\n---", sk, re.S)
print("  frontmatter:", "✅ 有效" if m else "❌ 无")
if m:
    for line in m.group(1).splitlines()[:8]:
        print("    " + line[:110])

# 第三方依赖检查
dep = [p for p in inst if any(x in p.name.lower() for x in
       ("requirements", "package.json", "package-lock", "pyproject", ".lock", "poetry"))]
print(f"  第三方依赖文件: {'❌ ' + str(dep) if dep else '✅ 无 (零依赖)'}")

# 网络外发检查 (全部运行时脚本)
NET = re.compile(r"requests\.(get|post|put)|urllib\.request|urlopen|http\.client|socket\.(socket|create_connection)")
net_hits = []
for p in (DEST / "scripts").glob("*.py"):
    t = p.read_text(encoding="utf-8", errors="replace")
    if NET.search(t):
        net_hits.append(p.name)
print(f"  运行时脚本网络外发: {'❌ ' + str(net_hits) if net_hits else '✅ 0 处 (纯离线)'}")

# 跑一次自带校验脚本
sc = DEST / "scripts" / "self_check.py"
ex = None
for p in (DEST / "assets").glob("example-architecture.html"):
    ex = p
    break
if sc.exists() and ex:
    p = subprocess.run([sys.executable, str(sc), str(ex)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=str(DEST))
    tail = (p.stdout or "").strip().splitlines()[-6:]
    print(f"  self_check.py 跑通: exit={p.returncode}")
    for l in tail:
        print("    " + l[:140])

# 清理克隆
shutil.rmtree(TMP, ignore_errors=True)
print("\n  ✅ 临时克隆已清理")
print(f"\nDESKTOP/工作区: {DEST}")
