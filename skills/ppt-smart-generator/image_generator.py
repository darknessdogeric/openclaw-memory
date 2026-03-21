# -*- coding: utf-8 -*-
"""
PPT智能生成器 - 配图生成模块
模拟AI生图接口，实际使用可接入真实API
"""
import os
import json
import random
import hashlib
from datetime import datetime

class ImageGenerator:
    """AI配图生成器（模拟版）"""
    
    # 预定义图片主题和风格
    THEMES = {
        "business": [
            "modern office building", "business meeting", "handshake deal",
            "corporate team", "presentation", "office interior",
            "business person working", "skyscraper view", "meeting room"
        ],
        "tech": [
            "technology abstract", "AI brain network", "digital circuit",
            "server room", "coding screen", "innovation concept",
            "robot hand", "data visualization", "cyber security"
        ],
        "illustration": [
            "flat design illustration", "business cartoon", "startup team drawing",
            "isometric office", "minimalist graphic", "vector art business"
        ],
        "nature": [
            "landscape mountains", "ocean view", "sunrise horizon",
            "forest trees", "blue sky clouds", "peaceful nature"
        ],
        "abstract": [
            "abstract geometric shapes", "gradient color background",
            "modern art pattern", "minimalist design", "colorful abstraction"
        ]
    }
    
    COLORS = {
        "blue": ["#1e40af", "#3b82f6", "#06b6d4"],
        "gold": ["#d4af37", "#f59e0b", "#fbbf24"],
        "purple": ["#7c3aed", "#a855f7", "#8b5cf6"],
        "green": ["#10b981", "#34d399", "#059669"],
        "red": ["#ef4444", "#f87171", "#dc2626"]
    }
    
    def __init__(self, output_dir="ppt_output/images"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_image_prompt(self, slide_title, slide_content, style="business"):
        """
        根据幻灯片内容生成图片提示词
        """
        # 提取关键词
        keywords = self._extract_keywords(slide_title + " " + slide_content)
        
        # 选择主题
        theme_pool = self.THEMES.get(style, self.THEMES["business"])
        base_theme = random.choice(theme_pool)
        
        # 构建提示词
        prompt = f"{base_theme}, "
        if keywords:
            prompt += f"with {', '.join(keywords[:3])}, "
        prompt += "high quality, professional, 16:9 aspect ratio"
        
        return prompt
    
    def _extract_keywords(self, text):
        """提取关键词"""
        keyword_map = {
            "团队": "team", "办公": "office", "技术": "technology",
            "数据": "data", "创新": "innovation", "发展": "growth",
            "全球": "global", "市场": "market", "产品": "product",
            "服务": "service", "客户": "customer", "合作": "partnership"
        }
        
        found = []
        for cn, en in keyword_map.items():
            if cn in text:
                found.append(en)
        return found
    
    def generate_images(self, outline, style="business", count_per_section=1):
        """
        为大纲的每个章节生成配图
        """
        results = []
        
        for section in outline.get("sections", []):
            slide_num = section.get("num", 0)
            title = section.get("title", "")
            content = section.get("content", "")
            
            # 生成提示词
            prompt = self.generate_image_prompt(title, content, style)
            
            # 模拟生成图片（实际应调用AI生图API）
            # 这里创建占位符和元数据
            image_info = {
                "slide_num": slide_num,
                "title": title,
                "prompt": prompt,
                "style": style,
                "status": "placeholder",  # 实际应为 "generated"
                "path": None,  # 实际生成后填充
                "generated_at": datetime.now().isoformat()
            }
            
            results.append(image_info)
        
        return results
    
    def save_image_manifest(self, images, filename="image_manifest.json"):
        """保存图片清单"""
        manifest_path = os.path.join(self.output_dir, filename)
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(images, f, ensure_ascii=False, indent=2)
        return manifest_path
    
    def generate_placeholder_svg(self, slide_num, title, style="business"):
        """
        生成SVG占位图（当无法调用AI时使用）
        """
        color = random.choice(list(self.COLORS.values()))
        bg_color = color[0]
        
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="{bg_color}"/>
  <text x="50%" y="45%" font-family="Arial" font-size="48" 
        fill="white" text-anchor="middle" opacity="0.3">
    Slide {slide_num}
  </text>
  <text x="50%" y="55%" font-family="Arial" font-size="32" 
        fill="white" text-anchor="middle" opacity="0.5">
    {title}
  </text>
</svg>'''
        
        filename = f"slide_{slide_num:02d}_{title[:10]}.svg"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg)
        
        return filepath


def generate_for_outline(outline, style="business"):
    """为大纲生成配图的入口函数"""
    gen = ImageGenerator()
    images = gen.generate_images(outline, style)
    
    # 生成SVG占位图
    for img in images:
        path = gen.generate_placeholder_svg(img["slide_num"], img["title"], style)
        img["path"] = path
    
    # 保存清单
    manifest = gen.save_image_manifest(images)
    
    return {
        "images": images,
        "manifest": manifest,
        "count": len(images)
    }


if __name__ == "__main__":
    # 测试
    test_outline = {
        "sections": [
            {"num": 1, "title": "封面", "content": "项目介绍"},
            {"num": 2, "title": "团队", "content": "核心成员"},
            {"num": 3, "title": "产品", "content": "服务内容"}
        ]
    }
    result = generate_for_outline(test_outline, "tech")
    print(f"Generated {result['count']} image prompts")
    print(f"Manifest: {result['manifest']}")
