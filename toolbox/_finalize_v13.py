# -*- coding: utf-8 -*-
import io, sys, os, glob, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DESK = r'C:\Users\ericz\Desktop'
KB7 = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\07_战略与改革'
WS = r'D:\B166ER-openclaw\workspace'
MD = os.path.join(KB7, '2026-10-27_近期重点工作量化清单_v1.3.md')

# 定位“重要文件”目录（不写中文路径，靠已有 2026-10-26 文件反查）
dirs = set()
for f in glob.glob(os.path.join(DESK, '**', '2026-10-26_*.docx'), recursive=True):
    dirs.add(os.path.dirname(f))
if not dirs:
    print('FATAL 未定位到归置目录'); sys.exit(2)
IMP = sorted(dirs)[0]
print('归置目录: ' + IMP)

t = open(MD, encoding='utf-8').read()
n = 0


def rep(old, new):
    global t, n
    c = t.count(old)
    if c:
        t = t.replace(old, new); n += c
    else:
        print('   [MISS] ' + old[:56])


# ---- 关键节点表 / 汇总表 / 1.2 表：节点更正为 11-02 ----
rep('| 总府皇冠需求清单反馈 | **本周内** | 1.2 | 三方向比选无法启动 |',
    '| 总府皇冠信息搜集清单回收 | **11-02** | 1.2 | 方案无法起算 |')
rep('| 1.2 | 总府皇冠假日改造方案 | 改造 | 需求清单已编册提交对方 | 本周内反馈 | 三方向投资额 |',
    '| 1.2 | 总府皇冠假日改造方案 | 改造 | 需求清单已编册提交对方 | **11-02** | 三方向投资额·第四方向 |')
rep('| 需求清单 | 已编册提交对方 | 对方**本周内反馈** | **本周内** | 收到书面回复 |',
    '| 需求清单 | 已编册提交对方 | 对方按集团台账限期回传全部清单 | **11-02** | 收到书面回复 |')
rep('| 方向对比 | 3 个方向待比选 | **3×6 决策矩阵**，并增列悦榕联合品牌为第四方向 | **11-02** | 六指标全部有值，四方向齐备 |',
    '| 方向对比 | 3 个方向待比选 | **3×6 决策矩阵**，并增列悦榕联合品牌为第四方向 | 11-07 | 六指标全部有值，四方向齐备 |')

open(MD, 'w', encoding='utf-8').write(t)
print('节点更正替换 %d 处' % n)

# ---- 落地：KB + 归置目录（md 与 docx） ----
NAME_MD = os.path.basename(MD)
NAME_DOCX = NAME_MD.replace('.md', '.docx')
md_imp = os.path.join(IMP, NAME_MD)
docx_imp = os.path.join(IMP, NAME_DOCX)
open(md_imp, 'w', encoding='utf-8').write(t)

conv = os.path.join(WS, 'skills', 'docx-md-bridge', 'scripts', 'md_to_docx.py')
r = subprocess.run([sys.executable, conv, MD, docx_imp], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('转换: ' + (r.stdout or '').strip()[:120] + (r.stderr or '').strip()[:160])

# ---- 校验 ----
print()
print('=== 校验 ===')
for k in ['11-02', '11-07', '11-15', '## 四、悦榕集团合作对接', '附录D',
          '第 4 个意向方', '900 万元', '2700 至 8000 元', '20 项全覆盖', '14 处待补数据']:
    print('  %-24s %d 处' % (k, t.count(k)))
print()
for f in [MD, md_imp, docx_imp]:
    print('  %s  %.1f KB' % (os.path.basename(f), os.path.getsize(f) / 1024))
    if not os.path.exists(f):
        print('    !! 不存在')
