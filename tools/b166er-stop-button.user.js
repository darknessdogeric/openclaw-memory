// ==UserScript==
// @name         B166ER Emergency Stop Button
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  在 OpenClaw Web UI 添加紧急停止按钮
// @author       B166ER
// @match        http://localhost:3000/*
// @match        http://127.0.0.1:3000/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // 等待页面加载完成
    function init() {
        // 创建停止按钮
        const stopButton = document.createElement('button');
        stopButton.id = 'b166er-stop-btn';
        stopButton.innerHTML = '⏹ 停止';
        stopButton.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            background: linear-gradient(145deg, #ff4444, #cc0000);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(255, 68, 68, 0.4);
            transition: all 0.3s ease;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        `;

        // 悬停效果
        stopButton.addEventListener('mouseenter', () => {
            stopButton.style.transform = 'scale(1.05)';
            stopButton.style.boxShadow = '0 6px 20px rgba(255, 68, 68, 0.5)';
        });

        stopButton.addEventListener('mouseleave', () => {
            stopButton.style.transform = 'scale(1)';
            stopButton.style.boxShadow = '0 4px 15px rgba(255, 68, 68, 0.4)';
        });

        // 点击事件
        stopButton.addEventListener('click', async () => {
            if (stopButton.disabled) return;

            stopButton.disabled = true;
            stopButton.innerHTML = '⏳ 停止中...';
            stopButton.style.background = 'linear-gradient(145deg, #ff8800, #cc6600)';

            try {
                // 尝试通过 API 停止当前执行
                const response = await fetch('/api/sessions/stop', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });

                if (response.ok) {
                    stopButton.innerHTML = '✓ 已停止';
                    stopButton.style.background = 'linear-gradient(145deg, #44ff44, #00cc00)';
                    showNotification('✓ 执行已停止', 'success');
                } else {
                    throw new Error('Stop failed');
                }
            } catch (error) {
                // 备用方案：发送中断信号
                try {
                    await fetch('/api/interrupt', { method: 'POST' });
                    stopButton.innerHTML = '✓ 已中断';
                    stopButton.style.background = 'linear-gradient(145deg, #44ff44, #00cc00)';
                    showNotification('✓ 执行已中断', 'success');
                } catch (e) {
                    stopButton.innerHTML = '✗ 失败';
                    stopButton.style.background = 'linear-gradient(145deg, #888, #666)';
                    showNotification('✗ 停止失败，请刷新页面', 'error');
                }
            }

            // 3秒后重置按钮
            setTimeout(() => {
                stopButton.disabled = false;
                stopButton.innerHTML = '⏹ 停止';
                stopButton.style.background = 'linear-gradient(145deg, #ff4444, #cc0000)';
            }, 3000);
        });

        // 添加到页面
        document.body.appendChild(stopButton);

        // 添加键盘快捷键 Ctrl+Shift+S
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'S') {
                e.preventDefault();
                stopButton.click();
            }
        });

        console.log('[B166ER] 紧急停止按钮已加载');
        console.log('[B166ER] 快捷键: Ctrl+Shift+S');
    }

    // 显示通知
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 10000;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            color: white;
            background: ${type === 'success' ? 'linear-gradient(145deg, #44ff44, #00cc00)' : 'linear-gradient(145deg, #ff4444, #cc0000)'};
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;

        // 添加动画样式
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
