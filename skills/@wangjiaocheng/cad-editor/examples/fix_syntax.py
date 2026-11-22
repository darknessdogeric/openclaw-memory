import re
fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()

# Fix 1: doc.layers.add(...) - color should be kwarg, not dict key
text = re.sub(r"doc\.layers\.add\('(\w+)', 'color': (\d+)\)", r"doc.layers.add('\1', color=\2)", text)

# Fix 2: dxfattribs={... color=N} - 'color' should be dict key
text = re.sub(r"dxfattribs=\{'(\w+)', color=(\d+)\}", r"dxfattribs={'\1', 'color': \2}", text)
text = re.sub(r"dxfattribs=\{layer='(\w+)', color=(\d+)\}", r"dxfattribs={'layer': '\1', 'color': \2}", text)

# Fix 3: kwargs 'color' should be color=
text = re.sub(r"thickness=(\d+), 'color': (\d+)\)", r"thickness=\1, color=\2)", text)

open(fp, 'w', encoding='utf-8').write(text)
print('done')
# Show line 42 and 64 for verification
lines = open(fp, encoding='utf-8').readlines()
for i in [41, 63, 117, 118]:
    print(f'{i+1}: {lines[i].rstrip()}')