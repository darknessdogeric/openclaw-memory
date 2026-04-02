const WebSocket = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
const fs = require('fs');
const http = require('http');

const req = http.request({ hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' }, (res) => {
    let data = '';
    res.on('data', (c) => data += c);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        const target = tabs.find(t => (t.url||'').includes('douyin')) || tabs[0];
        console.log('Connecting to:', target.title);

        const ws = new WebSocket(target.webSocketDebuggerUrl);

        ws.on('open', () => {
            ws.send(JSON.stringify({ id: 1, method: 'Page.captureScreenshot', params: { format: 'png' } }));
        });

        ws.on('message', (data) => {
            const msg = JSON.parse(data);
            if (msg.id === 1 && msg.result && msg.result.data) {
                const buf = Buffer.from(msg.result.data, 'base64');
                fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_screenshot.png', buf);
                console.log('Screenshot saved! Size:', buf.length, 'bytes');
                ws.close();
            } else if (msg.id === 1 && msg.error) {
                console.log('Error:', JSON.stringify(msg.error));
                ws.close();
            }
        });

        ws.on('error', (e) => console.log('WS Error:', e.message));
        setTimeout(() => { ws.close(); process.exit(0); }, 10000);
    });
});
req.on('error', (e) => console.log('Error:', e.message));
req.setTimeout(5000, () => { req.destroy(); console.log('Timeout'); });
req.end();
