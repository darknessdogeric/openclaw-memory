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

        ws.on('open', () => {
            // Step 1: Focus title input
            const focusExpr = `
                (function() {
                    var inputs = document.querySelectorAll('input.semi-input');
                    for (var i = 0; i < inputs.length; i++) {
                        if (inputs[i].getAttribute('placeholder') && inputs[i].getAttribute('placeholder').indexOf('标题') > -1) {
                            inputs[i].focus();
                            return 'TITLE_FOCUSED';
                        }
                    }
                    return 'TITLE_NOT_FOUND';
                })()
            `;
            ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression: focusExpr } }));
        });

        ws.on('message', (data) => {
            const msg = JSON.parse(data.toString());
            const msgId = msg.id;

            if (msgId === 1) {
                console.log('Focus:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                console.log('Step 2: Typing title...');
                // Build title typing expression
                let titleTyping = '';
                for (let i = 0; i < TITLE.length; i++) {
                    const ch = TITLE.charAt(i);
                    const chJson = JSON.stringify(ch);
                    titleTyping += `var inp = document.activeElement; if(inp && inp.tagName === 'INPUT'){ inp.value = inp.value + ${chJson}; inp.dispatchEvent(new Event('input',{bubbles:true})); inp.dispatchEvent(new Event('change',{bubbles:true})); inp.dispatchEvent(new KeyboardEvent('keyup',{bubbles:true,key:${chJson}}));}`;
                }
                ws.send(JSON.stringify({ id: 2, method: 'Runtime.evaluate', params: { expression: titleTyping } }));
            } else if (msgId === 2) {
                console.log('Title typed:', msg.result && msg.result.result ? msg.result.result.value.substring(0,50) : msg.result);
                console.log('Step 3: Typing hashtags...');
                const hashtagExpr = 'document.execCommand("insertText",false,"\\n' + HASHTAGS.replace(/#/g, '#') + '");"HASHTAG_TYPED"';
                ws.send(JSON.stringify({ id: 3, method: 'Runtime.evaluate', params: { expression: hashtagExpr } }));
            } else if (msgId === 3) {
                console.log('Hashtag result:', msg.result && msg.result.result ? msg.result.result.value : msg.result);
                console.log('Step 4: Screenshot...');
                setTimeout(() => {
                    ws.send(JSON.stringify({ id: 4, method: 'Page.captureScreenshot', params: { format: 'png' } }));
                }, 2000);
            } else if (msgId === 4 && msg.result && msg.result.data) {
                const buf = Buffer.from(msg.result.data, 'base64');
                fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_filled_final.png', buf);
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
