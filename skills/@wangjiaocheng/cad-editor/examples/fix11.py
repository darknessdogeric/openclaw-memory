fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()
# Direct string replacements
text = text.replace(
    'LinearDimension.horizontal(msp, (x_right, prev), (x_right, y), offset=1500,',
    'LinearDimension.chain_vertical(msp, [(x_right, prev), (x_right, y)], offset=1500,'
)
text = text.replace(
    ", vertical=True)",
    ")"
)
open(fp, 'w', encoding='utf-8').write(text)
print('done')