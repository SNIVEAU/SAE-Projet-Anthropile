// document.addEventListener("DOMContentLoaded", function () {
//     const trashIcon = document.getElementById("clear-read-notifications");

//     if (trashIcon) {
//         trashIcon.addEventListener("click", function () {
//             const confirmDelete = window.confirm("Êtes-vous sûr de vouloir supprimer toutes les alertes lues ?");
            
//             if (confirmDelete) {
//                 // Appel à l'API pour supprimer les alertes lues en base de données
//                 fetch('/delete_all_read_alertes', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json'
//                     },
//                 })
//                 .then(response => response.json())
//                 .then(data => {
//                     if (data.success) {
//                         console.log("Toutes les alertes lues ont été supprimées en base de données.");
                        
//                         // Optionnel : Mettre à jour l'interface pour refléter la suppression
//                         const readNotifications = document.querySelectorAll(".notification.read");
//                         readNotifications.forEach(function (notification) {
//                             notification.remove();
//                         });

//                         // Afficher un message de succès si nécessaire (par exemple, un alert() ou autre)
//                         alert("Toutes les alertes lues ont été supprimées.");
//                     } else {
//                         console.error("Erreur lors de la suppression des alertes lues.");
//                         alert("Une erreur est survenue lors de la suppression.");
//                     }
//                 })
//                 .catch(error => {
//                     console.error("Erreur AJAX:", error);
//                     alert("Une erreur est survenue.");
//                 });
//             }
//         });
//     }
// });
