import re
fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()

# Use a custom circle function with msp.add_circle
text = text.replace(
    "BasicEntities.circle(msp, (x, -1500), 600, layer='axis')",
    "msp.add_circle((x, -1500), 600, dxfattribs={'layer': 'axis'})"
)
text = text.replace(
    "BasicEntities.circle(msp, (x, TOTAL_H+1500), 600, layer='axis')",
    "msp.add_circle((x, TOTAL_H+1500), 600, dxfattribs={'layer': 'axis'})"
)
text = text.replace(
    "BasicEntities.circle(msp, (-1500, y), 600, layer='axis')",
    "msp.add_circle((-1500, y), 600, dxfattribs={'layer': 'axis'})"
)
text = text.replace(
    "BasicEntities.circle(msp, (TOTAL_W+1500, y), 600, layer='axis')",
    "msp.add_circle((TOTAL_W+1500, y), 600, dxfattribs={'layer': 'axis'})"
)

open(fp, 'w', encoding='utf-8').write(text)
print('done')