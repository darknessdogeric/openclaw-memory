from PIL import Image
import numpy as np
import os

bg = np.array([242, 237, 227])
slides = sorted([f for f in os.listdir('.') if f.endswith('_wm.png')])

print(f'{"file":<40} {"content_bottom(retina)":<26} {"=design":<10} {"watermark(retina)":<22} {"=design":<10}')
print('-' * 120)
for f in slides:
    img = np.array(Image.open(f).convert('RGB'))
    H, W, _ = img.shape

    # 主体内容最底部（非背景像素）
    not_bg = np.abs(img.astype(int) - bg).sum(axis=2) > 20
    ys, _ = np.where(not_bg)
    content_bottom = H - ys.max() if len(ys) > 0 else 0

    # 水印位置（深墨蓝矩形）
    deep = np.abs(img.astype(int) - np.array([26, 31, 58])).sum(axis=2) < 40
    br = deep[-500:, -800:]
    ys_br, _ = np.where(br)
    wm_bottom = 500 - ys_br.max() if len(ys_br) > 0 else None

    # 原图设计 = retina / 2
    content_orig = content_bottom / 2
    wm_orig = wm_bottom / 2 if wm_bottom else 0

    print(f'{f:<40} {content_bottom:<26} {content_orig:<10.1f} {str(wm_bottom):<22} {wm_orig:<10.1f}')