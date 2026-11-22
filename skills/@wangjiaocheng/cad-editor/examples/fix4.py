import re
fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()

# Fix 1: doc.layers.add - remove quotes around color (it's a kwarg)
text = re.sub(r"doc\.layers\.add\('(\w+)',\s*'color':\s*(\d+)",
              r"doc.layers.add('\1', color=\2", text)

# Fix 2: dxfattribs - add quotes around color key
text = re.sub(r"(dxfattribs=\{[^}]*?),\s*color=(\d+)([^}]*?\})",
              lambda m: m.group(1) + f", 'color': {m.group(2)}" + m.group(3), text)

# Fix 3: kwargs context (outside dxfattribs) - remove quotes
text = re.sub(r"thickness=(\d+),\s*'color':\s*(\d+)\)",
              r"thickness=\1, color=\2)", text)

open(fp, 'w', encoding='utf-8').write(text)

# Verify
lines = open(fp, encoding='utf-8').readlines()
for i in [41, 63, 117, 118, 64]:
    print(f'{i+1}: {lines[i].rstrip()}')