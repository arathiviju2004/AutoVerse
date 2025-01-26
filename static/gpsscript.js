let map; // Map instance
let vehicleMarker; // Marker for tracking
let tracking = false; // Tracking state
let previousCoords = null; // Store previous GPS location
let totalDistance = 0; // Total distance traveled in kilometers
const farePerKm = 25; // Fare rate per kilometer (customize as needed)
let watchId = null; // ID for the GPS watchPosition

// Initialize the map on page load
function initializeMap() {
    map = L.map("map").setView([0, 0], 13); // Default map view
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "© OpenStreetMap contributors",
    }).addTo(map);

    vehicleMarker = L.marker([0, 0]).addTo(map); // Add a marker to the map
}

// Start tracking
document.getElementById("startButton").addEventListener("click", () => {
    if (!map) {
        initializeMap(); // Ensure map is initialized
    }

    tracking = true;
    totalDistance = 0; // Reset distance
    previousCoords = null; // Reset previous coordinates
    document.getElementById("fare").textContent = "";
    document.getElementById("startButton").disabled = true;
    document.getElementById("stopButton").disabled = false;

    if ("geolocation" in navigator) {
        watchId = navigator.geolocation.watchPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                updateLocation(latitude, longitude);
            },
            (error) => {
                console.error("Error getting GPS location:", error.message);
                alert("Error accessing GPS. Make sure location services are enabled.");
            },
            { enableHighAccuracy: true, maximumAge: 10000, timeout: 10000 }
        );
    } else {
        alert("Geolocation is not supported by your browser.");
    }
});

// Stop tracking
document.getElementById("stopButton").addEventListener("click", () => {
    tracking = false;
    document.getElementById("startButton").disabled = false;
    document.getElementById("stopButton").disabled = true;

    if (watchId !== null) {
        navigator.geolocation.clearWatch(watchId);
        watchId = null;
    }

    // Calculate and display the fare
    const fare = (totalDistance * farePerKm).toFixed(2);
    document.getElementById("fare").textContent = `Total Distance: ${totalDistance.toFixed(
        2
    )} km | Fare: ₹${fare}`;
});

// Update location on the map
function updateLocation(lat, lng) {
    if (tracking) {
        vehicleMarker.setLatLng([lat, lng]); // Update marker position
        map.setView([lat, lng], 13); // Adjust map view

        if (previousCoords) {
            const distance = calculateDistance(
                previousCoords.lat,
                previousCoords.lng,
                lat,
                lng
            );
            totalDistance += distance;
        }

        previousCoords = { lat, lng }; // Update previous coordinates
    }
}

// Haversine formula to calculate distance between two coordinates
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth's radius in km
    const dLat = degToRad(lat2 - lat1);
    const dLon = degToRad(lon2 - lon1);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(degToRad(lat1)) *
            Math.cos(degToRad(lat2)) *
            Math.sin(dLon / 2) *
            Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distance in km
}

// Convert degrees to radians
function degToRad(deg) {
    return deg * (Math.PI / 180);
}

// Initialize the map when the page loads
document.addEventListener("DOMContentLoaded", initializeMap);


