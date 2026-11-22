# -*- coding: utf-8 -*-
"""Wait for OCR to finish, then extract key clauses from the 管理合同."""
import io, sys, os, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OCR = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\contract_ocr.txt"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\contract_clauses.txt"

# 等 OCR 落盘
for _ in range(400):
    if os.path.exists(OCR) and os.path.getsize(OCR) > 20000:
        break
    time.sleep(15)
else:
    print("TIMEOUT waiting OCR"); sys.exit(1)

txt = open(OCR, encoding="utf-8").read()
pages = re.split(r"===== PAGE (\d+) =====", txt)
print("chars:", len(txt), "pages parsed:", (len(pages) - 1) // 2)

# 关键词 → 分类
KEYS = [
    ("期限/存续", r"合同期|十年|10\s*年|自.{0,6}起.{0,10}至|有效期|届满|续约|续签|自动续"),
    ("转让与主体", r"转让|受让|变更|甲乙双方|总府实业|六洲|上海|主体资格|签约方|权利义务转让"),
    ("管理费与费用", r"管理费|基本管理费|奖励性管理费|技术服务费|系统使用费|营销|预订|忠诚度|基金|费用.{0,8}支付|结算"),
    ("装修/翻新/PIP", r"翻新|装修|改造|PIP|property\s*improvement|设备更新|资本支出|投资.{0,8}改造"),
    ("终止与解除", r"解除|终止|提前.{0,4}终止|违约|单方|提前通知|重大违约"),
    ("违约金与赔偿", r"违约金|赔偿|补偿|损害赔偿|损失"),
    ("标准与审计", r"标准|审计|检查|评估|考核|不合格|整改"),
    ("争议解决", r"仲裁|诉讼|管辖|争议|协商解决|调解"),
    ("不可抗力", r"不可抗力|情势变更|政府行为"),
    ("品牌与知识产权", r"商标|品牌|许可|知识产权|品牌使用"),
]

hits = {k: [] for k, _ in KEYS}
for i in range(1, len(pages) - 1, 2):
    pno, body = pages[i], pages[i + 1]
    for line in body.split("\n"):
        s = line.strip()
        if len(s) < 8:
            continue
        for k, pat in KEYS:
            if re.search(pat, s, re.I):
                hits[k].append((pno, s[:260]))
                break

with open(OUT, "w", encoding="utf-8") as f:
    f.write(f"# 管理合同 OCR 条款提取（总府实业 × 六洲酒店管理(上海)）\n")
    f.write(f"# 源：2019.9.27 签订《总府皇冠假日酒店管理合同延期协议及转让协议》10 年（2019.9.28–2029.9.27）｜49 页盖章扫描件\n")
    f.write(f"# OCR: rapidocr_onnxruntime 200 DPI｜⚠️ 扫描件 OCR 文本仅供定位，**引用前须与原件逐字核对**\n\n")
    for k, _ in KEYS:
        f.write(f"\n{'='*90}\n## {k}  （命中 {len(hits[k])} 条）\n{'='*90}\n")
        seen = set()
        for pno, s in hits[k]:
            key = s[:60]
            if key in seen:
                continue
            seen.add(key)
            f.write(f"[P{pno}] {s}\n")
            if len(seen) >= 30:
                break
print("written", os.path.getsize(OUT), "->", OUT)
for k, _ in KEYS:
    print(f"  {k}: {len(hits[k])}")
