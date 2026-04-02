const WebSocket = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
const http = require('http');
const fs = require('fs');

const req = http.request({ hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' }, (res) => {
    let data = '';
    res.on('data', (c) => data += c);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        const target = tabs[0];
        console.log('Tab:', target.title);
        const ws = new WebSocket(target.webSocketDebuggerUrl);

        ws.on('open', () => {
            // List ALL inputs to find hashtag field
            ws.send(JSON.stringify({
                id: 1,
                method: 'Runtime.evaluate',
                params: {
                    expression: `
                        (function() {
                            var result = [];
                            var inputs = document.querySelectorAll('input');
                            inputs.forEach(function(inp, i) {
                                result.push({
                                    index: i,
                                    tag: 'INPUT',
                                    placeholder: inp.getAttribute('placeholder') || '',
                                    type: inp.type || '',
                                    value: (inp.value || '').substring(0, 20),
                                    display: window.getComputedStyle(inp).display,
                                    visible: window.getComputedStyle(inp).visibility !== 'hidden' && window.getComputedStyle(inp).display !== 'none'
                                });
                            });
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
                    try {
                        var inputs = JSON.parse(r);
                        inputs.filter(function(i) { return i.visible; }).forEach(function(i) {
                            console.log('INPUT ' + i.index + ' ph="' + i.placeholder + '" type="' + i.type + '" val="' + i.value + '"');
                        });
                    } catch(e) { console.log('parse error:', e.message); }
                }
                ws.close();
                process.exit(0);
            }
        });

        ws.on('error', function(e) { console.log('WS Error:', e.message); process.exit(1); });
        setTimeout(function() { ws.close(); process.exit(0); }, 10000);
    });
});
req.on('error', function(e) { console.log('Error:', e.message); process.exit(1); });
req.setTimeout(5000, function() { process.exit(1); });
req.end();
