# OTA Scraper - 技术路线手册

> 建立时间: 2026-04-04
> 状态: ✅ 已跑通

---

## 核心发现

**携程酒店详情页需要登录，但点评页(wap.ctrip.com)无需登录即可访问！**

---

## 已验证可工作的方案

### 方案A: 百度搜索 + Jina Reader（零成本，无需登录）

**原理**: 
1. 用百度搜索"酒店名 携程"找到真实的携程酒店URL
2. 携程的 `wap.ctrip.com/html5/hotel/hoteldetail/dianping/{HOTEL_ID}.html` 点评页**无需登录**即可访问
3. 通过 Jina Reader 抓取页面内容，绕过 JavaScript 渲染

**成功率**: ✅ 已验证可行

**可获取数据**:
- 总体评分 + 各维度评分（卫生/环境/服务/设施）
- 点评总数
- 关键词热度（早餐/江景/前台等）
- 点评正文内容
- 用户照片URL列表

**无法获取**: 实时房价、实时房态、预订信息

---

## 已知可用URL模板

### 携程
```
# 酒店详情页（需要登录）
https://hotels.ctrip.com/hotels/{HOTEL_ID}.html

# 酒店点评页（无需登录 ✅）
https://wap.ctrip.com/html5/hotel/hoteldetail/dianping/{HOTEL_ID}.html

# 格式: wap.ctrip.com/html5/hotel/hoteldetail/dianping/{携程酒店ID}.html
```

### 携程酒店ID获取方法
通过百度搜索"酒店名 携程" → 提取搜索结果中的 hotel ID

示例：乐山锦江嘉州宾馆
- 百度搜索: `https://www.baidu.com/s?wd=嘉州宾馆+携程+酒店`
- 找到URL中的酒店ID: `73690948`
- 点评页: `https://wap.ctrip.com/html5/hotel/hoteldetail/dianping/73690948.html`

---

## 乐山锦江嘉州宾馆数据（示例）

**HOTEL_ID**: 73690948

| 数据项 | 值 |
|--------|-----|
| 酒店名称 | 乐山锦江嘉州宾馆 |
| 总体评分 | 4.7/5.0 |
| 卫生评分 | 4.8 |
| 环境评分 | 4.8 |
| 服务评分 | 4.7 |
| 设施评分 | 4.6 |
| 点评总数 | 2418条 |
| 热门关键词 | 早餐很棒(444) / 江景壮观(342) / 前台热情(148) / 停车方便(125) |

---

## 各平台状态

| 平台 | 详情页 | 点评/搜索页 | 需要登录 |
|------|--------|-------------|---------|
| 携程 wap | 🔴 | 🟢 | 否 |
| 携程主站 | 🔴 | 🟢 部分 | 是 |
| 去哪儿 | 🔴 | 🟢 | 否(部分) |
| 飞猪 | 🟡 | 🟡 | 部分 |
| 美团 | 🔴 | 🔴 | 是 |
| Booking | 🔴 | 🔴 | 是 |
| Expedia | 🔴 | 🔴 | 是 |

---

## 技术实现

### Jina Reader 抓取命令
```python
import urllib.request, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://r.jina.ai/https://wap.ctrip.com/html5/hotel/hoteldetail/dianping/73690948.html"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
content = resp.read().decode("utf-8", errors="ignore")
```

### 数据提取（正则）
```python
import re

# 评分
scores = re.findall(r'(\d\.\d)\s*(?:分|分满意)', content)

# 点评数
review_count = re.findall(r'(\d+,?\d*)\s*条点评', content)

# 关键词热度
keywords = re.findall(r'([^\s\d]+)\s*(\d+)', content)
```

---

## 下一步

1. ✅ **已跑通**: 携程 wap 点评页数据抓取
2. ⏳ **进行中**: 去哪儿/飞猪/美团的 equivalent 公开页面
3. 🔴 **待解决**: 实时房价/房态（需要登录或API）
4. 🔴 **待解决**: 携程主站 hotel ID 规律（目前只有通过百度发现）

---

## 文件清单

```
ota-scraper/
├── ota_scraper.py              # 旧版主文件（参考）
├── test_quick.py              # Stealth测试
├── test_local_v2.py           # Playwright本地IP测试
├── test_jina.py               # Jina Reader测试
├── find_ctrip_city.py         # 携程城市ID探索
├── test_jjz_hotel.py          # 锦江嘉州酒店测试 ✅
├── baidu_hotel_search.py      # 百度搜索找酒店URL
├── extract_hotel_urls.py      # 从百度提取OTA URL
├── ctrip_leshan_content.txt   # 乐山携程页面内容
├── hotel_url_discovery.json    # URL发现结果
└── test_results.json           # Playwright测试结果
```
