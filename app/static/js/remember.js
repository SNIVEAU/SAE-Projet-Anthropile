document.addEventListener('DOMContentLoaded', function () {
    const rememberCheckbox = document.getElementById('remember');
    let activate = localStorage.getItem('rememberMe') === 'true';

    if (rememberCheckbox) {
        rememberCheckbox.checked = activate;

        rememberCheckbox.addEventListener('change', function () {
            activate = rememberCheckbox.checked;
            localStorage.setItem('rememberMe', activate);
        });
    }

    const userNameElement = document.getElementById('user-name');
    let connected = userNameElement ? true : false;
    let isNavigatingAway = false;

    function isconnected() { return connected; }
    function isactivated() { return activate; }

    document.querySelectorAll('a, button').forEach(element => {
        element.addEventListener('click', () => { isNavigatingAway = true; });
    });

    window.addEventListener('beforeunload', function () {
        const navigationType = performance.getEntriesByType("navigation")[0]?.type;

        if (navigationType === "reload") return;

        if (!isNavigatingAway && !isactivated() && isconnected()) {
            fetch('/logout', { method: 'POST', keepalive: true });
        }
    });

    window.addEventListener('unload', function () {
        const navigationType = performance.getEntriesByType("navigation")[0]?.type;

        if (navigationType === "reload") return;

        if (!isNavigatingAway && !isactivated() && isconnected()) {
            fetch('/logout', { method: 'POST', keepalive: true });
        }
    });
});
