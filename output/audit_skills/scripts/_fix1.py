# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, hashlib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
WS = os.path.join(ROOT,"skills")

# ============ FIX 1: 8 个无 description 技能 → 写可路由描述 ============
DESC = {
 "cad-batch-processing": "CAD 批量处理与 AutoCAD 自动化：解析 DWG/DXF 的图层、文字坐标、块属性，批量修改图纸并输出 JSON 供下游处理。触发：CAD 图纸批量处理、AutoCAD 自动化、DWG/DXF 解析。",
 "cost-governor": "LLM API 成本实时监控与预算熔断：跨 OpenAI/Anthropic/Google 追踪花费，设预算上限与 circuit breaker，防止夜间烧穿配额。触发：API 成本控制、token 预算、烧钱防护。",
 "hotel-feasibility-report": "酒店/民宿投资可行性研究报告方法论与工具链：地区级→单店逐层下钻（10 章 5 维结构），依据弥勒 v1-v4 与 PDF 实战经验。触发：酒店投资可行性、民宿可研、物业可研报告、改造投资测算。",
 "interior-fullplan": "室内设计全案方案自动生成：户型诊断、风格定位、平面布局逻辑、灯光系统、材料清单、预算拆分、设计说明、施工要点，输出 Markdown 可直接转方案册/PPT。触发：室内设计方案、全案、装修方案、软装选型。",
 "officecli": "OfficeCLI 单文件二进制 Office 文档读写：无需安装 Office 即可创建/读取/修改 docx、xlsx、pptx。触发：Office 文档读写、docx/xlsx/pptx 生成、免装 Office 环境。",
 "en": "英文版写作与翻译参考：术语对照、语气规范、跨语种一致性检查。触发：英文文档、翻译、英文邮件。",
 "zh-CN": "简体中文写作与本地化参考：标点与全角规范、术语本地化、简中排版约定。触发：中文文档、本地化、简中排版。",
 "skill-vetter": "技能评估器：在安装任何来自 ClawdHub / GitHub 的技能之前先做质量与风险评估（评分、重复度、权限风险、是否已被本地替代）。触发：评估技能、安装技能前审查、skill review、装之前先验。",
}
fixed = 0
for d, desc in DESC.items():
    for base in (WS, os.path.join(HOME,"skills")):
        p = os.path.join(base, d, "SKILL.md")
        if not os.path.exists(p): continue
        t = open(p, encoding="utf-8", errors="replace").read()
        if not t.lstrip().startswith("---"):
            # 无 frontmatter：加一个
            fm = "---\nname: %s\ndescription: %s\n---\n\n" % (d, desc)
            open(p, "w", encoding="utf-8", newline="\n").write(fm + t)
            fixed += 1
            continue
        end = t.find("\n---", 3)
        fm = t[:end]
        body = t[end:]
        if re.search(r"^description:", fm, re.M):
            fm2 = re.sub(r"^description:.*$", "description: " + desc, fm, count=1, flags=re.M)
        else:
            fm2 = fm + "\ndescription: " + desc
        open(p, "w", encoding="utf-8", newline="\n").write(fm2 + body)
        fixed += 1
print("FIX1 补 description: %d 处" % fixed)

# ============ FIX 2: 5 组跨技能路径错引 → 指向真实所在 ============
RELOC = [
 ("ppt-visual-editor", "assets/scenarios", "../ppt-deck-builder-pro/assets/scenarios"),
 ("ppt-visual-editor", "assets/slide_plan_template.json", "../ppt-deck-builder-pro/assets/slide_plan_template.json"),
 ("ppt-visual-editor", "references/brief-contract.md", "../ppt-deck-builder-pro/references/brief-contract.md"),
 ("ppt-visual-editor", "scripts/build_contact_sheet.py", "../ppt-deck-builder-pro/scripts/build_contact_sheet.py"),
 ("ppt-visual-editor", "scripts/generate_from_plan.py", "../ppt-deck-builder-pro/scripts/generate_from_plan.py"),
 ("ppt-visual-editor", "scripts/package_image_deck.sh", "../ppt-deck-builder-pro/scripts/package_image_deck.sh"),
 ("ppt-visual-editor", "scripts/rerun_single_page.sh", "../ppt-deck-builder-pro/scripts/rerun_single_page.sh"),
 ("wayfinding-signage", "references/accessibility-quick-check.md", "../color-palette-advisor/references/accessibility-quick-check.md"),
 ("arkcli-api-explorer", "references/api-key-query.md", "../arkcli-auth/references/api-key-query.md"),
 ("goal-management", "references/project-management.md", "../ontology/docs/examples/project-management.md"),
]
fix2 = 0
for skill, old, new in RELOC:
    for base in (WS, os.path.join(HOME,"skills"), os.path.join(HOME,".claude","skills")):
        p = os.path.join(base, skill, "SKILL.md")
        if not os.path.exists(p): continue
        t = open(p, encoding="utf-8", errors="replace").read()
        if old in t:
            t2 = t.replace(old, new)
            open(p, "w", encoding="utf-8", newline="\n").write(t2)
            fix2 += 1
print("FIX2 修跨技能路径错引: %d 处" % fix2)
