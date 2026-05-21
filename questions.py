import random

# 英単語リスト（例）
words = [
    ("a glass of ～", "コップ1杯の～"),
    ("a little too", "少し～すぎる"),
    ("a lot", "非常に"),
    ("a lot of ～", "多くの～"),
    ("a pair of ～", "1組の～"),
    ("a piece of ～", "1かけらの～"),
    ("a sheet of ～", "1枚の～"),
    ("a slice of ～", "（薄い）1切れの"),
    ("after a while", "しばらくして"),
    ("after school", "放課後に"),
    ("agree with ～", "～に同意する"),
    ("all over the world", "世界中で"),
    ("anything else", "ほかの何か"),
    ("arrive in[at,on] ～", "～に到着する"),
    ("as ～ as A can", "Aができるだけ"),
    ("as usual", "いつものように"),
    ("ask ～ for ～", "～に～を求める"),
    ("ask ～ to do", "Aに～するように頼む"),
    ("at first", "最初は"),
    ("at last", "ついに、とうとう"),
    ("at school", "学校で"),
    ("at the end of ～", "～の終わりに"),
    ("be able to ～", "～することができる"),
    ("be absent from ～", "～を休んでいる"),
    ("be born", "生まれる"),
    ("be covered with ～", "～で覆われている"),
    ("be different from ～", "～と違う"),
    ("be famous for ～", "～で有名である"),
    ("be full of ～", "～でいっぱいである"),
    ("be glad to do", "～してうれしい"),
    ("be good at ～", "～がじょうず"),
]

QUESTIONS = []
qid = 1

for eng, jp in words:

    # ---------- ① 英 → 日（6択） ----------
    wrongs_jp = [w[1] for w in words if w[1] != jp]
    choices = random.sample(wrongs_jp, 5) + [jp]
    random.shuffle(choices)

    QUESTIONS.append({
        "id": qid,
        "type": "choice",
        "q": f"{eng} の意味は？",
        "choices": choices,
        "a": jp
    })
    qid += 1

    # ---------- ② 日 → 英（6択） ----------
    wrongs_eng = [w[0] for w in words if w[0] != eng]
    choices = random.sample(wrongs_eng, 5) + [eng]
    random.shuffle(choices)

    QUESTIONS.append({
        "id": qid,
        "type": "choice",
        "q": f"{jp} は英語で？",
        "choices": choices,
        "a": eng
    })
    qid += 1

    # ---------- ③ 日 → 英（入力） ----------
#    QUESTIONS.append({
#        "id": qid,
#        "type": "input",
#        "q": f"{jp} は英語で？（入力）",
#        "a": eng
#    })
#    qid += 1

# 問題順シャッフル
random.shuffle(QUESTIONS)
