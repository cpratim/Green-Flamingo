let leadersWrapper = document.getElementById('leaders-wrapper');
let socket = null;
let tickerData = null;
let userData = null;
let N = 0;

let base = window.location.toString();

if (base.substring(0, 5) === 'https') {
    socket = io.connect('https://' + document.domain + ':' + location.port);
} else {
    socket = io.connect('http://' + document.domain + ':' + location.port);
}

function loadLeaders(data) {
    leadersWrapper.innerHTML = '';
    let leaders = {};
    for (let username in data) {
        let balance = data[username].balance;
        let quantity = data[username].quantity;
        let total = balance;
        if (tickerData != null) {
            total += quantity * tickerData.last_trade_price;
        }
        leaders[username] = total;
    }
    leaders = Object.entries(leaders).sort((a, b) => b[1] - a[1]);
    let i = 1;
    for (let leader in leaders) {
        console.log(leaders[leader]);
        let leaderDiv = document.createElement('div');
        leaderDiv.className = 'leader';
        let total = leaders[leader][1];
        leaderDiv.innerHTML = `<div class="number">${i}</div><div class="name">${leaders[leader][0]}</div><div class="balance">$${total.toFixed(2)}</div>`;
        leadersWrapper.appendChild(leaderDiv);
        i++;
    }
}

function refresh_leaderboard() {
    fetch('/api/all_users', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'ngrok-skip-browser-warning': 'true',
            'Access-Control-Allow-Origin': '*'
        },
    }).then(response => {
        return response.json();
    }).then(data => {
        userData = data;
        console.log(userData);
        loadLeaders(data);
    });
}

socket.on('new_user', function(data) {
    userData = data;
    refresh_leaderboard();
});

socket.on('trade', function(data) {
    tickerData = data;
    if (N % 5 == 0){
        refresh_leaderboard();
    }
    N++;
    
});
