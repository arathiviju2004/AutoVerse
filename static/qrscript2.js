

function domReady(fn) {
    if (
        document.readyState === "complete" ||
        document.readyState === "interactive"
    ) {
        setTimeout(fn, 1000);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

domReady(function () {
    // Load JSON file containing vehicle registration numbers
    async function loadVehicleList() {
        try {
            const response = await fetch("static/vehicleList.json"); // Path to your JSON file
            if (!response.ok) {
                throw new Error("Failed to load vehicle list");
            }
            return await response.json();
        } catch (error) {
            console.error("Error loading vehicle list:", error);
            return [];
        }
    }

    // If a QR code is found, check against the JSON file
    async function onScanSuccess(decodeText, decodeResult) {
        const vehicleList = await loadVehicleList();
    
        if (vehicleList.includes(decodeText)) {
            alert("QR code matches a vehicle in the list: " + decodeText);
            // Redirect to a different page or file
            window.location.href = "static/gpstracker.html"; // Replace with the desired page/file
            startTracking(); // Optionally, you can keep this for tracking if needed
        } else {
            alert("QR code does not match any vehicle in the list: " + decodeText);
        }
    }
    

    // Start GPS tracking
    function startTracking() {
        if ("geolocation" in navigator) {
            navigator.geolocation.watchPosition(
                (position) => {
                    console.log(
                        `Tracking... Latitude: ${position.coords.latitude}, Longitude: ${position.coords.longitude}`
                    );
                },
                (error) => {
                    console.error("Error getting location:", error);
                },
                {
                    enableHighAccuracy: true,
                }
            );
        } else {
            alert("Geolocation is not supported by your browser.");
        }
    }

    // Initialize QR code scanner
    let htmlscanner = new Html5QrcodeScanner(
        "my-qr-reader",
        { fps: 10, qrbox: 250 } // Corrected the typo in 'qrbox'
    );
    htmlscanner.render(onScanSuccess);
});
