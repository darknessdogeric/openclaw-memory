"""Snapshot baseline of AI agent config dirs to ensure no contamination."""
import os

home = os.path.expanduser("~")
print(f"Home: {home}")
print()

agent_dirs = [
    os.path.join(home, ".claude"),
    os.path.join(home, ".cursor"),
    os.path.join(home, ".windsurf"),
    os.path.join(home, ".copilot"),
    os.path.join(home, ".config", "Claude"),
    os.path.join(home, ".config", "opencode"),
    "C:\\Program Files\\Claude",
    "C:\\Program Files\\Cursor",
]

baseline = {}
for d in agent_dirs:
    exists = os.path.exists(d)
    print(f"CHECK: {d} = {'EXISTS' if exists else 'missing'}")
    if exists:
        # List files
        files = []
        for root, dirs, fnames in os.walk(d):
            for fn in fnames:
                full = os.path.join(root, fn)
                files.append((full, os.path.getsize(full), os.path.getmtime(full)))
        baseline[d] = files
        print(f"  Files: {len(files)}")
        for f, sz, mt in files[:10]:
            print(f"    {os.path.relpath(f, d)}: {sz}b, mtime={mt}")
        if len(files) > 10:
            print(f"    ... and {len(files) - 10} more")

import json
with open(r"D:\B166ER-OpenClaw\workspace\toolbox\officecli_stage1\baseline.json", 'w', encoding='utf-8') as f:
    json.dump({k: [(p, s, t) for (p, s, t) in v] for k, v in baseline.items()}, f, ensure_ascii=False, indent=2)
print()
print("Baseline saved to baseline.json")
