# -*- coding: utf-8 -*-
"""
call_deepseek.py - DeepSeek API 调用（骨架）
历史：methodology/sop-region-analysis.md 引用。v1.0 骨架 — 执行摘要用。
"""
import os, sys, json, urllib.request

def call_deepseek(prompt: str, model: str = 'deepseek-chat', max_tokens: int = 2000) -> dict:
    """
    调用 DeepSeek API。
    Key: 优先 DEEPSEEK_API_KEY 环境变量。
    """
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    if not api_key:
        return {'error': 'DEEPSEEK_API_KEY 未设置', 'fallback': 'manual'}

    payload = json.dumps({
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens,
        'temperature': 0.3,
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.deepseek.com/v1/chat/completions',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return {
                'content': data['choices'][0]['message']['content'],
                'model': model,
                'usage': data.get('usage', {}),
            }
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    prompt = ' '.join(sys.argv[1:]) or '写一段酒店行业 2026 趋势的执行摘要。'
    print(json.dumps(call_deepseek(prompt), ensure_ascii=False, indent=2)[:2000])