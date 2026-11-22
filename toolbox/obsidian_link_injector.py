#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
obsidian_link_injector.py

给 50-外部接入 下今天搬来的 .md 批量加 wikilink

策略:
1. 读每个文件的标题 + 正文前 500 字
2. 用关键词匹配映射 MOC + 已有热门笔记
3. 在 frontmatter 之后的正文末尾加 "## 🔗 相关笔记" 区块
4. 不动 frontmatter, 不动正文, 增量追加

安全:
- 原文件不动 frontmatter (除非没有就建一个)
- 用 ## 区块而不用 inline field (Obsidian 视觉可读)
- 已经有 ## 🔗 相关笔记 的文件跳过
- 写操作原子: 先 build 新内容 -> 一次性 write
"""
import sys, re
from pathlib import Path
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
TODAY = datetime.now().strftime("%Y-%m-%d")

# === 关键词 -> wikilink 映射 ===
# 每个 tuple: (匹配关键词列表, wikilink 目标, 权重)
KEYWORD_MAP = [
    # AHL 平台 MOC
    (["AHL", "去中心化", "AI 酒店", "AI单体", "AI赋能单体", "酒店数字化", "酒店AI",
      "中心化预订", "AI 数字员工", "令牌", "token经济", "Token", "春熙宾馆",
      "智能托管", "AHL管家", "AHL-Agent", "酒店AI解决方案"], "AHL 平台 MOC", 3),

    # 酒店行业 MOC
    (["酒店", "饭店", "民宿", "客房", "OTA", "RevPAR", "ADR", "OCC",
      "入住率", "ADR", "管理层", "收益管理", "前厅", "客房部", "餐饮部",
      "SOP", "维景", "中旅", "国旅", "酒店集团", "单体酒店",
      "星级", "五星", "四星", "三星"], "酒店行业 MOC", 3),

    # AI-Agent MOC
    (["Agent", "LLM", "GPT", "DeepSeek", "大模型", "提示词",
      "智能体", "SKILL", "MCP", "工具调用", "Function call", "RAG",
      "Embedding", "知识库", "Skill", "知识图谱"], "AI-Agent MOC", 3),

    # 安逸集团 D-day MOC
    (["安逸", "产业发展部", "集团", "十五五", "1234战略", "1244",
      "省旅投", "文旅", "巴蜀", "蜀文化", "蜀地"],
     "安逸集团-D-day MOC", 3),

    # 战略方法论
    (["战略", "方法论", "博弈论", "群论", "第一性", "奥卡姆",
      "STP", "定位", "差异化", "杠杆"],
     "战略-方法论 MOC", 2),

    # Eric 人格审美
    (["审美", "气韵", "意境", "Bach", "Lube", "音乐", "人格",
      "性格", "价值观", "B166ER 人格"],
     "Eric 人格-审美 MOC", 1),

    # 工具-系统
    (["Obsidian", "Vault", "Skill", "MCP", "脚本", "Python",
      "PowerShell", "工具链", "插件", "配置文件"],
     "工具-系统 MOC", 2),

    # B166ER 知识库
    (["B166ER", "Agent", "MCP服务器", "提示词库"],
     "B166ER 知识库 MOC", 2),

    # 跨境-出海
    (["跨境", "出海", "Booking", "Agoda", "TripAdvisor",
      "境外", "海外", "international"],
     "跨境-出海 MOC", 3),

    # 安逸集团知识库 (vault 已有)
    (["安逸集团知识库", "安逸十五五"],
     "../../02-安逸集团知识库-20260720/README", 2),

    # Token/经销商 (AHL 经济的核心)
    (["TOKEN", "Token", "token", "经销商", "分销"],
     "AHL 平台 MOC", 2),

    # SKILL (AHL Agent 核心机制)
    (["SKILL", "Skill", "skill", "全生命周期"],
     "AI-Agent MOC", 2),

    # 酒管供应链
    (["酒管", "供应链", "采购", "供应链工程", "采购总监"],
     "酒店行业 MOC", 2),

    # DeepSeek / 大模型
    (["DeepSeek", "Claude", "GPT-4", "Qwen", "API Key", "API密钥"],
     "AI-Agent MOC", 2),

    # 专利 / 法律
    (["专利", "补正", "权利要求", "说明书", "代理人", "知识产权"],
     "工具-系统 MOC", 1),

    # 软著
    (["软著", "软件著作权"],
     "工具-系统 MOC", 1),

    # 营销 / 详情页 (产品矩阵相关)
    (["详情页", "小红书", "营销", "九宫格", "海报", "详情图"],
     "B166ER 知识库 MOC", 1),

    # 安逸相关 (具体笔记)
    (["轻重分离", "1+5", "发展战略"],
     "../00-我们共同维护的/战略与节奏/03-安逸集团机会", 1),

    # 00-Dashboard (vault 核心 hub)
    (["dashboard", "面板", "控制台"],
     "../../20-我们共同维护的/00-Dashboard", 1),

    # 00-今日重点
    (["今日重点", "重点"],
     "../../20-我们共同维护的/00-今日重点", 1),
]

# 今天搬来的目录(在 50-外部接入 下)
TODAY_DIRS = [
    "张实项目总控",
    "新媒体产品线",
    "小红书产品线",
    "AHL源代码-docs",
    "AHL专利-原始申请",
    "AHL专利-技术材料",
    "AHL专利-补正",
    "AHL软著申请",
    "知局-v1.0",
    "自我革命",
    # 01-安逸入职物料-20260707 因为已有 9 个 source-desktop 在 vault,不重复处理
]


def pick_links(file_text: str, max_links: int = 5) -> list:
    """给一个文件挑最多 max_links 个 wikilink"""
    # 取文本: 标题 + 前 500 字
    title_match = re.search(r'^#+\s*(.+?)$', file_text, re.M)
    title = title_match.group(1) if title_match else ""

    # 去掉 frontmatter
    body = re.sub(r'^---\n.*?\n---\n', '', file_text, count=1, flags=re.S)
    preview = (title + "\n" + body[:500]).lower()

    # 关键词匹配
    candidates = []  # (score, link)
    for keywords, link, weight in KEYWORD_MAP:
        for kw in keywords:
            if kw.lower() in preview:
                candidates.append((weight, link))
                break

    # 去重, 排序, 取 top N
    seen = set()
    unique = []
    for score, link in candidates:
        if link not in seen:
            seen.add(link)
            unique.append((score, link))
    unique.sort(key=lambda x: -x[0])

    return [link for _, link in unique[:max_links]]


def has_related_section(text: str) -> bool:
    """检查文件是否已经有 ## 🔗 相关笔记 区块"""
    # 匹配 "## 🔗 相关笔记" 或 "## 相关笔记" 或 "## related"
    return bool(re.search(r'^##\s*(🔗\s*相关笔记|相关笔记|related)', text, re.M | re.I))


def read_text_robust(file: Path) -> str:
    """鲁棒读文本: 尝试 utf-8 -> utf-8-sig -> gbk -> gb18030 -> latin-1"""
    raw = file.read_bytes()
    for enc in ('utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'latin-1'):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode('utf-8', errors='ignore')


def inject_links(file: Path, dry_run: bool = False) -> dict:
    """给一个文件注入相关链接"""
    try:
        text = read_text_robust(file)
    except Exception as e:
        return {"file": str(file), "status": "READ_ERROR", "error": str(e)}

    if has_related_section(text):
        return {"file": str(file), "status": "SKIP_EXISTING"}

    links = pick_links(text)
    if not links:
        return {"file": str(file), "status": "NO_KEYWORDS"}

    # 构造 related 区块
    bullet = "\n".join(f"- [[{l}]]" for l in links)

    new_section = f"""

---

## 🔗 相关笔记

{bullet}

*该区块由 B166ER 自动注入 ({TODAY}) — 关键词匹配*
"""

    new_text = text.rstrip() + "\n" + new_section

    if dry_run:
        return {
            "file": str(file),
            "status": "DRY_RUN",
            "links": links
        }

    try:
        file.write_text(new_text, encoding='utf-8')
        return {"file": str(file), "status": "OK", "links": links}
    except Exception as e:
        return {"file": str(file), "status": "WRITE_ERROR", "error": str(e)}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help='只报告,不动文件')
    args = ap.parse_args()

    print(f"=== 批量加 wikilink (dry_run={args.dry_run}) ===\n")

    # 收集所有今天的 .md
    files = []
    for d in TODAY_DIRS:
        dp = VAULT / "50-外部接入" / d
        if dp.exists():
            files.extend(dp.rglob("*.md"))

    print(f"待处理文件: {len(files)}")

    # 处理
    stats = {"OK": 0, "SKIP_EXISTING": 0, "NO_KEYWORDS": 0, "ERROR": 0}
    samples = []
    for f in files:
        r = inject_links(f, dry_run=args.dry_run)
        status = r["status"]
        stats[status] = stats.get(status, 0) + 1
        if status == "OK" and len(samples) < 5:
            samples.append((f.relative_to(VAULT), r.get("links", [])))

    print(f"\n=== 结果 ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    if samples and not args.dry_run:
        print(f"\n=== 样本 (前 5 个) ===")
        for f, links in samples:
            print(f"\n  {f}")
            for l in links:
                print(f"    + [[{l}]]")


if __name__ == "__main__":
    main()