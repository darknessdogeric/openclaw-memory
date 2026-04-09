# B166ER 海报模板系统 v1.0

> 独立美工水平的海报生成工具

## 快速开始

```bash
# 渲染所有模板
python generate_posters.py

# 渲染单个模板
python generate_posters.py 01_roadshow
python generate_posters.py 02_product
python generate_posters.py 03_social
python generate_posters.py 04_card
python generate_posters.py 05_hotel

# 查看所有模板
python generate_posters.py --list
```

## 5套模板

| ID | 模板 | 尺寸 | 用途 |
|----|------|------|------|
| 01 | 融资路演封面 | 1920×1080 (16:9) | AHL融资BP封面 |
| 02 | 产品一页纸 | 1080×1920 (9:16) | 酒店服务介绍 |
| 03 | 朋友圈素材 | 1080×1920 (9:16) | 朋友圈/小红书配图 |
| 04 | 商务名片 | 1920×1080 (16:9) | 创始人名片 |
| 05 | 酒店场景展示 | 1920×1080 (16:9) | 酒店多场景展示 |

## 输出位置

```
poster_templates/output/
├── 01_roadshow.png         # 融资路演封面
├── 02_product_onepager.png # 产品一页纸
├── 03_social_media.png     # 朋友圈素材
├── 04_business_card.png    # 商务名片
└── 05_hotel_showcase.png  # 酒店场景展示
```

## 自定义内容

编辑对应的 HTML 文件中的文字内容：

**常用占位符（可直接搜索替换）：**
- `张实 Eric` → 你的名字
- `17760348653` → 你的电话
- `ericzhangshi@163.com` → 你的邮箱
- `ahlprotocol.ai` → 你的网站
- `AHL` → 你的品牌名
- `种子轮融资` → 当前融资阶段
- `500-800 万元` → 你的融资目标

## 添加新模板

1. 在 `poster_templates/` 下新建 HTML 文件
2. 使用 `Noto Sans SC` 或 `Microsoft YaHei` 字体
3. 建议尺寸：1920×1080（横版）或 1080×1920（竖版）
4. 运行 `python generate_posters.py` 渲染

## 字体说明

已预装中文字体：
- `Noto Sans SC` — 最佳（Google字体，清晰现代）
- `Microsoft YaHei` — 雅黑（系统内置）
- `SimHei` — 黑体（备用）

## 技术说明

- 渲染引擎：Playwright（Chromium）
- 输出格式：PNG
- 分辨率：原生尺寸（可通过CSS调整）
