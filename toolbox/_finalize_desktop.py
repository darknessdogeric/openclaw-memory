# -*- coding: utf-8 -*-
import io, sys, os, glob, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

DESK = r'C:\Users\ericz\Desktop'
PROJ = r'C:\Users\ericz\Desktop\产业发展部\项目\美团本地生活'
KB = r'D:\B166ER-openclaw\workspace\anyi\anyi-ops-kb\02_项目\安逸×美团本地生活合作'

primary = os.path.join(DESK, '安逸集团&美团充电宝战略合作框架协议_合并稿_20261106.docx')
revised = os.path.join(DESK, '安逸集团&美团充电宝战略合作框架协议_合并稿_20261106_修订版.docx')
good_src = os.path.join(PROJ, '安逸集团&美团充电宝战略合作框架协议_合并稿_20261106.docx')

print('锁文件:', [os.path.basename(x) for x in glob.glob(os.path.join(DESK, '~$*'))])


def junk_count(fp):
    d = Document(fp)
    f = ''.join(x.text for x in d.paragraphs)
    bad = sum(f.count(k) for k in ['B 甲方', 'B 乙方', 'B 统一', 'B 地址', 'B 联系',
                                   'B 法定', 'B 日期', '2 一、甲方', '2 二、乙方'])
    return len(d.paragraphs), len(f), bad


for fp in (primary, revised, good_src):
    if os.path.exists(fp):
        print('%-46s %8d  %s' % (os.path.basename(fp), os.path.getsize(fp), junk_count(fp)))

# 目标：桌面主名 = 最终内容；删除 _修订版
try:
    shutil.copy2(good_src, primary)
    print('primary refreshed OK')
except PermissionError as e:
    print('primary still locked:', e)

if os.path.exists(revised):
    try:
        os.remove(revised)
        print('revised removed')
    except PermissionError as e:
        print('revised NOT removable:', e)

print()
print('=== 最终桌面状态 ===')
for fp in sorted(glob.glob(os.path.join(DESK, '*美团*'))):
    if os.path.basename(fp).startswith('~$'):
        continue
    print('%-60s %8d' % (os.path.basename(fp), os.path.getsize(fp)))
for fp in sorted(glob.glob(os.path.join(DESK, '~$*'))):
    print('  [LOCK] %s' % os.path.basename(fp))

print()
print('=== 最终交付物校验（主名文件）===')
d = Document(primary if os.path.exists(primary) else good_src)
f = ''.join(x.text for x in d.paragraphs)
checks_absent = ['收入分配方式为9:1', '原告所在地', '设置（）小时免费权益方案',
                 '不再与其他第三方', '排他', '独家', '有效期一年',
                 '乙方：美团（XXXX）', '（专属约定）']
checks_present = ['天津三快信息技术有限公司', '唯一实际执行主体', '唯一有效执行文件',
                  '显示甲方会员入口', '乙方应支持甲方会员积分体系',
                  '甲方对所提供的标识纹样及设计图案享有知识产权',
                  '第四条 数据与会员', '本框架协议合作期限：3年',
                  '提交甲方所在地人民法院诉讼解决', '经甲方审核同意后方可变更',
                  '组建联合工作小组', '同时段最惠价格']
bad = 0
for k in checks_absent:
    if k in f:
        bad += 1
        print('  [应无] %-30s *** 仍存在 ***' % k)
for k in checks_present:
    if k not in f:
        bad += 1
        print('  [应有] %-30s *** 缺失 ***' % k)
for k in ['B 甲方', '2 一、甲方']:
    if k in f:
        bad += 1
        print('  [残渣] %-30s *** 仍存在 ***' % k)
print('  FAIL COUNT =', bad)
print('  段落 %d  字数 %d' % (len(d.paragraphs), len(f)))
