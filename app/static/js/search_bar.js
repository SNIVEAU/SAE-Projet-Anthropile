document.getElementById('search-input').addEventListener('input', function () {
    const searchValue = this.value.trim().toLowerCase();
    const keywords = searchValue.split(' '); // Diviser en mots-clés multiples
    const rows = document.querySelectorAll('#report-table tbody tr');

    rows.forEach(row => {
        const reportName = row.cells[0].textContent.toLowerCase();
        const collectionDate = row.cells[1].textContent.toLowerCase();
        const downloadLink = row.cells[2].textContent.toLowerCase();

        // Vérifier si chaque mot-clé est présent dans au moins une des colonnes
        const isMatch = keywords.every(keyword =>
            reportName.includes(keyword) ||
            collectionDate.includes(keyword) ||
            downloadLink.includes(keyword)
        );

        // Afficher ou masquer la ligne en fonction de la correspondance
        row.style.display = isMatch ? '' : 'none';
    });
});
