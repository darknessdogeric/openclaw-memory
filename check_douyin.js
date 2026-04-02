const http = require('http');

const options = { hostname: '127.0.0.1', port: 9222, path: '/json', method: 'GET' };
const req = http.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => data += chunk);
    res.on('end', () => {
        const tabs = JSON.parse(data);
        console.log('总标签页:', tabs.length);
        tabs.forEach((t, i) => {
            console.log(`[${i+1}] ${t.title}`);
            console.log(`     ${t.url}`);
        });
    });
});
req.on('error', (e) => console.log('Error:', e.message));
req.setTimeout(5000, () => { req.destroy(); console.log('Timeout'); });
req.end();
