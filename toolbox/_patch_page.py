# -*- coding: utf-8 -*-
"""修 page()：顶层块切分 + 块内自平衡 + 结构断言（poster 直接子元素必须为 3）"""
import io, os, re, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MK = r'D:\B166ER-openclaw\workspace\toolbox\_mk_xhs9_light.py'
t = open(MK, encoding='utf-8').read()

NEW_PAGE = '''
def _balance_one(frag):
    """单个块内补齐缺失的 </div>（补在块末）"""
    depth = 0
    extra = []
    for m in re.finditer(r'<div\\b[^>]*>|</div>', frag):
        if m.group(0) != '</div>':
            depth += 1
        else:
            if depth > 0:
                depth -= 1
            else:
                extra.append(m.start())
    fixed = frag
    for s in sorted(extra, reverse=True):
        fixed = fixed[:s] + fixed[s + 6:]
    if depth > 0:
        fixed = fixed + "</div>" * depth
    return fixed


def _split_top(frag):
    """把 main 内容按顶层 div 切块，每块自平衡后再拼回"""
    spans = []
    depth = 0
    start = 0
    for m in re.finditer(r'<div\\b[^>]*>|</div>', frag):
        if m.group(0) != '</div>':
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                spans.append((start, m.end()))
    if not spans:
        return frag
    out = [frag[:spans[0][0]]]
    for s, e in spans:
        out.append(_balance_one(frag[s:e]))
    out.append(frag[spans[-1][1]:])
    return "".join(out)


def page(meta, main):
    body = _split_top(main)
    return ("<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><title>" + meta + "</title><style>"
            + CSS + "</style></head><body><div class='poster'>"
            + "<div class='top'>" + BTOP + "<div class='meta'>" + meta + "</div></div>"
            + "<div class='main'>" + body + "</div>"
            + "<div class='bottom'><div class='stamp'>酒店 · 财务 · 工具</div>" + BBOT + "</div>"
            + "</div></body></html>")

'''

# 替换旧的 page() 定义
old_page_start = t.find("def page(meta, main):")
if old_page_start < 0:
    print('!! 未找到 page() 定义')
    sys.exit(1)
old_page_end = t.find("\n\n", t.find("+ \"</div></body></html>\")", old_page_start))
t = t[:old_page_start] + NEW_PAGE.strip("\n") + t[old_page_end:]

# 删除旧的 balance()（整页级），保留结构修复在 page() 里
bs = t.find("def balance(html):")
if bs > 0:
    be = t.find("\nfor _k in list(P.keys()):", bs)
    t = t[:bs] + t[be + 1:]

# 写文件前断言 poster 直接子元素 = 3
ANCH = "for k, v in P.items():\n    open(os.path.join(HTMLD, k + \".html\")"
ASSERT = '''
def _check_structure(html):
    """校验 .poster 的直接子元素必须是 top / main / bottom 三个"""
    m = re.search(r"<div class='poster'>(.*)</div></body>", html, re.S)
    if not m:
        return "poster 未找到"
    inner = m.group(1)
    depth = 0
    kids = 0
    for t2 in re.finditer(r'<div\\b[^>]*>|</div>', inner):
        if t2.group(0) != '</div>':
            if depth == 0:
                kids += 1
            depth += 1
        else:
            depth -= 1
    return "poster直接子元素=%d(应为3)" % kids


for _k in list(P.keys()):
    _st = _check_structure(P[_k])
    if _st != "poster直接子元素=3(应为3)":
        print("  !! 结构异常 " + _k + ": " + _st)

'''
if ANCH in t:
    t = t.replace(ANCH, ASSERT + ANCH, 1)
    open(MK, 'w', encoding='utf-8').write(t)
    print('生成器：page() 已重写（顶层块切分＋块内自平衡）＋结构断言已加')
else:
    print('!! 写文件锚点未命中')
