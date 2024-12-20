// delete_avis.js
document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-btn");
    const popup = document.getElementById("popup");
    const confirmDeleteButton = document.getElementById("confirm-delete");
    const cancelButton = document.getElementById("cancel");
    let avisIdToDelete = null;

    // Lorsqu'on clique sur le bouton Supprimer
    deleteButtons.forEach((button) => {
        button.addEventListener("click", function () {
            avisIdToDelete = button.getAttribute("data-avis-id");
            document.getElementById("avis-id").value = avisIdToDelete;  // Affecte l'ID de l'avis à supprimer
            popup.classList.remove("hidden");  // Affiche la popup de confirmation
        });
    });

    // Confirmer la suppression
    confirmDeleteButton.addEventListener("click", function () {
        if (avisIdToDelete) {
            // Modifie l'action du formulaire pour inclure l'ID de l'avis dans l'URL
            document.getElementById("delete-form").action = "/delete_avis/" + avisIdToDelete;
            // Soumet le formulaire
            document.getElementById("delete-form").submit();
        }
    });

    // Annuler la suppression
    cancelButton.addEventListener("click", function () {
        avisIdToDelete = null;
        popup.classList.add("hidden");  // Cache la popup si l'annulation est cliquée
    });
});
