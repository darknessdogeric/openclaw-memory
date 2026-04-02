const WebSocket = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
const http = require('http');
const fs = require('fs');

const req = http.request({ hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' }, (res) => {
    let data = '';
    res.on('data', (c) => data += c);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        const target = tabs[0];
        const ws = new WebSocket(target.webSocketDebuggerUrl);

        ws.on('open', () => {
            // Find ALL elements with text "#添加话题"
            ws.send(JSON.stringify({
                id: 1,
                method: 'Runtime.evaluate',
                params: {
                    expression: `
                        (function() {
                            var result = [];
                            var all = document.querySelectorAll('*');
                            for (var i = 0; i < all.length; i++) {
                                var el = all[i];
                                var txt = (el.innerText || '').trim();
                                if (txt === '#添加话题' || txt === '#添加话题或@好友') {
                                    var rect = el.getBoundingClientRect();
                                    if (rect.width > 0 && rect.height > 0) {
                                        result.push({
                                            tag: el.tagName,
                                            cls: el.className.substring(0, 60),
                                            text: txt,
                                            x: Math.round(rect.x),
                                            y: Math.round(rect.y),
                                            w: Math.round(rect.width),
                                            h: Math.round(rect.height)
                                        });
                                    }
                                }
                            }
                            return JSON.stringify(result);
                        })()
                    `
                }
            }));
        });

        ws.on('message', (data) => {
            const msg = JSON.parse(data.toString());
            if (msg.id === 1) {
                const r = msg.result && msg.result.result && msg.result.result.value;
                if (r) {
                    console.log('Found hashtag elements:', r);
                } else {
                    console.log('Result:', msg.result);
                }
                ws.close();
                process.exit(0);
            }
        });

        ws.on('error', (e) => { console.log('WS Error:', e.message); process.exit(1); });
        setTimeout(() => { ws.close(); process.exit(0); }, 15000);
    });
});
req.on('error', (e) => { console.log('Error:', e.message); process.exit(1); });
req.setTimeout(5000, () => process.exit(1));
req.end();
