// Scroll to top button
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.addEventListener('scroll', function () {
    const scrollToTopButton = document.querySelector('.scroll-to-top');
    if (window.scrollY > 200) {
        scrollToTopButton.classList.remove('hidden');
    } else {
        scrollToTopButton.classList.add('hidden');
    }
});