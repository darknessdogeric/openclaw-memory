const WebSocket = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
const http = require('http');
const fs = require('fs');

const HASHTAGS = '#酒店创业 #民宿运营 #AI工具 #去中心化';

const req = http.request({ hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' }, (res) => {
    let data = '';
    res.on('data', (c) => data += c);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        const target = tabs[0];
        console.log('Tab:', target.title);
        const ws = new WebSocket(target.webSocketDebuggerUrl);

        ws.on('open', () => {
            // Find and focus hashtag input
            ws.send(JSON.stringify({
                id: 1,
                method: 'Runtime.evaluate',
                params: {
                    expression: `
                        (function() {
                            var inputs = document.querySelectorAll('input');
                            for (var i = 0; i < inputs.length; i++) {
                                var ph = inputs[i].getAttribute('placeholder') || '';
                                var style = window.getComputedStyle(inputs[i]);
                                if ((ph.indexOf('话题') > -1 || ph.indexOf('#') > -1) &&
                                    style.display !== 'none' && style.visibility !== 'hidden') {
                                    inputs[i].scrollIntoView();
                                    inputs[i].focus();
                                    return 'HASHTAG_FOCUSED:' + ph;
                                }
                            }
                            return 'HASHTAG_NOT_FOUND';
                        })()
                    `
                }
            }));
        });

        ws.on('message', (data) => {
            const msg = JSON.parse(data.toString());
            const msgId = msg.id;

            if (msgId === 1) {
                const res = msg.result && msg.result.result ? msg.result.result.value : msg.result;
                console.log('Hashtag focus:', res);
                // Try to find hashtag input via DOM
                if (res === 'HASHTAG_NOT_FOUND') {
                    // Use Tab key to navigate to next field
                    ws.send(JSON.stringify({
                        id: 2,
                        method: 'Input.dispatchKeyEvent',
                        params: { type: 'keyDown', key: 'Tab', code: 'Tab' }
                    }));
                } else {
                    // Type hashtags
                    typeChars(ws, HASHTAGS, 3);
                }
            } else if (msgId === 2) {
                ws.send(JSON.stringify({
                    id: 3,
                    method: 'Input.dispatchKeyEvent',
                    params: { type: 'keyUp', key: 'Tab', code: 'Tab' }
                }));
            } else if (msgId === 3) {
                // Should now be on hashtag field, type
                typeChars(ws, HASHTAGS, 4);
            }
        });

        let charIndex = 0;
        function typeChars(ws, text, startId) {
            charIndex = 0;
            ws.send(JSON.stringify({
                id: startId,
                method: 'Input.dispatchKeyEvent',
                params: { type: 'keyDown', text: text[0], key: text[0], code: 'Space' }
            }));
            ws._onMessage = ws.onmessage;
            ws.onmessage = function(d) {
                const m = JSON.parse(d.toString());
                const mId = m.id;
                if (mId === startId) {
                    ws.send(JSON.stringify({ id: startId + 1, method: 'Input.dispatchKeyEvent', params: { type: 'keyUp', text: text[0], key: text[0], code: 'Space' } }));
                } else if (mId === startId + 1) {
                    charIndex++;
                    if (charIndex < text.length) {
                        const ch = text[charIndex];
                        ws.send(JSON.stringify({ id: startId + 2, method: 'Input.dispatchKeyEvent', params: { type: 'keyDown', text: ch, key: ch, code: 'Space' } }));
                        setTimeout(() => {
                            ws.send(JSON.stringify({ id: startId + 3, method: 'Input.dispatchKeyEvent', params: { type: 'keyUp', text: ch, key: ch, code: 'Space' } }));
                        }, 10);
                    } else {
                        // Done, screenshot
                        setTimeout(() => {
                            ws.send(JSON.stringify({ id: 100, method: 'Page.captureScreenshot', params: { format: 'png' } }));
                        }, 2000);
                    }
                } else if (mId === startId + 2) {
                    // keyUp was sent via setTimeout
                } else if (mId === startId + 3) {
                    charIndex++;
                    if (charIndex < text.length) {
                        const ch = text[charIndex];
                        ws.send(JSON.stringify({ id: startId + 2, method: 'Input.dispatchKeyEvent', params: { type: 'keyDown', text: ch, key: ch, code: 'Space' } }));
                        setTimeout(() => {
                            ws.send(JSON.stringify({ id: startId + 3, method: 'Input.dispatchKeyEvent', params: { type: 'keyUp', text: ch, key: ch, code: 'Space' } }));
                        }, 10);
                    } else {
                        setTimeout(() => {
                            ws.send(JSON.stringify({ id: 100, method: 'Page.captureScreenshot', params: { format: 'png' } }));
                        }, 2000);
                    }
                } else if (mId === 100 && m.result && m.result.data) {
                    const buf = Buffer.from(m.result.data, 'base64');
                    fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_tags_done.png', buf);
                    console.log('Done! Screenshot saved! Size:', buf.length);
                    ws.close();
                    process.exit(0);
                }
            };
        }

        ws.on('error', (e) => { console.log('WS Error:', e.message); process.exit(1); });
        setTimeout(() => { console.log('Timeout'); ws.close(); process.exit(0); }, 30000);
    });
});
req.on('error', (e) => { console.log('Error:', e.message); process.exit(1); });
req.setTimeout(5000, () => process.exit(1));
req.end();
