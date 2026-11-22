#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROI 2 实施: 给 hub MOC 加 ## 📋 桌面项目素材 区, 列出该主题的所有相关 .md

策略:
- 不破坏 MOC 原内容, 只在末尾追加
- wikilink 用相对路径: ../../50-外部接入/<dir>/<file>
- 按一级目录分组 (张实项目总控/, 新媒体产品线/, etc.)
- 加 frontmatter 标记: created + author (B166ER)

预期效果: 311 个孤岛 → 大部分变成"被反向链接"
"""
import sys, re
from pathlib import Path
from collections import defaultdict, OrderedDict
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
HUBS_DIR = VAULT / "emergence" / "hubs"
TODAY = "2026-07-28"
TODAY_DIRS = ["张实项目总控", "新媒体产品线", "小红书产品线",
              "AHL源代码-docs", "AHL专利-原始申请", "AHL专利-技术材料",
              "AHL专利-补正", "AHL软著申请", "知局-v1.0", "自我革命"]

# 主题映射: moc → 主要 wikilink target (在 related 区块中的第一个链接)
# 我们通过 MOC 文件里的相关 wiki link 来反推主题
TOPIC_MAP = {
    # MOC 路径 → 给它加的 section 里, 文件包含的 wikilink target
    "AHL 平台 MOC.md": "AHL 平台 MOC",
    "酒店行业 MOC.md": "酒店行业 MOC",
    "AI-Agent MOC.md": "AI-Agent MOC",
    "工具-系统 MOC.md": "工具-系统 MOC",
    "安逸集团-D-day MOC.md": "安逸集团-D-day MOC",
    "战略-方法论 MOC.md": "战略-方法论 MOC",
    "Eric 人格-审美 MOC.md": "Eric 人格-审美 MOC",
    "跨境-出海 MOC.md": "跨境-出海 MOC",
    "B166ER 知识库 MOC.md": "B166ER 知识库 MOC",
    # 死 MOC: 新媒体 MOC.md / B166ER 全景信息图 MOC.md 不处理
}


def read_text(file: Path):
    raw = file.read_bytes()
    for enc in ('utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'latin-1'):
        try: return raw.decode(enc)
        except: continue
    return raw.decode('utf-8', errors='ignore')


def extract_links_from_related(text: str):
    m = re.search(r'##\s*🔗\s*相关笔记\s*\n+(.+?)(?=\n##|\Z)', text, re.S)
    if not m: return []
    return re.findall(r'\[\[([^\]]+)\]\]', m.group(1))


def collect_files_by_topic():
    """按主题聚类文件"""
    topic_files = defaultdict(list)  # topic -> [(一级目录, [files]), ...]
    for d in TODAY_DIRS:
        dp = VAULT / "50-外部接入" / d
        if not dp.exists(): continue
        for f in dp.rglob("*.md"):
            try:
                text = read_text(f)
            except:
                continue
            targets = extract_links_from_related(text)
            if not targets:
                continue
            main_topic = targets[0]
            topic_files[main_topic].append((d, f.relative_to(VAULT)))
    return topic_files


def make_relative_link(moc_filename: str, file_rel: str):
    """生成 MOC 到 file 的相对路径 wikilink"""
    # moc 在: emergence/hubs/<name>
    # file 在: 50-外部接入/<dir>/...
    # 相对从 emergence/hubs/ → 需要 ../../50-外部接入/<dir>/<file>
    file_no_ext = str(file_rel).replace("\\", "/")
    return f"[[../../{file_no_ext}]]"


def build_section_for_moc(moc_filename: str, files_grouped: dict) -> str:
    """给一个 MOC 构建 ## 📋 桌面项目素材 section"""
    if not files_grouped:
        return ""

    section = f"""

---

## 📋 桌面项目素材 ({sum(len(v) for v in files_grouped.values())} 个)

> 由 B166ER 于 {TODAY} 注入 — 反向 link 桌面今日搬入的 {TODAY_DIRS} 目录素材
> 维护: 桌面新增 .md 自动同步 (scripts/obsidian_link_injector.py)

"""
    # 按一级目录分组
    for dir_name in sorted(files_grouped.keys()):
        section += f"\n### {dir_name} ({len(files_grouped[dir_name])} 个)\n\n"
        for file_rel in sorted(files_grouped[dir_name]):
            section += f"- {make_relative_link(moc_filename, file_rel)}\n"

    return section


def main():
    print(f"=== ROI 2: 给 hub MOC 加桌面素材索引 ({TODAY}) ===\n")

    topic_files = collect_files_by_topic()
    print(f"主题数: {len(topic_files)}")
    for t, lst in sorted(topic_files.items(), key=lambda x: -len(x[1])):
        print(f"  {t}: {len(lst)} 文件")
    print()

    # 给 9 个 hub MOC 各自加 section
    added_count = 0
    for moc_file, topic in TOPIC_MAP.items():
        moc_path = HUBS_DIR / moc_file
        if not moc_path.exists():
            print(f"[跳过] {moc_file} 不存在")
            continue

        # 收集该主题的所有文件 (按一级目录分组)
        if topic not in topic_files:
            print(f"[跳过] {topic} 主题无文件")
            continue

        # topic_files[topic] 是 [(一级目录, file_rel), ...] 需要按一级目录重新分组
        grouped = defaultdict(list)
        for dir_name, file_rel in topic_files[topic]:
            grouped[dir_name].append(file_rel)

        section = build_section_for_moc(moc_file, grouped)
        if not section:
            continue

        # 检查是否已有该 section
        text = read_text(moc_path)
        if "## 📋 桌面项目素材" in text:
            print(f"[跳过] {moc_file} 已有桌面项目素材 section")
            continue

        # 追加
        new_text = text.rstrip() + "\n" + section
        moc_path.write_text(new_text, encoding="utf-8")
        file_count = sum(len(v) for v in grouped.values())
        print(f"[OK] {moc_file:<32} +{file_count} file links")
        added_count += 1

    print(f"\n=== 完成 ===")
    print(f"已更新 {added_count} 个 hub MOC")


if __name__ == "__main__":
    main()