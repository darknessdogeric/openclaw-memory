# -*- coding: utf-8 -*-
"""
B166ER-Aware Career-Ops Wrapper
================================================================
让 B166ER 生态使用 career-ops 的核心方法论:
- 14 种求职模式 (apply/scan/followup/interview-prep/...)
- A-G 评分体系 (10 维)
- 6 个 Archetype (FDE/SA/PM/LLMOps/Agentic/Transformation)
- Liveness gate (链接存活检查)
- Pipeline (scan → evaluate → apply → followup)
================================================================
基于 santifer/career-ops (49.3K⭐) - https://github.com/santifer/career-ops
适配：保留方法论 + 数据模型，用 B166ER 的 scrape_matrix 替代 ClaudeCode 抓取
"""
from __future__ import annotations
import json
import time
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


# === 14 个 Career-Ops Modes (B166ER 适配版) ===
CAREER_MODES = {
    "scan": "Portal Scanner (Job Discovery) - 扫描 BOSS/拉勾/LinkedIn/V2EX 等",
    "job": "Full A-G Evaluation - 6 字母评分 + Archetype 分类",
    "jobs": "Multi-Job Comparison - 多个 offer 对比",
    "apply": "Live Application Assistant - 实时申请辅助",
    "cover": "Cover Letter Generator - 求职信生成（中文/英文）",
    "pdf": "ATS-Optimized PDF Generation - ATS 友好 PDF 简历",
    "latex": "LaTeX/Overleaf CV Export - LaTeX 简历导出",
    "interview": "Interactive Profile & CV Onboarding - 面试模拟",
    "interview-prep": "Company-Specific Interview Intelligence - 公司面试情报",
    "followup": "Follow-up Cadence Tracker - 跟进节奏跟踪",
    "patterns": "Rejection Pattern Detector - 拒绝模式分析",
    "batch": "Mass Processing of Jobs - 批量职位处理",
    "auto-pipeline": "Full Automatic Pipeline - 全自动 pipeline",
    "pipeline": "URL Inbox (Second Brain) - 链接收集",
}


# === A-G 评分体系 (career-ops 10 维评分，B166ER 适配) ===
@dataclass
class JobScore:
    """career-ops 风格 10 维评分"""
    # Block A: 角色匹配
    role_fit: float = 0.0           # 角色匹配度
    seniority_match: float = 0.0    # 资历匹配
    domain_match: float = 0.0       # 领域匹配
    # Block B: 个人能力 vs JD
    skills_match: float = 0.0       # 技能匹配
    experience_match: float = 0.0   # 经验匹配
    culture_fit: float = 0.0        # 文化匹配
    # Block C: 战略价值
    growth_potential: float = 0.0   # 成长空间
    network_value: float = 0.0      # 人脉价值
    # Block D: 薪酬
    comp_competitiveness: float = 0.0  # 薪酬竞争力
    comp_transparency: float = 0.0     # 薪酬透明度
    # Block E: 工作模式
    location_remote: float = 0.0    # 远程/位置
    # Block F: 风险
    company_stability: float = 0.0  # 公司稳定性
    # Block G: 真伪
    legitimacy: float = 0.0         # 招聘信息真伪（liveness check）

    @property
    def total(self):
        return round(sum([
            self.role_fit, self.seniority_match, self.domain_match,
            self.skills_match, self.experience_match, self.culture_fit,
            self.growth_potential, self.network_value,
            self.comp_competitiveness, self.comp_transparency,
            self.location_remote, self.company_stability,
            self.legitimacy,
        ]) / 13, 2)

    @property
    def grade(self):
        """career-ops A-F 评级"""
        t = self.total
        if t >= 9.0: return "A"
        if t >= 8.0: return "B"
        if t >= 7.0: return "C"
        if t >= 5.0: return "D"
        if t >= 3.0: return "E"
        return "F"


# === 6 Archetypes (career-ops 角色分类) ===
ARCHETYPES = {
    "FDE": "Forward Deployed Engineer - 前线部署工程师",
    "SA": "Solutions Architect - 解决方案架构师",
    "PM": "Product Manager - 产品经理",
    "LLMOps": "LLM Operations - 大模型运维",
    "Agentic": "Agentic Systems - Agent 系统工程师",
    "Transformation": "Transformation Lead - 转型负责人",
}


# === Liveness Gate (链接存活检查) ===
@dataclass
class LivenessCheck:
    """career-ops 风格的链接存活检查"""
    url: str
    is_live: bool = False
    status_code: int = 0
    title: str = ""
    has_jd: bool = False  # 是否有真实职位描述
    evidence: str = ""


def liveness_check(url: str, wait_ms: int = 8000) -> LivenessCheck:
    """
    用 B166ER 的 InvisiblePlaywright (跨境) 或 Obscura (国内) 检查链接存活
    """
    from invisible_playwright import InvisiblePlaywright
    check = LivenessCheck(url=url)
    try:
        with InvisiblePlaywright() as browser:
            page = browser.new_page()
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(wait_ms)
            check.is_live = True
            check.title = page.title()[:100]
            content = page.content()[:5000].lower()
            # 简单判断是否有 JD
            jd_keywords = ['responsibilit', 'requirement', 'qualification', '职位描述', '岗位职责', '任职要求', 'job description']
            check.has_jd = any(kw in content for kw in jd_keywords)
            if not check.has_jd:
                # 进一步：是否被重定向到搜索/首页
                closed_signals = ['no longer accepting', 'expired', '已下架', '已过期', 'page not found']
                if any(s in content for s in closed_signals):
                    check.is_live = False
                    check.evidence = "Closed/expired posting detected"
            page.close()
    except Exception as e:
        check.evidence = str(e)[:200]
    return check


# === Pipeline 状态机 (career-ops 求职管道) ===
PIPELINE_STAGES = [
    "discovered",   # scan 发现
    "evaluated",    # A-G 评估
    "shortlisted",  # 入选短名单
    "applying",     # 申请中
    "interviewing", # 面试中
    "offered",      # 已 offer
    "accepted",     # 已接受
    "rejected",     # 被拒
    "withdrawn",    # 主动撤回
]


# === CLI 演示 ===
if __name__ == "__main__":
    print("=" * 60)
    print("B166ER Career-Ops Wrapper - 演示")
    print("=" * 60)
    print(f"\n14 个模式:")
    for k, v in CAREER_MODES.items():
        print(f"  {k:20s} - {v}")
    print(f"\n6 个 Archetypes:")
    for k, v in ARCHETYPES.items():
        print(f"  {k:15s} - {v}")
    print(f"\nA-G 评分示例:")
    score = JobScore(
        role_fit=8.5, seniority_match=9.0, domain_match=7.5,
        skills_match=8.0, experience_match=9.0, culture_fit=7.0,
        growth_potential=9.0, network_value=8.0,
        comp_competitiveness=7.5, comp_transparency=6.0,
        location_remote=9.0, company_stability=8.0,
        legitimacy=9.0,
    )
    print(f"  Total: {score.total} | Grade: {score.grade}")
    print(f"\nPipeline stages: {' → '.join(PIPELINE_STAGES)}")
