let switchViewButton = document.getElementById('switch-view-button');
let artView = document.getElementById('art-section-wrapper').innerHTML;
let tradingView = document.getElementById('trading-section-wrapper').innerHTML;
let currentView = 'trading';

let artViewDiv = document.getElementById('art-section-wrapper');
let tradingViewDiv = document.getElementById('trading-section-wrapper');
let container = document.getElementById('container');
let qouteText = document.getElementById('qoute');
let changeText = document.getElementById('change');

let bidsWrapper = document.getElementById('bids-wrapper');
let asksWrapper = document.getElementById('asks-wrapper');
let volumeText = document.getElementById('volume');

let tickerData = null;
let base = window.location.toString();

let socket = null;
if (base.substring(0, 5) === 'https') {
    socket = io.connect('https://' + document.domain + ':' + location.port);
} else {
    socket = io.connect('http://' + document.domain + ':' + location.port);
}

socket.on('connect', function() {
    console.log('Connected to server');
});


function loadBids(bids) {
    bidsWrapper.innerHTML = '';
    for (let i = 0; i < bids.length; i++) {
        let bid = bids[i];
        let bidDiv = document.createElement('div');
        bidDiv.className = 'bid';
        bidDiv.innerHTML = `${bid[0]} (${bid[1]})`;
        bidsWrapper.appendChild(bidDiv);
    }
}

function loadAsks(asks) {
    asksWrapper.innerHTML = '';
    for (let i = 0; i < asks.length; i++) {
        let ask = asks[i];
        let askDiv = document.createElement('div');
        askDiv.className = 'ask';
        askDiv.innerHTML = `${ask[0]} (${ask[1]})`;
        asksWrapper.appendChild(askDiv);
    }
}

function refresh(data) {
    container = document.getElementById('container');
    qouteText = document.getElementById('qoute');
    changeText = document.getElementById('change');
    volumeText = document.getElementById('volume');
    bidsWrapper = document.getElementById('bids-wrapper');
    asksWrapper = document.getElementById('asks-wrapper');

    let last_trade_price = data.last_trade_price;
    let change = (data.last_trade_price / data.price) * 100 - 100;
    qouteText.innerHTML = `$${last_trade_price.toFixed(2)}`;
    changeText.innerHTML = `(${change.toFixed(2)}%)`;
    if (change < 0) {
        changeText.style.color = '#9B0000';
    } else {
        changeText.style.color = '#006341';
    }
    volumeText.innerHTML = `Volume: ${data.volume}`;
    loadBids(data.orderbook.bids);
    loadAsks(data.orderbook.asks);
    drawChart(data['trades']);
}


function drawChart(data) {
    container.innerHTML = '';
    var dataSet = anychart.data.set(data);
    var firstSeriesData = dataSet.mapAs({ x: 0, value: 1 });
    var chart = anychart.line();

    chart
        .crosshair()
        .enabled(true)
        .yLabel({ enabled: false })
        .yStroke(null)
        .xStroke('#cecece')
        .zIndex(99);
        chart.yAxis(true);

        chart.xAxis(false);    
    var firstSeries = chart.spline(firstSeriesData);
    firstSeries.markers().zIndex(100);
    firstSeries.hovered().markers().enabled(true).type('circle').size(4);
    firstSeries.color('#006341');
    chart.container('container');
    chart.draw();
    
}

artViewDiv.innerHTML = '';

socket.on('trade', function(data) {
    if (currentView == 'trading') {
        tickerData = data;
        refresh(data);
    }
});

document.addEventListener('DOMContentLoaded', function() {

    switchViewButton.addEventListener('click', function() {
        if (switchViewButton.innerHTML === 'Art View') {
            switchViewButton.innerHTML = 'Trading View';
            tradingViewDiv.innerHTML = '';
            artViewDiv.innerHTML = artView;
            currentView = 'art';
        } else {
            switchViewButton.innerHTML = 'Art View';
            artViewDiv.innerHTML = '';
            tradingViewDiv.innerHTML = tradingView;
            currentView = 'trading';
            refresh(tickerData);
        }

    });

});