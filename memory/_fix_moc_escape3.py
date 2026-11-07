"""彻底重写根 MOC 追加段 (Python 直写, 绕开 PowerShell 反引号转义)"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = Path(r"D:\B166ER-openclaw\workspace\anyi-ops-kb\00_MOC.md")
raw = p.read_bytes()
c = raw.decode("utf-8", errors="replace")

# 1) 定位并切掉损坏的追加段
marker = "## ?? 我要分析一笔交易"
i = c.find(marker)
if i < 0:
    print("未找到标记, 检查尾部")
    print(repr(c[-800:]))
    sys.exit(1)
head = c[:i].rstrip()
print(f"切掉损坏段: {len(c) - len(head)} 字符")

# 2) 清理头部可能残留的 NUL / 转义残留
head = head.replace("\x00", "").replace("\\x00", "")

# 3) 用 Python 直写新段 (无 PowerShell 转义)
NEW = """

---

## ?? 我要分析一笔交易 / 一个资产值不值 / 钱怎么还（资本·资产·金融侧）

- **看 `00_全域商业市场认知/02_资本资产金融/00_MOC_资本资产金融知识库_v1.0_2026-10-25.md`** — 索引 + 使用说明（先读这个）
- **判断"买贵没"必走四层** → `00_全域商业市场认知/02_资本资产金融/04_酒店资产四层定价框架_v1.0_2026-10-25.md`（可比倍数 → 历史锚点 → 现金流折现 → 管道期权）
- 谈物业/盘活/减值/REITs → `00_全域商业市场认知/02_资本资产金融/01_资产维度体系_v1.0_2026-10-25.md`（7 组 63 项，含轻重分离 G 组）
- 谈融资/并购/国资交易/退出 → `00_全域商业市场认知/02_资本资产金融/02_资本维度体系_v1.0_2026-10-25.md`（7 组 68 项，含国资交易流程 F 组 12 项）
- 谈盈利/现金流/偿债/财务体系 → `00_全域商业市场认知/02_资本资产金融/03_金融维度体系_v1.0_2026-10-25.md`（7 组 70 项，含业财结合 G 组）
- 爬资本侧数据 → `00_全域商业市场认知/02_资本资产金融/05_信源矩阵扩展KLM_资本资产金融_v1.0_2026-10-25.md`（K 资本市场 / L 资产不动产 / M 金融银行，与主矩阵 A–J 并行 = A–M）
- 看完整范例 → `00_全域商业市场认知/02_资本资产金融/06_交易案例库/C001_同程收购万达酒管_四层拆解_v1.0_2026-10-25.md`
"""
p.write_text(head + NEW, encoding="utf-8")

# 4) 校验
chk = p.read_text(encoding="utf-8")
print(f"文件大小: {p.stat().st_size} bytes")
print("NUL 残留:", "有 ❌" if "\x00" in chk else "无 ✅")
print("反斜杠转义残留:", "有 ❌" if "\\x00" in chk else "无 ✅")
print("反引号数:", chk.count("`"))
seg = chk[chk.find(marker):]
print("维度数 63/70:", ("63" in seg) and ("70" in seg))
out = Path(r"D:\B166ER-openclaw\workspace\memory\_moc_check.txt")
out.write_text(seg, encoding="utf-8")
print("预览写入:", out)
