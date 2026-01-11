from flask import Flask, render_template, request, session, render_template_string, jsonify

app = Flask(__name__)
app.secret_key = 'sadasdasdasfas'

@app.route("/")
def index():
    return render_template("login.html")

@app.post("/send_code")
def send_code():
    if request.is_json:
        data = request.get_json()
        email = data.get("user_email")
        if email:
            return jsonify({"message": "Код отправлен успешно", "email": email})
        return jsonify({"message": "Email не указан"}), 400
    return jsonify({"error": "Неверный формат данных"}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)