from flask import Flask, Blueprint, request, jsonify
from servicos.auth import AuthDatabase

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    
    if not dados or 'login' not in dados or 'senha' not in dados:
        return jsonify({"erro": "Login e senha são obrigatórios"}), 400

    db = AuthDatabase()
    usuario = db.autenticar_usuario(dados['login'], dados['senha'])

    if usuario:
        # Retorna sucesso e os dados do usuário para o frontend salvar
        return jsonify({
            "mensagem": "Autenticado com sucesso",
            "usuario": {
                "nome": usuario['nome_completo'],
                "cargo": usuario['cargo'],
                "login": usuario['login'],
                "setor": usuario['cod_setor']
            }
        }), 200
    else:
        return jsonify({"erro": "Usuário ou senha inválidos"}), 401