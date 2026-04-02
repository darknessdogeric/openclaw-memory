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
            // Find ALL input/textarea/editable elements with their placeholders
            ws.send(JSON.stringify({
                id: 1,
                method: 'Runtime.evaluate',
                params: {
                    expression: `
                        (function() {
                            const result = [];
                            const all = document.querySelectorAll('input, textarea, [contenteditable="true"], div');
                            for (const el of all) {
                                const ph = el.getAttribute('placeholder') || '';
                                const tag = el.tagName;
                                const cls = el.className || '';
                                const id = el.id || '';
                                const txt = (el.innerText || '').substring(0, 50);
                                const rect = el.getBoundingClientRect();
                                if (ph || el.contentEditable === 'true') {
                                    result.push({
                                        tag: tag,
                                        placeholder: ph,
                                        class: cls.substring(0, 80),
                                        id: id,
                                        text: txt,
                                        visible: rect.width > 0 && rect.height > 0,
                                        x: Math.round(rect.x),
                                        y: Math.round(rect.y),
                                        w: Math.round(rect.width),
                                        h: Math.round(rect.height)
                                    });
                                }
                            }
                            return JSON.stringify(result.filter(r => r.visible).slice(0, 20));
                        })()
                    `
                }
            }));
        });

        ws.on('message', (data) => {
            const msg = JSON.parse(data.toString());
            if (msg.id === 1 && msg.result && msg.result.result) {
                try {
                    const found = JSON.parse(msg.result.result.value);
                    console.log('Found', found.length, 'editable elements:');
                    found.forEach((el, i) => {
                        console.log(`[${i}] ${el.tag} ph="${el.placeholder}" class="${el.class}" pos=(${el.x},${el.y}) ${el.w}x${el.h}`);
                        console.log(`    text="${el.text}"`);
                    });
                } catch(e) {
                    console.log('Parse error:', e.message);
                    console.log('Raw:', msg.result.result.value.substring(0, 500));
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
