"""彻底修复根 MOC 追加段:
1) PowerShell 转义残留 \\x00N -> 反引号 (N 递增, 需正则)
2) 修正维度数 55->63, 60->70
3) 修正结尾多余反斜杠
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = Path(r"D:\B166ER-openclaw\workspace\anyi-ops-kb\00_MOC.md")
c = p.read_text(encoding="utf-8")

n_esc = len(re.findall(r"\\x00\d", c))
c = re.sub(r"\\x00\d", "`", c)

# 结尾多余反斜杠: .md\  -> .md`
c = re.sub(r"\.md\\(?![/\\])", ".md`", c)
# 反引号后紧跟中文标点时的配对检查
c = c.replace("`（", "`（").replace("`（", "`（")

# 维度数修正
c = c.replace("（7 组 55 项", "（7 组 63 项")
c = c.replace("（7 组 60 项", "（7 组 70 项")
c = c.replace("（7 组 55 项）", "（7 组 63 项）")
c = c.replace("（7 组 60 项）", "（7 组 70 项）")

p.write_text(c, encoding="utf-8")
print(f"转义残留修复: {n_esc} 处")
print(f"文件大小: {p.stat().st_size} bytes")

# 输出新段落（写到文件避免控制台编码问题）
idx = c.find("资本·资产·金融侧")
seg = c[max(0, idx - 120): idx + 1700]
out = Path(r"D:\B166ER-openclaw\workspace\memory\_moc_check.txt")
out.write_text(seg, encoding="utf-8")
print(f"预览写入: {out}")

# 校验: 段落内不应再有 \x00
tail = c[idx - 200:] if idx > 0 else ""
print("残留检查:", "OK 无残留" if "\\x00" not in tail else "仍有残留!")
print("维度数检查:", "63" in tail and "70" in tail)
