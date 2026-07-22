import os
import base64
from flask import Flask, render_template, request, jsonify, session, url_for
from gigachat import GigaChat

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-me")

CREDENTIALS = os.getenv("CREDENTIALS", "")
encoded_credentials = base64.b64encode(CREDENTIALS.encode()).decode()
GIGACHAT_SCOPE = "GIGACHAT_API_PERS"


def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get("filename")
        if filename:
            file_path = os.path.join(app.root_path, "static", filename)
            if os.path.exists(file_path):
                values["q"] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def get_chat():
    return session.get("chat_messages", [])


def save_chat(messages):
    session["chat_messages"] = messages


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/MurArt_Samara_bot_1")
def MurArt_Samara_bot_1():
    return render_template("MurArt_Samara_bot_1.html")


@app.route("/MurArt_Samara_bot_2")
def MurArt_Samara_bot_2():
    return render_template("MurArt_Samara_bot_2.html")


@app.route("/AI_assistant_bot")
def AI_assistant_bot():
    messages = get_chat()
    return render_template("AI_assistant_bot.html", messages=messages)


@app.route("/AI_assistant_bot/send", methods=["POST"])
def AI_assistant_bot_send():
    user_prompt = request.form.get("message", "").strip()
    if not user_prompt:
        return jsonify({"ok": False, "error": "empty"}), 400

    messages = get_chat()
    messages.append({"role": "user", "text": user_prompt})
    save_chat(messages)

    try:
        with GigaChat(
            credentials=encoded_credentials,
            scope=GIGACHAT_SCOPE,
            verify_ssl_certs=False
        ) as giga:
            response = giga.chat(user_prompt)
        ai_answer = response.choices[0].message.content.strip()
    except Exception as e:
        ai_answer = f"Ошибка ИИ: {e}"

    messages = get_chat()
    messages.append({"role": "bot", "text": ai_answer})
    save_chat(messages)

    return jsonify({"ok": True, "user": user_prompt, "bot": ai_answer})


@app.route("/AI_assistant_bot/reset", methods=["POST"])
def reset_ai_history():
    session.pop("chat_messages", None)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)