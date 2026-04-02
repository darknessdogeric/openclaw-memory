var ws = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
var http = require('http');
var fs = require('fs');

var HASHTAGS = '#酒店创业 #民宿运营 #AI工具 #去中心化';
var SNAP = 'C:\\Users\\ericz\\.openclaw\\workspace\\douyin_snap.png';

var req = http.request({hostname:'127.0.0.1', port:9222, path:'/json', method:'GET'}, function(res) {
  var body = '';
  res.on('data', function(c) { body += c; });
  res.on('end', function() {
    var tabs = JSON.parse(body);
    var wsUrl = tabs[0].webSocketDebuggerUrl;
    var conn = new ws(wsUrl);

    conn.on('open', function() {
      console.log('Connected, clicking hashtag...');
      conn.send(JSON.stringify({id:1, method:'Runtime.evaluate', params:{expression:"(function(){var els=document.querySelectorAll('div');for(var i=0;i<els.length;i++){var t=(els[i].innerText||'').trim();if(t==='#添加话题'){els[i].click();return 'OK';}}return 'FAIL';})()"}}));
    });

    conn.on('message', function(raw) {
      var msg = JSON.parse(raw.toString());
      if (msg.id === 1) {
        console.log('Click result:', msg.result && msg.result.result ? msg.result.result.value : 'n/a');
        setTimeout(function() {
          conn.send(JSON.stringify({id:2, method:'Page.captureScreenshot', params:{format:'png'}}));
        }, 1500);
      } else if (msg.id === 2 && msg.result && msg.result.data) {
        fs.writeFileSync(SNAP, Buffer.from(msg.result.data, 'base64'));
        console.log('Snap1 saved');
        // Try to type in hashtag input
        conn.send(JSON.stringify({id:3, method:'Runtime.evaluate', params:{expression:"(function(){var ins=document.querySelectorAll('input');for(var i=0;i<ins.length;i++){var ph=(ins[i].getAttribute('placeholder')||'').toLowerCase();if(ph.indexOf('#')>-1||ph.indexOf('话题')>-1){ins[i].focus();return 'FOUND:'+ph;}}return 'NOT_FOUND';})()"}}));
      } else if (msg.id === 3) {
        console.log('Tag field:', msg.result && msg.result.result ? msg.result.result.value : 'n/a');
        setTimeout(function() {
          conn.send(JSON.stringify({id:4, method:'Page.captureScreenshot', params:{format:'png'}}));
        }, 1500);
      } else if (msg.id === 4 && msg.result && msg.result.data) {
        fs.writeFileSync(SNAP, Buffer.from(msg.result.data, 'base64'));
        console.log('Snap2 saved! Done.');
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
