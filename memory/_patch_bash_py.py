"""给 ppt-deck-builder-pro 的 bash 脚本加可移植的 python 探测
问题: Windows Git Bash 里 `python3` 解析到 Microsoft Store 桩 (WindowsApps/python3),
      调用即静默退出 49 (无输出)。Linux 只有一个 python3, 所以不能写死。
修法: PY="$(command -v python3 || command -v python)" 然后统一用 "$PY"
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SCRIPTS = Path(r"D:\B166ER-openclaw\workspace\skills\ppt-deck-builder-pro\scripts")

RESOLVER = (
    '# Portable python resolver: prefer python3, fall back to python.\n'
    '# (Windows Git Bash: `python3` may resolve to the Microsoft Store stub which\n'
    '#  exits silently with code 49, so the fallback matters.)\n'
    'PY="$(command -v python3 || command -v python || true)"\n'
    'if [[ -z "$PY" ]]; then echo "python not found in PATH" >&2; exit 127; fi\n'
)

for sh in sorted(SCRIPTS.glob("*.sh")):
    text = sh.read_text(encoding="utf-8")
    if "PY=\"$(command -v python3" in text:
        print(f"  [skip] {sh.name} 已处理")
        continue

    # 1) 替换调用: python3 " -> "$PY" "
    new = re.sub(r'(?<![\w/])python3(\s+")', r'"$PY"\1', text)
    new = re.sub(r'(?<![\w/])python3(\s+-)', r'"$PY"\1', new)
    new = new.replace("python3 - <<'PY'", '"$PY" - <<\'PY\'')

    if new == text:
        print(f"  [skip] {sh.name} 无 python3 调用")
        continue

    # 2) 在 shebang 之后插入 resolver
    lines = new.splitlines(keepends=True)
    ins = 0
    for i, l in enumerate(lines):
        if l.startswith("#!"):
            ins = i + 1
            break
    # 跳过 shebang 后的空行
    while ins < len(lines) and lines[ins].strip() == "":
        ins += 1
    lines.insert(ins, RESOLVER + "\n")
    out = "".join(lines)
    sh.write_text(out, encoding="utf-8")
    n = out.count('"$PY"')
    print(f"  [OK] {sh.name}  替换 {n} 处 python3 -> \"$PY\"")

print("\n完成")
