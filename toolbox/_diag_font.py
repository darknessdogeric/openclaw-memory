# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

print('=== 1. 脚本里 set_font 与 split 的实际代码 ===')
B = r'D:\B166ER-openclaw\workspace\toolbox\_mk_chair_gongwen3.py'
src = open(B, encoding='utf-8').read()
i = src.find('def set_font')
print(src[i:i + 620])
print('...')
j = src.find('‖')
print(src[max(0, j - 320):j + 320])

print('')
print('=== 2. 成品文档 P5 原始 XML ===')
DX = r'C:\Users\ericz\Desktop\产业发展部\给董事长的单独汇报\2026-11-21_发展赛道与存量改造路径_汇报要点.docx'
d = Document(DX)
p = d.paragraphs[5]
x = p._element.xml
print(x[:1800])
