document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll('.note-selection input[type="radio"]');
    const labels = document.querySelectorAll('.note-selection label');

    // Initialize stars based on the checked radio input
    function updateStars() {
        stars.forEach((star, idx) => {
            if (star.checked) {
                for (let i = 0; i <= idx; i++) {
                    labels[i].querySelector('i').classList.add('fa-solid');
                    labels[i].querySelector('i').classList.remove('fa-regular');
                }
                for (let i = idx + 1; i < labels.length; i++) {
                    labels[i].querySelector('i').classList.remove('fa-solid');
                    labels[i].querySelector('i').classList.add('fa-regular');
                }
            }
        });
    }

    updateStars(); // Initialize on page load

    // Hover effect for highlighting stars
    labels.forEach((label, index) => {
        label.addEventListener('mouseover', () => {
            // Make all stars up to the hovered one gold
            for (let i = 0; i <= index; i++) {
                labels[i].querySelector('i').classList.add('fa-solid');
                labels[i].querySelector('i').classList.remove('fa-regular');
            }
            // Stars after the hovered one should be gray
            for (let i = index + 1; i < labels.length; i++) {
                labels[i].querySelector('i').classList.remove('fa-solid');
                labels[i].querySelector('i').classList.add('fa-regular');
            }
        });

        label.addEventListener('mouseout', updateStars);

        label.addEventListener('click', () => {
            // Set the checked state to the selected star
            stars.forEach((star, idx) => {
                star.checked = idx === index;
            });
            updateStars(); // Update based on the new selected star
        });
    });
});