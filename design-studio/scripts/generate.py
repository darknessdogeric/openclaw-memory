# -*- coding: utf-8 -*-
"""
Design Studio Engine v2.0
参数驱动: 平面图 / 立面图 / 三视图 / 概念渲染 / 设计简报 / Mood Board

用法:
  python generate.py full "医养酒店" 大理 "150间" --style 生物亲和
  python generate.py floorplan "3卧室2卫" 120 现代
  python generate.py elevation "精品酒店正立面" --style 新中式 --direction front
  python generate.py orthographic "度假别墅" --style 现代
  python generate.py brief "医养酒店" 大理 "150间"
"""
import sys, os, json, time, re, argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent  # scripts/ -> design-studio/
OUTPUT_DIR = ROOT / "output"
REF_DIR = ROOT / "references"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════
# 提示词模板
# ═══════════════════════════════════════════

QUALITY = "photorealistic architectural visualization, 8K quality, professional architectural photography, Unreal Engine 5 render"

def floorplan_prompt(rooms, area, style="现代"):
    """生成平面图提示词"""
    return f"""architectural floor plan, top-down plan view, {rooms} layout,
total area {area} square meters, {style} residential architecture,
clean professional architectural drafting style, black linework on white background,
dimension annotations on walls, door swings indicated with arcs,
furniture layout shown in light grey, room labels in architectural lettering,
window and door schedules, north arrow, 1:100 scale appearance,
professional architectural plan, centered composition, 1:1 square format"""

def elevation_prompt(building, style="现代", direction="front", stories=3, material="glass and steel"):
    """生成立面图提示词"""
    dir_map = {
        "front": "front elevation with main entrance centered, symmetrical facade composition",
        "side": "side elevation showing building depth and profile, cross-section relationship",
        "rear": "rear elevation with service entrance and mechanical screening",
        "left": "left side elevation, orthogonal projection, window rhythm",
        "right": "right side elevation, consistent with left facade language"
    }
    dir_desc = dir_map.get(direction, dir_map["front"])
    
    return f"""architectural elevation drawing, {dir_desc},
{building}, {style} architecture, {stories} stories,
{material} facade with precise details,
orthographic projection, no perspective distortion,
professional architectural drafting style, clean linework,
material hatch patterns, shadow indication at 45 degrees,
dimension lines with height markers, human scale figure for reference,
white background, architectural blueprint aesthetic, 9:16 vertical format"""

def orthographic_prompts(building, style="现代", stories=3):
    """生成三视图提示词 (front/side/top)"""
    front = f"""orthographic front view, {building}, {style} architecture,
{stories} stories, main facade with entrance, strict orthogonal projection,
no perspective, professional architectural orthographic drawing,
dimensioned, white background, 1:1 square format"""
    
    side = f"""orthographic side view, {building}, {style} architecture,
{stories} stories, showing building depth and profile,
strict orthogonal projection, professional architectural drawing,
white background, 1:1 square format"""
    
    top = f"""orthographic top view, roof plan of {building},
{style} architecture, building footprint, roof mechanical equipment,
surrounding simplified context, north arrow, professional architectural
roof plan drawing, white background, 1:1 square format"""
    
    return {"front": front, "side": side, "top": top}


# ═══════════════════════════════════════════
# 简报生成
# ═══════════════════════════════════════════

def generate_brief(project_type, location, scale, style="现代"):
    brief = f"""# {location}{project_type} — 项目设计简报

**生成日期**: {time.strftime('%Y-%m-%d')}
**设计引擎**: B166ER Design Studio v2.0

---

## 一、项目定位

| 参数 | 内容 |
|------|------|
| 项目类型 | {project_type} |
| 地理位置 | {location} |
| 规模 | {scale} |
| 设计风格 | {style} |

## 二、设计概念方向

### 概念A: {style}演绎
以{style}语言为基调，结合{location}的地域特征，创造独特的空间体验。

### 概念B: 在地文化融合
提取{location}的文化符号与建造传统，用当代材料和构造方式重新诠释。

### 概念C: 生态可持续
最大化利用自然采光通风，采用本地材料，减少碳足迹。

## 三、空间规划

### 功能分区
1. **到达体验区**: 大堂、礼宾、等候休息
2. **公共活动区**: 餐厅、会议、SPA、泳池
3. **客房区**: 标准间、套房、无障碍客房
4. **后勤服务区**: 厨房、洗衣、员工、设备
5. **户外景观区**: 庭院、露台、屋顶花园

### 流线设计
- 客人流线: 入口→大堂→电梯→客房，路径清晰愉悦
- 服务流线: 后勤入口→服务通道→各功能区，与客人流线分离
- 物流流线: 卸货区→仓库→厨房/客房，隐蔽高效

## 四、材质与色彩策略

### 主材体系
- 结构: 建议钢混框架+{location}当地石材饰面
- 立面: {style}特征材料组合
- 室内: 温暖木材+天然石材+手工质感墙面

### 色彩方案
基于{location}自然环境提取色调

## 五、概念图清单

本简报配套生成以下概念图：
1. 建筑外观渲染 (鸟瞰+人视)
2. 大堂室内渲染
3. 标准客房渲染
4. 平面图概念方案
5. 立面图概念方案
6. Mood Board 情绪板

## 六、下一步

1. ✅ 概念渲染图生成
2. 📋 Mood Board 情绪板
3. 📋 空间功能泡泡图
4. 📋 初步平面方案
5. 📋 投资估算框架
"""
    return brief


# ═══════════════════════════════════════════
# Mood Board生成
# ═══════════════════════════════════════════

def generate_moodboard(project_name, description, style="现代"):
    palettes = {
        "现代": ["#1a1a2e", "#16213e", "#e94560", "#f5f5f5", "#c9b99a"],
        "新中式": ["#2d1b00", "#8b4513", "#daa520", "#f5f0e8", "#2f4f4f"],
        "侘寂": ["#d4c5b9", "#a89380", "#8b7d6b", "#e8e0d5", "#5c4d44"],
        "生物亲和": ["#4a7c59", "#8db580", "#d4e4c5", "#f5f0e8", "#2d4a3e"],
        "奢华": ["#1a1a1a", "#b8860b", "#800020", "#faf0e6", "#2f2f2f"],
        "北欧": ["#f5f0e8", "#d4c5b9", "#8db580", "#2d4a3e", "#c9b99a"],
    }
    palette = palettes.get(style, palettes["现代"])
    
    keywords_map = {
        "现代": ["极简", "几何", "通透", "光影", "效率", "科技"],
        "新中式": ["意境", "留白", "庭院", "框景", "材料本色", "手作"],
        "侘寂": ["不完美", "时间痕迹", "自然", "朴素", "安静", "手工"],
        "生物亲和": ["自然光", "绿植", "有机形态", "疗愈", "水景", "木材"],
        "奢华": ["精致", "材质对比", "光影戏剧", "定制", "私密", "仪式感"],
        "北欧": ["温暖", "简约", "功能性", "自然光", "舒适", "木质感"],
    }
    keywords = keywords_map.get(style, keywords_map["现代"])
    
    colors_html = "".join([
        f'<div class="swatch" style="background:{c};" title="{c}"><span>{c}</span></div>'
        for c in palette
    ])
    kw_html = "".join([f'<span class="kw">{k}</span>' for k in keywords])
    
    html = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<title>{project_name} Mood Board</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0f0f0f;color:#e0e0e0;font-family:"DM Sans","Noto Sans SC",sans-serif;padding:60px;min-height:100vh}}
h1{{font-size:48px;font-weight:300;letter-spacing:-0.02em;margin-bottom:8px}}
.sub{{font-size:16px;color:#888;margin-bottom:48px}}
.sec{{margin-bottom:48px}}
.st{{font-size:12px;text-transform:uppercase;letter-spacing:.2em;color:#666;margin-bottom:16px}}
.palette{{display:flex;gap:12px;flex-wrap:wrap}}
.swatch{{width:100px;height:100px;border-radius:8px;display:flex;align-items:flex-end;padding:8px;font-size:10px;font-family:monospace}}
.kws{{display:flex;gap:8px;flex-wrap:wrap}}
.kw{{padding:8px 20px;border:1px solid #333;border-radius:100px;font-size:14px;color:#aaa}}
.desc{{max-width:600px;font-size:16px;line-height:1.8;color:#aaa}}
.foot{{margin-top:80px;font-size:11px;color:#444}}
</style></head><body>
<h1>{project_name}</h1><p class="sub">Mood Board · {style}风格</p>
<div class="sec"><div class="st">Color Palette</div><div class="palette">{colors_html}</div></div>
<div class="sec"><div class="st">Keywords</div><div class="kws">{kw_html}</div></div>
<div class="sec"><div class="st">Design Direction</div><p class="desc">{description}</p></div>
<div class="foot">B166ER Design Studio v2.0 · {time.strftime('%Y-%m-%d')}</div>
</body></html>'''
    
    fp = OUTPUT_DIR / f"moodboard_{project_name.replace(' ','_')}.html"
    fp.write_text(html, encoding='utf-8')
    return str(fp)


# ═══════════════════════════════════════════
# 项目汇总报告
# ═══════════════════════════════════════════

def generate_summary(project_type, location, scale, style, prompts):
    """生成完整的项目汇总Markdown"""
    sections = []
    sections.append(f"# {location}{project_type} — 设计概念包\n")
    sections.append(f"**生成日期**: {time.strftime('%Y-%m-%d %H:%M')}")
    sections.append(f"**引擎**: B166ER Design Studio v2.0\n")
    sections.append(f"## 项目参数\n")
    sections.append(f"| 参数 | 值 |")
    sections.append(f"|------|-----|")
    sections.append(f"| 项目类型 | {project_type} |")
    sections.append(f"| 地点 | {location} |")
    sections.append(f"| 规模 | {scale} |")
    sections.append(f"| 风格 | {style} |\n")
    
    sections.append(f"## 概念图提示词\n")
    for category, prompt_list in prompts.items():
        sections.append(f"### {category}\n")
        if isinstance(prompt_list, dict):
            for sub, p in prompt_list.items():
                sections.append(f"**{sub}**:\n```\n{p}\n```\n")
        elif isinstance(prompt_list, str):
            sections.append(f"```\n{prompt_list}\n```\n")
        else:
            for p in prompt_list:
                sections.append(f"```\n{p}\n```\n")
    
    sections.append(f"\n---\n*Generated by B166ER Design Studio v2.0*")
    
    content = "\n".join(sections)
    fp = OUTPUT_DIR / f"project_{location}_{project_type.replace(' ','_')}.md"
    fp.write_text(content, encoding='utf-8')
    return str(fp)


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Design Studio v2.0")
    sub = parser.add_subparsers(dest="cmd")
    
    # full
    p = sub.add_parser("full", help="生成全套设计文件")
    p.add_argument("project", help="项目类型: 酒店/民宿/医养/度假村")
    p.add_argument("location", help="地点")
    p.add_argument("scale", help="规模: 150间/8000平米")
    p.add_argument("--style", default="现代")
    p.add_argument("--stories", type=int, default=3)
    
    # floorplan
    p = sub.add_parser("floorplan", help="生成平面图提示词")
    p.add_argument("rooms", help="房间配置: 3卧室2卫")
    p.add_argument("area", type=int, help="总面积(平米)")
    p.add_argument("style", nargs="?", default="现代")
    
    # elevation
    p = sub.add_parser("elevation", help="生成立面图提示词")
    p.add_argument("building", help="建筑描述")
    p.add_argument("--style", default="现代")
    p.add_argument("--direction", default="front", choices=["front","side","rear","left","right"])
    p.add_argument("--stories", type=int, default=3)
    p.add_argument("--material", default="glass and steel")
    
    # orthographic
    p = sub.add_parser("orthographic", help="生成三视图提示词")
    p.add_argument("building", help="建筑描述")
    p.add_argument("--style", default="现代")
    p.add_argument("--stories", type=int, default=3)
    
    # brief
    p = sub.add_parser("brief", help="生成设计简报")
    p.add_argument("project", help="项目类型")
    p.add_argument("location", help="地点")
    p.add_argument("scale", help="规模")
    p.add_argument("--style", default="现代")
    
    # moodboard
    p = sub.add_parser("moodboard", help="生成Mood Board")
    p.add_argument("name", help="项目名称")
    p.add_argument("description", nargs="?", default="")
    p.add_argument("--style", default="现代")
    
    # architecture / interior (from v1.0)
    p = sub.add_parser("architecture")
    p.add_argument("desc", help="描述")
    p.add_argument("--style", default=None)
    p.add_argument("--mood", default=None)
    
    p = sub.add_parser("interior")
    p.add_argument("desc", help="描述")
    p.add_argument("--style", default=None)
    
    args = parser.parse_args()
    
    if not args.cmd:
        parser.print_help()
        return
    
    # ── full ──
    if args.cmd == "full":
        print(f"\n{'='*70}")
        print(f"Design Studio v2.0 — 全套设计文件生成")
        print(f"{'='*70}")
        print(f"项目: {args.location}{args.project}")
        print(f"规模: {args.scale} | 风格: {args.style}\n")
        
        prompts = {}
        
        # 1. 建筑外观
        arch_p = f"{args.style} {args.project} exterior, {args.location} landscape setting, {args.stories} stories, warm natural materials, dramatic composition, wide angle, golden hour, {QUALITY}"
        prompts["1-建筑外观"] = [arch_p, arch_p.replace("wide angle", "aerial bird's eye view")]
        
        # 2. 室内空间
        prompts["2-大堂"] = f"luxury {args.style} hotel lobby, spacious welcoming atmosphere, {args.location} cultural elements subtly integrated, natural materials, warm lighting, people relaxing, interior photography, photorealistic, 8K"
        prompts["3-客房"] = f"hotel guest room, {args.style} design, comfortable king bed, large window with {args.location} view, natural material palette, soft ambient lighting, photorealistic, 8K"
        
        # 3. 平面图
        prompts["4-平面图"] = floorplan_prompt(f"{args.project}标准层", args.scale, args.style)
        
        # 4. 立面图
        prompts["5-立面图"] = {
            "正立面": elevation_prompt(f"{args.location}{args.project}", args.style, "front", args.stories),
            "侧立面": elevation_prompt(f"{args.location}{args.project}", args.style, "side", args.stories),
        }
        
        # 5. 三视图
        prompts["6-三视图"] = orthographic_prompts(f"{args.location}{args.project}", args.style, args.stories)
        
        # 6. 简报
        brief = generate_brief(args.project, args.location, args.scale, args.style)
        bf = OUTPUT_DIR / f"brief_{args.location}_{args.project.replace(' ','_')}.md"
        bf.write_text(brief, encoding='utf-8')
        prompts["7-设计简报"] = f"已生成: {bf}"
        
        # 7. Mood Board
        mb_desc = args.description if hasattr(args, 'description') and args.description else f"以{args.style}语言在{args.location}打造{args.project}"
        mb = generate_moodboard(f"{args.location}{args.project}", mb_desc, args.style)
        prompts["8-MoodBoard"] = f"已生成: {mb}"
        
        # 汇总
        summary = generate_summary(args.project, args.location, args.scale, args.style, prompts)
        
        print(f"📄 项目汇总: {summary}")
        print(f"📄 设计简报: {bf}")
        print(f"🎨 Mood Board: {mb}")
        print(f"\n📐 生成的概念图提示词 (共{sum(len(v) if isinstance(v,(list,dict)) else 1 for v in prompts.values())}张):")
        for cat, plist in prompts.items():
            if isinstance(plist, dict):
                print(f"\n  [{cat}]")
                for sub, p in plist.items():
                    print(f"    {sub}: {p[:100]}...")
            elif isinstance(plist, list):
                print(f"\n  [{cat}]")
                for i, p in enumerate(plist):
                    print(f"    {i+1}. {p[:100]}...")
            elif isinstance(plist, str) and not plist.startswith("已生成"):
                print(f"\n  [{cat}]\n    {plist[:120]}...")
        print(f"\n✅ 完成! 所有文件在: {OUTPUT_DIR}")
    
    # ── floorplan ──
    elif args.cmd == "floorplan":
        p = floorplan_prompt(args.rooms, args.area, args.style)
        print(f"\n📐 平面图提示词:\n{p}")
        fp = OUTPUT_DIR / f"floorplan_{args.area}sqm.md"
        fp.write_text(f"# 平面图需求\n\n**户型**: {args.rooms}\n**面积**: {args.area}㎡\n**风格**: {args.style}\n\n## 生成提示词\n\n```\n{p}\n```\n\n## 在线工具\n- [Homestyler](https://www.homestyler.com)\n- [Home-design.ai](https://home-design.ai/floor-plan-generator)\n", encoding='utf-8')
        print(f"\n📄 已保存: {fp}")
    
    # ── elevation ──
    elif args.cmd == "elevation":
        p = elevation_prompt(args.building, args.style, args.direction, args.stories, args.material)
        print(f"\n🏛️ 立面图提示词 ({args.direction}):\n{p}")
    
    # ── orthographic ──
    elif args.cmd == "orthographic":
        views = orthographic_prompts(args.building, args.style, args.stories)
        print(f"\n📐 三视图提示词:")
        for view, p in views.items():
            print(f"\n--- {view.upper()} ---")
            print(p)
    
    # ── brief ──
    elif args.cmd == "brief":
        brief = generate_brief(args.project, args.location, args.scale, args.style)
        fp = OUTPUT_DIR / f"brief_{args.location}_{args.project.replace(' ','_')}.md"
        fp.write_text(brief, encoding='utf-8')
        print(f"\n📄 设计简报: {fp}")
    
    # ── moodboard ──
    elif args.cmd == "moodboard":
        desc = args.description or f"{args.style}风格设计概念"
        fp = generate_moodboard(args.name, desc, args.style)
        print(f"\n🎨 Mood Board: {fp}")
    
    # ── architecture / interior (v1 compat) ──
    elif args.cmd == "architecture":
        prompt = f"{args.desc}, {args.style or ''}, {args.mood or ''}, {QUALITY}"
        print(f"\n🏗️ 建筑外观:\n{prompt}")
    
    elif args.cmd == "interior":
        prompt = f"{args.desc}, {args.style or ''} interior design, wide angle lens, {QUALITY}"
        print(f"\n🛋️ 室内设计:\n{prompt}")


if __name__ == "__main__":
    main()
