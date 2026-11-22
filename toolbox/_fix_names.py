# -*- coding: utf-8 -*-
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CW = r'C:\Users\ericz\Desktop\2026-10-26_近期重点工作量化清单_v1.1.md'
cands = glob.glob(r'D:\B166ER-openclaw\workspace\anyi-ops-kb\08_*\2026-10-26_*要点吸收*.md')
if not cands:
    cands = glob.glob(r'D:\B166ER-openclaw\workspace\anyi-ops-kb\**\*要点吸收*.md', recursive=True)
if not cands:
    print('FATAL: 找不到纪要吸收文件'); sys.exit(1)
JX = cands[0]
print('定位: ' + JX)
print()


def read(p):
    return open(p, encoding='utf-8').read()


def write(p, t):
    open(p, 'w', encoding='utf-8').write(t)


common = [
    ('历程集团', '丽呈集团'),
    ('须与历程方案比选', '须与丽呈方案比选'),
    ('屿山集团', '岷山集团'),
    ('闽山集团', '岷山集团'),
]

# ---------------- 量化清单 v1.1 ----------------
print('[量化清单 v1.1]')
t = read(CW)
n = 0
for old, new in common:
    c = t.count(old)
    if c:
        t = t.replace(old, new); n += c
old_foot = '丽呈集团与国堰宾馆两处名称纠正'
new_foot = '丽呈集团、岷山集团、国堰宾馆三处转录错字校准（以知识库与人工文档为准）'
if old_foot in t:
    t = t.replace(old_foot, new_foot); n += 1
else:
    print('   [未命中] 页脚表述')
write(CW, t)
print('   替换 ' + str(n) + ' 处')

# ---------------- 纪要吸收 v1.0 ----------------
print('[纪要吸收 v1.0]')
t = read(JX)

sec_new = '''## 三、转录稿错字校准（以知识库与人工文档为准）

> **原则**：转录稿（得到大脑自动转写）存在同音错字，**不得据其改写规范名称**。
> **校准依据优先级**：① 人工撰写的正式文档 ② 知识库既有记录 ③ 转录稿。

| # | 转录稿写法 | 规范写法 | 校准依据 |
|---|---|---|---|
| 1 | 历程集团 | **丽呈集团** | 10-26《近期重点工作汇报》人工文档写作"丽呈"；知识库 00_KB_MOC、hotel-industry-knowledge-base、09-08 会议纪要均记"丽呈"；"历程"在知识库中仅出现于认知进化、理论框架等无关文件 |
| 2 | 闽山集团 | **岷山集团** | "闽山"全库仅出现于 10-26 转录稿；"岷山"在知识库多处出现（含《三份会议纪要吸收内化》） |
| 3 | 国宴宾馆 | **国堰宾馆** | 项目正式名称为"都江堰国堰宾馆"；知识库主体条目、10-23 纪要、近期汇报文档均用"国堰"。"国宴"仅残存于 8/17 会议纪要的**历史文件名**，属旧命名残留，非当前规范名 |

**结论**：10-26 纪要中的三处名称均为**转录错字**，不构成事实变更；工作台账维持"丽呈集团／岷山集团／国堰宾馆"不变。
'''

i = t.find('## 三、名称与事实纠正')
if i < 0:
    print('   [未命中] 第三节标题')
else:
    j = t.find('\n---\n', i)
    if j < 0:
        j = len(t)
    t = t[:i] + sec_new + t[j:]
    print('   第三节整块替换完成')

t = t.replace('| ⚠️ **名称纠正：丽呈 → 历程** |', '| 与 10-26 人工汇报文档口径一致（转录稿误作历程） |')
t = t.replace('| **名称纠正** | 2 | 历程集团｜国堰宾馆 |',
              '| **转录错字校准** | 3 | 丽呈集团｜岷山集团｜国堰宾馆（**维持原写法，不据转录稿改写**） |')
for old, new in common:
    t = t.replace(old, new)
write(JX, t)
print('   写回完成')

# ---------------- 校验 ----------------
print()
print('=== 残留检查（正确值应 >0，错值应 =0） ===')
for p, label in [(CW, '量化清单 v1.1'), (JX, '纪要吸收 v1.0')]:
    x = read(p)
    print(label + ':')
    for k in ['历程', '闽山', '屿山']:
        print('   错 ' + k + ' x' + str(x.count(k)))
    for k in ['丽呈集团', '岷山集团', '国堰宾馆']:
        print('   对 ' + k + ' x' + str(x.count(k)))
    print('   注 国宴 x' + str(x.count('国宴')) + '（仅应出现在校准说明中）')
