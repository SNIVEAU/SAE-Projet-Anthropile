document.getElementById("generate-report").addEventListener("click", function() {
    let selectedDate = document.getElementById("report-date").value;
    if (selectedDate) {
        window.location.href = `/download_pdf/${selectedDate}`;
    } else {
        alert("Veuillez sélectionner une date.");
    }
});