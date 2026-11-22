#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ROI 2: 给 311 个新加 related 的文件,做反向 link

策略:
1. 找出 311 个加了 related 区块的文件
2. 对每个文件 extract "它在 vault 里实际位置是哪里 / 它属于什么主题"
3. 按主题聚类
4. 给每个主题生成"主题卡片"放在对应 hub MOC 的"## 相关笔记" section
5. 或: 直接在 hub MOC 里 inline 加 [[文件名]] 引用
"""
import sys, re
from pathlib import Path
from collections import defaultdict, Counter
sys.stdout.reconfigure(encoding='utf-8')

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")

# 找今天处理过的文件 (50-外部接入 下今天搬来的)
TODAY_DIRS = ["张实项目总控", "新媒体产品线", "小红书产品线",
              "AHL源代码-docs", "AHL专利-原始申请", "AHL专利-技术材料",
              "AHL专利-补正", "AHL软著申请", "知局-v1.0", "自我革命"]


def read_text(file: Path):
    raw = file.read_bytes()
    for enc in ('utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'latin-1'):
        try: return raw.decode(enc)
        except: continue
    return raw.decode('utf-8', errors='ignore')


def extract_links_from_related(text: str):
    """从 ## 🔗 相关笔记 区块提取它指向的 MOC"""
    # 简化: 从 "## 🔗 相关笔记" 起,直到下一个 ## 或文末
    m = re.search(r'##\s*🔗\s*相关笔记\s*\n+(.+?)(?=\n##|\Z)', text, re.S)
    if not m: return []
    block = m.group(1)
    return re.findall(r'\[\[([^\]]+)\]\]', block)


def cluster_files():
    """按文件指向的 MOC 分组"""
    clusters = defaultdict(list)
    no_related = []
    for d in TODAY_DIRS:
        dp = VAULT / "50-外部接入" / d
        if not dp.exists(): continue
        for f in dp.rglob("*.md"):
            try:
                text = read_text(f)
            except:
                continue
            if "## 🔗 相关笔记" not in text:
                no_related.append(f.relative_to(VAULT))
                continue
            targets = extract_links_from_related(text)
            if not targets:
                no_related.append(f.relative_to(VAULT))
                continue
            # 用第一个 MOC 作为主分类
            main_topic = targets[0]
            clusters[main_topic].append(f.relative_to(VAULT))

    return clusters, no_related


def main():
    print("=== ROI 2: 文件主题聚类 ===\n")
    clusters, no_related = cluster_files()

    print(f"聚类数: {len(clusters)}")
    print(f"无 related 的文件: {len(no_related)}\n")

    print("=== 各主题文件数 ===")
    for topic in sorted(clusters.keys(), key=lambda t: -len(clusters[t])):
        print(f"\n### {topic} ({len(clusters[topic])} 文件)")
        for f in clusters[topic][:10]:
            print(f"  - {f}")
        if len(clusters[topic]) > 10:
            print(f"  ... ({len(clusters[topic])-10} more)")

    print(f"\n=== 无 related 的 {len(no_related)} 个文件 (前面已提取但还需手写) ===")
    for f in no_related[:10]:
        print(f"  {f}")


if __name__ == "__main__":
    main()