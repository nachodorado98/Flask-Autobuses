document.addEventListener('DOMContentLoaded', function() {
    var toggleNavbarBtn = document.getElementById('toggle-navbar');
    var navbar = document.getElementById('navbar');

    toggleNavbarBtn.addEventListener('click', function() {
        navbar.style.display = (navbar.style.display === 'block') ? 'none' : 'block';
    });
});
