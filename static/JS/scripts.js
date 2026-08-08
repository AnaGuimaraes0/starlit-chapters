function toggleUserMenu(btn) {
    const wrapper = btn.closest('.user-avatar-menu');
    if (!wrapper) return;

    const isOpen = wrapper.classList.toggle('open');
    btn.setAttribute('aria-expanded', isOpen);
}

document.addEventListener('DOMContentLoaded', function() {
    // Inicia os ícones padrão (como estrelas e livros)
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Monitora a rolagem da página para mudar o fundo do Navbar
    const nav = document.querySelector('nav');

    if (nav) {
        const handleScroll = function() {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        };

        handleScroll();
        window.addEventListener('scroll', handleScroll);
    }

    document.addEventListener('click', function (e) {
        document.querySelectorAll('.user-avatar-menu.open').forEach(function (wrapper) {
            if (!wrapper.contains(e.target)) {
                wrapper.classList.remove('open');
                const avatarBtn = wrapper.querySelector('.nav-user-avatar-btn');
                if (avatarBtn) {
                    avatarBtn.setAttribute('aria-expanded', 'false');
                }
            }
        });
    });
});