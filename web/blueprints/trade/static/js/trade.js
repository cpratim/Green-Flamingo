let marketLimitSelect = document.getElementById('market-limit-select');
let priceInput = document.getElementById('price-input');
let priceLabel = document.getElementById('price-label');

let buySellSelect = document.getElementById('buy-sell-select');
let submitOrderButton = document.getElementById('submit-order-button');

let buyMarker = document.getElementById('btnradio1');
let sellMarker = document.getElementById('btnradio2');

document.addEventListener('DOMContentLoaded', function() {
    marketLimitSelect.addEventListener('change', function() {
        let marketLimit = marketLimitSelect.value;
        if (marketLimit === 'Market') {
            priceInput.disabled = true;
            priceLabel.innerHTML = 'Market Price:';
        } else {
            priceInput.disabled = false;
            priceLabel.innerHTML = 'Limit Price:';
        }
    });

    buySellSelect.addEventListener('change', function() {
        if (buyMarker.checked) {
            submitOrderButton.innerHTML = 'Submit Buy Order';
            submitOrderButton.style.backgroundColor = '#28a745';
        } else {
            submitOrderButton.innerHTML = 'Submit Sell Order';
            submitOrderButton.style.backgroundColor = '#dc3545';
        }
    });
});
