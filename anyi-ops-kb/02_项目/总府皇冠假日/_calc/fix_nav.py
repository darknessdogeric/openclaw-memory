# -*- coding: utf-8 -*-
"""docx 标题大纲级别（Word 导航窗格可用）+ keep_with_next"""
import re, os, shutil
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
DOC = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\改造报告交付\总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.docx"
TMP = r"D:\B166ER-openclaw\workspace\.tmp\_v3_nav.docx"
d = Document(DOC)


def set_outline(p, lvl):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:outlineLvl")):
        pPr.remove(old)
    e = OxmlElement("w:outlineLvl")
    e.set(qn("w:val"), str(lvl))
    pPr.append(e)


cnt = {"0": 0, "1": 0, "2": 0, "3": 0}
for p in d.paragraphs:
    tx = p.text.strip()
    if not tx or len(tx) > 60:
        continue
    if re.match(r"^\d+\. [一二三四五六七八九十]+、", tx):
        continue          # 目录条目，不设大纲
    lvl = None
    if tx == "关于总府皇冠假日酒店改造升级工作思路的报告":
        lvl = 0
    elif re.match(r"^[一二三四五六七八九十]+、\S", tx):
        lvl = 1
    elif re.match(r"^（[一二三四五六七八九十]+）", tx):
        lvl = 2
    elif re.match(r"^\d+\.\d+\s", tx):
        lvl = 3
    if lvl is not None:
        set_outline(p, lvl)
        p.paragraph_format.keep_with_next = True
        cnt[str(lvl)] += 1

d.save(TMP)
shutil.move(TMP, DOC)
print("大纲级别设置: L0=%d L1=%d L2=%d L3=%d" % (cnt["0"], cnt["1"], cnt["2"], cnt["3"]))
d2 = Document(DOC)
ok = 0
for p in d2.paragraphs:
    pPr = p._p.find(qn("w:pPr"))
    if pPr is not None and pPr.find(qn("w:outlineLvl")) is not None:
        ok += 1
print("复核：带大纲级别的段落 %d 个" % ok)
print("段落 %d / 表格 %d" % (len(d2.paragraphs), len(d2.tables)))
