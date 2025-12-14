from database.conector import DatabaseManager
import datetime

class RelatoriosDatabase:
    def __init__(self, db_provider = None):
        self.db = db_provider or DatabaseManager()

    def get_balanco_financeiro_mensal(self, ano: int, mes: int):
        query = """
            SELECT
                (SELECT COALESCE(SUM(l.quantidade * l.preco_compra), 0) 
                 FROM Lote l 
                 WHERE EXTRACT(YEAR FROM l.data_recebimento) = %s AND EXTRACT(MONTH FROM l.data_recebimento) = %s
                ) AS total_custos,
                (SELECT COALESCE(SUM(v.valor_total), 0) 
                 FROM Venda v 
                 WHERE EXTRACT(YEAR FROM v.data_venda) = %s AND EXTRACT(MONTH FROM v.data_venda) = %s
                ) AS total_faturamento;
        """
        return self.db.execute_select_one(query, (ano, mes, ano, mes))

    def get_historico_anual(self):
        hoje = datetime.date.today()
        historico = []
        
        for i in range(6):
            mes_calc = hoje.month - i
            ano_calc = hoje.year
            if mes_calc <= 0:
                mes_calc += 12
                ano_calc -= 1
            
            dados = self.get_balanco_financeiro_mensal(ano_calc, mes_calc)
            faturamento = float(dados['total_faturamento'])
            custos = float(dados['total_custos'])
            
            historico.append({
                "mes": f"{mes_calc}/{ano_calc}",
                "faturamento": faturamento,
                "custos": custos,
                "lucro": faturamento - custos
            })
        return historico

    def get_todos_lotes(self):
        query = """
            SELECT p.cod_barras, l.cod_lote, p.nome as produto, f.nome_fornecedor, l.quantidade, l.data_validade
            FROM Lote l
            JOIN Produto p ON l.cod_produto = p.cod_barras
            JOIN Fornecedor f ON l.cod_fornecedor = f.cod_fornecedor
            ORDER BY l.data_recebimento DESC;
        """
        return self.db.execute_select_all(query)

    def deletar_lote(self, cod_lote):
        return self.db.execute_statement("DELETE FROM Lote WHERE cod_lote = %s", (cod_lote,))

    def get_funcionario_por_cpf(self, cpf):
        query = """
            SELECT f.nome_completo, f.cargo, s.nome_setor as setor, f.salario, f.cpf 
            FROM Funcionario f
            JOIN Setor s ON f.cod_setor = s.cod_setor
            WHERE f.cpf = %s
        """
        return self.db.execute_select_one(query, (cpf,))

    def criar_funcionario(self, dados):
        query = "INSERT INTO Funcionario (cpf, nome_completo, cod_setor, cargo, genero, endereco, salario) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        params = (dados['cpf'], dados['nome_completo'], dados['cod_setor'], dados['cargo'], dados['genero'], dados['endereco'], dados['salario'])
        return self.db.execute_statement(query, params)

    def deletar_funcionario(self, cpf):
        self.db.execute_statement("DELETE FROM Usuario WHERE cpf_funcionario = %s", (cpf,))
        return self.db.execute_statement("DELETE FROM Funcionario WHERE cpf = %s", (cpf,))
    
    def get_funcionarios_por_setor(self, nome_setor):
        query = """
            SELECT f.cpf, f.nome_completo, f.cargo, s.nome_setor as setor, f.salario
            FROM Funcionario f
            JOIN Setor s ON f.cod_setor = s.cod_setor
            WHERE s.nome_setor ILIKE %s
            ORDER BY f.nome_completo ASC
        """
        return self.db.execute_select_all(query, (f'%{nome_setor}%',))
    
    def get_historico_vendas_por_periodo(self, data_inicio=None, data_fim=None):
        """
        Se data_inicio/data_fim forem None retorna todas as vendas.
        Espera strings 'YYYY-MM-DD' ou objetos date/datetime.
        """
        query = """
            SELECT
                ven.cod_venda, ven.data_venda, fun.nome_completo, ven.valor_total, ven.forma_pagamento, ven.qntd_parcelas
            FROM
                venda ven
            JOIN
                funcionario fun
            ON
                ven.cpf_funcionario = fun.cpf
        """
        params = []
        if data_inicio and data_fim:
            query += " WHERE ven.data_venda BETWEEN %s AND %s"
            params = (data_inicio, data_fim)
        elif data_inicio:
            query += " WHERE ven.data_venda >= %s"
            params = (data_inicio,)
        elif data_fim:
            query += " WHERE ven.data_venda <= %s"
            params = (data_fim,)

        query += " ORDER BY ven.data_venda DESC;"
        return self.db.execute_select_all(query, params)