from flask import Flask, request, jsonify
import json
 
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)
 
def carregar(arquivo):
    with open(arquivo, 'r') as f:
        return json.load(f)
 
def salvar(arquivo, dados):
    with open(arquivo, 'w') as f:
        json.dump(dados, f, indent=4)
 
 
@app.get('/bolsas')
def get_bolsas():
    bolsas = carregar('bolsas.json')
 
    tipo_sanguineo = request.args.get('tipo_sanguineo')
    status         = request.args.get('status')
    hospital       = request.args.get('hospital')
 
    resultado = []
    for bolsa in bolsas:
        if tipo_sanguineo and bolsa.get('tipo_sanguineo') != tipo_sanguineo:
            continue
        if status and bolsa.get('status') != status:
            continue
        if hospital and hospital.lower() not in bolsa.get('hospital', '').lower():
            continue
        resultado.append(bolsa)
 
    return jsonify(resultado), 200
 
 
@app.get('/bolsas/<int:id>')
def get_bolsa_por_id(id):
    bolsas = carregar('bolsas.json')
 
    for bolsa in bolsas:
        if bolsa.get('id') == id:
            return jsonify(bolsa), 200
 
    return jsonify({"erro": "Bolsa não encontrada"}), 404
 
 
@app.post('/bolsas')
def criar_bolsa():
    dados = request.json

    campos_obrigatorios = ['nome', 'CPF', 'cidade', 'hospital', 'quantidade_bolsas', 'tipo_sanguineo', 'data_vencimento']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400
        
    campos_string = ['cidade', 'CPF', 'hospital', 'data_vencimento', 'tipo_sanguineo']
    for campo in campos_string:
        if not isinstance(dados[campo], str):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por uma string"}), 422 

    campos_inteiros = ['quantidade_bolsas']
    for campo in campos_inteiros:
        if not isinstance(dados[campo], int):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por uma número inteiro"}), 422 

    tipos_validos = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    if dados.get('tipo_sanguineo') not in tipos_validos:
        return jsonify({"erro": "Tipo sanguíneo inválido"}), 422
    

    bolsas = carregar('bolsas.json')

    novo_id = 1
    if bolsas:
        novo_id = bolsas[-1]['id'] + 1

    nova_bolsa = {
        "id": novo_id,
        "nome": dados["nome"],
        "CPF": dados["CPF"],
        "cidade": dados["cidade"],
        "hospital": dados["hospital"],
        "quantidade_bolsas": dados["quantidade_bolsas"],
        "tipo_sanguineo": dados["tipo_sanguineo"],
        "data_vencimento": dados["data_vencimento"]
    }

    bolsas.append(nova_bolsa)
    salvar('bolsas.json', bolsas)

    return jsonify({"mensagem": "Bolsa cadastrada com sucesso!", "bolsa": nova_bolsa}), 201
 
 
@app.put('/bolsas/<int:id>')
def atualizar_bolsa(id):
    bolsas = carregar('bolsas.json')
    dados = request.json

    campos_string = ['cidade', 'CPF', 'hospital', 'data_vencimento', 'tipo_sanguineo']
    for campo in campos_string:
        if campo in dados and not isinstance(dados[campo], str):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por uma string"}), 422

    campos_inteiros = ['quantidade_bolsas']
    for campo in campos_inteiros:
        if campo in dados and not isinstance(dados[campo], int):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por um número inteiro"}), 422

    tipos_validos = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    if 'tipo_sanguineo' in dados and dados['tipo_sanguineo'] not in tipos_validos:
        return jsonify({"erro": "Tipo sanguíneo inválido"}), 422

    for bolsa in bolsas:
        if bolsa.get('id') == id:
            if 'nome' in dados:
                bolsa['nome'] = dados['nome']
            if 'CPF' in dados:
                bolsa['CPF'] = dados['CPF']
            if 'cidade' in dados:
                bolsa['cidade'] = dados['cidade']
            if 'hospital' in dados:
                bolsa['hospital'] = dados['hospital']
            if 'quantidade_bolsas' in dados:
                bolsa['quantidade_bolsas'] = dados['quantidade_bolsas']
            if 'tipo_sanguineo' in dados:
                bolsa['tipo_sanguineo'] = dados['tipo_sanguineo']
            if 'data_vencimento' in dados:
                bolsa['data_vencimento'] = dados['data_vencimento']

            salvar('bolsas.json', bolsas)
            return jsonify({"mensagem": "Bolsa atualizada com sucesso!", "bolsa": bolsa}), 200

    return jsonify({"erro": "Bolsa não encontrada"}), 404
 
 
@app.delete('/bolsas/<int:id>')
def deletar_bolsa(id):
    bolsas = carregar('bolsas.json')
 
    for bolsa in bolsas:
        if bolsa.get('id') == id:
            bolsas.remove(bolsa)
            salvar('bolsas.json', bolsas)
            return jsonify({"mensagem": "Bolsa deletada com sucesso!"}), 200
 
    return jsonify({"erro": "Bolsa não encontrada"}), 404
 
 
@app.get('/pacientes/<int:id>')
def get_paciente_por_id(id):
    pacientes = carregar('pacientes.json')
 
    for paciente in pacientes:
        if paciente.get('id') == id:
            return jsonify(paciente), 200
 
    return jsonify({"erro": "Paciente não encontrado"}), 404
 
@app.post('/pacientes')
def criar_paciente():
    dados = request.json
    campos_obrigatorios = ['nome', 'CPF', 'idade', 'peso', 'altura', 'tipo_sanguineo', 'cidade', 'bairro', 'logradouro', 'telefone', 'email']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400
            
    campos_string = ['nome', 'tipo_sanguineo', 'cidade', 'bairro', 'logradouro', 'email', 'CPF', 'telefone']
    for campo in campos_string:
        if not isinstance(dados[campo], str):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por uma string"}), 422 

    campos_inteiros = ['idade']
    for campo in campos_inteiros:
        if not isinstance(dados[campo], int):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por uma número inteiro"}), 422 

    campos_float = ['peso', 'altura']
    for campo in campos_float:
        if not isinstance(dados[campo], float):
            return jsonify({"erro": f"O campo '{campo}' deve usar ponto para decimais"}), 422 

    pacientes = carregar('pacientes.json')

    novo_id = 1
    if pacientes:
        novo_id = pacientes[-1]['id'] + 1

    novo_paciente = {
        "id": novo_id,
        "nome": dados["nome"],
        "CPF": dados["CPF"],
        "idade": dados.get("idade"),
        "peso": dados.get("peso"),
        "altura": dados.get("altura"),
        "tipo_sanguineo": dados["tipo_sanguineo"],
        "cidade": dados.get("cidade"),
        "bairro": dados.get("bairro"),
        "logradouro": dados.get("logradouro"),
        "telefone": dados.get("telefone"),
        "email": dados.get("email")
    }

    pacientes.append(novo_paciente)
    salvar('pacientes.json', pacientes)

    return jsonify({"mensagem": "Paciente cadastrado com sucesso!", "paciente": novo_paciente}), 201
 
 
@app.get('/agendamentos/<int:id_paciente>')
def get_agendamentos(id_paciente):
    agendamentos = carregar('agendamentos.json')
    filtrados = [a for a in agendamentos if a.get('id_paciente') == id_paciente]
    return jsonify(filtrados), 200
 
@app.post('/agendamentos')
def criar_agendamento():
    dados = request.json

    campos_obrigatorios = ['id_paciente', 'nome_hospital']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400
        
    campos_string = ['nome_hospital']
    for campo in campos_string:
        if not isinstance(dados[campo], str):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por uma string"}), 422 

    campos_inteiros = ['id_paciente']
    for campo in campos_inteiros:
        if not isinstance(dados[campo], int):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por uma número inteiro"}), 422 

    agendamentos = carregar('agendamentos.json')

    novo_id = 1
    if agendamentos:
        novo_id = agendamentos[-1]['id'] + 1

    novo_agendamento = {
        "id": novo_id,
        "id_paciente": dados["id_paciente"],
        "nome_hospital": dados["nome_hospital"]
    }

    agendamentos.append(novo_agendamento)
    salvar('agendamentos.json', agendamentos)

    return jsonify({"mensagem": "Agendamento criado com sucesso!", "agendamento": novo_agendamento}), 201
 
 
@app.put('/agendamentos/<int:id>')
def atualizar_agendamento(id):
    agendamentos = carregar('agendamentos.json')
    dados = request.json

    campos_string = ['nome_hospital']
    for campo in campos_string:
        if campo in dados and not isinstance(dados[campo], str):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por uma string"}), 422

    campos_inteiros = ['id_paciente']
    for campo in campos_inteiros:
        if campo in dados and not isinstance(dados[campo], int):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por um número inteiro"}), 422

    for agendamento in agendamentos:
        if agendamento.get('id') == id:
            if 'id_paciente' in dados:
                agendamento['id_paciente'] = dados['id_paciente']
            if 'nome_hospital' in dados:
                agendamento['nome_hospital'] = dados['nome_hospital']

            salvar('agendamentos.json', agendamentos)
            return jsonify({"mensagem": "Agendamento atualizado com sucesso!", "agendamento": agendamento}), 200

    return jsonify({"erro": "Agendamento não encontrado"}), 404
 
@app.delete('/agendamentos/<int:id>')
def cancelar_agendamento(id):
    agendamentos = carregar('agendamentos.json')
 
    for agendamento in agendamentos:
        if agendamento.get('id') == id:
            agendamentos.remove(agendamento)
            salvar('agendamentos.json', agendamentos)
            return jsonify({"mensagem": "Agendamento cancelado com sucesso!"}), 200
 
    return jsonify({"erro": "Agendamento não encontrado"}), 404
 
 
@app.post('/doacoes')
def registrar_doacao():
    dados = request.json

    campos_obrigatorios = ['id_paciente', 'tipo_sanguineo', 'ultima_doacao']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400
        
    campos_string = ['tipo_sanguineo', 'ultima_doacao']
    for campo in campos_string:
        if not isinstance(dados[campo], str):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por uma string"}), 422 

    campos_inteiros = ['id_paciente']
    for campo in campos_inteiros:
        if not isinstance(dados[campo], int):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por uma número inteiro"}), 422 

    doacoes = carregar('doacoes.json')

    novo_id = 1
    if doacoes:
        novo_id = doacoes[-1]['id'] + 1

    nova_doacao = {
        "id": novo_id,
        "id_paciente": dados["id_paciente"],
        "tipo_sanguineo": dados["tipo_sanguineo"],
        "ultima_doacao": dados["ultima_doacao"]
    }

    doacoes.append(nova_doacao)
    salvar('doacoes.json', doacoes)

    return jsonify({"mensagem": "Doação registrada com sucesso!", "doacao": nova_doacao}), 201
 
 
@app.get('/notificacoes/<int:id_paciente>')
def get_notificacoes(id_paciente):
    pacientes = carregar('pacientes.json')
 
    for paciente in pacientes:
        if paciente.get('id') == id_paciente:
            notificacao = {
                "id": 1,
                "titulo": f"Olá, {paciente['nome']}!",
                "mensagem": f"O estoque para o tipo {paciente['tipo_sanguineo']} precisa de doações.",
                "lida": False
            }
            return jsonify([notificacao]), 200
 
    return jsonify({"erro": "Paciente não encontrado"}), 404
 
 
app.run(debug=True)