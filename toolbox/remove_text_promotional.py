# -*- coding: utf-8 -*-
"""
去宣传片截图中的文字 (OCR 检测 + OpenCV inpaint)
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import cv2
import numpy as np
from pathlib import Path
from rapidocr_onnxruntime import RapidOCR

INPUT_DIR = Path(r'C:\Users\ericz\Desktop\产业发展部\旗下酒店\天府山庄\宣传片')
OUTPUT_DIR = INPUT_DIR / 'cleaned'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = sorted([INPUT_DIR / f'psc ({n}).jpg' for n in range(18, 33) if (INPUT_DIR / f'psc ({n}).jpg').exists()])
print(f'找到 {len(files)} 张图片')

def imread_unicode(path):
    return cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)

def imwrite_unicode(path, img):
    cv2.imencode('.jpg', img)[1].tofile(str(path))

engine = RapidOCR()

def to_float(x):
    try: return float(x)
    except: return 0.0

def process_image(path, out_path):
    img = imread_unicode(path)
    if img is None:
        print(f'  [跳过] 无法读取: {path.name}')
        return
    h, w = img.shape[:2]
    # 用 OCR 检测文字
    ocr = engine(str(path))
    texts = ocr[0] if (ocr and ocr[0]) else []
    # 建 mask
    mask = np.zeros((h, w), dtype=np.uint8)
    if texts:
        for r in texts:
            box = r[0]
            x1, y1 = max(0, int(box[0][0]) - 8), max(0, int(box[0][1]) - 8)
            x2, y2 = min(w, int(box[2][0]) + 8), min(h, int(box[2][1]) + 8)
            mask[y1:y2, x1:x2] = 255
        print(f'  {path.name}: OCR 检测到 {len(texts)} 块, inpaint 中...')
    else:
        # fallback: 字幕区 (底部 15%) + 标题区 (顶部 10%)
        mask[int(h*0.85):h, :] = 255
        mask[:int(h*0.10), :] = 255
        print(f'  {path.name}: OCR 无结果, 用底/顶 fallback')
    # 膨胀 (覆盖边缘)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    # Inpaint
    result = cv2.inpaint(img, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
    imwrite_unicode(out_path, result)
    return len(texts)

# 处理
print('=' * 60)
total = 0
for f in files:
    out = OUTPUT_DIR / f.name
    n = process_image(f, out)
    total += (n or 0)
print('=' * 60)
print(f'完成. 输出目录: {OUTPUT_DIR}')
print(f'总 OCR 文字块: {total}')
