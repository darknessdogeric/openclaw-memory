"""修 resolver: command -v python3 在 Windows 会成功返回 Microsoft Store 桩,
必须实跑 --version 验证可用性, 才能真正回退到 python。
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SCRIPTS = Path(r"D:\B166ER-openclaw\workspace\skills\ppt-deck-builder-pro\scripts")

OLD = (
    '# Portable python resolver: prefer python3, fall back to python.\n'
    '# (Windows Git Bash: `python3` may resolve to the Microsoft Store stub which\n'
    '#  exits silently with code 49, so the fallback matters.)\n'
    'PY="$(command -v python3 || command -v python || true)"\n'
    'if [[ -z "$PY" ]]; then echo "python not found in PATH" >&2; exit 127; fi\n'
)

NEW = (
    '# Portable python resolver.\n'
    '# NOTE: `command -v python3` SUCCEEDS on Windows Git Bash even when it points at\n'
    '# the Microsoft Store stub (WindowsApps/python3), which exits silently with code 49.\n'
    '# So each candidate must be proven runnable (`--version` actually works) before use.\n'
    'PY=""\n'
    'for _pycand in python3 python; do\n'
    '  if command -v "$_pycand" >/dev/null 2>&1 && "$_pycand" --version >/dev/null 2>&1; then\n'
    '    PY="$(command -v "$_pycand")"\n'
    '    break\n'
    '  fi\n'
    'done\n'
    'if [[ -z "$PY" ]]; then\n'
    '  echo "ERROR: no working python found (tried python3, python)" >&2\n'
    '  exit 127\n'
    'fi\n'
)

for sh in sorted(SCRIPTS.glob("*.sh")):
    text = sh.read_text(encoding="utf-8")
    if OLD not in text:
        print(f"  [skip] {sh.name} 无旧 resolver")
        continue
    sh.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print(f"  [OK] {sh.name} resolver 已换成'实跑验证'版")

print("\n完成")
