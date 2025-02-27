function initializeMap(addresses) {
    // Initialisation de la carte
    let map = L.map('mapid');

    // Ajout d'une couche de tuiles (tiles) OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Créer un tableau pour stocker les coordonnées des points
    let markers = [];

    // Ajouter des marqueurs pour chaque point de collecte
    addresses.forEach(function (point) {
        if (point.lat && point.lng) {
            let marker = L.marker([point.lat, point.lng]) // Créer un marqueur
                .addTo(map)
                .bindPopup(`<b>${point.name}</b><br>${point.address}`); // Ajouter un popup
            markers.push(marker.getLatLng()); // Ajouter les coordonnées du marqueur au tableau
        } else {
            console.error("Coordonnées manquantes pour :", point);
        }
    });

    console.warn("Aucun marqueur valide trouvé.");
    map.setView([16.2250, -61.5510], 10); 
}

// Exécuter la fonction initializeMap lorsque le DOM est chargé
document.addEventListener("DOMContentLoaded", function () {
    // Passer les données addresses à la fonction initializeMap
    if (typeof addresses !== 'undefined') {
        initializeMap(addresses);
    } else {
        console.error("La variable addresses n'est pas définie.");
    }
});