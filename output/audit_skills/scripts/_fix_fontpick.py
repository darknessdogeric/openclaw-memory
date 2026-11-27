"""修 fontpick: 顶层 case 分支里误用 local (bash 只允许函数内用)"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = Path(r"D:\B166ER-openclaw\workspace\skills\fontpick\scripts\script.sh")
src = p.read_text(encoding="utf-8")
lines = src.splitlines()

# 定位顶层 case 起点
case_start = None
for i, l in enumerate(lines):
    if re.match(r"^case\s", l):
        case_start = i
        break
if case_start is None:
    print("未找到顶层 case, 退出")
    sys.exit(1)

print(f"顶层 case 起始行: L{case_start+1}  {lines[case_start].strip()}")

fixed = 0
for i in range(case_start, len(lines)):
    l = lines[i]
    # 顶层分支里的 `local xxx=...` -> `xxx=...`
    m = re.match(r"^(\s*)local\s+(\w+)=(.*)$", l)
    if m:
        indent, name, val = m.groups()
        lines[i] = f"{indent}{name}={val}"
        fixed += 1
    else:
        # 顶层分支里的 `local xxx` (单独声明) -> 去掉 local
        m2 = re.match(r"^(\s*)local\s+(\w+)\s*$", l)
        if m2:
            indent, name = m2.groups()
            lines[i] = f"{indent}{name}"
            fixed += 1

p.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"已修复 {fixed} 处误用的 local")

# 验证语法
import subprocess
r = subprocess.run([r"D:\Git\usr\bin\bash.exe", "-n", str(p)],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("语法检查:", "PASS ✅" if r.returncode == 0 else f"FAIL ❌\n{r.stderr}")

# 实测
for cmd in ["palette #1E3A5F", "contrast #1E3A5F #F2EDE3", "harmonize #1E3A5F", "swatch #C8963E"]:
    print(f"\n--- fontpick {cmd} ---")
    r2 = subprocess.run([r"D:\Git\usr\bin\bash.exe", str(p)] + cmd.split(),
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r2.stdout or "") + (r2.stderr or "")
    for line in out.splitlines()[:6]:
        print("   " + line)
