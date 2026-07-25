import os
import uuid
import io
import base64
from PIL import Image, ImageFilter, ImageOps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from gigachat import GigaChat
from random import *
from werkzeug.utils import secure_filename
from db_service import DB_service

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

CREDENTIALS = os.getenv("CREDENTIALS", "")
encoded_credentials = base64.b64encode(CREDENTIALS.encode()).decode()
GIGACHAT_SCOPE = "GIGACHAT_API_PERS"

db = DB_service()
db.create_tables()

def get_user_info():
    user_id = request.args.get('user_id') or session.get('user_id')
    username = request.args.get('username') or session.get('username')
    
    if user_id:
        session['user_id'] = int(user_id)
    if username:
        session['username'] = str(username)
    
    return session.get('user_id', 123456789), session.get('username', 'Player')

def ensure_game_exists(user_id):
    if session.get('game_bot_choice') is not None and session.get('game_attempts') is not None:
        return int(session['game_bot_choice']), int(session['game_attempts'])
    
    game = db.get_game(user_id)
    if game:
        chat_id, bot_choice, attempts, created_at = game
        session['game_bot_choice'] = int(bot_choice)
        session['game_attempts'] = int(attempts)
        return int(bot_choice), int(attempts)
    
    bot_choice = randint(1, 1000)
    db.start_game(user_id, bot_choice)
    session['game_bot_choice'] = int(bot_choice)
    session['game_attempts'] = 0
    return int(bot_choice), 0

def get_chat():
    return session.get("chat_messages", [])

def save_chat(messages):
    session["chat_messages"] = messages

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def is_real_image(file_storage):
    try:
        file_storage.stream.seek(0)
        img = Image.open(file_storage.stream)
        img.verify()
        file_storage.stream.seek(0)
        return True
    except Exception:
        file_storage.stream.seek(0)
        return False



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

@app.route("/Blur_bot")
def Blur_bot():
    return render_template("Blur_bot.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files.get("file")

        if not file or not file.filename:
            return jsonify({"ok": False, "error": "Файл не выбран"}), 400

        if not allowed_file(file.filename):
            return jsonify({"ok": False, "error": "Можно загружать только фото"}), 400

        if not is_real_image(file):
            return jsonify({"ok": False, "error": "Это не изображение"}), 400

        base_name = secure_filename(file.filename.rsplit(".", 1)[0])
        uid = uuid.uuid4().hex[:8]
        download_name = f"{base_name}_{uid}_blurred.png"

        file.stream.seek(0)
        img = Image.open(file.stream).convert("RGB")
        img = ImageOps.exif_transpose(img)

        blurred = img.filter(ImageFilter.GaussianBlur(radius=8))
        small = blurred.resize((48, 48), Image.Resampling.LANCZOS)
        pixelated = small.resize(img.size, Image.Resampling.NEAREST)
        result = Image.blend(blurred, pixelated, 0.5)

        bio = io.BytesIO()
        result.save(bio, format="PNG", optimize=True)
        bio.seek(0)

        img_base64 = base64.b64encode(bio.read()).decode("utf-8")
        
        return jsonify({
            "ok": True,
            "image": f"data:image/png;base64,{img_base64}",
            "filename": download_name
        })

    except Exception as e:
        return jsonify({"ok": False, "error": f"Ошибка: {str(e)}"}), 500

@app.route("/Number_Guess_bot")
def Number_Guess_bot():
    user_id, username = get_user_info()
    
    if not session.get('user_registered'):
        db.create_user(user_id=int(user_id), chat_id=int(user_id), username=str(username))
        session['user_registered'] = True
    
    attempts = ensure_game_exists(user_id)
    
    attempts = int(attempts) if not isinstance(attempts, tuple) else int(attempts[1])
    
    message = session.pop('message', "Введите число и проверьте свою удачу 🎲")
    message_class = session.pop('message_class', "")
    status = session.pop('status', "Новая игра" if attempts == 0 else "Идет игра")

    return render_template(
        'Number_Guess_bot.html',
        tries=attempts,
        status=status,
        message=message,
        message_class=message_class
    )


@app.route('/guess', methods=['POST'])
def guess():
    user_id = request.form.get('user_id') or session.get('user_id') or 123456789
    username = request.form.get('username') or session.get('username') or 'Player'
    
    session['user_id'] = int(user_id)
    session['username'] = str(username)

    if not session.get('user_registered'):
        db.create_user(user_id=int(user_id), chat_id=int(user_id), username=str(username))
        session['user_registered'] = True
    
    user_guess_str = request.form.get('guess')
    bot_choice, attempts = ensure_game_exists(int(user_id))
    attempts += 1
    
    try:
        user_guess = int(user_guess_str)
        if not (1 <= user_guess <= 1000):
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({
            'tries': attempts - 1,
            'status': "Ошибка",
            'message': "❌ Введите число от 1 до 1000",
            'message_class': "error",
            'reveal_number': False
        })
    
    if user_guess == bot_choice:
        db.end_game(int(user_id), str(username), attempts)
        session.pop('game_bot_choice', None)
        session.pop('game_attempts', None)
        
        return jsonify({
            'tries': attempts,
            'status': "Победа!",
            'message': f"🎉 Победа! Вы угадали число {bot_choice} за {attempts} попыток!",
            'message_class': "success",
            'reveal_number': True,  
            'the_number': bot_choice
        })
        
    elif user_guess < bot_choice:
        session['game_attempts'] = attempts
        db.save_attempt(int(user_id), attempts)
        return jsonify({
            'tries': attempts,
            'status': "Мимо",
            'message': f"📈 Загаданное число БОЛЬШЕ, чем {user_guess}",
            'message_class': "hint",
            'reveal_number': False
        })
        
    else:
        session['game_attempts'] = attempts
        db.save_attempt(int(user_id), attempts)
        return jsonify({
            'tries': attempts,
            'status': "Мимо",
            'message': f"📉 Загаданное число МЕНЬШЕ, чем {user_guess}",
            'message_class': "hint",
            'reveal_number': False
        })


@app.route('/reset', methods=['POST'])
def reset():
    user_id = request.form.get('user_id') or session.get('user_id') or 123456789
    username = request.form.get('username') or session.get('username') or 'Player'
    
    bot_choice = randint(1, 1000)
    db.start_game(int(user_id), bot_choice)
    
    session['game_bot_choice'] = bot_choice
    session['game_attempts'] = 0
    session['user_registered'] = True
    
    return jsonify({
        'tries': 0,
        'status': "Новая игра",
        'message': "🔄 Игра сброшена. Удачи!",
        'message_class': "",
        'reveal_number': False
    })

@app.route("/Number_Guess_statistic")
def Number_Guess_statistic():
    leaderboard = db.get_leaderboard(limit=10)
    
    return render_template(
        'Number_Guess_statistic.html',
        leaderboard=leaderboard
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)