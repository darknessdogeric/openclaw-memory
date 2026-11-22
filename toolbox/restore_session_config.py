#!/usr/bin/env python3
"""
restore_session_config.py - 从快照恢复 OpenClaw 侧边栏配置
========================================================

R292 触发: OpenClaw 升级后 / gateway 重启后

用法:
    python toolbox/restore_session_config.py --snapshot PATH
    python toolbox/restore_session_config.py --latest

注意: 这是模板/文档脚本。实际恢复操作由 B166ER 在 turn 中执行:
  1. 读取快照 JSON
  2. 调用 sessions group_set 重设分组
  3. 调用 sessions action=patch 重设每个 session 的 label/icon/color/group/pinned

R66 v3.0 (2026-09-03) 验证: 已通过禁词扫描
R292 关联: 升级后恢复
"""
from __future__ import annotations
import sys
import io
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
MEMORY_DIR = WORKSPACE / "memory"

# Force UTF-8 stdout/stderr (Windows GBK codepage fix)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def find_latest_snapshot() -> Path | None:
    if not MEMORY_DIR.exists():
        return None
    snapshots = sorted(MEMORY_DIR.glob("session-config-snapshot-*.json"), reverse=True)
    return snapshots[0] if snapshots else None


def main():
    parser = argparse.ArgumentParser(description="Restore session/sidebar config from snapshot")
    parser.add_argument("--snapshot", default=None, help="Path to snapshot JSON")
    parser.add_argument("--latest", action="store_true", help="Use latest snapshot")
    args = parser.parse_args()

    if args.latest:
        snap_path = find_latest_snapshot()
        if not snap_path:
            print("[restore_session_config] No snapshot found in memory/", file=sys.stderr)
            return 1
    elif args.snapshot:
        snap_path = Path(args.snapshot)
    else:
        print("[restore_session_config] Specify --snapshot PATH or --latest", file=sys.stderr)
        return 1

    if not snap_path.exists():
        print(f"[restore_session_config] Snapshot not found: {snap_path}", file=sys.stderr)
        return 1

    with open(snap_path, encoding="utf-8") as f:
        snapshot = json.load(f)

    print(f"[restore_session_config] Loaded snapshot: {snap_path}")
    print(f"  timestamp: {snapshot.get('timestamp', 'N/A')}")
    print(f"  groups: {len(snapshot.get('groups', []))}")
    print(f"  sessions: {len(snapshot.get('sessions', []))}")
    print()
    print("Next steps (B166ER turn):")
    print("  1. sessions group_set names=[...]")
    print("  2. sessions action=patch sessionKey=... label/group/icon/color/pinned")
    return 0


if __name__ == "__main__":
    sys.exit(main())