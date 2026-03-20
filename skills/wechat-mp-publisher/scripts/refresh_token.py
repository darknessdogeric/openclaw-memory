#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强制刷新access_token
"""

import requests
import yaml
from pathlib import Path
import time

config_path = Path(__file__).parent.parent / "config.yaml"

with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

app_id = config['wechat_mp']['app_id']
app_secret = config['wechat_mp']['app_secret']

# 强制获取新token
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
    expires_in = data.get('expires_in', 7200)
    
    # 更新配置
    config['wechat_mp']['access_token'] = access_token
    config['wechat_mp']['token_expires_at'] = time.time() + expires_in
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True)
    
    print(f"Token refreshed successfully!")
    print(f"Expires in: {expires_in} seconds")
else:
    print(f"Error: {data}")
