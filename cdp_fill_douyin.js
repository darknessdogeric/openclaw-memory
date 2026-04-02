const WebSocket = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
const http = require('http');
const fs = require('fs');

const TITLE = '酒店老板都在转发的救命神器';
const CONTENT = `酒店被OTA抽成15-25%，一年白干。现在有了新解法：

✅ 7×24小时AI管家
✅ 告别15%平台佣金，只收2%技术服务费
✅ 单体酒店也有自己的数字化运营团队

100间房的酒店，每年省下10万+。

这不是未来，这是现在正在发生的事。`;

const HASHTAGS = '#酒店创业 #民宿运营 #AI工具 #去中心化';

const req = http.request({ hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' }, (res) => {
    let data = '';
    res.on('data', (c) => data += c);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        const target = tabs[0];
        console.log('Tab:', target.title);

        const ws = new WebSocket(target.webSocketDebuggerUrl);
        let currentStep = 0;

        ws.on('open', () => {
            console.log('WS connected, Step 1: filling title...');
            ws.send(JSON.stringify({
                id: 1,
                method: 'Runtime.evaluate',
                params: {
                    expression: `
                        (function() {
                            const all = document.querySelectorAll('input, textarea, [contenteditable="true"]');
                            for (const el of all) {
                                const ph = el.placeholder || '';
                                const txt = el.innerText || '';
                                if (ph.includes('标题') || txt.includes('填写作品标题')) {
                                    el.focus();
                                    el.innerText = ${JSON.stringify(TITLE)};
                                    el.dispatchEvent(new Event('input', {bubbles:true}));
                                    el.dispatchEvent(new Event('change', {bubbles:true}));
                                    return 'TITLE_OK';
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
                console.log('Step 1 result:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                console.log('Step 2: filling content...');
                ws.send(JSON.stringify({
                    id: 2,
                    method: 'Runtime.evaluate',
                    params: {
                        expression: `
                            (function() {
                                const all = document.querySelectorAll('input, textarea, [contenteditable="true"]');
                                for (const el of all) {
                                    const ph = el.placeholder || '';
                                    if (ph.includes('简介') || ph.includes('添加作品简介')) {
                                        el.focus();
                                        el.innerText = ${JSON.stringify(CONTENT)};
                                        el.dispatchEvent(new Event('input', {bubbles:true}));
                                        el.dispatchEvent(new Event('change', {bubbles:true}));
                                        return 'CONTENT_OK';
                                    }
                                }
                                return 'CONTENT_NOT_FOUND';
                            })()
                        `
                    }
                }));
            } else if (msgId === 2) {
                console.log('Step 2 result:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                console.log('Step 3: filling hashtags...');
                ws.send(JSON.stringify({
                    id: 3,
                    method: 'Runtime.evaluate',
                    params: {
                        expression: `
                            (function() {
                                const all = document.querySelectorAll('input, textarea, [contenteditable="true"]');
                                for (const el of all) {
                                    const ph = el.placeholder || '';
                                    if (ph.includes('话题') || ph.includes('#')) {
                                        el.focus();
                                        el.innerText = ${JSON.stringify(HASHTAGS)};
                                        el.dispatchEvent(new Event('input', {bubbles:true}));
                                        el.dispatchEvent(new Event('change', {bubbles:true}));
                                        return 'TAG_OK';
                                    }
                                }
                                return 'TAG_NOT_FOUND';
                            })()
                        `
                    }
                }));
            } else if (msgId === 3) {
                console.log('Step 3 result:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                console.log('Step 4: taking screenshot...');
                setTimeout(() => {
                    ws.send(JSON.stringify({ id: 4, method: 'Page.captureScreenshot', params: { format: 'png' } }));
                }, 2000);
            } else if (msgId === 4 && msg.result && msg.result.data) {
                const buf = Buffer.from(msg.result.data, 'base64');
                fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_filled.png', buf);
                console.log('Screenshot saved! Size:', buf.length);
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
