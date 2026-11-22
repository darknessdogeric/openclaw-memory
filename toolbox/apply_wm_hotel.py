import sys, os
sys.path.insert(0, 'toolbox')
from watermark_tool import protect_output, verify_output

src = 'toolbox/hotel_benchmark.png'
wm  = protect_output(src)
print('Watermarked file :', wm)
print('Size            :', os.path.getsize(wm), 'bytes')
print('Extract verify  :', verify_output(wm))
