document.addEventListener('DOMContentLoaded', () => {
    verificarAcesso();
    ativarLinkAtual();
});

function verificarAcesso() {
    const user = JSON.parse(localStorage.getItem('usuario'));

    // Se não estiver logado e não for a tela de login (/), chuta pra fora
    if (!user && window.location.pathname !== '/') {
        window.location.href = '/';
        return;
    }

    if (!user) return; // Se estiver na tela de login, não faz nada

    const cargo = user.cargo;
    console.log("Usuário:", user.nome, "| Cargo:", cargo);

    // --- REGRAS DE VISUALIZAÇÃO ---
    
    // 1. Diretor Financeiro: Vê APENAS Home (Dashboard) e Histórico de vendas
    if (cargo === 'Diretor Financeiro') {
        esconder('menu-vendas');
        esconder('menu-estoque');
        esconder('menu-funcionarios');
    }
    
    // 2. Operador de Caixa: Vê APENAS Vendas
    else if (cargo === 'Operador de Caixa') {
        esconder('menu-home');
        esconder('menu-estoque');
        esconder('menu-historico');
        esconder('menu-funcionarios');
    }

    // 3. Diretor Geral: Vê TUDO (Não escondemos nada)
    
    // 4. Outros (Gerente, etc): Definir regras se precisar
}

function esconder(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
}

function ativarLinkAtual() {
    const path = window.location.pathname;
    const links = document.querySelectorAll('.nav-links a');

    links.forEach(link => {
        if (path.includes(link.getAttribute('href'))) {
            link.parentElement.classList.add('active'); // Adiciona classe ao LI
            link.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
            link.style.borderRadius = '8px';
        }
    });
}

function logout() {
    localStorage.removeItem('usuario');
    window.location.href = '/';
}