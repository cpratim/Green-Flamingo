let buyButton = document.getElementById('buy-button');
let sellButton = document.getElementById('sell-button');
let marketLimitSwitch = document.getElementById('market-limit-switch');
let buySellSwitch = "buy";
let orderType = "market";
let priceInputLabel = document.getElementById('price-input-label');
let priceInput = document.getElementById('price-input');
let orderEstimate = document.getElementById('order-estimate');
let quantityInput = document.getElementById('quantity-input');
let username = document.getElementById('username').content;
let ordersWrapper = document.getElementById('orders-wrapper');
let ownedQuantity = 0;
let orderButton = document.getElementById('order-button');
let balanceText = document.getElementById('balance');
let buyPowerText = document.getElementById('order-box-footer-text');
let balance = 0;
let orders = [];
let portfolioValueText = document.getElementById('portfolio-value');
let piecesOwnedText = document.getElementById('pieces-owned');
let alerts = document.getElementById('alerts');


function makeOrder(order) {
    
    let orderDiv = document.createElement('div');
    orderDiv.id = 'position-box';
    orderDiv.innerHTML = `
        <div id="position-box-data-left">
            <div id="position-box-data-wrapper-left">
                <div id="position-box-title">${order.side} ECON</div>
                <div id="position-box-type">Status: ${order.type}</div>
            </div>
        </div>
        <div id="position-box-data-right">
            <div id="position-box-data-wrapper-right">
                <div id="position-box-quantity">Quantity: ${order.quantity} Pieces</div>
                <div id="position-box-price">Fill Price: $${order.price}</div>
            </div>
            
        </div>
    `
    ordersWrapper.appendChild(orderDiv);
}

function postOrder(side, price, quantity) {
    fetch('/api/user_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            side: side,
            price: price,
            quantity: quantity,
            ticker: "ECON"
        })
    })
    .then(response => response.json())
    .then(data => {
        if ('error' in data) {
            alerts.innerHTML = '<div class="alert danger">Invalid Order!</div>'
        }
        else {
            alerts.innerHTML = '<div class="alert success">Order Filled!</div>'
            ownedQuantity = data.quantity;
            orders = data.history;
            ordersWrapper.innerHTML = '';
            balance = data.balance;
            if ('ECON' in data.portfolio) {
                ownedQuantity = data.portfolio.ECON;
            }
            if (ownedQuantity >= 0) {
                piecesOwnedText.innerHTML = ownedQuantity;
            }
            balanceText.innerHTML = `$${data.balance.toFixed(2)}`;
            if (buySellSwitch === "buy") {
                buyPowerText.innerHTML = `$${data.balance.toFixed(2)} buying power available`;
            } else {
                buyPowerText.innerHTML = `${ownedQuantity} pieces owned`;
            }
            for (let i = orders.length-1; i >= 0; i--) {
                makeOrder(orders[i]);
            }
        }
    });
}

function getUserData() {
    let url = `/api/user/${username}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if ('ECON' in data.portfolio) {
                ownedQuantity = data.portfolio.ECON;
                console.log(ownedQuantity);
            }
            if (ownedQuantity >= 0) {
                piecesOwnedText.innerHTML = ownedQuantity;
            }
            balanceText.innerHTML = `$${data.balance.toFixed(2)}`;
            if (buySellSwitch === "buy") {
                buyPowerText.innerHTML = `$${data.balance.toFixed(2)} buying power available`;
            } else {
                buyPowerText.innerHTML = `${ownedQuantity} pieces owned`;
            }
            balance = data.balance;
            orders = data.history;
            ordersWrapper.innerHTML = '';
            for (let i = orders.length-1; i >= 0; i--) {
                makeOrder(orders[i]);
            }
        });
}

function marketLimitChange() {
    console.log("marketLimitChange");
    console.log(marketLimitSwitch.value);
    if (marketLimitSwitch.value == "market") {
        orderType = "market";
        priceInputLabel.innerHTML = "Market Price:";
        priceInput.disabled = true;
    } else {
        orderType = "limit";
        priceInputLabel.innerHTML = "Limit Price:";
        priceInput.disabled = false;
    }
}

function refreshForm(data) {
    if (orderType == "market") {
        priceInput.value = data.last_trade_price;
        let quantity = quantityInput.value;
        let portfolioValue = balance;
        let estimate = quantity * data.last_trade_price;
        if (ownedQuantity > 0) {
            portfolioValue += ownedQuantity * data.last_trade_price;
        }
        portfolioValueText.innerHTML = `$${portfolioValue.toFixed(2)}`;
        if (buySellSwitch == "buy") {
            orderEstimate.innerHTML = `Buy Order Estimated Cost: $${estimate.toFixed(2)}`;
        } else {
            orderEstimate.innerHTML = `Sell Order Estimated Profit: $${estimate.toFixed(2)}`;
        }
    }
}


socket.on('trade', function(data) {
    if (currentView == 'trading') {
        refreshForm(data);
    }
});


document.addEventListener('DOMContentLoaded', function() {
    getUserData();
    buyButton.addEventListener('click', function() {
        buySellSwitch = "buy";
        buyButton.classList.add("active");
        sellButton.classList.remove("active");
        let quantity = quantityInput.value;
        let estimate = quantity * tickerData.last_trade_price;
        buyPowerText.innerHTML = `$${balance.toFixed(2)} buying power available`;
        orderEstimate.innerHTML = `Buy Order Estimated Cost: $${estimate.toFixed(2)}`;
    });
    sellButton.addEventListener('click', function() {
        buySellSwitch = "sell";
        sellButton.classList.add("active");
        buyButton.classList.remove("active");
        let quantity = quantityInput.value;
        let estimate = quantity * tickerData.last_trade_price;
        buyPowerText.innerHTML = `${ownedQuantity} pieces owned`;
        orderEstimate.innerHTML = `Sell Order Estimated Profit: $${estimate.toFixed(2)}`;
    });
    orderButton.addEventListener('click', function() {
        let side = buySellSwitch;
        let price = priceInput.value;
        let quantity = quantityInput.value;
        postOrder(side, price, quantity);
    });
    quantityInput.addEventListener('input', function() {
        refreshForm(tickerData);
    });
});