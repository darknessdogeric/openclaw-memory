#!/usr/bin/env python3
"""
Taobao/Tmall Scraper - 淘宝/天猫专用抓取器
Phase 2: Playwright浏览器渲染 + 反爬对抗
"""

import asyncio
import json
import re
import time
import random
from typing import List, Dict, Optional
from dataclasses import dataclass
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

@dataclass
class TaobaoProduct:
    """淘宝/天猫商品数据结构"""
    item_id: str
    title: str
    price: float
    original_price: Optional[float]
    discount: str
    shop_name: str
    shop_type: str  # 天猫/淘宝/旗舰店
    location: str
    sales: str
    url: str
    image: str


class StealthHelper:
    """浏览器反检测辅助类"""
    
    @staticmethod
    def get_stealth_scripts() -> str:
        """获取反检测注入脚本"""
        return """
        // 隐藏 webdriver 属性
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        
        // 伪装 plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                {name: "Chrome PDF Plugin", filename: "internal-pdf-viewer"},
                {name: "Chrome PDF Viewer", filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai"},
                {name: "Native Client", filename: "internal-nacl-plugin"}
            ]
        });
        
        // 伪装 languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-CN', 'zh', 'en-US', 'en']
        });
        
        // 隐藏 automation 属性
        delete navigator.__proto__.webdriver;
        
        // 伪装 Chrome
        window.chrome = {
            runtime: {},
            loadTimes: () => {},
            csi: () => {},
            app: {}
        };
        
        // 伪装 permission
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        """
    
    @staticmethod
    def get_random_viewport() -> Dict:
        """获取随机视口大小"""
        viewports = [
            {'width': 1920, 'height': 1080},
            {'width': 1366, 'height': 768},
            {'width': 1440, 'height': 900},
            {'width': 1536, 'height': 864},
            {'width': 1680, 'height': 1050}
        ]
        return random.choice(viewports)
    
    @staticmethod
    def get_random_ua() -> str:
        """获取随机User-Agent"""
        ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'
        ]
        return random.choice(ua_list)


class TaobaoScraper:
    """淘宝/天猫抓取器"""
    
    SEARCH_URL = "https://s.taobao.com/search"
    TMALL_SEARCH_URL = "https://list.tmall.com/search_product.htm"
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.stealth = StealthHelper()
    
    async def init_browser(self):
        """初始化浏览器"""
        self.playwright = await async_playwright().start()
        
        # 启动浏览器
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials',
                '--disable-setuid-sandbox',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=1920,1080'
            ]
        )
        
        # 创建上下文
        viewport = self.stealth.get_random_viewport()
        self.context = await self.browser.new_context(
            viewport=viewport,
            user_agent=self.stealth.get_random_ua(),
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
            geolocation={'latitude': 31.2304, 'longitude': 121.4737},  # 上海
            permissions=['geolocation'],
            color_scheme='light'
        )
        
        # 注入反检测脚本
        await self.context.add_init_script(self.stealth.get_stealth_scripts())
        
        # 设置Cookie（模拟已登录用户）
        await self._set_initial_cookies()
    
    async def _set_initial_cookies(self):
        """设置初始Cookie"""
        # 淘宝需要一些基础Cookie才能正常访问
        cookies = [
            {
                'name': 'cna',
                'value': f'{self._random_string(24)}',
                'domain': '.taobao.com',
                'path': '/'
            },
            {
                'name': 'isg',
                'value': f'{self._random_string(32)}',
                'domain': '.taobao.com',
                'path': '/'
            }
        ]
        await self.context.add_cookies(cookies)
    
    def _random_string(self, length: int) -> str:
        """生成随机字符串"""
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    async def search_taobao(self, keyword: str, page: int = 1) -> List[TaobaoProduct]:
        """
        搜索淘宝商品
        
        Args:
            keyword: 搜索关键词
            page: 页码
            
        Returns:
            商品列表
        """
        if not self.context:
            await self.init_browser()
        
        page_obj = await self.context.new_page()
        
        try:
            # 构建搜索URL
            search_url = f"{self.SEARCH_URL}?q={keyword}&page={page}"
            
            # 模拟人类行为：先访问首页
            await page_obj.goto('https://www.taobao.com', wait_until='domcontentloaded', timeout=30000)
            await self._random_delay(2, 4)
            
            # 在搜索框输入关键词
            search_box = await page_obj.wait_for_selector('#q', timeout=10000)
            if search_box:
                # 模拟人类输入：逐字输入，有停顿
                await search_box.click()
                await self._random_delay(0.5, 1)
                
                for char in keyword:
                    await search_box.type(char, delay=random.uniform(50, 150))
                
                await self._random_delay(0.5, 1.5)
                
                # 点击搜索按钮
                search_btn = await page_obj.wait_for_selector('.btn-search', timeout=5000)
                if search_btn:
                    await search_btn.click()
            else:
                # 直接访问搜索结果页
                await page_obj.goto(search_url, wait_until='networkidle', timeout=60000)
            
            # 等待页面加载
            await page_obj.wait_for_load_state('networkidle', timeout=60000)
            
            # 检查是否有验证码
            if await self._check_captcha(page_obj):
                print("⚠️ 检测到验证码，尝试处理...")
                captcha_solved = await self._handle_captcha(page_obj)
                if not captcha_solved:
                    print("❌ 验证码处理失败")
                    return []
            
            # 等待商品列表加载
            await page_obj.wait_for_selector('.item, .Card--doubleCardWrapper--L2XFE73', timeout=15000)
            
            # 模拟滚动加载更多
            await self._simulate_scroll(page_obj)
            
            # 提取商品数据
            products = await self._extract_taobao_data(page_obj)
            
            return products
            
        except Exception as e:
            print(f"淘宝搜索失败: {e}")
            return []
        finally:
            await page_obj.close()
    
    async def search_tmall(self, keyword: str, page: int = 1) -> List[TaobaoProduct]:
        """搜索天猫商品"""
        if not self.context:
            await self.init_browser()
        
        page_obj = await self.context.new_page()
        
        try:
            # 天猫搜索URL
            search_url = f"{self.TMALL_SEARCH_URL}?q={keyword}&page={page}"
            
            await page_obj.goto(search_url, wait_until='networkidle', timeout=60000)
            
            # 等待商品列表
            await page_obj.wait_for_selector('.product-iWrap, .product', timeout=15000)
            
            # 模拟滚动
            await self._simulate_scroll(page_obj)
            
            # 提取数据
            products = await self._extract_tmall_data(page_obj)
            
            return products
            
        except Exception as e:
            print(f"天猫搜索失败: {e}")
            return []
        finally:
            await page_obj.close()
    
    async def _check_captcha(self, page: Page) -> bool:
        """检查是否出现验证码"""
        captcha_selectors = [
            '#nc_1_wrapper',  # 滑块验证码
            '.nc-container',   # 滑块
            '#J_captcha',      # 验证码容器
            '.captcha-dialog', # 验证码弹窗
            'iframe[src*="captcha"]'  # 验证码iframe
        ]
        
        for selector in captcha_selectors:
            try:
                element = await page.query_selector(selector)
                if element and await element.is_visible():
                    return True
            except:
                continue
        
        return False
    
    async def _handle_captcha(self, page: Page) -> bool:
        """处理验证码"""
        try:
            # 方案1: 等待人工处理（开发/测试阶段）
            print("请手动完成验证码...")
            print("等待60秒...")
            await asyncio.sleep(60)
            
            # 检查是否通过
            return not await self._check_captcha(page)
            
        except Exception as e:
            print(f"验证码处理失败: {e}")
            return False
    
    async def _simulate_scroll(self, page: Page):
        """模拟人类滚动行为"""
        # 随机滚动几次
        scroll_times = random.randint(3, 6)
        
        for _ in range(scroll_times):
            # 随机滚动距离
            scroll_distance = random.randint(300, 800)
            
            # 平滑滚动
            await page.evaluate(f'''
                window.scrollBy({{
                    top: {scroll_distance},
                    behavior: 'smooth'
                }});
            ''')
            
            # 随机停留时间
            await self._random_delay(1, 3)
        
        # 滚动回顶部
        await page.evaluate('window.scrollTo(0, 0);')
        await self._random_delay(0.5, 1)
    
    async def _extract_taobao_data(self, page: Page) -> List[TaobaoProduct]:
        """提取淘宝商品数据"""
        products = []
        
        # 执行JavaScript提取数据
        items = await page.query_selector_all('.item, .Card--doubleCardWrapper--L2XFE73')
        
        for item in items[:10]:  # 取前10个
            try:
                # 提取标题
                title_elem = await item.query_selector('.title, .Text--title--jOqRVdF')
                title = await title_elem.inner_text() if title_elem else "未知商品"
                
                # 提取价格
                price_elem = await item.query_selector('.price, .Price--priceInt--ZlsSi_M')
                price_text = await price_elem.inner_text() if price_elem else "0"
                price = self._parse_price(price_text)
                
                # 提取店铺
                shop_elem = await item.query_selector('.shop, .Text--shop--DSSaZtT')
                shop_name = await shop_elem.inner_text() if shop_elem else "未知店铺"
                
                # 提取销量
                sales_elem = await item.query_selector('.deal-cnt, .Text--slk--FpQdRFz')
                sales = await sales_elem.inner_text() if sales_elem else "0"
                
                # 提取链接
                link_elem = await item.query_selector('a')
                href = await link_elem.get_attribute('href') if link_elem else ""
                url = f"https:{href}" if href.startswith('//') else href
                
                # 提取商品ID
                item_id = self._extract_item_id(url)
                
                product = TaobaoProduct(
                    item_id=item_id,
                    title=title.strip(),
                    price=price,
                    original_price=None,
                    discount="",
                    shop_name=shop_name.strip(),
                    shop_type="淘宝",
                    location="",
                    sales=sales,
                    url=url,
                    image=""
                )
                products.append(product)
                
            except Exception as e:
                print(f"提取商品数据失败: {e}")
                continue
        
        return products
    
    async def _extract_tmall_data(self, page: Page) -> List[TaobaoProduct]:
        """提取天猫商品数据"""
        products = []
        
        items = await page.query_selector_all('.product-iWrap, .product')
        
        for item in items[:10]:
            try:
                # 提取标题
                title_elem = await item.query_selector('.productTitle a')
                title = await title_elem.get_attribute('title') if title_elem else "未知商品"
                
                # 提取价格
                price_elem = await item.query_selector('.productPrice em')
                price_text = await price_elem.inner_text() if price_elem else "0"
                price = self._parse_price(price_text)
                
                # 提取店铺
                shop_elem = await item.query_selector('.productShop a')
                shop_name = await shop_elem.inner_text() if shop_elem else "未知店铺"
                
                # 提取销量
                sales_elem = await item.query_selector('.productStatus span')
                sales = await sales_elem.inner_text() if sales_elem else "0"
                
                # 提取链接
                link_elem = await item.query_selector('.productTitle a')
                href = await link_elem.get_attribute('href') if link_elem else ""
                url = f"https:{href}" if href.startswith('//') else href
                
                item_id = self._extract_item_id(url)
                
                product = TaobaoProduct(
                    item_id=item_id,
                    title=title.strip(),
                    price=price,
                    original_price=None,
                    discount="",
                    shop_name=shop_name.strip(),
                    shop_type="天猫",
                    location="",
                    sales=sales,
                    url=url,
                    image=""
                )
                products.append(product)
                
            except Exception as e:
                print(f"提取天猫数据失败: {e}")
                continue
        
        return products
    
    def _parse_price(self, price_text: str) -> float:
        """解析价格文本"""
        # 提取数字
        numbers = re.findall(r'[\d.]+', price_text.replace(',', ''))
        if numbers:
            return float(numbers[0])
        return 0.0
    
    def _extract_item_id(self, url: str) -> str:
        """从URL提取商品ID"""
        match = re.search(r'id=(\d+)', url)
        if match:
            return match.group(1)
        return ""
    
    async def _random_delay(self, min_sec: float, max_sec: float):
        """随机延迟"""
        delay = random.uniform(min_sec, max_sec)
        delay += random.gauss(0, 0.3)
        delay = max(min_sec, min(max_sec, delay))
        await asyncio.sleep(delay)
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


class TaobaoPriceComparison:
    """淘宝/天猫比价器"""
    
    def __init__(self, headless: bool = True):
        self.scraper = TaobaoScraper(headless=headless)
    
    async def compare(self, keyword: str, top_n: int = 3) -> Dict:
        """比价"""
        print(f"🔍 正在淘宝/天猫搜索: {keyword}...")
        
        # 初始化浏览器
        await self.scraper.init_browser()
        
        try:
            # 搜索淘宝
            taobao_products = await self.scraper.search_taobao(keyword, page=1)
            
            # 延迟后搜索天猫
            await asyncio.sleep(3)
            tmall_products = await self.scraper.search_tmall(keyword, page=1)
            
            # 合并结果
            all_products = taobao_products + tmall_products
            
            if not all_products:
                return {
                    'success': False,
                    'error': '未找到商品',
                    'results': []
                }
            
            # 按价格排序
            all_products.sort(key=lambda x: x.price)
            
            # 取前N个
            top_products = all_products[:top_n]
            
            # 找出最优选项
            best = self._find_best_option(top_products)
            
            return {
                'success': True,
                'keyword': keyword,
                'platform': '淘宝/天猫',
                'total_found': len(all_products),
                'results': [self._product_to_dict(p) for p in top_products],
                'best_option': best
            }
            
        finally:
            await self.scraper.close()
    
    def _find_best_option(self, products: List[TaobaoProduct]) -> Dict:
        """找出最佳选项"""
        if not products:
            return {}
        
        # 优先天猫旗舰店，其次按价格
        for p in products:
            if '旗舰' in p.shop_name or p.shop_type == '天猫':
                return {
                    'platform': p.shop_type,
                    'item_id': p.item_id,
                    'title': p.title,
                    'price': p.price,
                    'shop_name': p.shop_name,
                    'url': p.url,
                    'reason': '天猫旗舰店' if '旗舰' in p.shop_name else '天猫商家'
                }
        
        # 返回最低价
        cheapest = min(products, key=lambda x: x.price)
        return {
            'platform': cheapest.shop_type,
            'item_id': cheapest.item_id,
            'title': cheapest.title,
            'price': cheapest.price,
            'shop_name': cheapest.shop_name,
            'url': cheapest.url,
            'reason': '最低价'
        }
    
    def _product_to_dict(self, product: TaobaoProduct) -> Dict:
        """转换为字典"""
        return {
            'item_id': product.item_id,
            'title': product.title,
            'price': product.price,
            'original_price': product.original_price,
            'discount': product.discount,
            'shop_name': product.shop_name,
            'shop_type': product.shop_type,
            'sales': product.sales,
            'url': product.url
        }


async def main():
    """测试入口"""
    import sys
    
    keyword = sys.argv[1] if len(sys.argv) > 1 else "iPhone 16 Pro"
    
    comparator = TaobaoPriceComparison(headless=False)  # 非 headless 便于调试
    result = await comparator.compare(keyword)
    
    if result['success']:
        print(f"\n{'='*60}")
        print(f"🔍 淘宝/天猫比价结果: {result['keyword']}")
        print(f"{'='*60}\n")
        
        for i, p in enumerate(result['results'], 1):
            print(f"{i}. [{p['shop_type']}] {p['title'][:40]}...")
            print(f"   💰 ¥{p['price']:.0f}")
            print(f"   🏪 {p['shop_name']}")
            print(f"   📈 销量: {p['sales']}")
            print(f"   🔗 {p['url']}\n")
        
        best = result['best_option']
        print(f"{'='*60}")
        print(f"🏆 最佳选项")
        print(f"{'='*60}")
        print(f"平台: {best['platform']}")
        print(f"商品: {best['title'][:50]}")
        print(f"价格: ¥{best['price']:.0f}")
        print(f"店铺: {best['shop_name']}")
        print(f"理由: {best['reason']}")
        print(f"链接: {best['url']}")
    else:
        print(f"❌ {result['error']}")


if __name__ == '__main__':
    asyncio.run(main())
