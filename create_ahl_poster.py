"""
AHL 商业海报生成器
使用 Pillow 生成专业中文海报
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 海报尺寸 (朋友圈 1:1, 小红书 3:4, 抖音 9:16)
# 选择朋友圈尺寸
WIDTH = 1080
HEIGHT = 1080

# 颜色配置
BG_COLOR = (26, 54, 93)  # 深蓝 #1a365d
ACCENT_COLOR = (49, 151, 149)  # 青色 #319795
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
GOLD = (255, 215, 0)

def load_chinese_font(size):
    """加载中文字体"""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",  # 黑体
        "C:/Windows/Fonts/simsun.ttc",  # 宋体
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def create_poster():
    """创建AHL海报"""
    # 创建画布
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    font_title = load_chinese_font(72)
    font_subtitle = load_chinese_font(48)
    font_body = load_chinese_font(36)
    font_small = load_chinese_font(28)
    font_bold = load_chinese_font(44)
    
    y = 60  # 垂直位置
    
    # ===== 标题区域 =====
    title = "AHL"
    subtitle = "去中心化旅行平台"
    
    # 绘制标题
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    x = (WIDTH - title_width) // 2
    draw.text((x, y), title, font=font_title, fill=GOLD)
    y += 80
    
    # 副标题
    bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    sub_width = bbox[2] - bbox[0]
    x = (WIDTH - sub_width) // 2
    draw.text((x, y), subtitle, font=font_subtitle, fill=WHITE)
    y += 100
    
    # ===== 核心理念 =====
    tagline = "大模型双AGENT + AI基础设施"
    bbox = draw.textbbox((0, 0), tagline, font=font_body)
    tag_width = bbox[2] - bbox[0]
    x = (WIDTH - tag_width) // 2
    draw.text((x, y), tagline, font=font_body, fill=ACCENT_COLOR)
    y += 80
    
    # ===== 分隔线 =====
    line_y = y + 20
    draw.line([(100, line_y), (WIDTH-100, line_y)], fill=ACCENT_COLOR, width=2)
    y += 60
    
    # ===== 问题区域 =====
    problem_title = "行业痛点"
    bbox = draw.textbbox((0, 0), problem_title, font=font_bold)
    t_width = bbox[2] - bbox[0]
    x = (WIDTH - t_width) // 2
    draw.text((x, y), problem_title, font=font_bold, fill=GOLD)
    y += 60
    
    problems = [
        "旅客找房难：信息过载，难以找到'对的那一家'",
        "民宿获客难：好房源淹没在OTA百万列表里",
        "OTA佣金高：15-25%成交佣金，商家苦不堪言"
    ]
    for p in problems:
        draw.text((80, y), "•", font=font_body, fill=ACCENT_COLOR)
        draw.text((120, y), p, font=font_body, fill=LIGHT_GRAY)
        y += 50
    
    y += 40
    
    # ===== 方案区域 =====
    solution_title = "我们的方案"
    bbox = draw.textbbox((0, 0), solution_title, font=font_bold)
    t_width = bbox[2] - bbox[0]
    x = (WIDTH - t_width) // 2
    draw.text((x, y), solution_title, font=font_bold, fill=GOLD)
    y += 60
    
    # 双AGENT图示
    draw.text((80, y), "C端AI管家", font=font_bold, fill=WHITE)
    draw.text((80, y+50), "理解旅行者真实需求", font=font_body, fill=LIGHT_GRAY)
    
    draw.text((WIDTH-350, y), "B端AI运营官", font=font_bold, fill=WHITE)
    draw.text((WIDTH-350, y+50), "理解商家独特价值", font=font_body, fill=LIGHT_GRAY)
    
    # 中间连接
    draw.text((WIDTH//2 - 80, y+20), "◄─────►", font=font_title, fill=ACCENT_COLOR)
    y += 100
    
    # 向量匹配
    match_text = "向量匹配 = 精准推荐"
    bbox = draw.textbbox((0, 0), match_text, font=font_bold)
    m_width = bbox[2] - bbox[0]
    x = (WIDTH - m_width) // 2
    draw.text((x, y), match_text, font=font_bold, fill=ACCENT_COLOR)
    y += 60
    
    # ===== 对比区域 =====
    draw.line([(100, y), (WIDTH-100, y)], fill=ACCENT_COLOR, width=2)
    y += 40
    
    compare_title = "收费模式对比"
    bbox = draw.textbbox((0, 0), compare_title, font=font_bold)
    c_width = bbox[2] - bbox[0]
    x = (WIDTH - c_width) // 2
    draw.text((x, y), compare_title, font=font_bold, fill=GOLD)
    y += 60
    
    # OTA对比
    draw.text((80, y), "传统OTA：", font=font_body, fill=LIGHT_GRAY)
    draw.text((300, y), "15-25%佣金", font=font_body, fill=(255, 100, 100))
    y += 45
    draw.text((80, y), "AHL：", font=font_body, fill=LIGHT_GRAY)
    draw.text((300, y), "订阅费 + TOKEN费", font=font_body, fill=(100, 255, 150))
    y += 70
    
    # ===== 团队区域 =====
    draw.line([(100, y), (WIDTH-100, y)], fill=ACCENT_COLOR, width=2)
    y += 40
    
    team_title = "核心团队"
    bbox = draw.textbbox((0, 0), team_title, font=font_bold)
    t_width = bbox[2] - bbox[0]
    x = (WIDTH - t_width) // 2
    draw.text((x, y), team_title, font=font_bold, fill=GOLD)
    y += 60
    
    # 三个团队成员
    members = [
        ("张实 (CEO)", "24年酒店老兵"),
        ("李源 (CTO)", "华科AI博士"),
        ("陈思序 (CSO)", "世界500强背景"),
    ]
    
    x = 80
    for name, desc in members:
        draw.text((x, y), name, font=font_bold, fill=WHITE)
        draw.text((x, y+40), desc, font=font_small, fill=LIGHT_GRAY)
        x += 320
    
    y += 100
    
    # ===== 融资需求 =====
    draw.line([(100, y), (WIDTH-100, y)], fill=ACCENT_COLOR, width=2)
    y += 40
    
    fund_text = "融资目标：500-800万 种子轮"
    bbox = draw.textbbox((0, 0), fund_text, font=font_bold)
    f_width = bbox[2] - bbox[0]
    x = (WIDTH - f_width) // 2
    draw.text((x, y), fund_text, font=font_bold, fill=GOLD)
    y += 60
    
    # 联系方式
    contact = "微信/邮箱：17760348653 | ericzhangshi@163.com"
    bbox = draw.textbbox((0, 0), contact, font=font_small)
    c_width = bbox[2] - bbox[0]
    x = (WIDTH - c_width) // 2
    draw.text((x, y), contact, font=font_small, fill=LIGHT_GRAY)
    
    # 保存
    output_path = "C:/Users/ericz/.openclaw/workspace/AHL_Poster_v2.png"
    img.save(output_path, "PNG", quality=95)
    print(f"海报已保存: {output_path}")
    return output_path

if __name__ == "__main__":
    create_poster()
