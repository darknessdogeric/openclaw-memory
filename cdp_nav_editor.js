const WebSocket = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
const http = require('http');
const fs = require('fs');

const req = http.request({ hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' }, (res) => {
    let data = '';
    res.on('data', (c) => data += c);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        const target = tabs[0];
        console.log('Target:', target.title);

        const ws = new WebSocket(target.webSocketDebuggerUrl);

        ws.on('open', () => {
            // 尝试多个可能的图文发布URL
            const urls = [
                'https://creator.douyin.com/creator-micro/content/publish/picture-text',
                'https://creator.douyin.com/creator-micro/content/publish',
            ];
            console.log('Navigating to:', urls[0]);
            ws.send(JSON.stringify({ id: 1, method: 'Page.navigate', params: { url: urls[0] } }));
        });

        let loaded = false;
        ws.on('message', (data) => {
            const msg = JSON.parse(data.toString());
            if (msg.id === 1) console.log('Nav sent');
            if (msg.method === 'Page.loadEventFired') {
                if (!loaded) {
                    console.log('Page loaded, waiting for content...');
                    loaded = true;
                    setTimeout(() => {
                        ws.send(JSON.stringify({ id: 2, method: 'Page.captureScreenshot', params: { format: 'png' } }));
                    }, 4000);
                }
            }
            if (msg.id === 2 && msg.result && msg.result.data) {
                const buf = Buffer.from(msg.result.data, 'base64');
                fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_editor2.png', buf);
                console.log('Screenshot saved! Size:', buf.length);
                ws.close();
                process.exit(0);
            }
        });

        ws.on('error', (e) => { console.log('WS Error:', e.message); process.exit(1); });
        setTimeout(() => { console.log('Timeout'); ws.close(); process.exit(0); }, 20000);
    });
});
req.on('error', (e) => { console.log('Error:', e.message); process.exit(1); });
req.setTimeout(5000, () => { process.exit(1); });
req.end();
