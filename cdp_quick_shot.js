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
            console.log('Connected, taking screenshot...');
            ws.send(JSON.stringify({ id: 1, method: 'Page.captureScreenshot', params: { format: 'png' } }));
        });

        ws.on('message', (data) => {
            const msg = JSON.parse(data.toString());
            if (msg.id === 1 && msg.result && msg.result.data) {
                const buf = Buffer.from(msg.result.data, 'base64');
                fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_creator.png', buf);
                console.log('Screenshot saved! Size:', buf.length);
                ws.close();
                process.exit(0);
            }
            if (msg.id === 1 && msg.error) {
                console.log('Error:', JSON.stringify(msg.error));
                ws.close();
                process.exit(1);
            }
        });

        ws.on('error', (e) => { console.log('WS Error:', e.message); process.exit(1); });
        setTimeout(() => { console.log('Timeout'); ws.close(); process.exit(1); }, 10000);
    });
});
req.on('error', (e) => { console.log('HTTP Error:', e.message); process.exit(1); });
req.setTimeout(5000, () => { console.log('HTTP Timeout'); process.exit(1); });
req.end();
