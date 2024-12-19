document.addEventListener('DOMContentLoaded', function () {
    // Sélectionner tous les champs focusables
    const formElements = Array.from(document.querySelectorAll('.form-control, input, textarea, select'))
        .filter(el => el.tabIndex !== -1 && typeof el.focus === 'function');
    const totalElements = formElements.length;

    // Ajouter les événements pour les touches fléchées
    formElements.forEach((element, index) => {
        element.addEventListener('keydown', function (event) {
            if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
                event.preventDefault();
                let newIndex = index;

                if (event.key === 'ArrowDown') {
                    newIndex = (index + 1) % totalElements;
                } else if (event.key === 'ArrowUp') {
                    newIndex = (index - 1 + totalElements) % totalElements;
                }

                formElements[newIndex].focus();
            }
        });
    });
});
