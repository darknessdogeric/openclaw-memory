"""修复根 MOC 追加段中的 PowerShell 转义残留 (\\x002 -> `)"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = Path(r"D:\B166ER-openclaw\workspace\anyi-ops-kb\00_MOC.md")
c = p.read_text(encoding="utf-8")

before = c.count("\\x002")
c = c.replace("\\x002", "`")
# 收尾可能多了个反斜杠, 修成正常闭合
c = c.replace(".md\\（", ".md`（")
c = c.replace(".md\\（", ".md`（")
p.write_text(c, encoding="utf-8")
print(f"修复 \\x002 残留: {before} 处")
print(f"文件大小: {p.stat().st_size} bytes")

# 验证新段落渲染
idx = c.find("资本·资产·金融侧")
if idx > 0:
    seg = c[idx - 200: idx + 1600]
    print("\n=== 修复后段落预览 ===")
    for line in seg.splitlines():
        if line.strip():
            print("  " + line[:150])
