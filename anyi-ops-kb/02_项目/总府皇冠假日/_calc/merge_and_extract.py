# -*- coding: utf-8 -*-
"""Merge available OCR pages (partial OK) + extract key contract clauses."""
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
PAGES = os.path.join(D, "ocr_pages")
NP = 49
MERGED = os.path.join(D, "contract_ocr.txt")
CLAUSES = os.path.join(D, "contract_clauses.txt")

# 1) 合并已落盘页（缺页标记 pending）
parts, missing = [], []
for p in range(1, NP + 1):
    f = os.path.join(PAGES, f"p{p:02d}.txt")
    if os.path.exists(f):
        t = open(f, encoding="utf-8").read()
    else:
        t = "[PENDING — 该页 OCR 未完成，待补]"
        missing.append(p)
    parts.append(f"\n===== PAGE {p} =====\n{t}")
open(MERGED, "w", encoding="utf-8").write("".join(parts))
print(f"merged: {os.path.getsize(MERGED)} chars, missing pages: {missing}")

txt = "".join(parts)
pages = re.split(r"===== PAGE (\d+) =====", txt)

KEYS = [
    ("期限与存续", r"合同期|十年|10\s*年|有效期|届满|续约|续签|自动续|存续|起始|终止日"),
    ("转让与主体", r"转让|受让|主体资格|甲乙|总府实业|六洲|上海|签约方|权利义务|债权债务"),
    ("管理费与费用", r"管理费|奖励性|技术服务费|系统使用费|营销|预订|忠诚度|基金|结算|付费|佣金"),
    ("装修翻新与PIP", r"翻新|装修|改造|PIP|设备更新|资本支出|投资.{0,8}改造|工程"),
    ("终止与解除", r"解除|终止|提前.{0,4}终止|违约|单方|重大违约|不可抗力"),
    ("违约金与赔偿", r"违约金|赔偿|补偿|损害"),
    ("标准与审计", r"标准|审计|检查|评估|考核|不合格|整改|监督"),
    ("争议解决", r"仲裁|诉讼|管辖|争议|协商解决"),
    ("品牌与知识产权", r"商标|品牌|许可|知识产权|品牌使用|系统"),
]

hits = {k: [] for k, _ in KEYS}
for i in range(1, len(pages) - 1, 2):
    pno, body = pages[i], pages[i + 1]
    for line in body.split("\n"):
        s = line.strip()
        if len(s) < 10 or "PENDING" in s:
            continue
        for k, pat in KEYS:
            if re.search(pat, s, re.I):
                hits[k].append((pno, s[:300]))
                break

with open(CLAUSES, "w", encoding="utf-8") as f:
    f.write("# 管理合同 OCR 条款提取\n")
    f.write("# 源：2019.9.27 签订《总府皇冠假日酒店管理合同延期协议及转让协议》10 年（2019.9.28–2029.9.27）｜49 页盖章扫描件\n")
    f.write("# OCR：rapidocr_onnxruntime 200 DPI\n")
    f.write(f"# ⚠️ 已完成 {NP - len(missing)}/49 页，缺页 {missing}（待补）\n")
    f.write("# ⚠️ 扫描件 OCR 文本仅供定位，**引用前须与原件逐字核对**\n\n")
    for k, _ in KEYS:
        f.write(f"\n{'='*88}\n## {k}（命中 {len(hits[k])}）\n{'='*88}\n")
        seen = set()
        for pno, s in hits[k]:
            kk = s[:60]
            if kk in seen:
                continue
            seen.add(kk)
            f.write(f"[P{pno}] {s}\n")
            if len(seen) >= 26:
                break
print("clauses ->", os.path.getsize(CLAUSES))
for k, _ in KEYS:
    print(f"  {k}: {len(hits[k])}")
