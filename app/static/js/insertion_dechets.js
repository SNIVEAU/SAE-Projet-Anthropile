document.addEventListener("DOMContentLoaded", function () {
  // Initialisation de la carte et centrage sur la Guadeloupe
  var map = L.map('mapid').setView([16.2450, -61.5110], 9); // Guadeloupe

  // Ajout des tuiles OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  // Fonction pour géocoder une adresse avec Nominatim
  function geocodeAddress(address, callback) {
    fetch('https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(address))
      .then(response => response.json())
      .then(data => {
        if (data && data.length > 0) {
          var latLng = [parseFloat(data[0].lat), parseFloat(data[0].lon)];
          callback(latLng); // Appel du callback avec les coordonnées obtenues
        } else {
          console.log("Adresse non trouvée : " + address);
        }
      })
      .catch(error => console.error('Erreur de géocodage :', error)); // Gestion des erreurs
  }

  // Récupérer les adresses depuis le serveur (passées depuis Flask)

  // Parcours des adresses et ajout des marqueurs après géocodage
  addresses.forEach(function (location) {
    geocodeAddress(location.address, function (latLng) {
      // Vérifier que les coordonnées sont valides avant d'ajouter le marqueur
      if (latLng) {
        L.marker(latLng).addTo(map)
          .bindPopup(
            `<strong>${location.name}</strong><br>
            <button type="button" onclick="selectPointDeCollecte('${location.id}')">Sélectionner ce point</button>`
          ); // Ajout d'un bouton pour sélectionner le point
      }
    });
  });
});

// Fonction JavaScript pour mettre à jour le champ id_point_collecte
function selectPointDeCollecte(id) {
  document.querySelector("select[name='id_point_collecte']").value = id;
}
