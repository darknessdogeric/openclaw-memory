var ws = require('C:\\Users\\ericz\\AppData\\Roaming\\npm\\node_modules\\ws');
var http = require('http');
var fs = require('fs');

var TITLE = '酒店老板都在转发的救命神器';
var CONTENT = '酒店被OTA抽成15-25%，一年白干。现在有了新解法：\n\n✅ 7×24小时AI管家\n✅ 告别15%平台佣金，只收2%技术服务费\n✅ 单体酒店也有自己的数字化运营团队\n\n100间房的酒店，每年省下10万+。\n\n这不是未来，这是现在正在发生的事。';
var TAGS = '#酒店创业 #民宿运营 #AI工具 #去中心化';

var req = http.request({hostname:'127.0.0.1', port:9222, path:'/json', method:'GET'}, function(res) {
  var body = '';
  res.on('data', function(c) { body += c; });
  res.on('end', function() {
    var tabs = JSON.parse(body);
    console.log('Tab:', tabs[0].title, tabs[0].url);
    var conn = new ws(tabs[0].webSocketDebuggerUrl);
    var step = 0;

    function nextStep() {
      step++;
      if (step === 1) {
        // Step 1: Navigate to editor
        console.log('[1] Navigating to editor...');
        conn.send(JSON.stringify({id:1,method:'Page.navigate',params:{url:'https://creator.douyin.com/creator-micro/content/publish/picture-text'}}));
      } else if (step === 2) {
        setTimeout(function() {
          conn.send(JSON.stringify({id:2,method:'Page.captureScreenshot',params:{format:'png'}}));
        }, 4000);
      } else if (step === 2) {
        // Wait for nav
      } else if (step === 3) {
        // Fill title
        console.log('[3] Filling title...');
        var titleExpr = '';
        for (var i=0; i<TITLE.length; i++) {
          var ch = TITLE.charAt(i);
          titleExpr += '{var inp=document.activeElement;if(inp&&inp.tagName==="INPUT"){inp.value=inp.value+"'+ch.replace(/\\/g,'\\\\').replace(/"/g,'\\"')+'";inp.dispatchEvent(new Event("input",{bubbles:true}));}}';
        }
        conn.send(JSON.stringify({id:3,method:'Runtime.evaluate',params:{expression:"(function(){var ins=document.querySelectorAll('input.semi-input');for(var i=0;i<ins.length;i++){if(ins[i].getAttribute('placeholder')&&ins[i].getAttribute('placeholder').indexOf('标题')>-1){ins[i].focus();return 'TITLE_FOCUSED';}}return 'NOT_FOUND';})()"}}));
      } else if (step === 4) {
        // Focus title input
        var titleExpr = '';
        for (var i=0; i<TITLE.length; i++) {
          var ch = TITLE.charAt(i);
          titleExpr += '{var inp=document.activeElement;if(inp&&inp.tagName==="INPUT"){inp.value=inp.value+"'+ch.replace(/\\/g,'\\\\').replace(/"/g,'\\"')+'";inp.dispatchEvent(new Event("input",{bubbles:true}));}}';
        }
        var fullExpr = '(function(){var ins=document.querySelectorAll("input.semi-input");for(var i=0;i<ins.length;i++){if(ins[i].getAttribute("placeholder")&&ins[i].getAttribute("placeholder").indexOf("标题")>-1){ins[i].focus();'+titleExpr+'ins[i].dispatchEvent(new Event("change",{bubbles:true}));return "TITLE_DONE";}}return "NOT_FOUND";})()';
        conn.send(JSON.stringify({id:4,method:'Runtime.evaluate',params:{expression:fullExpr}}));
      } else if (step === 5) {
        console.log('[5] Title result:', msg.result&&msg.result.result?msg.result.result.value:'n/a');
        console.log('[5] Filling content...');
        // Fill content in editor div
        var contentExpr = CONTENT.split('\n').map(function(line) {
          if (line === '') return '';
          return 'document.execCommand('insertText',false,"'+line+'");document.execCommand('insertLineBreak',false);';
        }).join('');
        var fullContent = '(function(){var editor=document.querySelector("div.editor-comp-publish");if(editor){editor.focus();'+contentExpr+';return "CONTENT_OK";}return "NOT_FOUND";})()';
        conn.send(JSON.stringify({id:5,method:'Runtime.evaluate',params:{expression:fullContent}}));
      } else if (step === 6) {
        console.log('[6] Content result:', msg.result&&msg.result.result?msg.result.result.value:'n/a');
        // Click hashtag button
        console.log('[6] Clicking hashtag button...');
        conn.send(JSON.stringify({id:6,method:'Runtime.evaluate',params:{expression:"(function(){var els=document.querySelectorAll('div');for(var i=0;i<els.length;i++){if((els[i].innerText||'').trim()==='#添加话题'&&els[i].getBoundingClientRect().width>0){els[i].click();return 'CLICKED';}}return 'NOT_FOUND';})()"}}));
      } else if (step === 7) {
        console.log('[7] Hashtag click:', msg.result&&msg.result.result?msg.result.result.value:'n/a');
        setTimeout(function() { conn.send(JSON.stringify({id:7,method:'Page.captureScreenshot',params:{format:'png'}}); }, 2000);
      } else if (step === 8) {
        console.log('[8] Taking screenshot...');
      } else if (step === 9) {
        console.log('[9] Done!', msg.result&&msg.result.data?'screenshot saved':'no data');
        conn.close();
        process.exit(0);
      }
    }

    conn.on('message', function(raw) {
      var msg = JSON.parse(raw.toString());
      if (msg.method === 'Page.loadEventFired') {
        step = 1;
        setTimeout(function() { nextStep(); }, 3000);
      } else if (msg.id === 1) {
        console.log('[1] Nav result:', msg.result);
        setTimeout(function() { nextStep(); }, 5000);
      } else if (msg.id === 2 && msg.result && msg.result.data) {
        fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\fill_step1.png', Buffer.from(msg.result.data,'base64'));
        console.log('[2] Editor loaded, screenshot saved');
        // Scroll to top
        conn.send(JSON.stringify({id:3,method:'Runtime.evaluate',params:{expression:"window.scrollTo(0,0)"}}));
      } else if (msg.id === 3) {
        setTimeout(function() {
          // Focus and type title
          conn.send(JSON.stringify({id:4,method:'Runtime.evaluate',params:{expression:"(function(){var ins=document.querySelectorAll('input.semi-input');for(var i=0;i<ins.length;i++){if(ins[i].getAttribute('placeholder')&&ins[i].getAttribute('placeholder').indexOf('标题')>-1){ins[i].focus();return 'FOCUSED';}}return 'NOT_FOUND';})()"}}));
        }, 1000);
      } else if (msg.id === 4) {
        console.log('[4] Focus:', msg.result&&msg.result.result?msg.result.result.value:'n/a');
        // Type title using keyboard events
        var ch = TITLE.charAt(0);
        conn.send(JSON.stringify({id:5,method:'Input.dispatchKeyEvent',params:{type:'keyDown',text:ch,key:ch,keyCode:ch.charCodeAt(0)}}));
      } else if (msg.id === 5) {
        var ch = TITLE.charAt(0);
        conn.send(JSON.stringify({id:6,method:'Input.dispatchKeyEvent',params:{type:'keyUp',text:ch,key:ch,keyCode:ch.charCodeAt(0)}}));
      } else if (msg.id === 6) {
        // Type remaining characters
        var remaining = TITLE.substring(1);
        var expr = '';
        for (var i=0; i<remaining.length; i++) {
          var ch2 = remaining.charAt(i);
          expr += '{var inp=document.activeElement;if(inp&&inp.tagName==="INPUT"){inp.value=inp.value+"'+ch2.replace(/\\/g,'\\\\').replace(/"/g,'\\"')+'";inp.dispatchEvent(new Event("input",{bubbles:true}));}';
        }
        conn.send(JSON.stringify({id:7,method:'Runtime.evaluate',params:{expression:'(function(){'+expr+'return "TITLE_TYPED";})()'}}));
      } else if (msg.id === 7) {
        console.log('[7] Title typed:', msg.result&&msg.result.result?msg.result.result.value:'n/a');
        // Tab to content field
        conn.send(JSON.stringify({id:8,method:'Input.dispatchKeyEvent',params:{type:'keyDown',text:'',key:'Tab',keyCode:9}}));
      } else if (msg.id === 8) {
        conn.send(JSON.stringify({id:9,method:'Input.dispatchKeyEvent',params:{type:'keyUp',text:'',key:'Tab',keyCode:9}}));
      } else if (msg.id === 9) {
        // Type content
        var lines = CONTENT.split('\n');
        var contentExpr = '';
        for (var li=0; li<lines.length; li++) {
          if (lines[li] === '') {
            contentExpr += 'document.execCommand(\'insertLineBreak\',false);';
          } else {
            contentExpr += 'document.execCommand(\'insertText\',false,"'+lines[li].replace(/\\/g,'\\\\').replace(/"/g,'\\"')+'");document.execCommand(\'insertLineBreak\',false);';
          }
        }
        conn.send(JSON.stringify({id:10,method:'Runtime.evaluate',params:{expression:'(function(){try{'+contentExpr+';return "CONTENT_OK";}catch(e){return "ERR:"+e.message;}})()'}}));
      } else if (msg.id === 10) {
        console.log('[10] Content:', msg.result&&msg.result.result?msg.result.result.value:'n/a');
        // Click hashtag
        conn.send(JSON.stringify({id:11,method:'Runtime.evaluate',params:{expression:"(function(){var els=document.querySelectorAll('div');for(var i=0;i<els.length;i++){if((els[i].innerText||'').trim()==='#添加话题'&&els[i].getBoundingClientRect().width>0){els[i].click();return 'CLICKED';}}return 'NOT_FOUND';})()"}}));
      } else if (msg.id === 11) {
        console.log('[11] Hashtag click:', msg.result&&msg.result.result?msg.result.result.value:'n/a');
        setTimeout(function() {
          conn.send(JSON.stringify({id:12,method:'Runtime.evaluate',params:{expression:"document.execCommand('insertText',false,'"+TAGS+"');'CONTENT_TAGGED';"}}));
        }, 1000);
      } else if (msg.id === 12) {
        console.log('[12] Tags:', msg.result&&msg.result.result?msg.result.result.value:'n/a');
        setTimeout(function() {
          conn.send(JSON.stringify({id:13,method:'Page.captureScreenshot',params:{format:'png'}}));
        }, 2000);
      } else if (msg.id === 13 && msg.result && msg.result.data) {
        fs.writeFileSync('C:\\Users\\ericz\\.openclaw\\workspace\\fill_done.png', Buffer.from(msg.result.data,'base64'));
        console.log('[13] DONE! Screenshot saved');
        conn.close();
        process.exit(0);
      }
    });

    conn.on('error', function(e) { console.log('Err:', e.message); process.exit(1); });
    setTimeout(function() { console.log('Timeout at step', step); conn.close(); process.exit(0); }, 60000);
  });
});
req.on('error', function(e) { console.log('HTTP Err:', e.message); process.exit(1); });
req.setTimeout(5000, function() { process.exit(1); });
req.end();
