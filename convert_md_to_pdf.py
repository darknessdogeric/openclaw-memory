import subprocess
import os

# 获取当前目录
base_dir = r'C:\Users\Administrator\Desktop\张实项目总控\06-AHL-去中心化旅行平台'

# 文件列表
files = [
    '01-政府申请-项目说明书.md',
    '02-商业计划书-投资人版.md', 
    '03-用户说明书与取费标准.md',
    '04-团队分享汇报材料.md'
]

print('开始转换Markdown为PDF...')
print('='*50)

for md_file in files:
    md_path = os.path.join(base_dir, md_file)
    pdf_file = md_file.replace('.md', '.pdf')
    pdf_path = os.path.join(base_dir, pdf_file)
    
    if os.path.exists(md_path):
        print(f'\n正在转换: {md_file}')
        try:
            # 使用pandoc转换
            cmd = [
                'pandoc',
                md_path,
                '-o', pdf_path,
                '--pdf-engine=xelatex',
                '-V', 'CJKmainfont=SimHei',
                '-V', 'geometry:margin=2cm',
                '--toc'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f'✅ 成功生成: {pdf_file}')
            else:
                print(f'❌ 转换失败: {result.stderr}')
                print('尝试备用方案...')
                
                # 备用：先生成HTML
                html_file = md_file.replace('.md', '.html')
                html_path = os.path.join(base_dir, html_file)
                
                import markdown
                with open(md_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
                
                html_with_style = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{md_file.replace('.md', '')}</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; font-size: 28px; }}
        h2 {{ color: #34495e; border-left: 4px solid #3498db; padding-left: 10px; margin-top: 30px; font-size: 22px; }}
        h3 {{ color: #7f8c8d; margin-top: 20px; font-size: 18px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; font-size: 14px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #3498db; color: white; font-weight: bold; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        code {{ background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        blockquote {{ border-left: 4px solid #3498db; padding-left: 15px; color: #555; margin: 15px 0; }}
        ul, ol {{ margin: 10px 0; padding-left: 30px; }}
        li {{ margin: 5px 0; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>'''
                
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_with_style)
                print(f'📄 已生成HTML: {html_file}')
                print(f'💡 请用浏览器打开HTML，打印为PDF')
                
        except Exception as e:
            print(f'❌ 错误: {str(e)}')
    else:
        print(f'❌ 文件不存在: {md_file}')

print('\n' + '='*50)
print('转换完成！')
print('\n如果PDF未生成，请使用以下方法：')
print('1. 打开生成的HTML文件')
print('2. 按Ctrl+P打开打印对话框')
print('3. 选择"另存为PDF"')
print('4. 保存即可')
