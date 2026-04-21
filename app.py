from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import string
from gtts import gTTS

app = Flask(__name__)
CORS(app)

# 🧠 "Banco de dados" temporário
vouchers = {}

# 🔢 Gerar código único
def gerar_codigo():
    return "ZOO" + ''.join(random.choices(string.digits, k=5))

# 🎟️ Criar voucher
def criar_voucher(tipo="geral", desconto=10):
    codigo = gerar_codigo()

    vouchers[codigo] = {
        "tipo": tipo,
        "desconto": desconto,
        "usado": False,
        "criado_em": datetime.now(),
        "expira_em": datetime.now() + timedelta(minutes=30)
    }

    return codigo

# 🌐 HOME (ESSENCIAL)
@app.route("/")
def home():
    return render_template("index.html")

# 🎤 PROCESSAMENTO DE VOZ
@app.route("/processar", methods=["POST"])
def processar():
    data = request.json
    pergunta = data.get("texto", "").lower()

    if "leão" in pergunta:
        resposta = "O leão fica na área da savana."
    elif "banheiro" in pergunta:
        resposta = "Os banheiros estão próximos à entrada."
    else:
        resposta = "Desculpe, não entendi sua pergunta."

    # 🔊 áudio
    tts = gTTS(resposta, lang="pt")
    caminho_audio = "static/resposta.mp3"
    tts.save(caminho_audio)

    return jsonify({
        "resposta": resposta,
        "audio": "/" + caminho_audio
    })

# 🌐 PERGUNTAS (SEU SISTEMA ORIGINAL)
@app.route("/pergunta", methods=["POST"])
def pergunta():
    data = request.json or {}
    texto = data.get("texto", "").lower()

    print(f"[LOG] Pergunta recebida: {texto}")

    resposta = "Pergunta registrada!"
    codigo = None
    desconto = None

    if "leão" in texto:
        resposta = "O leão é conhecido como o rei da selva!"
        desconto = 20
        codigo = criar_voucher("pelucia_leao", desconto)

    elif "elefante" in texto:
        resposta = "Elefantes são os maiores animais terrestres!"
        desconto = 20
        codigo = criar_voucher("pelucia_elefante", desconto)

    elif "girafa" in texto:
        resposta = "A girafa é o animal mais alto do mundo!"
        desconto = 20
        codigo = criar_voucher("pelucia_girafa", desconto)

    print(f"[LOG] Resposta gerada: {resposta}")

    return jsonify({
        "resposta": resposta,
        "voucher": codigo,
        "desconto": desconto,
        "tipo": vouchers[codigo]["tipo"] if codigo else None,
        "mensagem": f"Use este código na loja para {desconto}% de desconto!" if codigo else None,
        "expira_em": vouchers[codigo]["expira_em"].strftime("%H:%M") if codigo else None
    })

# 🚀 RODAR SERVIDOR (UMA VEZ SÓ)
if __name__ == "__main__":
    app.run(debug=True)