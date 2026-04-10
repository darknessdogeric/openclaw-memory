# -*- coding: utf-8 -*-
"""
B166ER 全盘知识文件扫描器 V1.0
扫描所有可纳入知识库的文件，建立完整清单
"""
import os
import json
from pathlib import Path
from datetime import datetime

# 扫描目标目录
SCAN_ROOTS = [
    Path.home() / "Desktop" / "张实项目总控",
    Path.home() / "Desktop" / "自我革命",
    Path.home() / "Desktop" / "项目资料",
    Path.home() / "Desktop" / "工作文档",
    Path.home() / "Desktop" / "个人资料",
    Path.home() / ".openclaw" / "workspace",
]

# 文件类型优先级
EXT_PRIORITY = {
    ".md": 1,      # 最高优先级 - 直接可读
    ".txt": 2,     # 直接可读
    ".json": 3,    # 结构化数据
    ".docx": 4,    # 需要转换
    ".pdf": 5,     # 需要转换
    ".pptx": 6,    # 需要转换
    ".xlsx": 7,    # 需要转换
    ".csv": 8,     # 结构化数据
}

# 排除目录
EXCLUDE_DIRS = {
    "node_modules", ".git", "__pycache__", "venv", ".venv",
    "备份", "归档", "archive", "temp", "tmp", ".cache"
}

def scan_directory(root_path, max_depth=5):
    """扫描目录，返回所有可索引文件"""
    results = []
    
    if not root_path.exists():
        return results
    
    for root, dirs, files in os.walk(root_path):
        # 排除目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        # 检查深度
        depth = root.replace(str(root_path), "").count(os.sep)
        if depth > max_depth:
            continue
        
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in EXT_PRIORITY:
                full_path = Path(root) / f
                try:
                    size = full_path.stat().st_size
                    mtime = datetime.fromtimestamp(full_path.stat().st_mtime).strftime("%Y-%m-%d")
                    
                    results.append({
                        "path": str(full_path),
                        "name": f,
                        "ext": ext,
                        "size_kb": round(size / 1024, 1),
                        "mtime": mtime,
                        "priority": EXT_PRIORITY.get(ext, 99)
                    })
                except:
                    pass
    
    return results

def scan_all():
    """扫描所有目标目录"""
    all_files = []
    
    for root in SCAN_ROOTS:
        print(f"扫描: {root.name}...")
        files = scan_directory(root)
        all_files.extend(files)
        print(f"  发现 {len(files)} 个可索引文件")
    
    # 按优先级和大小排序
    all_files.sort(key=lambda x: (x["priority"], -x["size_kb"]))
    
    return all_files

def save_inventory(files, output_path):
    """保存清单"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(files, f, ensure_ascii=False, indent=2)
    return len(files)

def generate_report(files):
    """生成扫描报告"""
    report = {
        "total": len(files),
        "by_ext": {},
        "by_priority": {},
        "total_size_mb": 0,
        "top_20_largest": [],
        "md_files": [],
    }
    
    for f in files:
        ext = f["ext"]
        report["by_ext"][ext] = report["by_ext"].get(ext, 0) + 1
        report["total_size_mb"] += f["size_kb"] / 1024
    
    # Top 20 largest
    by_size = sorted(files, key=lambda x: -x["size_kb"])[:20]
    report["top_20_largest"] = by_size
    
    # All .md files
    report["md_files"] = [f for f in files if f["ext"] == ".md"]
    
    report["total_size_mb"] = round(report["total_size_mb"], 1)
    
    return report

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    
    print("=" * 60)
    print("B166ER 全盘知识文件扫描")
    print("=" * 60)
    
    all_files = scan_all()
    
    # 保存清单
    inventory_path = Path.home() / ".openclaw" / "workspace" / "memory" / "file_inventory.json"
    count = save_inventory(all_files, inventory_path)
    print(f"\n✅ 清单已保存: {count} 个文件")
    
    # 生成报告
    report = generate_report(all_files)
    
    print("\n" + "=" * 60)
    print("扫描报告")
    print("=" * 60)
    print(f"总文件数: {report['total']}")
    print(f"总大小: {report['total_size_mb']} MB")
    print("\n按类型:")
    for ext, count in sorted(report["by_ext"].items(), key=lambda x: -x[1]):
        print(f"  {ext}: {count}个")
    
    print(f"\n.md文件 ({len(report['md_files'])}个):")
    for f in report["md_files"][:10]:
        print(f"  [{f['size_kb']}KB] {f['path']}")
    
    print(f"\n最大文件 Top 10:")
    for f in report["top_20_largest"][:10]:
        print(f"  [{f['size_kb']}KB] {f['name']}")
