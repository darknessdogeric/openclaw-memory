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
      // Select all text in hashtag input and replace
      conn.send(JSON.stringify({id:1, method:'Runtime.evaluate', params:{expression:"(function(){var ins=document.querySelectorAll('input');for(var i=0;i<ins.length;i++){var ph=(ins[i].getAttribute('placeholder')||'').toLowerCase();if(ph.indexOf('#')>-1){ins[i].focus();ins[i].select();return 'SELECTED';}}return 'NOT_FOUND';})()"}}));
    });

    conn.on('message', function(raw) {
      var msg = JSON.parse(raw.toString());
      if (msg.id === 1) {
        console.log('Select result:', msg.result && msg.result.result ? msg.result.result.value : 'n/a');
        // Type the correct hashtags
        setTimeout(function() {
          conn.send(JSON.stringify({id:2, method:'Runtime.evaluate', params:{expression:"(function(){var ins=document.querySelectorAll('input');for(var i=0;i<ins.length;i++){var ph=(ins[i].getAttribute('placeholder')||'').toLowerCase();if(ph.indexOf('#')>-1){ins[i].focus();return 'READY';}}return 'NOT_FOUND';})()"}}));
        }, 500);
      } else if (msg.id === 2) {
        console.log('Ready for typing');
        // Use keyboard to type each character
        var tag = '#酒店创业 #民宿运营 #AI工具 #去中心化';
        var idx = 0;
        function typeNext() {
          if (idx < tag.length) {
            var ch = tag.charAt(idx);
            var keyCode = ch.charCodeAt(0);
            conn.send(JSON.stringify({id:10+idx, method:'Input.dispatchKeyEvent', params:{type:'keyDown', text:ch, key:ch, keyCode:keyCode}}));
          } else {
            // Done, press Enter to confirm
            setTimeout(function() {
              conn.send(JSON.stringify({id:99, method:'Input.dispatchKeyEvent', params:{type:'keyDown', text:'', key:'Enter', keyCode:13}}));
            }, 200);
          }
        }
        // Start typing
        var ch = tag.charAt(0);
        conn.send(JSON.stringify({id:10, method:'Input.dispatchKeyEvent', params:{type:'keyDown', text:ch, key:ch, keyCode:ch.charCodeAt(0)}}));
        // Also set value directly
        conn.send(JSON.stringify({id:11, method:'Runtime.evaluate', params:{expression:"(function(){var ins=document.querySelectorAll('input');for(var i=0;i<ins.length;i++){var ph=(ins[i].getAttribute('placeholder')||'').toLowerCase();if(ph.indexOf('#')>-1){ins[i].value='"+tag+"';ins[i].dispatchEvent(new Event('input',{bubbles:true}));return 'DONE:'+ins[i].value;}}return 'FAIL';})()"}}));
      } else if (msg.id === 11) {
        console.log('Value set:', msg.result && msg.result.result ? msg.result.result.value : 'n/a');
        setTimeout(function() { conn.send(JSON.stringify({id:12, method:'Page.captureScreenshot', params:{format:'png'}})); }, 1500);
      } else if (msg.id === 12 && msg.result && msg.result.data) {
        fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\douyin_snap2.png', Buffer.from(msg.result.data, 'base64'));
        console.log('Screenshot saved!');
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
