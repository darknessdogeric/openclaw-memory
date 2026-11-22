# -*- coding: utf-8 -*-
"""fix_mixed_encoding.py - 修复 UTF-8 / GBK 混合编码文件（可复用）

用法:
    python toolbox/fix_mixed_encoding.py --dry <file> ...
    python toolbox/fix_mixed_encoding.py --apply <file> ...
原理：结构性切分 —— 以"连续合法 UTF-8 游程"为界切块，块间按 GB18030 逐字符安全解码。
      边界处半个多字节字符用 1/2/4 字节试探，失败则标 U+FFFD。
"""
import io, sys, os, re, glob, shutil, argparse, datetime

def u8run(raw, i, n):
    j = i
    while j < n:
        b = raw[j]
        if b < 0x80: j += 1; continue
        L = 2 if 0xC2 <= b <= 0xDF else (3 if 0xE0 <= b <= 0xEF else (4 if 0xF0 <= b <= 0xF4 else 0))
        if not L or j + L > n: break
        try: raw[j:j+L].decode("utf-8")
        except Exception: break
        j += L
    return j - i

def next_run(raw, s, minrun=12):
    n = len(raw); i = s
    while i < n:
        if u8run(raw, i, n) >= minrun: return i
        i += 1
    return n

def gbk_safe(b):
    out = []; i = 0; n = len(b)
    while i < n:
        if b[i] < 0x80:
            out.append(chr(b[i])); i += 1; continue
        done = False
        for L in (2, 4):
            if i + L > n: continue
            try:
                out.append(b[i:i+L].decode("gb18030")); i += L; done = True; break
            except Exception: pass
        if not done:
            out.append("\ufffd"); i += 1
    return "".join(out)

def repair(raw):
    blocks = []; p = 0; n = len(raw)
    while p < n:
        ue = n
        try: raw[p:].decode("utf-8")
        except UnicodeDecodeError as e: ue = p + e.start
        if ue > p:
            blocks.append(("u8", p, ue)); p = ue
            if p >= n: break
        ge = next_run(raw, p + 1)
        blocks.append(("gbk", p, ge)); p = ge
    parts = []
    for enc, s, e in blocks:
        seg = raw[s:e]
        parts.append(seg.decode("utf-8") if enc == "u8" else gbk_safe(seg))
    return "".join(parts), len(blocks)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", nargs="+")
    ap.add_argument("--apply", nargs="+")
    ap.add_argument("--backup-dir", default=None)
    a = ap.parse_args()
    for mode in ("dry", "apply"):
        for p in (getattr(a, mode) or []):
            if not os.path.exists(p):
                print("  MISSING", p); continue
            raw = open(p, "rb").read()
            try:
                before = raw.decode("utf-8").count("\ufffd")
            except UnicodeDecodeError:
                before = -1
            fixed, nblk = repair(raw)
            after = fixed.count("\ufffd")
            print("  %-5s U+FFFD %-5s -> %-5s  块 %-4d  %s" % (mode.upper(), before, after, nblk, os.path.basename(p)[:56]))
            if mode == "apply" and after < (before if before > 0 else 0):
                bd = a.backup_dir or (os.path.dirname(p) + "/.encbak")
                os.makedirs(bd, exist_ok=True)
                shutil.copy2(p, os.path.join(bd, os.path.basename(p) + "." + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".bak"))
                with open(p, "w", encoding="utf-8", newline="") as f:
                    f.write(fixed)
                print("        ✔ 已修复并备份")

if __name__ == "__main__":
    main()
