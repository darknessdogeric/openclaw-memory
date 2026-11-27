# -*- coding: utf-8 -*-
import io, sys, os, re, json, glob, shutil as sh, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")

print("="*100); print("### A. ~/skills 是不是 Junction（决定能不能搬）"); print("="*100)
out = subprocess.run(["cmd","/c","dir","/AL", os.path.join(HOME,"skills")], capture_output=True, timeout=60)
print(out.stdout.decode("gbk","replace")[:1200])
print()
try:
    import ctypes
    from ctypes import wintypes
    p = os.path.join(HOME,"skills")
    print("  realpath(HOME/skills) =", os.path.realpath(p))
except Exception as e:
    print("  realpath 失败", str(e)[:60])

print()
print("="*100); print("### B. 依赖就绪真伪（pip / brew 的正确判法）"); print("="*100)
r = subprocess.run([sys.executable,"-m","pip","--version"], capture_output=True, timeout=90)
print("  python -m pip --version → rc=%s %s" % (r.returncode, r.stdout.decode("utf-8","replace").strip()[:70]))
print("  ★ pip 作为独立 exe 不在 PATH，但 python -m pip 可用 → 不算缺依赖")
print("  ★ brew 是 macOS 专属；本机 Windows → 平台不适用 ≠ 缺依赖")
print("  ★ arkcli / gstack 是真缺（无可执行文件、无 Python 包替代）")
for b in ["arkcli","gstack"]:
    print("     which(%s) = %r" % (b, sh.which(b)))
