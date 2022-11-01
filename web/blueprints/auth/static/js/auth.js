let registerFormButton = document.getElementById('register-submit-button');
let loginFormButton = document.getElementById('login-submit-button');
let alerts = document.getElementById('alerts');

function authenticateUser(username, password) {
    fetch('/login_handler', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'ngrok-skip-browser-warning': 'true',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    }).then(response => {
        return response.json();
    }).then(data => {
        alerts.innerHTML = '';
        let status = data.status;
        if (status === '200') {
            window.location.href = '/create';
            
        } else {
            let alert = createAlert('danger', 'Invalid Credentials!', '/login', 'Try Again!');
            alerts.appendChild(alert);
        }
    });
}

function registerUser(username, email, password) {
    fetch('http://127.0.0.1:5100/api/v1/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'ngrok-skip-browser-warning': 'true',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
            username: username,
            password: password,
            email: email
        })
    }).then(response => {
        return response.json();
    }).then(data => {
        let status = data.status;
        alerts.innerHTML = '';
        if (status === '200') {
            let alert = createAlert('success', 'Registration Successful!', '/login', 'Login Here!');
            alerts.appendChild(alert);
        } else {
            let alert = createAlert('danger', 'Registration Failed!', '/register', 'Try Again!');
            alerts.appendChild(alert);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    loginFormButton.addEventListener('click', function() {
        let email = document.getElementById('username').value;
        let password = document.getElementById('password').value;
        authenticateUser(email, password);
    });
    registerFormButton.addEventListener('click', function() {
        let username = document.getElementById('username').value;
        let email = document.getElementById('email').value;
        let password = document.getElementById('password').value;
        registerUser(username, email, password);
    });
});