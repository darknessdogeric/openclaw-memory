# -*- coding: utf-8 -*-
import io, sys, os, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
EV = r"D:\B166ER-openclaw\workspace\output\book_纹样设计速查手册"
# ★ 章节名以权威 OPAC 目录为准（越秀外国语学院 MARC 目录），不再从正文猜
CH = {"一":"纹样简史","二":"几何物语","三":"植物之美","四":"祥瑞兽谱",
      "五":"鸟鸣花落","六":"万物生灵","七":"人物之美"}
T2S = str.maketrans("紋樣華麗龍鳳鳥蟲獸蝶人物幾何雲氣連續變形團窠龜背如意萬字方勝鎖子盤腸纏枝寶相蓮牡丹瓜果獸面簡單東西飛天雞羽翼禽獸馬牛羊魚龍鳳鳥雀鴛鴦花鳥蟲魚書畫器物神話福祿壽喜吉祥禪道佛仙禽鳥花果木葉枝根莖藤蔓瓜實稻黍稷麥豆稻粱稷",
 "纹样华丽龙凤鸟虫兽蝶人物几何云气连续变形团窠龟背如意万字方胜锁子盘肠缠枝宝相莲牡丹瓜果兽面简单东西飞天鸡羽翼禽兽马牛羊鱼龙凤鸟雀鸳鸯花鸟虫鱼书画器物神话福禄寿喜吉祥禅道佛仙禽鸟花果木叶枝根茎藤蔓瓜实稻黍稷麦豆稻粱稷")
s = open(os.path.join(EV,"sanmin_纹样之美完整目录.txt"), encoding="utf-8").read().replace("\n"," ")
conv = lambda x: x.translate(T2S)
# 切段：先找所有"第X章"位置
marks=[(m.start(), m.group(1)) for m in re.finditer(r"第([一二三四五六七八九十])章", s)]
print("章标记 %d 个: %s" % (len(marks), [m[1] for m in marks]))
items=[]
pat = re.compile(r"([\u4e00-\u9fff]{2,14}?)(\d{1,3})(?![0-9])")
for m in pat.finditer(s):
    name=m.group(1); page=int(m.group(2))
    if not (1<=page<=245): continue
    name=re.sub(r"第[一二三四五六七八九十]章.*$","",name)
    name=re.sub(r"[一-鿿]{0,3}頁$","",name)
    if len(name)<2: continue
    ch=None; cno=None
    for st,c in marks:
        if st<=m.start(): cno=c
        else: break
    items.append({"name":conv(name),"name_raw":name,"page":page,
                  "chapter_no":cno,"chapter":CH.get(cno,"?") if cno else "?"})
seen=set(); clean=[]
for r in items:
    k=(r["name"],r["page"])
    if k in seen: continue
    seen.add(k); clean.append(r)
print("解析 %d 条" % len(clean))
bys={}
for r in clean: bys.setdefault(r["chapter"],[]).append(r)
for c in ["纹样简史","几何物语","植物之美","祥瑞兽谱","鸟鸣花落","万物生灵","人物之美"]:
    rs=bys.get(c,[]); ps=[x["page"] for x in rs]
    print("   %-8s %3d 条 ｜ 页 %s" % (c,len(rs), ("%d-%d"%(min(ps),max(ps))) if ps else "—"))
# 校验：页码单调性（同名不同页 → 可能是误切）
dups={}
for r in clean: dups.setdefault(r["name"],set()).add(r["page"])
multi={k:v for k,v in dups.items() if len(v)>1}
print("   同名多页（可能切分噪声）: %d 例" % len(multi))
p=json.load(open(os.path.join(EV,"纹样索引.json"),encoding="utf-8"))
p["index_meihua"]=clean
json.dump(p, open(os.path.join(EV,"纹样索引.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("   索引已更新")
print()
print("="*100); print("内化笔记格式样本：《Kano模型》"); print("="*100)
KB=r"D:\B166ER-openclaw\workspace\anyi-ops-kb\04_方法论"
f=os.path.join(KB,"方法论书籍内化","《Kano模型》核心内化笔记_v1.0_2026-10-11.md")
print(open(f,encoding="utf-8").read())
print()
print("=== 该目录是否有索引文件 ===")
for x in sorted(os.listdir(os.path.join(KB,"方法论书籍内化"))): print("   ", x)
