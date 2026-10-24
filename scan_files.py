# -*- coding: utf-8 -*-
"""
scan_files.py - B166ER 全盘知识文件扫描器 (V2.0, 2026-10-25 重建)
沿用历史版 scan_files.py 的语义（清单 + 报告），
但扫描根改为本机真实路径 D:\\B166ER-openclaw\\workspace（历史版指向已不存在的 C:\\Users\\ericz\\...）。
输出: memory/file_inventory.json + 扫描报告
"""
import os, json, sys, time
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(r"D:\B166ER-openclaw\workspace")
OPENCLAW = Path(r"D:\B166ER-openclaw")

SCAN_ROOTS = [
    WORKSPACE,
    OPENCLAW / "knowledge",
    OPENCLAW / "agents" / "main" / "agent" / "workshop-skills",
]

EXT_PRIORITY = {
    ".md": 1, ".txt": 2, ".json": 3, ".yaml": 4, ".yml": 4,
    ".csv": 5, ".py": 6, ".html": 7, ".css": 8, ".js": 9, ".ts": 10,
}

EXCLUDE_DIRS = {
    "node_modules", ".git", "__pycache__", "venv", ".venv",
    "备份", "归档", "archive", "temp", "tmp", ".cache", ".chroma_db",
    ".bak", "backups", ".archive-20260929", ".git_rebase_backup_20260914_171759",
    "site-packages", ".playwright-cli", ".npm", ".nvm", "dist", "build",
}


def scan_directory(root_path, max_depth=6):
    results = []
    if not root_path.exists():
        return results
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".git")]
        rel_depth = len(Path(root).relative_to(root_path).parts)
        if rel_depth > max_depth:
            dirs[:] = []
            continue
        for f in files:
            ext = Path(f).suffix.lower()
            if ext not in EXT_PRIORITY:
                continue
            full_path = Path(root) / f
            try:
                st = full_path.stat()
                results.append({
                    "path": str(full_path),
                    "rel": str(full_path.relative_to(WORKSPACE)) if str(full_path).startswith(str(WORKSPACE)) else str(full_path),
                    "name": f,
                    "ext": ext,
                    "size_kb": round(st.st_size / 1024, 1),
                    "mtime": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "priority": EXT_PRIORITY[ext],
                })
            except Exception:
                pass
    return results


def scan_all():
    all_files = []
    seen = set()
    for root in SCAN_ROOTS:
        print(f"  扫描: {root}")
        files = scan_directory(root)
        new = 0
        for f in files:
            if f["path"] in seen:
                continue
            seen.add(f["path"])
            all_files.append(f)
            new += 1
        print(f"    -> {new} 个可索引文件")
    all_files.sort(key=lambda x: (x["priority"], -x["size_kb"]))
    return all_files


def generate_report(files):
    by_ext, by_priority, total_mb = {}, {}, 0.0
    for f in files:
        by_ext[f["ext"]] = by_ext.get(f["ext"], 0) + 1
        by_priority[str(f["priority"])] = by_priority.get(str(f["priority"]), 0) + 1
        total_mb += f["size_kb"] / 1024
    by_dir = {}
    for f in files:
        top = f["rel"].split("\\")[0] if "\\" in f["rel"] else f["rel"]
        by_dir[top] = by_dir.get(top, 0) + 1
    return {
        "total": len(files),
        "by_ext": dict(sorted(by_ext.items(), key=lambda x: -x[1])),
        "by_top_dir": dict(sorted(by_dir.items(), key=lambda x: -x[1])[:30]),
        "total_size_mb": round(total_mb, 1),
        "md_files": [f for f in files if f["ext"] == ".md"],
        "top_20_largest": sorted(files, key=lambda x: -x["size_kb"])[:20],
    }


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 60)
    print("B166ER 全盘知识文件扫描 V2.0")
    print("=" * 60)
    t0 = time.time()
    all_files = scan_all()

    inv_path = WORKSPACE / "memory" / "file_inventory.json"
    with open(inv_path, "w", encoding="utf-8") as f:
        json.dump(all_files, f, ensure_ascii=False, indent=2)

    report = generate_report(all_files)
    report["scanned_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report["elapsed_sec"] = round(time.time() - t0, 1)
    report_path = WORKSPACE / "memory" / "file_scan_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("扫描报告")
    print("=" * 60)
    print(f"总文件数: {report['total']}   总大小: {report['total_size_mb']} MB   耗时: {report['elapsed_sec']}s")
    print("\n按类型:")
    for ext, n in report["by_ext"].items():
        print(f"  {ext}: {n}")
    print(f"\n.md 文件: {len(report['md_files'])}")
    print("\nTop 目录:")
    for d, n in list(report["by_top_dir"].items())[:15]:
        print(f"  {d}: {n}")
    print("\n最大文件 Top 10:")
    for f in report["top_20_largest"][:10]:
        print(f"  [{f['size_kb']}KB] {f['rel']}")
    print(f"\n清单: {inv_path}")
    print(f"报告: {report_path}")
