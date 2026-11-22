# -*- coding: utf-8 -*-
import io, os, glob


def _is_sep(line):
    s = line.strip().replace('|', '').replace(' ', '').replace(chr(9), '')
    return len(s) > 0 and set(s) <= set('-:')


def check(ROOT, DESK=None):
    bad = []
    mdir = os.path.join(ROOT, 'output', 'nm_20261120')
    if os.path.isdir(mdir):
        for md in sorted(glob.glob(os.path.join(mdir, '*.md'))):
            L = io.open(md, encoding='utf-8', errors='replace').read().split(chr(10))
            i = 0
            while i < len(L):
                st = L[i].strip()
                if st.startswith('|') and st.endswith('|'):
                    j = i
                    while j < len(L) and L[j].strip().startswith('|') and L[j].strip().endswith('|'):
                        j += 1
                    blk = L[i:j]
                    nm = os.path.basename(md)
                    if len(blk) < 2 or not _is_sep(blk[1]):
                        bad.append(nm + ' L' + str(i + 1) + ' 缺表头分隔行')
                    stray = sum(1 for b in blk[2:] if _is_sep(b))
                    if stray:
                        bad.append(nm + ' L' + str(i + 1) + ' 有 ' + str(stray) + ' 行游离分隔行')
                    i = j
                else:
                    i += 1
    if DESK and os.path.isdir(DESK):
        try:
            import docx
        except Exception:
            docx = None
        if docx is not None:
            for fn in sorted(os.listdir(DESK)):
                if not fn.endswith('.docx'):
                    continue
                try:
                    dd = docx.Document(os.path.join(DESK, fn))
                except Exception:
                    continue
                for tb in dd.tables:
                    for r in tb.rows:
                        joined = ' | '.join(c.text for c in r.cells)
                        if joined.strip() and _is_sep(joined):
                            bad.append(fn + ' 有可见分隔行')
    if bad:
        return False, ('表格结构缺陷 ' + str(len(bad)) + ' 项: ' + '; '.join(bad[:4])), bad[:6]
    return True, 'md 表格块结构正常 | docx 无可见分隔行', []
