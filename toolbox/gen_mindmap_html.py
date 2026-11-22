"""生成自定义样式的 markmap HTML(大字体 + 暖色背景)"""
import os

SOURCE_MD = r"D:\B166ER-OpenClaw\workspace\toolbox\hotel_brand_mindmap.md"
OUTPUT_HTML = r"C:\Users\ericz\Desktop\酒店品牌市场指数_2026H2_思维导图.html"

with open(SOURCE_MD, 'r', encoding='utf-8') as f:
    md_content = f.read()

# 自定义 CSS - 暖色背景 + 大字体 + 无 toolbar
html = f"""<!doctype html>
<html>
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>酒店品牌市场指数 2026 H2</title>
<style>
* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}
html, body {{
  width: 100%;
  height: 100%;
  background: #faf4ea;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC",
               "Microsoft YaHei", "微软雅黑", sans-serif;
  overflow: hidden;
}}
#mindmap {{
  display: block;
  width: 100vw;
  height: 100vh;
}}
/* markmap 节点样式覆盖 */
g.markmap-node text {{
  font-family: "PingFang SC", "Microsoft YaHei", "微软雅黑", sans-serif !important;
  fill: #3c2819 !important;
}}
g.markmap-node circle {{
  stroke-width: 2px !important;
}}
</style>
</head>
<body>
<svg id="mindmap"></svg>

<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script src="https://cdn.jsdelivr.net/npm/markmap-view@0.18.12"></script>
<script src="https://cdn.jsdelivr.net/npm/markmap-toolbar@0.18.12/dist/index.js"></script>

<script>
const { Markmap, loadCSS, builtinMarkmaps } = window.markmap;

const md = `{md_content.replace('`', '\\`')}`;

const transformer = new window.markmap.Transformer();
const { root } = transformer.transform(md);

const markmap = Markmap.create(document.querySelector('#mindmap'), {{
  maxWidth: 360,
  initialExpandLevel: -1,  // 全部展开
  zoom: true,
  pan: true,
  color: (node) => {{
    const level = node.depth;
    const colors = ['#b7791f', '#c8102e', '#1f4d2a', '#1f2a4d', '#4d3f1f', '#2a4d2a'];
    return colors[level % colors.length] || '#b7791f';
  }},
  fontSize: '20px',
  spacingHorizontal: 80,
  spacingVertical: 12,
}});

// 不显示 toolbar (移除右下角 logo)
// window.markmap.Markmap.toolbar.create(markmap);  // commented out
</script>
</body>
</html>
"""

with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'OK: {OUTPUT_HTML}')
print(f'大小: {os.path.getsize(OUTPUT_HTML) / 1024:.1f} KB')