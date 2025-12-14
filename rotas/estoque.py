from flask import Flask, Blueprint, request, jsonify
from servicos.estoque import EstoqueDatabase

estoque_bp = Blueprint('estoque', __name__)

# --- FORNECEDOR ---
@estoque_bp.route('/fornecedores', methods=['GET'])
def get_fornecedores():
    db = EstoqueDatabase()
    fornecedores = db.get_todos_fornecedores()
    return jsonify(fornecedores)

@estoque_bp.route('/fornecedor', methods=['POST'])
def criar_fornecedor():
    dados = request.get_json()
    if 'nome_fornecedor' not in dados or 'data_contratacao' not in dados:
        return jsonify({"erro": "Campos obrigatórios faltando."}), 400

    if EstoqueDatabase().criar_fornecedor(dados):
        return jsonify({"mensagem": "Fornecedor criado!"}), 201
    return jsonify({"erro": "Erro ao criar fornecedor."}), 500

#Pra mostrar que não é possível deletar Fornecedor
@estoque_bp.route('/fornecedor', methods=['DELETE'])
def deletar_fornecedor():
    # Ex: /fornecedor?cod_fornecedor=10
    cod = request.args.get('cod_fornecedor')
    if not cod:
        return jsonify({"erro": "cod_fornecedor é obrigatório."}), 400

    if EstoqueDatabase().deletar_fornecedor(cod):
        return jsonify({"mensagem": f"Fornecedor {cod} removido com sucesso!"}), 200
    else:
        return jsonify({"erro": "Erro ao remover. Verifique se existem LOTES vinculados a este fornecedor."}), 500

# --- LOTE ---
@estoque_bp.route('/lote', methods=['POST'])
def criar_lote():
    dados = request.get_json()
    campos_obrigatorios = ['quantidade', 'nome_fornecedor', 'cod_produto', 'preco_compra', 'data_recebimento', 'data_validade']
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Campos obrigatórios faltando."}), 400

    if EstoqueDatabase().criar_lote(dados):
        return jsonify({"mensagem": "Lote criado!"}), 201
    return jsonify({"erro": "Erro ao criar lote."}), 500