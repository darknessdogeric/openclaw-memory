#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Summarize Skill - 文本摘要技能
支持多种摘要类型：文章、论文、视频字幕、聊天记录等
"""

import sys
import argparse
import re

class TextSummarizer:
    """文本摘要器"""
    
    def __init__(self, text, summary_type="auto"):
        self.text = text
        self.summary_type = summary_type
        self.sentences = self._split_sentences()
    
    def _split_sentences(self):
        """分句"""
        # 中文分句
        text = re.sub(r'([。！？；])', r'\1\n', self.text)
        sentences = [s.strip() for s in text.split('\n') if s.strip()]
        return sentences
    
    def _extract_keywords(self, top_n=10):
        """提取关键词"""
        import jieba
        import jieba.analyse
        
        keywords = jieba.analyse.extract_tags(
            self.text, 
            topK=top_n, 
            withWeight=True
        )
        return keywords
    
    def _sentence_importance(self):
        """计算句子重要性"""
        word_freq = {}
        
        # 统计词频
        for sentence in self.sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 计算句子得分
        scores = []
        for sentence in self.sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            if words:
                score = sum(word_freq.get(word, 0) for word in words) / len(words)
                scores.append(score)
            else:
                scores.append(0)
        
        return scores
    
    def summarize_extractive(self, ratio=0.3):
        """抽取式摘要"""
        if not self.sentences:
            return ""
        
        scores = self._sentence_importance()
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        
        # 选择前 N 个句子
        num_sentences = max(1, int(len(self.sentences) * ratio))
        top_indices = sorted([idx for idx, _ in ranked[:num_sentences]])
        
        summary = ' '.join([self.sentences[i] for i in top_indices])
        return summary
    
    def summarize_abstractive(self, max_length=200):
        """生成式摘要（简化版）"""
        # 提取关键句子
        extractive = self.summarize_extractive(ratio=0.5)
        
        # 进一步压缩
        sentences = self._split_sentences()
        if len(extractive) > max_length:
            # 保留前半部分和后半部分的关键信息
            words = extractive[:max_length].rsplit(' ', 1)[0]
            return words + "..."
        
        return extractive
    
    def get_structured_summary(self):
        """结构化摘要"""
        summary = {
            'original_length': len(self.text),
            'sentence_count': len(self.sentences),
            'extractive_summary': self.summarize_extractive(),
            'abstractive_summary': self.summarize_abstractive(),
        }
        
        try:
            summary['keywords'] = [kw[0] for kw in self._extract_keywords()]
        except:
            summary['keywords'] = []
        
        return summary

class PaperSummarizer(TextSummarizer):
    """论文摘要器"""
    
    def __init__(self, text):
        super().__init__(text, "paper")
    
    def summarize(self):
        """论文结构化摘要"""
        # 尝试提取论文结构
        sections = {
            'abstract': self._extract_section(r'[摘要|Abstract][：:]\s*([^\n]+(?:\n(?![关键词|Key])[^\n]+)*)'),
            'introduction': self._extract_section(r'[引言|Introduction][：:]?\s*([^#]+?)(?=[方法|Methodology]|$)'),
            'methodology': self._extract_section(r'[方法|Methodology|Methods][：:]?\s*([^#]+?)(?=[结果|Results]|$)'),
            'results': self._extract_section(r'[结果|Results|Findings][：:]?\s*([^#]+?)(?=[讨论|Discussion]|$)'),
            'conclusion': self._extract_section(r'[结论|Conclusion|总结][：:]?\s*([^#]+?)(?=$)'),
        }
        
        return {
            'type': 'paper',
            'sections': sections,
            'summary': self._generate_paper_summary(sections)
        }
    
    def _extract_section(self, pattern):
        """提取章节内容"""
        match = re.search(pattern, self.text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
    
    def _generate_paper_summary(self, sections):
        """生成论文摘要"""
        summary_parts = []
        
        if sections['abstract']:
            summary_parts.append(f"【摘要】{sections['abstract'][:200]}...")
        
        if sections['methodology']:
            summary_parts.append(f"【方法】{self._summarize_section(sections['methodology'])}")
        
        if sections['results']:
            summary_parts.append(f"【结果】{self._summarize_section(sections['results'])}")
        
        if sections['conclusion']:
            summary_parts.append(f"【结论】{self._summarize_section(sections['conclusion'])}")
        
        return '\n'.join(summary_parts)
    
    def _summarize_section(self, text, max_len=100):
        """章节摘要"""
        sentences = re.split(r'[。！？]', text)
        summary = '。'.join(sentences[:2])
        if len(summary) > max_len:
            summary = summary[:max_len] + '...'
        return summary

class VideoSummarizer:
    """视频字幕摘要器"""
    
    def __init__(self, subtitle_text):
        self.subtitle_text = subtitle_text
    
    def summarize(self):
        """视频内容摘要"""
        # 清理字幕时间戳
        clean_text = re.sub(r'\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,.]\d{3}', '', self.subtitle_text)
        clean_text = re.sub(r'\n\d+\n', '\n', clean_text)
        
        summarizer = TextSummarizer(clean_text, "video")
        
        return {
            'type': 'video',
            'original_duration': self._estimate_duration(),
            'content_summary': summarizer.summarize_extractive(ratio=0.2),
            'key_points': self._extract_key_points(clean_text)
        }
    
    def _estimate_duration(self):
        """估算视频时长"""
        lines = self.subtitle_text.strip().split('\n')
        return f"约 {len(lines) // 2} 句字幕"
    
    def _extract_key_points(self, text):
        """提取关键点"""
        sentences = re.split(r'[。！？]', text)
        # 提取包含关键信息的句子
        key_indicators = ['重要', '关键', '核心', '首先', '其次', '最后', '总结', '结论']
        key_points = []
        
        for sent in sentences[:20]:  # 只看前20句
            if any(indicator in sent for indicator in key_indicators):
                key_points.append(sent.strip())
        
        return key_points[:5]  # 最多5个关键点

class ChatSummarizer:
    """聊天记录摘要器"""
    
    def __init__(self, chat_text):
        self.chat_text = chat_text
    
    def summarize(self):
        """聊天摘要"""
        # 解析聊天参与者
        participants = self._extract_participants()
        
        # 提取关键讨论点
        topics = self._extract_topics()
        
        # 提取决策/行动项
        actions = self._extract_actions()
        
        return {
            'type': 'chat',
            'participants': participants,
            'topics': topics,
            'actions': actions,
            'summary': self._generate_chat_summary(participants, topics, actions)
        }
    
    def _extract_participants(self):
        """提取参与者"""
        pattern = r'^(\w+)[：:]' if re.search(r'\w+[：:]', self.chat_text) else r'^(\w+)[:\s]'
        matches = re.findall(pattern, self.chat_text, re.MULTILINE)
        return list(set(matches))
    
    def _extract_topics(self):
        """提取讨论主题"""
        topic_indicators = ['讨论', '关于', '问题是', '主题是', '说到']
        topics = []
        
        lines = self.chat_text.split('\n')
        for line in lines:
            for indicator in topic_indicators:
                if indicator in line:
                    topic = line[line.find(indicator):line.find(indicator)+50]
                    topics.append(topic.strip())
                    break
        
        return topics[:5]
    
    def _extract_actions(self):
        """提取行动项"""
        action_keywords = ['需要', '必须', '应该', '完成', '确认', '跟进']
        actions = []
        
        lines = self.chat_text.split('\n')
        for line in lines:
            for keyword in action_keywords:
                if keyword in line and ('?' not in line or '吗' not in line):
                    actions.append(line.strip())
                    break
        
        return actions[:5]
    
    def _generate_chat_summary(self, participants, topics, actions):
        """生成聊天摘要"""
        summary = f"【参与者】{', '.join(participants)}\n"
        
        if topics:
            summary += f"\n【讨论主题】\n" + '\n'.join([f"- {t}" for t in topics[:3]])
        
        if actions:
            summary += f"\n\n【行动项】\n" + '\n'.join([f"- {a}" for a in actions[:3]])
        
        return summary

def main():
    parser = argparse.ArgumentParser(description='文本摘要工具')
    parser.add_argument('input', help='输入文件路径或文本')
    parser.add_argument('-t', '--type', choices=['auto', 'text', 'paper', 'video', 'chat'], 
                        default='auto', help='摘要类型')
    parser.add_argument('-r', '--ratio', type=float, default=0.3, help='摘要比例')
    parser.add_argument('-o', '--output', help='输出文件')
    
    args = parser.parse_args()
    
    # 读取输入
    if args.input.endswith('.txt') or args.input.endswith('.md'):
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.input
    
    # 自动检测类型
    summary_type = args.type
    if summary_type == 'auto':
        if 'abstract' in text.lower() or '摘要' in text[:500]:
            summary_type = 'paper'
        elif re.search(r'\d{2}:\d{2}:\d{2}', text):
            summary_type = 'video'
        elif re.search(r'\w+[：:]\s*\w+', text[:1000]):
            summary_type = 'chat'
        else:
            summary_type = 'text'
    
    # 执行摘要
    if summary_type == 'paper':
        summarizer = PaperSummarizer(text)
        result = summarizer.summarize()
    elif summary_type == 'video':
        summarizer = VideoSummarizer(text)
        result = summarizer.summarize()
    elif summary_type == 'chat':
        summarizer = ChatSummarizer(text)
        result = summarizer.summarize()
    else:
        summarizer = TextSummarizer(text, summary_type)
        result = {
            'type': 'text',
            'extractive': summarizer.summarize_extractive(args.ratio),
            'abstractive': summarizer.summarize_abstractive()
        }
    
    # 输出结果
    import json
    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"摘要已保存至: {args.output}")
    else:
        print(output)

if __name__ == '__main__':
    main()
