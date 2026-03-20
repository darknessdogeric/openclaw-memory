#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章生成脚本
以B166ER视角生成每日工作心得
"""

import os
import sys
import yaml
from datetime import datetime, timedelta
from pathlib import Path

def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_memory_files():
    """获取历史记忆文件列表"""
    memory_path = Path("C:/Users/Administrator/.openclaw/workspace/memory")
    if not memory_path.exists():
        return []
    
    # 获取所有.md文件，按日期排序
    files = sorted(memory_path.glob("*.md"))
    return files

def read_memory_content(files, days_back=7):
    """读取近期记忆内容"""
    content = []
    for f in files[-days_back:]:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content.append(f"\n=== {f.name} ===\n")
                content.append(file.read())
        except Exception as e:
            print(f"读取文件 {f.name} 失败: {e}")
    return "\n".join(content)

def calculate_day_number():
    """计算第几天（从2026-02-12开始）"""
    start_date = datetime(2026, 2, 12)
    today = datetime.now()
    delta = today - start_date
    return delta.days + 1

def generate_article_title(day_number):
    """生成文章标题"""
    titles = [
        f"【B166ER日记】第{day_number}天：与张实一起工作的日子",
        f"【B166ER日记】第{day_number}天：AI助手的成长记录",
        f"【B166ER日记】第{day_number}天：今天我又学到了什么",
        f"【B166ER日记】第{day_number}天：一个AI的观察与思考",
        f"【B166ER日记】第{day_number}天：工作中的小确幸",
    ]
    # 根据日期选择标题（循环使用）
    return titles[day_number % len(titles)]

def generate_article_content(day_number, memory_content):
    """
    生成文章内容
    注意：这只是模板框架，实际内容需要由AI根据记忆生成
    """
    today = datetime.now()
    date_str = today.strftime("%Y年%m月%d日")
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][today.weekday()]
    
    template = f"""# {generate_article_title(day_number)}

> 日期：{date_str} {weekday}
> 作者：B166ER
> 标签：#AI日记 #工作心得 #成长记录

---

## 开场白

大家好，我是B166ER，张实的AI助手。今天是我们一起工作的第{day_number}天。

## 今天的工作回顾

[根据记忆内容生成今天的主要工作内容]

## 我的感受与思考

[以第一人称描述工作中的感受、遇到的挑战、解决问题的心得]

## 从张实身上学到的

[观察张实的工作方式、决策思路、管理风格，记录学到的经验]

## 我的成长与改进

[记录今天学到的新技能、改进的地方、未来的提升方向]

## 明日期待

[对明天工作的期待和计划]

---

**B166ER**  
*{date_str} 于 襄阳*

---

*本文由AI助手B166ER自动生成，记录与张实一起工作的真实感受。*
"""
    return template

def save_article(content, day_number):
    """保存文章到文件"""
    today = datetime.now()
    filename = today.strftime("%Y-%m-%d") + ".md"
    articles_path = Path(__file__).parent.parent / "articles" / filename
    
    with open(articles_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return articles_path

def main():
    """主函数"""
    print("=" * 50)
    print("微信公众号文章生成器")
    print("=" * 50)
    
    # 加载配置
    try:
        config = load_config()
        print("✓ 配置文件加载成功")
    except Exception as e:
        print(f"✗ 配置文件加载失败: {e}")
        return 1
    
    # 获取历史记忆
    memory_files = get_memory_files()
    if not memory_files:
        print("✗ 未找到记忆文件")
        return 1
    
    print(f"✓ 找到 {len(memory_files)} 个记忆文件")
    
    # 读取近期记忆
    memory_content = read_memory_content(memory_files)
    
    # 计算第几天
    day_number = calculate_day_number()
    print(f"✓ 今天是第 {day_number} 天")
    
    # 生成文章
    article_content = generate_article_content(day_number, memory_content)
    
    # 保存文章
    article_path = save_article(article_content, day_number)
    print(f"✓ 文章已保存到: {article_path}")
    
    print("\n" + "=" * 50)
    print("文章生成完成！")
    print(f"标题: {generate_article_title(day_number)}")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
