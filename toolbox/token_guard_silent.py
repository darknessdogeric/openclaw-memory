#!/usr/bin/env python3
"""
Token Guard v3 Silent - 后台静默版
不输出到 dashboard，只写日志文件
"""
import sys
import os
import re
import json
import argparse
from datetime import datetime

LOG_FILE = r'D:\B166ER-OpenClaw\workspace\toolbox\.tmp\token_guard.log'

THRESHOLDS = {
    'OK': 0.65,    # <65% 无操作
    'WARN': 0.78,  # 65-78% 警告
    'HIGH': 0.88,  # 78-88% 高度警告
    'CRITICAL': 1.0,  # >88% 危急
}

def parse_context(ctx):
    """Parse context string like '264k/1.0m' to bytes"""
    m = re.match(r'(\d+(?:\.\d+)?)([kKmM])/(\d+(?:\.\d+)?)([kKmM])', ctx)
    if not m:
        raise ValueError(f"Invalid context format: {ctx}")
    val = float(m.group(1))
    unit = m.group(2).lower()
    max_val = float(m.group(3))
    max_unit = m.group(4).lower()
    used = int(val * 1024) if unit == 'k' else int(val * 1024 * 1024)
    max_bytes = int(max_val * 1024) if max_unit == 'k' else int(max_val * 1024 * 1024)
    return used, max_bytes

def check(used, max_bytes):
    ratio = used / max_bytes
    if ratio < THRESHOLDS['OK']:
        level = 'OK'
        action = 'none'
    elif ratio < THRESHOLDS['WARN']:
        level = 'WARN'
        action = 'caution'
    elif ratio < THRESHOLDS['HIGH']:
        level = 'HIGH'
        action = 'compact'
    else:
        level = 'CRITICAL'
        action = 'urgent'
    return ratio, level, action

def log_result(used, max_bytes, ratio, level, action):
    """Write to log file, don't print to stdout"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"{timestamp} | used={used} max={max_bytes} ratio={ratio:.3f} level={level} action={action}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--context', required=True)
    parser.add_argument('--silent', action='store_true', default=True,
                        help='Silent mode (default: true, no stdout output)')
    parser.add_argument('--json', action='store_true',
                        help='Output JSON to stdout (overrides silent)')
    args = parser.parse_args()
    
    try:
        used, max_bytes = parse_context(args.context)
        ratio, level, action = check(used, max_bytes)
        log_result(used, max_bytes, ratio, level, action)
        
        if args.json:
            # Override silent only if --json is explicit
            result = {
                'context_used': used,
                'context_max': max_bytes,
                'ratio': round(ratio, 3),
                'level': level,
                'action': action
            }
            print(json.dumps(result, ensure_ascii=False))
        elif not args.silent:
            print(f"Token Guard v3 silent · {args.context}")
            print(f"  used: {used:,} / max: {max_bytes:,}")
            print(f"  ratio: {ratio:.1%}")
            print(f"  level: {level}")
            print(f"  action: {action}")
        # else: completely silent (no output)
    except Exception as e:
        if not args.silent:
            print(f"Token Guard error: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()