"""
v6.0 终极方案:
- d3 + markmap-view 直接内嵌到 HTML (零外部依赖)
- 完全离线可用
"""
import os
import json

OUT_DIR = r"D:\B166ER-OpenClaw\workspace\outputs\酒管公司供应链工程-交付包-v1.0\04-思维导图"
SKILL_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\guizang-social-card-skill"
SRC_MD = os.path.join(OUT_DIR, "思维导图源文件.md")
HTML_OUT = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图.html")
ASSETS = os.path.join(SKILL_DIR, "assets")


def main():
    # 读取本地 JS
    with open(os.path.join(ASSETS, "d3.min.js"), "r", encoding="utf-8", errors="ignore") as f:
        d3_js = f.read()
    with open(os.path.join(ASSETS, "markmap-unpkg.min.js"), "r", encoding="utf-8", errors="ignore") as f:
        mm_js = f.read()

    # 解析 MD (v2.0: 按缩进识别层级)
    with open(SRC_MD, "r", encoding="utf-8") as f:
        md_text = f.read()
    lines = md_text.split("\n")

    root = {"depth": 0, "content": "", "children": []}
    stack = [root]
    for line in lines:
        s = line.strip()
        if not s:
            continue
        # 计算前导空格数 (2空格 = 1层)
        indent = len(line) - len(line.lstrip())
        if s.startswith("# "):
            lv = 1; c = s[2:].strip()
        elif s.startswith("## "):
            lv = 2; c = s[3:].strip()
        elif s.startswith("### "):
            lv = 3; c = s[4:].strip()
        elif s.startswith("- ") or s.startswith("* "):
            # 列表项: 无缩进 = lv 3, 2空格缩进 = lv 4, 4空格缩进 = lv 5...
            lv = 3 + (indent // 2)
            c = s[2:].strip()
        else:
            continue
        while stack and stack[-1]["depth"] >= lv:
            stack.pop()
        if not stack:
            stack = [root]
        parent = stack[-1]
        node = {"depth": lv, "content": c, "children": []}
        parent["children"].append(node)
        stack.append(node)

    def to_mm(n, idx):
        return {
            "content": n["content"],
            "payload": {"idx": idx},
            "children": [to_mm(c, idx) for c in n["children"]],
        }

    children = [to_mm(c, i) for i, c in enumerate(root["children"])]
    if len(children) == 1:
        markmap_data = children[0]
    else:
        markmap_data = {"content": "酒管公司供应链工程", "payload": {"idx": 0}, "children": children}

    mm_json = json.dumps(markmap_data, ensure_ascii=False)

    # HTML 内嵌 d3 + markmap
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<title>酒管公司供应链工程 · 思维导图 v6.0</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{
  width: 100%;
  height: 100%;
  font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", "SimHei", sans-serif;
  background: #ffffff;
  overflow: hidden;
}}
#mindmap {{ display: block; width: 100vw; height: 100vh; }}
#mindmap text {{
  font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", "SimHei", sans-serif !important;
  font-weight: 600 !important;
  font-size: 16px !important;
}}
</style>
<script>
{d3_js}
</script>
<script>
{mm_js}
</script>
</head>
<body>
<svg id="mindmap"></svg>
<script>
window.addEventListener('load', () => {{
  const data = {mm_json};
  if (!window.markmap || !window.markmap.Markmap) {{
    console.error('markmap JS 未加载');
    document.body.innerHTML = '<pre style="color:red;padding:20px;font-size:24px">markmap JS 未加载</pre>';
    return;
  }}
  const mm = window.markmap.Markmap.create('svg#mindmap', {{
    autoFit: true,
    fitRatio: 0.95,
    maxWidth: 220,
    color: (node) => {{
      if (node.depth === 1) {{
        const colors = ['#1F4E79', '#C00000', '#7030A0', '#385723', '#806000', '#5B9BD5', '#2E75B6', '#404040'];
        return colors[(node.payload?.idx || 0) % colors.length];
      }}
      if (node.depth === 2) return '#5B9BD5';
      if (node.depth === 3) return '#7F7F7F';
      return '#999999';
    }},
    paddingX: 24,
    paddingY: 12,
    spacingHorizontal: 80,
    spacingVertical: 16,
    nodeMinHeight: 22,
    duration: 0,
  }}, data);
  let n = 0;
  const fitInterval = setInterval(() => {{
    mm.fit();
    n++;
    if (n >= 5) clearInterval(fitInterval);
  }}, 500);
  console.log('markmap 渲染完成, nodes:', data.children?.length || 1);
}});
</script>
</body>
</html>"""

    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK HTML: {HTML_OUT}")
    print(f"   Size: {os.path.getsize(HTML_OUT):,} bytes")
    print(f"   Top-level nodes: {len(children)}")


if __name__ == "__main__":
    main()