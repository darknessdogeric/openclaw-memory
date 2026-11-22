# -*- coding: utf-8 -*-
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

PROJ = r'C:\Users\ericz\Desktop\产业发展部\项目\美团本地生活'
KB = r'D:\B166ER-openclaw\workspace\anyi\anyi-ops-kb\02_项目\安逸×美团本地生活合作'
W = r'D:\B166ER-openclaw\workspace'

TARGET = '安逸集团&美团充电宝战略合作框架协议_合并稿_20261106.docx'

ABSENT = ['收入分配方式为9:1', '原告所在地', '设置（）小时免费权益方案',
          '不再与其他第三方', '排他', '排它', '独家', '有效期一年',
          '乙方：美团（XXXX）', '（专属约定）', '具体以双方约定为准']
PRESENT = ['天津三快信息技术有限公司', '唯一实际执行主体', '唯一有效执行文件',
           '显示甲方会员入口', '乙方应支持甲方会员积分体系',
           '甲方对所提供的标识纹样及设计图案享有知识产权',
           '第四条 数据与会员', '本框架协议合作期限：3年',
           '提交甲方所在地人民法院诉讼解决', '经甲方审核同意后方可变更',
           '组建联合工作小组', '同时段最惠价格', '用电安全、消防安全及消费者权益保护']
JUNK = ['B 甲方', 'B 乙方', 'B 统一', 'B 地址', 'B 联系', 'B 法定', 'B 日期',
        '2 一、甲方', '2 二、乙方']

for label, folder in [('项目文件夹', PROJ), ('KB', KB)]:
    fp = os.path.join(folder, TARGET)
    print('=' * 68)
    print(label, '->', fp)
    if not os.path.exists(fp):
        print('  !! MISSING')
        continue
    d = Document(fp)
    f = ''.join(x.text for x in d.paragraphs)
    bad = 0
    for k in ABSENT:
        if k in f:
            bad += 1
            print('  [应无] %-30s *** 仍存在 ***' % k)
    for k in PRESENT:
        if k not in f:
            bad += 1
            print('  [应有] %-30s *** 缺失 ***' % k)
    for k in JUNK:
        if k in f:
            bad += 1
            print('  [残渣] %-30s *** 仍存在 ***' % k)
    print('  段落 %d  字数 %d  大小 %d  FAIL=%d' % (
        len(d.paragraphs), len(f), os.path.getsize(fp), bad))
    print()

# ---------- 修 MEMORY.md 里写错的交付说明 ----------
m = os.path.join(W, 'MEMORY.md')
txt = open(m, encoding='utf-8').read()
old = ('**交付**：《安逸集团&美团充电宝战略合作框架协议_合并稿_20261106.docx》（74 段，正文 3,509 字，8 章）'
       '→ 项目文件夹 / KB；桌面同名文件当时被 Word 占用（Eric 打开中）无法覆盖，故桌面上为 **_修订版** '
       '文件名（内容为最终版）。KB 同步归档 09_框架协议合并说明_两版逐条对照.md + 10_乙方原版。')
new = ('**交付**：《安逸集团&美团充电宝战略合作框架协议_合并稿_20261106.docx》（74 段，正文 3,493 字，8 章）'
       '→ **桌面\\产业发展部\\项目\\美团本地生活\\**（与源文件同目录，主名）+ KB 项目目录（主名），两份均已校验 FAIL=0。'
       '**桌面根目录同名文件是早期 bug 版且正被 Word 占用（Eric 打开中），无法覆盖或删除**，内容含渲染残渣 18 处'
       '（"B 甲方"/"2 一、甲方"）且缺"唯一实际执行主体"；关闭 Word 后需删除该残留。'
       'KB 同步归档 09_框架协议合并说明_两版逐条对照.md + 10_乙方原版。')
if old in txt:
    txt = txt.replace(old, new)
    open(m, 'w', encoding='utf-8').write(txt)
    print('MEMORY.md 交付说明已更正')
else:
    print('!! MEMORY.md 原句未匹配（需人工核对）')
    idx = txt.find('合并稿_20261106.docx**（74 段')
    print('   上下文:', repr(txt[idx-60:idx+260]) if idx > 0 else 'not found')

# ---------- 追加当日日志 ----------
dpath = os.path.join(W, 'memory', '2026-11-06.md')
entry = '''

## 10:21 中断后复核与桌面状态修正

- 上一轮在更新进度卡时被中断（工具参数路由问题，非任务失败）。合并稿交付本身已完成并通过校验。
- **桌面占用情况**：桌面根目录 `安逸集团&美团充电宝战略合作框架协议_合并稿_20261106.docx` 一直被 Word 占用（存在 `~$集团&美团充电宝...` 锁文件），python-docx 保存报 PermissionError，无法覆盖也无法删除。该文件是**第一版生成、含解析器 bug 的版本**（正文混入 "B 甲方"/"2 一、甲方" 等残渣 18 处，且缺"唯一实际执行主体"保护条款）。
- **修正过程中的一个失误**：为清理桌面，我删除了兜底的 `_修订版`（当时它是干净的最终版），结果桌面根目录只剩那份被占用的 bug 版。**最终版在项目文件夹与 KB，均为主名、内容干净、FAIL=0**，未丢失。
- **最终交付位置**：`桌面\产业发展部\项目\美团本地生活\安逸集团&美团充电宝战略合作框架协议_合并稿_20261106.docx`（与源文件同目录，主名）+ KB 项目目录同名文件。桌面根目录的残留待 Word 关闭后删除。
- **工具坑（补记）**：① 被 Word 占用的 docx 无法覆盖 → 必须先写 staging 再 copy，copy 失败时改用备用文件名，不要先删唯一的干净副本 ② glob 匹配 docx 会命中 `~$` 锁文件，需过滤 ③ 自写标记语言解析器不支持多字符标签（`^NB`→N+B、`^H2`→H+2），必须用正则 `^([A-Z][A-Z0-9]*)(.*)$`，否则正文字面量混入标签残渣 ④ 校验脚本里"应无项"要用 `not in` 判定，我一度写反导致误报 FAIL。
'''
with open(dpath, 'a', encoding='utf-8') as fh:
    fh.write(entry)
print('daily log appended ->', len(open(dpath, encoding='utf-8').read().split(chr(10))), 'lines')
