document.addEventListener("DOMContentLoaded", function () {
    const markAsReadButtons = document.querySelectorAll(".button");

    markAsReadButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const notificationId = button.getAttribute("id_notif");
            const estTrie = window.location.pathname.split('/').pop();

            fetch(`/marquer_lu/${notificationId}/${estTrie}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erreur serveur");
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const notificationElement = document.querySelector(`[notif-id="${notificationId}"]`);
                    if (notificationElement) {
                        notificationElement.classList.remove("unread");
                        notificationElement.classList.add("read");
                    }
                    button.style.display = "none";
                } else {
                    alert("Erreur: " + (data.error || "Une erreur inconnue est survenue."));
                }
            })
            .catch(error => {
                console.error("Erreur réseau : ", error);
                alert("Une erreur est survenue. Vérifiez votre connexion.");
            });
        });
    });
});
