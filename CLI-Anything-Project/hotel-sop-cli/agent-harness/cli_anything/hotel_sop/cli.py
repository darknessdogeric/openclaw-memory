"""Hotel SOP Query CLI

Command line interface for querying hotel PP&SOP knowledge base.
"""

import click
import sys
from pathlib import Path

# Fix Windows Unicode
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# SOP Knowledge Base (simplified in-memory structure)
SOP_DB = {
    "房务部": {
        "客房清洁": ["进房程序", "撤床程序", "铺床程序", "抹尘程序", "卫生间清洁", "吸尘程序", "查房程序"],
        "对客服务": ["迎送服务", "迷你吧服务", "洗衣服务", "加床服务", "叫醒服务", "遗留物品处理"],
        "布草管理": ["布草收发", "布草洗涤", "布草盘点", "报废标准"],
    },
    "餐饮部": {
        "餐厅服务": ["餐前准备", "迎宾领位", "点菜服务", "上菜程序", "巡台服务", "结账送客"],
        "宴会服务": ["婚宴", "寿宴", "宝宝宴", "商务宴", "乔迁宴", "战友聚会"],
        "厨房管理": ["原料验收", "粗加工", "切配", "烹饪", "出菜", "留样"],
    },
    "前厅部": {
        "预订服务": ["电话预订", "网络预订", "团体预订", "预订变更", "NO-SHOW处理"],
        "接待服务": ["散客入住", "团队入住", "VIP接待", "行李服务", "问询服务"],
        "收银服务": ["押金收取", "结账退房", "外币兑换", "发票开具", "夜审"],
    },
    "销售部": {
        "客户开发": ["电话拜访", "上门拜访", "协议签订", "客户档案", "CRM维护"],
        "会议销售": ["场地勘察", "方案报价", "合同签订", "会前协调", "会中服务", "会后跟进"],
        "OTA运营": ["房源优化", "定价策略", "促销活动", "评价管理", "数据分析"],
    },
    "财务部": {
        "收入审计": ["前台审计", "餐饮审计", "其他收入审计", "折扣审核", "免单审核"],
        "成本控制": ["采购审批", "库存管理", "成本核算", "报损处理", "盘点"],
        "报表编制": ["日报", "周报", "月报", "预算执行", "经营分析"],
    },
    "工程部": {
        "设备维护": ["空调系统", "电梯系统", "给排水", "强弱电", "消防系统"],
        "客房维修": ["报修接单", "上门维修", "紧急抢修", "维修记录", "配件管理"],
        "能源管理": ["用电监控", "用水监控", "用气监控", "节能措施"],
    },
    "安保部": {
        "门岗管理": ["人员进出", "车辆进出", "访客登记", "物品放行"],
        "巡逻检查": ["楼层巡逻", "外围巡逻", "监控查看", "异常处理"],
        "消防管理": ["设施检查", "演练组织", "火警处理", "疏散引导"],
    },
}

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """酒店SOP查询工具
    
    快速查询各部门标准操作程序(SOP)
    """
    pass

@cli.command()
def deps():
    """列出所有部门"""
    click.echo("\n" + "="*50)
    click.echo("酒店部门列表")
    click.echo("="*50)
    
    for i, dept in enumerate(SOP_DB.keys(), 1):
        category_count = len(SOP_DB[dept])
        total_sops = sum(len(items) for items in SOP_DB[dept].values())
        click.echo(f"{i}. {dept:10} ({category_count}个类别, {total_sops}个SOP)")
    
    click.echo("="*50)
    click.echo(f"\n总计: {len(SOP_DB)}个部门")

@cli.command()
@click.argument('department')
def cat(department):
    """查看指定部门的所有SOP类别"""
    if department not in SOP_DB:
        click.echo(f"错误: 未找到部门 '{department}'")
        click.echo(f"可用部门: {', '.join(SOP_DB.keys())}")
        return
    
    click.echo(f"\n{'='*50}")
    click.echo(f"{department} - SOP类别")
    click.echo("="*50)
    
    for category, sops in SOP_DB[department].items():
        click.echo(f"\n📁 {category}")
        for sop in sops:
            click.echo(f"   • {sop}")
    
    click.echo(f"\n{'='*50}")
    total = sum(len(items) for items in SOP_DB[department].values())
    click.echo(f"总计: {len(SOP_DB[department])}个类别, {total}个SOP")

@cli.command()
@click.argument('keyword')
def search(keyword):
    """按关键词搜索SOP"""
    click.echo(f"\n搜索关键词: '{keyword}'")
    click.echo("="*50)
    
    results = []
    for dept, categories in SOP_DB.items():
        for category, sops in categories.items():
            for sop in sops:
                if keyword.lower() in sop.lower() or keyword.lower() in category.lower():
                    results.append((dept, category, sop))
    
    if not results:
        click.echo("未找到匹配结果")
        return
    
    current_dept = None
    for dept, category, sop in results:
        if dept != current_dept:
            click.echo(f"\n🏢 {dept}")
            current_dept = dept
        click.echo(f"   📂 {category} → {sop}")
    
    click.echo(f"\n{'='*50}")
    click.echo(f"找到 {len(results)} 个匹配结果")

@cli.command()
@click.argument('department')
@click.argument('category')
def show(department, category):
    """显示指定SOP的详细内容"""
    if department not in SOP_DB:
        click.echo(f"错误: 未找到部门 '{department}'")
        return
    
    if category not in SOP_DB[department]:
        click.echo(f"错误: 未找到类别 '{category}'")
        click.echo(f"可用类别: {', '.join(SOP_DB[department].keys())}")
        return
    
    click.echo(f"\n{'='*60}")
    click.echo(f"{department} > {category}")
    click.echo("="*60)
    
    sops = SOP_DB[department][category]
    for i, sop in enumerate(sops, 1):
        click.echo(f"\n{i}. {sop}")
        click.echo("   " + "-"*40)
        # 模拟SOP内容
        steps = [
            "准备阶段: 检查工具/物料",
            "执行阶段: 按标准操作",
            "检查阶段: 质量确认",
            "记录阶段: 填写表单",
        ]
        for step in steps:
            click.echo(f"   ✓ {step}")
    
    click.echo(f"\n{'='*60}")

@cli.command()
def stats():
    """显示SOP知识库统计"""
    click.echo("\n" + "="*50)
    click.echo("PP&SOP知识库统计")
    click.echo("="*50)
    
    total_deps = len(SOP_DB)
    total_cats = sum(len(cats) for cats in SOP_DB.values())
    total_sops = sum(sum(len(items) for items in cats.values()) for cats in SOP_DB.values())
    
    click.echo(f"\n📊 总体统计:")
    click.echo(f"   部门数量: {total_deps}")
    click.echo(f"   类别数量: {total_cats}")
    click.echo(f"   SOP条目:  {total_sops}")
    
    click.echo(f"\n📈 部门分布:")
    for dept, categories in SOP_DB.items():
        cat_count = len(categories)
        sop_count = sum(len(items) for items in categories.values())
        bar = "█" * int(sop_count / 2)
        click.echo(f"   {dept:8} {bar} ({sop_count})")
    
    click.echo("\n" + "="*50)

def main():
    cli()

if __name__ == '__main__':
    main()
