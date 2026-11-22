# -*- coding: utf-8 -*-
"""会话改名后，同步更新 KB 索引与今日 memory 中的旧名引用（UTF-8 显式，原子写）"""
import io, os, sys, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OLD = '安逸集团相关'
NEW = '安逸集团事务'

TARGETS = [
    r'D:\B166ER-openclaw\workspace\anyi-ops-kb\00_安逸集团知识库总览\安逸事务线_会话恢复索引_2026-10-29.md',
    r'D:\B166ER-openclaw\workspace\memory\2026-10-29.md',
]

for path in TARGETS:
    if not os.path.exists(path):
        print('SKIP (not found): %s' % path)
        continue
    with open(path, 'rb') as f:
        raw = f.read()
    enc = 'utf-8'
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        enc = 'gbk'
        text = raw.decode('gbk')

    n = text.count(OLD)
    if n == 0:
        print('NO-OP  %s  (无旧名引用)  enc=%s' % (os.path.basename(path), enc))
        continue

    shutil.copy2(path, path + '.bak-rename-20261029')
    new_text = text.replace(OLD, NEW)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding=enc, newline='') as f:
        f.write(new_text)
    os.replace(tmp, path)

    with open(path, 'rb') as f:
        chk = f.read()
    chk.decode(enc)  # 编码自检
    assert OLD not in chk.decode(enc), '仍有旧名残留: %s' % path
    print('OK  %s  替换 %d 处  enc=%s  %d -> %d bytes' % (
        os.path.basename(path), n, enc, len(raw), os.path.getsize(path)))
