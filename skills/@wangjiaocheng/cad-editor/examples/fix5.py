fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()

# Simply add closing ) at end of doc.layers.add lines if missing
import re
def add_closing(match):
    return match.group(0) + ')'

text = re.sub(r"doc\.layers\.add\('(\w+)',\s*color=(\d+)\s*$",
              r"doc.layers.add('\1', color=\2)", text, flags=re.MULTILINE)

open(fp, 'w', encoding='utf-8').write(text)
lines = open(fp, encoding='utf-8').readlines()
for i in [41, 42, 43]:
    print(f'{i+1}: {lines[i].rstrip()}')