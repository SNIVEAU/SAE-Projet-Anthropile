function confirmEdit(url) {
    if (confirm("Êtes-vous sûr de vouloir modifier ce point de collecte ?")) {
        window.location.href = url;  // Redirige vers l'URL de modification
    }
}
function confirmDelete(url) {
    if (confirm("Êtes-vous sûr de vouloir supprimer ce point de collecte ?")) {
        window.location.href = url;  // Redirige vers l'URL de suppression
    }
}
document.addEventListener("DOMContentLoaded", function () {
    // Initialisation de la carte et centrage sur la Guadeloupe
    var map = L.map('mapid').setView([16.2650, -61.5510], 10); // Guadeloupe

    // Ajout des tuiles OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Parcours des adresses et ajout des marqueurs
    addresses.forEach(function (location) {
        // Vérifier que les coordonnées sont valides avant d'ajouter le marqueur
        if (location.lat && location.lng) {
            var latLng = [location.lat, location.lng];
            L.marker(latLng).addTo(map)
                .bindPopup(
                    `<strong>${location.name}</strong><br>
      <button onclick="window.location.href='${location.detailUrl}'">Voir le détail</button>`
                ); // Ajout d'une popup avec le nom et le bouton
        }
    });
});