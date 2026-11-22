# -*- coding: utf-8 -*-
"""收尾：补公文文首（红头/文号/签发人/主送）+ 更新附件说明 + 重出 Word"""
import io, os, sys, re
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "merge2.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.md")
t = open(MD, encoding="utf-8").read()

i_c = t.find("## 目录")
body = t[i_c:]

HEAD = """**\u5185\u90e8\u8d44\u6599\u3000\u6ce8\u610f\u4fdd\u5bc6**\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u4efd\u53f7\uff1a000001

**\u5b89\u9038\u4ea7\u53d1\u30142026\u3015\u603b\u5e9c\u6539\u9020\u65b9\u6848\u7b2c 001 \u53f7**

\u7b7e\u53d1\u4eba\uff1a

# \u5173\u4e8e\u603b\u5e9c\u7687\u51a0\u5047\u65e5\u9152\u5e97\u6539\u9020\u5347\u7ea7\u9879\u76ee\u7684\u53ef\u884c\u6027\u7814\u7a76\u62a5\u544a

**\u4e3b\u9001\uff1a\u5b89\u9038\u9152\u5e97\u96c6\u56e2\uff1a**

\u5404\u6709\u5173\u5355\u4f4d\uff1a

"""
final = HEAD + body

# 附件说明：替换为最新清单
old_att_start = final.find("**\u9644\u4ef6**\uff1a")
if old_att_start != -1:
    tail_new = """**\u9644\u4ef6**\uff1a

1. \u300a\u603b\u5e9c\u7687\u51a0\u6539\u9020_\u7acb\u9879\u65b9\u6848_\u7ec6\u9879\u6982\u7b97\u8868\u300b\uff082026 \u5e74 11 \u6708 13 \u65e5\uff0c12 \u4e2a\u5de5\u4f5c\u8868\uff1a\u65b9\u5411\u603b\u8868\u3001CAPEX \u660e\u7ec6\u3001HMA \u54c1\u724c\u8d39\u7528\u5206\u89e3\u3001240 \u884c\u6708\u5ea6\u6536\u5165\u6a21\u578b\u3001\u5f00\u5de5\u6708\u4efd\u77e9\u9635\u3001\u5206\u671f\u5f00\u4e1a\u60c5\u666f\u3001\u654f\u611f\u6027\u3001\u54c1\u724c\u843d\u5730\u72b6\u6001\u6838\u67e5\u3001\u56fd\u8d44\u95e8\u69db\u6821\u9a8c\u3001\u53e3\u5f84\u4e0e\u6570\u636e\u6e90\uff09
2. \u300a\u603b\u5e9c\u7687\u51a0\u6539\u9020_\u7b2c\u4e8c\u6279\u6b21\u8d44\u6599\u5438\u6536\u4e0e\u7ed3\u8bba\u4fee\u8ba2\u62a5\u544a\u300b\uff082026 \u5e74 11 \u6708 10 \u65e5\uff09
3. \u300a\u603b\u5e9c\u7687\u51a0\u6539\u9020_\u7efc\u5408\u6539\u9020\u62a5\u544a\u300b\u7b2c\u4e00\u81f3\u5341\u4e00\u6b21\u90e8\u5206\uff082026 \u5e74 11 \u6708 5 \u65e5\uff09
4. \u300a\u603b\u5e9c\u7687\u51a0\u6539\u9020_\u73b0\u884c\u7ba1\u7406\u5408\u540c\u6761\u6b3e\u5206\u6790\u300b\uff0849 \u9875\u5168\u672c\uff0c2026 \u5e74 11 \u6708 5 \u65e5\uff09

**\u6284\u9001**\uff1a\u56db\u5ddd\u603b\u5e9c\u5b9e\u4e1a\u6709\u9650\u516c\u53f8\uff0c\u96c6\u56e2\u8d22\u52a1\u90e8\uff0c\u96c6\u56e2\u5de5\u7a0b\u90e8\uff0c\u96c6\u56e2\u603b\u7ecf\u7406\u529e\u516c\u5ba4\uff0c\u96c6\u56e2\u6cd5\u5f8b\u5408\u89c4\u90e8\u3002

\u56db\u5ddd\u5bbe\u9986\u96c6\u56e2\uff08\u5b89\u9038\u9152\u5e97\u96c6\u56e2\uff09\u4ea7\u4e1a\u53d1\u5c55\u90e8\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u2026 \u5e74 11 \u6708 13 \u65e5

\u5370\u53d1\u673a\u5173\uff1a\u56db\u5ddd\u5bbe\u9986\u96c6\u56e2\uff08\u5b89\u9038\u9152\u5e97\u96c6\u56e2\uff09\u4ea7\u4e1a\u53d1\u5c55\u90e8\u3000\u3000\u3000\u5370\u53d1\u65e5\u671f\uff1a2026 \u5e74 11 \u6708 13 \u65e5
"""
    final = final[:old_att_start] + tail_new

open(MD, "w", encoding="utf-8").write(final)
L("MD bytes:", len(final.encode("utf-8")))
L("--- 头部 ---")
for l in final.split("\n")[:16]:
    L("  " + l.encode("unicode_escape").decode("ascii")[:110])
L("--- 尾部 ---")
for l in final.split("\n")[-14:]:
    L("  " + l.encode("unicode_escape").decode("ascii")[:110])
EMOJI = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50]"
L("emoji:", len(re.findall(EMOJI, final)))
bad = [l for l in final.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 95)]
L("heading issues:", len(bad))
for b in bad[:5]:
    L("  !", b[:110])

sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx")
convert(MD, out)
L("DOCX %.1f KB" % (os.path.getsize(out)/1024))
L("DONE")
