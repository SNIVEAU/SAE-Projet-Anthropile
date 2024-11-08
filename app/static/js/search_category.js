document.getElementById('search-input').addEventListener('input', function () {
    const searchValue = this.value.trim().toLowerCase();
    const rows = document.querySelectorAll('table tbody tr');

    rows.forEach(row => {
        const categoryName = row.cells[1].textContent.toLowerCase();
        const isMatch = categoryName.includes(searchValue);
        row.style.display = isMatch ? '' : 'none';
    });
});
