#!/usr/bin/env python3
"""
生成 6 个 PPT 场景模板 (Kimi 官方场景 → 我们的 brief + 12 套风格映射)
每个场景 = 一个完整的 plan.json 骨架, 已内置 brief (5 参数) + 页面序列
用法: python scripts/make_scenarios.py [输出目录]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets" / "scenarios"

SCENARIOS = {
    "01_工作汇报": {
        "kimi_prompt": "我把这季度门店销售数据转成word文档转成10页PPT，商业风格，突出增长趋势",
        "name": "工作汇报",
        "brief": {
            "total_slides": 10,
            "style_preset": "corporate_pro",
            "audience": {
                "who": "直属上级与跨部门负责人",
                "knows": "本季度的业务盘子与日常经营数据",
                "wants": "确认本季度执行是否到位、下季度资源该往哪投",
                "action": "当场同意或调整下季度的资源分配方案",
            },
            "required_sections": [
                {"name": "结论先行", "conclusion": "本季度整体达标，但增长集中在两个门店", "slides": 1},
                {"name": "核心数据", "conclusion": "营收同比 +18%，其中 62% 来自两家标杆店", "slides": 2},
                {"name": "增长拆解", "conclusion": "增量来自房价而非入住率，出租率反而下滑 3pp", "slides": 2},
                {"name": "问题定位", "conclusion": "出租率下滑集中在新改造的 6 家店", "slides": 2},
                {"name": "行动建议", "conclusion": "6 家店进入二次调优，两家标杆店输出 SOP", "slides": 3},
            ],
            "data_sources": [
                {"type": "internal", "where": "本季度门店经营台账 (Word/Excel)", "confidence": "🟢🟢 一手"},
                {"type": "internal", "where": "去年同期同口径数据", "confidence": "🟢🟢 一手"},
            ],
            "explicit_constraints": [
                "不出现个人绩效排名",
                "同比与环比口径必须标注",
                "所有对比用同口径",
            ],
            "success_check": "听众能复述'增长来自哪两家、问题出在哪六家、下季度先动哪里'",
        },
        "pages": [
            ("cover", "结论先行", "开场给结论, 不给目录"),
            ("dashboard", "核心数据总览", "3-4 个关键指标卡 + 同比"),
            ("chart", "增长拆解", "增长来源瀑布图"),
            ("comparison", "新老店对比", "改造店 vs 未改造店"),
            ("diagnostic", "问题定位", "6 家店出租率下滑归因"),
            ("path", "行动路径", "二次调优三步走"),
            ("cards", "标杆 SOP 输出", "两家标杆店的四条经验"),
            ("data", "资源分配建议", "下季度资源投向"),
            ("cards", "风险与预案", "三个风险 + 对应预案"),
            ("conclusion", "收尾", "要什么决策"),
        ],
    },
    "02_行业研究": {
        "kimi_prompt": "生成一份2025年中国新能源车市场分析PPT，包含竞争格局、技术路线、政策背景",
        "name": "行业研究",
        "brief": {
            "total_slides": 15,
            "style_preset": "light_consulting",
            "audience": {
                "who": "集团战略部与投委会",
                "knows": "本行业基本盘, 但不掌握最新竞争与政策变化",
                "wants": "判断这个赛道值不值得加大投入、往哪个细分押注",
                "action": "认可或否决加大投入的提案",
            },
            "required_sections": [
                {"name": "市场规模", "conclusion": "赛道规模 X 亿, 增速 Y%, 但集中在 Z 细分", "slides": 2},
                {"name": "竞争格局", "conclusion": "头部 3 家占 60% 份额, 且以价格战换份额", "slides": 3},
                {"name": "技术路线", "conclusion": "两条路线未定胜负, 押注需分散", "slides": 3},
                {"name": "政策背景", "conclusion": "补贴退坡但准入放松, 政策友好度中性偏正", "slides": 3},
                {"name": "趋势判断", "conclusion": "未来 3 年集中度会提升, 窗口在收缩", "slides": 4},
            ],
            "data_sources": [
                {"type": "web", "where": "行业协会年度报告 + 上市公司财报", "confidence": "🟡🟡 多源"},
                {"type": "web", "where": "政策原文 (发改委/工信部)", "confidence": "🟢🟢 一手"},
                {"type": "internal", "where": "我方在赛道的实际经营数据", "confidence": "🟢🟢 一手"},
            ],
            "explicit_constraints": [
                "所有市场规模数字标注来源与年份",
                "政策引用必须给出文号或发布日期",
                "预测一律给区间不给单点",
                "区分'事实'与'判断', 分别标注",
            ],
            "success_check": "听众能说出'赛道多大、谁赢了、我们该不该进'三个问题各自的答案",
        },
        "pages": [
            ("cover", "标题页", "赛道 + 时间 + 一句话结论"),
            ("data", "市场规模", "规模与增速"),
            ("chart", "规模细分", "细分赛道结构"),
            ("matrix", "竞争格局", "头部玩家 × 维度"),
            ("comparison", "份额对比", "CR3 集中度"),
            ("cards", "头部玩家画像", "3 家公司的打法"),
            ("cards", "技术路线 A", "路线特征与代表"),
            ("cards", "技术路线 B", "路线特征与代表"),
            ("comparison", "路线对比", "成本/成熟度/时间窗"),
            ("data", "政策梳理", "时间轴"),
            ("cards", "政策影响", "利好/中性/利空"),
            ("path", "演化路径", "3 年趋势推演"),
            ("diagnostic", "关键变量", "决定胜负的 3 个变量"),
            ("data", "机会测算", "可进入的细分空间"),
            ("conclusion", "结论与建议", "加投 / 不加投 / 换方向"),
        ],
    },
    "03_课程课件": {
        "kimi_prompt": "我做一份从AGENT入门到进阶的PPT，适合非技术背景的产品经理，15页左右",
        "name": "课程课件",
        "brief": {
            "total_slides": 15,
            "style_preset": "whiteboard_handdrawn",
            "audience": {
                "who": "非技术背景的产品经理 (10-20 人)",
                "knows": "会用 AI 对话, 但不懂技术原理",
                "wants": "理解 Agent 是什么、能干什么、怎么在自己业务里用起来",
                "action": "回去挑一个自己的业务场景试做一次",
            },
            "required_sections": [
                {"name": "是什么", "conclusion": "Agent = 会用工具并自己完成目标的 AI", "slides": 3},
                {"name": "和 ChatGPT 差在哪", "conclusion": "差在'能不能自己动手'，不在'能不能聊'", "slides": 3},
                {"name": "怎么用", "conclusion": "三步: 目标 / 工具 / 验收标准", "slides": 4},
                {"name": "案例", "conclusion": "一个产品经理本周就能跑通的例子", "slides": 3},
                {"name": "进阶", "conclusion": "多 Agent 协作与踩坑清单", "slides": 2},
            ],
            "data_sources": [
                {"type": "doc", "where": "讲义与真实产品截图 (脱敏)", "confidence": "🟢🟢 一手"},
                {"type": "demo", "where": "可现场演示的最小 Agent", "confidence": "🟢🟢 一手"},
            ],
            "explicit_constraints": [
                "全程用类比, 不用代码",
                "每个概念配一个产品经理 daily 的例子",
                "术语首次出现给一句话解释",
                "不做技术选型对比",
            ],
            "success_check": "学员能用自己的话向同事解释 Agent, 并说出一个能试的场景",
        },
        "pages": [
            ("cover", "封面", "标题 + 一句话承诺"),
            ("diagnostic", "今天解决什么", "3 个具体问题"),
            ("cards", "Agent 是什么", "3 个要素"),
            ("comparison", "ChatGPT vs Agent", "对话 vs 动手"),
            ("path", "Agent 干活三步", "目标/工具/验收"),
            ("cards", "工具长什么样", "工具即能力"),
            ("cards", "案例 1: 竞品日报", "从需求到产出"),
            ("cards", "案例 2: 需求文档", "从需求到产出"),
            ("cards", "案例 3: 客服话术", "从需求到产出"),
            ("diagnostic", "最容易踩的 3 个坑", "越权/幻觉/不验收"),
            ("cards", "验收标准怎么写", "可判定的标准"),
            ("data", "能力与场景矩阵", "什么场景值得上"),
            ("cards", "进阶: 多 Agent", "什么时候需要"),
            ("cards", "进阶: 资源准备", "需要什么账号/权限"),
            ("conclusion", "行动清单", "本周做一件事"),
        ],
    },
    "04_产品发布": {
        "kimi_prompt": "为一次AI写作工具产品发布会制作演示PPT，包含痛点、解决方案、核心功能、定价",
        "name": "产品发布",
        "brief": {
            "total_slides": 12,
            "style_preset": "gradient_modern",
            "audience": {
                "who": "发布会现场 + 线上看直播的潜在客户与媒体",
                "knows": "知道 AI 写作这个品类存在, 但没用过我们的产品",
                "wants": "相信这个产品真能解决我的问题, 并记住它叫什么",
                "action": "发布会后试用并进入付费转化流程",
            },
            "required_sections": [
                {"name": "痛点", "conclusion": "写不出来不是能力问题, 是流程问题", "slides": 2},
                {"name": "解决方案", "conclusion": "把写作拆成 5 步, 每步都有 AI 兜底", "slides": 2},
                {"name": "核心功能", "conclusion": "3 个功能构成闭环, 单个都不够", "slides": 3},
                {"name": "定价", "conclusion": "按坐席收费, 不按字数, 无隐藏项", "slides": 2},
                {"name": "行动", "conclusion": "现场扫码领 30 天全功能", "slides": 3},
            ],
            "data_sources": [
                {"type": "internal", "where": "产品实测录屏 + 前后对比数据", "confidence": "🟢🟢 一手"},
                {"type": "internal", "where": "定价表与套餐", "confidence": "🟢🟢 一手"},
                {"type": "web", "where": "品类市场数据 (发布会背景)", "confidence": "🟡🟡 多源"},
            ],
            "explicit_constraints": [
                "不承诺未上线功能",
                "竞品不点名比较",
                "价格必须与销售口径一致",
                "涉及客户名的必须已获授权",
            ],
            "success_check": "观众能复述产品名、3 个核心功能、起步价, 并知道下一步做什么",
        },
        "pages": [
            ("cover", "封面", "产品名 + 一句话"),
            ("cards", "痛点 1", "写不出来"),
            ("cards", "痛点 2", "改不完"),
            ("path", "解决方案总览", "5 步流程"),
            ("cards", "核心功能 1", "功能 + 演示"),
            ("cards", "核心功能 2", "功能 + 演示"),
            ("cards", "核心功能 3", "功能 + 演示"),
            ("comparison", "使用前后对比", "同一篇稿子"),
            ("data", "效率数据", "时间与质量"),
            ("cards", "定价方案", "套餐表"),
            ("cards", "客户证言", "2 条"),
            ("conclusion", "行动号召", "扫码 + 落地页"),
        ],
    },
    "05_提案融资": {
        "kimi_prompt": "我把这份商业计划书PDF转成融资路演PPT，突出市场规模和团队优势",
        "name": "提案融资",
        "brief": {
            "total_slides": 12,
            "style_preset": "startup_roadshow",
            "audience": {
                "who": "投资人 (机构合伙人 + 独立投资人)",
                "knows": "赛道常识, 不了解我们的具体能力",
                "wants": "判断这个团队能不能拿下这个大市场, 值不值得投",
                "action": "进入下一轮尽调 / 本轮打钩",
            },
            "required_sections": [
                {"name": "问题", "conclusion": "一个每年重复 N 次、人力成本极高的结构性浪费", "slides": 2},
                {"name": "方案", "conclusion": "用协议层直接撮合供需, 砍掉中间环节", "slides": 2},
                {"name": "市场规模", "conclusion": "TAM X 亿, 我们先吃 SAM Y 亿", "slides": 2},
                {"name": "团队与壁垒", "conclusion": "行业积累 + 唯一的数据/渠道资产, 别人复制不了", "slides": 3},
                {"name": "融资", "conclusion": "本轮融 X 千万, 18 个月跑到 Y 里程碑", "slides": 3},
            ],
            "data_sources": [
                {"type": "doc", "where": "商业计划书 PDF", "confidence": "🟢🟢 一手"},
                {"type": "web", "where": "市场研究报告 (TAM/SAM)", "confidence": "🟡🟡 多源"},
                {"type": "internal", "where": "已签客户/试点数据 (需脱敏)", "confidence": "🟢🟢 一手"},
            ],
            "explicit_constraints": [
                "不披露未公开客户名单, 用行业描述替代",
                "TAM/SAM/SOM 口径必须写明",
                "财务预测标注假设",
                "不承诺回购或保底条款",
            ],
            "success_check": "投资人能复述'什么问题、凭什么你们、融多少换什么'",
        },
        "pages": [
            ("cover", "封面", "公司/项目 + 一句话"),
            ("cards", "问题", "痛点 + 量化"),
            ("data", "问题规模", "浪费的总量"),
            ("path", "解决方案", "链路对比"),
            ("cards", "产品形态", "怎么用"),
            ("data", "市场规模", "TAM/SAM/SOM"),
            ("comparison", "竞争格局", "我们 vs 现有方案"),
            ("cards", "壁垒", "3 条不可复制"),
            ("cards", "团队", "履历 + 分工"),
            ("data", "里程碑与指标", "18 个月"),
            ("cards", "融资计划", "用途 + 里程碑"),
            ("conclusion", "收尾", "联系方式 + 一句话"),
        ],
    },
    "06_长文转化": {
        "kimi_prompt": "我有一篇十万字的研究报告，帮我提炼成20页图文并茂的汇报PPT",
        "name": "长文转化",
        "brief": {
            "total_slides": 20,
            "style_preset": "data_viz_pro",
            "audience": {
                "who": "需要向上汇报或对外分享的汇报人 + 其听众",
                "knows": "读过报告, 但不记得细节",
                "wants": "用 20 页抓住报告的核心论据与关键数据",
                "action": "认可这份提炼, 并采用其中的数据与结论",
            },
            "required_sections": [
                {"name": "摘要", "conclusion": "报告的 3 个核心结论, 每个一句话", "slides": 2},
                {"name": "研究框架", "conclusion": "全文的 4 部分结构与论证路径", "slides": 2},
                {"name": "关键论据 1", "conclusion": "该部分最重要的一组数据与推论", "slides": 5},
                {"name": "关键论据 2", "conclusion": "同上", "slides": 5},
                {"name": "关键论据 3", "conclusion": "同上", "slides": 4},
                {"name": "结论与建议", "conclusion": "建议做什么, 依据哪几条", "slides": 2},
            ],
            "data_sources": [
                {"type": "doc", "where": "原始研究报告 (全文, 逐章读取)", "confidence": "🟢🟢 一手"},
                {"type": "doc", "where": "报告内图表原图 (可裁切复用)", "confidence": "🟢🟢 一手"},
            ],
            "explicit_constraints": [
                "所有数字必须能在原文中定位到出处",
                "不得添加原文没有的推论",
                "原文有相反结论时必须并列呈现",
                "摘要是提炼, 不是缩写",
            ],
            "success_check": "听众能凭这 20 页复述报告的全部核心结论, 且每个数字可回溯到原文",
        },
        "pages": [
            ("cover", "封面", "报告题目 + 副题"),
            ("cards", "三个核心结论", "3 条"),
            ("path", "研究框架", "4 部分"),
            ("data", "研究方法", "样本与口径"),
            ("cards", "论据组 1 概览", "小节标题"),
            ("data", "论据组 1 数据 1", "核心图"),
            ("data", "论据组 1 数据 2", "支撑图"),
            ("comparison", "论据组 1 对比", "A vs B"),
            ("cards", "论据组 1 推论", "这一组说明什么"),
            ("cards", "论据组 2 概览", "小节标题"),
            ("data", "论据组 2 数据 1", "核心图"),
            ("data", "论据组 2 数据 2", "支撑图"),
            ("comparison", "论据组 2 对比", "A vs B"),
            ("cards", "论据组 2 推论", "这一组说明什么"),
            ("cards", "论据组 3 概览", "小节标题"),
            ("data", "论据组 3 数据 1", "核心图"),
            ("data", "论据组 3 数据 2", "支撑图"),
            ("cards", "论据组 3 推论", "这一组说明什么"),
            ("cards", "反方观点", "原文相反结论"),
            ("conclusion", "结论与建议", "做什么 + 依据"),
        ],
    },
}


def build_plan(key, sc):
    pages = []
    for i, (ptype, name, goal) in enumerate(sc["pages"], 1):
        pages.append({
            "slide_number": i,
            "page_type": ptype,
            "page_goal": goal,
            "content": name,
            "style_preset": sc["brief"]["style_preset"],
            "text_density": "medium",
            "note": "TODO: 补 approved_text_lines / prompt_override",
        })
    total = len(pages)
    brief = dict(sc["brief"])
    brief["total_slides"] = total
    brief["scenario"] = sc["name"]
    brief["kimi_reference_prompt"] = sc["kimi_prompt"]
    return {
        "title": f"{sc['name']} PPT",
        "total_slides": total,
        "style_preset": brief["style_preset"],
        "style_goal": f"面向「{brief['audience']['who']}」的{sc['name']}演示",
        "image_provider": "runninghub_g31",
        "resolution": "4k",
        "aspect_ratio": "16:9",
        "brief": brief,
        "slides": pages,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for key, sc in SCENARIOS.items():
        plan = build_plan(key, sc)
        p = OUT / f"{key}.json"
        p.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] {p.name}  {plan['total_slides']} 页  preset={plan['style_preset']}")
    print(f"\n输出目录: {OUT}")
    print(f"共 {len(SCENARIOS)} 个场景模板")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
