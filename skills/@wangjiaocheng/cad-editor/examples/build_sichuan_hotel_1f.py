# -*- coding: utf-8 -*-
"""使用 CAD Editor skill 创建总府四川宾馆 1F 全非房方案
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\skills\@wangjiaocheng\cad-editor\scripts')

from core.document import CADDocument
from core.renderer import Renderer
from layer.manager import LayerManager
from layer.linetypes import Linetypes
from entities.basic import BasicEntities
from entities.text import TextEntity
from templates.architectural import ArchitecturalTemplates
from dimension.linear import LinearDimension

# 真实尺寸 (mm)
TOTAL_W = 87155
TOTAL_H = 54190
h_dist_m = [4405, 2775, 5200, 4400, 5200, 4400, 5200, 4400, 5600, 4400, 5200, 4400, 5200, 2775, 4400, 5200, 4400, 5200, 4400]
h_cum = [0]
for d in h_dist_m: h_cum.append(h_cum[-1] + d)
h_axis = h_cum

v_dist_m = [5400, 2800, 6800, 7045, 1995, 6600, 1605, 2200, 3870, 3075, 3800, 3600, 5400]
v_cum = [0]
for d in v_dist_m: v_cum.append(v_cum[-1] + d)
v_axis = v_cum

# 创建文档
doc = CADDocument.new(version='R2010')
msp = doc.modelspace()

Linetypes.load_standard(doc)
LayerManager(doc).setup_template('arch')

# 建筑主体外轮廓
msp.add_line((0, 0), (TOTAL_W, 0), dxfattribs={'layer': 'wall'})
msp.add_line((TOTAL_W, 0), (TOTAL_W, v_axis[8]), dxfattribs={'layer': 'wall'})
msp.add_line((0, v_axis[8]), (TOTAL_W, v_axis[8]), dxfattribs={'layer': 'wall'})
msp.add_line((h_axis[8], v_axis[8]), (h_axis[8], TOTAL_H), dxfattribs={'layer': 'wall'})
msp.add_line((h_axis[13], v_axis[8]), (h_axis[13], TOTAL_H), dxfattribs={'layer': 'wall'})
msp.add_line((h_axis[8], TOTAL_H), (h_axis[13], TOTAL_H), dxfattribs={'layer': 'wall'})

# 早餐厅
ArchitecturalTemplates.wall(msp, [
    (0, 0), (h_axis[10], 0), (h_axis[10], v_axis[3]), (0, v_axis[3])
], thickness=200, layer='wall', color=1)

# 厨房
ArchitecturalTemplates.wall(msp, [
    (0, 0), (h_axis[3], 0), (h_axis[3], v_axis[1]), (0, v_axis[1])
], thickness=200, layer='wall', color=1)

# 包间隔墙
bw = (h_axis[8] - h_axis[5]) * 0.45
for i, x0 in enumerate([h_axis[3], h_axis[5], h_axis[7]]):
    msp.add_line((x0 + bw, v_axis[1]*0.6 + 100), (x0 + bw, v_axis[3]),
                 dxfattribs={'layer': 'wall', 'linetype': 'DASHED', 'color': 1})

# 健身房
ArchitecturalTemplates.wall(msp, [
    (h_axis[11], v_axis[1]), (h_axis[13], v_axis[1]),
    (h_axis[13], v_axis[2]), (h_axis[11], v_axis[2])
], thickness=200, layer='wall', color=3)

# 洗衣房
ArchitecturalTemplates.wall(msp, [
    (h_axis[14], v_axis[1]), (h_axis[16], v_axis[1]),
    (h_axis[16], v_axis[2]), (h_axis[14], v_axis[2])
], thickness=200, layer='wall', color=3)

# 卫生间
ArchitecturalTemplates.wall(msp, [
    (h_axis[17], v_axis[1]), (h_axis[19], v_axis[1]),
    (h_axis[19], v_axis[2]), (h_axis[17], v_axis[2])
], thickness=150, layer='wall', color=3)

# 大堂
ArchitecturalTemplates.wall(msp, [
    (0, v_axis[4]), (h_axis[10], v_axis[4]),
    (h_axis[10], v_axis[7]), (0, v_axis[7])
], thickness=200, layer='wall', color=3)

# 大堂内部隔断
for x_int in [h_axis[2], h_axis[4], h_axis[5], h_axis[7], h_axis[9]]:
    msp.add_line((x_int, v_axis[5]), (x_int, v_axis[6]),
                 dxfattribs={'layer': 'wall', 'linetype': 'DASHED', 'color': 3})
msp.add_line((h_axis[2], v_axis[5]), (h_axis[4], v_axis[5]), dxfattribs={'layer': 'wall', 'linetype': 'DASHED', 'color': 3})
msp.add_line((h_axis[2], v_axis[6]), (h_axis[4], v_axis[6]), dxfattribs={'layer': 'wall', 'linetype': 'DASHED', 'color': 3})
msp.add_line((h_axis[7], v_axis[5]), (h_axis[9], v_axis[5]), dxfattribs={'layer': 'wall', 'linetype': 'DASHED', 'color': 3})
msp.add_line((h_axis[7], v_axis[6]), (h_axis[9], v_axis[6]), dxfattribs={'layer': 'wall', 'linetype': 'DASHED', 'color': 3})

# 楼梯+电梯
ArchitecturalTemplates.wall(msp, [
    (h_axis[10], v_axis[4]), (h_axis[13], v_axis[4]),
    (h_axis[13], v_axis[7]), (h_axis[10], v_axis[7])
], thickness=240, layer='wall', color=3)

# 电梯方框
for pt in [
    ((h_axis[10]+800, v_axis[5]), (h_axis[10]+800, v_axis[6])),
    ((h_axis[10]+800, v_axis[5]), (h_axis[10]+2200, v_axis[5])),
    ((h_axis[10]+2200, v_axis[5]), (h_axis[10]+2200, v_axis[6])),
    ((h_axis[10]+2200, v_axis[6]), (h_axis[10]+800, v_axis[6])),
]:
    msp.add_line(pt[0], pt[1], dxfattribs={'layer': 'wall', 'color': 3})

# 楼梯
ArchitecturalTemplates.stair_straight(msp, (h_axis[11]+1500, v_axis[5]+600),
                                      step_count=12, step_width=300, total_width=1800,
                                      direction='up-right', layer='wall')

# 走廊
msp.add_line((0, v_axis[3]), (TOTAL_W, v_axis[3]), dxfattribs={'layer': 'wall'})
msp.add_line((0, v_axis[4]), (TOTAL_W, v_axis[4]), dxfattribs={'layer': 'wall'})

# 北翼外租
ArchitecturalTemplates.wall(msp, [
    (h_axis[8], v_axis[8]), (h_axis[13], v_axis[8]),
    (h_axis[13], TOTAL_H), (h_axis[8], TOTAL_H)
], thickness=240, layer='wall', color=5)

# 入口标记
msp.add_line((h_axis[10], v_axis[6]), (h_axis[10], v_axis[7]),
             dxfattribs={'layer': 'wall', 'linetype': 'DASHED'})
msp.add_line((h_axis[11], v_axis[6]), (h_axis[11], v_axis[7]),
             dxfattribs={'layer': 'wall', 'linetype': 'DASHED'})
msp.add_line((0, v_axis[3]), (0, v_axis[4]),
             dxfattribs={'layer': 'wall', 'linetype': 'DASHED'})

# === 文字标注 ===
TextEntity.text(msp, "早餐厅 80座 1200㎡", (h_axis[5], v_axis[2]),
                height=2000, layer='text', halign='CENTER')
TextEntity.text(msp, "厨房 300㎡", (h_axis[1]+(h_axis[3]-h_axis[1])/2, v_axis[0]+v_axis[1]/2),
                height=1500, layer='text', halign='CENTER')
for i, x0 in enumerate([h_axis[3], h_axis[5], h_axis[7]]):
    TextEntity.text(msp, f'包间{i+1} 80㎡', (x0+bw/2, (v_axis[1]*0.6+v_axis[3])/2),
                    height=1200, layer='text', halign='CENTER')
TextEntity.text(msp, "健身房 52㎡", ((h_axis[11]+h_axis[13])/2, (v_axis[1]+v_axis[2])/2),
                height=1200, layer='text', halign='CENTER')
TextEntity.text(msp, "洗衣房 27㎡", ((h_axis[14]+h_axis[16])/2, (v_axis[1]+v_axis[2])/2),
                height=1200, layer='text', halign='CENTER')
TextEntity.text(msp, "卫生间", ((h_axis[17]+h_axis[19])/2, (v_axis[1]+v_axis[2])/2),
                height=1200, layer='text', halign='CENTER')
TextEntity.text(msp, "大堂+接待 800㎡", (h_axis[5], v_axis[5]+(v_axis[7]-v_axis[5])*0.65),
                height=2200, layer='text', halign='CENTER')
TextEntity.text(msp, "行李房 12㎡ | 总台 | 前厅办公 24㎡ | 布草回收 20㎡",
                (h_axis[5], v_axis[5]+(v_axis[7]-v_axis[5])*0.3),
                height=800, layer='text', halign='CENTER')
TextEntity.text(msp, "楼梯+电梯", ((h_axis[10]+h_axis[13])/2, (v_axis[4]+v_axis[7])/2),
                height=1800, layer='text', halign='CENTER')
TextEntity.text(msp, "走廊 200㎡", (h_axis[5], (v_axis[3]+v_axis[4])/2),
                height=1400, layer='text', halign='CENTER')
TextEntity.text(msp, "外租区域 1200㎡", ((h_axis[8]+h_axis[13])/2, v_axis[8]+(TOTAL_H-v_axis[8])*0.6),
                height=2200, layer='text', halign='CENTER')
TextEntity.text(msp, "(与皇冠联动保留)", ((h_axis[8]+h_axis[13])/2, v_axis[8]+(TOTAL_H-v_axis[8])*0.4),
                height=1500, layer='text', halign='CENTER')
TextEntity.text(msp, "主入口", (h_axis[10]+1500, v_axis[6]-500),
                height=1500, layer='text', halign='CENTER', color=1)
TextEntity.text(msp, "后勤入口", (500, v_axis[3]-500),
                height=1500, layer='text', halign='CENTER', color=1)

# === 轴线 ===
chinese = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
for i, x in enumerate(h_axis):
    if 9 <= i <= 13:
        msp.add_line((x, 0), (x, TOTAL_H), dxfattribs={'layer': 'axis', 'linetype': 'CENTER'})
    else:
        msp.add_line((x, 0), (x, v_axis[8]), dxfattribs={'layer': 'axis', 'linetype': 'CENTER'})
    msp.add_circle((x, -1500), 600, dxfattribs={'layer': 'axis'})
    TextEntity.text(msp, chinese[i], (x, -1500), height=800, layer='axis', halign='CENTER')
    msp.add_circle((x, TOTAL_H+1500), 600, dxfattribs={'layer': 'axis'})
    TextEntity.text(msp, chinese[i], (x, TOTAL_H+1500), height=800, layer='axis', halign='CENTER')

letters = 'ABCDEFGHIJKLMN'
for i, y in enumerate(v_axis):
    if i < 8:
        msp.add_line((0, y), (TOTAL_W, y), dxfattribs={'layer': 'axis', 'linetype': 'CENTER'})
    else:
        msp.add_line((h_axis[8], y), (h_axis[13], y), dxfattribs={'layer': 'axis', 'linetype': 'CENTER'})
    msp.add_circle((-1500, y), 600, dxfattribs={'layer': 'axis'})
    TextEntity.text(msp, letters[i], (-1500, y), height=800, layer='axis', halign='CENTER')
    msp.add_circle((TOTAL_W+1500, y), 600, dxfattribs={'layer': 'axis'})
    TextEntity.text(msp, letters[i], (TOTAL_W+1500, y), height=800, layer='axis', halign='CENTER')

# === 尺寸标注 ===
y_top = TOTAL_H + 3500
prev = 0
for i, x in enumerate(h_axis[1:]):
    seg = h_dist_m[i]
    LinearDimension.horizontal(msp, (prev, y_top), (x, y_top), offset=1500,
                                text=f'{seg*1000:.0f}', layer='dimension')
    prev = x

x_right = TOTAL_W + 3500
prev = 0
for i, y in enumerate(v_axis[1:]):
    seg = v_dist_m[i]
    LinearDimension.chain_vertical(msp, [(x_right, prev), (x_right, y)],
                                    offset=1500, layer='dimension')
    prev = y

TextEntity.text(msp, f"总长 {TOTAL_W/1000:.1f} m", (TOTAL_W/2, y_top+2500),
                height=1500, layer='dimension', halign='CENTER')
TextEntity.text(msp, f"总高 {TOTAL_H/1000:.1f} m", (TOTAL_W+8000, TOTAL_H/2),
                height=1500, layer='dimension', halign='CENTER')
TextEntity.text(msp, f"主体 {v_cum[8]/1000:.1f} m", (-8000, v_axis[4]),
                height=1500, layer='dimension', halign='CENTER')
TextEntity.text(msp, f"北翼 {(TOTAL_H-v_cum[8])/1000:.1f} m",
                ((h_axis[8]+h_axis[13])/2, -5000),
                height=1500, layer='dimension', halign='CENTER')

# === 标题 ===
TextEntity.text(msp, "总府四川宾馆 · 方案四 v4.0 · 1F 全非房方案",
                (TOTAL_W/2, TOTAL_H+6500), height=3000, layer='text', halign='CENTER')
TextEntity.text(msp, "总府街 31 号 · 87×54m L 形 · 176 间客房 · Eric 9/27 13:43 指令",
                (TOTAL_W/2, TOTAL_H+8500), height=1500, layer='text', halign='CENTER')

# === 保存 + 渲染 ===
out_dir = r'C:\Users\ericz\Desktop\产业发展部\旗下酒店\川宾改造\CAD图纸_v4.0'
os.makedirs(out_dir, exist_ok=True)
out_dxf = os.path.join(out_dir, '总府四川宾馆_方案四v4.0_1F_全非房.dxf')
CADDocument.save(doc, out_dxf)
print(f'DXF saved: {out_dxf}')

Renderer.render_quick(doc, output_dir=out_dir, name='总府四川宾馆_方案四v4.0_1F_全非房')
print('\n=== 输出 ===')
for f in sorted(os.listdir(out_dir)):
    fp = os.path.join(out_dir, f)
    print(f'  {f}: {os.path.getsize(fp):,} bytes')