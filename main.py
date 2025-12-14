# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_cors import CORS

# Importando as rotas da API (Backend)
from rotas.produto import produto_bp
from rotas.relatorios import relatorios_bp
from rotas.estoque import estoque_bp
from rotas.vendas import venda_bp
# from rotas.historico import historico_bp
from rotas.auth import auth_bp

# Inicializa a aplicação
# Como o main.py está ao lado da pasta templates e static, não precisa configurar nada extra.
app = Flask(__name__)
CORS(app)

# --- REGISTRO DAS ROTAS DA API (DADOS) ---
app.register_blueprint(produto_bp)
app.register_blueprint(relatorios_bp)
app.register_blueprint(estoque_bp)
app.register_blueprint(venda_bp)
# app.register_blueprint(historico_bp)
app.register_blueprint(auth_bp)

# --- ROTAS DAS PÁGINAS (TELAS) ---

# 1. Tela de Login (Raiz)
@app.route('/')
def root():
    # Busca o arquivo em: templates/index.html
    return render_template('index.html')

# 2. Dashboard
@app.route('/pagina/home') 
def pagina_home():
    # Busca o arquivo em: templates/home.html
    return render_template('home.html')

# 3. Frente de Caixa
@app.route('/pagina/vendas')
def pagina_vendas():
    # Busca o arquivo em: templates/vendas.html
    return render_template('vendas.html')

# 4. Histórico de vendas
@app.route('/pagina/historico')
def pagina_historico():
    # Busca o arquivo em: templates/historico.html
    return render_template('historico.html')

# 5. Controle de Estoque
@app.route('/pagina/estoque')
def pagina_estoque():
    # Busca o arquivo em: templates/estoque.html
    return render_template('estoque.html')

# 6. Gestão de Funcionários
@app.route('/pagina/funcionarios')
def pagina_funcionarios():
    # Busca o arquivo em: templates/funcionarios.html
    return render_template('funcionarios.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)