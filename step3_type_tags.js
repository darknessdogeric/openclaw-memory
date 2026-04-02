var ws = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
var http = require('http');
var fs = require('fs');

var TAG = '#酒店创业 #民宿运营 #AI工具 #去中心化';

var req = http.request({hostname:'127.0.0.1', port:9222, path:'/json', method:'GET'}, function(res) {
  var body = '';
  res.on('data', function(c) { body += c; });
  res.on('end', function() {
    var tabs = JSON.parse(body);
    var conn = new ws(tabs[0].webSocketDebuggerUrl);

    conn.on('open', function() {
      // Click on the hashtag input to focus it
      conn.send(JSON.stringify({id:1, method:'Runtime.evaluate', params:{expression:"(function(){var ins=document.querySelectorAll('input');for(var i=0;i<ins.length;i++){var ph=(ins[i].getAttribute('placeholder')||'').toLowerCase();if(ph.indexOf('#')>-1){ins[i].click();return 'CLICKED';}}return 'NOT_FOUND';})()"}}));
    });

    conn.on('message', function(raw) {
      var msg = JSON.parse(raw.toString());
      if (msg.id === 1) {
        console.log('Focus:', msg.result && msg.result.result ? msg.result.result.value : 'n/a');
        // Ctrl+A to select all
        setTimeout(function() {
          conn.send(JSON.stringify({id:2, method:'Input.dispatchKeyEvent', params:{type:'keyDown', modifiers:2, text:'', key:'a', keyCode:65}}));
        }, 300);
      } else if (msg.id === 2) {
        conn.send(JSON.stringify({id:3, method:'Input.dispatchKeyEvent', params:{type:'keyUp', modifiers:2, text:'', key:'a', keyCode:65}}));
      } else if (msg.id === 3) {
        // Type new tags - use execCommand to replace
        var expr = "(function(){document.execCommand('insertText',false,'" + TAG + "');return 'TAGGED';})()";
        conn.send(JSON.stringify({id:4, method:'Runtime.evaluate', params:{expression:expr}}));
      } else if (msg.id === 4) {
        console.log('Type result:', msg.result && msg.result.result ? msg.result.result.value : 'n/a');
        // Press Enter to confirm selection
        setTimeout(function() {
          conn.send(JSON.stringify({id:5, method:'Input.dispatchKeyEvent', params:{type:'keyDown', text:'', key:'Enter', keyCode:13}}));
        }, 500);
      } else if (msg.id === 5) {
        conn.send(JSON.stringify({id:6, method:'Input.dispatchKeyEvent', params:{type:'keyUp', text:'', key:'Enter', keyCode:13}}));
      } else if (msg.id === 6) {
        // Take screenshot
        setTimeout(function() {
          conn.send(JSON.stringify({id:7, method:'Page.captureScreenshot', params:{format:'png'}}));
        }, 2000);
      } else if (msg.id === 7 && msg.result && msg.result.data) {
        fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_snap3.png', Buffer.from(msg.result.data, 'base64'));
        console.log('Done!');
        conn.close();
        process.exit(0);
      }
    });

    conn.on('error', function(e) { console.log('Err:', e.message); process.exit(1); });
    setTimeout(function() { conn.close(); process.exit(0); }, 25000);
  });
});
req.on('error', function(e) { console.log('HTTP Err:', e.message); process.exit(1); });
req.setTimeout(5000, function() { process.exit(1); });
req.end();
