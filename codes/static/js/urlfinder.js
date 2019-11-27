let wsProto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
let sock = new WebSocket(wsProto + '//' + window.location.host + '/ws/urlfinder/');
sock.onclose = (e) => {console.error('socket closed');};
sock.onmessage = (e) => {
    console.log(e);
    let msg = JSON.parse(e.data);
    let logmsg = msg['log'];
    if (logmsg) {
        let logElem = document.getElementById('log');
        logElem.value += logmsg + '\n';
        logElem.scrollTop = logElem.scrollHeight;
    }
};
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('urlfinderform').onsubmit = (e) => {
        sock.send(JSON.stringify({'query': e.originalTarget[0].value}));
        e.preventDefault();
    };
}, false);
