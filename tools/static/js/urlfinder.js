let wsProto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
let sock = new WebSocket(wsProto + '//' + window.location.host + '/ws/urlfinder/');
let runningQueries = [];
sock.onclose = (e) => {console.error('socket closed');};
function appendResult(query, site, url) {
    let resultRow = document.createElement('tr');
    let queryCol = document.createElement('td');
    queryCol.innerText = query || '-';
    resultRow.appendChild(queryCol);
    let siteCol = document.createElement('td');
    siteCol.innerText = site || '-';
    resultRow.appendChild(siteCol);
    let urlCol = document.createElement('td');
    let urlLink = document.createElement('a');
    if (url)
        urlLink.href = url;
    urlLink.innerText = url || '-';
    urlCol.appendChild(urlLink);
    resultRow.appendChild(urlCol);
    document.getElementById('results').appendChild(resultRow);
}
sock.onmessage = (e) => {
    let msg = JSON.parse(e.data);
    if (msg.log) {
        let logElem = document.getElementById('log');
        logElem.value += msg.log + '\n';
        logElem.scrollTop = logElem.scrollHeight;
    }
    if (msg.result) {
        appendResult(msg.result.query, msg.result.label, msg.result.url)
    }
    if (msg.control) {
        if (msg.control.code === 'nothing') {
            appendResult(msg.control.query, 'nothing found');
        } else if (msg.control.code === 'done') {
            let queryIndex = runningQueries.indexOf(msg.control.query);
            if (queryIndex < 0) {
                alert('weird bug: old query completed how do i fix pls help');
            } else {
                runningQueries.splice(queryIndex, 1);
                if (runningQueries.length === 0) {
                    document.getElementById('results-loading').style.visibility = 'hidden';
                }
            }
        }
    }
};
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('toggle-log').onclick = (e) => {
        logElem = document.getElementById('log');
        if (window.getComputedStyle(logElem).visibility === 'hidden') {
            logElem.style.visibility = 'visible';
            e.target.innerText = 'Hide Log'
        } else {
            logElem.style.visibility = 'hidden';
            e.target.innerText = 'Show Log'
        }
    };
    document.getElementById('urlfinderform').onsubmit = (e) => {
        let query = e.target[0].value;
        runningQueries.push(query);
        sock.send(JSON.stringify({'query': query}));
        document.getElementById('results-loading').style.visibility = 'visible';
        e.preventDefault();
    };
}, false);
