from database.conector import DatabaseManager

class VendaDatabase:
    def __init__(self, db_provider = None):
        self.db = db_provider or DatabaseManager()

    def registrar_venda(self, dados_venda):
        """
        Registra a venda deixando o Banco de Dados gerar o ID (Serial).
        """
        try:
            query_venda = """
                INSERT INTO Venda (
                    data_venda, 
                    cpf_funcionario, 
                    valor_total, 
                    forma_pagamento, 
                    qntd_parcelas,   
                    valor_desconto   
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING cod_venda;
            """
            
            params_venda = (    
                dados_venda['data_venda'],
                dados_venda['cpf_funcionario'],
                dados_venda['valor_total'],
                dados_venda['forma_pagamento'],
                dados_venda['parcelas'],    
                dados_venda.get('desconto', 0) 
            )
            
            self.db.cursor.execute(query_venda, params_venda)
           
            cod_venda_gerado = self.db.cursor.fetchone()[0]
            
            query_item = """
                INSERT INTO Venda_Contem_Produto (
                    cod_venda, 
                    cod_barras, 
                    quantidade
                ) VALUES (%s, %s, %s);
            """
            
            for item in dados_venda['itens']:
                params_item = (
                    cod_venda_gerado,
                    item['cod_produto'],
                    item['quantidade']
                )
                self.db.cursor.execute(query_item, params_item)

            self.db.conn.commit()
            print(f"Venda {cod_venda_gerado} registrada com sucesso!")
            return True

        # except Exception as e:
        #     # Se der qualquer erro, desfaz tudo (Rollback)
        #     self.db.conn.rollback()
        #     print(f"\n!!! ERRO AO GRAVAR VENDA !!!")
        #     print(f"Detalhe: {e}")
            
        #     self.db.conn.commit()
        #     print(f"Venda {cod_venda_gerado} registrada com sucesso!")
            
        #     # ALTERAÇÃO AQUI: Retorna o ID gerado em vez de apenas True
        #     return cod_venda_gerado 

        except Exception as e:
            self.db.conn.rollback()
            print(f"\n!!! ERRO AO GRAVAR VENDA !!!")
            print(f"Detalhe: {e}")
            return None # Retorna None em caso de erro