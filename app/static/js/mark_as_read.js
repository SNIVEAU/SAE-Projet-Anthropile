document.addEventListener("DOMContentLoaded", function () {
    const markAsReadButtons = document.querySelectorAll(".button");

    markAsReadButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const notificationId = button.getAttribute("id_notif");

            fetch(`/marquer_lu/${notificationId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
            })
            .then(response => {
                if (response.ok) {
                    const notificationElement = document.querySelector(`[notif-id="${notificationId}"]`);
                    notificationElement.classList.remove("unread");
                    notificationElement.classList.add("read");

                    button.style.display = "none";
                } else {
                    alert("Une erreur est survenue lors de la mise à jour de la notification.");
                }
            })
            .catch((error) => {
                console.error("Erreur réseau : ", error);
                alert("Une erreur est survenue.");
            });
        });
    });
});
