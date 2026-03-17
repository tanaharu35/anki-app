import os
from flask import Flask, request, redirect
import random
import sqlite3
import gspread
from google.oauth2.service_account import Credentials
from questions import QUESTIONS
#from datetime import datetime
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

DB = "data.db"

JST = timezone(timedelta(hours=9))

# ===== Google Sheets 設定 =====
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "service_account.json",
    scopes=SCOPES
)

gc = gspread.authorize(creds)
sheet = gc.open("study_log").sheet1
# ==============================

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


switch_html = """
<div style="margin-bottom:20px;">
  <a href="/admin?mode=daily">📅 日別表示</a> |
  <a href="/admin?mode=word">📘 単語別ランキング</a>
</div>
"""

def render_daily(records):
    daily = {}

    for r in records:
        day = r["日付"]
        correct = int(r["正解"])

        if day not in daily:
            daily[day] = {"total": 0, "correct": 0}

        daily[day]["total"] += 1
        daily[day]["correct"] += correct

    rows = sorted(daily.items(), reverse=True)

    rows_html = ""
    for day, data in rows:
        rows_html += f"""
        <tr>
          <td>{day}</td>
          <td>{data['total']}</td>
          <td>{data['correct']}</td>
        </tr>
        """

    return f"""
    <table>
      <tr>
        <th>日付</th>
        <th>解いた問題数</th>
        <th>正解数</th>
      </tr>
      {rows_html}
    </table>
    """

id_to_word = {q["id"]: q["a"] for q in QUESTIONS}

def render_word_rank(records):
    stats = {}

    for r in records:
        qid = r["問題ID"]
        correct = int(r["正解"])
        word = id_to_word.get(qid, f"ID:{qid}")

        if word not in stats:
            stats[word] = {"total": 0, "correct": 0}

        stats[word]["total"] += 1
        stats[word]["correct"] += correct

    # 正答率でソート（低い順 = 苦手）
    ranked = sorted(
        stats.items(),
        key=lambda x: x[1]["correct"] / x[1]["total"]
    )

    rows_html = ""
    for word, data in ranked:
        rate = int(data["correct"] / data["total"] * 100)
        rows_html += f"""
        <tr>
          <td>{word}</td>
          <td>{data['total']}</td>
          <td>{data['correct']}</td>
          <td>{rate}%</td>
        </tr>
        """

    return f"""
    <table>
      <tr>
        <th>単語</th>
        <th>出題回数</th>
        <th>正解数</th>
        <th>正答率</th>
      </tr>
      {rows_html}
    </table>
    """

@app.route("/", methods=["GET", "POST"])
def quiz():
    init_db()

    message = ""
    effect = ""
    streak = 0
    now_jst = datetime.now(JST)
    
    if request.method == "POST":
        qid = int(request.form["qid"])
        user_answer = request.form["answer"]
        question = next(q for q in QUESTIONS if q["id"] == qid)

        correct = int(user_answer == question["a"])

        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            cur.execute("SELECT streak FROM logs ORDER BY id DESC LIMIT 1")
            last = cur.fetchone()
            streak = (last[0] if last and last[0] is not None else 0)

            if correct:
                streak += 1
            else:
                streak = 0

#            cur.execute(
#                "INSERT INTO logs (question_id, correct, streak, time) VALUES (?, ?, ?, ?)",
#                (qid, correct, streak, datetime.now().isoformat())
#            )
            cur.execute(
                "INSERT INTO logs (question_id, correct, streak, time) VALUES (?, ?, ?, ?)",
                (qid, correct, streak, now_jst.isoformat())
            )
#            sheet.append_row([
#                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                qid,
#                correct,
#                streak
#            ])
            sheet.insert_row([
                now_jst.strftime("%Y-%m-%d"),
                qid,
                correct,
                streak,
                now_jst.strftime("%H:%M:%S")
            ], index=2)

        if correct:
            if streak >= 5:
                message = f"🔥 {streak}れんぞくせいかい！天才！！ 🔥"
            elif streak >= 3:
                message = f"✨ {streak}れんぞく！すごい！ ✨"
            else:
                message = f"🎉 せいかい！！（{streak}れんぞく） 🎉"
            effect = "correct"
        else:
            message = f"🙂 おしい！ こたえは「{question['a']}」だよ"
            effect = "wrong"

    today = datetime.now().strftime("%Y-%m-%d")

    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) FROM logs
            WHERE correct = 1
              AND substr(time, 1, 10) = ?
        """, (today,))
        today_correct = cur.fetchone()[0]

    question = select_question()
    choices = question["choices"].copy()
    random.shuffle(choices)

    buttons_html = ""
    for c in choices:
        buttons_html += f"""
        <button name="answer" value="{c}" style="font-size:40px;padding:10px;margin:5px;width:400px;">
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
                font-size: 2rem;
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
                font-size: 40px;
                padding: 10px;
                margin: 5px;
                width: 400px;
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
            .big-streak {{
                font-size: 40px;
            }}
        </style>
    </head>
    <body>

        <div class="{effect} {'big-streak' if streak >= 5 else ''}">
            {message}
        </div>
#        <div style="margin:20px;">
#            <img src="/static/syuuki.jpg" style="width:90%; max-width:800px;">
#        </div>
        <div style="margin:20px;">
            <img src="/static/syuuki.jpg" style="width:90%; max-width:800px; border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.2);">
        </div>
        <h2>{question['q']}</h2>

        <form method="post">
            <input type="hidden" name="qid" value="{question['id']}">
            {buttons_html}
            <div style="margin-top:20px;font-size:20px;color:#333;">
                📊 本日の正解数：{today_correct} 問
            </div>
        </form>

    </body>
    </html>
    """


#@app.route("/parent")
#def parent():
#    with sqlite3.connect(DB) as conn:
#        cur = conn.cursor()
#        cur.execute("SELECT COUNT(*), SUM(correct) FROM logs")
#        total, correct = cur.fetchone()
#
#    correct = correct or 0
#
#    return f"""
#    <h2>今日の記録</h2>
#    <p>回答数: {total}</p>
#    <p>正解数: {correct}</p>
#    """

@app.route("/admin")
def admin():
    mode = request.args.get("mode", "daily")
    
    # スプレッドシートから全データ取得（ヘッダ除外）
    records = sheet.get_all_records()

    if mode == "word":
        content = render_word_rank(records)
    else:
        content = render_daily(records)

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
      <h2>📊 学習状況</h2>
      {switch_html}
      {content}
    </body>
    </html>
    """

#    daily = {}
#
#    for r in records:
#        day = r["日付"]
#        correct = int(r["正解"])
#
#        if day not in daily:
#            daily[day] = {"total": 0, "correct": 0}
#
#        daily[day]["total"] += 1
#        daily[day]["correct"] += correct
#
#    # 日付の新しい順に並べ替え
#    rows = sorted(daily.items(), reverse=True)
#
#    rows_html = ""
#    for day, data in rows:
#        rows_html += f"""
#        <tr>
#            <td>{day}</td>
#            <td>{data['total']}</td>
#            <td>{data['correct']}</td>
#        </tr>
#        """
#
#    return f"""
#    <html>
#    <head>
#        <title>学習ログ（保護者用）</title>
#    </head>
#    <body>
#
#        <h2>📘 学習履歴（1日ごと）</h2>
#
#        <table>
#            <tr>
#                <th>日付</th>
#                <th>解いた問題数</th>
#                <th>正解数</th>
#            </tr>
#            {rows_html}
#        </table>
#
#    </body>
#    </html>
#    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
