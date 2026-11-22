#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, json
with open('toolbox/_xiaoland_deepdive.json','r',encoding='utf-8') as f:
    deep = json.load(f)
c = deep['1688_laserradar']['content']
idx = c.find('title="')
if idx >= 0:
    snippet = c[idx:idx+2500]
    print('Snippet (raw decoded):')
    print(repr(snippet[:800]))
    print()
    # 楼 in mojibake is ¥ from GBK
    test = '楼'.encode('utf-8').decode('gbk', errors='replace')
    print('楼 →', repr(test))
    test2 = '绗'.encode('utf-8').decode('gbk', errors='replace')
    print('绗 →', repr(test2))
    test3 = '鎴愪氦'.encode('utf-8').decode('gbk', errors='replace')
    print('鎴愪氦 →', repr(test3))