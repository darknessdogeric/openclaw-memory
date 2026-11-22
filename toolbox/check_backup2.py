import os
import shutil

backup = r'D:\B166ER-Backup\weekly\2026-09-27'
ws_dir = os.path.join(backup, 'workspace')
nested = os.path.join(ws_dir, 'workspace')
obsidian_in_ws = os.path.join(ws_dir, 'obsidian-vault')

print('Top backup contents:', os.listdir(backup))
print()

# Just count files in each, no full size walk
def safe_count(d):
    cnt = 0
    sz = 0
    err = 0
    for r, dns, fs in os.walk(d):
        for f in fs:
            try:
                p = os.path.join(r, f)
                sz += os.path.getsize(p)
                cnt += 1
            except (OSError, FileNotFoundError):
                err += 1
    return cnt, sz, err

print('Nested workspace exists:', os.path.exists(nested))
if os.path.exists(nested):
    cnt, sz, err = safe_count(nested)
    print('Nested: %d files, %.2f GB, %d errors' % (cnt, sz/1024**3, err))
print()
print('obsidian-vault inside workspace exists:', os.path.exists(obsidian_in_ws))
if os.path.exists(obsidian_in_ws):
    cnt, sz, err = safe_count(obsidian_in_ws)
    print('obsidian-vault: %d files, %.2f GB, %d errors' % (cnt, sz/1024**3, err))
print()
# Top-level only, exclude nested
def safe_count_no_nested(d, excluded):
    cnt = 0
    sz = 0
    for r, dns, fs in os.walk(d):
        if r.startswith(excluded):
            continue
        for f in fs:
            try:
                p = os.path.join(r, f)
                sz += os.path.getsize(p)
                cnt += 1
            except OSError:
                pass
    return cnt, sz

cnt, sz = safe_count_no_nested(ws_dir, nested)
print('Top-level backup (excl nested): %d files, %.2f GB' % (cnt, sz/1024**3))

# Now check the source for comparison
src = r'D:\B166ER-OpenClaw\workspace'
src_cnt, src_sz = safe_count_no_nested(src, '')
print('Source workspace: %d files, %.2f GB' % (src_cnt, src_sz/1024**3))

# Show top-level dirs only
print()
print('Top-level dirs in backup workspace:')
for n in sorted(os.listdir(ws_dir)):
    p = os.path.join(ws_dir, n)
    if os.path.isdir(p):
        try:
            sub_sz = sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(p) for f in fs if os.path.exists(os.path.join(r,f)))
            print('  %s: %.2f GB' % (n, sub_sz/1024**3))
        except Exception:
            print('  %s: (error)' % n)
