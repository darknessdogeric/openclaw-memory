#!/usr/bin/env python
"""并发锁测试 - 验证 cron_to_obsidian.py 的 O_EXCL 原子锁"""
import subprocess, threading, time, os, sys

LOCK_FILE = r'D:\B166ER-OpenClaw\workspace\toolbox\.cron_obsidian.lock'
SCRIPT = r'D:\B166ER-OpenClaw\workspace\toolbox\cron_to_obsidian.py'
CONTENT_FILE = r'D:\B166ER-OpenClaw\workspace\toolbox\.lock_test_content.md'

# Clean state
if os.path.exists(LOCK_FILE):
    os.remove(LOCK_FILE)

results = []
results_lock = threading.Lock()

def run_task(name):
    try:
        r = subprocess.run(
            ['python', SCRIPT,
             '--task', f'concurrent-{name}',
             '--content-file', CONTENT_FILE,
             '--importance', 'high',
             '--summary', f'task {name}'],
            capture_output=True, text=True, timeout=30
        )
        with results_lock:
            results.append((name, r.returncode, r.stdout, r.stderr))
    except Exception as e:
        with results_lock:
            results.append((name, -1, '', str(e)))

threads = [threading.Thread(target=run_task, args=(i,)) for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print('=== Concurrent test results ===')
for name, rc, out, err in sorted(results):
    print(f'\n--- Task {name}: rc={rc} ---')
    if out.strip():
        print(f'  stdout: {out.strip()[:300]}')
    if err.strip():
        print(f'  stderr: {err.strip()[:200]}')

# Verify lock state
print('\n=== Lock state after all done ===')
if os.path.exists(LOCK_FILE):
    with open(LOCK_FILE, 'r') as f:
        pid = f.read().strip()
    print(f'Lock file exists with PID: {pid}')
else:
    print('Lock file cleaned up properly')