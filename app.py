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

        return redirect("/")

    question = random.choice(QUESTIONS)

    return f"""
    <h2>{question['q']}</h2>
    <form method="post">
        <input type="hidden" name="qid" value="{question['id']}">
        <input name="answer" autofocus>
        <button>答える</button>
    </form>
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
