#!/usr/bin/env python3
"""
token_guard.py - 上下文使用量守护
================================

用法:
    python toolbox/token_guard.py --context "61k/1.0m"
    python toolbox/token_guard.py --context 61500 --max 1000000
    python toolbox/token_guard.py --json --context "61k/1.0m"

阈值:
    < 65%     → OK      (no action)
    >= 65%    → WARN    (avoid long output)
    >= 78%    → DANGER  (suggest /compact)
    >= 88%    → CRITICAL(strongly suggest /compact)

输出 JSON:
{
  "context_used": "61k",
  "context_max": "1.0m",
  "ratio": 0.061,
  "level": "OK",
  "action": "none" | "warn" | "suggest_compact" | "strong_compact"
}

R291 关联: 上下文管理标准
"""
from __future__ import annotations
import sys
import io
import os

# Force UTF-8 stdout/stderr (Windows GBK codepage fix)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import argparse
import re
import json


THRESHOLDS = {
    "warn": 0.65,
    "danger": 0.78,
    "critical": 0.88,
}

def parse_context(ctx_str: str) -> tuple[int, int]:
    """Parse '61k/1.0m' → (61000, 1000000). Supports k/m suffix."""
    if "/" not in ctx_str:
        raise ValueError(f"context must be 'used/max' format: {ctx_str}")
    used_str, max_str = ctx_str.split("/", 1)

    def to_num(s: str) -> int:
        s = s.strip().lower()
        m = re.match(r"^([\d.]+)\s*([km]?)$", s)
        if not m:
            raise ValueError(f"Invalid number: {s}")
        num = float(m.group(1))
        suffix = m.group(2)
        if suffix == "k":
            return int(num * 1000)
        elif suffix == "m":
            return int(num * 1_000_000)
        return int(num)

    return to_num(used_str), to_num(max_str)


def determine_level(ratio: float) -> tuple[str, str]:
    """Return (level, action) based on ratio"""
    if ratio >= THRESHOLDS["critical"]:
        return "CRITICAL", "strong_compact"
    elif ratio >= THRESHOLDS["danger"]:
        return "DANGER", "suggest_compact"
    elif ratio >= THRESHOLDS["warn"]:
        return "WARN", "warn"
    else:
        return "OK", "none"


def main():
    parser = argparse.ArgumentParser(description="Token usage guard")
    parser.add_argument("--context", required=True, help="Context as 'used/max' (e.g. 61k/1.0m)")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    args = parser.parse_args()

    try:
        used, max_val = parse_context(args.context)
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

    ratio = used / max_val if max_val > 0 else 0
    level, action = determine_level(ratio)

    result = {
        "context_used": used,
        "context_max": max_val,
        "ratio": round(ratio, 4),
        "level": level,
        "action": action,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return 0

    # Human-readable output
    pct = ratio * 100
    print(f"Token Guard · {args.context}")
    print(f"  used: {used:,} / max: {max_val:,}")
    print(f"  ratio: {pct:.1f}%")
    print(f"  level: {level}")
    print(f"  action: {action}")
    if action == "strong_compact":
        print("  [!!] 强烈建议执行 /compact")
    elif action == "suggest_compact":
        print("  [i] 建议执行 /compact")
    elif action == "warn":
        print("  [*] 警告:避免长输出")
    return 0


if __name__ == "__main__":
    sys.exit(main())