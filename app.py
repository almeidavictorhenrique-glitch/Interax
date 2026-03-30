from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# CRIA O APP PRIMEIRO
app = Flask(__name__)
CORS(app)

@app.route("/pergunta", methods=["POST"])
def pergunta():
    data = request.json
    texto = data["texto"]
    idioma = data.get("idioma", "pt")

    with open("dados.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {idioma} | {texto}\n")

    if "leão" in texto.lower():
        resposta = "O leão fica na área da savana e é carnivoro"
    elif "elefante" in texto.lower():
        resposta = "O elefante está próximo ao lago"
    elif "girafa" in texto.lower():
        resposta = "A girafa tem um pescoço enorme"
    else:
        resposta = "Pergunta registrada!"

    return jsonify({"resposta": resposta})

app.run(debug=True)