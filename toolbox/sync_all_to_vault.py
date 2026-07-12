#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""全面同步 workspace -> vault (智能去重 + 按类目组织)"""
import sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")

# ===== 智能去重规则 =====
# 跳过: 临时/重复/过期的文件
SKIP_PATTERNS = [
    'music_batch_',  # 音乐批次（重复）
    'music_deep_research_backup',  # 旧备份
    'music_deep_research_combined',  # 旧版
    '_check_', '_test_', '_tmp_',  # 测试/临时
    '-temp.md',  # 临时日记
    'B166ER-军团能力清单',  # 已被能力图谱覆盖
    'B166ER-skill-upgrade-checklist',  # 过程文件
]

# 必同步的 workspace 根目录核心
WORKSPACE_CORE = [
    'AGENTS.md', 'MEMORY.md', 'HEARTBEAT.md', 'SOUL.md', 'USER.md',
    'IDENTITY.md', 'TOOLS.md', 'PROJECT-TRACKING.md', 'DREAMS.md',
    'B166ER-STYLE.md', 'B166ER-底层理论架构-V2.2.md',
]

# AHL 相关 workspace 根
AHL_ROOT = [
    'AHL-4层架构图.md', 'AHL-Agent-Skill完整说明书.md',
    'AHL-Agent-Skill技术团队完整说明书.md', 'AHL-Archive-System.md',
    'AHL-Product-Catalog.md', 'AHL-电梯演讲-一页纸.md',
    'AHL组织架构演进方案.md', 'AHL-数据库关联配置.md',
    'ahl-marketing-agent-architecture-v2.md', 'ahl-marketing-agent-architecture-v3.md',
    'ahl-marketing-member-agent-architecture-v1.md',
    'AHL试点-岗位问题采集问卷集.md', 'AHL试点培训材料-全体员工版.md',
    'AHL试点培训材料-内部使用.md', 'API申请指南.md',
    'b-agent-revenue-management-SKILL-v2.md', 'b-agent-revenue-management-SKILL.md',
]

# B166ER 工具/项目根
B166ER_ROOT = [
    'B166ER-爬虫能力提升方案.md',
]


def should_skip(name: str) -> bool:
    for p in SKIP_PATTERNS:
        if p in name:
            return True
    return False


def sync_file(src: Path, dst: Path, label: str = ""):
    """同步一个文件"""
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def main():
    stats = {
        'workspace_core': 0, 'ahl_root': 0, 'b166er_root': 0,
        'memory_kb': 0, 'memory_diary': 0,
        'reports': 0, 'docs': 0, 'skipped': 0,
    }

    # ===== Phase 1: workspace 根核心 =====
    print("=" * 60)
    print("Phase 1: workspace 根核心 → 00-Workspace-核心/")
    print("=" * 60)
    dst_dir = VAULT / "00-Workspace-核心"
    for f in WORKSPACE_CORE:
        src = WORKSPACE / f
        if not src.exists():
            continue
        if sync_file(src, dst_dir / f, "核心"):
            print(f"  [OK] {f} ({src.stat().st_size}b)")
            stats['workspace_core'] += 1

    # ===== Phase 2: AHL 根文件 → 20-我们共同维护的/项目档案/AHL/ =====
    print("\n" + "=" * 60)
    print("Phase 2: AHL 根 → 20-我们共同维护的/项目档案/AHL/")
    print("=" * 60)
    dst_dir = VAULT / "20-我们共同维护的" / "项目档案" / "AHL"
    for f in AHL_ROOT:
        src = WORKSPACE / f
        if not src.exists():
            continue
        if sync_file(src, dst_dir / f, "AHL"):
            print(f"  [OK] {f} ({src.stat().st_size}b)")
            stats['ahl_root'] += 1

    # ===== Phase 3: B166ER 工具/项目根 → 20-我们共同维护的/项目档案/B166ER/ =====
    print("\n" + "=" * 60)
    print("Phase 3: B166ER 根 → 20-我们共同维护的/项目档案/B166ER/")
    print("=" * 60)
    dst_dir = VAULT / "20-我们共同维护的" / "项目档案" / "B166ER"
    for f in B166ER_ROOT:
        src = WORKSPACE / f
        if not src.exists():
            continue
        if sync_file(src, dst_dir / f, "B166ER"):
            print(f"  [OK] {f} ({src.stat().st_size}b)")
            stats['b166er_root'] += 1

    # ===== Phase 4: memory/ 全部 KB → 10-我为你生成的/知识库/ =====
    print("\n" + "=" * 60)
    print("Phase 4: memory/ KB → 10-我为你生成的/知识库/")
    print("=" * 60)
    dst_dir = VAULT / "10-我为你生成的" / "知识库"
    mem_dir = WORKSPACE / "memory"
    if mem_dir.exists():
        for f in sorted(mem_dir.glob("*.md")):
            if should_skip(f.name):
                stats['skipped'] += 1
                continue
            # 日记 (YYYY-MM-DD 开头) → 01-日记
            import re
            if re.match(r'^\d{4}-\d{2}-\d{2}', f.name):
                dst = VAULT / "01-日记" / f.name
                if sync_file(f, dst, "日记"):
                    stats['memory_diary'] += 1
            else:
                # KB
                dst = dst_dir / f.name
                if sync_file(f, dst, "KB"):
                    stats['memory_kb'] += 1
    print(f"  KB: {stats['memory_kb']} | 日记: {stats['memory_diary']} | 跳过: {stats['skipped']}")

    # ===== Phase 5: reports/ 全部 → 20-我们共同维护的/报告/ =====
    print("\n" + "=" * 60)
    print("Phase 5: reports/ → 20-我们共同维护的/报告/")
    print("=" * 60)
    dst_dir = VAULT / "20-我们共同维护的" / "报告"
    rep_dir = WORKSPACE / "reports"
    if rep_dir.exists():
        for f in sorted(rep_dir.glob("*.md")):
            if should_skip(f.name):
                continue
            if sync_file(f, dst_dir / f.name, "报告"):
                print(f"  [OK] {f.name} ({f.stat().st_size}b)")
                stats['reports'] += 1

    # ===== Phase 6: docs/ 全部 → 20-我们共同维护的/技术文档/ =====
    print("\n" + "=" * 60)
    print("Phase 6: docs/ → 20-我们共同维护的/技术文档/")
    print("=" * 60)
    dst_dir = VAULT / "20-我们共同维护的" / "技术文档"
    docs_dir = WORKSPACE / "docs"
    if docs_dir.exists():
        for f in sorted(docs_dir.glob("*.md")):
            if should_skip(f.name):
                continue
            # 分类子目录
            if 'AHL' in f.name or 'ahl' in f.name:
                sub = "AHL"
            elif 'B166ER' in f.name or 'B166ER' in f.name.lower():
                sub = "B166ER"
            elif '收益' in f.name or '酒店' in f.name or '民宿' in f.name or '生产' in f.name:
                sub = "酒店行业"
            elif '博弈' in f.name or '审美' in f.name or '递归' in f.name or '成长' in f.name:
                sub = "思维方法"
            elif 'AHL' not in f.name and 'ahl' not in f.name and 'Agent' in f.name:
                sub = "AHL"  # AHL-Agent-Skill → AHL
            else:
                sub = "其他"
            target = dst_dir / sub / f.name
            if sync_file(f, target, f"{sub}"):
                stats['docs'] += 1
    print(f"  文档: {stats['docs']}")

    # ===== 最终统计 =====
    print("\n" + "=" * 60)
    print("同步完成")
    print("=" * 60)
    total = sum(stats.values())
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"  TOTAL: {total} 文件")
    print()

    # 重新统计 vault
    md = list(VAULT.rglob("*.md"))
    print(f"  VAULT 总 .md: {len(md)}")
    print(f"  VAULT 总目录数: {len(list(VAULT.rglob('*')))}")


if __name__ == "__main__":
    main()
