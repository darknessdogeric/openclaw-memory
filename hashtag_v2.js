const WebSocket = require('ws');
const http = require('http');
const fs = require('fs');

const HASHTAGS = '#酒店创业 #民宿运营 #AI工具 #去中心化';
const SNAP = 'C:\\Users\\ericz\\.openclaw\\workspace\\douyin_snap.png';

const req = http.request({hostname:'127.0.0.1', port:9222, path:'/json', method:'GET'}, (res) => {
  let d = '';
  res.on('data', c => d += c);
  res.on('end', () => {
    const tabs = JSON.parse(d);
    const ws = new WebSocket(tabs[0].webSocketDebuggerUrl);

    ws.on('open', () => {
      // Click the hashtag button
      ws.send(JSON.stringify({id:1, method:'Runtime.evaluate', params:{expression:"(function(){var els=document.querySelectorAll('div');for(var i=0;i<els.length;i++){if(els[i].innerText.trim()==='#添加话题'&&els[i].getBoundingClientRect().width>0){els[i].click();return 'OK';}}return 'FAIL';})()"}}));
    });

    ws.on('message', (raw) => {
      const msg = JSON.parse(raw.toString());
      if (msg.id===1) { console.log('Click:', msg.result&&msg.result.result?msg.result.result.value:'n/a'); setTimeout(()=>ws.send(JSON.stringify({id:2,method:'Page.captureScreenshot',params:{format:'png'}})),1500); }
      else if (msg.id===2&&msg.result&&msg.result.data) {
        fs.writeFileSync(SNAP, Buffer.from(msg.result.data,'base64'));
        console.log('Snap1 done');
        ws.send(JSON.stringify({id:3,method:'Runtime.evaluate',params:{expression:"(function(){var ins=document.querySelectorAll('input');for(var i=0;i<ins.length;i++){var ph=ins[i].getAttribute('placeholder')||'';if(ph.indexOf('#')>-1){ins[i].focus();ins[i].value='"+HASHTAGS+"';ins[i].dispatchEvent(new Event('input',{bubbles:true}));return 'TAGGED:'+ins[i].value;}}return 'NO_TAG_INPUT';})()"}}));
      }
      else if (msg.id===3) { console.log('Tag result:', msg.result&&msg.result.result?msg.result.result.value:'n/a'); setTimeout(()=>ws.send(JSON.stringify({id:4,method:'Page.captureScreenshot',params:{format:'png'}})),1500); }
      else if (msg.id===4&&msg.result&&msg.result.data) {
        fs.writeFileSync(SNAP, Buffer.from(msg.result.data,'base64'));
        console.log('Snap2 done!');
        ws.close(); process.exit(0);
      }
    });

    ws.on('error', e => { console.log('Err:', e.message); process.exit(1); });
    setTimeout(() => { ws.close(); process.exit(0); }, 25000);
  });
});
req.on('error', e => { console.log('HTTP Err:', e.message); process.exit(1); });
req.setTimeout(5000, () => process.exit(1));
req.end();
