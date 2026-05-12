# -*- coding: utf-8 -*-
"""
PPT智能生成器 - 大纲规划模块
分析内容，生成结构化PPT大纲
"""
import json
import re

class OutlinePlanner:
    """AI大纲规划器"""
    
    def __init__(self):
        self.default_sections = [
            "封面", "目录", "背景/痛点", "解决方案", 
            "产品/服务", "市场分析", "商业模式", "团队介绍",
            "竞争优势", "发展规划", "融资计划", "结尾"
        ]
    
    def analyze_content(self, content):
        """
        分析输入内容，提取关键信息
        """
        if isinstance(content, str):
            # 文本内容分析
            lines = content.split('\n')
            keywords = self._extract_keywords(lines)
            topics = self._identify_topics(content)
            return {
                "keywords": keywords,
                "topics": topics,
                "length": len(content),
                "type": "text"
            }
        elif isinstance(content, dict):
            # 结构化内容
            return {
                "keywords": content.get("keywords", []),
                "topics": content.get("topics", []),
                "sections": content.get("sections", []),
                "type": "structured"
            }
        else:
            return {"type": "unknown"}
    
    def _extract_keywords(self, lines):
        """提取关键词"""
        keywords = []
        for line in lines[:20]:  # 只看前20行
            # 提取数字（关键数据）
            numbers = re.findall(r'\d+[亿万亿%元]', line)
            keywords.extend(numbers)
            # 提取重要名词
            if any(x in line for x in ["行业", "市场", "产品", "服务", "技术", "团队"]):
                keywords.append(line.strip()[:20])
        return list(set(keywords))[:10]
    
    def _identify_topics(self, content):
        """识别主题"""
        topics = []
        content_lower = content.lower()
        
        if any(x in content_lower for x in ["融资", "投资", "天使", "轮次"]):
            topics.append("融资相关")
        if any(x in content_lower for x in ["政府", "申请", "扶持", "补贴"]):
            topics.append("政府申请")
        if any(x in content_lower for x in ["商业", "盈利", "收入", "模式"]):
            topics.append("商业模式")
        if any(x in content_lower for x in ["技术", "架构", "AI", "系统"]):
            topics.append("技术方案")
            
        return topics if topics else ["通用演示"]
    
    def generate_outline(self, content, slides_count=10):
        """
        生成PPT大纲
        """
        analysis = self.analyze_content(content)
        
        # 根据内容类型生成不同大纲
        if "政府" in analysis["topics"]:
            outline = self._gov_outline(analysis, slides_count)
        elif "融资" in analysis["topics"]:
            outline = self._pitch_outline(analysis, slides_count)
        else:
            outline = self._general_outline(analysis, slides_count)
        
        return outline
    
    def _gov_outline(self, analysis, count):
        """政府申请项目大纲"""
        return {
            "title": "政府专项申请项目",
            "sections": [
                {"num": 1, "title": "项目概述", "content": "核心定位与创新点"},
                {"num": 2, "title": "项目背景", "content": "行业痛点与政策机遇"},
                {"num": 3, "title": "建设方案", "content": "技术架构与实施计划"},
                {"num": 4, "title": "团队介绍", "content": "核心成员与能力"},
                {"num": 5, "title": "支持需求", "content": "资金/场地/设备需求"},
                {"num": 6, "title": "经济社会效益", "content": "预期贡献与价值"},
                {"num": 7, "title": "风险分析", "content": "风险识别与对策"},
                {"num": 8, "title": "结语", "content": "恳请支持"}
            ],
            "keywords": analysis["keywords"],
            "style": "formal",
            "color_theme": "blue_gold"
        }
    
    def _pitch_outline(self, analysis, count):
        """商业计划书大纲"""
        return {
            "title": "商业计划书",
            "sections": [
                {"num": 1, "title": "封面", "content": "项目名称与定位"},
                {"num": 2, "title": "痛点", "content": "市场需求与问题"},
                {"num": 3, "title": "解决方案", "content": "产品与服务"},
                {"num": 4, "title": "市场机会", "content": "市场规模与增长"},
                {"num": 5, "title": "商业模式", "content": "盈利方式"},
                {"num": 6, "title": "竞争优势", "content": "差异化壁垒"},
                {"num": 7, "title": "团队", "content": "核心成员"},
                {"num": 8, "title": "融资计划", "content": "资金需求与用途"},
                {"num": 9, "title": "里程碑", "content": "发展规划"},
                {"num": 10, "title": "联系", "content": "合作方式"}
            ],
            "keywords": analysis["keywords"],
            "style": "business",
            "color_theme": "blue"
        }
    
    def _general_outline(self, analysis, count):
        """通用演示大纲"""
        return {
            "title": "演示文稿",
            "sections": [
                {"num": 1, "title": "封面", "content": "主题"},
                {"num": 2, "title": "目录", "content": "内容概览"},
            ] + [
                {"num": i+3, "title": f"第{i}部分", "content": "关键内容"}
                for i in range(min(count-4, 6))
            ] + [
                {"num": count-1, "title": "总结", "content": "核心要点"},
                {"num": count, "title": "结尾", "content": "感谢"}
            ],
            "keywords": analysis["keywords"],
            "style": "general",
            "color_theme": "default"
        }


def plan_outline(content, slides_count=10):
    """规划PPT大纲的入口函数"""
    planner = OutlinePlanner()
    return planner.generate_outline(content, slides_count)


if __name__ == "__main__":
    # 测试
    test_content = """
    AHL去中心化住宿业交易生态协议
    项目概述：构建全球首个基于大语言模型的去中心化住宿业交易生态协议
    行业痛点：OTA垄断佣金20-30%，年损失1200亿
    解决方案：双AGENT+多SKILL架构，效率费3-5%
    申请支持：算力800万/年，场地108万，设备575万
    """
    result = plan_outline(test_content)
    print(json.dumps(result, ensure_ascii=False, indent=2))
