# -*- coding: utf-8 -*-
"""
Design Studio → PPT 设计提案生成器
将设计概念包转换为可演示的PPT
"""
import sys, os, time, json
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUTPUT_DIR = ROOT / "output"

def generate_ppt_content(project_type, location, scale, style, concepts=None):
    """
    生成PPT内容JSON (用于ppt-deck-builder-pro)
    返回可直接输入ppt-deck-builder的plan结构
    """
    if concepts is None:
        concepts = {}
    
    slides = []
    
    # Slide 1: 封面
    slides.append({
        "type": "cover",
        "title": f"{location}{project_type}",
        "subtitle": f"设计概念提案 | {style}风格",
        "date": time.strftime("%Y年%m月"),
        "meta": f"规模: {scale}"
    })
    
    # Slide 2: 项目概览
    slides.append({
        "type": "content",
        "title": "项目概览",
        "bullets": [
            f"项目类型: {project_type}",
            f"地理位置: {location}",
            f"项目规模: {scale}",
            f"设计风格: {style}",
            f"设计阶段: 概念方案",
        ]
    })
    
    # Slide 3: 设计理念
    slides.append({
        "type": "content",
        "title": "设计理念",
        "bullets": [
            f"以{style}设计语言回应{location}的自然与人文环境",
            "强调空间体验的序列感和到达感",
            "自然材料与现代构造的对话",
            "室内外空间的无缝连接",
            "可持续发展的被动式设计策略",
        ]
    })
    
    # Slide 4: 建筑概念
    slides.append({
        "type": "image_text",
        "title": "建筑外观概念",
        "image_placeholder": "[建筑外观渲染图]",
        "text": f"采用{style}建筑语言，{_get_style_desc(style)}。立面以{_get_material_desc(style)}为主，营造与自然和谐共生的建筑形态。"
    })
    
    # Slide 5: 大堂概念
    slides.append({
        "type": "image_text",
        "title": "大堂空间概念",
        "image_placeholder": "[大堂室内渲染图]",
        "text": "大堂作为到达体验的核心，强调空间的开阔感和仪式感。挑高设计引入自然光，创造令人印象深刻的到达序列。"
    })
    
    # Slide 6: 客房概念
    slides.append({
        "type": "image_text",
        "title": "客房概念",
        "image_placeholder": "[客房渲染图]",
        "text": f"客房以舒适度为第一原则，最大化景观朝向。{style}风格的材质和色调营造宁静雅致的休憩氛围。"
    })
    
    # Slide 7: 平面概念
    slides.append({
        "type": "content",
        "title": "空间规划概念",
        "bullets": [
            "功能分区: 公共区/客房区/后勤区三区独立",
            "动线设计: 客人流线与服务流线完全分离",
            "垂直交通: 核心筒集中布置，高效便捷",
            "朝向策略: 主要功能空间争取最佳景观朝向",
            "弹性设计: 可合并拆分的多功能空间",
        ]
    })
    
    # Slide 8: 立面概念
    slides.append({
        "type": "content",
        "title": "立面与三视图概念",
        "bullets": [
            f"正立面: 强调入口仪式感，{style}比例关系",
            "侧立面: 体量进退创造光影变化",
            "屋顶: 可上人屋顶花园，第五立面设计",
            "材质: 水平线条与垂直元素交错",
        ]
    })
    
    # Slide 9: 材质与色彩
    slides.append({
        "type": "content",
        "title": "材质与色彩策略",
        "bullets": [
            f"主材: {_get_material_desc(style)}",
            "室内: 温暖木材 + 天然石材 + 手工质感",
            "色彩: 基于自然环境提取，克制雅致",
            "照明: 分层照明设计，满足功能与氛围",
        ]
    })
    
    # Slide 10: 下一步
    slides.append({
        "type": "content",
        "title": "下一步工作",
        "bullets": [
            "✅ 概念方案确认",
            "📋 方案深化设计",
            "📋 材料样板确认",
            "📋 初步工程估算",
            "📋 施工图设计启动",
        ]
    })
    
    # Slide 11: 封底
    slides.append({
        "type": "cover",
        "title": "谢谢",
        "subtitle": f"{location}{project_type} 设计概念提案",
        "date": "B166ER Design Studio",
    })
    
    return {
        "template": _get_ppt_template(style),
        "slides": slides,
        "output": f"{location}_{project_type}_设计提案.pptx"
    }

def _get_style_desc(style):
    m = {
        "现代": "简洁几何形态与大面积玻璃幕墙",
        "新中式": "传统建筑元素的当代转译",
        "侘寂": "不完美之美，时间痕迹的价值",
        "生物亲和": "有机曲线形态与自然元素融合",
        "工业": "裸露结构与材料本真的表达",
        "奢华": "精致细节与贵重材料的极致演绎",
        "北欧": "温暖简约与功能美学的平衡",
    }
    return m.get(style, f"{style}建筑设计语言")

def _get_material_desc(style):
    m = {
        "现代": "玻璃、钢材、素混凝土",
        "新中式": "深色木材、青砖、石材",
        "侘寂": "手工涂料、原木、夯土",
        "生物亲和": "木材、石材、绿植墙面",
        "工业": "裸露钢结构、混凝土、金属板",
        "奢华": "大理石、黄铜、丝绒、水晶",
        "北欧": "浅色橡木、白色涂料、天然石材",
    }
    return m.get(style, "木材、石材、玻璃")

def _get_ppt_template(style):
    m = {
        "现代": "minimal_white",
        "新中式": "elegant_chinese",
        "侘寂": "minimal_white",
        "生物亲和": "green_nature",
        "工业": "dark_blue_business",
        "奢华": "luxury_premium",
        "北欧": "light_consulting",
    }
    return m.get(style, "corporate_pro")

def export_plan_json(project_type, location, scale, style):
    """导出PPT plan JSON"""
    plan = generate_ppt_content(project_type, location, scale, style)
    
    # 保存JSON
    fp = OUTPUT_DIR / f"ppt_plan_{location}_{project_type.replace(' ','_')}.json"
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    # 同时生成人类可读的slides大纲
    md_fp = OUTPUT_DIR / f"ppt_outline_{location}_{project_type.replace(' ','_')}.md"
    lines = [f"# {location}{project_type} — 设计提案PPT大纲\n"]
    lines.append(f"**模板**: {plan['template']}")
    lines.append(f"**输出**: {plan['output']}\n")
    for i, slide in enumerate(plan['slides']):
        lines.append(f"## Slide {i+1}: {slide.get('title','')}")
        if slide.get('type') == 'content':
            for b in slide.get('bullets', []):
                lines.append(f"- {b}")
        elif slide.get('type') == 'image_text':
            lines.append(f"图片: {slide.get('image_placeholder','')}")
            lines.append(f"文字: {slide.get('text','')}")
        lines.append("")
    
    with open(md_fp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"PPT Plan JSON: {fp}")
    print(f"PPT Outline MD: {md_fp}")
    print(f"推荐模板: {plan['template']}")
    return str(fp), str(md_fp)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("用法: python ppt_gen.py <项目类型> <地点> <规模> <风格>")
        sys.exit(1)
    export_plan_json(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
