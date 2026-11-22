# -*- coding: utf-8 -*-
"""v4 补丁：Mandai 中文名去掉悦榕庄项目色彩；补回五项不做"""
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SRC = r'D:\B166ER-openclaw\workspace\toolbox\_mk_chair_v4.py'
t = open(SRC, encoding='utf-8').read()

R1_OLD = "H3 = '三、样板：Mandai Rainforest Resort by Banyan Tree（新加坡万态雨林悦榕庄）'"
R1_NEW = "H3 = '三、样板：Mandai Rainforest Resort by Banyan Tree（悦榕集团新加坡样本）'"

R2_OLD = " '所以集团不按业态分类，按抢什么资源分类。业态是分类，资源是打法，方式是载体，资源是目的。',\n]"
R2_NEW = (" '所以集团不按业态分类，按抢什么资源分类。业态是分类，资源是打法，方式是载体，资源是目的。',\n"
          " '同时明确五项不做：自建高端奢华度假品牌、重资产新建（除已履行决策程序的项目外）、经济型与中端标准化连锁、'\n"
          " '非必要全服务会议型产品、以拓展带改造的对冲。',\n]")

miss = 0
for a, b in ((R1_OLD, R1_NEW), (R2_OLD, R2_NEW)):
    if a in t:
        t = t.replace(a, b, 1)
        print('  已替换: ' + a[:46])
    else:
        print('  !! 未命中: ' + a[:46])
        miss += 1
open(SRC, 'w', encoding='utf-8').write(t)
print('补丁完成，未命中 %d 处' % miss)

r = subprocess.run([sys.executable, SRC], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r.stdout)
if r.stderr:
    print('STDERR:', r.stderr[:200])
