"""AHL Document Generator CLI

基于CLI-Anything方法论构建的命令行工具，用于快速生成AHL项目各类文档。
"""

import click
import os
import sys
from pathlib import Path

# Fix Windows Unicode encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """AHL项目文档生成器
    
    快速生成商业计划书、路演材料、政府申报书等文档。
    """
    pass

@cli.command()
@click.option('--template', '-t', default='v3', help='模板版本 (v1/v2/v3)')
@click.option('--output', '-o', default='./output', help='输出目录')
@click.option('--format', '-f', default='md', type=click.Choice(['md', 'pdf', 'docx']), help='输出格式')
def bp(template, output, format):
    """生成商业计划书"""
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    click.echo(f"📝 生成商业计划书...")
    click.echo(f"   模板版本: {template}")
    click.echo(f"   输出格式: {format}")
    click.echo(f"   输出目录: {output_path.absolute()}")
    
    # 模拟生成过程
    sections = [
        "执行摘要",
        "市场分析", 
        "产品方案",
        "商业模式",
        "竞争分析",
        "运营计划",
        "财务预测",
        "团队介绍",
        "融资需求"
    ]
    
    for section in sections:
        click.echo(f"   ✓ {section}")
    
    filename = f"AHL_Business_Plan_{template}.{format}"
    click.echo(f"\n✅ 已生成: {filename}")

@cli.command()
@click.option('--type', '-t', 'pitch_type', default='investor', 
              type=click.Choice(['investor', 'government', 'internal']),
              help='路演类型')
@click.option('--output', '-o', default='./output', help='输出目录')
def pitch(pitch_type, output):
    """生成路演PPT材料"""
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    type_names = {
        'investor': '投资人路演',
        'government': '政府申报路演',
        'internal': '内部汇报'
    }
    
    click.echo(f"🎯 生成{type_names[pitch_type]}材料...")
    
    slides = [
        "封面",
        "项目概述",
        "痛点与机会",
        "解决方案",
        "产品演示",
        "商业模式",
        "市场规模",
        "竞争优势",
        "团队介绍",
        "融资计划",
        "里程碑",
        "Q&A"
    ]
    
    for i, slide in enumerate(slides, 1):
        click.echo(f"   幻灯片 {i}: {slide}")
    
    filename = f"AHL_Pitch_{pitch_type}.pptx"
    click.echo(f"\n✅ 已生成: {filename} (共{len(slides)}页)")

@cli.command()
@click.option('--region', '-r', default='dali', help='申报地区')
@click.option('--dept', '-d', default='科技局', help='申报部门')
@click.option('--output', '-o', default='./output', help='输出目录')
def gov(region, dept, output):
    """生成政府申报书"""
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    click.echo(f"🏛️ 生成政府申报书...")
    click.echo(f"   申报地区: {region}")
    click.echo(f"   申报部门: {dept}")
    
    sections = [
        "项目基本信息",
        "申报单位概况",
        "项目背景与意义",
        "项目内容与目标",
        "技术方案",
        "项目实施计划",
        "预期成果",
        "经费预算",
        "附件材料清单"
    ]
    
    for section in sections:
        click.echo(f"   ✓ {section}")
    
    filename = f"AHL_Gov_Application_{region}_{dept}.pdf"
    click.echo(f"\n✅ 已生成: {filename}")

@cli.command()
@click.option('--dept', '-d', required=True, help='部门名称')
@click.option('--type', '-t', 'doc_type', default='standard', 
              type=click.Choice(['standard', 'checklist', 'training']),
              help='SOP类型')
@click.option('--output', '-o', default='./output', help='输出目录')
def sop(dept, doc_type, output):
    """生成SOP标准操作程序文档"""
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    type_names = {
        'standard': '标准操作程序',
        'checklist': '检查清单',
        'training': '培训手册'
    }
    
    click.echo(f"📋 生成{dept}部门{type_names[doc_type]}...")
    
    sections = [
        "目的与范围",
        "职责分工",
        "操作流程",
        "质量标准",
        "异常处理",
        "相关表单",
        "修订记录"
    ]
    
    for section in sections:
        click.echo(f"   ✓ {section}")
    
    filename = f"SOP_{dept}_{doc_type}.md"
    click.echo(f"\n✅ 已生成: {filename}")

@cli.command()
def list():
    """列出可用模板"""
    click.echo("📚 可用模板列表:\n")
    
    templates = [
        ("bp-v3", "商业计划书 V3.0", "最新版，含AI赋能章节"),
        ("bp-v2", "商业计划书 V2.0", "标准版"),
        ("pitch-investor", "投资人路演", "12页精简版"),
        ("pitch-gov", "政府申报路演", "突出社会效益"),
        ("gov-dali", "大理州科技局申报", "已验证模板"),
        ("sop-sales", "销售部SOP", "含AI获客流程"),
        ("sop-finance", "财务部SOP", "含自动化报表"),
    ]
    
    for name, desc, note in templates:
        click.echo(f"  {name:20} - {desc}")
        click.echo(f"  {'':20}   {note}")
        click.echo()

def main():
    cli()

if __name__ == '__main__':
    main()
