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

    // Variable pour stocker le dernier marqueur temporaire
    var lastTempMarker = null;

    // Ajouter un événement click pour récupérer les coordonnées
    map.on('click', function (e) {
        // Récupération des coordonnées du clic
        var lat = e.latlng.lat;
        var lng = e.latlng.lng;

        // Supprimer le dernier marqueur temporaire s'il existe
        if (lastTempMarker) {
            map.removeLayer(lastTempMarker);
        }

        // Ajouter un nouveau marqueur temporaire au point cliqué
        lastTempMarker = L.marker([lat, lng]).addTo(map);

        // Mettre à jour les champs du formulaire
        var latInput = document.querySelector('input[name="latitude"]');
        var lngInput = document.querySelector('input[name="longitude"]');
        var addressInput = document.querySelector('input[name="adresse"]');

        if (latInput && lngInput) {
            latInput.value = lat;
            lngInput.value = lng;
        }

        // Effectuer une requête de géocodage inversé pour obtenir l'adresse
        fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`)
            .then(response => response.json())
            .then(data => {
                if (data && data.display_name) {
                    var address = data.display_name; // Adresse complète

                    // Mettre à jour le champ adresse
                    if (addressInput) {
                        addressInput.value = address;
                    }

                    console.log("Adresse récupérée :", address);
                } else {
                    console.error("Aucune adresse trouvée pour ces coordonnées.");
                }
            })
            .catch(error => {
                console.error("Erreur lors de la requête de géocodage inversé :", error);
            });
    });
});

// Fonction pour effacer la valeur d'un champ de coordonnées
function clearCoordinate(coordinate) {
    document.querySelector(`[name='latitude']`).value = '';
    document.querySelector(`[name='longitude']`).value = '';
}
