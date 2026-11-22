# -*- coding: utf-8 -*-
"""合并立项报告 md → 转 docx → 归位 → 同步 memory/README"""
import io, os, sys, glob, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert

NAME = "总府皇冠改造_立项报告_v1.0_2026-11-08"
p1 = os.path.join(KB, "_calc", "_launch_p1.md")
p2 = os.path.join(KB, "_calc", "_launch_p2.md")
assert os.path.exists(p1) and os.path.exists(p2)
body = open(p1, encoding="utf-8").read().rstrip() + "\n\n" + open(p2, encoding="utf-8").read().lstrip()
md = os.path.join(KB, NAME + ".md")
open(md, "w", encoding="utf-8").write(body)
print("MD merged: %d bytes" % len(body.encode("utf-8")))

out = os.path.join(REP, NAME + ".docx")
convert(md, out)
print("DOCX: %s  %.1f KB" % (os.path.basename(out), os.path.getsize(out)/1024))

for f in glob.glob(os.path.join(KB, "测算与中间产物", "*.xlsx")):
    shutil.copy2(f, os.path.join(CAL, os.path.basename(f)))
print("XLSX synced:", len(glob.glob(os.path.join(CAL, "*.xlsx"))))

# 清临时分片
for f in (p1, p2):
    os.remove(f)

# memory
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-08.md"
add = """

---

## 🏗 总府皇冠改造 · 立项报告 + 三方向全维度 EXCEL（完成）

### 交付物（已归位到产业发展部项目文件夹）
| 文件 | 位置 | 规模 |
|---|---|---|
| 总府皇冠改造_立项报告_v1.0_2026-11-08.docx | 改造报告交付 | 约 60 KB |
| 总府皇冠改造_立项经济测算_方向一_沿用皇冠_全维度_v1.0_2026-11-08.xlsx | 测算与中间产物 | 47.8 KB / 13 Sheet |
| 方向二_洲至奢选_全维度 | 测算与中间产物 | 48.5 KB / 13 Sheet |
| 方向三_外部奢华品牌_全维度 | 测算与中间产物 | 48.1 KB / 13 Sheet |
| 三方向对比与国资口径校验_v1.0_2026-11-08.xlsx | 测算与中间产物 | 15.8 KB / 6 Sheet |

### ⭐⭐⭐ 立项报告核心结论
1. ⭐ **必要性四来源互证**：规划刚性｜消防机电人防硬缺口｜**品牌方三年审计 95.92%→74.0%→69.6%**｜出租率不动而 ADR −28%
2. ⭐ **可行性五维全成立**（技术/财务/品牌/合规/政策）
3. ⭐⭐⭐ **完全不停业 = 不可能**（消防报警系统级 + 喷淋立管 + 冷源主机三项硬约束）；**短停业技术可行、品牌方已明确"可以接受"**；⭐ **真正卡点是消防审查机构是否认可分区验收（R-01），与品牌谈判无关，现在就能问**
4. ⭐⭐⭐⭐ **那个问询值 6,857 万**：方向二 一次全停业 IRR 9.49% → 分期开业 IRR **21.48%**、NPV +2,944→+16,597 万、回收 9.7→5.5 年
5. ⭐⭐⭐ **品牌路径只有两条**（洲际方书面）：①全新一代摩登时尚皇冠假日 ②洲至奢选（需 3改2/40㎡+）；改造内容 80% 共通 → 按并集一次做到位
6. ⭐⭐⭐⭐ **"做减法"与国资同向**：415→268 间（−35%）而总建面不变 → 同投资额提升单间品质 → 正是"避免超标准建设"的正解
7. ⭐⭐⭐⭐ **三方向（中性 20 年）**：方向二 IRR 9.49%/NPV +2,944/回收 9.7 年（唯一双正）｜方向一 8.16%/+192/10.3 年（勉强）｜方向三 5.37%/−7,149/12.6 年（不达标）
8. ⭐⭐⭐⭐ **保守面必须一起报**：保守情景三方向 IRR 全部 <8%（4.03/4.74/0.94%），且**全部未含融资年利息**；⭐ **决定成败的是"建完能卖什么价"，不是"省多少钱建"**

### ⭐⭐⭐ 本轮新增的全网数据（全部可溯源）
- **HMA 制度性费率分解**（Hotel Development Guide, Darren Blanchard, 2026-10）：base 2–4%｜incentive 5–15%｜marketing 1–3%｜⭐ **pre-opening（此前漏计，已入 CAPEX）**｜⭐ **"基础费与盈利无关、照付"→ 停业期基础费处理必须是显性测算项**
- **2025 全国酒店四连降**：星级 7,586 家（−130）｜营收 1,448 亿（−109 亿）｜ADR 360.2｜OCC 46.8%｜⭐ **五星商务协议客 40%→不足30%、散客 24%→45%**｜五星 736 家 OCC 62.5% ADR 755｜⭐ **701–1000 元是挤压带**
- **成都**：春熙路—太古里 12 家 ADR 1,280/OCC 76.3%/RevPAR 977｜全国奢华 OCC 72.3% ADR 985｜近郊 MSI<1｜⭐ **成都顶奢基础房型 45–65 ㎡**（瑞吉65/丽思48/华尔道夫50-55/尼依格罗50/W45）
- **丽晶成都**：2026-07-15 签约、**2029Q3 开业、180 间、224m**；⭐ **"GOP 率 35%–45% 行业标准"锚点**
- **洲至奢选棕榈泉**：原费尔蒙 336 间、雅高到期未续约后业主引入、⭐ **"以蜀绣为魂"** = 在地文化实物范式

### ⚠️ v6 引擎四个 bug（自造，已修）
① op_year 数的是运营"月"不是"年"（爬坡从第 1 个月就衰减）② 运营期历月错位 ③ 时间轴漏了部门收入字段 ④ **年度 IT/培训费被按月重复计 12 次**
⭐ **教训：造完引擎必须做"手算校验"** —— 方向二 GOP 率应为 46.2%、品牌费率 10.3%（与已发布 v3 一致），算出来 6.2% 就是错的。

### ⚠️⚠️ 两个环境级教训（本轮踩到）
⭐⭐ **① PowerShell here-string 写中文文件名的落盘不可靠** —— 两次写入报告 md，PowerShell 回报成功且 Get-Item 读到字节数，但**文件实际未落在目标目录**（全盘按字节数搜索无果）。⭐⭐ **正解：一律用 write 全局写盘 + Python 内部处理路径，不经 PowerShell。**
⭐⭐ **② PowerShell 把中文路径传给原生 exe 时按 ANSI 代码页转换 → 路径被改写、FileNotFoundError。** ⭐⭐ **正解：中文路径一律由 Python 进程内部处理（glob / in-process 调用），不经命令行传参。**
<!-- project: github.com/darknessdogeric/openclaw-memory -->

---
"""
os.makedirs(os.path.dirname(MEM), exist_ok=True)
mode = "a" if os.path.exists(MEM) else "w"
with open(MEM, mode, encoding="utf-8") as f:
    f.write(add)
print("MEM ok")

RM = os.path.join(KB, "00_项目总览_README.md")
rm_add = """

| **立项报告** | v1.0 | ✅ docx | ⭐⭐⭐⭐ **必要性/可行性/三方向时间与经济测算/品牌筛选/细致市场调研/国资口径/不停业论证** 全部成文；⭐⭐⭐ **核心：完全不停业=不可能、短停业技术可行且品牌方已明确"可以接受"、真正卡点是消防审查机构（R-01）** |
| **立项经济测算 EXCEL（4 份）** | v1.0 | ✅ xlsx | 三方向各 **13 Sheet**（含 243 行月度模型、开工月份矩阵、分期开业情景、敏感性、国资校验、时间计划、不停业论证）+ 三方向对比 6 Sheet |

### ⭐ 立项关键结论速查（2026-11-08）
| 项 | 方向一 沿用皇冠 | 方向二 洲至奢选 | 方向三 外部奢牌 |
|---|---|---|---|
| CAPEX | 4,735 万 | 12,355 万 | 23,515 万 |
| 停业月数 / 损失 | 14 / 11,732 万 | 18 / 15,273 万 | 20 / 16,956 万 |
| 中性 IRR（20 年） | 8.16% | ⭐ **9.49%** | 5.37% |
| NPV @8% | +192 万 | ⭐ **+2,944 万** | −7,149 万 |
| ⭐ 分期开业 IRR | 不适用 | ⭐ **21.48%** | ⭐ **13.71%** |

<!-- project: github.com/darknessdogeric/openclaw-memory -->
"""
with open(RM, "a", encoding="utf-8") as f:
    f.write(rm_add)
print("README ok")

print("\n=== 改造报告交付 ===")
for f in sorted(glob.glob(os.path.join(REP, "*"))):
    print("  %-74s %7.1f KB" % (os.path.basename(f), os.path.getsize(f)/1024))
