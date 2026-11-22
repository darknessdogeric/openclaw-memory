import re, io
p = "gen_v5_plan.py"
s = io.open(p, encoding="utf-8").read().split("\n")
bad = [334, 353, 381, 392, 407, 421]
for ln in bad:
    i = ln - 1
    t = s[i]
    st = t.lstrip()
    if not st.startswith("'**"):
        continue
    indent = t[:len(t) - len(st)]
    s[i] = indent + "[" + st
io.open(p, "w", encoding="utf-8").write("\n".join(s))
print("patched", len(bad))
