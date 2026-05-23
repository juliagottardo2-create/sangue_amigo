from flask import Flask, jsonify, request

app = Flask(__name__)

pacientes = [{"nome": "Exemplo"}]

@app.route("/pacientes")
def listar_pacientes():
    pacientes = [
        { 
            "nome":  "string" ,
            "idade": 0,
            "peso": 0.0,
            "altura": 0.0, 
            "tipo_sanguineo":  "string", 
            "cidade":  "string" ,
            "bairro": "string",
            "logradouro": "string",
            "telefone":  "string",
            "email": "string"
        } 
    ]
    return jsonify(pacientes)


@app.route("/pacientes/<int:id>")
def retornar_pacientes_especificos(id):
    pacientes = [
        { 
            "nome":  "string" ,
            "CPF": "string",
            "idade": 0 ,
            "peso": 0.0 ,
            "altura": 0.0, 
            "tipo_sanguineo":  "string", 
            "email":  "string" 

        } 
    ]
    return jsonify(pacientes[id])


@app.route("/bolsas_de_sangue")
def pedidos_bolsas_sangue():
    bolsas = [
        {
            "cidade": "string" ,
            "hospital": "string", 
            "quantidade_bolsas": 0, 
            "urgencia": "string" ,
            "data_pedido": "string" 

        }
    ]
    return jsonify(bolsas)

@app.route("/estoque")
def bolsas_tipo_sanguineo_total():
    estoque = [
        {
            "tipo_sanguineo": "string",
            "quantidade": "string",
            "status": "string"
        }
    ]
    return jsonify(estoque)

@app.route("/hospital")
def listar_hospitais():
    dados_hospitais = {
        "nome_hospital": "string",
        "cnpj": "string",
        "cidade": "string",
        "bairro": "string",
        "logradouro": "string",
        "telefone": "string"
    }
    return jsonify(dados_hospitais)

@app.route("/doadores/aptos")
def pacientes_permitidos():
    request.args.get('tipo')
    dados_pacientes_permitidos = [
        {
            "nome": "string",
            "CPF": "string",
            "idade": 0,
            "peso": 0.0,
            "altura": 0.0,
            "telefone": "string",
            "email": "string",
            "tipo_sanguineo": "string",
            "status": "string",
            "cidade": "string",
            "bairro": "string",
            "logradouro": "string"
        }
    ]
    return jsonify(dados_pacientes_permitidos)

@app.route("/pacientes/<id>/historico")
def doacoes_pacientes_especificos(id):
    dados_pacientes_especificos = {
        "nome": "string",
        "CPF": "string",
        "idade": 0,
        "peso": 0.0,
        "altura": 0.0,
        "telefone": "string",
        "email": "string",
        "tipo_sanguineo": "string",
        "cidade": "string",
        "bairro": "string",
        "logradouro": "string",
        "doacoes_realizadas": "string"
    }
    return jsonify(dados_pacientes_especificos)

@app.route("/pacientes/<id>/proxima_doacao")
def data_estimada_proxima_doacao(id):
    dados_pacientes_proxima_doacao = {
        "nome": "string",
        "CPF": "string",
        "data_estimada": "string"
    }
    return jsonify(dados_pacientes_proxima_doacao)

@app.route("/agendamentos/hospitais/<id>")
def lista_horarios_doacao_hospital(id):
    dados_hospital_data_doacao = [
        {
            "nome_hospital": "string",
            "cnpj": "string",
            "dia_doacao": "string",
            "horario_doacao": "string"
        }
    ]
    return jsonify(dados_hospital_data_doacao)


if __name__=='__main__':
    app.run(debug=True)