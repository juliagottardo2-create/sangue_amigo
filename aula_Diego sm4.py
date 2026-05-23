from flask import Flask, request, jsonify
import json
import os
 
app = Flask(__name__)
 
def carregar():
        with open('bolsas.json', 'r') as f:
            return json.load(f)
        
def salvar(bolsas):
    with open('bolsas.json', 'w') as f:
        json.dump(bolsas, f, indent=4)

@app.get('/bolsas/<int:id>') 
def get_bolsas_pr_id(id):
    bolsas = carregar()

    for bolsa in bolsas:
        if bolsa.get('id') == id:
            return jsonify(bolsa), 200
        
    return jsonify({"mansagem": "Bolsa não encontrada"})

@app.route("/bolsas", methods=["POST"])
def cadastrar_bolsas_sangue():
    dados = request.json

    campos_obrigatorios = ["nome", "CPF", "cidade", "hospital", "quantidade_bolsas", "tipo_sanguineo", "data_vencimento"]
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400
        
    campos_str = ["nome", "CPF", "cidade", "hospital", "tipo_sanguineo", "data_vencimento"]
    for campo in campos_str:
        if not isinstance(dados[campo], str):
            return jsonify({"erro": f"O campo '{campo}' deve ser preenchido por uma string"}), 422
        
    nova_bolsa = {
        "id": dados["id"],
        "idUsuario": dados["idUsuario"],
        "iddoacao_sangue": dados.get("iddoacao_sangue"),
        "idcentro_doacao": dados.get("idcentro_doacao"),
        "tipo_sanguineo": dados["tipo_sanguineo"],
        "volume": dados.get("volume"),
        "status": dados.get("status"),
        "data_expiracao": dados.get("ldata_expiracao"),
    }
 
    lista_bolsas= ler_arquivo("bolsas.json")
    lista_bolsas.append(nova_bolsa)
    salvar_arquivo("bolsas.json", lista_bolsas)
 
    return jsonify({"mensagem": "Bolsa cadastrado com sucesso!", "bolsas": nova_bolsa}), 201

 
@app.route("/pacientes", methods=["POST"])
def cadastrar_paciente():
    dados = request.json
    if not dados.get("nome"):
        return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400
    if not dados.get("CPF"):
        return jsonify({"erro": "O campo 'CPF' é obrigatório"}), 400
    if not dados.get("tipo_sanguineo"):
        return jsonify({"erro": "O campo 'tipo_sanguineo' é obrigatório"}), 400
    
    if not isinstance(dados["nome"], str):
        return jsonify({"erro": "O campo 'nome' deve ser prenchido por uma string"}), 422
    if not isinstance(dados["CPF"], str):
        return jsonify({"erro": "O campo 'CPF' deve ser prenchido por uma string"}), 422
    if not isinstance(dados["tipo_sanguineo"], str):
        return jsonify({"erro": "O campo 'tipo_sanguineo' deve ser prenchido por uma string"}), 422
    
    novo_paciente = {
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
 
    lista_pacientes = ler_arquivo("pacientes.json")
    lista_pacientes.append(novo_paciente)
    salvar_arquivo("pacientes.json", lista_pacientes)
 
    return jsonify({"mensagem": "Paciente cadastrado com sucesso!", "paciente": novo_paciente}), 201
 
@app.route("/agendamento", methods=["POST"])
def criar_agendamento():
    dados = request.json
    if not dados.get("id_paciente"):
        return jsonify({"erro": "O campo 'id_paciente' é obrigatório"}), 400
    if not dados.get("nome_hospital"):
        return jsonify({"erro": "O campo 'nome_hospital' é obrigatório"}), 400
    
    if not isinstance(dados["id_paciente"], int):
        return jsonify({"erro": "O campo 'id_paciente' deve ser prenchido por numero inteiro"}), 422
    if not isinstance(dados["nome_hospital"], str):
        return jsonify({"erro": "O campo 'nome_hospital' deve ser prenchido por uma string"}), 422
    
    novo_agendamento = {
        "id_paciente": dados["id_paciente"],
        "nome_hospital": dados["nome_hospital"]
    }
 
    lista_agendamentos = ler_arquivo("agendamentos.json")
    lista_agendamentos.append(novo_agendamento)
    salvar_arquivo("agendamentos.json", lista_agendamentos)
 
    return jsonify({"mensagem": "Agendamento criado com sucesso!", "agendamento": novo_agendamento}), 201
 
@app.route("/doacoes", methods=["POST"])
def registrar_doacao():
    dados = request.json
    if not dados.get("id_paciente"):
        return jsonify({"erro": "O campo 'id_paciente' é obrigatório"}), 400
    if not dados.get("tipo_sanguineo"):
        return jsonify({"erro": "O campo 'tipo_sanguineo' é obrigatório"}), 400
    if not dados.get("ultima_doacao"):
        return jsonify({"erro": "O campo 'ultima_doacao' é obrigatório"}), 400
    
    if not isinstance(dados["id_paciente"], int):
        return jsonify({"erro": "O campo 'id_paciente' deve ser preenchido por numero inteiro"}), 422
    if not isinstance(dados["tipo_sanguineo"], str):
        return jsonify({"erro": "O campo 'tipo_sanguineo' deve ser preenchido por uma string"}), 422
    if not isinstance(dados["ultima_doacao"], str):
        return jsonify({"erro": "O campo 'ultima_doacao' deve ser prenchidos por uma string"}), 422
    
    nova_doacao = {
        "id_paciente": dados["id_paciente"],
        "tipo_sanguineo": dados["tipo_sanguineo"],
        "ultima_doacao": dados["ultima_doacao"]
    }
 
    lista_doacoes = ler_arquivo("doacoes.json")
    lista_doacoes.append(nova_doacao)
    salvar_arquivo("doacoes.json", lista_doacoes)
 
    return jsonify({"mensagem": "Doação registrada com sucesso!", "doacao": nova_doacao}), 200
 
app.run(debug=True)