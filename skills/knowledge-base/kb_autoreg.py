# -*- coding: utf-8 -*-
"""
kb_autoreg.py - 知识库自动注册与增量索引
功能：
1. 监控知识库目录变化（新增/修改）
2. 增量注册到OpenViking
3. 速率限制管理（Jina免费版100请求/分钟）
4. 文件hash追踪，避免重复索引
"""

import os
import json
import time
import hashlib
from pathlib import Path

# ============ 配置 ============
KB_DIR = Path("C:/Users/ericz/.openclaw/workspace/memory")
OV_INDEX_FILE = Path("C:/Users/ericz/.openclaw/workspace/.kb_index_manifest.json")
RATE_LIMIT = 80  # 保险阈值，每分钟最多80请求
RATE_WINDOW = 60  # 滑动窗口（秒）

# ============ 索引清单管理 ============

def load_manifest():
    """加载索引清单（记录每个文件的hash和索引状态）"""
    if OV_INDEX_FILE.exists():
        with open(OV_INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"files": {}, "last_full_scan": None}

def save_manifest(manifest):
    """保存索引清单"""
    with open(OV_INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

def compute_file_hash(filepath):
    """计算文件的MD5 hash"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return hashlib.md5(f.read().encode('utf-8')).hexdigest()

# ============ 增量扫描 ============

def scan_kb_directory():
    """
    扫描KB目录，返回需要更新的文件列表
    返回: {"added": [], "modified": [], "deleted": []}
    """
    manifest = load_manifest()
    current_files = {}
    changes = {"added": [], "modified": [], "deleted": []}
    
    # 遍历KB目录
    if not KB_DIR.exists():
        return changes
    
    for filepath in KB_DIR.rglob("*.md"):
        rel_path = str(filepath.relative_to(KB_DIR))
        current_files[rel_path] = True
        
        if rel_path not in manifest["files"]:
            # 新文件
            changes["added"].append(filepath)
        else:
            # 已存在，检查是否修改
            current_hash = compute_file_hash(filepath)
            if current_hash != manifest["files"][rel_path].get("hash"):
                changes["modified"].append(filepath)
    
    # 检测删除的文件
    for rel_path in manifest["files"]:
        if rel_path not in current_files:
            changes["deleted"].append(rel_path)
    
    return changes

# ============ OpenViking 增量注册 ============

def register_to_openviking(filepath):
    """
    将单个文件注册到OpenViking（带速率限制）
    """
    import subprocess
    
    # 检查速率
    if not check_rate_limit():
        print(f"  [rate-limit] 等待速率窗口...")
        time.sleep(RATE_WINDOW)
    
    # 执行ov add-resource
    result = subprocess.run(
        ["ov", "add-resource", str(filepath)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"  [ok] {filepath.name}")
        return True
    else:
        print(f"  [fail] {filepath.name}: {result.stderr[:100]}")
        return False

def check_rate_limit():
    """简单速率检查（记录上次请求时间）"""
    lock_file = Path("C:/Users/ericz/.openclaw/workspace/.kb_rate_lock")
    now = time.time()
    
    if lock_file.exists():
        with open(lock_file, 'r') as f:
            last_times = json.load(f)
    else:
        last_times = []
    
    # 清理超过窗口的记录
    last_times = [t for t in last_times if now - t < RATE_WINDOW]
    
    if len(last_times) >= RATE_LIMIT:
        return False
    
    last_times.append(now)
    with open(lock_file, 'w') as f:
        json.dump(last_times, f)
    
    return True

# ============ 增量同步主流程 ============

def run_incremental_sync():
    """
    增量同步主流程
    1. 扫描变化
    2. 更新manifest
    3. 增量注册到OpenViking
    """
    print(f"[kb_autoreg] 开始增量扫描: {KB_DIR}")
    
    manifest = load_manifest()
    changes = scan_kb_directory()
    
    print(f"  新增: {len(changes['added'])} 个")
    print(f"  修改: {len(changes['modified'])} 个")
    print(f"  删除: {len(changes['deleted'])} 个")
    
    if not any(changes.values()):
        print("  [ok] 无变化，跳过")
        return
    
    # 处理新增文件
    for filepath in changes["added"]:
        if register_to_openviking(filepath):
            rel_path = str(filepath.relative_to(KB_DIR))
            manifest["files"][rel_path] = {
                "hash": compute_file_hash(filepath),
                "indexed": True,
                "added_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    # 处理修改文件
    for filepath in changes["modified"]:
        # 删除旧索引（通过ov rm）
        rel_path = str(filepath.relative_to(KB_DIR))
        old_entry = manifest["files"].get(rel_path, {})
        
        # 重新注册
        if register_to_openviking(filepath):
            manifest["files"][rel_path] = {
                "hash": compute_file_hash(filepath),
                "indexed": True,
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    # 处理删除文件
    for rel_path in changes["deleted"]:
        # 从manifest移除
        if rel_path in manifest["files"]:
            del manifest["files"][rel_path]
            print(f"  [del] {rel_path}")
    
    # 更新全量扫描时间
    manifest["last_full_scan"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save_manifest(manifest)
    
    print(f"[kb_autoreg] 完成")

# ============ 全量重建 ============

def run_full_reindex():
    """
    全量重建索引（谨慎使用，会消耗大量API配额）
    """
    print(f"[kb_autoreg] 开始全量重建索引...")
    
    manifest = {"files": {}, "last_full_scan": time.strftime("%Y-%m-%d %H:%M:%S")}
    total = 0
    
    for filepath in KB_DIR.rglob("*.md"):
        if register_to_openviking(filepath):
            rel_path = str(filepath.relative_to(KB_DIR))
            manifest["files"][rel_path] = {
                "hash": compute_file_hash(filepath),
                "indexed": True,
                "indexed_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            total += 1
            print(f"  [{total}] {rel_path}")
    
    save_manifest(manifest)
    print(f"[kb_autoreg] 全量重建完成: {total} 个文件")

# ============ 状态检查 ============

def show_status():
    """显示索引状态"""
    manifest = load_manifest()
    print(f"索引清单: {len(manifest['files'])} 个文件")
    print(f"最后全量扫描: {manifest.get('last_full_scan', '从未')}")
    
    # 统计状态
    indexed = sum(1 for f in manifest["files"].values() if f.get("indexed"))
    print(f"已索引: {indexed}")
    
    # 检查文件变化
    changes = scan_kb_directory()
    if any(changes.values()):
        print(f"\n待处理变化:")
        print(f"  新增: {len(changes['added'])}")
        print(f"  修改: {len(changes['modified'])}")
        print(f"  删除: {len(changes['deleted'])}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python kb_autoreg.py [sync|reindex|status]")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "sync":
        run_incremental_sync()
    elif cmd == "reindex":
        run_full_reindex()
    elif cmd == "status":
        show_status()
    else:
        print(f"未知命令: {cmd}")
