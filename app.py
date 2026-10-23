from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Coloque aqui a senha do MySQL, se você tiver uma
        database="neymar_site"
    )

@app.route("/mensagens", methods=["GET"])
def listar_mensagens():
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nome, email, mensagem, data_envio "
            "FROM mensagens_contato ORDER BY id DESC"
        )
        mensagens = cursor.fetchall()
        for item in mensagens:
            if item.get("data_envio"):
                item["data_envio"] = item["data_envio"].strftime("%d/%m/%Y %H:%M")
        return jsonify(mensagens)
    except Error as erro:
        return jsonify({"erro": "Erro ao consultar o banco de dados."}), 500
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

@app.route("/mensagens", methods=["POST"])
def cadastrar_mensagem():
    dados = request.get_json(silent=True) or {}
    nome = str(dados.get("nome", "")).strip()
    email = str(dados.get("email", "")).strip()
    mensagem = str(dados.get("mensagem", "")).strip()

    if not nome or not email or not mensagem:
        return jsonify({"erro": "Preencha nome, e-mail e mensagem."}), 400

    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO mensagens_contato (nome, email, mensagem) "
            "VALUES (%s, %s, %s)",
            (nome, email, mensagem)
        )
        conexao.commit()
        novo_id = cursor.lastrowid
        return jsonify({
            "id": novo_id,
            "nome": nome,
            "email": email,
            "mensagem": mensagem
        }), 201
    except Error as erro:
        return jsonify({"erro": "Não foi possível salvar a mensagem no banco."}), 500
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
