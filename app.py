# App Flask volontairement trouée pour tester CodeQL + Dependabot.
# Ne pas exposer. Chaque route est une faille classique pour que le
# SAST ait de quoi gueuler.

import hashlib
import os
import pickle
import sqlite3

from flask import Flask, render_template_string, request, send_file

app = Flask(__name__)
app.secret_key = "super-secret-key-1234-do-not-use"
app.config["FLAG"] = "FLAG{dev_sec_ops_rocks}"

DB_PATH = "users.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(id INTEGER PRIMARY KEY, name TEXT, password TEXT, role TEXT)"
    )
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin')")
    conn.execute("INSERT OR IGNORE INTO users VALUES (2, 'alice', 'alice', 'user')")
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return (
        "<h1>vulnerable app</h1>"
        "<ul>"
        "<li><a href='/search?q=admin'>/search?q=admin</a></li>"
        "<li><a href='/greet?name=Bob'>/greet?name=Bob</a></li>"
        "<li><a href='/ping?host=127.0.0.1'>/ping?host=127.0.0.1</a></li>"
        "<li><a href='/download?file=readme.txt'>/download?file=readme.txt</a></li>"
        "<li>/hash?pwd=...</li>"
        "<li>POST /deserialize</li>"
        "</ul>"
    )


@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, role FROM users WHERE name = '" + q + "'")
    rows = cur.fetchall()
    conn.close()
    return {"rows": rows}


@app.route("/greet")
def greet():
    name = request.args.get("name", "world")
    return render_template_string("<h1>Hello " + name + "</h1>")


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    out = os.popen("ping -c 1 -W 1 " + host).read()
    return "<pre>" + out + "</pre>"


@app.route("/download")
def download():
    filename = request.args.get("file", "readme.txt")
    return send_file(os.path.join("files", filename))


@app.route("/deserialize", methods=["POST"])
def deserialize():
    return str(pickle.loads(request.get_data()))


@app.route("/hash")
def hash_pwd():
    return hashlib.md5(request.args.get("pwd", "").encode()).hexdigest()


if __name__ == "__main__":
    os.makedirs("files", exist_ok=True)
    with open("files/readme.txt", "w") as f:
        f.write("sample\n")
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
