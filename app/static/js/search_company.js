document.getElementById('search-input').addEventListener('input', function () {
    const searchValue = this.value.trim().toLowerCase();
    const rows = document.querySelectorAll('#company-table tbody tr');

    rows.forEach(row => {
        const companyName = row.cells[1].textContent.toLowerCase();
        const isMatch = companyName.includes(searchValue);
        row.style.display = isMatch ? '' : 'none';
    });
});
