function createAlert(alertType, message, redirect, redirectMessage) {
    let alert = document.createElement('div');
    alert.classList.add('alert', 'alert-' + alertType, 'alert-dismissible');
    let button = document.createElement('button');
    button.classList.add('btn-close');
    button.setAttribute('data-bs-dismiss', 'alert');
    let strong = document.createElement('strong');
    strong.innerText = message + ' ';
    let link = document.createElement('a');
    link.classList.add('alert-link');
    link.setAttribute('href', redirect);
    link.innerText = redirectMessage;
    alert.appendChild(button);
    alert.appendChild(strong);
    alert.appendChild(link);
    return alert;
}