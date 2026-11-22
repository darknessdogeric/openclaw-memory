# -*- coding: utf-8 -*-
"""补提取第一批次中旧格式文件（.xls / .doc）—— 多策略降级。"""
import io, os, sys, re, json, traceback
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SRC = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\第一批次文件"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\batch1_extra"
os.makedirs(OUT, exist_ok=True)


def read_xls(path):
    """xlrd -> msoffcrypto(常见口令) -> 原始流兜底"""
    import xlrd
    try:
        bk = xlrd.open_workbook(path)
        rows = []
        for sh in bk.sheets():
            rows.append(f"--- SHEET: {sh.name} ({sh.nrows}x{sh.ncols}) ---")
            for r in range(min(sh.nrows, 400)):
                vals = []
                for c in range(min(sh.ncols, 40)):
                    try:
                        v = sh.cell_value(r, c)
                    except Exception:
                        v = ""
                    if isinstance(v, float) and v == int(v):
                        v = int(v)
                    vals.append(str(v).strip())
                if any(vals):
                    rows.append(" | ".join(vals).rstrip(" |"))
        return "\n".join(rows), "xlrd"
    except Exception as e:
        pass
    # msoffcrypto
    try:
        import msoffcrypto
        for pwd in ("", "VelvetSweatshop", "123", "111"):
            try:
                with open(path, "rb") as f:
                    of = msoffcrypto.OfficeFile(f)
                    of.load_key(password=pwd)
                    buf = io.BytesIO()
                    of.decrypt(buf)
                    bk = xlrd.open_workbook(file_contents=buf.getvalue())
                rows = []
                for sh in bk.sheets():
                    rows.append(f"--- SHEET: {sh.name} ({sh.nrows}x{sh.ncols}) ---")
                    for r in range(min(sh.nrows, 400)):
                        vals = []
                        for c in range(min(sh.ncols, 40)):
                            try:
                                v = sh.cell_value(r, c)
                            except Exception:
                                v = ""
                            if isinstance(v, float) and v == int(v):
                                v = int(v)
                            vals.append(str(v).strip())
                        if any(vals):
                            rows.append(" | ".join(vals).rstrip(" |"))
                return "\n".join(rows), f"msoffcrypto(pwd={pwd!r})"
            except Exception:
                continue
    except Exception:
        pass
    return None, "FAIL"


def read_doc(path):
    """旧 .doc：olefile 提取 WordDocument 流的可见文本（含 UTF-16LE 与 GBK 猜测）"""
    try:
        import olefile
        if not olefile.isOleFile(path):
            return None, "not-ole"
        ole = olefile.OleFileIO(path)
        if "WordDocument" not in ole.listdir():
            return None, "no-WordDocument"
        data = ole.openstream("WordDocument").read()
        # 1) 抽取可打印的 UTF-16LE 片段
        out = []
        i = 0
        buf = []
        while i + 1 < len(data):
            ch = data[i] | (data[i + 1] << 8)
            if ch == 0x0D or ch == 0x07 or ch == 0x0B:
                if buf:
                    out.append("".join(buf))
                    buf = []
                out.append("")
            elif 0x20 <= ch < 0x7F or 0x4E00 <= ch <= 0x9FFF or 0x3000 <= ch <= 0x303F or 0xFF00 <= ch <= 0xFFEF:
                buf.append(chr(ch))
            else:
                if buf:
                    out.append("".join(buf))
                    buf = []
            i += 2
        if buf:
            out.append("".join(buf))
        txt = "\n".join(x for x in out if x.strip())
        if len(txt) > 40:
            return txt, "olefile-utf16"
        # 2) 兜底：整流按 GBK 解
        raw = data.decode("gbk", errors="ignore")
        keep = "".join(c if (0x20 <= ord(c) < 0x7F or 0x4E00 <= ord(c) <= 0x9FFF or c in "\r\n\t") else "" for c in raw)
        keep = re.sub(r"\n{3,}", "\n\n", keep)
        if len(keep) > 40:
            return keep, "olefile-gbk"
        return None, "too-short"
    except Exception:
        return None, "FAIL"


targets = []
for root, dirs, files in os.walk(SRC):
    for f in files:
        p = os.path.join(root, f)
        if f.lower().endswith(".xls") or f.lower().endswith(".doc"):
            targets.append(p)

report = []
for p in sorted(targets):
    ext = os.path.splitext(p)[1].lower()
    rel = os.path.relpath(p, SRC)
    if ext == ".xls":
        txt, how = read_xls(p)
    else:
        txt, how = read_doc(p)
    safe = re.sub(r'[\\/:*?"<>|]+', "_", rel)
    if txt:
        with open(os.path.join(OUT, safe + ".txt"), "w", encoding="utf-8") as f:
            f.write(f"# 源文件: {rel}\n# 提取方式: {how}\n\n")
            f.write(txt)
    report.append({"rel": rel, "method": how, "chars": len(txt) if txt else 0})

print(f"目标 {len(targets)} 个\n")
ok = [r for r in report if r["chars"] > 0]
bad = [r for r in report if r["chars"] == 0]
print(f"=== 成功 {len(ok)} / 失败 {len(bad)} ===")
for r in ok:
    print(f"  [OK  {r['chars']:>6}] {r['rel']}  <- {r['method']}")
print("\n=== 仍失败 ===")
for r in bad:
    print(f"  [FAIL      ] {r['rel']}  <- {r['method']}")
json.dump(report, open(os.path.join(OUT, "_extract_report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n输出目录:", OUT)
