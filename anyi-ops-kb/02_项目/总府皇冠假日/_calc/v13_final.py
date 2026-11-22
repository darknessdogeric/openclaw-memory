# -*- coding: utf-8 -*-
"""v13 收官：补第八节表列、填剩余破折号、清旧值、出 v3.2、终检、同步 memory/README"""
import io, os, sys, re, json, glob, shutil
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "v13.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")

MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v3.2_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ══ ① 第六章八方案造价总表：补「相对集团 1.8 亿额度」列 ══
OVER = {"S1": 3313.6, "S2": 3288.0, "S3": 11171.3, "S4": 10190.7,
        "S5": 21550.7, "S6": 26381.3, "S7": 38850.9, "S8": 32276.7}
lines = t.split("\n")
n = 0
for i, l in enumerate(lines):
    m = re.match(r"^\| (S[1-8]) \| ([^|]+)\|([^|]+)\|([^|]+)\|(\d+) \| (\d+) \| ([\d,\.]+) \| ([\d,\.]+) \| ([\d,\.]+) \| ([\d,\.]+) \|$", l)
    if m:
        k = m.group(1)
        lines[i] = l[:-1].rstrip() + " +%s |" % format(OVER[k], ",.1f")
        n += 1
t = "\n".join(lines)
L("第八节表补列行数:", n)

# ══ ② 第五章剩余破折号 ══
DASH = re.compile(r"^\|(\s*)—(\s*)\|")
FILL = [
 ("集团口径静态回收期 13.89 年", "改造量集中在公共区域，客房与机电可分期实施以缓解现金流压力"),
 ("集团口径静态回收期 12.57 年", "定价天花板高于沿用皇冠，长期提价空间更大"),
 ("减房使全口径内部收益率由 4.60% 降至", "可先以 S1 为基准，仅对不达标房型局部 3 改 2，改造量可控"),
]
lines = t.split("\n")
f = 0
for i, l in enumerate(lines):
    if not DASH.match(l):
        continue
    for kw, txt in FILL:
        if kw in l:
            lines[i] = DASH.sub(lambda m: "| %s |" % txt, l, count=1)
            f += 1
            L("[FILL]", esc(kw[:24]))
            break
t = "\n".join(lines)
L("补破折号:", f)

# ══ ③ 旧值 5.37% ══
for i, l in enumerate(t.split("\n")):
    if "5.37%" in l:
        L("旧值所在 L%d | %s" % (i, esc(l.strip()[:200])))

open(MD, "w", encoding="utf-8").write(t)

# ══ ④ 出 Word + 大纲 + 终检 ══
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v3.2_2026-11-14.docx")
convert(MD, out)
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
TMP = os.path.join(T, "_v32d.docx")
d = Document(out)
def set_outline(p, lvl):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:outlineLvl")):
        pPr.remove(old)
    e = OxmlElement("w:outlineLvl"); e.set(qn("w:val"), str(lvl)); pPr.append(e)
cnt = {"0": 0, "1": 0, "2": 0}
for p in d.paragraphs:
    tx = p.text.strip()
    if not tx or len(tx) > 60: continue
    if re.match(r"^\d+\. [一二三四五六七八九十]+、", tx): continue
    lvl = None
    if tx == "关于总府皇冠假日酒店改造升级工作思路的报告": lvl = 0
    elif re.match(r"^[一二三四五六七八九十]+、\S", tx): lvl = 1
    elif re.match(r"^（[一二三四五六七八九十]+）", tx): lvl = 2
    elif re.match(r"^\d+\.\d+\s", tx): lvl = 2
    if lvl is not None:
        set_outline(p, lvl); p.paragraph_format.keep_with_next = True; cnt[str(lvl)] += 1
d.save(TMP); shutil.move(TMP, out)
L("DOCX %.1f KB | 大纲 L0=%d L1=%d L2=%d" % (os.path.getsize(out)/1024, cnt["0"], cnt["1"], cnt["2"]))
d = Document(out)
blank = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "\u2014", "-", "\uff0f", "/"):
                blank += 1
                L("  BLANK 表%d 行%d 列%d : %s" % (ti, ri, ci, " || ".join(cell.text.strip()[:22] for cell in row.cells)))
L("docx: 段落 %d / 表格 %d / 空白格 %d" % (len(d.paragraphs), len(d.tables), blank))
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
L("emoji:", len(re.findall(EMO, t)), "| ??:", len(re.findall(r"\?\?", t)), "| 单问号:", len(re.findall(r"\?(?=[\d(（])", t)))
bad = [l for l in t.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 95)]
L("标题异常:", len(bad))
m = re.search(r"^## 目录\n", t, re.M)
ls = t[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc_items = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
body_items = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("目录与正文一致:", toc_items == body_items, "| 目录", len(toc_items), "正文", len(body_items))

# ══ ⑤ 清理旧 docx ══
for n in ("总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx",
          "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.docx",
          "总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.docx",
          "总府皇冠改造_立项报告_集团汇报件_v3.1_2026-11-14.docx"):
    p = os.path.join(REP, n)
    if os.path.exists(p):
        try:
            os.remove(p); L("removed", n)
        except Exception:
            L("[仍被 Word 占用]", n)
for f in glob.glob(os.path.join(REP, "~$*")):
    try:
        os.remove(f); L("removed lock", os.path.basename(f))
    except Exception:
        L("[锁文件残留]", os.path.basename(f))

# ══ ⑥ memory + README ══
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
open(MEM, "a", encoding="utf-8").write("""

---

## 10:40 ⭐⭐⭐ 造价三段式重构 + 三品牌标准完整造价（v3.2）

**交付**：改造报告交付\\总府皇冠改造_立项报告_集团汇报件_v3.2_2026-11-14.docx（98 KB，60 张表 0 空白）
测算与中间产物\\总府皇冠改造_完整造价构成表_v1.0_2026-11-14.xlsx（29.1 KB / 10 个工作表）

### ⭐ 造价构成按三段式重构（Eric 指示的组成方式）
**段一 停业损失 ＋ 段二 机电水电强弱电及隐蔽工程（品牌无关）＋ 段三 装修改造造价（品牌相关）**。
段二在八方案间几乎不变，段一随停业月数变化，段三才是品牌决策变量 —— 混在一起列示会把品牌决策的真实增量淹没在共同成本里。

### ⭐⭐⭐ 挖到最硬底稿：业主方 43 项自编造价（18,000 万，与洲际 PIP 勾稽）
来源：总府实业〔2024〕11 号《总府皇冠假日酒店排危升级改造专题报告》第三章。**合计 18,000 万元，与洲际 PIP 原件 18,000—20,000 万元口径完全吻合；其改造面积 44,600 ㎡ 与集团 715 定稿专栏 6 一致。** 天然三分类：设施设备 15 项 6,950（品牌无关）＋ 二次装修 6 项 8,700（品牌相关）＋ 其他 4 项 2,350（拆除 300／设计监理 520／消防 1,400／监控 130）。
**⭐ 它暴露了上一版最大漏项：装修 8,700 万里客房 430 间占 6,000 万（13.95 万/间），而我上版给沿用皇冠客房只算 2,904 万 —— 差一半。**
编制依据：《建设项目经济评价方法与参数（第三版）》《四川省建设工程单位计算表》《全国统一安装工程概算定额四川省单位估价表》。

### 三段式造价（万元）
| 方案 | 停业损失 | 机电水电强弱电隐蔽 | 装修改造 | 改造投资合计 | 总需求 |
|---|---|---|---|---|---|
| S1 皇冠·保留·不减房 | 9,780 | 11,060 | 10,253.6 | 21,313.6 | 31,093.6 |
| S4 洲至奢选·保留·不减房 | 12,225 | 11,060 | 17,130.7 | 28,190.7 | 40,415.7 |
| S5 洲至奢选·重做·不减房 | 13,855 | 11,060 | 28,490.7 | 39,550.7 | 53,405.7 |
| S7 外部奢牌·重做·3改2 | 16,300 | 11,600 | 45,250.9 | 56,850.9 | 73,150.9 |
段二在 8 方案间为 11,060（不减房）／11,600（3改2）：品牌无关基础 9,000（43 项）＋ 第二批次实测修正 8 项 2,060（竖井、给排水隐蔽、储油发电合规、给排水水处理、电梯 6 台、发电机组 2 台、消防现代化修正、新风 25 台）。

### ⭐ 可保留项节约（S1 4,538.7 万，占装修 44.3%）
全网可复现方法：① 石材纳米涂层「焕新保新」使翻新成本降约 40%、**客房卫生间由传统 1.8—2 万元/间降至约 0.5 万元/间**（迈点网 2025-09）② 石材修复后光亮度提升 80%、木质家具划痕修复肉眼无痕（廊坊沙龙 2026-05）③ **保留原木地板与地砖、天花板修补、家具贴膜**（柏曼南宁朝阳广场店，130 项「留/弃/修」评估体系，2025-08）④ 保留大堂主框架、保留主卫具与瓷砖只换镜柜龙头（方致酒店设计）⑤ 石材 420 元/㎡ 对真石漆 40 元/㎡、材料造价降 90%（维也纳国际经典版）。
分项含客房卫生间石材、地面木地板、实木家具、卫具龙头镜柜、客房门、大堂与走廊与宴会石材、后场、外立面挂大理石。3 改 2 因移卫重做，卫生间石材剔除（S2 降至 3,819.2 万）；外部奢牌要求全新视觉，公区与外立面不可保留。

### ⭐ 三口径重跑结果（v10 引擎）
| 方案 | 改造投资 | 全口径 IRR/NPV/静态 | 集团口径 IRR/静态 | 增量口径 IRR/静态 |
|---|---|---|---|---|
| S1 | 21,313.6 | 4.60% / −6,002.9 / 14 年 | 7.56% / 10.15 年 | 15.61% / 8 年 |
| S4 | 28,190.7 | 6.13% / −4,403.4 / 13 年 | 9.27% / 8.96 年 | 14.52% / 8 年 |
| S3 | 29,171.3 | 1.35% / −14,454.7 / 18 年 | 3.76% / 13.89 年 | 10.50% / 10 年 |
| S5 | 39,550.7 | 2.45% / −16,436.0 / 17 年 | 4.90% / 12.57 年 | 9.26% / 11 年 |
| S2 | 21,288.0 | −0.29% / −13,369.2 / 未回收 | 2.77% / 15.20 年 | 11.88% / 9 年 |
| S6 | 44,381.3 | −2.67% / −30,906.2 / 未回收 | −0.53% / 21.15 年 | 4.74% / 14 年 |
| S7 | 56,850.9 | −4.08% / −42,104.1 / 未回收 | −2.13% / 25.26 年 | 2.41% / 17 年 |

### ⭐⭐ 三个结论
1. **按集团口径「回收期 5-8 年」，七方案全部未落入**（最接近 S4 8.96 年、S1 10.15 年）；**按全口径 IRR，S1 4.60% 与 S4 6.13% 高于 3.5% 底线**。瓶颈已从盈利能力转到回收期与投资规模。
2. **集团 1.8 亿元额度不足以支撑任何方案**：最省的 S1 改造投资 21,313.6 万即超 3,313.6 万，计入停业损失后总需求 31,093.6 万，**占六家改造总盘子的 76.2%、第二批全部额度的 111.0%**。S4 占 99.1%／144.3%，S7 占 179.3%／261.3%。
3. **减房不是解法**：3 改 2 停业长 4—6 个月、竖井工程 +540 万、房量少 134 间，全口径 IRR 由 4.60% 降至 −0.29%。应作为 S1 的局部执行方案（对不达标房型单独 3 改 2）。
4. **基准方案定为 S1「沿用皇冠 + 公区保留石材 + 不减房」**；洲至奢选 S4 的增量代价 = 段三 +6,877.1 万 + 段一 +2,445 万 = 9,322.1 万，换 1.53 个百分点全口径 IRR，在额度已超支前提下不成立。
5. 保留路线的三项代价须写明：1996 年石材基层与防水须逐处检测并设补差准备金；外部奢牌公区与外立面石材不可保留；客房 25.35 ㎡ 仍低于洲际 35 ㎡ 下限，须品牌方面积例外。

### 交叉验证（独立算法互证）
- 客房单间：本次 S1 测 14.70 万/间；业主方底稿自算 6,000 万 ÷ 430 间 = 13.95 万/间 —— 两套独立算法吻合。
- 停业刚性支出：本次 284 万/月（人工+利息+能耗维持）；集团 715 定稿附件 6 载 3,674 万/年（人工 1,412＋现有贷款利息 1,724＋改造期融资利息 540）—— 同量级。
- 集团 17%/5.6 年反推：两者同反推约 3,206 万/年 → 确认集团口径为「改造后年经营现金流 ÷ 改造投资」；进一步反解其隐含平均房价约 **1,186 元/间/晚**（430 间口径 1,108 元），高于 2024 成都全市高端 834 元约 42%，差额已定位到房价一项。

### 引擎脚本
_calc/area_base.py（面积与 43 项底稿）｜v9_engine.py（三段式造价 + 保留项节约）｜v9_export.py（造价表 10 表）｜v10_econ.py（三口径现金流）｜v11_chapters.py + v11_apply.py（新第六、九章写回）｜v12_final.py / v13_final.py（收官）
<!-- project: github.com/darknessdogeric/openclaw-memory -->

---
""")
RM = os.path.join(KB, "00_项目总览_README.md")
open(RM, "a", encoding="utf-8").write("""

| **立项报告（集团汇报件 v3.2）** | v3.2 | docx 98 KB | ⭐⭐⭐⭐ **造价三段式重构**：停业损失 ＋ 机电水电强弱电及隐蔽工程（品牌无关）＋ 装修改造；第六、九、十一章重写；含 8 方案完整造价 | ⭐ 基准方案 S1「沿用皇冠+公区保留石材+不减房」改造投资 **21,313.6 万**、全口径 IRR 4.60%、可保留项节约 **4,538.7 万**；⭐ **集团 1.8 亿额度不足以支撑任何方案**（S1 占六家总盘 76.2%、第二批 111.0%） |
| **完整造价构成表 v1.0** | v1.0 | xlsx 10 表 | 方法与口径、面积底稿、段一停业损失、段二机电水电强弱电、段三客房改造、段三公共区域后场、可保留项与节约、八方案造价总表、与集团规划值对照、数据源 | ⭐ 锚点＝业主方 2024 报告 43 项自编造价 18,000 万（与洲际 PIP 勾稽） |
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
L("memory + README synced")

L("\n=== 最终交付 ===")
for f in sorted(glob.glob(os.path.join(REP, "*.docx"))):
    if os.path.basename(f).startswith("~$"): continue
    if not re.search(r"立项报告_集团汇报件|立项方案_数据源清单", f): continue
    L("  [报告] %-68s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
for f in sorted(glob.glob(os.path.join(TGT, "测算与中间产物", "*.xlsx"))):
    L("  [测算] %-68s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
L("DONE")
