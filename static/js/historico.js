async function filtrarVendas() {
    const inicio = document.getElementById('data-inicio').value;
    const fim = document.getElementById('data-fim').value;
    const tbody = document.getElementById('historico-body');
    tbody.innerHTML = '';

    // validação simples
    if (!inicio && !fim) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center">Escolha pelo menos uma data.</td></tr>';
        return;
    }

    const params = new URLSearchParams();
    if (inicio) params.append('inicio', inicio);
    if (fim) params.append('fim', fim);

    try {
        const res = await fetch(`/relatorios/historico_vendas?${params.toString()}`);
        const data = await res.json();
        if (!res.ok) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center">${data.erro || data.mensagem || 'Erro'}</td></tr>`;
            return;
        }
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center">Nenhuma venda encontrada</td></tr>';
            return;
        }
        data.forEach(v => {
            const dt = new Date(v.data_venda).toLocaleDateString();
            tbody.innerHTML += `
                <tr>
                    <td>${v.cod_venda}</td>
                    <td>${dt}</td>
                    <td>${v.nome_completo}</td>
                    <td>R$ ${parseFloat(v.valor_total).toFixed(2)}</td>
                    <td>${v.forma_pagamento}</td>
                    <td>${v.qntd_parcelas || ''}</td>
                </tr>
            `;
        });
    } catch (e) {
        console.error(e);
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center">Erro ao comunicar com o servidor.</td></tr>';
    }
}