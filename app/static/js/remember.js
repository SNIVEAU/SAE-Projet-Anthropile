document.addEventListener('DOMContentLoaded', function () {
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function () {
            if (confirm("Voulez-vous vraiment vous déconnecter ?")) {
                window.location.href = "{{ url_for('logout') }}";
            }
        });
    }
});

// Ouvrir/fermer le menu au clic
document.querySelector('.menu-toggle').addEventListener('click', function() {
    const menu = document.querySelector('nav.menu');
    menu.classList.toggle('active');
});

// Fermer le menu si on clique sur la croix
document.querySelector('.close-menu').addEventListener('click', function() {
    const menu = document.querySelector('nav.menu');
    menu.classList.remove('active');
});

// Fermer le menu si on clique en dehors
document.addEventListener('click', function(event) {
    const menu = document.querySelector('nav.menu');
    const menuToggle = document.querySelector('.menu-toggle');

    if (!menu.contains(event.target) && !menuToggle.contains(event.target)) {
        menu.classList.remove('active');
    }
});
document.addEventListener('DOMContentLoaded', function () {
    const rememberCheckbox = document.getElementById('remember');

    // Restaurez l'état de 'activate' depuis le localStorage si disponible
    let activate = localStorage.getItem('rememberMe') === 'true';
    if (rememberCheckbox) {
        // Applique l'état stocké dans localStorage à la checkbox
        rememberCheckbox.checked = activate;

        // Mettre à jour la variable 'activate' et stocker dans localStorage lorsque la checkbox change
        rememberCheckbox.addEventListener('change', function () {
            activate = rememberCheckbox.checked;
            localStorage.setItem('rememberMe', activate);  // Stocke l'état dans localStorage
            console.log("Remember me status:", activate ? "activated" : "deactivated");
        });
    } else {
        console.warn("Remember checkbox not found");
    }
    

    let isNavigatingAway = false;

    // Fonction pour vérifier l'état de 'activate'
    function isactivated() {
        return activate;
    }

    // Fonction pour gérer le clic sur les liens
    function handleLinkClick() {
        isNavigatingAway = true;
    }

    // Ajouter un écouteur d'événement pour tous les liens de navigation
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', handleLinkClick);
    });
    

    // Détecter les événements de rechargement et de fermeture de page
    window.addEventListener("beforeunload", function (event) {
        // Si l'utilisateur quitte la page sans avoir cliqué sur un lien et sans activer "Se souvenir de moi"
        if (!isNavigatingAway && !isactivated()) {
            navigator.sendBeacon("/logout"); // Envoie une requête de déconnexion
        }
        
    });
});
