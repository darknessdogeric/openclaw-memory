# -*- coding: utf-8 -*-
"""Mine 洲际品牌标准(PIP) for 国际联号标准配置: 餐饮outlet/康体/会议/客房/行政酒廊/人力."""
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC = r"D:\B166ER-openclaw\workspace\.tmp\extract"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\pip_standards.txt"

PATS = [
    ("餐饮outlet", r"餐厅|咖啡|酒吧|餐厅数量|outlet|全日餐厅|全日制"),
    ("康体SPA", r"康体|水疗|泳池|健身房|SPA|桑拿|按摩"),
    ("会议宴会", r"会议室|宴会厅|多功能厅|会议区|会议室数量"),
    ("客房配置", r"客房面积|最小客房|豪华客房|行政楼层|行政酒廊|套间"),
    ("人力配置", r"员工|人房比|雇员|服务人员"),
    ("非房收入", r"餐饮收入|会议收入|康体收入|其他收入|收入占比"),
    ("品牌标准关键", r"必须.{0,30}(配备|设置|提供|具备)"),
]

files = sorted(glob.glob(os.path.join(SRC, "*.txt")))
pip = [f for f in files if "品牌标准" in os.path.basename(f) or "PIP" in os.path.basename(f)]
print("total files:", len(files), "| brand-standard files:", len(pip))
for f in pip:
    print("   *", os.path.basename(f)[:90])

with open(OUT, "w", encoding="utf-8") as out:
    for label, pat in PATS:
        out.write(f"\n{'='*92}\n### {label}  (pattern: {pat})\n{'='*92}\n")
        seen, n = set(), 0
        for fp in files:
            try:
                lines = open(fp, encoding="utf-8", errors="replace").read().split("\n")
            except Exception:
                continue
            fn = os.path.basename(fp)[:52]
            for ln, l in enumerate(lines):
                l = l.strip()
                if len(l) < 12 or len(l) > 400:
                    continue
                if not re.search(pat, l):
                    continue
                k = re.sub(r"\s+", "", l)[:80]
                if k in seen:
                    continue
                seen.add(k)
                out.write(f"[{fn} L{ln}] {l[:330]}\n")
                n += 1
                if n >= 60:
                    break
            if n >= 60:
                break
        print(f"  {label}: {n} kept")
print("written", os.path.getsize(OUT))
