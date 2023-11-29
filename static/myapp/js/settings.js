document.addEventListener('DOMContentLoaded', init);

function init() {
    document.querySelector("#reboot").addEventListener("click", reboot);
}

function reboot() {
    fetch('/myapp/reboot', {
        method: 'GET',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
        }
    }).then(response => response.json())
        .then(data => {
            console.log(data);
        });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
