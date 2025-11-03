from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


BREVO_API_KEY = os.getenv("API_KEY")
LIST_ID = 16

@app.route("/lead", methods=["POST"])
def lead():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "O campo 'email' é obrigatório."}), 400

    try:
        response = requests.post(
            "https://api.brevo.com/v3/contacts",
            headers={
                "accept": "application/json",
                "api-key": BREVO_API_KEY,
                "content-type": "application/json",
            },
            json={
                "email": email,
                "listIds": [LIST_ID],
                "updateEnabled": True,
            },
        )

        print("Status code:", response.status_code)
        print("Response text:", response.text)

        # tenta converter pra JSON, se falhar, mostra o texto cru
        try:
            response_data = response.json()
        except ValueError:
            response_data = {"raw_response": response.text}

        if response.status_code in [200, 201]:
            return jsonify({"success": True, "message": "Contato adicionado com sucesso!"}), 200
        else:
            return jsonify({
                "error": "Falha ao adicionar contato no Brevo",
                "details": response_data
            }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Webhook rodando!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
