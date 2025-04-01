// Initialize the map centered at MIT
var map = L.map('map').setView([42.3601, -71.0942], 16);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Define some locations
var locations = {
    "stata": [42.3628, -71.0913],
    "simmons": [42.3564, -71.1011],
    "killian": [42.3588, -71.0921],
    "lobby7": [42.3592, -71.0935]
};

// Add markers and click event
Object.keys(locations).forEach(location => {
    var marker = L.marker(locations[location]).addTo(map)
        .bindPopup(location)
        .on('click', () => fetchConfession(location));
});

// Fetch confession from backend
function fetchConfession(location) {
    fetch(`http://127.0.0.1:5000/confession?location=${encodeURIComponent(location)}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("confession-box").innerText = data.confession;
        })
        .catch(error => {
            console.error("Error fetching confession:", error);
            document.getElementById("confession-box").innerText = "Error fetching confession.";
        });
}
