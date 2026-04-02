const WebSocket = require('ws');
const http = require('http');

// Get Chrome tabs
const options = { hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' };
const req = http.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => data += chunk);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        if (!tabs.length) { console.log('No tabs'); process.exit(1); }
        const target = tabs.find(t => t.type === 'page') || tabs[0];
        console.log('Using tab:', target.title, target.url);

        const ws = new WebSocket(target.webSocketDebuggerUrl);
        let id = 1;

        ws.on('open', () => {
            console.log('Connected, navigating to Douyin...');
            ws.send(JSON.stringify({ id: id++, method: 'Page.navigate', params: { url: 'https://www.douyin.com' } }));
        });

        ws.on('message', (data) => {
            const msg = JSON.parse(data);
            if (msg.id === 1 && !msg.result && msg.error) console.log('Error:', msg.error);
            else if (msg.id === 1) console.log('Navigation command sent');
        });

        ws.on('error', (e) => console.log('WS Error:', e.message));
        setTimeout(() => { ws.close(); console.log('Done'); }, 3000);
    });
});
req.on('error', (e) => console.log('HTTP Error:', e.message));
req.setTimeout(5000, () => { req.destroy(); console.log('Timeout'); });
req.end();
