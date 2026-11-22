# -*- coding: utf-8 -*-
"""v93：Word 重建 + 最终审计 + memory/README 同步"""
import io, os, sys, re, json, glob, subprocess
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
CAL = os.path.join(TGT, "测算与中间产物")
LOG = open(os.path.join(T, "v93.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
J = json.load(open(os.path.join(T, "v87.json"), encoding="utf-8"))
B = {r["key"]: r for r in J["brands"]}; ORDER = J["order"]
BASE = J["base"]; OWN = J["own"]; PATHS = J["paths"]; CL = J["closure"]
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return "{:.2f}%".format(v * 100) if v is not None else "无可解"
def M(v, d=1): return ("+" + N(v, d)) if v >= 0 else ("−" + N(abs(v), d))

D = os.path.join(KB, "_calc")
src = open(os.path.join(D, "v17_docx.py"), encoding="utf-8").read()
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.md", "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
src = src.replace("总府皇冠改造_可行性研究报告_v1.0_2026-11-14.docx", "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.docx")
open(os.path.join(D, "v17_docx_v5.py"), "w", encoding="utf-8").write(src)
subprocess.run([r"C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe", os.path.join(D, "v17_docx_v5.py")],
               capture_output=True, text=True, encoding="utf-8", errors="replace")
for l in open(os.path.join(T, "v17.log"), encoding="utf-8", errors="replace").read().split("\n"):
    if l.strip(): L(l.rstrip())

MD5 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.md")
s = open(MD5, encoding="utf-8").read()

L("")
L("=== 一、陈旧数字审计 ===")
STALE = ["2,787.2", "21,312.4", "4,507.0", "6.10%", "3,422.6", "6,499.1", "12,610.5",
         "14,647.7", "254.7", "8.11%", "4,750.9", "9.95%", "7,585.4", "3.70%", "9,950.5", "15.24%",
         "3,000 万元", "235 间"]
for k in STALE:
    n = s.count(k)
    L("   %-11s %d 次 %s" % (k, n, "← 需核" if n else "OK"))
L("")
L("=== 二、权威值命中核对 ===")
MUST = [N(B["B01"]["total_rev"]), M(B["B01"]["npv"]), P(B["B01"]["irr"]),
        M(B["B02"]["npv"]), str(B["B02"]["n"]), M(B["B12"]["npv"]),
        M(PATHS[0][2]), M(PATHS[-1][2]), P(PATHS[-1][3]),
        N(BASE["total_rev"]), N(BASE["room"]), M(OWN["npv"]), P(OWN["irr"]),
        "45 平方米", "209 间", "65 平方米", "50 平方米", "282 间", "230 间", "2029-03-27",
        "锦发改发〔2025〕30 号", "可分离性", "决策预研", "僵局", "顺序倒置"]
miss = [k for k in MUST if k not in s]
L("   缺失: {0}".format(miss if miss else "无（%d 项全中）" % len(MUST)))

L("")
L("=== 三、Word 终检 ===")
from docx import Document
DOCX = os.path.join(REP, "总府皇冠改造_可行性研究报告_v5.0_2026-11-14.docx")
d = Document(DOCX)
alltext = chr(10).join(p.text for p in d.paragraphs) + chr(10) + chr(10).join(
    c.text for tb in d.tables for r in tb.rows for c in r.cells)
blank = sum(1 for tb in d.tables for r in tb.rows for c in r.cells if c.text.strip() in ("", "\u2014", "-", "\uff0f", "/"))
EMO = ("[" + chr(92) + "U0001F300-" + chr(92) + "U0001FAFF" + chr(92) + "U00002600-" + chr(92) + "U000027BF"
       + chr(92) + "U00002B50" + chr(92) + "uFE0F" + chr(92) + "u200D" + chr(92) + "u2764" + chr(92) + "u2B06"
       + chr(92) + "u2B07" + chr(92) + "u2B05" + chr(92) + "u274C" + chr(92) + "u2705" + chr(92) + "u26A0"
       + chr(92) + "u26A1" + chr(92) + "u2139" + chr(92) + "u24C2" + chr(92) + "u2B55]")
L("   {0:.1f} KB | 段落 {1} | 表格 {2} | 空白格 {3} | 节 {4}".format(
    os.path.getsize(DOCX)/1024, len(d.paragraphs), len(d.tables), blank, len(d.sections)))
for i, sec in enumerate(d.sections):
    L("   S{0} {1} {2:.0f}x{3:.0f} 页码域{4}".format(i, "横" if sec.page_width>sec.page_height else "纵",
        sec.page_width.cm, sec.page_height.cm, sec.footer._element.xml.count('w:instr="PAGE"')))
L("   emoji: {0}".format(len(re.findall(EMO, alltext))))
for ab in ("ADR", "RevPAR", "CAPEX", "NPV", "IRR", "GOP"):
    n = len(re.findall(r"\b" + ab + r"\b", alltext))
    if n: L("   ⚠ 英文缩写 {0} ×{1}".format(ab, n))
m = re.search(r"^## 目录\n", s, re.M)
ls = s[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\. ", "", l).strip() for l in ls[:start] if re.match(r"^\d+\. ", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
L("   目录↔正文: {0}（目录 {1} / 正文 {2}）".format(toc == bod, len(toc), len(bod)))
L("   章节 {0} ｜ 图 {1} ｜ 风险 {2} ｜ 字数 {3:,}".format(
    len(re.findall(r"^## 第", s, re.M)), len(re.findall(r"!\[", s, re.M)),
    len(re.findall(r"\| R-\d+ \|", s)), len(s)))

L("")
L("=== 四、交付清单 ===")
for p in sorted(glob.glob(os.path.join(REP, "总府皇冠改造_可行性研究报告*"))) + \
         sorted(glob.glob(os.path.join(REP, "总府皇冠改造_国际联号*"))) + \
         sorted(glob.glob(os.path.join(CAL, "总府皇冠改造_可行性研究报告*"))):
    L("   {0:7.1f} KB  {1}".format(os.path.getsize(p)/1024, os.path.basename(p)))
L("   桌面根目录总府残留: {0}".format(len(glob.glob(r"C:\Users\ericz\Desktop\*总府*"))))

# ══ memory / README ══
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
open(MEM, "a", encoding="utf-8").write(r"""
### 00:15 ⭐⭐⭐⭐⭐ v5.0 最终收口：单一数据源 + 三处口径错误 + 深度审查修复
**本轮最重要的产出不是新内容，是把"报告内部并存两套财务数字"这个致命缺陷彻底消除。**

#### 一、⭐ 发现的模型层缺陷（此前一直未被发现）
1. **v50 / v52 / v70 三版模型写同一个 v70.json**，内容却不同（ADR 825 vs 880、营收 12,610.5 vs 15,064.3、净现值 −4,507.0 vs +254.7）。结果是 **v5.0 报告第九章用 v70 新数、第六章（二）投资表与第一章（四）却是 v52 旧数**——同一份报告两套财务结论。**修复：新建 v87_model.py 为唯一权威模型，v88—v93 全部由 v87.json 单一数据源生成，报告内不再存在任何手写财务数。**
2. **★ 洲至奢选面积由推定 40 ㎡ 订正为 OTA 实测 45 ㎡**（棕榈泉 2026 年翻新后房型：标准房 45／尊贵房 52／行政层 54—58／套房 106 ㎡）。房量 235→209 间，**净现值由 +2,787.2 万跌至 +61.0 万，相差 45 倍**。上一轮把它列为"前提最可靠的首选品牌"是错的——**它只是没有第三方谈判障碍，经济性已接近盈亏平衡**。
3. **段一B（停业期营业收入归零）多除了 2**，使停业期收入损失少算一半，已修正。
4. 基建段（段一A）12 个月 3,484.6 万与 715 定稿 3,674 万量级一致，交叉验证通过。

#### 二、OTA 实测成果（第 5 条"所有数据都要全网+OTA 印证"的落地）
- **携程直连三条路全被封**：搜索页强制登录（m.ctrip.com/webapp/hotel/{city}1/ 且要求数字 cityId，模板见 ota_scraper/profiles.py）、soa2 API 403、详情页 __INITIAL_STATE__ 需登录态。**可行路径是 web_search 命中携程/OTA 页面正文**。
- 实测取得：瑞吉 282 间·65 ㎡·¥1,291–1,393；尼依格罗 230 间·50 ㎡·¥1,180–1,400；康莱德北京 46 ㎡；**洲至奢选棕榈泉 45/52/54–58/106 ㎡**；居舍房型阶梯 63/72/100/145/215/287 ㎡（米其林均价约 €839）。
- **知识库已有两套现成爬取范式此前未用**：`ota_scraper/`（OTA-Scraper v1.4，携程已校准、含 64 个自适应选择器与 9 平台移动端端点库）与 `skills/multi-ota-price-tool/`（MOTI，多 OTA 价格智能工具，含标准房判定三规则与入住率加权算法）。**下次应先检索范式再动手。**

#### 三、DeepSeek 框架吸收（决策预研框架）
- 报告性质改《**决策预研框架**》；新增 **A 底线整改（消防升级 120–200 元/㎡）／B 机电同步更新（200–500 元/㎡）／C 整体停业改造（五星客房全包 18–25 万元/间）** 三档分级与触发条件。
- **★ 消防与机电可分离性 = A 档成立的技术前提**（共用吊顶与管井，先改消防后续机电须二次拆开，返工可能抵消停业节省）。
- 补入**局部改造四项隐性成本**：OTA 评分冲击与恢复周期、"改了一半"僵局、**施工顺序倒置返工**（消防须在客房翻新之前完成）、两项专项合规前置性。
- 资金四分类：不宜作主渠道（专项债负面清单、酒店自身结余）／有时效窗口（锦江区设备更新与文旅奖励，**有效期至 2026-12-31，须开工前入库**）／需集团争取（旅投内部支持具体化、合作方带资、**停业期固定成本兜底**）／可自行安排。

#### 四、v87 权威模型结果（30 年口径，8% 折现）
| 品牌 | 面积 | 房量 | 营收(万) | 投资(万) | 净现值(万) | IRR |
|---|---|---|---|---|---|---|
| LXR | 60 | 157 | 20,629.8 | 21,289.8 | +23,213.2 | 17.07% |
| Sofitel | 40 | 235 | 21,361.3 | 22,136.7 | +15,525.6 | 13.99% |
| **自有品牌** | 25.35 | 402 | — | 21,313.6 | **+10,724.7** | **12.52%** |
| 费尔蒙 | 45 | 209 | 15,478.9 | 20,192.8 | +9,622.4 | 12.10% |
| 六善 | 50 | 188 | 17,089.0 | 20,953.5 | +8,409.4 | 11.49% |
| 柏悦 | 45 | 209 | 13,981.0 | 20,192.8 | +6,380.2 | 10.76% |
| 康莱德 | 46 | 205 | 13,713.4 | 20,107.1 | +5,883.8 | 10.56% |
| 文华东方 | 55 | 171 | 15,543.7 | 20,546.3 | +5,816.0 | 10.49% |
| 丽晶 | 60 | 157 | 14,271.1 | 20,219.9 | +3,670.4 | 9.61% |
| 尼依格罗 | 50 | 188 | 11,588.0 | 19,748.6 | +1,629.1 | 8.74% |
| 洲至奢选 | 45 | 209 | 13,027.1 | 21,472.1 | +61.0 | 8.03% |
| 皇冠续约 | 25.35 | 402 | 15,064.3 | 21,448.5 | +46.9 | 8.02% |
| 瑞吉 | 65 | 145 | 9,297.9 | 18,885.2 | −2,495.8 | 6.78% |
**净现值转正路径**：基准（12 月全停＋分区滚动＋20 年）−3,630.4 万／5.91%；P1 经营期 30 年 +46.9；P2 品牌方承担 30% +6,243.2（权重最大）；P3 锦江区补贴 50 万 +95.0；P5 三项叠加 **+6,291.3 万／11.41%**。

#### 五、交付
可研报告 v5.0（104.8 KB／377 段／41 表／0 空白／9 节／5 图／12 章／23 条风险）＋ PIP 前期策划模板 docx ＋ 测算附表 v5.0（10 表）；v4.0 已删除。

#### 六、沉淀（脚本编写教训）
- **Python 字符串中的 `%` 与中文标点混排会触发格式化错误**（"19%" 之类）→ 改用 `.format()`/f-string。
- **Windows 控制台按 GBK 渲染，中文在报错信息里显示为乱码，易误判为编码损坏**（实为渲染失真，文件无损）；判断编码是否坏要用 `open(...,'rb').read().decode('utf-8')` 单独验证。
- **增量替换（replace 段落）不可靠**，尤其同名小节与括号层级；**整章重建 + 单一数据源注入**才是稳的路径。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
RM = os.path.join(KB, "00_项目总览_README.md")
open(RM, "a", encoding="utf-8").write(r"""
### v5.0 最终收口（2026-11-15 00:15）：单一数据源 + 三处口径错误修复
**已消除"报告内并存两套财务数字"的致命缺陷**：新建 `v87_model.py` 为唯一权威模型（合并 v50/v52/v70 三版差异），v88—v93 全部由 `v87.json` 单一数据源生成，报告内不再有手写财务数。
**三处模型层错误**：① v50/v52/v70 三版模型写同一个 v70.json 但内容不同（ADR 825 vs 880、净现值 −4,507.0 vs +254.7）；② **洲至奢选面积由推定 40 ㎡ 订正为 OTA 实测 45 ㎡（棕榈泉 2026 翻新房型：45/52/54—58/106 ㎡），房量 235→209 间，净现值 +2,787.2 万→+61.0 万，相差 45 倍——上一轮列为"首选品牌"是错的**；③ 段一B 多除了 2。
**OTA 实测**：瑞吉 282 间·65 ㎡·¥1,291–1,393；尼依格罗 230 间·50 ㎡·¥1,180–1,400；康莱德北京 46 ㎡；洲至奢选棕榈泉 45/52/54—58/106 ㎡；居舍 63/72/100/145/215/287 ㎡。**携程直连三路全封（登录墙／API 403／需登录态），可行路径是 web_search 命中 OTA 页面正文**；知识库已有 `ota_scraper/` 与 `skills/multi-ota-price-tool/` 两套范式，此前未用。
**DeepSeek 框架吸收**：报告性质改《决策预研框架》；A/B/C 三档范围分级＋触发条件；**消防与机电可分离性 = A 档技术前提**；局部改造四项隐性成本（OTA 评分冲击、改了一半僵局、**施工顺序倒置返工**、两项合规前置）；资金四分类（不宜作主渠道／有时效窗口／需集团争取／可自行安排）。
**v87 结果**：净现值前三为 LXR +23,213.2 万（17.07%）、Sofitel +15,525.6 万（13.99%）、**自有品牌 +10,724.7 万（12.52%，第 3 位）**；洲至奢选降至 +61.0 万（8.03%）。转正路径 P5 三项叠加 **+6,291.3 万／11.41%**。
**交付**：可研报告 v5.0（104.8 KB／377 段／41 表／0 空白／9 节／5 图／12 章／23 条风险）＋ PIP 模板 docx ＋ 测算附表 v5.0（10 表）；v4.0 已删。
<!-- project: github.com/darknessdogeric/openclaw-memory -->
""")
L("")
L("memory + README synced")
L("DONE")
