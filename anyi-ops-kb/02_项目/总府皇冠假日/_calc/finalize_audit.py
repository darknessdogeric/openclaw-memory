# -*- coding: utf-8 -*-
import io, os, sys, subprocess, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
B = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
DK = r"C:\Users\ericz\Desktop"
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-05.md"
RM = os.path.join(B, "00_项目总览_README.md")
PY = sys.executable
MD2DOCX = r"D:\B166ER-openclaw\workspace\.tmp\md2docx_cn.py"
md = os.path.join(B, "总府皇冠改造_第一批次数据缺口审计报告_v1.0_2026-11-05.md")
docx = os.path.join(DK, "总府皇冠改造_第一批次数据缺口审计报告_v1.0_2026-11-05.docx")
r = subprocess.run([PY, MD2DOCX, md, docx], capture_output=True, text=True, encoding='utf-8', errors='replace')
print("DOCX:", (r.stdout or "").strip() or (r.stderr or "").strip()[-160:] or ("OK" if os.path.exists(docx) else "MISSING"))
add = """

---

## 第一批次数据缺口审计报告成稿（桌面 docx）

### 本轮补提取 17/18 份旧格式文件成功
- bug 修复: 原用 "WordDocument" in ole.listdir() 判断失败(listdir 返回列表的列表) → 误判 6 份解析失败。修正后 17/18 成功(仅 2025年12月利润表真加密)。
- 新提取: 近24个月经营指标 / 房间分布表(带颜色) / 楼层房间数量表 / 房型净面积 / 消防逐系统台账 / 疏散核算 / 机电7份台账 / 缺口说明件5份

### 三条重大发现(数据修正,非缺口)
1. 真实正常售卖房量=351间(非402): 房间分布表单元格颜色还原 绿351/红14/灰14/蓝12/深蓝1/黄19; 工程部官方楼层表=415间(中区255+高区160,逐层一致)。6层异常(10间里8间状态差、正常售卖0)。
2. 面积账改写核心论据: 客房层建筑面积22,645.47㎡÷268间=84.5㎡/间; 标准层1,158㎡/23间=50.35㎡ → 25.35㎡面积不达标 应改写为 房量过多而非面积不足,减房即解 → 技术门槛硬变软,真正门槛是费率/投入/额度。
3. 24个月真实月度曲线 → 开工月份选择值9,431万: 月均营收564.5万(旧均摊531万偏低6.3%); 低谷12月466.7万(毛利率-0.7%唯一亏损月); 高峰3月791万(43.4%); 峰谷差69%; 方向二18月均摊14,670万 vs 精确15,155-15,501万(低估485-831万); 3月餐饮占比仅9.0%挑战第九部分13.4%→25%假设。

### 机电老化财务指纹
维保21.2→7.9万(-63%) + 能耗25.5→37.3万(+46%) + 三年43次爆管 = 该修的不修、靠抢修维持。ADR 505.54→363.99(-28%)而出租率纹丝不动(70.68%→70.78%) = 不是住不满、是住不起价。

### 官方缺口9项(目录名自证)
15.各版本方案投资构成与测算依据=0文件; ④⑤历次改扩建/竣工装修日期=在九寨暂未查到历史资料(查错档案库); (没有)品牌方分阶段书面意见=0文件(红线R-01); (没有)品牌方物业评估意见=0文件(第八部分反向论证); 26减房测算/30超高端档造价(有8项范围清单)/32沿用皇冠PIP造价/21合同(保密渠道,已另取49页)。

### 一封函闭合2缺口+解红线R-01
致洲际/六洲改造可行性咨询函5问: ①分阶段施工/分区验收/分区开业可行 ②品牌方物业评估意见 ③洲至奢选委托vs特许及费率 ④在地文化主导权划分 ⑤FLS顾问与供应商名单 → 值9,431万+方向三可行性,成本近乎为零,现在就能发。

### 模型待改4项
M1停业损失按真实月度曲线(替代均摊815万); M2客房基数三口径并列(415/402/351); M3餐饮占比分旺淡季检验; M4面积不足改写为房量过多(减房即解)

---
"""
with open(MEM, "a", encoding="utf-8") as f:
    f.write(add)
print("MEM: appended", len(add))
rm_add = """

| **第一批次数据缺口审计报告** | v1.0 | docx | 17/18 旧格式补提成功; 三重大发现: ①真实可售房量351间(非402,官方415间) ②面积账84.5㎡/间→面积不足改写为房量过多减房即解 ③24个月曲线→开工月份选择值9,431万(停业损失改按真实月度曲线) |

### 关键新数据(2026-11-05 审计)
- 可售房量: 名义415 / 在建402 / 正常售卖351(房间分布表颜色还原,与工程部楼层表、财务可售间夜三方互证)
- 24个月经营基线(2024/10-2026/09): 月均营收564.5万; 低谷12月466.7万(毛利率-0.7%); 高峰3月791万(43.4%); 峰谷差69%
- 机电老化: 维保-63% + 能耗+46% + 三年43次爆管; ADR -28%而出租率持平(不是住不满、是住不起价)
- 官方缺口9项: 一封函闭合2项(品牌方书面意见)、查错档案库2项(九寨)、0文件1项(投资构成测算)、待协同/展开3项
"""
with open(RM, "a", encoding="utf-8") as f:
    f.write(rm_add)
print("README: appended", len(rm_add))
oc = os.path.join(B, "_calc", "floorplan_ocr")
done = len([f for f in glob.glob(os.path.join(oc, "*.txt")) if os.path.basename(f) != "_progress.txt"])
print("平面图 OCR:", done, "/31")
print("=== 桌面 Word 清单 ===")
for f in sorted(glob.glob(os.path.join(DK, "总府皇冠改造_*.docx")), key=lambda p: os.path.getmtime(p), reverse=True):
    print("  %-58s %6.1f KB" % (os.path.basename(f), os.path.getsize(f)/1024))
