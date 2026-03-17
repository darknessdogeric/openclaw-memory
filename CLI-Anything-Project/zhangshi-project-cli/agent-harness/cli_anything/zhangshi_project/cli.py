"""Zhang Shi Project Control Center CLI

Manage all projects from command line.
"""

import click
import sys
from datetime import datetime, timedelta

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Project Database
PROJECTS = {
    "01-自媒体计划": {
        "status": "启动准备",
        "priority": "⭐⭐⭐",
        "path": "/01-自媒体计划/",
        "milestones": ["内容规划", "账号搭建", "首批发布"],
        "next_action": "待AHL融资后启动"
    },
    "02-人寿医养酒店": {
        "status": "资金待到位",
        "priority": "⭐⭐",
        "path": "/02-人寿医养酒店计划/",
        "milestones": ["资金到位", "选址确定", "设计启动"],
        "next_action": "等待人寿资金"
    },
    "03-AI单体酒店赋能": {
        "status": "资料完备",
        "priority": "⭐⭐⭐",
        "path": "/03-AI单体酒店赋能/",
        "milestones": ["重宾国际改造", "AI工具部署", "效果验证"],
        "next_action": "推进重宾国际项目"
    },
    "04-AI赋能部门SOP": {
        "status": "资料完备",
        "priority": "⭐⭐⭐",
        "path": "/04-AI赋能部门SOP/",
        "milestones": ["11个部门SOP", "AI工具集成", "培训交付"],
        "next_action": "持续优化SOP"
    },
    "05-AHL去中心化旅行平台": {
        "status": "核心项目",
        "priority": "⭐⭐⭐⭐⭐",
        "path": "/05-AHL-去中心化旅行平台/",
        "milestones": ["种子轮融资", "MVP开发", "大理0号实验室", "苏州酒管项目"],
        "next_action": "推进融资+苏州项目实施"
    },
    "06-电子潮玩周边": {
        "status": "概念阶段",
        "priority": "⭐",
        "path": "/06-电子潮玩周边计划/",
        "milestones": ["市场调研", "供应链搭建", "首批产品"],
        "next_action": "低优先级"
    },
    "07-美国跨境电商": {
        "status": "概念阶段",
        "priority": "⭐",
        "path": "/07-美国跨境电商计划/",
        "milestones": ["星旗智造规划", "平台选择", "首批出货"],
        "next_action": "低优先级"
    },
}

# Milestones
MILESTONES = [
    {"date": "2026-03-23", "project": "苏州酒管项目", "event": "Phase 1启动", "status": "即将到来"},
    {"date": "2026-03-31", "project": "AHL", "event": "融资材料最终版", "status": "待完成"},
    {"date": "2026-04-15", "project": "AHL", "event": "首批投资人会议", "status": "计划中"},
    {"date": "2026-04-30", "project": "AHL", "event": "种子轮融资截止", "status": "关键节点"},
]

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """张实项目总控中心 CLI
    
    管理所有项目、查看进度、跟踪里程碑
    """
    pass

@cli.command()
def list():
    """列出所有项目"""
    click.echo("\n" + "="*70)
    click.echo("张实项目总控中心 - 项目清单")
    click.echo("="*70)
    
    for name, info in PROJECTS.items():
        status_emoji = {"核心项目": "🔥", "资料完备": "✅", "启动准备": "🟡", 
                       "资金待到位": "⏳", "概念阶段": "💡"}.get(info["status"], "📋")
        click.echo(f"\n{status_emoji} {name}")
        click.echo(f"   状态: {info['status']} | 优先级: {info['priority']}")
        click.echo(f"   下一步: {info['next_action']}")
    
    click.echo("\n" + "="*70)
    click.echo(f"总计: {len(PROJECTS)}个项目")

@cli.command()
@click.argument('project_id')
def show(project_id):
    """查看指定项目详情"""
    # 支持模糊匹配
    matched = None
    for name, info in PROJECTS.items():
        if project_id in name or project_id in info["path"]:
            matched = (name, info)
            break
    
    if not matched:
        click.echo(f"错误: 未找到项目 '{project_id}'")
        return
    
    name, info = matched
    click.echo("\n" + "="*70)
    click.echo(f"项目详情: {name}")
    click.echo("="*70)
    click.echo(f"状态: {info['status']}")
    click.echo(f"优先级: {info['priority']}")
    click.echo(f"路径: {info['path']}")
    click.echo(f"\n关键里程碑:")
    for i, ms in enumerate(info['milestones'], 1):
        click.echo(f"   {i}. {ms}")
    click.echo(f"\n下一步行动: {info['next_action']}")
    click.echo("="*70)

@cli.command()
def milestones():
    """查看近期里程碑"""
    click.echo("\n" + "="*70)
    click.echo("近期里程碑")
    click.echo("="*70)
    
    today = datetime.now()
    
    for ms in sorted(MILESTONES, key=lambda x: x["date"]):
        ms_date = datetime.strptime(ms["date"], "%Y-%m-%d")
        days_left = (ms_date - today).days
        
        if days_left < 0:
            status = "已过期"
            emoji = "⚠️"
        elif days_left <= 7:
            status = "紧急"
            emoji = "🔥"
        elif days_left <= 30:
            status = "临近"
            emoji = "📅"
        else:
            status = "计划中"
            emoji = "📌"
        
        click.echo(f"\n{emoji} {ms['date']} ({days_left}天)")
        click.echo(f"   项目: {ms['project']}")
        click.echo(f"   事件: {ms['event']}")
        click.echo(f"   状态: {status}")
    
    click.echo("\n" + "="*70)

@cli.command()
def priority():
    """查看优先级排序"""
    click.echo("\n" + "="*70)
    click.echo("项目优先级排序")
    click.echo("="*70)
    
    priority_order = ["⭐⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"]
    
    for p in priority_order:
        projects = [(n, i) for n, i in PROJECTS.items() if i["priority"] == p]
        if projects:
            click.echo(f"\n优先级 {p}:")
            for name, info in projects:
                click.echo(f"   • {name} ({info['status']})")
    
    click.echo("\n" + "="*70)

@cli.command()
def dashboard():
    """显示项目总览仪表盘"""
    click.echo("\n" + "="*70)
    click.echo("张实项目总控中心 - 仪表盘")
    click.echo("="*70)
    
    # 统计
    total = len(PROJECTS)
    by_status = {}
    for info in PROJECTS.values():
        s = info["status"]
        by_status[s] = by_status.get(s, 0) + 1
    
    click.echo(f"\n📊 项目统计:")
    click.echo(f"   总计: {total}个项目")
    for status, count in sorted(by_status.items(), key=lambda x: -x[1]):
        bar = "█" * count
        click.echo(f"   {status:12} {bar} ({count})")
    
    # 高优先级项目
    click.echo(f"\n🔥 高优先级项目 (⭐⭐⭐以上):")
    for name, info in PROJECTS.items():
        if "⭐⭐⭐" in info["priority"]:
            click.echo(f"   • {name}")
    
    # 即将到期
    click.echo(f"\n📅 即将到期 (7天内):")
    today = datetime.now()
    urgent = []
    for ms in MILESTONES:
        ms_date = datetime.strptime(ms["date"], "%Y-%m-%d")
        days = (ms_date - today).days
        if 0 <= days <= 7:
            urgent.append((ms, days))
    
    if urgent:
        for ms, days in urgent:
            click.echo(f"   ⚠️ {ms['date']} ({days}天) - {ms['project']}: {ms['event']}")
    else:
        click.echo("   无紧急事项")
    
    click.echo("\n" + "="*70)

@cli.command()
@click.argument('keyword')
def search(keyword):
    """搜索项目"""
    click.echo(f"\n搜索: '{keyword}'")
    click.echo("="*70)
    
    results = []
    for name, info in PROJECTS.items():
        if (keyword.lower() in name.lower() or 
            keyword.lower() in info["next_action"].lower() or
            any(keyword.lower() in ms.lower() for ms in info["milestones"])):
            results.append((name, info))
    
    if not results:
        click.echo("未找到匹配项目")
        return
    
    for name, info in results:
        click.echo(f"\n📋 {name}")
        click.echo(f"   状态: {info['status']} | 优先级: {info['priority']}")
    
    click.echo(f"\n{'='*70}")
    click.echo(f"找到 {len(results)} 个匹配项目")

def main():
    cli()

if __name__ == '__main__':
    main()
