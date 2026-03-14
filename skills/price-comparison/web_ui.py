#!/usr/bin/env python3
"""
Price Comparison Web UI - 全网比价Web界面
使用Flask提供可视化界面
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from universal_price_compare import UniversalPriceComparator
from price_cache import PriceCacheManager, PriceMonitor

app = Flask(__name__)

# 全局实例
comparator = None
cache_manager = None
price_monitor = None


def init_app():
    """初始化应用"""
    global comparator, cache_manager, price_monitor
    
    comparator = UniversalPriceComparator(
        platforms=['jd', 'taobao', 'pdd'],
        use_proxy=False,
        taobao_headless=True
    )
    
    cache_manager = PriceCacheManager()
    price_monitor = PriceMonitor(cache_manager)
    
    print("✅ Web应用初始化完成")


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def api_search():
    """API: 搜索比价"""
    data = request.json
    keyword = data.get('keyword', '').strip()
    platforms = data.get('platforms', ['jd', 'taobao', 'pdd'])
    use_cache = data.get('use_cache', True)
    
    if not keyword:
        return jsonify({'success': False, 'error': '请输入商品名称'})
    
    # 检查缓存
    if use_cache:
        cached_results = []
        for platform in platforms:
            cached = cache_manager.get_cached_price(keyword, platform)
            if cached:
                cached_results.append({
                    'platform': platform,
                    'from_cache': True,
                    'data': cached
                })
        
        if cached_results and len(cached_results) == len(platforms):
            return jsonify({
                'success': True,
                'keyword': keyword,
                'from_cache': True,
                'results': cached_results,
                'message': '返回缓存数据'
            })
    
    # 执行比价
    try:
        result = comparator.compare(keyword, top_n=5)
        
        # 缓存结果
        if result['success']:
            for item in result['results']:
                cache_manager.cache_price(
                    keyword,
                    item['platform'],
                    item
                )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/history/<sku_id>')
def api_history(sku_id):
    """API: 获取价格历史"""
    platform = request.args.get('platform', 'jd')
    days = int(request.args.get('days', 7))
    
    history = cache_manager.get_price_history(sku_id, platform, days)
    trend = cache_manager.get_price_trend(sku_id, platform)
    
    return jsonify({
        'success': True,
        'sku_id': sku_id,
        'platform': platform,
        'history': history,
        'trend': trend
    })


@app.route('/api/stats')
def api_stats():
    """API: 获取统计信息"""
    cache_stats = cache_manager.get_cache_stats()
    
    return jsonify({
        'success': True,
        'cache': cache_stats,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/alert', methods=['POST'])
def api_set_alert():
    """API: 设置价格提醒"""
    data = request.json
    
    keyword = data.get('keyword')
    platform = data.get('platform', 'jd')
    target_price = float(data.get('target_price', 0))
    email = data.get('email')
    
    if not keyword or target_price <= 0:
        return jsonify({
            'success': False,
            'error': '参数错误'
        })
    
    success = price_monitor.set_price_alert(
        keyword, platform, target_price, email
    )
    
    return jsonify({
        'success': success,
        'message': '提醒设置成功' if success else '设置失败'
    })


# HTML模板（内联）
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>全网比价工具 - Price Comparison</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .search-box {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        
        .search-form {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .search-input {
            flex: 1;
            min-width: 300px;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .search-input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .platform-select {
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            min-width: 150px;
        }
        
        .search-btn {
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .search-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .search-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .results {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            display: none;
        }
        
        .results.show {
            display: block;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .platform-section {
            margin-bottom: 30px;
        }
        
        .platform-title {
            font-size: 1.3em;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        
        .product-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .product-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        
        .product-title {
            font-size: 1.1em;
            color: #333;
            margin-bottom: 10px;
        }
        
        .product-price {
            font-size: 1.5em;
            color: #e74c3c;
            font-weight: bold;
        }
        
        .product-original-price {
            color: #999;
            text-decoration: line-through;
            margin-left: 10px;
        }
        
        .product-discount {
            background: #e74c3c;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            margin-left: 10px;
        }
        
        .product-shop {
            color: #666;
            margin-top: 8px;
        }
        
        .product-score {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 10px;
        }
        
        .best-option {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border-radius: 15px;
            padding: 25px;
            margin-top: 30px;
        }
        
        .best-option h3 {
            font-size: 1.3em;
            margin-bottom: 15px;
        }
        
        .best-option .price {
            font-size: 2em;
            font-weight: bold;
        }
        
        .error-message {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        footer {
            text-align: center;
            color: white;
            margin-top: 30px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔍 全网比价工具</h1>
            <p class="subtitle">支持京东、淘宝、天猫、拼多多</p>
        </header>
        
        <div class="search-box">
            <form class="search-form" id="searchForm">
                <input type="text" class="search-input" id="keyword" 
                       placeholder="输入商品名称，如：iPhone 16 Pro" required>
                <select class="platform-select" id="platforms" multiple>
                    <option value="jd" selected>京东</option>
                    <option value="taobao">淘宝</option>
                    <option value="pdd">拼多多</option>
                </select>
                <button type="submit" class="search-btn" id="searchBtn">开始比价</button>
            </form>
        </div>
        
        <div class="results" id="results">
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>正在全网搜索，请稍候...</p>
            </div>
            <div id="resultsContent"></div>
        </div>
        
        <footer>
            <p>Price Comparison Skill v3.0 | Powered by B166ER</p>
        </footer>
    </div>
    
    <script>
        document.getElementById('searchForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const keyword = document.getElementById('keyword').value;
            const platformsSelect = document.getElementById('platforms');
            const platforms = Array.from(platformsSelect.selectedOptions).map(o => o.value);
            
            const resultsDiv = document.getElementById('results');
            const loadingDiv = document.getElementById('loading');
            const contentDiv = document.getElementById('resultsContent');
            const searchBtn = document.getElementById('searchBtn');
            
            // 显示加载状态
            resultsDiv.classList.add('show');
            loadingDiv.style.display = 'block';
            contentDiv.innerHTML = '';
            searchBtn.disabled = true;
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        keyword: keyword,
                        platforms: platforms,
                        use_cache: true
                    })
                });
                
                const data = await response.json();
                
                loadingDiv.style.display = 'none';
                
                if (data.success) {
                    renderResults(data);
                } else {
                    contentDiv.innerHTML = `
                        <div class="error-message">
                            查询失败：${data.error || '未知错误'}
                        </div>
                    `;
                }
            } catch (error) {
                loadingDiv.style.display = 'none';
                contentDiv.innerHTML = `
                    <div class="error-message">
                        网络错误：${error.message}
                    </div>
                `;
            } finally {
                searchBtn.disabled = false;
            }
        });
        
        function renderResults(data) {
            const contentDiv = document.getElementById('resultsContent');
            let html = '';
            
            // 按平台分组
            const platformGroups = {};
            data.results.forEach(item => {
                if (!platformGroups[item.platform]) {
                    platformGroups[item.platform] = [];
                }
                platformGroups[item.platform].push(item);
            });
            
            // 渲染每个平台
            for (const [platform, items] of Object.entries(platformGroups)) {
                html += `
                    <div class="platform-section">
                        <h3 class="platform-title">📦 ${platform}</h3>
                `;
                
                items.forEach(item => {
                    html += `
                        <div class="product-card">
                            <div class="product-title">${item.title}</div>
                            <div>
                                <span class="product-price">¥${item.price.toFixed(0)}</span>
                                ${item.original_price ? `
                                    <span class="product-original-price">¥${item.original_price.toFixed(0)}</span>
                                ` : ''}
                                ${item.discount ? `<span class="product-discount">${item.discount}</span>` : ''}
                            </div>
                            <div class="product-shop">
                                🏪 ${item.shop_name} (${item.shop_type})
                            </div>
                            <span class="product-score">⭐ 推荐度: ${item.recommendation_score}/100</span>
                        </div>
                    `;
                });
                
                html += '</div>';
            }
            
            // 最佳选项
            if (data.best_option) {
                const best = data.best_option;
                html += `
                    <div class="best-option">
                        <h3>🏆 最佳购买选项</h3>
                        <div style="margin-bottom: 10px;">${best.platform} - ${best.title}</div>
                        <div class="price">¥${best.price.toFixed(0)}</div>
                        <div style="margin-top: 10px;">
                            🏪 ${best.shop_name}<br>
                            ✨ ${best.reason}<br>
                            🔗 <a href="${best.url}" target="_blank" style="color: white;">查看商品</a>
                        </div>
                    </div>
                `;
            }
            
            contentDiv.innerHTML = html;
        }
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    """首页 - 直接返回HTML"""
    return HTML_TEMPLATE


def main():
    """启动Web服务器"""
    init_app()
    
    print("\n" + "="*60)
    print("🌐 全网比价Web界面")
    print("="*60)
    print("\n启动服务器...")
    print("访问地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务器\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    main()
