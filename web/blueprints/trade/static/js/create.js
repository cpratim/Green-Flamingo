let artPlaceholder = document.getElementById('art-placeholder');
let artInput = document.getElementById('art-input');
let launchButton = document.getElementById('launch-button');
let imageIDMeta = document.getElementById('image-id');
let usernameMeta = document.getElementById('username');
let alerts = document.getElementById('alerts');

let socket = io();

function updateArtPlaceholder(art) {
    artPlaceholder.style.backgroundImage = `url(http://127.0.0.1:5100/api/v1/art/${art})`;
    imageIDMeta.content = art;
    artPlaceholder.style.backgroundColor = 'transparent';
    artPlaceholder.innerHTML = '';
}

function postForm(title, description, ticker, category, ipoPrice, artID, quantity) {
    fetch('http://127.0.0.1:5100/api/v1/art/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'ngrok-skip-browser-warning': 'true',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
            username: usernameMeta.content,
            title: title,
            description: description,
            ticker: ticker,
            category: category,
            ipoPrice: ipoPrice,
            quantity: quantity,
            artID: artID
        })
    }).then(response => {
        return response.json();
    }).then(data => {
        let status = data.status;
        if (status === 'success') {

            window.location.href = `/trade/${usernameMeta.content}/${ticker}`;
        } else {
            let alert = createAlert('danger', 'Invalid Form Input!', '/create', 'Try Again!');
            alerts.appendChild(alert);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    artInput.addEventListener('change', function() {
        console.log('here');
        let file = artInput.files[0];
        let reader = new FileReader();
        let blob = new Blob([file], {type: 'image/png'});
        socket.emit('upload', blob);
    });

    socket.on('upload', function(art) {
        console.log(art);
        updateArtPlaceholder(art);
    });

    launchButton.addEventListener('click', function() {
        let title = document.getElementById('art-title').value;
        let description = document.getElementById('art-description').value;
        let ticker = document.getElementById('art-ticker').value;
        let price = document.getElementById('ipo-price').value;
        let category = document.getElementById('art-category').value;
        let imageID = imageIDMeta.getAttribute('content');
        let quantity = document.getElementById('ipo-quantity').value;
        postForm(title, description, ticker, category, price, imageID, quantity);
    });
});