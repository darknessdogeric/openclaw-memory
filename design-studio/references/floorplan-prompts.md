# 平面图 / 立面图 / 三视图 提示词库

## 平面图 (Floor Plan)

### 户型平面图
```
# 通用
architectural floor plan, top-down plan view, [N]-bedroom [N]-bathroom layout,
open-plan living dining kitchen, total area [X] square meters,
[style] residential design, professional architectural drafting style,
clean black linework on white background, dimension annotations,
door swings indicated, furniture layout shown, 1:100 scale appearance

# 酒店客房层
hotel guest floor plan, top-down view, [N] guest rooms per floor,
central corridor layout, elevator core, service stair,
standard room [X] sqm, suite [Y] sqm, professional architectural drawing,
dimensioned, room numbers labeled, fire escape route indicated,
black linework on white, 1:200 scale

# 酒店公共层
hotel ground floor plan, lobby restaurant bar spa layout,
reception desk, lounge seating, all-day dining restaurant,
back-of-house kitchen service corridor, restrooms,
vertical circulation elevators stairs, main entrance portico,
professional architectural plan, dimensioned, 1:200 scale

# 度假村总平
resort master plan, site plan top-down, [N] buildings in [style] architecture,
landscape gardens, infinity pool, pathways, parking area,
surrounding [geography] context, professional landscape architecture drawing,
green spaces indicated, building footprints numbered, north arrow
```

### 在线工具增强
生成平面图时，同时输出可输入到免费工具的文本描述：
- Homestyler: https://www.homestyler.com — AI户型生成
- Home-design.ai: https://home-design.ai/floor-plan-generator — 参数→户型
- Planner 5D: https://planner5d.com — AI户型识别+家具布置

---

## 立面图 (Elevation)

### 建筑立面
```
# 正面 (Front/Facade)
architectural front elevation, [building name], [style] architecture,
[N] stories height, [material] facade, entrance detail,
symmetrical composition, professional architectural elevation drawing,
orthographic projection, precise linework, material hatches,
shadow indication, human scale figure for reference, white background

# 侧面 (Side)
architectural side elevation, [building name], orthogonal projection,
showing depth and massing, window rhythm, roof profile,
material transitions indicated, section cut lines,
professional drafting style, clean linework, white background

# 背面 (Rear)
architectural rear elevation, [building name], orthogonal view,
service entrance, mechanical equipment screening,
balcony arrangement, consistent with front elevation language,
professional architectural drawing, white background
```

### 室内立面
```
# 大堂立面
interior elevation, hotel lobby, double-height space,
reception desk wall, feature art wall, material palette indicated,
[style] interior design, professional interior elevation drawing,
finish annotations, lighting fixture locations, human scale figure

# 客房立面
interior elevation, hotel guest room, bed headboard wall,
window wall with [view], bathroom entrance wall,
[style] interior, finish and material callouts,
professional interior elevation, dimensioned
```

---

## 三视图 (Orthographic Views)

生成三张图：Front / Side / Top

### 通用三视图模板
```
# 正视图 (Front)
orthographic front view, [building type] [style] architecture,
[N] stories, [material] facade, entrance centered,
strict orthogonal projection, no perspective distortion,
professional architectural orthographic drawing, white background,
dimension lines, building height [X] meters, width [Y] meters

# 侧视图 (Side)
orthographic side view, [building type],
showing building depth and profile, roof slope,
window placement on side facade, material consistency,
professional orthographic drawing, white background,
dimension lines, depth [Z] meters

# 俯视图 (Top/Plan)
orthographic top view, [building type],
roof plan with mechanical equipment, building footprint,
surrounding site context (simplified), north arrow,
professional architectural roof plan, white background,
overall dimensions [X]×[Z] meters
```

---

## 快速参数替换表

| 参数 | 替换值示例 |
|------|-----------|
| [N] | 数字: 3, 5, 150 |
| [style] | modern, Chinese, wabi-sabi, industrial, Nordic, biophilic |
| [material] | glass, steel, stone, wood, concrete, brick |
| [building type] | hotel, resort, villa, guesthouse, wellness center |
| [geography] | mountain, lakefront, beach, urban, forest, valley |
| [view] | city skyline, garden, ocean, mountain, courtyard |
| [X] [Y] [Z] | 尺寸数字 (米) |
