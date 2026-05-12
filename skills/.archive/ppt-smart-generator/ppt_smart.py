# -*- coding: utf-8 -*-
"""
PPT智能生成器 - 主程序
AI大纲规划 + 配图生成 + PPT组装
"""
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
import argparse
import json
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from outline_planner import plan_outline, OutlinePlanner
from image_generator import generate_for_outline, ImageGenerator
from ppt_assembler import assemble_ppt, TEMPLATES


class PPTSmartGenerator:
    """PPT智能生成器主类"""
    
    def __init__(self, output_dir="ppt_output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.outline = None
        self.images = []
        self.manifest = {}
    
    def generate(self, content, 
                 slides_count=10,
                 template="premium",
                 image_style="business",
                 output_name=None):
        """
        完整生成流程
        1. AI分析内容，规划大纲
        2. 生成配图提示词
        3. 组装PPT
        """
        print("=" * 50)
        print("PPT智能生成器")
        print("=" * 50)
        
        # Step 1: AI大纲规划
        print("\n[1/3] AI分析内容，规划大纲...")
        self.outline = plan_outline(content, slides_count)
        print(f"  ✓ 生成 {len(self.outline['sections'])} 页大纲")
        print(f"  ✓ 风格: {self.outline.get('style', 'general')}")
        print(f"  ✓ 主题色: {self.outline.get('color_theme', 'default')}")
        
        # Step 2: 配图生成
        print("\n[2/3] 生成配图...")
        img_result = generate_for_outline(self.outline, image_style)
        self.images = img_result["images"]
        print(f"  ✓ 生成 {len(self.images)} 张配图提示词")
        print(f"  ✓ 清单保存至: {img_result['manifest']}")
        
        # Step 3: 组装PPT
        print("\n[3/3] 组装PPT...")
        
        # 生成文件名
        if not output_name:
            output_name = f"PPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        output_path = os.path.join(self.output_dir, f"{output_name}.pptx")
        
        assemble_ppt(
            self.outline, 
            self.images,
            template=template,
            output=output_path
        )
        print(f"  ✓ PPT已保存: {output_path}")
        
        # 保存元数据
        self.manifest = {
            "generated_at": datetime.now().isoformat(),
            "outline": self.outline,
            "images": self.images,
            "template": template,
            "image_style": image_style,
            "output": output_path
        }
        
        manifest_path = os.path.join(self.output_dir, f"{output_name}_manifest.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(self.manifest, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 50)
        print("生成完成!")
        print("=" * 50)
        
        return {
            "outline": self.outline,
            "images": self.images,
            "output": output_path,
            "manifest": manifest_path
        }
    
    def preview_outline(self):
        """预览大纲"""
        if not self.outline:
            print("请先生成PPT")
            return
        
        print(f"\n{'='*40}")
        print(f"大纲预览: {self.outline.get('title')}")
        print(f"{'='*40}")
        
        for s in self.outline.get("sections", []):
            print(f"  {s['num']:2d}. {s['title']}")
            print(f"      {s['content'][:40]}...")
        print()


def main():
    parser = argparse.ArgumentParser(description="PPT智能生成器")
    parser.add_argument("content", nargs="?", help="PPT内容（文本或文件路径）")
    parser.add_argument("-t", "--template", default="premium", 
                       choices=list(TEMPLATES.keys()),
                       help="模板风格")
    parser.add_argument("-s", "--style", default="business",
                       choices=["business", "tech", "illustration", "nature", "abstract"],
                       help="配图风格")
    parser.add_argument("-o", "--output", help="输出文件名")
    parser.add_argument("-c", "--slides", type=int, default=10, help="幻灯片数量")
    parser.add_argument("--preview", action="store_true", help="仅预览大纲")
    
    args = parser.parse_args()
    
    # 内容
    if args.content:
        # 如果是文件，读取内容
        if os.path.isfile(args.content):
            with open(args.content, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = args.content
    else:
        # 默认示例内容
        content = """
        AHL去中心化住宿业交易生态协议
        项目概述：构建全球首个基于大语言模型的去中心化住宿业交易生态协议
        从货架经济向客户经济的范式革命
        行业痛点：OTA垄断佣金20-30%，年损失1200亿，匹配转化率<3%
        解决方案：双AGENT+多SKILL架构，效率费3-5%，向量匹配准确率95%+
        技术架构：C端AI管家+B端AI运营官，9大AGENT×87个SKILL
        申请支持：算力800万/年，场地108万，设备575万
        四年规划：Phase1协议研发，Phase2矩阵建设，Phase3生态规模化，Phase4全球化
        团队：张实24年酒店业经验，CTO待补充，CSO待补充
        """
    
    # 生成
    generator = PPTSmartGenerator()
    
    if args.preview:
        # 仅预览大纲
        outline = plan_outline(content, args.slides)
        print(json.dumps(outline, ensure_ascii=False, indent=2))
    else:
        # 完整生成
        result = generator.generate(
            content,
            slides_count=args.slides,
            template=args.template,
            image_style=args.style,
            output_name=args.output
        )
        
        print(f"\n📄 输出文件: {result['output']}")
        print(f"📋 大纲预览:")
        for s in result['outline']['sections'][:5]:
            print(f"   {s['num']}. {s['title']}")


if __name__ == "__main__":
    main()
