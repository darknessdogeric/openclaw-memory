---
name: image-gen
description: AI图像生成技能，支持文本生成图像。可使用OpenAI DALL-E、Stability AI或免费的Pollinations服务。适用于生成酒店宣传图、产品图、概念图等。
---

# ImageGen Skill - AI图像生成

使用AI根据文本描述生成图像。

## 功能特性

- ✅ **多提供商支持**: OpenAI DALL-E / Stability AI / Pollinations(免费)
- ✅ **无需API Key**: Pollinations服务完全免费，无需注册
- ✅ **高清图像**: 支持1024x1024及更高分辨率
- ✅ **批量生成**: 可一次生成多张图像
- ✅ **自动保存**: 图像自动保存到桌面

## 安装依赖

```bash
pip install requests
```

## 使用方法

### 命令行

```bash
# 使用免费服务生成图像（推荐）
python image_gen.py "一个现代化的酒店大堂，温馨舒适，有绿植和落地窗"

# 指定提供商
python image_gen.py "豪华酒店客房，海景，白色床单" -p pollinations

# 指定尺寸
python image_gen.py "酒店餐厅，精致的西餐摆盘" -s 1024x1024

# 生成多张
python image_gen.py "酒店游泳池，阳光明媚" -n 3
```

### Python API

```python
from image_gen import ImageGenerator

# 创建生成器（默认使用免费的Pollinations）
gen = ImageGenerator()

# 生成图像
result = gen.generate("一个温馨的民宿客厅，有壁炉和书架")

if result['success']:
    print(f"图像已保存: {result['images'][0]}")
```

### 使用OpenAI DALL-E（需API Key）

```python
from image_gen import ImageGenerator

# 设置API Key
import os
os.environ['OPENAI_API_KEY'] = 'your-api-key'

# 创建生成器
gen = ImageGenerator('openai')

# 生成高清图像
result = gen.generate(
    prompt="五星级酒店的豪华套房，现代简约风格",
    size="1024x1024",
    quality="hd"
)
```

## 提供商对比

| 提供商 | 费用 | 质量 | 速度 | 需要API Key |
|--------|------|------|------|-------------|
| Pollinations | 免费 | 中等 | 10-30秒 | ❌ 不需要 |
| OpenAI DALL-E | 付费 | 高 | 5-10秒 | ✅ 需要 |
| Stability AI | 付费 | 高 | 5-15秒 | ✅ 需要 |

## 提示词技巧

### 好的提示词示例

```
# 酒店场景
"现代化酒店大堂，大理石地面，水晶吊灯，绿植装饰，温馨氛围，高清摄影风格"

# 客房场景
"豪华酒店客房，海景落地窗，白色床铺，木质家具，柔和灯光，极简风格"

# 餐饮场景
"精致西餐摆盘，牛排配蔬菜，红酒杯，白色桌布，餐厅背景，美食摄影"

# 民宿场景
"温馨民宿客厅，壁炉，书架，舒适沙发，自然光线，日式简约风格"
```

### 提示词结构

```
[主体] + [细节] + [风格] + [光线] + [质量]

示例:
主体: 酒店大堂
细节: 大理石地面、水晶吊灯、绿植
风格: 现代简约
光线: 自然光、柔和
质量: 高清摄影、4K
```

## 输出位置

生成的图像自动保存到:
```
%USERPROFILE%\Desktop\AI_Generated_Images\
```

文件名格式: `{提供商}_{时间戳}.png`

## 配置API Key（可选）

创建配置文件:
```bash
# Windows
mkdir %USERPROFILE%\.openclaw\config
```

创建文件 `%USERPROFILE%\.openclaw\config\image_gen_keys.json`:
```json
{
  "openai": "sk-your-openai-key",
  "stability": "sk-your-stability-key"
}
```

## 故障排除

### 问题: "未配置API密钥"
**解决**: 使用 `-p pollinations` 参数使用免费服务

### 问题: 生成超时
**解决**: 
- 检查网络连接
- 简化提示词
- 尝试其他提供商

### 问题: 图像质量不佳
**解决**:
- 使用更详细的提示词
- 添加风格描述（如"高清摄影"、"4K"）
- 使用OpenAI DALL-E获得更高质量

## 注意事项

1. **版权问题**: AI生成图像的版权归属因提供商而异，商业使用前请确认
2. **内容审核**: 部分提供商会自动过滤不当内容
3. **使用限制**: 免费服务可能有速率限制
4. **提示词语言**: 英文提示词通常效果更好

## 应用场景

- 🏨 酒店宣传图生成
- 📱 社交媒体配图
- 🎨 概念设计图
- 📄 PPT/文档插图
- 🖼️ 装饰画生成

## 更新日志

- v1.0 (2026-03-09): 初始版本，支持Pollinations免费服务
