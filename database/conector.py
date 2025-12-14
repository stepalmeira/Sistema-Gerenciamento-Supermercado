from typing import Any
import psycopg2
from psycopg2.extras import DictCursor
from typing import List, Dict, Any, Tuple


class DatabaseManager:
    "Classe de Gerenciamento do database"

    #Mudar nome de database, usuário e senha para o seu contexto depois de pegar do repositorio
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            dbname="supermercado_castelus",
            user="postgres",
            password='password',
            host="127.0.0.1",
            port=5432
        )
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)

    #Alguns prints para ajudar no debug
    def execute_statement(self, statement: str, params: tuple = ()) -> bool:
        """
        Executa INSERT, UPDATE, DELETE com suporte a parâmetros (%s)
        """
        try:
            # AQUI ESTAVA O ERRO: Faltava passar 'params'
            self.cursor.execute(statement, params) 
            self.conn.commit()
        except Exception as e:
            print("\n!!! ERRO NO BANCO DE DADOS !!!")
            print(f"Detalhe do erro: {e}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            self.conn.rollback()
            return False
        return True

    def execute_select_all(self, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        "Usado para SELECTS no geral"
        self.cursor.execute(query, params)
        return [dict(item) for item in self.cursor.fetchall()]

    def execute_select_one(self, query: str, params: tuple = ()):
        "Usado para SELECT com apenas uma linha de resposta, aceitando parâmetros"
        
        # O self.cursor.execute deve receber a query E os parâmetros
        self.cursor.execute(query, params) 
        
        query_result = self.cursor.fetchone()

        if not query_result:
            return None

        return dict(query_result)