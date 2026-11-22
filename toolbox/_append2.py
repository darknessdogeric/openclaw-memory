import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with io.open('memory/2026-08-07.md', 'a', encoding='utf-8') as f:
    f.write('''
### 🆕 20:20 任务 — 原 PPT 图片分离

- **触发**: Eric 20:20 「我需要把原来的PPT里的图片分离出来。」
- **目标文件**: `C:\\Users\\ericz\\Desktop\\安逸茶山\\250306安逸茶山康养休生谷项目汇报PPT(修)(3).pptx` (45MB)
- **方法**: zipfile 直抽 `ppt/media/` (全量保真) + python-pptx 解析 picture shape (按 slide 关联) 双路径
- **结果**:
  - `toolbox/anyi_pptx_images/raw/` — 100 个原始嵌入资源 (含 SVG 图标)
  - `toolbox/anyi_pptx_images/by_slide/` — 58 张按 slide 关联的实际图片
  - `toolbox/anyi_pptx_images/manifest.csv` — 索引清单
- **验证**: slide 11 实景图 s11_img02.jpg 抽出来是茶田帐篷房实景，完好无损
- **命名规则**: `s{NN}_img{NN}.{ext}` (slide 编号 + 该 slide 内图片序号)
- **脚本**: `toolbox/extract_pptx_images.py` (可复用于其他 PPTX)
''')
print('OK')