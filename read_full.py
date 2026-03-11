import pandas as pd
import glob
import os

base_path = r'C:\Users\Administrator\Desktop'
target_dirs = glob.glob(base_path + r'\*项目总控*\*AHL*\*苏州*\项目场景')

if target_dirs:
    path = target_dirs[0] + '\\'
else:
    path = None

if path:
    files = glob.glob(path + '*.xlsx')
    
    output = []
    for i, f in enumerate(files):
        output.append(f"\n{'='*60}")
        output.append(f"FILE {i+1}: {os.path.basename(f)}")
        output.append('='*60)
        try:
            xl = pd.ExcelFile(f)
            output.append(f"Sheets: {xl.sheet_names}")
            for sheet in xl.sheet_names:
                output.append(f"\n--- Sheet: {sheet} ---")
                df = pd.read_excel(f, sheet_name=sheet)
                output.append(f"Shape: {df.shape}")
                # 读取全部内容
                output.append(df.to_string(index=False))
                output.append("\n" + "="*60)
        except Exception as e:
            output.append(f"Error: {e}")
    
    with open('suzhou_full.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print("Saved to suzhou_full.txt")
