#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传封面图片到微信公众号
"""

import requests
from pathlib import Path
import yaml

# 读取配置
config_path = Path(__file__).parent.parent / "config.yaml"
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

app_id = config['wechat_mp']['app_id']
app_secret = config['wechat_mp']['app_secret']

# 获取access_token
url = "https://api.weixin.qq.com/cgi-bin/token"
params = {
    "grant_type": "client_credential",
    "appid": app_id,
    "secret": app_secret
}

response = requests.get(url, params=params, timeout=30)
data = response.json()

if 'access_token' not in data:
    print(f"Error getting token: {data}")
    exit(1)

access_token = data['access_token']
print(f"Access Token OK")

# 上传永久图片素材
# 先创建一个简单的测试图片
from PIL import Image, ImageDraw, ImageFont

# 创建一个简单的封面图
img = Image.new('RGB', (900, 500), color=(70, 130, 180))
draw = ImageDraw.Draw(img)

# 添加文字
try:
    font = ImageFont.truetype("arial.ttf", 40)
except:
    font = ImageFont.load_default()

draw.text((300, 220), "B166ER Diary", fill=(255, 255, 255), font=font)

# 保存图片
image_path = Path(__file__).parent.parent / "assets" / "default_cover.jpg"
image_path.parent.mkdir(exist_ok=True)
img.save(image_path)
print(f"Cover image created: {image_path}")

# 上传图片
upload_url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"

with open(image_path, 'rb') as f:
    files = {'media': f}
    response = requests.post(upload_url, files=files, timeout=30)
    result = response.json()
    
    print(f"Upload result: {result}")
    
    if 'media_id' in result:
        print(f"Image uploaded successfully!")
        print(f"Media ID: {result['media_id']}")
        print(f"URL: {result.get('url', 'N/A')}")
        
        # 保存media_id到配置
        config['wechat_mp']['default_cover_media_id'] = result['media_id']
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True)
        print(f"Media ID saved to config")
    else:
        print(f"Upload failed: {result}")
