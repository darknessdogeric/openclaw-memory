import os
from PIL import Image
import numpy as np

OUT_DIR = r'D:\B166ER-OpenClaw\workspace\toolbox\xhs_hotel_9slides_jun2026_v4'
bg = np.array([242, 237, 227])
print(f'{"file":<38} {"bottom_px_retina":<20} {"design_px":<12} {"status":<10}')
print('-' * 90)
for f in sorted(os.listdir(OUT_DIR)):
    if f.endswith('_wm.png'):
        img = np.array(Image.open(os.path.join(OUT_DIR, f)).convert('RGB'))
        H, W, _ = img.shape
        not_bg = np.abs(img.astype(int) - bg).sum(axis=2) > 20
        ys, _ = np.where(not_bg)
        cb = H - ys.max() if len(ys) > 0 else 0
        orig = cb / 2
        status = 'OK' if 20 <= orig <= 80 else ('TIGHT' if orig < 20 else 'LOOSE')
        print(f'{f:<38} {cb:<20} {orig:<12.1f} {status:<10}')
