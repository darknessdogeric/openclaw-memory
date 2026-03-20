#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试微信公众号API
"""

import requests
import sys
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

if 'access_token' in data:
    access_token = data['access_token']
    print(f"Access Token: {access_token[:20]}...")
    
    # 测试创建草稿 - 最简单的形式
    draft_url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    # 先测试上传一张图片作为封面
    # 创建一个简单的测试图片或跳过封面
    
    draft_data = {
        "articles": [
            {
                "title": "测试文章",
                "author": "B166ER",
                "digest": "测试摘要",
                "content": "<p>这是一篇测试文章</p>",
                "content_source_url": "",
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }
        ]
    }
    
    response = requests.post(draft_url, json=draft_data, timeout=30)
    result = response.json()
    print(f"Draft result: {result}")
    
else:
    print(f"Error: {data}")
    sys.exit(1)
