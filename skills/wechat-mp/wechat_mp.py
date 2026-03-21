#!/usr/bin/env python3
"""
微信公众号推送模块
"""

import json
import os
import requests
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")

def load_config():
    """加载配置"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_access_token():
    """获取Access Token"""
    config = load_config()
    app_id = config.get('wechat_mp', {}).get('app_id')
    app_secret = config.get('wechat_mp', {}).get('app_secret')
    
    if not app_id or not app_secret:
        return None, "请先配置 app_id 和 app_secret"
    
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    resp = requests.get(url).json()
    
    if 'access_token' in resp:
        return resp['access_token'], None
    else:
        return None, resp.get('errmsg', '获取token失败')

def send_text(user_id: str, message: str) -> dict:
    """发送文本消息"""
    token, err = get_access_token()
    if err:
        return {"success": False, "error": err}
    
    url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
    data = {
        "touser": user_id,
        "msgtype": "text",
        "text": {"content": message}
    }
    resp = requests.post(url, json=data).json()
    
    if resp.get('errcode') == 0:
        return {"success": True, "message": "发送成功"}
    else:
        return {"success": False, "error": resp.get('errmsg', '发送失败')}

def get_users() -> dict:
    """获取用户列表"""
    token, err = get_access_token()
    if err:
        return {"success": False, "error": err}
    
    url = f"https://api.weixin.qq.com/cgi-bin/user/get?access_token={token}"
    resp = requests.get(url).json()
    
    if 'total' in resp:
        return {"success": True, "total": resp['total'], "users": resp.get('data', {}).get('openid', [])}
    else:
        return {"success": False, "error": resp.get('errmsg', '获取失败')}

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python wechat_mp.py <command> [args]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "send":
        user_id = sys.argv[2] if len(sys.argv) > 2 else ""
        message = sys.argv[3] if len(sys.argv) > 3 else ""
        result = send_text(user_id, message)
        print(json.dumps(result, ensure_ascii=False))
    elif cmd == "list":
        result = get_users()
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Unknown command: {cmd}")
