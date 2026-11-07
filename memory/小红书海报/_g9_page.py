# -*- coding: utf-8 -*-
"""页面装配 — Clean & Minimal: head 固定 / body 撑满均匀分布 / foot 固定"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _g9_lib import CSS


def page(idx, total, kicker, title, sub, body, foot_q="", foot_s=""):
    hcls = "sm" if len(title) > 34 else ""
    head = ['<div class="wrap">', '<div class="head">']
    head.append('<div class="kick">' + kicker + '</div>')
    head.append('<h1 class="' + hcls + '">' + title + '</h1>')
    if sub:
        head.append('<div class="sub">' + sub + '</div>')
    head.append('</div>')
    head.append('<div class="body">' + body + '</div>')
    head.append('<div class="foot">')
    if foot_q:
        head.append('<div class="q">' + foot_q + '</div>')
        head.append('<div class="s">' + foot_s + '</div>')
    head.append('</div>')
    head.append('</div>')
    head.append('<div class="brand"><div class="bn">B</div><div class="bl">B166ER</div></div>')
    head.append('<div class="wm">' + str(idx) + ' / ' + str(total) +
                ' · 酒店分级分类 · 2026-10-31</div>')
    return ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><title>' + kicker +
            '</title><style>' + CSS + '</style></head><body>' + "".join(head) +
            '</body></html>')