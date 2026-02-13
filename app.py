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
            streak INTEGER,
            time TEXT
        )
        """)

def select_question():
    with sqlite3.connect(DB) as conn:
        stats = conn.execute("""
            SELECT question_id,
                   AVG(correct) as rate
            FROM logs
            GROUP BY question_id
        """).fetchall()

    rates = {qid: rate for qid, rate in stats}

    weighted = []
    for q in QUESTIONS:
        rate = rates.get(q["id"], 0.0)
        weight = 1.5 - rate   # 苦手ほど重く
        weighted.extend([q] * int(weight * 10))

    return random.choice(weighted if weighted else QUESTIONS)

@app.route("/", methods=["GET", "POST"])
def quiz():
    init_db()

    message = ""
    effect = ""

    if request.method == "POST":
        qid = int(request.form["qid"])
        user_answer = request.form["answer"]
        question = next(q for q in QUESTIONS if q["id"] == qid)

        correct = int(user_answer == question["a"])

         with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            cur.execute("SELECT streak FROM logs ORDER BY id DESC LIMIT 1")
            last = cur.fetchone()
            streak = (last[0] if last else 0)

            if correct:
                streak += 1
            else:
                streak = 0

            cur.execute(
                "INSERT INTO logs (question_id, correct, streak, time) VALUES (?, ?, ?, ?)",
                (qid, correct, streak, datetime.now().isoformat())
            )

            conn.execute(
                "INSERT INTO logs (question_id, correct, time) VALUES (?, ?, ?)",
                (qid, correct, datetime.now().isoformat())
            )

        if correct:
            if streak >= 5:
                message = "🔥 5れんぞくせいかい！天才！！ 🔥"
            elif streak >= 3:
                message = "✨ 3れんぞく！すごい！ ✨"
            else:
                message = "🎉 せいかい！！ 🎉"
            effect = "correct"
        else:
            message = f"🙂 おしい！ こたえは「{question['a']}」だよ"
            effect = "wrong"

    question = select_question()
    choices = question["choices"].copy()
    random.shuffle(choices)

    buttons_html = ""
    for c in choices:
        buttons_html += f"""
        <button name="answer" value="{c}" style="font-size:20px;padding:10px;margin:5px;width:200px;">
            {c}
        </button><br>
        """

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
            button {{
                font-size: 20px;
                padding: 10px;
                margin: 5px;
                width: 200px;
                border-radius: 12px;
                background-color: white;
                border: 2px solid #888;
                transition: 0.2s;
            }}
            button:hover {{
                background-color: #cce7ff;
                border-color: #3399ff;
            }}
            button:active {{
                background-color: #99d0ff;
                transform: scale(0.97);
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
            {buttons_html}
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
