document.addEventListener("DOMContentLoaded", function () {
    function updateNotificationBadge() {
        fetch("/api/notifications_non_lues")
            .then(response => response.json())
            .then(data => {
                const badge = document.querySelector(".cloche .badge");
                
                if (data.alertes_non_lues > 0) {
                    if (!badge) {
                        const newBadge = document.createElement("div");
                        newBadge.classList.add("badge");
                        newBadge.textContent = data.alertes_non_lues > 99 ? "+99" : data.alertes_non_lues;
                        document.querySelector(".cloche").appendChild(newBadge);
                    } else {
                        badge.textContent = data.alertes_non_lues > 99 ? "+99" : data.alertes_non_lues;
                        badge.style.display = "flex";
                    }
                } else if (badge) {
                    badge.style.display = "none";
                }
            })
            .catch(error => console.error("Erreur lors de la mise à jour des notifications:", error));
    }

    // Rafraîchir toutes les 30 secondes
    setInterval(updateNotificationBadge, 30000);

    // Chargement initial des notifications
    updateNotificationBadge();
});