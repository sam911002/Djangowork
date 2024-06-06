window.addEventListener('scroll', function() {
    var header = document.querySelector('.header');
    if (window.scrollY > 0) {
        header.classList.add('transparent');
    } else {
        header.classList.remove('transparent');
    }
});