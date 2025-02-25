document.addEventListener("DOMContentLoaded", function () {
    const sortButton = document.getElementById("sort-by-priority");

    if (sortButton) {
        let currentPath = window.location.pathname;
        if (currentPath.endsWith("/0")) {
            sortButton.textContent = "Trier par priorité";
        } else if (currentPath.endsWith("/1")) {
            sortButton.textContent = "Trier par date";
        }

        sortButton.addEventListener("click", function () {
            let newPath;

            if (currentPath.endsWith("/0")) {
                newPath = currentPath.slice(0, -2) + "/1";
            } else if (currentPath.endsWith("/1")) {
                newPath = currentPath.slice(0, -2) + "/0";
            } else {
                newPath = currentPath + "/0";
            }

            window.location.href = newPath;
        });
    }
});
