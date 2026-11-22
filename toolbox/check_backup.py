import os

backup = r'D:\B166ER-Backup\weekly\2026-09-27'
ws_dir = os.path.join(backup, 'workspace')
nested = os.path.join(ws_dir, 'workspace')
obsidian_in_ws = os.path.join(ws_dir, 'obsidian-vault')

print('Top backup contents:', os.listdir(backup))
print()
print('Nested workspace exists:', os.path.exists(nested))
if os.path.exists(nested):
    nested_size = sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(nested) for f in fs)
    print('Nested workspace size: %.2f GB' % (nested_size / 1024**3))
print()
print('obsidian-vault inside workspace exists:', os.path.exists(obsidian_in_ws))
if os.path.exists(obsidian_in_ws):
    ov_size = sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(obsidian_in_ws) for f in fs)
    print('obsidian-vault inside workspace size: %.2f GB' % (ov_size / 1024**3))
print()
top_size = sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(ws_dir) for f in fs if not r.startswith(nested))
print('Top-level backup size (excluding nested): %.2f GB' % (top_size / 1024**3))
