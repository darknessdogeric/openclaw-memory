var ws = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
var http = require('http');
var fs = require('fs');

var req = http.request({hostname:'127.0.0.1', port:9222, path:'/json', method:'GET'}, function(res) {
  var body = '';
  res.on('data', function(c) { body += c; });
  res.on('end', function() {
    var tabs = JSON.parse(body);
    var conn = new ws(tabs[0].webSocketDebuggerUrl);
    conn.on('open', function() {
      // Scroll to top
      conn.send(JSON.stringify({id:1,method:'Runtime.evaluate',params:{expression:"window.scrollTo(0,0)"}}));
    });
    conn.on('message', function(raw) {
      var msg = JSON.parse(raw.toString());
      if (msg.id===1) {
        setTimeout(function() {
          conn.send(JSON.stringify({id:2,method:'Page.captureScreenshot',params:{format:'png'}}));
        }, 1000);
      } else if (msg.id===2&&msg.result&&msg.result.data) {
        fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_editor_top.png', Buffer.from(msg.result.data,'base64'));
        console.log('OK');
        conn.close(); process.exit(0);
      }
    });
    conn.on('error', function(e) { process.exit(1); });
    setTimeout(function() { conn.close(); process.exit(0); }, 15000);
  });
});
req.on('error', function(e) { process.exit(1); });
req.setTimeout(5000, function() { process.exit(1); });
req.end();
