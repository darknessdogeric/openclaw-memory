# -*- coding: utf-8 -*-
"""修正版：补提取剩余 6 份 .doc / .xls（原脚本 ole.listdir 判断有 bug）"""
import io, os, sys, re, json, traceback
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import olefile

SRC = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\第一批次文件"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\batch1_extra"
os.makedirs(OUT, exist_ok=True)


def stream_names(path):
    o = olefile.OleFileIO(path)
    return o, {"/".join(x) for x in o.listdir()}


def doc_text(path):
    """WordDocument 流：FIB -> fcMin/ccpText 提取正文；失败则全流启发式"""
    o, names = stream_names(path)
    if "WordDocument" not in names:
        o.close()
        return None, "no-WordDocument"
    data = o.openstream("WordDocument").read()
    o.close()
    best = ""
    # 方案A：FIB 解析 fcMin/fcMac（Word 97+）
    try:
        fcClx = int.from_bytes(data[0x01A2:0x01A6], "little")
        lcbClx = int.from_bytes(data[0x01A6:0x01AA], "little")
        ccpText = int.from_bytes(data[0x004C:0x0050], "little")
        if fcClx and lcbClx and fcClx + lcbClx <= len(data):
            clx = data[fcClx:fcClx + lcbClx]
            i = 0
            while i < len(clx):
                t = clx[i]
                if t == 1:
                    cb = clx[i + 1]
                    i += 2 + cb
                elif t == 2:
                    cb = int.from_bytes(clx[i + 1:i + 3], "little")
                    i += 3 + cb
                else:
                    i += 1
                    continue
                fc = int.from_bytes(clx[i:i + 4], "little")
                i += 4
                txt = data[fc:fc + ccpText * 2]
                s = txt.decode("utf-16-le", errors="ignore")
                s = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", s)
                s = re.sub(r"\r", "\n", s)
                if len(s) > len(best):
                    best = s
    except Exception:
        pass
    if len(best) < 30:
        # 方案B：全流扫描可打印片段
        out = []
        buf = []
        for i in range(0, len(data) - 1, 2):
            ch = data[i] | (data[i + 1] << 8)
            if ch in (0x0D, 0x07, 0x0B, 0x03):
                if buf:
                    out.append("".join(buf)); buf = []
                out.append("")
            elif 0x20 <= ch < 0x7F or 0x4E00 <= ch <= 0x9FFF or 0x3000 <= ch <= 0x303F or 0xFF00 <= ch <= 0xFFEF:
                buf.append(chr(ch))
            else:
                if buf:
                    out.append("".join(buf)); buf = []
        cand = "\n".join(x for x in out if x.strip())
        if len(cand) > len(best):
            best = cand
    if len(best) < 20:
        return None, "empty"
    return best, "ole-worddoc"


def xls_text(path):
    import xlrd
    errs = []
    for kw in ({}, {"formatting_info": True}, {"on_demand": True}, {"ignore_workbook_corruption": True}):
        try:
            bk = xlrd.open_workbook(path, **kw)
            rows = []
            for sh in bk.sheets():
                rows.append(f"--- SHEET: {sh.name} ({sh.nrows}x{sh.ncols}) ---")
                for r in range(min(sh.nrows, 500)):
                    vals = []
                    for c in range(min(sh.ncols, 50)):
                        try:
                            v = sh.cell_value(r, c)
                        except Exception:
                            v = ""
                        if isinstance(v, float) and v == int(v):
                            v = int(v)
                        vals.append(str(v).strip())
                    if any(vals):
                        rows.append(" | ".join(vals).rstrip(" |"))
            return "\n".join(rows), f"xlrd{kw if kw else ''}"
        except Exception as e:
            errs.append(f"{kw}: {e}")
    # 兜底：pandas
    try:
        import pandas as pd
        dfs = pd.read_excel(path, sheet_name=None, header=None)
        rows = []
        for name, df in dfs.items():
            rows.append(f"--- SHEET: {name} ---")
            for _, row in df.iterrows():
                vals = [str(v).strip() for v in row.tolist()]
                if any(vals):
                    rows.append(" | ".join(vals).rstrip(" |"))
        return "\n".join(rows), "pandas"
    except Exception as e:
        errs.append(f"pandas: {e}")
    return None, " | ".join(errs)[-300:]


targets = []
for root, dirs, files in os.walk(SRC):
    for f in files:
        p = os.path.join(root, f)
        rel = os.path.relpath(p, SRC)
        if rel.endswith(".doc") or "2025年12月份利润表" in rel:
            targets.append(p)

rep = []
for p in sorted(targets):
    rel = os.path.relpath(p, SRC)
    if rel.endswith(".doc"):
        txt, how = doc_text(p)
    else:
        txt, how = xls_text(p)
    safe = re.sub(r'[\\/:*?"<>|]+', "_", rel)
    if txt:
        with open(os.path.join(OUT, safe + ".txt"), "w", encoding="utf-8") as f:
            f.write(f"# 源文件: {rel}\n# 提取方式: {how}\n\n")
            f.write(txt)
    rep.append((rel, how, len(txt) if txt else 0))

print(f"=== 补提取 {len(rep)} 份 ===")
for rel, how, n in rep:
    print(f"  [{'OK ' if n else 'FAIL'}] {n:>7} 字符 | {rel}")
    if not n:
        print(f"          -> {how[:260]}")
