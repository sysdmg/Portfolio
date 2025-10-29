// Sample cafe data
const cafes = [
    {
        id: 1,
        name: "Digital Den Cafe",
        address: "123 Tech Street",
        coordinates: [37.7749, -122.4194], // San Francisco coordinates
        hasWifi: true,
        hasPower: true,
        wifiSpeed: "100 Mbps",
        powerOutlets: 12,
        openingHours: "8:00 AM - 8:00 PM",
        description: "Spacious cafe with dedicated workspaces"
    },
    {
        id: 2,
        name: "Workspace Coffee",
        address: "456 Startup Avenue",
        coordinates: [37.7833, -122.4167],
        hasWifi: true,
        hasPower: true,
        wifiSpeed: "75 Mbps",
        powerOutlets: 8,
        openingHours: "7:00 AM - 7:00 PM",
        description: "Quiet atmosphere with meeting rooms"
    },
    // Add more sample cafes as needed
];

// Initialize the map
let map = L.map('map').setView([37.7749, -122.4194], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Store markers for easy removal/filtering
let markers = [];

// Function to create a cafe marker
function createMarker(cafe) {
    const marker = L.marker(cafe.coordinates)
        .bindPopup(`
            <h3>${cafe.name}</h3>
            <p>${cafe.address}</p>
            <p><strong>WiFi:</strong> ${cafe.hasWifi ? '✓' + ' ' + cafe.wifiSpeed : '✗'}</p>
            <p><strong>Power Outlets:</strong> ${cafe.hasPower ? '✓' + ' (' + cafe.powerOutlets + ' available)' : '✗'}</p>
            <p><strong>Hours:</strong> ${cafe.openingHours}</p>
        `);
    return marker;
}

// Function to create a cafe list item
function createCafeItem(cafe) {
    const div = document.createElement('div');
    div.className = 'cafe-item';
    div.innerHTML = `
        <h3>${cafe.name}</h3>
        <p>${cafe.address}</p>
        <div class="features">
            <span class="feature">
                <span>WiFi:</span> ${cafe.hasWifi ? '✓' : '✗'}
            </span>
            <span class="feature">
                <span>Power:</span> ${cafe.hasPower ? '✓' : '✗'}
            </span>
        </div>
    `;
    div.addEventListener('click', () => {
        map.setView(cafe.coordinates, 15);
        markers.find(m => m.cafe.id === cafe.id).marker.openPopup();
    });
    return div;
}

// Function to update the map and list based on filters
function updateDisplay() {
    const searchText = document.getElementById('search').value.toLowerCase();
    const wifiFilter = document.getElementById('wifi-filter').checked;
    const powerFilter = document.getElementById('power-filter').checked;

    // Clear existing markers and list
    markers.forEach(m => m.marker.remove());
    markers = [];
    document.getElementById('cafe-items').innerHTML = '';

    // Filter and display cafes
    cafes.filter(cafe => {
        const matchesSearch = cafe.name.toLowerCase().includes(searchText) ||
                            cafe.address.toLowerCase().includes(searchText);
        const matchesWifi = !wifiFilter || cafe.hasWifi;
        const matchesPower = !powerFilter || cafe.hasPower;
        return matchesSearch && matchesWifi && matchesPower;
    }).forEach(cafe => {
        // Add marker to map
        const marker = createMarker(cafe);
        marker.addTo(map);
        markers.push({ cafe, marker });

        // Add item to list
        document.getElementById('cafe-items').appendChild(createCafeItem(cafe));
    });
}

// Event listeners
document.getElementById('search').addEventListener('input', updateDisplay);
document.getElementById('wifi-filter').addEventListener('change', updateDisplay);
document.getElementById('power-filter').addEventListener('change', updateDisplay);
document.getElementById('search-btn').addEventListener('click', updateDisplay);

// Initial display
updateDisplay();