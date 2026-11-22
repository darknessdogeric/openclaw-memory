#!/usr/bin/env python3
"""
entity_extractor.py — B166ER 每日实体抽取器
R60-11 沉淀动作核心工具

功能:
  1. 扫描 memory/*.md 当日实体
  2. 提取实体 + 关系 → graph.jsonl (JSONL, append模式)
  3. 更新 relations-trend.md (累计频次)
  4. 更新 eric-4-projects-dashboard.md (如有新实体/关系)

用法:
  python entity_extractor.py today    # 仅处理今天
  python entity_extractor.py full    # 全量重扫 (慎用)
  python entity_extractor.py --days N # 最近N天
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")
MEMORY_DIR = WORKSPACE / "memory"
ONTOLOGY_DIR = MEMORY_DIR / "ontology"
GRAPH_JSONL = ONTOLOGY_DIR / "graph.jsonl"
RELATIONS_TREND_MD = ONTOLOGY_DIR / "relations-trend.md"
DASHBOARD_MD = MEMORY_DIR / "eric-4-projects-dashboard.md"
PUSH_QUEUE_PY = WORKSPACE / "toolbox" / "push_queue.py"

# ========================
# 实体模式定义
# ========================

ENTITY_PATTERNS = {
    "Person": [
        (r"Eric", "Eric", 0.95),
        (r"张实", "张实", 0.95),
        (r"B166ER", "B166ER", 0.95),
    ],
    "Company": [
        (r"安逸酒店集团", "安逸酒店集团", 0.95),
        (r"安逸集团", "安逸酒店集团", 0.9),
        (r"四川省旅游投资集团", "四川旅游投", 0.9),
        (r"四川旅游投", "四川旅游投", 0.9),
        (r"省旅投", "四川旅游投", 0.85),
        (r"AHL", "AHL", 0.95),
        (r"智元机器人", "智元机器人", 0.85),
        (r"亚朵", "亚朵", 0.8),
        (r"携程", "携程", 0.8),
        (r"美团", "美团", 0.8),
        (r"首旅如家", "首旅如家", 0.8),
        (r"高盛", "高盛", 0.8),
        (r"OpenAI", "OpenAI", 0.8),
        (r"Anthropic", "Anthropic", 0.8),
        (r"特斯拉", "特斯拉", 0.8),
    ],
    "Project": [
        (r"AHL\s*(?:集团内孵化|协议栈|v\d|范式)?", "AHL", 0.9),
        (r"1244\s*战略", "1244战略", 0.9),
        (r"1244战略", "1244战略", 0.95),
        (r"医养酒店", "医养酒店", 0.9),
        (r"安逸\s*1244", "1244战略", 0.9),
        (r"深度自迭代", "深度自迭代", 0.85),
        (r"B166ER\s*深度", "B166ER深度自迭代", 0.85),
        (r"R66", "R66监控", 0.85),
        (r"R60", "R60规则", 0.85),
        (r"端午.*复盘", "端午复盘", 0.9),
    ],
    "Event": [
        (r"党委会", "党委会", 0.95),
        (r"D-?day", "D-day", 0.9),
        (r"D-day", "D-day", 0.95),
        (r"公示期", "公示期", 0.9),
        (r"入职", "入职", 0.9),
        (r"2026年端午节", "端午节", 0.95),
        (r"STR\s*6月", "STR6月数据", 0.9),
        (r"STR.*数据", "STR数据发布", 0.85),
        (r"霍尔木兹", "霍尔木兹海峡事件", 0.9),
    ],
    "Place": [
        (r"襄阳", "襄阳", 0.9),
        (r"成都", "成都", 0.85),
        (r"重庆", "重庆", 0.85),
        (r"四川", "四川", 0.8),
        (r"大理", "大理", 0.8),
        (r"北京", "北京", 0.8),
    ],
    "Tool": [
        (r"OpenClaw", "OpenClaw", 0.95),
        (r"DeepSeek", "DeepSeek", 0.9),
        (r"TrendRadar", "TrendRadar", 0.9),
        (r"Agent\s*TARS", "Agent TARS", 0.85),
        (r"Playwright", "Playwright", 0.8),
        (r"Obscura", "Obscura", 0.8),
        (r"scrape_matrix", "scrape_matrix", 0.85),
        (r"Booking.*extractor", "Booking价格提取器", 0.85),
    ],
}

# 关系模式
RELATION_PATTERNS = [
    # works_at / manages / uses / related_to
    (r"Eric.*在.*安逸", "pers_Eric", "works_at", "comp_安逸酒店集团", 0.95),
    (r"Eric.*入职", "pers_Eric", "即将入职", "comp_安逸酒店集团", 0.9),
    (r"Eric.*担任.*产业发展部", "pers_Eric", "即将担任", "role_产业发展部部长", 0.9),
    # [R66修订·2026-09-03] 删除 "167家酒店"(早期口径,已被715定稿56家/103家目标覆盖)
    # [R66修订·2026-09-03] 删除 "350亿授信"(USER.md 8/30 已清理的虚构内容,Eric 明确指令)
    (r"AHL.*安逸", "proj_AHL", "落地于", "comp_安逸酒店集团", 0.9),
    (r"1244.*AHL", "proj_1244战略", "协同", "proj_AHL", 0.85),
    (r"Eric.*使用.*OpenClaw", "pers_Eric", "使用", "tool_OpenClaw", 0.95),
    (r"Eric.*使用.*DeepSeek", "pers_Eric", "使用", "tool_DeepSeek", 0.9),
    (r"B166ER.*cron", "tool_B166ER", "运行", "event_cron任务", 0.9),
    (r"D-?day.*党委会", "event_D-day", "触发事件", "event_党委会", 0.9),
    (r"7月.*入职", "event_入职", "时间", "time_7月中上旬", 0.85),
    (r"党委会.*7/?13|7/?14", "event_党委会", "预定日期", "date_7月13或14", 0.85),
    (r"Eric.*医养酒店", "pers_Eric", "管理", "proj_医养酒店", 0.85),
    (r"医养酒店.*轻资产", "proj_医养酒店", "模式", "mode_轻资产", 0.85),
    (r"AHL.*去中心化", "proj_AHL", "特性", "feature_去中心化", 0.9),
    (r"AHL.*双Agent", "proj_AHL", "架构", "arch_双Agent", 0.9),
    (r"端午节.*断点", "event_端午节", "状态", "status_断点", 0.8),
]


def get_entity_id(entity_type: str, name: str) -> str:
    """生成实体稳定ID"""
    type_prefix = {
        "Person": "pers", "Company": "comp", "Project": "proj",
        "Event": "even", "Place": "plac", "Tool": "tool"
    }.get(entity_type, "unk")
    # 简单hash生成短ID
    hash_val = sum(ord(c) for c in name) % 1000
    return f"{type_prefix}_{hash_val:04d}"


def extract_entities_from_text(text: str) -> list[dict]:
    """从文本中提取实体"""
    found = {}
    for entity_type, patterns in ENTITY_PATTERNS.items():
        for pattern, name, confidence in patterns:
            if re.search(pattern, text):
                eid = get_entity_id(entity_type, name)
                if eid not in found or found[eid]["confidence"] < confidence:
                    found[eid] = {
                        "id": eid,
                        "type": entity_type,
                        "name": name,
                        "confidence": confidence,
                        "aliases": []
                    }
    return list(found.values())


def extract_relations_from_text(text: str, entities: list[dict]) -> list[dict]:
    """从文本中提取关系"""
    relations = []
    entity_names = {e["name"] for e in entities}
    entity_map = {e["name"]: e["id"] for e in entities}

    for pattern, src, rel, tgt, conf in RELATION_PATTERNS:
        if re.search(pattern, text):
            # 简化：subject=Eric, object=最相关的entity
            src_id = entity_map.get("Eric", "pers_0001") if "pers_Eric" in src else src
            # 找到tgt对应的实体
            tgt_id = tgt  # 可能需要映射
            relations.append({
                "from": src_id,
                "relation": rel,
                "to": tgt_id,
                "confidence": conf
            })
    return relations


def get_memory_files(days: int = 1) -> list[Path]:
    """获取最近N天的memory文件"""
    files = []
    today = datetime.now().date()
    for i in range(days):
        date = today - timedelta(days=i)
        fpath = MEMORY_DIR / f"{date.strftime('%Y-%m-%d')}.md"
        if fpath.exists():
            files.append(fpath)
    return sorted(files)


def load_existing_graph() -> dict:
    """加载已存在的graph.jsonl，返回 {entity_id: entity} 和 {relation_key: count}"""
    entities = {}
    relation_counts = {}
    if GRAPH_JSONL.exists():
        with open(GRAPH_JSONL, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    if obj.get("type") == "entity":
                        entities[obj["id"]] = obj
                    elif obj.get("type") == "relation":
                        key = f"{obj['from']}|{obj['relation']}|{obj['to']}"
                        relation_counts[key] = relation_counts.get(key, 0) + 1
                except json.JSONDecodeError:
                    continue
    return entities, relation_counts


def save_graph_entry(entry: dict):
    """追加单条到graph.jsonl"""
    ONTOLOGY_DIR.mkdir(parents=True, exist_ok=True)
    with open(GRAPH_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def update_relations_trend(new_relations: list[dict], existing_counts: dict):
    """更新 relations-trend.md"""
    # 累计频次
    for rel in new_relations:
        key = f"{rel['from']}|{rel['relation']}|{rel['to']}"
        existing_counts[key] = existing_counts.get(key, 0) + 1

    # 生成top关系
    sorted_rels = sorted(existing_counts.items(), key=lambda x: -x[1])[:20]
    total = sum(existing_counts.values())

    lines = [
        "# 关系趋势 (Relations Trend)",
        f"> 自动生成 from entity_extractor.py · {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"**累计关系总数**: {total}",
        "",
        "## Top 20 高频关系",
        "",
        "| 排名 | 主体 | 关系 | 客体 | 累计频次 |",
        "|------|------|------|------|----------|",
    ]

    for i, (key, count) in enumerate(sorted_rels, 1):
        parts = key.split("|")
        if len(parts) == 3:
            src, rel, tgt = parts
            lines.append(f"| {i} | {src} | {rel} | {tgt} | {count} |")

    lines.append("")
    lines.append("---")
    lines.append("*每行代表该关系在graph.jsonl中的累计出现次数*")

    ONTOLOGY_DIR.mkdir(parents=True, exist_ok=True)
    with open(RELATIONS_TREND_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def update_dashboard(new_entities: list, new_relations: list):
    """更新 Eric 4项目仪表板"""
    # Eric 4个核心项目
    projects = {
        "AHL": {"status": "待入职后启动", "confidence": 0.9},
        "1244战略": {"status": "待入职后融合", "confidence": 0.85},
        "医养酒店": {"status": "个人研究", "confidence": 0.8},
        "深度自迭代": {"status": "持续运行", "confidence": 0.95},
    }

    # 检测有无新进展
    new_proj_mentions = []
    for e in new_entities:
        if e["name"] in projects:
            projects[e["name"]]["status"] = "今日提及"
            new_proj_mentions.append(e["name"])

    lines = [
        "# Eric 4 项目仪表板",
        f"> 自动生成 from entity_extractor.py · {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 项目状态",
        "",
        "| 项目 | 状态 | 置信度 | 最近更新 |",
        "|------|------|--------|----------|",
    ]

    today = datetime.now().strftime("%Y-%m-%d")
    for name, info in projects.items():
        lines.append(f"| {name} | {info['status']} | {info['confidence']} | {today} |")

    lines.append("")
    lines.append("## 今日抽取实体")
    lines.append("")
    lines.append(f"**新实体数**: {len(new_entities)}")
    lines.append(f"**新关系数**: {len(new_relations)}")

    if new_proj_mentions:
        lines.append("")
        lines.append(f"**今日提及项目**: {', '.join(new_proj_mentions)}")

    lines.append("")
    lines.append("## 4项目资金状态")
    lines.append("")
    lines.append("| 项目 | 资金状态 | 来源 |")
    lines.append("|------|---------|------|")
    # [R66修订·2026-09-03] 删除 "350亿授信" 虚构值;按USER.md vR66版,仅保留"国企薪酬"
    lines.append("| 安逸集团入职 | 已解决（国企薪酬） | USER.md |")
    lines.append("| AHL孵化 | 集团资源支持 | 入职后 |")
    lines.append("| 医养酒店 | 个人研究 | 自筹 |")
    lines.append("| 深度自迭代 | B166ER自我运行 | 免费 |")

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    with open(DASHBOARD_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return len(new_proj_mentions)


def call_push_queue(message: str, detail: str, tag: str):
    """调用 push_queue.py（如果存在）"""
    if PUSH_QUEUE_PY.exists():
        import subprocess
        cmd = [
            sys.executable, str(PUSH_QUEUE_PY),
            "--push", message, detail, tag
        ]
        try:
            subprocess.run(cmd, capture_output=True, timeout=10)
        except Exception:
            pass  # 非关键，失败不影响主流程
    else:
        print(f"[push_queue] 工具不存在，跳过: {detail}")


def run_extraction(days: int = 1, full: bool = False):
    """执行抽取主流程"""
    print(f"[entity_extractor] 启动 · days={days} · full={full}")

    files = get_memory_files(days if not full else 999)
    if not files:
        print("[entity_extractor] 未找到memory文件")
        return

    print(f"[entity_extractor] 扫描文件: {[f.name for f in files]}")

    existing_entities, existing_relation_counts = load_existing_graph()
    print(f"[entity_extractor] 已加载 {len(existing_entities)} 实体, {len(existing_relation_counts)} 关系")

    all_new_entities = []
    all_new_relations = []

    for fpath in files:
        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()

        entities = extract_entities_from_text(text)
        relations = extract_relations_from_text(text, entities)

        # 去重，只新增
        for e in entities:
            if e["id"] not in existing_entities:
                entry = {
                    "type": "entity",
                    "date": fpath.stem,
                    **e
                }
                save_graph_entry(entry)
                existing_entities[e["id"]] = e
                all_new_entities.append(e)  # 追加dict，供 update_dashboard 使用
                print(f"  [NEW ENTITY] {e['type']}:{e['name']}")

        for r in relations:
            key = f"{r['from']}|{r['relation']}|{r['to']}"
            if key not in existing_relation_counts:
                entry = {
                    "type": "relation",
                    "date": fpath.stem,
                    **r
                }
                save_graph_entry(entry)
                existing_relation_counts[key] = 1
                all_new_relations.append(r)  # 追加dict，供 update_relations_trend 使用
                print(f"  [NEW RELATION] {key}")

    # 更新趋势
    update_relations_trend(all_new_relations, existing_relation_counts)
    print(f"[entity_extractor] relations-trend.md 已更新")

    # 更新仪表板
    proj_mentions = update_dashboard(all_new_entities, all_new_relations)
    print(f"[entity_extractor] dashboard 已更新，{proj_mentions} 个项目今日提及")

    # push通知
    n_ents = len(all_new_entities)
    n_rels = len(all_new_relations)
    if n_ents > 0 or n_rels > 0:
        msg = f"21:30 实体抽取已出"
        detail = f"{n_ents} 实体 + {n_rels} 关系入 graph"
        call_push_queue(msg, detail, "21:30-cron")
        print(f"[entity_extractor] push通知已发送: {detail}")
    else:
        print("[entity_extractor] 无新增，跳过push")

    print(f"[entity_extractor] 完成！新增 {n_ents} 实体, {n_rels} 关系")
    return n_ents, n_rels


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python entity_extractor.py [today|full|--days N]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "today":
        run_extraction(days=1)
    elif cmd == "full":
        run_extraction(full=True)
    elif cmd == "--days" and len(sys.argv) >= 3:
        run_extraction(days=int(sys.argv[2]))
    else:
        print("用法: python entity_extractor.py [today|full|--days N]")
        sys.exit(1)
