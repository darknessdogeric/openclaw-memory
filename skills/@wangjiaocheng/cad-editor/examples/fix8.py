import re
fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()

# Remove all doc.layers.add lines (they conflict with template)
text = re.sub(r"doc\.layers\.add\([^)]*\)\s*\n", "", text)

# Replace layer names: use existing template layers
text = text.replace("'REFORM'", "'wall'")   # wall + color=1 (red)
text = text.replace("'KEEP'", "'wall'")     # wall + color=3 (green)
text = text.replace("'RENT'", "'wall'")     # wall + color=5 (blue)
text = text.replace("'DIM'", "'dimension'")
text = text.replace("'AXIS'", "'axis'")
text = text.replace("'LABEL'", "'text'")
text = text.replace("'MYAXIS'", "'axis'")
text = text.replace("'MYWALL'", "'wall'")
text = text.replace("'MYTEXT'", "'text'")
text = text.replace("'MYDIM'", "'dimension'")

open(fp, 'w', encoding='utf-8').write(text)
print('done')