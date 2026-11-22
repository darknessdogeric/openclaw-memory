"""Verify AI agent config dirs unchanged + final summary."""
import os, json, hashlib

# Re-read baseline and compare
home = os.path.expanduser("~")
agent_dirs = [
    os.path.join(home, ".claude"),
    os.path.join(home, ".cursor"),
    os.path.join(home, ".copilot"),
]

with open(r'D:\B166ER-OpenClaw\workspace\toolbox\officecli_stage1\baseline.json', 'r', encoding='utf-8') as f:
    baseline_raw = json.load(f)

# baseline_raw has keys as paths and values as lists of [path, size, mtime]
baseline = {}
for k, v in baseline_raw.items():
    baseline[k] = [tuple(item) for item in v]

current = {}
for d in agent_dirs:
    if not os.path.exists(d):
        continue
    files = []
    for root, dirs, fnames in os.walk(d):
        for fn in fnames:
            full = os.path.join(root, fn)
            try:
                files.append((full, os.path.getsize(full), os.path.getmtime(full)))
            except OSError:
                pass
    current[d] = files
    print(f'Scanned {d}: {len(files)} files', flush=True)

print("=== Comparing AI agent configs ===")
for d, base_files in baseline.items():
    curr_files = current.get(d, [])
    base_set = set(base_files)
    curr_set = set(curr_files)

    added = curr_set - base_set
    removed = base_set - curr_set

    # Check size changes for files in both
    size_changes = []
    base_dict = {p: (s, t) for (p, s, t) in base_files}
    curr_dict = {p: (s, t) for (p, s, t) in curr_files}
    for p in (set(base_dict) & set(curr_dict)):
        bs, bt = base_dict[p]
        cs, ct = curr_dict[p]
        if bs != cs:
            size_changes.append((p, bs, cs))

    print(f"\n{d}:")
    print(f"  Baseline files: {len(base_files)}")
    print(f"  Current files: {len(curr_files)}")
    print(f"  Added: {len(added)}")
    if added:
        for p, s, t in list(added)[:5]:
            print(f"    + {p} ({s}b)")
    print(f"  Removed: {len(removed)}")
    if removed:
        for p, s, t in list(removed)[:5]:
            print(f"    - {p}")
    print(f"  Size-changed: {len(size_changes)}")
    if size_changes:
        for p, bs, cs in size_changes[:5]:
            print(f"    * {p}: {bs} -> {cs}")

print()
print("=== Final verdict on auto-inject ===")
all_clean = True
for d in agent_dirs:
    if d in baseline and d in current:
        base_n = len(baseline[d])
        curr_n = len(current[d])
        if base_n != curr_n:
            print(f"  {d}: FILE COUNT CHANGED {base_n} -> {curr_n}")
            all_clean = False
        else:
            print(f"  {d}: OK ({base_n} files)")

if all_clean:
    print("\nVERDICT: No auto-injection contamination.")
else:
    print("\nVERDICT: Possible contamination. Investigate.")

# Save current as new baseline
with open(r'D:\B166ER-OpenClaw\workspace\toolbox\officecli_stage1\baseline_after.json', 'w', encoding='utf-8') as f:
    json.dump({k: [(p, s, t) for (p, s, t) in v] for k, v in current.items()}, f, ensure_ascii=False, indent=2)
