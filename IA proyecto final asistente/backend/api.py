from flask import Flask, request, jsonify
from flask_cors import CORS
from modelo import responder

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    mensaje = request.json.get("pregunta")
    respuesta = responder(mensaje)
    return jsonify({"respuesta": respuesta})

app.run(host="0.0.0.0", port=5001)
##Hola mundo