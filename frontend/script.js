// Initialize the map centered at MIT
var map = L.map('map').setView([42.3601, -71.0942], 16);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Define some locations
var locations = {
    "Stata Center": [42.361677900508745, -71.09062677005224],
    "Simmons Hall": [42.3570809844781, -71.10151119925918],
    "Killian Court": [42.35887146633117, -71.09152799223449],
    "Lobby 7": [42.35930750246464, -71.0931051310534]
};

// Add markers and click event
Object.keys(locations).forEach(location => {
    var marker = L.marker(locations[location]).addTo(map)
        .bindPopup(location)
        .on('click', () => fetchConfession(location));
});

function fetchConfession(location) {
    let confessionBox = document.getElementById("confession-box");

    // Show initial fetching status
    confessionBox.innerText = "Eavesdropping...";

    fetch(`http://127.0.0.1:5000/confession?location=${encodeURIComponent(location)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            confessionBox.innerText = "Generating confession..."; // Show generation status
            return response.json();
        })
        .then(data => {
            confessionBox.innerText = data.confession;
        })
        .catch(error => {
            console.error("Error fetching confession:", error);
            confessionBox.innerText = "Error fetching confession.";
        });
}
