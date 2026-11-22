# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

WS = 'D:\\B166ER-openclaw\\workspace'
KB = os.path.join(WS, 'anyi-ops-kb')
ROOT = 'C:\\Users\\ericz\\Desktop\\产业发展部\\酒店摸排'
D1 = os.path.join(ROOT, '01_发文件')
D2 = os.path.join(ROOT, '02_摸排底册与口径')
D3 = os.path.join(ROOT, '03_填报与回收')

# ---------- 1. 项目索引 ----------
idx = []
idx.append('# 酒店摸排　文件索引')
idx.append('')
idx.append('> **项目**：集团旗下酒店全面摸排与基础数据填报');
idx.append('> **发起**：Eric 2026-11-13 11:43（现状掌握与实际有出入，须由酒店自报形成完整底数）');
idx.append('> **承办**：安逸酒店集团产业发展部');
idx.append('> **建立日期**：2026-11-13');
idx.append('> **关联**：《2026-11-13_关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告》第三、四、五、六章');
idx.append('');
idx.append('## 一、目录结构');
idx.append('');
idx.append('```');
idx.append('酒店摸排');
idx.append('├─ 00_酒店摸排_文件索引.md          本文件');
idx.append('├─ 01_发文件/                        报集团、拟下发各酒店');
idx.append('│   └─ 关于开展集团旗下酒店全面摸排与基础数据填报工作的通知_20261113.docx');
idx.append('│       正文六部分 + 附件一至附件四，可直接整份下发');
idx.append('├─ 02_摸排底册与口径/                 底册与口径，酒店自行核对用');
idx.append('│   ├─ 附件一_安逸集团旗下酒店摸排底册_v1.0.docx / .md');
idx.append('│   └─ （口径定义见主件附件二）');
idx.append('└─ 03_填报与回收/                     回收归集区');
idx.append('    └─ 附件三_填报表（空白模板）_v1.0.docx / .md');
idx.append('```');
idx.append('');
idx.append('## 二、文件清单与用途');
idx.append('');
idx.append('| 文件 | 规格 | 用途 |');
idx.append('|---|---|---|');
idx.append('| 01_发文件/关于开展集团旗下酒店全面摸排与基础数据填报工作的通知_20261113.docx | 51.5 KB / 92 段 / 14 表 | 整份下发。正文为通知与工作要求；附件一为摸排底册供核对；附件二为填报须知与口径定义；附件三为八张填报表；附件四为差异说明汇总表 |');
idx.append('| 02_摸排底册与口径/附件一_安逸集团旗下酒店摸排底册_v1.0.docx | 40.8 KB / 106 条目 | 单独下发便于酒店核对是否在册、是否遗漏、房数是否准确。含 11 处房数冲突标记与 5 家到期合同标记 |');
idx.append('| 03_填报与回收/附件三_填报表（空白模板）_v1.0.docx | 39.1 KB / 10 张表 | 单独下发便于酒店填报与内部先填。表六之一为现行收费清单逐项填报表 |');
idx.append('');
idx.append('## 三、填报与回收进度');
idx.append('');
idx.append('| 环节 | 时点 | 状态 |');
idx.append('|---|---|---|');
idx.append('| 发文 | 2026-11-14 前 | 待执行 |');
idx.append('| 各店填报 | 2026-11-20 前 | 待启动 |');
idx.append('| 集团复核 | 2026-11-25 前 | 待启动 |');
idx.append('| 存量改造分级分诊初稿 | 2026-11-30 前 | 待启动 |');
idx.append('');
idx.append('## 四、回收件存放规则');
idx.append('');
idx.append('各店回收件按酒店名称建子文件夹存放于 03_填报与回收/ 下，格式为「酒店简称_填报人_报送日期」，盖章扫描件与可编辑版并存。复核退回件在原目录下加后缀「_退回重报」。');
idx.append('');
idx.append('## 五、来源与时间戳');
idx.append('');
idx.append('| 数据源 | 时点 |');
idx.append('|---|---|');
idx.append('| 安逸直营酒店名录（17及32名录）_脱敏版 | 2026-11-04 |');
idx.append('| 轻资产在管酒店0915（43家）_脱敏版 | 2026-11-04 |');
idx.append('| 202609在营酒店（自有资产+轻资产委托管理项目） | 2026-09 |');
idx.append('| 摸排底册（产业发展部自摸底，未经各店确认） | 2026-11-13 |');

ip = os.path.join(ROOT, '00_酒店摸排_文件索引.md')
open(ip, 'w', encoding='utf-8').write(chr(10).join(idx))
print('索引已建: ' + ip + '  (' + str(os.path.getsize(ip)) + ' B)');

# ---------- 2. 来源台账追加 ----------
led = os.path.join(KB, '00_来源台账.md')
mark = '2026-11-13 追加 — 旗下酒店摸排底册与摸排发文'
t = open(led, encoding='utf-8', errors='replace').read()
if mark in t:
    print('台账已含该条目，跳过');
else:
    blk = []
    blk.append('');
    blk.append('## 📥 入库清单（2026-11-13 追加 — 旗下酒店摸排底册与摸排发文）');
    blk.append('');
    blk.append('> **任务来源**：Eric 2026-11-13 11:43 —— "目前你的实际情况掌握和安逸的现状有出入……我需要一份旗下酒店摸排的相关文件，发到旗下所有酒店。"');
    blk.append('> **归档执行**：B166ER 2026-11-13，读取集团五份原始名录 xlsx 逐条提取归一化去重，生成 106 条目摸排底册与八张填报表');
    blk.append('> **交付位置**：`产业发展部\\酒店摸排\\`（新建项目文件夹，按 发文件／底册与口径／填报与回收 分子目录）');
    blk.append('');
    blk.append('| # | 材料 | 原始路径 | 成文/生成日期 | 数据截止 | 类型 | 入库位置 |');
    blk.append('|---|------|----------|------------|---------|------|----------|');
    blk.append('| 1 | **安逸直营酒店名录（17及32名录）_脱敏版_2026-11-04.xlsx** | `产业发展部\\旗下酒店\\` | 2026-11-04 | 2026-11-04 | 集团原始名录 | 底册来源 |');
    blk.append('| 2 | **轻资产在管酒店0915（43家）_脱敏版_2026-11-04.xlsx** | `产业发展部\\旗下酒店\\` | 2026-11-04 | 2026-11-04 | 集团原始名录 | 底册来源 |');
    blk.append('| 3 | **202609在营酒店（自有资产+轻资产委托管理项目）-(地址+负责人+电话)(1).xlsx** | `产业发展部\\重要文件\\` | 2026-09 | 2026-09 | 集团原始名录 | 底册来源 |');
    blk.append('| 4 | **附件一_安逸集团旗下酒店摸排底册_v1.0** | 产业发展部自建 | 2026-11-13 | 2026-11-13 | 摸排底册（未经各店确认） | `产业发展部\\酒店摸排\\02_摸排底册与口径\\` |');
    blk.append('| 5 | **关于开展集团旗下酒店全面摸排与基础数据填报工作的通知_20261113** | 产业发展部自建 | 2026-11-13 | 2026-11-13 | 集团发文（待下发） | `产业发展部\\酒店摸排\\01_发文件\\` |');
    blk.append('| 6 | **附件三_填报表（空白模板）_v1.0** | 产业发展部自建 | 2026-11-13 | 2026-11-13 | 填报表模板 | `产业发展部\\酒店摸排\\03_填报与回收\\` |');
    blk.append('');
    blk.append('**KB 吸收件**：`anyi-ops-kb/07_战略与改革/2026-11-13_安逸集团旗下酒店自摸底与摸排方案_v1.0.md`');
    blk.append('');
    open(led, 'a', encoding='utf-8').write(chr(10).join(blk))
    print('台账已追加 -> ' + str(os.path.getsize(led)) + ' B');

# ---------- 3. 最终校验 ----------
CHK = [('关于开展集团旗下酒店全面摸排与基础数据填报工作的通知_20261113.docx', D1),
       ('附件一_安逸集团旗下酒店摸排底册_v1.0.docx', D2),
       ('附件三_填报表（空白模板）_v1.0.docx', D3)]
KEYS = ['附件二', '五、改造级别定义', 'L0', 'L1', 'L2', 'L3', 'L4', '单房投资参考', '代收代付', '可售房数', 'RevPAR', '差异说明汇总表']
for fn, dd in CHK:
    p = os.path.join(dd, fn)
    d = Document(p)
    ft = ''.join(x.text for x in d.paragraphs) + chr(10) + ''.join(cl.text for t in d.tables for rr in t.rows for cl in rr.cells)
    miss = [k for k in KEYS if k not in ft]
    print('');
    print('== ' + fn)
    print('   %.1f KB  段落 %d  表格 %d  粗体残留:%s' % (os.path.getsize(p)/1024, len(d.paragraphs), len(d.tables), '有' if '**' in ft else '无'));
    print('   关键内容缺失: ' + (', '.join(miss) if miss else '无'));
print('');
print('=== 目录清单 ===');
for root, dirs, files in os.walk(ROOT):
    lvl = root[len(ROOT):].count(os.sep);
    print('  ' * lvl + '[' + os.path.basename(root) + ']');
    for f in sorted(files):
        print('  ' * (lvl + 1) + f[:70] + '  (' + str(os.path.getsize(os.path.join(root, f))//1024) + ' KB)');