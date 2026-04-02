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

        ws.on('open', () => {
            console.log('Step 1: Filling title...');
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
                                    inp.value = ${JSON.stringify(TITLE)};
                                    inp.dispatchEvent(new Event('input', {bubbles:true}));
                                    inp.dispatchEvent(new Event('change', {bubbles:true}));
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
                console.log('Title result:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                console.log('Step 2: Filling content in editor div...');
                ws.send(JSON.stringify({
                    id: 2,
                    method: 'Runtime.evaluate',
                    params: {
                        expression: `
                            (function() {
                                const editor = document.querySelector('div.editor-comp-publish');
                                if (editor) {
                                    editor.focus();
                                    // Type content line by line
                                    const text = ${JSON.stringify(CONTENT)};
                                    document.execCommand('insertText', false, text);
                                    return 'CONTENT_OK: ' + text.length + ' chars';
                                }
                                return 'EDITOR_NOT_FOUND';
                            })()
                        `
                    }
                }));
            } else if (msgId === 2) {
                console.log('Content result:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                console.log('Step 3: Filling hashtags...');
                ws.send(JSON.stringify({
                    id: 3,
                    method: 'Runtime.evaluate',
                    params: {
                        expression: `
                            (function() {
                                // Try to find hashtag input - look for inputs with # in placeholder or near topic text
                                const all = document.querySelectorAll('input');
                                for (const inp of all) {
                                    const ph = inp.getAttribute('placeholder') || '';
                                    if (ph.includes('#') || ph.includes('话题')) {
                                        inp.focus();
                                        inp.value = ${JSON.stringify(HASHTAGS)};
                                        inp.dispatchEvent(new Event('input', {bubbles:true}));
                                        inp.dispatchEvent(new Event('change', {bubbles:true}));
                                        return 'TAG_OK';
                                    }
                                }
                                // Alternative: use execCommand after hashtags keyword
                                const editor = document.querySelector('div.editor-comp-publish');
                                if (editor) {
                                    editor.focus();
                                    document.execCommand('insertText', false, '\\n${HASHTAGS}');
                                    return 'TAG_VIA_EDITOR';
                                }
                                return 'TAG_NOT_FOUND';
                            })()
                        `
                    }
                }));
            } else if (msgId === 3) {
                console.log('Hashtag result:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                console.log('Step 4: Screenshot...');
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
