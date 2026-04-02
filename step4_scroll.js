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
      // Scroll to bottom
      conn.send(JSON.stringify({id:1, method:'Runtime.evaluate', params:{expression:"window.scrollTo(0, document.body.scrollHeight)"}}));
    });

    conn.on('message', function(raw) {
      var msg = JSON.parse(raw.toString());
      if (msg.id === 1) {
        console.log('Scrolled');
        setTimeout(function() {
          conn.send(JSON.stringify({id:2, method:'Page.captureScreenshot', params:{format:'png'}}));
        }, 1500);
      } else if (msg.id === 2 && msg.result && msg.result.data) {
        fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_bottom.png', Buffer.from(msg.result.data, 'base64'));
        console.log('Screenshot saved!');
        // Find publish button
        conn.send(JSON.stringify({id:3, method:'Runtime.evaluate', params:{expression:"(function(){var btns=document.querySelectorAll('button, div[role='button']');var result=[];for(var i=0;i<btns.length;i++){var t=(btns[i].innerText||'').trim();if(t.length>0&&t.length<20&&btns[i].getBoundingClientRect().width>0){result.push(t+'|'+(btns[i].getBoundingClientRect().y));}}return JSON.stringify(result.slice(0,20));})()"}}));
      } else if (msg.id === 3) {
        console.log('Buttons found:', msg.result && msg.result.result ? msg.result.result.value : 'n/a');
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
