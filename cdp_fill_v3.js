const WebSocket = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
const http = require('http');
const fs = require('fs');

const TITLE = '酒店老板都在转发的救命神器';
const HASHTAGS = '#酒店创业 #民宿运营 #AI工具 #去中心化';

const req = http.request({ hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' }, (res) => {
    let data = '';
    res.on('data', (c) => data += c);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        const target = tabs[0];
        console.log('Tab:', target.title);

        const ws = new WebSocket(target.webSocketDebuggerUrl);
        let step = 0;

        function typeText(text) {
            // Use Input.dispatchEvent with keydown/keypress/keyup for each character
            let expressions = [];
            for (const ch of text) {
                if (ch === '\n') {
                    expressions.push(`document.execCommand('insertLineBreak', false)`);
                } else {
                    const key = ch === ' ' ? 'Space' : (ch.match(/[a-zA-Z0-9]/) ? ch.toUpperCase() : ch);
                    expressions.push(`
                        (function() {
                            const ev = new KeyboardEvent('keydown', {bubbles:true, cancelable:true, key:'${key}', code:'${key === ' ' ? 'Space' : 'Key' + key}'});
                            arguments[0].dispatchEvent(ev);
                            arguments[0].value = arguments[0].value + '${ch}';
                            const ev2 = new KeyboardEvent('input', {bubbles:true, cancelable:true, inputType:'insertText', data:'${ch}'});
                            arguments[0].dispatchEvent(ev2);
                            const ev3 = new KeyboardEvent('keyup', {bubbles:true, cancelable:true, key:'${key}', code:'${key === ' ' ? 'Space' : 'Key' + key}'});
                            arguments[0].dispatchEvent(ev3);
                        })(arguments[0])
                    `);
                }
            }
            return expressions.join(';');
        }

        ws.on('open', () => {
            console.log('WS connected, Step 1: Click title input...');
            ws.send(JSON.stringify({
                id: 1,
                method: 'Runtime.evaluate',
                params: {
                    expression: `
                        (function() {
                            const inputs = document.querySelectorAll('input.semi-input');
                            for (const inp of inputs) {
                                const ph = inp.getAttribute('placeholder') || '';
                                if (ph.includes('标题')) {
                                    inp.focus();
                                    inp.click();
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
                console.log('Click result:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                console.log('Step 2: Type title...');
                ws.send(JSON.stringify({
                    id: 2,
                    method: 'Runtime.evaluate',
                    params: {
                        expression: `
                            (function() {
                                const inputs = document.querySelectorAll('input.semi-input');
                                for (const inp of inputs) {
                                    const ph = inp.getAttribute('placeholder') || '';
                                    if (ph.includes('标题')) {
                                        inp.focus();
                                        return 'READY';
                                    }
                                }
                                return 'NOT_FOUND';
                            })()
                        `
                    }
                }));
            } else if (msgId === 2) {
                console.log('Ready for typing');
                // Type title using keyboard
                const titleExpr = typeText(TITLE);
                ws.send(JSON.stringify({
                    id: 3,
                    method: 'Runtime.evaluate',
                    params: {
                        expression: `
                            (function() {
                                const inputs = document.querySelectorAll('input.semi-input');
                                for (const inp of inputs) {
                                    const ph = inp.getAttribute('placeholder') || '';
                                    if (ph.includes('标题')) {
                                        inp.focus();
                                        ${titleExpr}
                                        inp.dispatchEvent(new Event('change', {bubbles:true}));
                                        return 'TITLE_TYPED:' + inp.value;
                                    }
                                }
                                return 'NOT_FOUND';
                            })()
                        `
                    }
                }));
            } else if (msgId === 3) {
                console.log('Title typed:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                console.log('Step 3: Type hashtags (Tab to next field)...');
                // Tab to hashtag field and type
                ws.send(JSON.stringify({
                    id: 4,
                    method: 'Runtime.evaluate',
                    params: {
                        expression: `
                            (function() {
                                // Find hashtag input (look for placeholder containing # or 话题)
                                const all = document.querySelectorAll('input, textarea, [contenteditable]');
                                for (const el of all) {
                                    const ph = el.getAttribute('placeholder') || '';
                                    const style = window.getComputedStyle(el);
                                    if ((ph.includes('话题') || ph.includes('#')) && style.display !== 'none' && style.visibility !== 'hidden') {
                                        el.focus();
                                        return 'HASHTAG_READY:' + ph;
                                    }
                                }
                                // Fallback: Tab from current position
                                document.execCommand('insertText', false, '\\n${HASHTAGS}');
                                return 'HASHTAG_VIA_TAB';
                            })()
                        `
                    }
                }));
            } else if (msgId === 4) {
                console.log('Hashtag result:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                console.log('Step 4: Screenshot...');
                setTimeout(() => {
                    ws.send(JSON.stringify({ id: 5, method: 'Page.captureScreenshot', params: { format: 'png' } }));
                }, 2000);
            } else if (msgId === 5 && msg.result && msg.result.data) {
                const buf = Buffer.from(msg.result.data, 'base64');
                fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_filled_v3.png', buf);
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
