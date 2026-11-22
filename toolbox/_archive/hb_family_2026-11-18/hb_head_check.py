"""Check head of HEARTBEAT.md."""
path = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
try:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for i in range(5):
            ln = f.readline()
            print(f'[{i}] {ln!r}')
except Exception as e:
    print(f'ERROR: {e}')