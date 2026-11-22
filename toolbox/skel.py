# -*- coding: utf-8 -*-
import io, re
F1 = r"C:\Users\ericz\Desktop\安逸集团基于2025年审计数据的经营治理与资产优化工作部署会议内容梳理-2026年11月11日-来自【得到大脑】.md"
F2 = r"C:\Users\ericz\Desktop\安逸酒店集团资产经营策略与中长期发展规划研讨-2026年11月11日-来自【得到大脑】.md"
KEY = re.compile(r"(审计|整改|关停|转让|出租|处置|专项债|抵押|资产包|REITs|基金|规划|决定|要求|责任部门|时限|考核|压降|目标|亿|千万|国资|混改|酒店清单|清单|策略|一揽子)")
out = []
for tag, F in (("A审计治理", F1), ("B资产经营策略", F2)):
    lines = io.open(F, encoding="utf-8").read().split("\n")
    out.append("=" * 110)
    out.append("FILE %s | 行数=%d | 字数=%d" % (tag, len(lines), sum(len(x) for x in lines)))
    out.append("=" * 110)
    out.append("---- 前 60 行 ----")
    for i, l in enumerate(lines[:60], 1):
        if l.strip():
            out.append("%4d| %s" % (i, l[:190]))
    out.append("---- 关键行索引（含决策/金额/清单） ----")
    n = 0
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if len(s) > 8 and KEY.search(s):
            out.append("%4d| %s" % (i, s[:190]))
            n += 1
            if n > 130:
                out.append("     ... (截断)")
                break
    out.append("")
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\meet_skeleton.txt","w",encoding="utf-8").write("\n".join(out))
print("OK lines=%d" % len(out))
