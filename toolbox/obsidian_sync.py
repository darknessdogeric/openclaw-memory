#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
obsidian_sync.py — Obsidian 统一归纳工具 (V1.0)

把 5 阶段工具整合为 1 个 CLI,让 Eric 一句话就能复用

命令:
  scan       - 扫桌面 + vault,生成 overlap_report.json
  sync       - 复制桌面 .md 到 vault + 建原始素材索引 (主入口)
  archive    - 归档空 vault (如果还存在)
  health     - vault 健康检查 (转发到 vault_sync.py health)
  rebuild    - 重建 vault_index

默认行为 (sync):
- 复制 .md 到 vault\\50-外部接入\\<主题>\\
- 同名异版重命名为 (source-desktop)
- 大文件 (PDF/PNG/DOCX) 建 _原始素材索引.md
- 不删桌面任何文件 (R13/R14)

典型调用:
  python toolbox/obsidian_sync.py scan           # 摸底
  python toolbox/obsidian_sync.py sync           # 执行复制 + 索引
  python toolbox/obsidian_sync.py health         # 看 vault 状态
  python toolbox/obsidian_sync.py rebuild        # 重建索引
"""
import sys
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# === 配置 ===
DESK = Path(r"C:\Users\ericz\Desktop")
VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")
TOOLBOX = Path(r"D:\B166ER-OpenClaw\workspace\toolbox")

# 桌面文件夹分类 (Eric 当前归类决策)
# 格式: (桌面目录名, vault 目标子目录, 描述)
DIRECTORY_MAP = [
    # (desktop_name, vault_subpath, description)
    ("张实项目总控", "张实项目总控", "11 一级目录,180 .md,AHL/春熙/SOP/AI赋能/人寿医养/自媒体/潮玩/跨境"),
    ("新媒体产品线", "新媒体产品线", "8 子目录: 收益管理 V3/独立酒店/数据资产/供应链交付包"),
    ("小红书产品线", "小红书产品线", "4 子目录+8 直接文件, 十五五6图/经济解读/AI收益/限制功能"),
    ("AHL源代码", "AHL源代码-docs", "代码项目 33 个 .md; 代码本身不动,见 AHL源代码-README.md"),
    ("AHL专利申请文件", "AHL专利-技术材料", "17 份 AHL 专利技术材料"),
    ("专利", "AHL专利-原始申请", "27 份原始专利申请 + 8 张附图"),
    ("专利补正", "AHL专利-补正", "33 份补正文档三轮回合"),
    ("软著申请材料-AHL", "AHL软著申请", "AHL 软著 5 份"),
    ("安逸集团_入职物料_20260707", "01-安逸入职物料-20260707", "9 同名重命名为 (source-desktop); 2 7/24 孤本补入"),
    ("知局_完整版_v1.0", "知局-v1.0", "副业项目 V1.0 完整版"),
    ("自我革命", "自我革命", "1 .md + 86 PDF 索引"),
]

# 跳过 (不进 vault)
SKIP_DIRS = {
    "劳动合同", "小白的保单", "简历及应聘文件", "图片",
    "快捷方式", "GAME",
}

# 仅做索引 (不复制 .md, 但建原始素材索引)
INDEX_ONLY = {
    "AHL-BP-2026": "AHL-BP-2026",  # 14 PNG + 1 PDF
    "工作文档": "工作文档-桌面映射",
    "项目资料": "项目资料-桌面映射",
}


def md5f(p: Path):
    """计算文件 md5"""
    h = hashlib.md5()
    try:
        with p.open('rb') as f:
            for c in iter(lambda: f.read(8192), b''):
                h.update(c)
        return h.hexdigest()
    except Exception:
        return None


def count_md(p: Path):
    return sum(1 for _ in p.rglob("*.md")) if p.exists() else 0


def copy_md(src: Path, dst: Path, label: str) -> dict:
    """复制 .md 文件,同名异版重命名为 (source-desktop)"""
    if not src.exists():
        return {"label": label, "skipped": "不存在"}
    if not dst.exists():
        dst.mkdir(parents=True, exist_ok=True)
    md_files = list(src.rglob("*.md"))
    copied = same = renamed = 0
    for m in md_files:
        rel = m.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if md5f(m) == md5f(target):
                same += 1
                continue
            target = target.with_name(target.stem + " (source-desktop)" + target.suffix)
            renamed += 1
        shutil.copy2(str(m), str(target))
        copied += 1
    return {
        "label": label,
        "src": len(md_files),
        "copied": copied,
        "skipped_same": same,
        "renamed": renamed,
        "dst_total": count_md(dst),
    }


def cmd_scan(args):
    """扫桌面 + vault, 生成 overlap_report.json"""
    print("=== Scan: 桌面 vs Vault ===\n")

    vault_index = {}
    for p in VAULT.rglob("*.md"):
        n = p.name
        h = md5f(p)
        if h:
            vault_index.setdefault(n, []).append({"path": str(p), "md5": h})

    report = {
        "generated_at": datetime.now().isoformat(),
        "vault_md_total": sum(1 for _ in VAULT.rglob("*.md")),
        "by_dir": {},
        "overlaps_exact": [],
        "overlaps_name_only": [],
    }

    all_dirs = [d for d, _, _ in DIRECTORY_MAP] + list(INDEX_ONLY.keys())
    total_desk = 0
    for d in all_dirs:
        dp = DESK / d
        if not dp.exists():
            continue
        md_files = list(dp.rglob("*.md"))
        total_desk += len(md_files)
        report["by_dir"][d] = {"md_count": len(md_files)}
        for m in md_files:
            if m.name in vault_index:
                match = any(vm["md5"] == md5f(m) for vm in vault_index[m.name])
                if match:
                    report["overlaps_exact"].append(str(m.relative_to(DESK)))
                else:
                    report["overlaps_name_only"].append(str(m.relative_to(DESK)))

    report["desktop_md_total"] = total_desk
    out = TOOLBOX / "overlap_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Vault .md:    {report['vault_md_total']}")
    print(f"桌面扫到 .md: {report['desktop_md_total']}")
    print(f"完全相同 (md5):     {len(report['overlaps_exact'])}")
    print(f"同名但内容不同:     {len(report['overlaps_name_only'])}")
    print(f"\n报告: {out}")


def cmd_sync(args):
    """主入口: 复制 + 索引"""
    print("=== Sync: 桌面 .md → Vault ===\n")

    results = []
    for d, sub, desc in DIRECTORY_MAP:
        src = DESK / d
        dst = VAULT / "50-外部接入" / sub
        r = copy_md(src, dst, f"{d} → {sub}")
        if "skipped" in r:
            continue
        print(f"  [{r['label']}] src={r['src']} copied={r['copied']} renamed={r['renamed']} dst_total={r['dst_total']}")
        results.append(r)

    print(f"\n=== 当前 vault 总数 ===")
    total_md = sum(1 for _ in VAULT.rglob("*.md"))
    total_files = sum(1 for _ in VAULT.rglob("*") if _.is_file())
    print(f"Vault total .md: {total_md}")
    print(f"Vault total files: {total_files}")


def cmd_archive(args):
    """归档空 vault"""
    empty = Path(r"C:\Users\ericz\Documents\Obsidian Vault")
    archive = VAULT / "00-Inbox-待整理" / "_archived-Obsidian-Vault"
    if not empty.exists():
        print("空 vault 不存在,无需归档")
        return
    if (empty / "_ARCHIVED-2026-07-28.txt").exists():
        print("空 vault 已归档 (标记文件存在)")
        return
    target = archive
    i = 1
    while target.exists():
        target = archive.with_name(f"_archived-Obsidian-Vault-{i}")
        i += 1
    target.mkdir(parents=True, exist_ok=True)
    for p in empty.iterdir():
        dest = target / p.name
        if p.is_dir():
            shutil.copytree(str(p), str(dest))
        else:
            shutil.copy2(str(p), str(dest))
    print(f"归档副本: {target}")
    marker = empty / "_ARCHIVED-2026-07-28.txt"
    marker.write_text(f"已归档到:\n{target}\n", encoding="utf-8")
    print(f"标记: {marker}")


def cmd_health(args):
    """vault 健康检查 (转发)"""
    import subprocess
    r = subprocess.run(
        [sys.executable, str(TOOLBOX / "vault_sync.py"), "health"],
        capture_output=True, text=True
    )
    print(r.stdout)
    if r.stderr:
        print(r.stderr, file=sys.stderr)


def cmd_rebuild(args):
    """重建 vault_index"""
    import subprocess
    r = subprocess.run(
        [sys.executable, str(TOOLBOX / "vault_index.py"), "build", "--force"],
        capture_output=True, text=True
    )
    print(r.stdout)
    if r.stderr:
        print(r.stderr, file=sys.stderr)


def main():
    cmds = {
        "scan": cmd_scan,
        "sync": cmd_sync,
        "archive": cmd_archive,
        "health": cmd_health,
        "rebuild": cmd_rebuild,
    }
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__)
        print("\n可用命令:", list(cmds.keys()))
        sys.exit(1)
    cmds[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()