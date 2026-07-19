from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/MurArt_Samara_bot_1")
def MurArt_Samara_bot_1():
    return render_template("MurArt_Samara_bot_1.html")

@app.route("/MurArt_Samara_bot_2")
def MurArt_Samara_bot_2():
    return render_template("MurArt_Samara_bot_2.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)