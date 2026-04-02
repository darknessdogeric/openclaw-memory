const WebSocket = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
const http = require('http');
const fs = require('fs');

const TITLE = '酒店老板都在转发的救命神器';

const req = http.request({ hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' }, (res) => {
    let data = '';
    res.on('data', (c) => data += c);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        const target = tabs[0];
        console.log('Tab:', target.title);

        const ws = new WebSocket(target.webSocketDebuggerUrl);
        let charIndex = 0;

        ws.on('open', () => {
            // Step 1: Focus title input
            ws.send(JSON.stringify({
                id: 1,
                method: 'Runtime.evaluate',
                params: {
                    expression: `
                        (function() {
                            var ins = document.querySelectorAll('input.semi-input');
                            for (var i = 0; i < ins.length; i++) {
                                if (ins[i].getAttribute('placeholder') && ins[i].getAttribute('placeholder').indexOf('标题') > -1) {
                                    ins[i].focus();
                                    return 'TITLE_FOCUSED';
                                }
                            }
                            return 'TITLE_NOT_FOUND';
                        })()
                    `
                }
            }));
        });

        ws.on('message', (data) => {
            const msg = JSON.parse(data.toString());
            const msgId = msg.id;

            if (msgId === 1) {
                console.log('Focus:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                if (msg.result && msg.result.result && msg.result.result.value === 'TITLE_FOCUSED') {
                    charIndex = 0;
                    // Start typing first character
                    ws.send(JSON.stringify({
                        id: 2,
                        method: 'Input.dispatchKeyEvent',
                        params: {
                            type: 'keyDown',
                            text: TITLE[0],
                            key: TITLE[0],
                            code: 'Space'
                        }
                    }));
                }
            } else if (msgId === 2 && charIndex === 0) {
                // First keyDown sent, send keyUp then next
                ws.send(JSON.stringify({
                    id: 3,
                    method: 'Input.dispatchKeyEvent',
                    params: {
                        type: 'keyUp',
                        text: TITLE[0],
                        key: TITLE[0],
                        code: 'Space'
                    }
                }));
            } else if (msgId === 3) {
                charIndex++;
                if (charIndex < TITLE.length) {
                    const ch = TITLE[charIndex];
                    // keyDown
                    ws.send(JSON.stringify({
                        id: 4 + charIndex * 2,
                        method: 'Input.dispatchKeyEvent',
                        params: { type: 'keyDown', text: ch, key: ch, code: 'Space' }
                    }));
                } else {
                    // Done typing, screenshot
                    console.log('Done typing title');
                    setTimeout(() => {
                        ws.send(JSON.stringify({ id: 999, method: 'Page.captureScreenshot', params: { format: 'png' } }));
                    }, 2000);
                }
            } else if (msgId > 3 && msgId % 2 === 0) {
                // keyUp
                const ch = TITLE[(msgId - 4) / 2];
                ws.send(JSON.stringify({
                    id: msgId + 1,
                    method: 'Input.dispatchKeyEvent',
                    params: { type: 'keyUp', text: ch, key: ch, code: 'Space' }
                }));
            } else if (msgId > 3 && msgId % 2 === 1 && msgId < 900) {
                charIndex++;
                if (charIndex < TITLE.length) {
                    const ch = TITLE[charIndex];
                    ws.send(JSON.stringify({
                        id: msgId + 1,
                        method: 'Input.dispatchKeyEvent',
                        params: { type: 'keyDown', text: ch, key: ch, code: 'Space' }
                    }));
                } else {
                    console.log('Done typing');
                    setTimeout(() => {
                        ws.send(JSON.stringify({ id: 999, method: 'Page.captureScreenshot', params: { format: 'png' } }));
                    }, 2000);
                }
            } else if (msgId === 999 && msg.result && msg.result.data) {
                const buf = Buffer.from(msg.result.data, 'base64');
                fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_keyboard_fill.png', buf);
                console.log('Screenshot saved! Size:', buf.length);
                ws.close();
                process.exit(0);
            }
        });

        ws.on('error', (e) => { console.log('WS Error:', e.message); process.exit(1); });
        setTimeout(() => { console.log('Timeout'); ws.close(); process.exit(0); }, 30000);
    });
});
req.on('error', (e) => { console.log('Error:', e.message); process.exit(1); });
req.setTimeout(5000, () => process.exit(1));
req.end();
