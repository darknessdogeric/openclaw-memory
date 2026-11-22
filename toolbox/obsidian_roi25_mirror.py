#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ROI 2.5 mirror: 把 ROI 2.5 加了 related 的 67 个文件的 mirror 反向 link 加到 hub MOC"""
import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
HUBS_DIR = VAULT / "emergence" / "hubs"


def read_text(file: Path):
    raw = file.read_bytes()
    for enc in ('utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'latin-1'):
        try: return raw.decode(enc)
        except: continue
    return raw.decode('utf-8', errors='ignore')


def get_roi25_files():
    """找 ROI 2.5 新增的相关文件 (有 ## 🔗 相关笔记 但 stem 不在 backlink_count)"""
    all_md = list(VAULT.rglob("*.md"))
    bl = {}
    for p in all_md:
        try: t = read_text(p)
        except: continue
        for l in re.findall(r'\[\[([^\]|#]+)', t):
            target = l.strip().split('/')[-1].strip().rstrip('.md').lower()
            if target: bl[target] = bl.get(target, 0) + 1

    # 孤岛 = stem 不在 backlink_count
    islands = [p for p in all_md if p.stem.lower() not in bl]

    # 从孤岛里筛出"有 ## 🔗 相关笔记 但还没被反向 link"的
    candidates = []
    for p in islands:
        try: t = read_text(p)
        except: continue
        if "## 🔗 相关笔记" not in t:
            continue
        # ROI 2.5 标识
        if "ROI 2.5" not in t:
            continue
        # 提取主题 (related 区块的第一个 wikilink target, 但去掉 .md)
        m = re.search(r'##\s*🔗\s*相关笔记\s*\n+(.+?)(?=\n##|\Z)', t, re.S)
        if not m: continue
        targets = re.findall(r'\[\[([^\]]+)\]\]', m.group(1))
        if not targets:
            continue
        main_topic = targets[0].strip()
        candidates.append((p, main_topic))
    return candidates


def main():
    print("=== ROI 2.5 mirror: 反向 link 添加到 hub MOC ===\n")
    candidates = get_roi25_files()
    print(f"候选文件: {len(candidates)}")

    # 按 topic 分组
    from collections import defaultdict
    by_topic = defaultdict(list)
    for f, topic in candidates:
        by_topic[topic].append(f)

    # moc filename 映射
    topic_to_moc = {
        "安逸集团-D-day MOC": "安逸集团-D-day MOC.md",
        "酒店行业 MOC": "酒店行业 MOC.md",
        "AHL 平台 MOC": "AHL 平台 MOC.md",
        "战略-方法论 MOC": "战略-方法论 MOC.md",
        "AI-Agent MOC": "AI-Agent MOC.md",
        "工具-系统 MOC": "工具-系统 MOC.md",
        "B166ER 知识库 MOC": "B166ER 知识库 MOC.md",
    }

    total_added = 0
    for topic, files in by_topic.items():
        moc_file = topic_to_moc.get(topic)
        if not moc_file:
            print(f"[跳过] {topic} 无对应 MOC 文件")
            continue
        moc_path = HUBS_DIR / moc_file
        if not moc_path.exists():
            print(f"[跳过] {moc_file} 不存在")
            continue

        text = read_text(moc_path)
        # 找 "## 📋 桌面项目素材" 区块,从这里追加
        # 策略: 在 MOC 末尾追加一个 "## 📋 桌面项目素材 (补遗)" section
        # 这样不会破坏原有内容

        # 检查是否已有补充 section
        sup_marker = "## 📋 桌面项目补遗"
        if sup_marker in text:
            # 已经有这个 section, 把文件加进去
            # 先去掉尾部, 重新构建
            base = text.split(sup_marker)[0]
            existing_sup = text.split(sup_marker)[1]
            # 解析已存在的文件列表
            existing_files = set(re.findall(r'- \[\[(.+?)\]\]', existing_sup))
            new_files = [f for f in files if make_rel(moc_file, f.relative_to(VAULT)) not in {ef.replace('../../', '') for ef in existing_files}]
            if not new_files:
                print(f"[跳过] {moc_file} 补遗已包含所有 {topic} 文件")
                continue
            # 追加到补遗
            new_section_text = sup_marker + "\n\n" + existing_sup
            for f in new_files:
                rel = make_rel(moc_file, f.relative_to(VAULT))
                new_section_text += f"- [[../../{rel}]]\n"
            new_text = base + new_section_text
            moc_path.write_text(new_text, encoding='utf-8')
            print(f"[追加] {moc_file} +{len(new_files)} 文件")
            total_added += len(new_files)
        else:
            # 新建补遗 section
            section = "\n\n---\n\n## 📋 桌面项目补遗 (ROI 2.5 补漏)\n\n"
            for f in sorted(files):
                rel = make_rel(moc_file, f.relative_to(VAULT))
                section += f"- [[../../{rel}]]\n"
            new_text = text.rstrip() + section
            moc_path.write_text(new_text, encoding='utf-8')
            print(f"[新建] {moc_file} +{len(files)} 文件")
            total_added += len(files)

    print(f"\n=== 总追加: {total_added} 文件 ===")


def make_rel(moc_filename: str, file_rel: Path):
    """MOC → file 的相对路径"""
    return str(file_rel).replace("\\", "/")


if __name__ == "__main__":
    main()