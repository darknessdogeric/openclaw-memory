#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ROI 2.5: 补 90 个 50-外部接入 漏网孤岛"""
import sys, re
from pathlib import Path
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
TODAY = "2026-07-28"

# 找所有 50-外部接入 的孤岛
def read_text(file: Path):
    raw = file.read_bytes()
    for enc in ('utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'latin-1'):
        try: return raw.decode(enc)
        except: continue
    return raw.decode('utf-8', errors='ignore')


def get_islands():
    all_md = list(VAULT.rglob("*.md"))
    bl = {}
    for p in all_md:
        try: t = read_text(p)
        except: continue
        for l in re.findall(r'\[\[([^\]|#]+)', t):
            target = l.strip().split('/')[-1].strip().rstrip('.md').lower()
            if target: bl[target] = bl.get(target, 0) + 1
    islands = []
    for p in all_md:
        if '50-外部接入' in str(p) and p.stem.lower() not in bl:
            islands.append(p)
    return islands


def pick_topic(file: Path, title: str, preview: str) -> list:
    """根据文件名+标题+预览,挑相关 wikilinks (扩展关键词覆盖)"""
    # 主题分类 (优先级降序)
    # 检查关键词
    preview_lower = preview.lower()
    title_lower = title.lower()

    topics = []  # (score, link)

    # 旅游强国 / 十五五
    if '旅游强国' in preview or '十五五' in preview:
        topics.append((3, "安逸集团-D-day MOC"))
        topics.append((2, "战略-方法论 MOC"))
    # FMHY
    if 'fmhy' in preview_lower:
        topics.append((3, "B166ER 知识库 MOC"))
        topics.append((2, "工具-系统 MOC"))
    # AHL源代码索引
    if 'ahl源代码' in preview_lower or '源代码' in title_lower and 'ahl' in preview_lower:
        topics.append((3, "AHL 平台 MOC"))
    # 张实项目总控索引
    if '张实项目总控' in title or '原始素材' in title:
        topics.append((3, "AHL 平台 MOC"))
        topics.append((2, "酒店行业 MOC"))
    # 安逸 (source-desktop 副本)
    if '安逸' in title or '安逸' in preview:
        topics.append((3, "安逸集团-D-day MOC"))
    # 7/24 研讨会纪要
    if '研讨会' in title or '研讨会' in preview:
        topics.append((3, "安逸集团-D-day MOC"))
    # 酒店
    if '酒店' in title or '酒店' in preview:
        topics.append((2, "酒店行业 MOC"))
    # 收益管理
    if '收益管理' in title or '收益管理' in preview:
        topics.append((3, "AHL 平台 MOC"))
        topics.append((2, "酒店行业 MOC"))
    # 默认
    if not topics:
        topics.append((1, "工具-系统 MOC"))

    # 去重排序
    seen = set()
    unique = []
    for score, link in topics:
        if link not in seen:
            seen.add(link)
            unique.append((score, link))
    unique.sort(key=lambda x: -x[0])
    return [l for _, l in unique[:3]]


def inject(file: Path, links: list, dry_run=False):
    try: text = read_text(file)
    except: return "READ_ERROR"
    if "## 🔗 相关笔记" in text:
        return "SKIP_EXISTING"
    bullet = "\n".join(f"- [[{l}]]" for l in links)
    section = f"\n\n---\n\n## 🔗 相关笔记\n\n{bullet}\n\n*该区块由 B166ER 自动注入 ({TODAY}) — ROI 2.5 漏网修复*\n"
    if dry_run:
        return "DRY_RUN"
    try:
        # 不管有无 frontmatter, 直接 append
        new_text = text.rstrip() + section
        file.write_text(new_text, encoding='utf-8')
        return "OK"
    except:
        return "WRITE_ERROR"


def main():
    print("=== ROI 2.5: 补 50-外部接入 漏网孤岛 ===\n")
    islands = get_islands()
    print(f"找到 {len(islands)} 个孤岛")

    stats = {"OK": 0, "SKIP_EXISTING": 0, "READ_ERROR": 0, "WRITE_ERROR": 0}
    samples = []
    for f in islands:
        try: t = read_text(f)
        except:
            stats["READ_ERROR"] += 1
            continue
        # 提取标题
        title_m = re.search(r'^#+\s*(.+?)$', t, re.M)
        title = title_m.group(1) if title_m else f.stem
        # 去掉 frontmatter
        body = re.sub(r'^---\n.*?\n---\n', '', t, count=1, flags=re.S)
        preview = title + "\n" + body[:300]

        links = pick_topic(f, title, preview)
        r = inject(f, links)
        stats[r] = stats.get(r, 0) + 1
        if r == "OK" and len(samples) < 8:
            samples.append((f.relative_to(VAULT), links))

    print(f"\n=== 结果 ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    if samples:
        print(f"\n=== 样本 (前 8 个) ===")
        for f, lks in samples:
            print(f"\n  {f}")
            for l in lks:
                print(f"    + [[{l}]]")


if __name__ == "__main__":
    main()