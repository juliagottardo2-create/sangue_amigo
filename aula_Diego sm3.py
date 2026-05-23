from flask import Flask, request, jsonify
import json
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)
 
def carregar(pathFile):   #perguntar 
        with open(pathFile, 'r') as f:
            return json.load(f)
        
def salvar(pathFile, bolsas):
    with open(pathFile, 'w') as f:
        json.dump(bolsas, f, indent=4)

@app.get('/bolsa/<int:id>')
def get_bolsa_por_id(id):
    bolsas = carregar("bolsas.json")

    for bolsa in bolsas:
        if bolsa.get('id') == id:
            return jsonify(bolsa), 200
        
    return jsonify({"erro": "Bolsa não encontrada"}), 404

@app.post("/bolsas", methods=["POST"])
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
        
    lista_bolsas = carregar("bolsas.json")

    nova_bolsa = {         
        "id": dados["id"],
        "nome": dados["nome"],
        "CPF": dados["CPF"],
        "cidade": dados["cidade"],
        "hospital": dados["hospital"],
        "quantidade_bolsas": dados["quantidade_bolsas"],
        "tipo_sanguineo": dados["tipo_sanguineo"],
        "data_vencimento": dados["data_vencimento"]
    }
 
    lista_bolsas.append(nova_bolsa)
    salvar("bolsas.json", lista_bolsas)
 
    return jsonify({"mensagem": "Bolsa cadastrado com sucesso!", "bolsas": nova_bolsa}), 201

 
@app.post("/pacientes", methods=["POST"])
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
 
    lista_pacientes = carregar("pacientes.json")
    lista_pacientes.append(novo_paciente)
    salvar("pacientes.json", lista_pacientes)
 
    return jsonify({"mensagem": "Paciente cadastrado com sucesso!", "paciente": novo_paciente}), 201
 
@app.post("/agendamento", methods=["POST"])
def criar_agendamento():
    dados = request.json
    if not dados.get("id_paciente"):
        return jsonify({"erro": "O campo 'id_paciente' é obrigatório"}), 400
    if not dados.get("nome_hospital"):
        return jsonify({"erro": "O campo 'nome_hospital' é obrigatório"}), 400
    
    if not isinstance(dados["id_paciente"], int):
        return jsonify({"erro": "O campo 'id_paciente' deve ser preenchido por numero inteiro"}), 422
    if not isinstance(dados["nome_hospital"], str):
        return jsonify({"erro": "O campo 'nome_hospital' deve ser preenchido por uma string"}), 422
    
    novo_agendamento = {
        "id_paciente": dados["id_paciente"],
        "nome_hospital": dados["nome_hospital"]
    }
 
    lista_agendamentos = carregar("agendamentos.json")
    lista_agendamentos.append(novo_agendamento)
    salvar("agendamentos.json", lista_agendamentos)
 
    return jsonify({"mensagem": "Agendamento criado com sucesso!", "agendamento": novo_agendamento}), 201
 
@app.post("/doacoes", methods=["POST"])
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
    
    lista_doacoes = carregar("doacoes.json")

    nova_doacao = {
        "id": len(lista_doacoes) + 1,
        "id_paciente": dados["id_paciente"],
        "tipo_sanguineo": dados["tipo_sanguineo"],
        "ultima_doacao": dados["ultima_doacao"]
    }
 
    lista_doacoes.append(nova_doacao)
    salvar("doacoes.json", lista_doacoes)
 
    return jsonify({"mensagem": "Doação registrada com sucesso!", "doacao": nova_doacao}), 200

@app.get('/bolsas')
def get_bolsas():
    todas_as_bolsas = carregar("bolsas.json")

    filtro_tipo = request.args.get('tipo_sanguineo')
    filtro_status = request.args.get('status')
    filtro_hospital = request.args.get('hospital')

    resultado = []

    for bolsa in todas_as_bolsas:
        if not filyto_tipo or bolsa>get('tipo_sanguineo') == filtro_tipo:

            if not filtro_status or bolsa.get('status') == filtro_status:

                if filtro_hospital:
                    valor_no_banco = bolsa.get('hospital', ""). lower
                    if filtro_hospital.lower() in valor_no_banco:
                        resultado.append(bolsa)
                
                else:
                    resultado.append(bolsa)

        resultado.append(bolsa)
    return jsonify (resultado), 200

@app.put('/bolsas/<int:id>')
def atualizar(id):
    bolsas = carregar("bolsas.json")
    dados = request.json

    if not dados:
        return jsonify({"erro": "Dados fornecidos inválidos!"}), 400

    for bolsa in bolsas:
        if bolsa.get('id') == id:
            bolsa.update(dados)
            salvar("bolsas.json",bolsas)
            return jsonify(dados), 200
            
    return jsonify({"Erro": "Bolsa não encontrada"}), 404
        
@app.delete('/bolsas/<int:id>')
def deletar(id):
    bolsas = carregar("bolsas.json")

    for bolsa in bolsas:
        if bolsa.get('id') == id:
            bolsas.remove(bolsa)
            salvar("bolsas.json",bolsas)
            return jsonify({"mensagem": "Bolsa deletada!"}), 200
    return jsonify({"erro": "Não encontrado"}), 404
    
app.run(debug=True)