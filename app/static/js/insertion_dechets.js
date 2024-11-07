document.addEventListener("DOMContentLoaded", function () {
  // Initialisation de la carte et centrage sur la Guadeloupe
  var map = L.map('mapid').setView([16.2450, -61.5110], 9); // Guadeloupe

  // Ajout des tuiles OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  // Récupérer les adresses depuis le serveur (passées depuis Flask)

  // Parcours des adresses et ajout des marqueurs après géocodage
  addresses.forEach(function (location) {
    // Vérifier que les coordonnées sont valides avant d'ajouter le marqueur
    if (location.lat && location.lng) {
      var latLng = [location.lat, location.lng];
      L.marker(latLng).addTo(map)
        .bindPopup(
          `<strong>${location.name}</strong><br>
          <button type="button" onclick="selectPointDeCollecte('${location.id}')">Sélectionner ce point</button>`
        ); // Ajout d'une popup avec le nom et le bouton
    }
  });
});

// Fonction JavaScript pour mettre à jour le champ id_point_collecte
function selectPointDeCollecte(id) {
  document.querySelector("select[name='id_point_collecte']").value = id;
}
