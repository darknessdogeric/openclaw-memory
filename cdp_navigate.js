const WebSocket = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
const http = require('http');
const fs = require('fs');

const req = http.request({ hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' }, (res) => {
    let data = '';
    res.on('data', (c) => data += c);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        const target = tabs.find(t => (t.url||'').includes('douyin')) || tabs[0];
        console.log('Target:', target.title);

        const ws = new WebSocket(target.webSocketDebuggerUrl);

        ws.on('open', () => {
            console.log('Connected, navigating to creator page...');
            ws.send(JSON.stringify({ id: 1, method: 'Page.navigate', params: { url: 'https://creator.douyin.com/creator-micro/home' } }));
        });

        ws.on('message', (data) => {
            const msg = JSON.parse(data);
            if (msg.id === 1 && !msg.result) console.log('Sent nav command');
            if (msg.method === 'Page.loadEventFired') {
                console.log('Page loaded!');
                setTimeout(() => {
                    ws.send(JSON.stringify({ id: 2, method: 'Page.captureScreenshot', params: { format: 'png' } }));
                }, 2000);
            }
            if (msg.id === 2 && msg.result && msg.result.data) {
                const buf = Buffer.from(msg.result.data, 'base64');
                fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_creator.png', buf);
                console.log('Creator screenshot saved! Size:', buf.length);
                ws.close();
            }
        });

        ws.on('error', (e) => console.log('WS Error:', e.message));
        setTimeout(() => { ws.close(); process.exit(0); }, 15000);
    });
});
req.on('error', (e) => console.log('Error:', e.message));
req.setTimeout(5000, () => { req.destroy(); console.log('Timeout'); });
req.end();
