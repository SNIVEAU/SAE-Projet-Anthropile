document.addEventListener("DOMContentLoaded", function () {
    const btnPeriode = document.getElementById("btn-periode");
    const btnJour = document.getElementById("btn-jour");
    const dateSeule = document.getElementById("date-seule");
    const datePeriode = document.getElementById("date-periode");
    const generateButton = document.getElementById("generate-report");

    // Affichage des champs selon le choix de l'utilisateur
    btnPeriode.addEventListener("click", function () {
        dateSeule.style.display = "none";
        datePeriode.style.display = "block";
    });

    btnJour.addEventListener("click", function () {
        dateSeule.style.display = "block";
        datePeriode.style.display = "none";
    });

    // Gestion de la génération de rapport
    generateButton.addEventListener("click", function () {
        let date = document.getElementById("report-date").value;
        let startDate = document.getElementById("start-date").value;
        let endDate = document.getElementById("end-date").value;

        if (dateSeule.style.display !== "none" && date) {
            alert("Génération du rapport pour la date : " + date);
        } else if (datePeriode.style.display !== "none" && startDate && endDate) {
            alert("Génération du rapport du " + startDate + " au " + endDate);
        } else {
            alert("Veuillez sélectionner une date ou une période valide.");
        }
    });
});
