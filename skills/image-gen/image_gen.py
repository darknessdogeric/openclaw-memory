#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ImageGen Skill - AI图像生成技能
支持多种图像生成API：OpenAI DALL-E / Stability AI / 本地Stable Diffusion
"""

import os
import sys
import json
import base64
import requests
from pathlib import Path
from datetime import datetime

class ImageGenerator:
    """AI图像生成器"""
    
    def __init__(self, provider="openai"):
        self.provider = provider
        self.api_keys = self._load_api_keys()
    
    def _load_api_keys(self):
        """加载API密钥"""
        keys_file = Path.home() / '.openclaw' / 'config' / 'image_gen_keys.json'
        if keys_file.exists():
            with open(keys_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def generate_image_openai(self, prompt, size="1024x1024", quality="standard", n=1):
        """使用OpenAI DALL-E生成图像"""
        api_key = self.api_keys.get('openai') or os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            return {"error": "未配置OpenAI API密钥"}
        
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "dall-e-3" if quality == "hd" else "dall-e-2",
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": n
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=120)
            response.raise_for_status()
            result = response.json()
            
            # 下载图像
            images = []
            for i, img_data in enumerate(result.get('data', [])):
                img_url = img_data.get('url')
                if img_url:
                    img_path = self._download_image(img_url, f"openai_{i}")
                    images.append(img_path)
            
            return {
                "success": True,
                "provider": "openai",
                "images": images,
                "prompt": prompt
            }
        except Exception as e:
            return {"error": str(e)}
    
    def generate_image_stability(self, prompt, width=1024, height=1024, cfg_scale=7):
        """使用Stability AI生成图像"""
        api_key = self.api_keys.get('stability') or os.getenv('STABILITY_API_KEY')
        
        if not api_key:
            return {"error": "未配置Stability API密钥"}
        
        url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "image/*"
        }
        
        files = {
            "prompt": (None, prompt),
            "mode": (None, "text-to-image"),
            "width": (None, str(width)),
            "height": (None, str(height)),
            "cfg_scale": (None, str(cfg_scale))
        }
        
        try:
            response = requests.post(url, headers=headers, files=files, timeout=120)
            response.raise_for_status()
            
            # 保存图像
            img_path = self._save_image(response.content, "stability")
            
            return {
                "success": True,
                "provider": "stability",
                "images": [img_path],
                "prompt": prompt
            }
        except Exception as e:
            return {"error": str(e)}
    
    def generate_image_pollinations(self, prompt, width=1024, height=1024, seed=None):
        """使用Pollinations AI（免费，无需API Key）生成图像"""
        # Pollinations是免费的图像生成API
        seed = seed or int(datetime.now().timestamp())
        encoded_prompt = requests.utils.quote(prompt)
        
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true"
        
        try:
            response = requests.get(url, timeout=120)
            response.raise_for_status()
            
            # 保存图像
            img_path = self._save_image(response.content, "pollinations")
            
            return {
                "success": True,
                "provider": "pollinations",
                "images": [img_path],
                "prompt": prompt,
                "seed": seed
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _download_image(self, url, prefix):
        """下载图像"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return self._save_image(response.content, prefix)
        except Exception as e:
            return None
    
    def _save_image(self, content, prefix):
        """保存图像到本地"""
        output_dir = Path.home() / 'Desktop' / 'AI_Generated_Images'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.png"
        filepath = output_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(content)
        
        return str(filepath)
    
    def generate(self, prompt, provider=None, **kwargs):
        """通用生成接口"""
        provider = provider or self.provider
        
        if provider == "openai":
            return self.generate_image_openai(prompt, **kwargs)
        elif provider == "stability":
            return self.generate_image_stability(prompt, **kwargs)
        elif provider == "pollinations":
            return self.generate_image_pollinations(prompt, **kwargs)
        else:
            # 默认使用免费的Pollinations
            return self.generate_image_pollinations(prompt, **kwargs)

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI图像生成工具')
    parser.add_argument('prompt', help='图像描述提示词')
    parser.add_argument('-p', '--provider', choices=['openai', 'stability', 'pollinations'], 
                        default='pollinations', help='图像生成服务提供商')
    parser.add_argument('-s', '--size', default='1024x1024', help='图像尺寸 (如 1024x1024)')
    parser.add_argument('-n', '--num', type=int, default=1, help='生成图像数量')
    
    args = parser.parse_args()
    
    print(f"🎨 正在生成图像...")
    print(f"📝 提示词: {args.prompt}")
    print(f"🔧 提供商: {args.provider}")
    print("-" * 50)
    
    generator = ImageGenerator(args.provider)
    result = generator.generate(args.prompt)
    
    if "error" in result:
        print(f"❌ 生成失败: {result['error']}")
        sys.exit(1)
    else:
        print(f"✅ 生成成功!")
        print(f"📁 保存位置:")
        for img_path in result.get('images', []):
            print(f"   - {img_path}")

if __name__ == '__main__':
    main()
