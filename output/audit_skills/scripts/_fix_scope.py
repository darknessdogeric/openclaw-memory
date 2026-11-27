# -*- coding: utf-8 -*-
import io, sys, os, re, ast
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
P = os.path.join(ROOT,"skills","tool-index-builder","scripts","build_tool_index.py")
t = open(P, encoding="utf-8", errors="replace").read()

# 1) classify() 多返回 embedded_id
old_ret = '''    if oneoff or dated or embedded_id:
        cat = "oneoff_family"
    elif has_doc:
        cat = "capability"
    else:
        cat = "orphan"
    return cat, purpose, has_doc, hit_kw[:6]'''
new_ret = '''    if oneoff or dated or embedded_id:
        cat = "oneoff_family"
    elif has_doc:
        cat = "capability"
    else:
        cat = "orphan"
    return cat, purpose, has_doc, hit_kw[:6], embedded_id'''
assert old_ret in t, "classify 返回段未命中"
t = t.replace(old_ret, new_ret, 1)

# 2) main() 解包 5 个值
old_call = '''        cat, purpose, has_doc, kw = classify(b, head, owner)'''
new_call = '''        cat, purpose, has_doc, kw, embedded_id = classify(b, head, owner)'''
assert old_call in t, "classify 调用未命中"
t = t.replace(old_call, new_call, 1)

ast.parse(t)
open(P,"w",encoding="utf-8",newline="\n").write(t)
print("✔ 已修：classify 返回 embedded_id，main 正确解包")
