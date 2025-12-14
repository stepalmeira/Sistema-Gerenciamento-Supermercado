from flask import Flask, Blueprint, request, jsonify
from servicos.relatorios import RelatoriosDatabase
import datetime

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorios/balanco_financeiro', methods=['GET'])
def get_balanco():
    hoje = datetime.date.today()
    db = RelatoriosDatabase()
    dados = db.get_balanco_financeiro_mensal(hoje.year, hoje.month)
    
    custos = float(dados['total_custos'])
    fat = float(dados['total_faturamento'])
    return jsonify({
        "analise_financeira": {
            "total_gasto_em_compras": custos,
            "total_recebido_em_vendas": fat,
            "lucro_bruto_operacional": fat - custos
        }
    })

@relatorios_bp.route('/relatorios/historico_anual', methods=['GET'])
def get_historico():
    db = RelatoriosDatabase()
    return jsonify(db.get_historico_anual())

@relatorios_bp.route('/estoque/lotes', methods=['GET'])
def get_lotes():
    db = RelatoriosDatabase()
    return jsonify(db.get_todos_lotes())

@relatorios_bp.route('/estoque/lote', methods=['DELETE'])
def delete_lote():
    cod = request.args.get('cod_lote')
    if RelatoriosDatabase().deletar_lote(cod):
        return jsonify({"msg": "Lote removido"}), 200
    return jsonify({"erro": "Erro ao remover"}), 500

# --- ROTAS DE FUNCIONÁRIO ---
@relatorios_bp.route('/funcionario', methods=['GET', 'POST', 'DELETE'])
def gerir_funcionario():
    db = RelatoriosDatabase()
    
    if request.method == 'GET':
        cpf = request.args.get('cpf')
        setor = request.args.get('setor')
        if cpf:
            # Caso 1: Busca por CPF
            func = db.get_funcionario_por_cpf(cpf)
            if func:
                func['salario'] = float(func['salario'])
                return jsonify({"dados_contratuais": func})
            return jsonify({"erro": "Funcionário não encontrado"}), 404
        
        elif setor:
            # Caso 2: Busca por Setor
            funcs = db.get_funcionarios_por_setor(setor)
            if funcs:
                # Converte o salário para float em todos os resultados
                for func in funcs:
                    func['salario'] = float(func['salario'])
                return jsonify({"funcionarios": funcs})
            return jsonify({"mensagem": f"Nenhum funcionário encontrado no setor: {setor}"}), 404

    if request.method == 'POST':
        dados = request.get_json()
        if db.criar_funcionario(dados):
            return jsonify({"msg": "Criado"}), 201
        return jsonify({"erro": "Erro ao criar"}), 500

    if request.method == 'DELETE':
        cpf = request.args.get('cpf')
        if db.deletar_funcionario(cpf):
            return jsonify({"msg": "Removido"}), 200
        return jsonify({"erro": "Erro ao remover (pode ter vendas vinculadas)"}), 500


@relatorios_bp.route('/relatorios/historico_vendas', methods=['GET'])
def get_historico_vendas():
    db = RelatoriosDatabase()
    inicio = request.args.get('inicio')  # 'YYYY-MM-DD'
    fim = request.args.get('fim')        # 'YYYY-MM-DD'
    resultados = db.get_historico_vendas_por_periodo(inicio, fim)
    # converte formatos numéricos/datas se necessário antes de jsonify
    for r in resultados:
        r['valor_total'] = float(r['valor_total'])
    return jsonify(resultados)