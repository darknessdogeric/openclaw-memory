const WebSocket = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
const http = require('http');
const fs = require('fs');

const req = http.request({ hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' }, (res) => {
    let data = '';
    res.on('data', (c) => data += c);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        const target = tabs[0];
        console.log('Using tab:', target.title);

        const ws = new WebSocket(target.webSocketDebuggerUrl);

        ws.on('open', () => {
            console.log('Connected');
            // 先点击"发布图文"按钮 - 使用 Runtime.evaluate 在页面执行点击
            ws.send(JSON.stringify({
                id: 1,
                method: 'Runtime.evaluate',
                params: {
                    expression: `
                        // 找到"发布图文"按钮并点击
                        const buttons = document.querySelectorAll('*');
                        let clicked = false;
                        for (const btn of buttons) {
                            if (btn.innerText && btn.innerText.includes('发布图文') && btn.offsetParent !== null) {
                                btn.click();
                                console.log('Clicked:', btn.innerText);
                                clicked = true;
                                break;
                            }
                        }
                        clicked ? 'CLICKED' : 'NOT_FOUND';
                    `
                }
            }));
        });

        ws.on('message', (data) => {
            const msg = JSON.parse(data.toString());
            if (msg.id === 1) {
                console.log('Click result:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                // 等待页面加载后截图
                setTimeout(() => {
                    ws.send(JSON.stringify({ id: 2, method: 'Page.captureScreenshot', params: { format: 'png' } }));
                }, 3000);
            }
            if (msg.id === 2 && msg.result && msg.result.data) {
                const buf = Buffer.from(msg.result.data, 'base64');
                fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_editor.png', buf);
                console.log('Editor screenshot saved! Size:', buf.length);
                ws.close();
                process.exit(0);
            }
        });

        ws.on('error', (e) => { console.log('WS Error:', e.message); process.exit(1); });
        setTimeout(() => { console.log('Timeout'); ws.close(); process.exit(1); }, 15000);
    });
});
req.on('error', (e) => { console.log('HTTP Error:', e.message); process.exit(1); });
req.setTimeout(5000, () => { process.exit(1); });
req.end();
