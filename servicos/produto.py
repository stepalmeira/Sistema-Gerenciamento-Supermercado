from database.conector import DatabaseManager

class ProdutoDatabase:

    def __init__(self, db_provider = None):
        # Avoid creating a DB connection at import time by lazy-initializing
        self.db = db_provider or DatabaseManager()

    def get_produto_by_cod_barras(self, cod_barras):

        query = "SELECT nome, preco_venda, tipo_produto, estoque_minimo FROM produto WHERE cod_barras = %s;"
        result = self.db.execute_select_one(query, (cod_barras,))
        return result
    
    def get_produtos_proxima_validade(self, dias=30):
        """
        Lista produtos que vencerão nos próximos 'dias'.
        Retorna: lista de dicionários.
        """
        query = """
            SELECT 
                p.nome AS produto_nome, 
                l.cod_lote, 
                l.data_validade
            FROM 
                Lote l
            JOIN 
                Produto p ON l.cod_produto = p.cod_barras
            WHERE 
                l.data_validade BETWEEN current_date AND current_date + interval '%s days'
            ORDER BY 
                l.data_validade ASC;
        """
        # Passamos a variável 'dias' como tupla de parâmetros
        return self.db.execute_select_all(query, (dias,))
    
    def get_produtos_em_falta(self):
        """
        Calcula o estoque atual (Entradas - Saídas) e lista produtos 
        cujo estoque atual é menor que o estoque_minimo.
        """
        query = """
            SELECT
                p.nome, 
                p.cod_barras,
                p.estoque_minimo,
                -- COALESCE garante que, se não houver registros (entrada ou saída), o valor seja 0
                (COALESCE(SUM(l.quantidade), 0) - COALESCE(SUM(vcp.quantidade), 0)) AS estoque_atual
            FROM 
                Produto p
            LEFT JOIN 
                Lote l ON p.cod_barras = l.cod_produto        -- Entradas
            LEFT JOIN 
                Venda_Contem_Produto vcp ON p.cod_barras = vcp.cod_barras -- Saídas
            GROUP BY 
                p.cod_barras, p.nome, p.estoque_minimo
            HAVING 
                (COALESCE(SUM(l.quantidade), 0) - COALESCE(SUM(vcp.quantidade), 0)) < p.estoque_minimo
            ORDER BY 
                estoque_atual ASC;
        """
        # Esta consulta não tem parâmetros dinâmicos, então passamos uma tupla vazia.
        return self.db.execute_select_all(query, ())
    

    # teste stefanie 
    def get_produtos_em_estoque_por_descricao(self, descricao):
        """
        Busca por nome do produto e retorna todos os produtos com aqueles
        termos no nome e suas quantidades em estoque
        """
        query = """
            SELECT
                p.cod_barras,
                p.nome,
                p.tipo_produto,
                p.estoque_minimo,
                (COALESCE(entradas.total_comprado, 0) - COALESCE(saidas.total_vendido, 0)) AS "qtd_em_estoque"
            FROM
                Produto p
            LEFT JOIN (
                SELECT cod_produto, SUM(quantidade) as total_comprado
                FROM Lote
                GROUP BY cod_produto
            ) entradas ON p.cod_barras = entradas.cod_produto
            LEFT JOIN (
                SELECT cod_barras, SUM(quantidade) as total_vendido
                FROM Venda_Contem_Produto
                GROUP BY cod_barras
            ) saidas ON p.cod_barras = saidas.cod_barras
            -- 3. Filtro de busca
            WHERE
                p.nome ILIKE %s
        """
        return self.db.execute_select_all(query, (f'%{descricao}%',))


    def get_produtos_em_estoque_por_categoria(self, categoria):
        """
        Busca pela categoria de produtos e retorna todos os produtos  dentro
        daquela categoria e suas quantidades em estoque
        """
        query = """
            SELECT
                p.cod_barras,
                p.nome,
                p.tipo_produto,
                p.estoque_minimo,
                (COALESCE(entradas.total_comprado, 0) - COALESCE(saidas.total_vendido, 0)) AS "qtd_em_estoque"
            FROM
                Produto p
            LEFT JOIN (
                SELECT cod_produto, SUM(quantidade) as total_comprado
                FROM Lote
                GROUP BY cod_produto
            ) entradas ON p.cod_barras = entradas.cod_produto
            LEFT JOIN (
                SELECT cod_barras, SUM(quantidade) as total_vendido
                FROM Venda_Contem_Produto
                GROUP BY cod_barras
            ) saidas ON p.cod_barras = saidas.cod_barras
            -- 3. Filtro de busca
            WHERE
                p.tipo_produto ILIKE %s
        """
        return self.db.execute_select_all(query, (f'%{categoria}%',))

    def get_todas_categorias(self):
        """
        Retorna lista de todas as categorias (tipo_produto) disponíveis.
        """
        query = "SELECT DISTINCT tipo_produto FROM Produto ORDER BY tipo_produto ASC;"
        return self.db.execute_select_all(query, ())
    

    def criar_produto(self, dados):
        """
        Insere um novo produto na tabela Produto.
        """
        query = """
            INSERT INTO Produto (cod_barras, nome, tipo_produto, preco_venda, estoque_minimo)
            VALUES (%s, %s, %s, %s, %s);
        """
        params = (
            dados['cod_barras'],
            dados['nome'],
            dados['tipo_produto'],
            dados['preco_venda'],
            dados['estoque_minimo']
        )
        return self.db.execute_statement(query, params)