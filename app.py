import os
from flask import Flask, request, redirect
import random
import sqlite3
from questions import QUESTIONS
from datetime import datetime

app = Flask(__name__)

DB = "data.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,
            correct INTEGER,
            time TEXT
        )
        """)

@app.route("/", methods=["GET", "POST"])
def quiz():
    init_db()

    message = ""
    effect = ""

    if request.method == "POST":
        qid = int(request.form["qid"])
        user_answer = request.form["answer"].strip()
        question = next(q for q in QUESTIONS if q["id"] == qid)

        correct = int(user_answer == question["a"])

        with sqlite3.connect(DB) as conn:
            conn.execute(
                "INSERT INTO logs (question_id, correct, time) VALUES (?, ?, ?)",
                (qid, correct, datetime.now().isoformat())
            )

        if correct:
            message = "🎉 せいかい！！すごい！！ 🎉"
            effect = "correct"
        else:
            message = f"🙂 おしい！ こたえは「{question['a']}」だよ"
            effect = "wrong"

    question = random.choice(QUESTIONS)

    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: sans-serif;
                text-align: center;
                background-color: {"#fff3a0" if effect=="correct" else "#f0f0f0"};
            }}
            .correct {{
                font-size: 32px;
                color: red;
                animation: pop 0.4s ease-in-out infinite alternate;
            }}
            @keyframes pop {{
                from {{ transform: scale(1); }}
                to {{ transform: scale(1.1); }}
            }}
            .wrong {{
                font-size: 24px;
                color: gray;
            }}
            input {{
                font-size: 20px;
            }}
            button {{
                font-size: 20px;
                padding: 10px 20px;
            }}
        </style>
    </head>
    <body>

        <div class="{effect}">
            {message}
        </div>

        <h2>{question['q']}</h2>

        <form method="post">
            <input type="hidden" name="qid" value="{question['id']}">
            <input name="answer" autofocus>
            <br><br>
            <button>こたえる</button>
        </form>

    </body>
    </html>
    """

@app.route("/parent")
def parent():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*), SUM(correct) FROM logs")
        total, correct = cur.fetchone()

    correct = correct or 0

    return f"""
    <h2>今日の記録</h2>
    <p>回答数: {total}</p>
    <p>正解数: {correct}</p>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

@app.route("/admin")
def admin():
    init_db()

    with sqlite3.connect(DB) as conn:
        rows = conn.execute("""
            SELECT
              substr(time, 1, 10) as day,
              COUNT(*) as total,
              SUM(correct) as correct
            FROM logs
            GROUP BY day
            ORDER BY day DESC
        """).fetchall()

    rows_html = ""
    for day, total, correct in rows:
        rows_html += f"""
        <tr>
            <td>{day}</td>
            <td>{total}</td>
            <td>{correct}</td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <title>学習ログ（保護者用）</title>
        <style>
            body {{
                font-family: sans-serif;
                padding: 20px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 10px;
                text-align: center;
            }}
            th {{
                background-color: #f5f5f5;
            }}
        </style>
    </head>
    <body>

        <h2>📘 学習履歴（1日ごと）</h2>

        <table>
            <tr>
                <th>日付</th>
                <th>解いた問題数</th>
                <th>正解数</th>
            </tr>
            {rows_html}
        </table>

    </body>
    </html>
    """
