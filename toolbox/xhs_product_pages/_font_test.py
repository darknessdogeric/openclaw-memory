"""字体渲染测试 - 找出哪个字体缺字"""
from PIL import Image, ImageDraw, ImageFont

W, H = 2000, 600
img = Image.new('RGB', (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)

fonts = {
    'SourceHanSerifHeavy': r'C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf',
    'NotoSansRegular':     r'C:\Windows\Fonts\Noto Sans SC (TrueType).otf',
    'NotoSansBold':        r'C:\Windows\Fonts\Noto Sans SC Bold (TrueType).otf',
    'NotoSansMedium':      r'C:\Windows\Fonts\Noto Sans SC Medium (TrueType).otf',
    'NotoSansVF':          r'C:\Windows\Fonts\NotoSansSC-VF.ttf',
}

# 测试字串（含可能的难字）
text = "独立酒店境外市场拓展指南困多久是问题跨境实战ERIC出品"

x = 20
for name, path in fonts.items():
    f = ImageFont.truetype(path, 28)
    d.text((x, 20), f"{name}:", fill=(0,0,0), font=f)
    d.text((x, 60), text, fill=(0,0,0), font=f)
    x += 400

img.save(r'D:\B166ER-OpenClaw\workspace\output\小红书商品图_独立酒店境外市场拓展指南\_font_test.png')
print("测试图保存")