var ws = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
var http = require('http');
var fs = require('fs');

var SNAP = 'C:\\Users\\ericz\\.openclaw\\workspace\\editor_nav.png';

var req = http.request({hostname:'127.0.0.1',port:9222,path:'/json',method:'GET'}, function(res) {
  var body = '';
  res.on('data', function(c) { body += c; });
  res.on('end', function() {
    var tabs = JSON.parse(body);
    console.log('Using tab:', tabs[0].title);
    var conn = new ws(tabs[0].webSocketDebuggerUrl);

    conn.on('open', function() {
      console.log('WS connected, navigating...');
      conn.send(JSON.stringify({id:1,method:'Page.navigate',params:{url:'https://creator.douyin.com/creator-micro/content/publish/picture-text'}}));
    });

    conn.on('message', function(raw) {
      var msg = JSON.parse(raw.toString());
      if (msg.id === 1) { console.log('Nav sent'); }
      if (msg.method === 'Page.loadEventFired') {
        console.log('Page loaded');
        setTimeout(function() {
          conn.send(JSON.stringify({id:2,method:'Page.captureScreenshot',params:{format:'png'}}));
        }, 4000);
      }
      if (msg.id === 2 && msg.result && msg.result.data) {
        fs.writeFileSync(SNAP, Buffer.from(msg.result.data,'base64'));
        console.log('Screenshot saved! Size:', msg.result.data.length);
        conn.close();
        process.exit(0);
      }
    });

    conn.on('error', function(e) { console.log('WS Err:', e.message); process.exit(1); });
    setTimeout(function() { conn.close(); process.exit(0); }, 25000);
  });
});
req.on('error', function(e) { console.log('HTTP Err:', e.message); process.exit(1); });
req.setTimeout(5000, function() { process.exit(1); });
req.end();
