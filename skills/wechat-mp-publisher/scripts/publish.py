#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章发布流程
整合文章生成和发布功能
"""

import os
import sys
import argparse
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from wechat_api import WeChatMPPublisher

def publish_article_file(article_path):
    """发布指定路径的文章文件"""
    publisher = WeChatMPPublisher()
    
    # 读取文章文件
    try:
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] 读取文章文件失败: {e}")
        return False
    
    # 解析文章标题和内容
    lines = content.split('\n')
    title = ""
    article_content = ""
    
    # 简单解析：第一行是标题（去除#号），后面是内容
    if lines:
        title_line = lines[0].strip()
        if title_line.startswith('#'):
            title = title_line.lstrip('#').strip()
        else:
            title = title_line
        
        article_content = '\n'.join(lines[1:]).strip()
    
    if not title:
        title = "B166ER日记"
    
    print(f"Title: {title}")
    print(f"Content length: {len(article_content)} chars")
    
    # 发布文章
    return publisher.publish_article(
        title=title,
        content=article_content,
        author="B166ER",
        digest=title[:100]
    )

def main():
    parser = argparse.ArgumentParser(description='WeChat MP Publisher')
    parser.add_argument('--file', '-f', help='Article file path')
    parser.add_argument('--test', '-t', action='store_true',
                        help='Test API connection')
    
    args = parser.parse_args()
    
    if args.test:
        # 测试模式
        print("Testing WeChat MP API connection...")
        publisher = WeChatMPPublisher()
        token = publisher.get_access_token()
        if token:
            print("[OK] API connection test passed!")
            return 0
        else:
            print("[ERROR] API connection test failed!")
            return 1
    
    if args.file:
        # 发布指定文件
        if not os.path.exists(args.file):
            print(f"[ERROR] File not found: {args.file}")
            return 1
        
        success = publish_article_file(args.file)
        return 0 if success else 1
    else:
        # 显示帮助
        parser.print_help()
        return 0

if __name__ == "__main__":
    sys.exit(main())
