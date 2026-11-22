# -*- coding: utf-8 -*-
"""纯 Python 提取 Word 97-2003 (.doc) 正文：FIB -> Clx -> piece table"""
import io, sys, os, re, struct, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import olefile

SRC = glob.glob(r'C:\Users\ericz\Desktop\产业发展部\重要文件\重要项目情况\*.doc')[0]
OUT = r'D:\B166ER-openclaw\workspace\tmp\_proj_txt\gulu.txt'
print('源文件: %s  %.1f MB' % (os.path.basename(SRC), os.path.getsize(SRC) / 1024 / 1024))

ole = olefile.OleFileIO(SRC)
print('OLE 流:', [ '/'.join(s) for s in ole.listdir() ][:14])

wd = ole.openstream('WordDocument').read()
print('WordDocument 流 %.2f MB' % (len(wd) / 1024 / 1024))

wIdent, nFib = struct.unpack_from('<HH', wd, 0)
flags = struct.unpack_from('<H', wd, 0x0A)[0]
which = (flags >> 9) & 1
tbl_name = '1Table' if which else '0Table'
print('wIdent=0x%04X nFib=%d flags=0x%04X -> 表流=%s' % (wIdent, nFib, flags, tbl_name))

if not ole.exists(tbl_name):
    tbl_name = '0Table' if ole.exists('0Table') else '1Table'
    print('回退表流: %s' % tbl_name)
tbl = ole.openstream(tbl_name).read()

fcMin, fcMac = struct.unpack_from('<II', wd, 0x18)
fcClx, lcbClx = struct.unpack_from('<II', wd, 0x01A2)
print('fcMin=%d fcMac=%d fcClx=%d lcbClx=%d 表流长=%d' % (fcMin, fcMac, fcClx, lcbClx, len(tbl)))

text = []
if lcbClx == 0:
    raw = wd[fcMin:fcMac]
    text.append(raw.decode('utf-16-le', 'replace'))
else:
    clx = tbl[fcClx:fcClx + lcbClx]
    pos = 0
    while pos < len(clx):
        t = clx[pos]
        if t == 0x01:
            cb = struct.unpack_from('<I', clx, pos + 1)[0]
            pos += 5 + cb
            continue
        if t == 0x02:
            lcb = struct.unpack_from('<I', clx, pos + 1)[0]
            plc = clx[pos + 5: pos + 5 + lcb]
            n = (lcb - 4) // 12
            cps = list(struct.unpack_from('<%dI' % (n + 1), plc, 0))
            base = 4 * (n + 1)
            for i in range(n):
                off = base + i * 8
                fc = struct.unpack_from('<I', plc, off + 2)[0]
                cp_start, cp_end = cps[i], cps[i + 1]
                ncp = cp_end - cp_start
                if ncp <= 0:
                    continue
                if fc & 0x40000000:
                    real = (fc & 0x3FFFFFFF) // 2
                    text.append(wd[real: real + ncp].decode('cp1252', 'replace'))
                else:
                    real = fc & 0x3FFFFFFF
                    text.append(wd[real: real + ncp * 2].decode('utf-16-le', 'replace'))
            break
        break

s = ''.join(text)
print('原始字符数 %d' % len(s))
# 清理 Word 控制字符
s = s.replace('\r', '\n').replace('\x07', '\t').replace('\x0b', '\n')
s = re.sub(r'\x13[^\x14\x15]*[\x14\x15]', '', s)
s = re.sub(r'[\x00-\x0f]', '', s)
s = re.sub(r'[\x00-\x08\x0e-\x1f]', '', s)
s = re.sub(r'\n{3,}', '\n\n', s)
open(OUT, 'w', encoding='utf-8').write(s)
print('清洗后 %d 字符 -> %s' % (len(s), OUT))
print('=' * 90)
print(s[:7000])
