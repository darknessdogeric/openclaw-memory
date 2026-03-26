# -*- coding: utf-8 -*-
import markdown

with open(r'C:\Users\ericz\.openclaw\workspace\ppt_output\AHL-商业计划书-V3.0-话费模式.md', 'r', encoding='utf-8') as f:
    content = f.read()

html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AHL商业计划书 V3.0 - 话费模式</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#0a0f1a 0%,#1a1f3a 50%,#0d1421 100%);color:#e0e0e0;line-height:1.8;min-height:100vh;padding:40px 20px}
.container{max-width:900px;margin:0 auto}
h1{font-size:2.5em;background:linear-gradient(135deg,#7c3aed,#3b82f6,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:20px;text-align:center}
.subtitle{text-align:center;color:#888;font-size:1.1em;margin-bottom:40px;padding-bottom:20px;border-bottom:1px solid #333}
h2{color:#7c3aed;font-size:1.6em;margin:40px 0 20px;padding-left:15px;border-left:4px solid #7c3aed}
h3{color:#3b82f6;font-size:1.3em;margin:25px 0 15px}
p{margin:12px 0;color:#b0b0b0}
.highlight{background:linear-gradient(135deg,rgba(124,58,237,0.2),rgba(59,130,246,0.2));border-left:4px solid #7c3aed;padding:20px;margin:20px 0;border-radius:0 10px 10px 0}
pre{background:#0d1421;border:1px solid #333;border-radius:10px;padding:15px;margin:15px 0;overflow-x:auto;font-size:0.85em;color:#a0d2db;white-space:pre-wrap}
table{width:100%;border-collapse:collapse;margin:20px 0;background:rgba(26,31,58,0.5)}
th,td{padding:12px;text-align:left;border-bottom:1px solid #333}
th{background:linear-gradient(135deg,#7c3aed,#3b82f6);color:#fff}
tr:hover{background:rgba(124,58,237,0.1)}
.card{background:linear-gradient(135deg,#1a1f3a,#0d1421);border:1px solid #333;border-radius:15px;padding:20px;margin:15px 0}
.card h4{color:#7c3aed;margin-bottom:10px}
.footer{text-align:center;margin-top:60px;padding-top:30px;border-top:1px solid #333;color:#666}
.faq{background:rgba(26,31,58,0.8);border-radius:15px;padding:20px;margin:15px 0}
.faq-q{color:#ec4899;font-weight:bold;margin:15px 0 5px}
.faq-a{color:#b0b0b0;padding-left:20px}
blockquote {border-left:4px solid #ec4899;padding-left:15px;color:#888;font-style:italic;margin:15px 0}
</style>
</head>
<body>
<div class="container">
CONTENT_PLACEHOLDER
<div class="footer">
<p><strong>AHL - AI去中心化旅行服务平台</strong></p>
<p>版本 V3.0 话费模式 | 编制日期: 2026年3月24日</p>
</div>
</div>
</body>
</html>'''

md = markdown.Markdown(extensions=['tables', 'fenced_code'])
html_content = md.convert(content)
html = html_template.replace('CONTENT_PLACEHOLDER', html_content)

with open(r'C:\Users\ericz\.openclaw\workspace\ppt_output\AHL-商业计划书-V3.0-话费模式.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('HTML generated successfully')
