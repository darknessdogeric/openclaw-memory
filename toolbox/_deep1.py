# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
KB = 'D:\\B166ER-openclaw\\workspace\\anyi-ops-kb'

FILES = [
 ('董事长要求_生活方式酒店模型', '07_战略与改革', '十五五战略定位研究', '07_董事长要求_生活方式酒店具体模型_前台后台双层架构_v1.0.md'),
 ('7家酒店周报调研纪要与集团认知', '07_战略与改革', '十五五战略定位研究', '06_7家酒店周报调研纪要与集团认知_v0.6_2026-08-14.md'),
 ('酒店业务现状分析_专家座谈', '07_战略与改革', '', '2026-08-13_安逸集团酒店业务现状分析与发展建议_战略规划专家座谈_v1.0.md'),
 ('邹士勇发言稿_高参圆桌', '02_项目', '高参峰会', '邹士勇发言稿_2026高参圆桌国资酒店_2026-08-28_v4.0_精简版.md'),
 ('15五规划战略拓扑图', '07_战略与改革', '', '安逸酒店集团十五五规划战略拓扑图_v1.0_2026-09-12.md'),
 ('15五规划权威要点', '07_战略与改革', '', '安逸酒店集团十五五规划_权威要点_v1.0_2026-09-26.md'),
 ('对下属酒店KPI维度', '07_战略与改革', '', '安逸集团_对下属酒店KPI维度_v1.1_2026-08-09.md'),
 ('春熙路有限服务产品方案', '02_项目', '花园宾馆改造', '安逸春熙路标杆中高档有限服务精选酒店产品方案_v1.4_财务重测版2_2026-08-26.md'),
]
KEY = ['定位','主赛道','赛道','生活方式','有限服务','全服务','产品线','客群','目标客','中端','高端','下沉','政务','度假','康养','区域','双层','前台','后台','模型','主张','错位','核心','结论','建议','不做','取舍','品牌矩阵','轻资产','输出','轻重']
for tag, d1, d2, fn in FILES:
    path = os.path.join(KB, d1, d2, fn) if d2 else os.path.join(KB, d1, fn)
    print('=' * 92)
    print('【' + tag + '】' + fn)
    if not os.path.exists(path):
        print('  !! 缺失'); continue
    t = open(path, encoding='utf-8', errors='replace').read()
    lines = t.split(chr(10))
    print('  长度 %d 字符' % len(t))
    for h in [l for l in lines if l.strip().startswith('#')][:24]:
        print('   ' + h.strip()[:108])
    print('  --- 关键段落 ---')
    n = 0
    for l in lines:
        s = l.strip()
        if len(s) < 12 or s.startswith('#') or s.startswith('|') or s.startswith('>'):
            continue
        if any(k in s for k in KEY):
            print('   * ' + s[:230])
            n += 1
            if n >= 13: break
    print()
