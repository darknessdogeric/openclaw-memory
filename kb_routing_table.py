# -*- coding: utf-8 -*-
"""
kb_routing_table.py - 路由表构建与差异检查 (V2.0, 2026-10-25)

职责:
1. 扫描索引库 (.kb_rag.db) 中已纳入的 KB 类文件
2. 与 skills/knowledge-base/SKILL.md 的路由决策表比对
3. 输出 routing_update_needed.json —— 标记需新增/更新/失效的路由条目

用法: python kb_routing_table.py [--apply]
"""
import os, re, sys, json, sqlite3
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(r"D:\B166ER-openclaw\workspace")
DB = WORKSPACE / ".kb_rag.db"
SKILL_MD = WORKSPACE / "skills" / "knowledge-base" / "SKILL.md"
OUT = WORKSPACE / "memory" / "routing_update_needed.json"

# 语义类型 → 路由关键词（中文触发词）
SEMANTIC_RULES = [
    ("审美/设计/品牌",      ["审美", "设计", "品位", "气韵", "意境", "海报", "排版", "配色", "字体"]),
    ("博弈/分析/决策",      ["博弈", "谈判", "策略", "纳什", "决策", "博弈论"]),
    ("酒店行业/运营",       ["酒店", "住宿", "民宿", "客房", "出租率", "ADR", "RevPAR", "OTA"]),
    ("酒店收益管理",        ["收益管理", "动态定价", "GOP", "房价", "预测"]),
    ("酒店私域/会员",       ["私域", "会员", "RFM", "复购", "积分", "社群"]),
    ("酒店新媒体/营销",     ["新媒体", "抖音", "小红书", "短视频", "直播", "内容营销"]),
    ("酒店智能化/AI",       ["智能化", "AI获客", "PMS", "数字化", "智慧酒店"]),
    ("酒店财务/投资/资产",  ["资产", "投资", "融资", "估值", "IRR", "NPV", "尽调", "改造"]),
    ("酒店SOP/运营标准",    ["SOP", "标准操作", "运营", "流程", "部门"]),
    ("酒店资产/投融管退",  ["投融管退", "资产管理", "退出"]),
    ("AI/LLM/Agent",       ["AI", "LLM", "AGENT", "Prompt", "RAG", "大模型", "TOKEN"]),
    ("创业融资",            ["融资", "股权", "YC", "路演", "BP", "VC", "投资", "IPO"]),
    ("金融证券/量化",       ["金融", "证券", "股票", "REITs", "量化", "回测", "因子", "美股", "A股"]),
    ("大乐透/彩票预测",     ["大乐透", "彩票", "预测", "机选", "奖池"]),
    ("跨境/贸易/出海",      ["跨境", "选品", "Amazon", "出海", "WFOE", "VIE", "关税"]),
    ("目标管理/复盘",       ["OKR", "目标", "复盘", "PDCA"]),
    ("研究报告/数据",        ["研报", "研究报告", "数据采集", "行业分析"]),
    ("AHL项目/去中心化",     ["AHL", "去中心化", "协议", "钱包"]),
    ("理论架构/认知",        ["理论", "元认知", "认识论", "方法论", "第一性原理"]),
]

KB_NAME_HINT = re.compile(r"knowledge-base|知识库|_kb|KB_|_v\d|框架|方法论|手册|标准|规范|报告", re.I)


def indexed_md():
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    rows = [r[0] for r in c.execute("select path from files where path like '%.md'")]
    c.close()
    return rows


def skill_routing_rows():
    """从 SKILL.md 抽取现有路由表的目标文件（反引号内的 .md 或 kb 名）"""
    if not SKILL_MD.exists():
        return set()
    text = SKILL_MD.read_text(encoding="utf-8", errors="ignore")
    found = set()
    for m in re.finditer(r"`([^`]+?\.(?:md|json))`", text):
        found.add(m.group(1))
    for m in re.finditer(r"`([a-z0-9\-]*(?:knowledge-base|kb)[a-z0-9\-\.]*)`", text, re.I):
        found.add(m.group(1))
    return found


def main():
    md_paths = indexed_md()
    # 判定 KB 候选：文件名含 KB 语义特征，且体积/内容像知识库
    kb_candidates = []
    for p in md_paths:
        name = p.replace("/", "\\").split("\\")[-1]
        if KB_NAME_HINT.search(name):
            kb_candidates.append(p)
    kb_candidates.sort()

    existing = skill_routing_rows()
    existing_basenames = {e.split("\\")[-1] for e in existing}

    new_routes, covered = [], []
    for p in kb_candidates:
        base = p.replace("/", "\\").split("\\")[-1]
        if base in existing_basenames:
            covered.append(p)
        else:
            new_routes.append(p)

    # 给新路由推断语义类型
    inferred = []
    for p in new_routes:
        tags = []
        low = p.lower()
        for sem, kws in SEMANTIC_RULES:
            for kw in kws:
                if kw.lower() in low:
                    tags.append(sem)
                    break
        inferred.append({"path": p, "name": p.replace("/", "\\").split("\\")[-1], "semantic": tags or ["未分类"]})

    payload = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "indexed_md_total": len(md_paths),
        "kb_candidates": len(kb_candidates),
        "already_routed": len(covered),
        "new_routes_needed": len(inferred),
        "routing_table": inferred,
        "status": "OK" if not inferred else "NEEDS_UPDATE",
        "note": "新增路由候选：需在 skills/knowledge-base/SKILL.md 路由决策表中登记后生效",
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"[路由] 已索引 md: {len(md_paths)}  KB候选: {len(kb_candidates)}  已覆盖: {len(covered)}  新增待登记: {len(inferred)}")
    print(f"[路由] 输出: {OUT}")
    for r in inferred[:20]:
        print(f"   + {r['name']}  -> {', '.join(r['semantic'])}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
