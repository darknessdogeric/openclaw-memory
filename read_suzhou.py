# -*- coding: utf-8 -*-
import pandas as pd
import glob
import os

# 使用原始字符串避免转义问题
base_path = r'C:\Users\Administrator\Desktop'
# 查找目标文件夹
target_dirs = glob.glob(base_path + r'\*项目总控*\*AHL*\*苏州*\项目场景')

if target_dirs:
    path = target_dirs[0] + '\\'
    print(f"找到路径: {path}")
else:
    # 备用方案
    path = r'C:\Users\Administrator\Desktop\张实项目总控\06-AHL-去中心化旅行平台\苏州酒管公司项目\项目场景\'
    print(f"使用备用路径: {path}")

files = glob.glob(path + '*.xlsx')
print(f"\n找到 {len(files)} 个文件")

output = []
for i, f in enumerate(files):
    output.append(f"\n{'='*60}")
    output.append(f"文件 {i+1}: {os.path.basename(f)}")
    output.append('='*60)
    try:
        xl = pd.ExcelFile(f)
        output.append(f"工作表: {xl.sheet_names}")
        for sheet in xl.sheet_names[:3]:  # 只读前3个工作表避免太长
            output.append(f"\n--- 工作表: {sheet} ---")
            df = pd.read_excel(f, sheet_name=sheet)
            output.append(f"行列: {df.shape}")
            output.append(df.head(30).to_string())
            output.append("\n")
    except Exception as e:
        output.append(f"Error: {e}")

with open('suzhou_project_content.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("\n内容已保存到 suzhou_project_content.txt")
