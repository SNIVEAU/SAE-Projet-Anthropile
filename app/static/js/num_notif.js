document.addEventListener("DOMContentLoaded", function () {
    function updateNotificationBadge() {
        fetch("/api/notifications_non_lues")
            .then(response => response.json())
            .then(data => {
                const badge = document.querySelector(".cloche .badge");
                
                if (data.count > 0) {
                    if (!badge) {
                        const newBadge = document.createElement("div");
                        newBadge.classList.add("badge");
                        newBadge.textContent = data.count > 99 ? "+99" : data.count;
                        document.querySelector(".cloche").appendChild(newBadge);
                    } else {
                        badge.textContent = data.count > 99 ? "+99" : data.count;
                        badge.style.display = "block";
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