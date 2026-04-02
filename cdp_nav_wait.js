const WebSocket = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
const http = require('http');
const fs = require('fs');

const req = http.request({ hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' }, (res) => {
    let data = '';
    res.on('data', (c) => data += c);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        const target = tabs[0]; // first tab
        console.log('Target:', target.title, target.url);

        const ws = new WebSocket(target.webSocketDebuggerUrl);
        let navDone = false;

        ws.on('open', () => {
            console.log('WS connected');
            ws.send(JSON.stringify({ id: 1, method: 'Page.navigate', params: { url: 'https://creator.douyin.com/creator-micro/home' } }));
        });

        ws.on('message', (data) => {
            const msg = JSON.parse(data.toString());
            if (msg.id === 1) {
                console.log('Nav command sent');
                navDone = true;
            }
            if (msg.method === 'Page.loadEventFired') {
                console.log('Page fully loaded');
                setTimeout(() => {
                    ws.send(JSON.stringify({ id: 2, method: 'Page.captureScreenshot', params: { format: 'png' } }));
                }, 3000);
            }
            if (msg.id === 2 && msg.result && msg.result.data) {
                const buf = Buffer.from(msg.result.data, 'base64');
                fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_creator.png', buf);
                console.log('Screenshot saved! Size:', buf.length);
                ws.close();
                process.exit(0);
            }
        });

        ws.on('error', (e) => console.log('WS Error:', e.message));
        setTimeout(() => { console.log('Timeout reached'); ws.close(); process.exit(0); }, 20000);
    });
});
req.on('error', (e) => { console.log('Error:', e.message); process.exit(1); });
req.setTimeout(5000, () => { console.log('HTTP Timeout'); req.destroy(); process.exit(1); });
req.end();
