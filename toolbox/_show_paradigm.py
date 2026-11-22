# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb'

def show_md(p, title, limit=9000):
    print('#' * 88)
    print('### ' + title + '  ->  ' + os.path.basename(p))
    print('#' * 88)
    t = open(p, encoding='utf-8').read()
    print(t[:limit])
    if len(t) > limit:
        print('... [截断，剩余 %d 字符]' % (len(t) - limit))
    print()

show_md(os.path.join(KB, '02_项目', '商投集团合作', '2026-10-11_安逸商投合作框架协议_v1.3.md'), '范本一：安逸-商投合作框架协议 v1.3（定稿）')
show_md(os.path.join(KB, '02_项目', '空港投资', '2026-10-26_安逸-空港投资合作框架协议_起草备忘_v1.1.md'), '范本二：安逸-空港投资合作框架协议 起草备忘 v1.1（10-26 最新）')
