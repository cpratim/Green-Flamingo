let marker = document.getElementById("trades")

document.addEventListener("DOMContentLoaded", () => {
    let socket = io();

    socket.on('connect', function() {
        console.log('connected');

    });
    socket.on('trade', function(data) {
        marker.innerHTML = data.price;
    });
});