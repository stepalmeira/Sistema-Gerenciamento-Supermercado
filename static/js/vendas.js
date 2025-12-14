// Variáveis de Estado
let carrinho = [];
let totalVenda = 0.0;

// Foca no scanner ao abrir a página
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('barcode');
    if(input) input.focus();
});

// --- FUNÇÃO PRINCIPAL: ADICIONAR PRODUTO ---
async function addProduct() {
    const input = document.getElementById('barcode');
    const codigo = input.value;

    if (!codigo) return alert("Digite ou escaneie um código!");

    try {
        // Busca no seu Backend
        const res = await fetch(`http://127.0.0.1:8000/produto?codigo=${codigo}`);
        
        if (res.ok) {
            const produto = await res.json();
            adicionarAoCarrinho(produto);
            
            input.value = ''; // Limpa campo
            input.focus();    // Foca para o próximo
        } else {
            alert("Produto não encontrado!");
            input.select(); 
        }
    } catch (erro) {
        console.error(erro);
        alert("Erro de conexão com o servidor.");
    }
}

// --- FUNÇÃO AUXILIAR: ATUALIZAR TELA E MEMÓRIA ---
function adicionarAoCarrinho(produto) {
    const codigoProduto = produto.cod_barras || document.getElementById('barcode').value;

    // 1. VERIFICA SE O PRODUTO JÁ EXISTE NO CARRINHO
    // Essa é a correção principal: procuramos o item antes de adicionar
    const itemExistente = carrinho.find(item => item.cod_produto === codigoProduto);

    if (itemExistente) {
        // Se já existe, apenas aumenta a quantidade
        itemExistente.quantidade += 1;
    } else {
        // Se não existe, adiciona um novo item
        carrinho.push({
            cod_produto: codigoProduto,
            nome: produto.nome,
            preco: produto.preco_venda,
            quantidade: 1
        });
    }

    // 2. RE-RENDERIZA A LISTA (Para mostrar as quantidades certas)
    renderizarLista();
    atualizarTotal();
}

// Função para desenhar a lista visualmente
function renderizarLista() {
    const lista = document.getElementById('saleList');
    lista.innerHTML = ''; // Limpa a lista visual para recriar atualizada

    if (carrinho.length === 0) {
        lista.innerHTML = '<div class="empty" style="text-align:center; color:#ccc; padding-top:50px;">Carrinho Vazio</div>';
        return;
    }

    carrinho.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.style.cssText = "display:flex; justify-content:space-between; align-items:center; padding:10px; border-bottom:1px solid #eee; background:#fff; margin-bottom:5px; border-radius:5px;";
        
        // Calcula o subtotal deste item (Preço x Quantidade)
        const subtotal = item.preco * item.quantidade;
        
        itemDiv.innerHTML = `
            <div style="display:flex; flex-direction:column;">
                <span style="font-weight:500">${item.nome}</span>
                <span style="font-size:13px; color:#666">
                    ${item.quantidade}x R$ ${item.preco.toFixed(2)}
                </span>
            </div>
            <strong style="color:#27ae60; font-size: 1.1em;">R$ ${subtotal.toFixed(2)}</strong>
        `;
        lista.appendChild(itemDiv);
    });

    lista.scrollTop = lista.scrollHeight; // Rola para o final para ver o último item
}

// --- ATUALIZA TOTAL GERAL ---
function atualizarTotal() {
    totalVenda = carrinho.reduce((acc, item) => acc + (item.preco * item.quantidade), 0);
    document.getElementById('total-venda').innerText = `R$ ${totalVenda.toFixed(2)}`;
}

// --- FUNÇÃO FINAL: FECHAR COMPRA ---
async function finalizarVenda() {
    if (carrinho.length === 0) return alert("Carrinho vazio!");

    const pgto = prompt("Forma de Pagamento (Dinheiro, Crédito, Débito):", "Dinheiro");
    if (!pgto) return; 

    const user = JSON.parse(localStorage.getItem('usuario'));
    const cpfFuncionario = (user && user.cpf_funcionario) ? user.cpf_funcionario : "11223344556"; 

    // CORREÇÃO AQUI: Gerar um ID numérico seguro para INT (Max 2 Bilhões)
    // Usamos Math.floor(Math.random() * 1000000) para gerar um ID aleatório até 1 milhão
    const codigoVendaNumerico = Math.floor(Math.random() * 100000000);

    const vendaJSON = {
        data_venda: new Date().toISOString(),
        cpf_funcionario: cpfFuncionario, 
        valor_total: totalVenda,
        forma_pagamento: pgto,
        parcelas: 1,
        desconto: 0,
        itens: carrinho.map(item => ({
            cod_produto: item.cod_produto,
            quantidade: item.quantidade
        }))
    };

    console.log("Enviando venda:", vendaJSON);

    try {
        const res = await fetch('http://127.0.0.1:8000/venda', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(vendaJSON)
        });

        if (res.ok) {
            // 1. Pegamos a resposta do servidor
            const resposta = await res.json();
            
            // 2. Mostramos o ID real que veio do banco
            alert(`✅ Venda ${resposta.codigo_venda} realizada com sucesso!`);
            
            window.location.reload();
        } else {
            const erro = await res.json();
            alert("Erro: " + erro.erro);
        }
    } catch (e) {
        alert("Erro fatal ao enviar venda.");
        console.error(e);
    }
}

// Atalhos
document.getElementById('barcode').addEventListener('keypress', (e) => {
    if(e.key === 'Enter') addProduct();
});
document.addEventListener('keydown', (e) => {
    if(e.key === 'F9') finalizarVenda();
});