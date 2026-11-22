import os, shutil
src = r'D:\Users\ericz\Desktop\产业发展部\AHL项目\AHL_小红书12图'
print('exists:', os.path.exists(src))
if not os.path.exists(src):
    raise SystemExit(1)

# 把刚才复制过去的 7 张麦肯锡图重命名
for i in range(1, 8):
    src_file = os.path.join(src, f'ahl_xhs_{i:02d}.png')
    dst_file = os.path.join(src, f'ahl_mckinsey_{i:02d}.png')
    if os.path.exists(src_file):
        shutil.move(src_file, dst_file)
        print(f'Moved: {src_file} -> {dst_file}')

# 把原 v1 的 12 张图（深空科技风）重命名避免混淆
for i in range(1, 13):
    src_file = os.path.join(src, f'ahl_xhs_{i:02d}.png')
    if os.path.exists(src_file):
        dst_file = os.path.join(src, f'ahl_darkspace_{i:02d}.png')
        shutil.move(src_file, dst_file)
        print(f'Moved: {src_file} -> {dst_file}')

# 最终列表
print('\n=== Final layout ===')
files = sorted([f for f in os.listdir(src) if f.endswith('.png')])
for f in files:
    p = os.path.join(src, f)
    print(f'  {f} ({os.path.getsize(p)//1024} KB)')
print(f'\nTotal: {len(files)} PNG files')
