# -*- coding: utf-8 -*-
"""2026-10 月度更新 第二阶段：主酒店KB + 知识库索引刷新"""
import io, os, json

BASE = r"D:\B166ER-openclaw\workspace"
TODAY = "2026-10-25"
out = []

def read(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()

def write(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)

# 复用第一阶段脚本中的酒店段落（避免重复粘贴 6KB 正文）
import importlib.util
spec = importlib.util.spec_from_file_location(
    "kb1", os.path.join(BASE, r"toolbox\kb_tools\kb_monthly_update_2026_10.py"))
# 直接读源文件取常量，避免执行
src = read(os.path.join(BASE, r"toolbox\kb_tools\kb_monthly_update_2026_10.py"))
ns = {}
start = src.index('HOTEL_SECTION = r"""')
end = src.index('"""', start + len('HOTEL_SECTION = r"""'))
HOTEL_SECTION = src[start + len('HOTEL_SECTION = r"""'):end]

MAIN_HOTEL = r"memory\hotel-industry-knowledge-base.md"

try:
    p = os.path.join(BASE, MAIN_HOTEL)
    t = read(p)
    b = len(t)
    old = "> **深化**: 2026-05-14 — V9.0 修复章节编号错误 + 新增三章：OTA多平台运营策略/STR数据方法论/ESG与可持续发展"
    new = old + "\n> **行业动态更新**: " + TODAY + " — 新增「行业动态（2026-10 更新）」章节：国庆量增价弱/供给增速差/集团财报结构/中高端负增长/AI入口崛起/首单酒店REIT"
    if old in t:
        t = t.replace(old, new, 1)
    else:
        t = t.replace("> **版本**: v9.0  ", "> **版本**: v9.0  \n> **行业动态更新**: " + TODAY, 1)
    t = t.rstrip() + "\n\n---\n\n" + HOTEL_SECTION + "\n"
    write(p, t)
    out.append({"kb": "酒店行业全景 KB v9.0 (主路由库)", "path": MAIN_HOTEL,
                "status": "OK", "bytes_before": b, "bytes_after": len(t)})
    print("OK   main hotel KB  %d -> %d" % (b, len(t)))
except Exception as e:
    out.append({"kb": "酒店行业全景 KB v9.0 (主路由库)", "path": MAIN_HOTEL,
                "status": "FAIL", "error": repr(e)})
    print("FAIL main hotel KB", repr(e))

# ---------------- 索引刷新 ----------------
IDX = r"memory\knowledge-base-index.md"
try:
    p = os.path.join(BASE, IDX)
    t = read(p)
    b = len(t)
    t = t.replace("> 更新: 2026-05-04", "> 更新: " + TODAY + "（月度知识库更新轮）", 1)
    # 路由决策表：修正版本号 + 补登 TMC
    t = t.replace("| 酒店行业全景 | `hotel-industry-knowledge-base.md` (102KB, V8.1) | 酒店/民宿/行业/产业链/市场 |",
                  "| 酒店行业全景 | `hotel-industry-knowledge-base.md` (102KB, V9.0) | 酒店/民宿/行业/产业链/市场 |", 1)
    t = t.replace("| 酒店收益管理 | `hotel-revenue-management-knowledge-base-v4.md` (40KB) | 收益管理/动态定价/RevPAR/STR指数/OTA博弈 |",
                  "| 酒店收益管理 | `hotel-revenue-management-knowledge-base-v5.md` (47KB) | 收益管理/动态定价/RevPAR/STR指数/OTA博弈 |", 1)
    anchor = "| 跨境贸易 | `跨境贸易知识库V1.0.md` (14KB) | 跨境/选品/亚马逊/出海 |"
    if anchor in t and "商旅TMC知识库V1.0.md" not in t:
        t = t.replace(anchor, anchor + "\n| 商旅TMC | `商旅TMC知识库V1.0.md` (15KB) | 商旅/差旅/TMC/企业差旅/协议价/差标 |", 1)
    # 核心知识库表：更新状态日期
    t = t.replace("| 酒店行业全景 | 102KB | V8.1 | ✅ 核心 (2026-05-03) |",
                  "| 酒店行业全景 | 102KB | V9.0 | ✅ 核心 (" + TODAY + " 行业动态) |", 1)
    t = t.replace("| AI/LLM技术 | 121KB | V2 | ✅ 完善 |",
                  "| AI/LLM技术 | 121KB | V2 | ✅ " + TODAY + " 行业动态 |", 1)
    t = t.replace("| 酒店收益管理 | 40KB | V4 | ✅ 最新 |",
                  "| 酒店收益管理 | 47KB | V5 | ✅ 最新 |", 1)
    t = t.replace("| 跨境贸易 | 14KB | V1 | ✅ 完善 |",
                  "| 跨境贸易 | 14KB | V1 | ✅ " + TODAY + " 行业动态 |", 1)
    # 新增商旅TMC行
    cb_row = "| 跨境贸易 | 14KB | V1 | ✅ " + TODAY + " 行业动态 |"
    if cb_row in t and "商旅TMC | 15KB | V1" not in t:
        t = t.replace(cb_row, cb_row + "\n| 商旅TMC | 15KB | V1 | ✅ " + TODAY + " 行业动态 |", 1)
    # 版本历史
    t = t.replace("- V3.0 (2026-04-06): **三层架构确立**，路由决策表，自动迭代机制，进化系统，自动纳入机制",
                  "- V3.0 (2026-04-06): **三层架构确立**，路由决策表，自动迭代机制，进化系统，自动纳入机制\n- V3.2 (" + TODAY + "): 月度更新轮 — 酒店行业全景(主库+v7)/AI-LLM/商旅TMC/跨境贸易 四库追加「行业动态」章节；补登商旅TMC至路由表；修正酒店行业全景 V9.0 与收益管理 V5 版本号", 1)
    write(p, t)
    out.append({"kb": "知识库索引", "path": IDX, "status": "OK",
                "bytes_before": b, "bytes_after": len(t)})
    print("OK   index          %d -> %d" % (b, len(t)))
except Exception as e:
    out.append({"kb": "知识库索引", "path": IDX, "status": "FAIL", "error": repr(e)})
    print("FAIL index", repr(e))

print("\nJSON " + json.dumps(out, ensure_ascii=False))
