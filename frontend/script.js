// Initialize the map centered at MIT
var map = L.map('map').setView([42.3601, -71.0942], 16);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Define some locations and their placeholder confessions
var locations = {
    "Stata Center": { coords: [42.3618784401601, -71.09072610287322], confession: "I once stayed in Stata for 48 hours straight, surviving only on Soylent and coffee." },
    "Simmons Hall": { coords: [42.35703064313976, -71.10166718351876], confession: "Sometimes I just walk into Simmons because it feels like a giant cheese grater." },
    "Killian Court": { coords: [42.35915382446763, -71.09156883355729], confession: "I graduated last year and still have nightmares about running naked through Killian." },
    "Lobby 7": { coords: [42.35951439870911, -71.09314417218918], confession: "I used to believe that the Infinite Corridor actually never ended." }
};

// Add markers and click event
Object.keys(locations).forEach(location => {
    var place = locations[location];
    var marker = L.marker(place.coords).addTo(map)
        .bindPopup(location)
        .on('click', () => {
            document.getElementById("confession-box").innerText = place.confession;
        });
});
