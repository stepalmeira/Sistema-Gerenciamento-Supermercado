from database.conector import DatabaseManager

class AuthDatabase:
    def __init__(self, db_provider = None):
        self.db = db_provider or DatabaseManager()

    def autenticar_usuario(self, login, senha):
        """
        Verifica login e senha. 
        Se correto, retorna os dados do funcionário (Nome e Cargo).
        """
        # Fazemos um JOIN para pegar o cargo direto da tabela Funcionario
        query = """
            SELECT 
                u.login,
                f.nome_completo,
                f.cargo,
                f.cpf,
                f.cod_setor
            FROM 
                Usuario u
            JOIN 
                Funcionario f ON u.cpf_funcionario = f.cpf
            WHERE 
                u.login = %s AND u.senha = %s;
        """
        return self.db.execute_select_one(query, (login, senha))