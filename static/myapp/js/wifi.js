document.addEventListener('DOMContentLoaded', init);

function init() {
    getWifiNetworks();
    setInterval(getWifiNetworks, 5000);
    document.querySelector("#wifi-form button").addEventListener("click", connectToWiFi);
    
}

function getWifiNetworks() {
    fetch('/myapp/wifi/get_networks')
        .then(response => response.json())
        .then(data => {
            const networks = data.wifi_networks;
            console.log(networks);
            const select = document.getElementById("network-select");
            select.innerHTML = "";
            networks.forEach(network => {
                const option = document.createElement("option");
                option.text = network.ssid;
                select.add(option);
            });
        });
}

function connectToWiFi() {
    const selectedNetwork = document.getElementById("network-select").value;
    const password = document.getElementById("password").value;

    if (selectedNetwork && password) {
        console.log("Connecting to Wi-Fi network:", selectedNetwork, "with password:", password);
        fetch('/myapp/wifi/connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie('csrftoken'),
                 // Include the CSRF token
            },
            body: JSON.stringify({
                "ssid": selectedNetwork,
                "password": password
            })
        })
    } else {
        console.log("Please select a Wi-Fi network and enter the password.");
    }
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

