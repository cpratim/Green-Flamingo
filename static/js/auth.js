let loginFormButton = document.getElementById('login-submit-button');
let alerts = document.getElementById('alerts');

function authenticateUser(username) {
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'ngrok-skip-browser-warning': 'true',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
            username: username,
        })
    }).then(response => {
        return response.json();
    }).then(data => {
        alerts.innerHTML = '';
        let status = data.status;
        if (status === '200') {
            fetch('/api/new_user', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                    'ngrok-skip-browser-warning': 'true',
                    'Access-Control-Allow-Origin': '*'
                },
            }).then(response => {
                window.location.href = '/';
            });
        } else {
            let alert = createAlert('danger', 'Invalid Credentials!', '/login', 'Try Again!');
            alerts.appendChild(alert);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    loginFormButton.addEventListener('click', function() {
        let username = document.getElementById('username').value;
        authenticateUser(username);
    });
});