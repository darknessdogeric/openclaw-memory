"""Check tail of HEARTBEAT.md safely."""
import sys

path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
try:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    print(f'Total lines: {len(lines)}')
    print('=== Last 5 ===')
    for i, ln in enumerate(lines[-5:], start=len(lines) - 5):
        print(f'[{i}] {ln.rstrip()}')
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)