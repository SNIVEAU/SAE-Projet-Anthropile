const track = document.querySelector('.carousel-track');
const slides = Array.from(track.children);
const slideWidth = slides[0].getBoundingClientRect().width + 20; // largeur d'une slide + espace
let currentIndex = 0;

function moveSlides(n) {
    currentIndex = (currentIndex + n + slides.length) % slides.length;
    track.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
}

setInterval(() => moveSlides(2), 5000); // Défilement automatique
