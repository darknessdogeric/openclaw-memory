import pandas as pd
import glob
import os

base_path = r'C:\Users\Administrator\Desktop'
target_dirs = glob.glob(base_path + r'\*项目总控*\*AHL*\*苏州*\项目场景')

if target_dirs:
    path = target_dirs[0] + '\\'
    print(f"Found path: {path}")
else:
    path = None
    print("Path not found")

if path:
    files = glob.glob(path + '*.xlsx')
    print(f"Found {len(files)} files")
    
    output = []
    for i, f in enumerate(files):
        output.append(f"\n{'='*60}")
        output.append(f"File {i+1}: {os.path.basename(f)}")
        output.append('='*60)
        try:
            xl = pd.ExcelFile(f)
            output.append(f"Sheets: {xl.sheet_names}")
            for sheet in xl.sheet_names[:3]:
                output.append(f"\n--- Sheet: {sheet} ---")
                df = pd.read_excel(f, sheet_name=sheet)
                output.append(f"Shape: {df.shape}")
                output.append(df.head(30).to_string())
                output.append("\n")
        except Exception as e:
            output.append(f"Error: {e}")
    
    with open('suzhou_project_content.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print("Saved to suzhou_project_content.txt")
