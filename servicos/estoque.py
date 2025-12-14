from database.conector import DatabaseManager

class EstoqueDatabase:
    def __init__(self, db_provider = None):
        self.db = db_provider or DatabaseManager()

    def criar_fornecedor(self, dados):
        """
        Insere um fornecedor.
        Se 'cod_fornecedor' for enviado, usa ele. Se não, deixa o banco gerar (SERIAL).
        """
        if 'cod_fornecedor' in dados:
            query = """
                INSERT INTO Fornecedor (cod_fornecedor, nome_fornecedor, data_contratacao)
                VALUES (%s, %s, %s);
            """
            params = (dados['cod_fornecedor'], dados['nome_fornecedor'], dados['data_contratacao'])
        else:
            query = """
                INSERT INTO Fornecedor (nome_fornecedor, data_contratacao)
                VALUES (%s, %s);
            """
            params = (dados['nome_fornecedor'], dados['data_contratacao'])
            
        return self.db.execute_statement(query, params)

    def criar_lote(self, dados):
        """
        Insere um lote de compra.
        """
        query = """
            INSERT INTO Lote (quantidade, nome_fornecedor, cod_produto, preco_compra, data_recebimento, data_validade)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        params = (
            dados['quantidade'],
            # dados['cod_fornecedor'],
            dados['nome_fornecedor'],
            dados['cod_produto'],
            dados['preco_compra'],
            dados['data_recebimento'],
            dados['data_validade']
        )
        return self.db.execute_statement(query, params)
    
        # --- DELETAR ---#Pra mostrar que não é possível deletar Fornecedor

    def deletar_fornecedor(self, cod_fornecedor: int):
        """
        Remove um fornecedor pelo código.
        """
        query = "DELETE FROM Fornecedor WHERE cod_fornecedor = %s;"
        return self.db.execute_statement(query, (cod_fornecedor,))
    
    def get_todos_fornecedores(self):
        """
        Retorna lista de todos os fornecedores com cod_fornecedor e nome_fornecedor.
        """
        query = """
                    SELECT
                        cod_fornecedor, nome_fornecedor
                    FROM
                        Fornecedor
                    ORDER BY
                        nome_fornecedor ASC;
                """
        return self.db.execute_select_all(query)