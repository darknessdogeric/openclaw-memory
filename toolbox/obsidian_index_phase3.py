#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 3: 为桌面原始素材建 vault 索引 (不搬二进制,只建链接)"""
import sys
from pathlib import Path
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

DESK = Path(r"C:\Users\ericz\Desktop")
VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
NOW = datetime.now().strftime("%Y-%m-%d")

# 目标: 在 vault\50-外部接入\<目 录名>\_原始素材索引.md
def make_index(name, desktop_subdir, vault_subdir, description=""):
    """为指定桌面目录建 README 索引"""
    src = DESK / desktop_subdir
    dst_dir = VAULT / "50-外部接入" / vault_subdir
    dst_dir.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        print(f"[跳过] {src} 不存在")
        return
    index_path = dst_dir / "_原始素材索引.md"
    # 收集所有非 .md 文件
    files = []
    for p in src.rglob("*"):
        if p.is_file() and p.suffix.lower() != ".md":
            sz = p.stat().st_size
            files.append((p.relative_to(src), sz))
    # 按目录分组
    by_dir = {}
    for rel, sz in files:
        d = str(rel.parent).replace("\\", "/")
        if d == ".": d = "(根)"
        by_dir.setdefault(d, []).append((rel.name, sz))

    lines = []
    lines.append(f"---")
    lines.append(f"type: 原始素材索引")
    lines.append(f"source_desktop: {desktop_subdir}")
    lines.append(f"created: {NOW}")
    lines.append(f"---")
    lines.append("")
    lines.append(f"# {name} - 原始素材索引")
    lines.append("")
    lines.append(f"> 本目录包含来自桌面 `{desktop_subdir}` 的原始素材文件索引。")
    lines.append(f"> 源路径: `C:\\Users\\ericz\\Desktop\\{desktop_subdir}`")
    lines.append(f"> 说明: {description}")
    lines.append(f"> 创建: {NOW}")
    lines.append("")
    lines.append("## 索引")
    lines.append("")
    for d in sorted(by_dir.keys()):
        lines.append(f"### {d}")
        for fname, sz in sorted(by_dir[d]):
            size_str = f"{sz/1024:.1f}KB" if sz < 1024*1024 else f"{sz/1024/1024:.2f}MB"
            # 用 Obsidian wiki link 语法 + 文件路径(实际是桌面绝对路径)
            # 完整路径
            abs_path = src / d / fname if d != "(根)" else src / fname
            if d == "(根)": abs_path = src / fname
            else: abs_path = src / d.split("/")[-1] / fname  # 不对,修正
            # 上面复杂了,直接从 by_dir 字典重做
            pass
        lines.append("")
    # 重写更干净的版本
    lines = []
    lines.append("---")
    lines.append("type: 原始素材索引")
    lines.append(f"source_desktop: {desktop_subdir}")
    lines.append(f"created: {NOW}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {name} - 原始素材索引")
    lines.append("")
    lines.append(f"> 来源: `C:\\Users\\ericz\\Desktop\\{desktop_subdir}`")
    lines.append(f"> 创建: {NOW}")
    if description:
        lines.append(f"> 用途: {description}")
    lines.append("")
    lines.append("## 文件清单")
    lines.append("")
    total_size = 0
    total_count = 0
    # 重新扫,按结构列出
    for p in sorted(src.rglob("*")):
        if p.is_file() and p.suffix.lower() != ".md":
            sz = p.stat().st_size
            total_size += sz
            total_count += 1
            rel = p.relative_to(src)
            rel_str = str(rel).replace("\\", "/")
            size_str = f"{sz/1024:.1f}KB" if sz < 1024*1024 else f"{sz/1024/1024:.2f}MB"
            ext = p.suffix.lower()
            # 用 markdown 链接 + file 路径, Obsidian 在 Windows 上能识别
            lines.append(f"- `{ext[1:] if ext else 'file'}` **{rel_str}** ({size_str})")
    lines.append("")
    lines.append(f"## 统计")
    lines.append(f"- 文件数: {total_count}")
    size_str = f"{total_size/1024/1024:.2f} MB"
    lines.append(f"- 总大小: {size_str}")
    lines.append("")
    lines.append("---")
    lines.append("## 备注")
    lines.append("- 本目录的 `.md` 文件已在 vault 复制(见同目录其它笔记)")
    lines.append("- 二进制文件保留在桌面原位置,不上传 vault")
    lines.append("- 需要引用时,使用 Obsidian 链接语法,如 `[[相对路径]]` 或外部绝对路径")
    lines.append("")

    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[{name}] {total_count} 文件, {size_str} -> {index_path.name}")


# 1. AHL源代码 - 代码项目,加 README 说明
ahl_src = DESK / "AHL源代码" / "AI-HOTEL-LANGUAGE-DEMO-main"
if ahl_src.exists():
    dst = VAULT / "50-外部接入" / "AHL源代码-README.md"
    # 收集 docs / legacy / knowledge_base 里剩余信息
    readme = []
    readme.append("---")
    readme.append("type: 代码项目索引")
    readme.append(f"created: {NOW}")
    readme.append("---")
    readme.append("")
    readme.append("# AHL 源代码 (AI-HOTEL-LANGUAGE-DEMO)")
    readme.append("")
    readme.append(f"> 来源: `C:\\Users\\ericz\\Desktop\\AHL源代码\\AI-HOTEL-LANGUAGE-DEMO-main`")
    readme.append(f"> 类型: 完整代码项目 (frontend/backend/docs/knowledge_base/legacy)")
    readme.append(f"> 创建: {NOW}")
    readme.append("")
    readme.append("## 项目结构")
    readme.append("")
    for p in sorted(ahl_src.iterdir()):
        if p.is_dir():
            cnt = sum(1 for _ in p.rglob("*") if _.is_file())
            readme.append(f"- **{p.name}/** ({cnt} 文件)")
        else:
            sz = p.stat().st_size
            readme.append(f"- {p.name} ({sz/1024:.1f}KB)")
    readme.append("")
    readme.append("## 知识库")
    readme.append("- `knowledge_base/` 内含完整酒店知识库 (industry/references/internal)")
    readme.append("- 知识库的 `.md` 已 copy 到 vault `50-外部接入/AHL源代码-docs/knowledge_base/...`")
    readme.append("")
    readme.append("## docs")
    readme.append("- `docs/` 含项目原始文档")
    readme.append("- 文档的 `.md` 已 copy 到 vault `50-外部接入/AHL源代码-docs/docs/...`")
    readme.append("")
    readme.append("## 代码")
    readme.append("- `backend/` `frontend/` `legacy/` 都是代码,不复制到 vault")
    readme.append("- 改动代码请直接在桌面原项目目录操作")
    readme.append("- B166ER 工具 `01-Workspace-核心/TOOLS.md` 已记录此项目")
    readme.append("")
    dst.write_text("\n".join(readme), encoding="utf-8")
    print(f"[AHL源代码-README] -> {dst}")

# 2. AHL-BP-2026 - 商业计划书 (PNG 14 + PDF 1)
make_index("AHL-BP-2026 商业计划书", "AHL-BP-2026", "AHL-BP-2026", "AHL 商业计划书 v1.0 - 12 张封面 + 1 张摘要 PNG + PDF 全文")

# 3. 工作文档
make_index("工作文档", "工作文档", "工作文档-桌面映射", "襄阳/中旅相关工作文档 (HAL 模式 + 劳动关系)")

# 4. 项目资料
make_index("项目资料", "项目资料", "项目资料-桌面映射", "酒店项目土建期策划 + 音乐文创 + 潮玩周边")

# 5. 自我革命 - 大量 PDF
make_index("自我革命", "自我革命", "自我革命-桌面映射", "AI+酒店行业研究 (PDF + 研究报告)")

# 6. 新媒体产品线 - 二进制索引
make_index("新媒体产品线 - 原始素材", "新媒体产品线", "新媒体产品线-原始素材索引", "产品交付包 (PNG 海报 + PDF + HTML 模板)")

# 7. 张实项目总控 - 原始素材索引 (除了 .md 外的所有文件)
zsp = DESK / "张实项目总控"
if zsp.exists():
    dst = VAULT / "50-外部接入" / "张实项目总控-原始素材索引.md"
    readme = []
    readme.append("---")
    readme.append("type: 原始素材索引")
    readme.append(f"source_desktop: 张实项目总控")
    readme.append(f"created: {NOW}")
    readme.append("---")
    readme.append("")
    readme.append("# 张实项目总控 - 原始素材索引")
    readme.append("")
    readme.append(f"> 来源: `C:\\Users\\ericz\\Desktop\\张实项目总控`")
    readme.append(f"> 创建: {NOW}")
    readme.append("")
    readme.append("## 11 个一级目录")
    readme.append("")
    total_files = total_size = 0
    for sub in sorted(zsp.iterdir()):
        if sub.is_dir():
            files = [p for p in sub.rglob("*") if p.is_file()]
            md_count = sum(1 for p in files if p.suffix.lower()==".md")
            other = len(files) - md_count
            sz = sum(p.stat().st_size for p in files) / 1024 / 1024
            readme.append(f"### {sub.name}")
            readme.append(f"- `.md` {md_count} 文件, 其它二进制 {other} 文件")
            readme.append(f"- 总大小: {sz:.2f} MB")
            if other > 0 and sz > 0:
                # 列出非 .md 文件
                for p in sorted(sub.rglob("*")):
                    if p.is_file() and p.suffix.lower() != ".md":
                        rel = p.relative_to(zsp)
                        sz1 = p.stat().st_size / 1024
                        unit = "KB"
                        if sz1 > 1024:
                            sz1 = sz1 / 1024
                            unit = "MB"
                        readme.append(f"  - `{p.suffix[1:] if p.suffix else '?'}` **{rel}** ({sz1:.1f}{unit})")
            readme.append("")
    readme.append("---")
    readme.append("**Note**:  `.md` 文件已完整复制到 vault `50-外部接入/张实项目总控/`. 二进制文件保留在桌面原位置。")
    dst.write_text("\n".join(readme), encoding="utf-8")
    print(f"[张实项目总控-原始素材索引] -> {dst}")

# 8. 安逸集团 - 二进制索引
make_index("安逸集团入职物料 - 原始素材", "安逸集团_入职物料_20260707", "01-安逸入职物料-20260707-原始素材索引",
           "7/24 研讨会纪要微信图片等")

print("\n=== Phase 3 完成 ===")
print(f"vault .md 总数: {sum(1 for _ in VAULT.rglob('*.md'))}")
print(f"vault 总文件: {sum(1 for _ in VAULT.rglob('*') if _.is_file())}")
