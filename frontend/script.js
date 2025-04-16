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
    "Lobby 7": [42.35930750246464, -71.0931051310534],
    "Next House": [42.355107554683016, -71.10162768938001],
    "East Campus": [42.36038761368802, -71.08853231135414],
    "Banana Lounge": [42.36067493812588, -71.09113360108799],
    "Z Center": [42.35892447631196, -71.09588882645764],
    "Stud": [42.359052772881476, -71.09483344230945],
    "Infinite Corridor": [42.359451, -71.092361],
    "Green Building": [42.36033219796149, -71.08931796450563],
    "Kresge": [42.358207270229336, -71.09499724517542],
    "Briggs Field": [42.35676511220947, -71.09906492870475],
    "Hayden Library": [42.35904661158103, -71.08922822676674],
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

    fetch(`http://127.0.0.1:5000/confession_db?location=${encodeURIComponent(location)}`)
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
