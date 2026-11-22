# -*- coding: utf-8 -*-
"""
总府川宾可研报告 - DeepSeek 评估报告生成器
B166ER · 2026-08-01 13:00 GMT+8
按 Eric 显式指令: 用 DeepSeek 生成评估报告 + 输出 PDF
"""
import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

# === 评估报告上下文数据 ===
EVAL_CONTEXT = {
    "project_name": "总府四川宾馆改造项目",
    "project_简称": "总府川宾",
    "evaluation_date": datetime.now().strftime("%Y-%m-%d"),
    "evaluator": "DeepSeek Chat (深度求索) + B166ER 协助",
    "report_being_evaluated": {
        "name": "总府四川宾馆改造项目可行性分析报告（7.13）",
        "pages": 77,
        "compilation_unit": "四川锦江旅游饭店管理有限责任公司（集团子公司）",
        "compilation_date": "2026年7月",
    },
    "project_basics": {
        "location": "成都市锦江区总府街 31 号",
        "total_area_sqm": 12155,
        "hotel_area_sqm": 10484,
        "leased_area_sqm": 1671,
        "buildings": "1961 年西楼砖混 + 1988 年南楼砖混",
        "current_status": "2019/5 因重大安全隐患停业，至今 7 年",
        "renovation_target": "总府四川宾馆（品牌重塑）",
        "rooms_target": 165,
        "room_size_target_m2": "24-28 主力房型",
    },
    "investment": {
        "total_wan": 4932.26,
        "decoration_wan": 2814.86,
        "equipment_wan": 998.10,
        "waterproof_wan": 43.47,
        "design_supervision_wan": 578.58,
        "other_engineering_wan": 256.11,
        "startup_wan": 241.13,
    },
    "operating_model": {
        "lessor": "四川锦弘集团有限责任公司（旅投集团全资子公司）",
        "lessee": "安逸酒店集团有限责任公司",
        "operator": "四川锦江旅游饭店管理有限责任公司",
        "lease_term_years": 15,
        "operating_period": "2027/5/1 至 2041/12/31",
        "rent_structure": "max(25% 营收分成, 12,155㎡ × 50 元/㎡/月 保底)",
        "rent_floor_annual_wan": 729.36,
        "rent_floor_pct_of_revenue": "稳定期约 27%",
    },
    "financial_assumptions": {
        "adr_stable_yuan": 520,
        "occ_y1": 0.745,
        "occ_y2": 0.826,
        "occ_stable": 0.856,
        "revpar_stable_yuan": 445,
        "room_revenue_stable_wan": 2679,
        "direct_cost_rate": 0.305,
        "gop_rate": 0.43,
        "ebitda_stable_wan": 466,
        "payback_years": 11,
        "irr": 0.0406,
        "npv_wan": 169.1,
        "lpr_5y": 0.035,
    },
    "competitors": {
        "tier1_count": 6,
        "tier1_adr_mean": 535,
        "tier1_occ_mean": 0.9025,
        "tier1_revpar_mean": 483,
        "key_competitors": [
            "蓉福朋喜来登 (万豪, 322 间, ADR 483, Occ 81%)",
            "太古里春熙路步行街城际 (华住, 210 间, ADR 489, Occ 92.5%)",
            "蓉希尔顿花园 (希尔顿, 174 间, ADR 550, Occ 95%)",
            "pagoda 君亭设计 (君亭, 206 间, ADR 660, Occ 88%)",
            "蓉希尔顿欢朋 (希尔顿, 253 间, ADR 523, Occ 93%)",
            "太古里春熙美居 (华住雅高, 374 间, ADR 505, Occ 92%)",
        ],
    },
    "policy_window": {
        "city_renewal": "成都市城市更新条例 (2026/6/1 长期)",
        "lodging_quality": "成都市住宿业高质量发展措施 (2025/12/30-2030/12/29, 最高 10 万补助)",
        "jinjiang_equipment": "锦江区设备更新补贴 (2025/10/16-2026/12/31, 5/8/10 万分级, **即将到期**)",
    },
    "key_findings_to_evaluate": [
        "ADR 520 元 vs 房型面积 24-28㎡ (市场平均 27-45㎡) - 价格支撑是否充分？",
        "Occ 成熟期 85.6% 假设是否过于乐观？(1961 砖混老楼 + 7 年停业)",
        "餐饮/会议剥离给总府皇冠假日 - 利润结构单一风险",
        "租金保底 50 元/㎡/月 vs 营收分成 25% - 缺乏敏感性测试",
        "IRR 4.06% 与 LPR 3.5% 比较 - 是否应用 WACC 而非 LPR？",
        "5km 6 家直接竞品 vs 报告自承 3km 1,823 家酒店 - 市场调研范围是否过窄？",
        "缺敏感性分析 (单变量/多变量)",
        "缺三情景分析 (悲观/基准/乐观)",
        "缺盈亏平衡分析",
        "缺 Monte Carlo 概率分析",
        "缺客源结构分析 (OTA/协议/会议/散客)",
        "缺品牌重塑风险评估",
        "缺退出风险评估 (15 年期满)",
        "缺集团最大补贴需求测算",
        "缺现金流断裂风险评估",
    ],
    "evaluation_framework": "国际通用方法论 (HVS / PKF / Cushman & Wakefield) + 国资委合规要求 + 集团内部决策需要",
}

PROMPT_TEMPLATE = """你是一位资深酒店投资可行性研究评估专家，请对《{project_name}》的可行性研究报告进行专业、独立、严谨的第三方评估。

## 评估对象
- **报告名称**：{report_name}
- **编制单位**：{compilation_unit}
- **编制日期**：{compilation_date}
- **报告页数**：{report_pages} 页

## 项目基本信息
- 位置：{location}
- 总建筑面积：{total_area_sqm}㎡（酒店自持 {hotel_area_sqm}㎡ + 外租 {leased_area_sqm}㎡）
- 物业历史：{buildings}
- 当前状态：{current_status}
- 改造目标：客房 {rooms_target} 间，主力房型 {room_size_target_m2}

## 投资估算（合计 {total_investment_wan} 万元）
- 装饰工程：{decoration_wan} 万元
- 设备费用：{equipment_wan} 万元
- 防水工程：{waterproof_wan} 万元
- 设计监理：{design_supervision_wan} 万元
- 其他工程：{other_engineering_wan} 万元
- 开办费：{startup_wan} 万元

## 经营模式
- 出租方：{lessor}
- 承租方：{lessee}
- 运营方：{operator}
- 租赁期：{lease_term_years} 年
- 运营期：{operating_period}
- 租金结构：{rent_structure}
- 保底年租：{rent_floor_annual_wan} 万元（占稳定期营收 {rent_floor_pct_of_revenue}）

## 财务测算核心数据
- 稳定期 ADR：{adr_stable_yuan} 元/间·夜
- 入住率假设：Y1 {occ_y1} → Y2 {occ_y2} → 稳态 {occ_stable}
- 稳定期 RevPAR：{revpar_stable_yuan} 元
- 客房年收入：{room_revenue_stable_wan} 万元（含税）
- 直接成本率：{direct_cost_rate}
- GOP 率：{gop_rate}
- EBITDA：{ebitda_stable_wan} 万元
- 投资回收期：{payback_years} 年
- IRR：{irr}（vs LPR {lpr_5y}）
- NPV：{npv_wan} 万元

## 主要竞品（Tier 1 直接竞品，6 家）
{tier1_competitors_list}

**Tier 1 加权均值**：ADR {tier1_adr_mean} 元，Occ {tier1_occ_mean}，RevPAR {tier1_revpar_mean} 元

## 关键政策窗口
- {city_renewal}
- {lodging_quality}
- {jinjiang_equipment}

## 评估重点（14 项）
{key_findings_list}

## 评估框架
请按**国际通用酒店投资可研方法论**（HVS / PKF / Cushman & Wakefield 标准） + **国资委合规要求** + **集团内部决策需要** 进行评估。

## 输出要求

请生成一份**完整、专业、严谨**的评估报告，要求：

1. **结构完整**：包含封面、目录、摘要、背景、方法论、各章节评估、风险评估、结论与建议、附录
2. **数据严谨**：所有结论必须有数据支撑，明确数据来源（报告原文 vs 行业基准 vs 推算）
3. **方法论标准**：参照国际通用方法论框架（HVS / PKF / Cushman & Wakefield），指出报告在敏感性分析、情景分析、盈亏平衡、概率分析、风险量化等方面的缺失
4. **客观独立**：以第三方评估专家视角，客观指出报告的优点和不足，**不偏袒编制单位**
5. **可操作**：每条评估意见都要给出具体改进建议
6. **量化分析**：尽可能给出量化对比（如 IRR 敏感性区间、敏感性分析示例、租金敏感性影响等）
7. **结论明确**：综合评分 + 是否可行 + 启动条件

## 报告结构建议

```
封面页
目录
执行摘要（1 页）
第一章 评估背景与项目概况
  1.1 评估背景
  1.2 评估依据与数据来源
  1.3 项目基本情况
第二章 评估方法论
  2.1 评估框架（国际标准 + 国资委要求 + 集团决策需要）
  2.2 评估指标体系
  2.3 评估流程
第三章 项目市场分析与定位评估
  3.1 宏观与区域市场分析评价
  3.2 竞对分析评价
  3.3 客源结构分析评价
  3.4 项目定位评价
第四章 投资估算与财务测算评估
  4.1 投资估算评价
  4.2 收入预测评价
  4.3 成本预测评价
  4.4 财务指标评价（IRR/NPV/回收期）
  4.5 财务测算方法论评价（敏感性/情景/盈亏/概率）
第五章 风险评估
  5.1 市场风险
  5.2 经营风险
  5.3 财务风险（含租金敏感性）
  5.4 合规风险（含国资委/三重一大）
  5.5 品牌重塑风险
  5.6 退出风险
第六章 合规与治理评估
  6.1 关联方定价合规
  6.2 国资委监管要求
  6.3 三重一大决策程序
第七章 综合评估结论
  7.1 综合评分
  7.2 是否可行的结论
  7.3 启动条件与改进要求
第八章 改进建议与下一步行动
附录 A: 数据来源说明
附录 B: 方法论差异说明（vs 国际标准）
附录 C: 关键指标对比表
```

**字数要求**：15000-20000 字（中文字符）
**输出格式**：Markdown（标题层级清晰，表格规范）
**语言**：中文，专业书面语

请直接输出完整报告内容，不要输出"以下是报告"之类的元描述。
"""


def build_prompt():
    """构建 DeepSeek prompt"""
    ctx = EVAL_CONTEXT
    tier1_list = "\n".join(f"- {c}" for c in ctx["competitors"]["key_competitors"])
    findings_list = "\n".join(f"{i+1}. {f}" for i, f in enumerate(ctx["key_findings_to_evaluate"]))

    return PROMPT_TEMPLATE.format(
        project_name=ctx["project_name"],
        report_name=ctx["report_being_evaluated"]["name"],
        compilation_unit=ctx["report_being_evaluated"]["compilation_unit"],
        compilation_date=ctx["report_being_evaluated"]["compilation_date"],
        report_pages=ctx["report_being_evaluated"]["pages"],
        location=ctx["project_basics"]["location"],
        total_area_sqm=f"{ctx['project_basics']['total_area_sqm']:,}",
        hotel_area_sqm=f"{ctx['project_basics']['hotel_area_sqm']:,}",
        leased_area_sqm=f"{ctx['project_basics']['leased_area_sqm']:,}",
        buildings=ctx["project_basics"]["buildings"],
        current_status=ctx["project_basics"]["current_status"],
        rooms_target=ctx["project_basics"]["rooms_target"],
        room_size_target_m2=ctx["project_basics"]["room_size_target_m2"],
        total_investment_wan=ctx["investment"]["total_wan"],
        decoration_wan=ctx["investment"]["decoration_wan"],
        equipment_wan=ctx["investment"]["equipment_wan"],
        waterproof_wan=ctx["investment"]["waterproof_wan"],
        design_supervision_wan=ctx["investment"]["design_supervision_wan"],
        other_engineering_wan=ctx["investment"]["other_engineering_wan"],
        startup_wan=ctx["investment"]["startup_wan"],
        lessor=ctx["operating_model"]["lessor"],
        lessee=ctx["operating_model"]["lessee"],
        operator=ctx["operating_model"]["operator"],
        lease_term_years=ctx["operating_model"]["lease_term_years"],
        operating_period=ctx["operating_model"]["operating_period"],
        rent_structure=ctx["operating_model"]["rent_structure"],
        rent_floor_annual_wan=ctx["operating_model"]["rent_floor_annual_wan"],
        rent_floor_pct_of_revenue=ctx["operating_model"]["rent_floor_pct_of_revenue"],
        adr_stable_yuan=ctx["financial_assumptions"]["adr_stable_yuan"],
        occ_y1=f"{ctx['financial_assumptions']['occ_y1']*100:.1f}%",
        occ_y2=f"{ctx['financial_assumptions']['occ_y2']*100:.1f}%",
        occ_stable=f"{ctx['financial_assumptions']['occ_stable']*100:.1f}%",
        revpar_stable_yuan=ctx["financial_assumptions"]["revpar_stable_yuan"],
        room_revenue_stable_wan=ctx["financial_assumptions"]["room_revenue_stable_wan"],
        direct_cost_rate=f"{ctx['financial_assumptions']['direct_cost_rate']*100:.1f}%",
        gop_rate=f"{ctx['financial_assumptions']['gop_rate']*100:.1f}%",
        ebitda_stable_wan=ctx["financial_assumptions"]["ebitda_stable_wan"],
        payback_years=ctx["financial_assumptions"]["payback_years"],
        irr=f"{ctx['financial_assumptions']['irr']*100:.2f}%",
        npv_wan=ctx["financial_assumptions"]["npv_wan"],
        lpr_5y=f"{ctx['financial_assumptions']['lpr_5y']*100:.1f}%",
        tier1_competitors_list=tier1_list,
        tier1_adr_mean=ctx["competitors"]["tier1_adr_mean"],
        tier1_occ_mean=f"{ctx['competitors']['tier1_occ_mean']*100:.2f}%",
        tier1_revpar_mean=ctx["competitors"]["tier1_revpar_mean"],
        city_renewal=ctx["policy_window"]["city_renewal"],
        lodging_quality=ctx["policy_window"]["lodging_quality"],
        jinjiang_equipment=ctx["policy_window"]["jinjiang_equipment"],
        key_findings_list=findings_list,
    )


def call_deepseek(prompt: str, max_tokens: 16000) -> str:
    """调用 DeepSeek API"""
    if not DEEPSEEK_API_KEY:
        raise ValueError("DEEPSEEK_API_KEY 环境变量未设置")

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "你是一位资深酒店投资可行性研究评估专家，拥有 20 年行业经验，熟悉国际通用方法论（HVS / PKF / Cushman & Wakefield）、国资委监管要求、酒店集团决策机制。你的评估报告以专业、严谨、独立、可操作著称。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3,
        "stream": False,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    }

    print(f"[调用 DeepSeek API...]")
    print(f"  Model: deepseek-chat")
    print(f"  Max tokens: {max_tokens}")
    print(f"  Prompt length: {len(prompt)} chars")

    req = urllib.request.Request(
        DEEPSEEK_API_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            content = data['choices'][0]['message']['content']
            usage = data.get('usage', {})
            print(f"  [完成] 输入 tokens: {usage.get('prompt_tokens', '?')}")
            print(f"  [完成] 输出 tokens: {usage.get('completion_tokens', '?')}")
            print(f"  [完成] 输出长度: {len(content)} chars")
            return content
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        print(f"  [HTTP Error] {e.code}: {body[:500]}")
        raise
    except Exception as e:
        print(f"  [Error] {e}")
        raise


def main():
    print("=" * 80)
    print("  总府川宾可研报告 - DeepSeek 评估报告生成")
    print(f"  Time: {datetime.now().isoformat()}")
    print("=" * 80)

    # 1. 构建 prompt
    prompt = build_prompt()
    print(f"\n[1] Prompt 构建完成 ({len(prompt)} chars)")

    # 2. 调用 DeepSeek
    content = call_deepseek(prompt, max_tokens=16000)

    # 3. 保存 MD
    timestamp = datetime.now().strftime("%Y-%m-%d")
    output_md = WORKSPACE / 'anyi-ops-kb' / '02_项目' / '总府四川宾馆' / f'评估报告_DeepSeek_{timestamp}.md'
    output_md.parent.mkdir(parents=True, exist_ok=True)

    header = f"""# 总府四川宾馆改造项目可行性研究报告 — 第三方评估报告

> **评估对象**：总府四川宾馆改造项目可行性分析报告（7.13）
> **评估人**：DeepSeek Chat (深度求索) + B166ER 协助
> **评估日期**：{timestamp}
> **报告类型**：独立第三方评估

---

"""

    full_content = header + content

    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(full_content)
    print(f"\n[2] MD 已保存: {output_md}")
    print(f"    Size: {len(full_content.encode('utf-8'))} bytes")

    return output_md


if __name__ == '__main__':
    main()