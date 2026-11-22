import re
fp = r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\examples\build_sichuan_hotel_1f.py'
text = open(fp, encoding='utf-8').read()
text = re.sub(r"doc\.layers\.add\('AXIS',", "doc.layers.add('MYAXIS',", text)
text = re.sub(r"doc\.layers\.add\('wall',", "doc.layers.add('MYWALL',", text)
text = re.sub(r"doc\.layers\.add\('text',", "doc.layers.add('MYTEXT',", text)
text = re.sub(r"doc\.layers\.add\('dim',", "doc.layers.add('MYDIM',", text)
open(fp, 'w', encoding='utf-8').write(text)
print('done')

# Also list existing layers
import sys
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\scripts')
from core.document import CADDocument
from layer.manager import LayerManager
doc = CADDocument.new()
LayerManager(doc).setup_template('arch')
print('existing layers:')
for l in doc.layers:
    print(' ', l.dxf.name)