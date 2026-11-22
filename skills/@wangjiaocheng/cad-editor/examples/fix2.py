import re
fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()
# Just replace ALL remaining ', color=N)' with ', 'color': N)' and ', 'color': N)' back to color=N
# Two-pass approach
# First: kwarg `, color=N)` → dict `, 'color': N)` (for inside dxfattribs={})
text = re.sub(r"(\{|,) color=([\d.]+)\)", r"\1 'color': \2", text)
# Then: dict 'color' inside non-dxfattribs context -> remove quotes
# Detect: anything OUTSIDE dxfattribs={} that has ', 'color': N)'
# Easier: just fix the specific patterns we know about
text = text.replace("thickness=200, layer='REFORM', 'color': 1)", "thickness=200, layer='REFORM', color=1)")
text = text.replace("thickness=200, layer='KEEP', color=3)", "thickness=200, layer='KEEP', color=3)")
text = text.replace("thickness=150, layer='KEEP', color=3)", "thickness=150, layer='KEEP', color=3)")
text = text.replace("thickness=240, layer='RENT', color=5)", "thickness=240, layer='RENT', color=5)")
text = text.replace("thickness=240, layer='KEEP', color=3)", "thickness=240, layer='KEEP', color=3)")
# Inside dxfattribs={}, color should be 'color'
text = text.replace("dxfattribs={'layer': 'AXIS_LINE', color=8}",
                   "dxfattribs={'layer': 'AXIS_LINE', 'color': 8}")

open(fp, 'w', encoding='utf-8').write(text)
# Verify
lines = open(fp, encoding='utf-8').readlines()
for i in [41, 63, 117]:
    print(f'{i+1}: {lines[i].rstrip()}')