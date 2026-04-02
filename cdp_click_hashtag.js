const WebSocket = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
const http = require('http');
const fs = require('fs');
const SCREENSHOT_PATH = 'C:\\Users\\ericz\\.openclaw\\workspace\\douyin_snap.png';
const HASHTAGS = '#酒店创业 #民宿运营 #AI工具 #去中心化';

const req = http.request({ hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' }, (res) => {
    let data = '';
    res.on('data', (c) => data += c);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        const target = tabs[0];
        const ws = new WebSocket(target.webSocketDebuggerUrl);
        let step = 0;

        function sendScreenshot(ws, id) {
            ws.send(JSON.stringify({ id: id, method: 'Page.captureScreenshot', params: { format: 'png' } }));
        }

        ws.on('open', () => {
            // Click the hashtag button
            ws.send(JSON.stringify({
                id: 1,
                method: 'Runtime.evaluate',
                params: {
                    expression: `
                        (function() {
                            var all = document.querySelectorAll('div');
                            for (var i = 0; i < all.length; i++) {
                                if (all[i].innerText.trim() === '#添加话题' && all[i].getBoundingClientRect().width > 0) {
                                    all[i].click();
                                    return 'CLICKED';
                                }
                            }
                            return 'NOT_FOUND';
                        })()
                    `
                }
            }));
        });

        ws.on('message', (data) => {
            const msg = JSON.parse(data.toString());
            const msgId = msg.id;

            if (msgId === 1) {
                console.log('Click:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                setTimeout(function() { sendScreenshot(ws, 2); }, 1500);
            } else if (msgId === 2 && msg.result && msg.result.data) {
                const buf = Buffer.from(msg.result.data, 'base64');
                fs.writeFileSync(SCREENSHOT_PATH, buf);
                console.log('Snap1 saved');
                // Find and fill hashtag input
                ws.send(JSON.stringify({
                    id: 3,
                    method: 'Runtime.evaluate',
                    params: {
                        expression: `
                            (function() {
                                var inputs = document.querySelectorAll('input');
                                for (var i = 0; i < inputs.length; i++) {
                                    var ph = inputs[i].getAttribute('placeholder') || '';
                                    if (ph.indexOf('#') > -1 || ph.indexOf('话题') > -1) {
                                        inputs[i].focus();
                                        inputs[i].value = ${JSON.stringify(HASHTAGS)};
                                        inputs[i].dispatchEvent(new Event('input', {bubbles:true}));
                                        inputs[i].dispatchEvent(new Event('change', {bubbles:true}));
                                        return 'HASHTAG_OK:' + inputs[i].value;
                                    }
                                }
                                return 'NOT_FOUND';
                            })()
                        `
                    }
                }));
            } else if (msgId === 3) {
                console.log('Hashtag:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                setTimeout(function() { sendScreenshot(ws, 4); }, 1500);
            } else if (msgId === 4 && msg.result && msg.result.data) {
                const buf = Buffer.from(msg.result.data, 'base64');
                fs.writeFileSync(SCREENSHOT_PATH, buf);
                console.log('Snap2 saved! Done.');
                ws.close();
                process.exit(0);
            }
        });

        ws.on('error', (e) => { console.log('WS Error:', e.message); process.exit(1); });
        setTimeout(() => { console.log('Timeout'); ws.close(); process.exit(0); }, 25000);
    });
});
req.on('error', (e) => { console.log('Error:', e.message); process.exit(1); });
req.setTimeout(5000, () => process.exit(1));
req.end();
