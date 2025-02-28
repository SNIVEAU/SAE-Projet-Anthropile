document.addEventListener("DOMContentLoaded", function () {
    const btnPeriode = document.getElementById("btn-periode");
    const btnJour = document.getElementById("btn-jour");
    const dateSeule = document.getElementById("date-seule");
    const datePeriode = document.getElementById("date-periode");
    const generateButton = document.getElementById("generate-report");

    // Fonction pour activer le bon bouton et désactiver l'autre
    function setActiveButton(activeBtn, inactiveBtn) {
        activeBtn.style.backgroundColor = "#0056b3";
        activeBtn.style.color = "#fff";
        activeBtn.style.fontWeight = "bold";
        activeBtn.style.transform = "scale(1.05)";
        
        inactiveBtn.style.backgroundColor = "#007bff";
        inactiveBtn.style.color = "#fff";
        inactiveBtn.style.fontWeight = "normal";
        inactiveBtn.style.transform = "scale(0.95)";
    }

    // Gestion de l'affichage des dates et des boutons actifs
    btnPeriode.addEventListener("click", function () {
        dateSeule.style.display = "none";  
        datePeriode.style.display = "block"; // Assure un bon affichage

        setActiveButton(btnPeriode, btnJour);
    });

    btnJour.addEventListener("click", function () {
        dateSeule.style.display = "flex"; // Remet l'affichage
        datePeriode.style.display = "none";  

        setActiveButton(btnJour, btnPeriode);
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
