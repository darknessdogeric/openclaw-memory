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
      // Scroll to bottom first
      conn.send(JSON.stringify({id:1, method:'Runtime.evaluate', params:{expression:"window.scrollTo(0, document.body.scrollHeight)"}}));
    });

    conn.on('message', function(raw) {
      var msg = JSON.parse(raw.toString());
      if (msg.id === 1) {
        setTimeout(function() {
          // Find and click the red publish button
          conn.send(JSON.stringify({id:2, method:'Runtime.evaluate', params:{expression:"(function(){var els=document.querySelectorAll('button, div');for(var i=0;i<els.length;i++){var t=(els[i].innerText||'').trim();if(t==='发布'&&els[i].getBoundingClientRect().width>0){els[i].click();return 'PUBLISH_CLICKED';}}return 'NOT_FOUND';})()"}}));
        }, 500);
      } else if (msg.id === 2) {
        console.log('Publish click:', msg.result && msg.result.result ? msg.result.result.value : 'n/a');
        setTimeout(function() {
          conn.send(JSON.stringify({id:3, method:'Page.captureScreenshot', params:{format:'png'}}));
        }, 2000);
      } else if (msg.id === 3 && msg.result && msg.result.data) {
        fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_publish_result.png', Buffer.from(msg.result.data, 'base64'));
        console.log('Result screenshot saved!');
        conn.close();
        process.exit(0);
      }
    });

    conn.on('error', function(e) { console.log('Err:', e.message); process.exit(1); });
    setTimeout(function() { conn.close(); process.exit(0); }, 20000);
  });
});
req.on('error', function(e) { console.log('HTTP Err:', e.message); process.exit(1); });
req.setTimeout(5000, function() { process.exit(1); });
req.end();
