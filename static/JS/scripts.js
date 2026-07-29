document.addEventListener('DOMContentLoaded', function() {
    
    // Inicia os ícones padrão (como estrelas e livros)
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Monitora a rolagem da página para mudar o fundo do Navbar
    const nav = document.querySelector('nav');
    
    if (nav) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });
    }
});