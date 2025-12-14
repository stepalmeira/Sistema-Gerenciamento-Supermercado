from flask import Flask, Blueprint, request, jsonify
from servicos.produto import ProdutoDatabase

app = Flask(__name__)

produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/produto', methods=['GET'])
def get_produto_por_codigo():
    codigo = request.args.get('codigo')
    if not codigo:
        return jsonify({"erro": "Código do produto é obrigatório"}), 400

    db = ProdutoDatabase()
    produto = db.get_produto_by_cod_barras(codigo)

    if produto:
        response_data = {
            # Use .get() para acessar as chaves do dicionário retornado pelo DatabaseManager
            "nome": produto.get('nome'), 
            "preco_venda": float(produto.get('preco_venda')),
            "tipo_produto": produto.get('tipo_produto'),
            "estoque_minimo": produto.get('estoque_minimo') 
        }
        return jsonify(response_data), 200
    else:
        return jsonify({"erro": "Produto não encontrado"}), 404
    
@produto_bp.route('/produto/validade', methods=['GET'])
def get_produtos_validade():
    # Pega o número de dias do parâmetro de query, ou usa 30 como padrão
    dias_str = request.args.get('dias', '30') 
    
    try:
        dias = int(dias_str)
        if dias <= 0:
            return jsonify({"erro": "O número de dias deve ser positivo."}), 400
    except ValueError:
        return jsonify({"erro": "O parâmetro 'dias' deve ser um número inteiro."}), 400
    
    produto_db = ProdutoDatabase()
    
    # Chama o novo método do serviço
    produtos = produto_db.get_produtos_proxima_validade(dias)

    if produtos:
        # A rota retorna uma lista de dicionários
        return jsonify(produtos), 200
    else:
        return jsonify({"mensagem": f"Nenhum produto vence nos próximos {dias} dias."}), 200


@produto_bp.route('/produto/em_falta', methods=['GET'])
def get_produtos_em_falta():
    
    produto_db = ProdutoDatabase()
    
    # Chama o novo método do serviço
    produtos = produto_db.get_produtos_em_falta()

    if produtos:
        # A rota retorna a lista de dicionários
        return jsonify(produtos), 200
    else:
        return jsonify({"mensagem": "Nenhum produto está abaixo do estoque mínimo definido."}), 200



# --- Quantidade de unidades de um produto em estoque ---
@produto_bp.route('/produto/em_estoque', methods=['GET'])
def get_produtos_em_estoque():

    produto_db = ProdutoDatabase()
    
    descricao = request.args.get('descricao')
    categoria = request.args.get('categoria')
    
    if descricao:
        # Busca por descrição
        produtos = produto_db.get_produtos_em_estoque_por_descricao(descricao)
        if produtos:
            return jsonify(produtos), 200
        return jsonify({"erro": "Nenhum produto encontrado com essa descrição."}), 404

    elif categoria:
        # Busca por categoria
        produtos = produto_db.get_produtos_em_estoque_por_categoria(categoria)
        if produtos:
            return jsonify(produtos), 200
        return jsonify({"erro": f"Nenhum produto encontrado na categoria: {categoria}."}), 404

    return jsonify({"erro": "É necessário fornecer uma descrição ou categoria."}), 400


@produto_bp.route('/produto/categorias', methods=['GET'])
def get_categorias():
    db = ProdutoDatabase()
    categorias = db.get_todas_categorias()
    return jsonify(categorias), 200


@produto_bp.route('/produto', methods=['POST'])
def criar_produto():
    dados = request.get_json()
    
    # Validação básica
    if not all(k in dados for k in ['cod_barras', 'nome', 'tipo_produto', 'preco_venda', 'estoque_minimo']):
        return jsonify({"erro": "Campos obrigatórios faltando."}), 400
    
    db = ProdutoDatabase()
    if db.criar_produto(dados):
        return jsonify({"mensagem": "Produto criado com sucesso!"}), 201
    return jsonify({"erro": "Erro ao criar produto."}), 500

   