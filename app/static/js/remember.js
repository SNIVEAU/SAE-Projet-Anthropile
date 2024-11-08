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

    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => { isNavigatingAway = true; });
    });

    window.addEventListener("beforeunload", function () {
        if (performance.navigation.type === performance.navigation.TYPE_RELOAD) return;

        if (!isNavigatingAway && !isactivated() && isconnected()) {
            fetch('/logout', { method: 'POST', keepalive: true });
        }
    });
});
