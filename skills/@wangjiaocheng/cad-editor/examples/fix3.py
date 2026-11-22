import re
fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()
# Just do a final unified fix
# Pattern 1: doc.layers.add('X', 'color': N  → doc.layers.add('X', color=N)
text = re.sub(r"doc\.layers\.add\('(\w+)', 'color': (\d+)\s*\)",
              r"doc.layers.add('\1', color=\2)", text)
# Pattern 2: dict 'color' key inside dxfattribs - need quotes
text = re.sub(r"dxfattribs=\{'layer': '(\w+)', color=(\d+)\}",
              r"dxfattribs={'layer': '\1', 'color': \2}", text)
# Pattern 3: dict 'color' inside dxfattribs (no layer)
text = re.sub(r"dxfattribs=\{'(\w+)', color=(\d+)\}",
              r"dxfattribs={'\1', 'color': \2}", text)
# Pattern 4: kwargs - remove quotes around color
# Match ', 'color': N)' when not preceded by quote + comma + curly
text = re.sub(r", 'color': (\d+)\)", r", color=\1)", text)
# Restore dxfattribs color quotes
text = re.sub(r"(dxfattribs=\{[^}]*?)color=(\d+)\}", lambda m: m.group(1) + f"'color': {m.group(2)}" + "}", text)

open(fp, 'w', encoding='utf-8').write(text)
lines = open(fp, encoding='utf-8').readlines()
for i in [41, 63, 117, 118]:
    print(f'{i+1}: {lines[i].rstrip()}')