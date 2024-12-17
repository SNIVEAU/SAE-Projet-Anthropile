document.addEventListener('DOMContentLoaded', function () {
    const rememberCheckbox = document.getElementById('remember');
    const userNameElement = document.getElementById('user-name');
    let isNavigatingAway = false;

    // Initialize "Remember Me" state
    const activate = localStorage.getItem('rememberMe') === 'true';
    if (rememberCheckbox) {
        rememberCheckbox.checked = activate;
        rememberCheckbox.addEventListener('change', function () {
            localStorage.setItem('rememberMe', rememberCheckbox.checked);
        });
    }

    // Check if user is connected
    const connected = !!userNameElement;

    // Event listeners for navigation
    const links = document.querySelectorAll('a');
    if (links.length > 0) {
        links.forEach(link => {
            link.addEventListener('click', () => {
                isNavigatingAway = true;
            });
        });
    }

    // Store a temporary state in sessionStorage before reload or navigation
    window.addEventListener("beforeunload", function (event) {
        // Check if the browser supports performance navigation entries
        const isReload = sessionStorage.getItem('isReloading') === 'true';

        if (!isNavigatingAway && !isReload && !rememberCheckbox?.checked && connected) {
            // Trigger logout only if not navigating or reloading
            fetch('/logout', { method: 'POST', keepalive: true })
                .catch(err => console.error('Logout failed:', err));
        }

        // Indicate a reload intent in sessionStorage
        sessionStorage.setItem('isReloading', 'true');

        // Clear the reload intent after some time to handle unintended cases
        setTimeout(() => sessionStorage.removeItem('isReloading'), 500);
    });

    // Check reload status on page load
    if (sessionStorage.getItem('isReloading') === 'true') {
        console.log('Page was reloaded.');
        sessionStorage.removeItem('isReloading');
    } else {
        console.log('Normal page load or navigation from another site.');
    }
});
