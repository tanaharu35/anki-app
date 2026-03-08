import random

elements = [
 ("H",1,1),("He",18,1),
 ("Li",1,2),("Be",2,2),("B",13,2),("C",14,2),("N",15,2),("O",16,2),("F",17,2),("Ne",18,2),
 ("Na",1,3),("Mg",2,3),("Al",13,3),("Si",14,3),("P",15,3),("S",16,3),("Cl",17,3),("Ar",18,3),
 ("K",1,4),("Ca",2,4),("Sc",3,4),("Ti",4,4),("V",5,4),("Cr",6,4),("Mn",7,4),("Fe",8,4),
 ("Co",9,4),("Ni",10,4),("Cu",11,4),("Zn",12,4),("Ge",14,4),("Br",17,4),
 ("Sr",2,5),("Pd",10,5),("Ag",11,5),("Cd",12,5),("Sn",14,5),("I",17,5),
 ("Ba",2,6),("Pt",10,6),("Au",11,6),("Hg",12,6),("Pb",14,6)
]

questions = []

symbols = [e[0] for e in elements]

for symbol, group, period in elements:

    # ------------------------
    # 族＋周期 → 元素記号
    # ------------------------

    q1 = f"第{group}族・第{period}周期の元素は？"

    wrong = random.sample([s for s in symbols if s != symbol], 5)

    choices = wrong + [symbol]
    random.shuffle(choices)

    questions.append({
        "q": q1,
        "choices": choices,
        "a": symbol
    })

    # ------------------------
    # 元素記号 → 族＆周期
    # ------------------------

    q2 = f"{symbol} の族と周期は？"

    correct = f"{group}族{period}周期"

    wrong_choices = set()

    while len(wrong_choices) < 5:
        g = random.randint(1,18)
        p = random.randint(1,6)
        w = f"{g}族{p}周期"

        if w != correct:
            wrong_choices.add(w)

    choices = list(wrong_choices) + [correct]
    random.shuffle(choices)

    questions.append({
        "q": q2,
        "choices": choices,
        "a": correct
    })

    random.shuffle(questions)
    QUESTIONS = questions

