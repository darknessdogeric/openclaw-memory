#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章发布脚本
由于API权限限制，文章保存为草稿后需要手动发布
"""

import os
import sys
import yaml
import json
import time
import requests
import re
from pathlib import Path
from datetime import datetime, timedelta

class WeChatMPPublisher:
    """微信公众号发布器"""
    
    def __init__(self):
        self.config_path = Path(__file__).parent.parent / "config.yaml"
        self.config = self._load_config()
        self.app_id = self.config['wechat_mp']['app_id']
        self.app_secret = self.config['wechat_mp']['app_secret']
        self.access_token = self.config['wechat_mp'].get('access_token', '')
        self.token_expires_at = self.config['wechat_mp'].get('token_expires_at', 0)
        self.cover_media_id = self.config['wechat_mp'].get('default_cover_media_id', '')
        
    def _load_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _save_config(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
    
    def get_access_token(self):
        if self.access_token and time.time() < self.token_expires_at - 300:
            return self.access_token
        
        url = f"https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if 'access_token' in data:
                self.access_token = data['access_token']
                expires_in = data.get('expires_in', 7200)
                self.token_expires_at = time.time() + expires_in
                self.config['wechat_mp']['access_token'] = self.access_token
                self.config['wechat_mp']['token_expires_at'] = self.token_expires_at
                self._save_config()
                return self.access_token
            else:
                print(f"Error: {data}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def markdown_to_html(self, markdown_text):
        """Markdown转HTML"""
        lines = markdown_text.split('\n')
        html_lines = []
        in_paragraph = False
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
                continue
            
            # 处理标题
            if line_stripped.startswith('# '):
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
                html_lines.append(f'<h1>{line_stripped[2:]}</h1>')
            elif line_stripped.startswith('## '):
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
                html_lines.append(f'<h2>{line_stripped[3:]}</h2>')
            elif line_stripped.startswith('### '):
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
                html_lines.append(f'<h3>{line_stripped[4:]}</h3>')
            elif line_stripped.startswith('> '):
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
                html_lines.append(f'<blockquote>{line_stripped[2:]}</blockquote>')
            elif line_stripped.startswith('---'):
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
                html_lines.append('<hr>')
            else:
                # 普通段落
                if not in_paragraph:
                    html_lines.append('<p>')
                    in_paragraph = True
                # 处理粗体和斜体
                line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
                line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
                html_lines.append(line)
        
        if in_paragraph:
            html_lines.append('</p>')
        
        return '\n'.join(html_lines)
    
    def create_draft(self, title, content, author="B166ER", digest=""):
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
        
        html_content = self.markdown_to_html(content)
        
        data = {
            "articles": [
                {
                    "title": title,
                    "author": author,
                    "digest": digest if digest else title[:100],
                    "content": html_content,
                    "content_source_url": "",
                    "thumb_media_id": self.cover_media_id,
                    "need_open_comment": 1,
                    "only_fans_can_comment": 0
                }
            ]
        }
        
        try:
            response = requests.post(url, json=data, timeout=30)
            result = response.json()
            
            if 'media_id' in result:
                return result['media_id']
            else:
                print(f"Error: {result}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def publish_article(self, title, content, author="B166ER", digest=""):
        """
        发布文章 - 创建草稿
        由于API权限限制，需要手动在后台发布
        """
        print("=" * 50)
        print("WeChat MP Publisher")
        print("=" * 50)
        print(f"Title: {title}")
        
        # 创建草稿
        media_id = self.create_draft(title, content, author, digest)
        if not media_id:
            print("[ERROR] 创建草稿失败")
            return False
        
        print("[OK] 草稿创建成功！")
        print(f"     Media ID: {media_id}")
        print("\n[INFO] 文章已保存到公众号草稿箱")
        print("[INFO] 请登录公众号后台手动发布")
        print("[INFO] 路径：内容与互动 -> 草稿箱")
        return True
    
    def get_draft_list(self):
        """获取草稿列表"""
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={access_token}"
        data = {
            "offset": 0,
            "count": 20,
            "no_content": 1
        }
        
        try:
            response = requests.post(url, json=data, timeout=30)
            result = response.json()
            
            if 'item' in result:
                return result['item']
            else:
                print(f"Error: {result}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def main():
    publisher = WeChatMPPublisher()
    token = publisher.get_access_token()
    if token:
        print("Token OK")
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
