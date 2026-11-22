fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()
# Replace vertical=True with offset call differently
# Use chain_vertical which takes list of points
text = text.replace(
    "LinearDimension.chain_vertical(msp, [(x_right, prev), (x_right, y)],",
    "LinearDimension.chain_vertical(msp, [(x_right, prev), (x_right, y)],"
)
# Then offset=1500 text=f'..' layer=..) needs no vertical arg
text = text.replace(", offset=1500, text=f'{seg*1000:.0f}', layer='dimension')",
                   ", offset=1500, text=f'{seg*1000:.0f}', layer='dimension')")
open(fp, 'w', encoding='utf-8').write(text)
print('done')
# Show line 205-210
lines = open(fp, encoding='utf-8').readlines()
for i in [200, 201, 202, 203, 204, 205]:
    if i < len(lines):
        print(f'{i+1}: {lines[i].rstrip()}')