import random

QUESTIONS = [
    {"id": 1,  "q": "「1つの」はどれ？", "a": "a", "choices": ["a","an","the","one","at","and"]},
    {"id": 2,  "q": "「できる」はどれ？", "a": "able", "choices": ["able","ago","all","again","aim","ask"]},
    {"id": 3,  "q": "「午後」はどれ？", "a": "afternoon", "choices": ["afternoon","apple","animal","ago","ago","and"]},
    {"id": 4,  "q": "「再び」はどれ？", "a": "again", "choices": ["again","ago","ally","always","any","and"]},
    {"id": 5,  "q": "「年齢」はどれ？", "a": "age", "choices": ["age","ago","also","all","and","an"]},

    {"id": 6,  "q": "「前」はどれ？", "a": "ago", "choices": ["ago","aunt","apple","about","as","are"]},
    {"id": 7,  "q": "「すべての」はどれ？", "a": "all", "choices": ["all","also","any","an","a","and"]},
    {"id": 8,  "q": "「すでに」はどれ？", "a": "already", "choices": ["already","again","always","ago","and","at"]},
    {"id": 9,  "q": "「もまた」はどれ？", "a": "also", "choices": ["also","always","ago","an","and","all"]},
    {"id": 10, "q": "「いつも」はどれ？", "a": "always", "choices": ["always","ago","ask","apple","at","and"]},

    {"id": 11, "q": "「アメリカ」はどれ？", "a": "America", "choices": ["America","autumn","animal","aunt","April","and"]},
    {"id": 12, "q": "「1つの（特定）」はどれ？", "a": "an", "choices": ["an","a","the","ago","about","all"]},
    {"id": 13, "q": "「～と」はどれ？", "a": "and", "choices": ["and","a","an","ago","about","all"]},
    {"id": 14, "q": "「怒った」はどれ？", "a": "angry", "choices": ["angry","able","again","ago","all","and"]},
    {"id": 15, "q": "「動物」はどれ？", "a": "animal", "choices": ["animal","apple","ago","already","about","also"]},

    {"id": 16, "q": "「りんご」はどれ？", "a": "apple", "choices": ["apple","ago","all","ago","and","an"]},
    {"id": 17, "q": "「4月」はどれ？", "a": "April", "choices": ["April","August","autumn","ate","ago","all"]},
    {"id": 18, "q": "「到着する」はどれ？", "a": "arrive", "choices": ["arrive","ask","again","ago","all","and"]},
    {"id": 19, "q": "「～に」はどれ？", "a": "at", "choices": ["at","and","a","an","ago","all"]},
    {"id": 20, "q": "「おば」はどれ？", "a": "aunt", "choices": ["aunt","ago","animal","apple","all","and"]},

    {"id": 21, "q": "「秋」はどれ？", "a": "autumn", "choices": ["autumn","ago","animal","all","and","at"]},
    {"id": 22, "q": "「悪い」はどれ？", "a": "bad", "choices": ["bad","big","blue","all","and","ago"]},
    {"id": 23, "q": "「カバン」はどれ？", "a": "bag", "choices": ["bag","ball","bat","and","all","ago"]},
    {"id": 24, "q": "「ボール」はどれ？", "a": "ball", "choices": ["ball","bag","blue","bad","ago","all"]},
    {"id": 25, "q": "「銀行」はどれ？", "a": "bank", "choices": ["bank","ball","bat","and","ago","all"]},

    {"id": 26, "q": "「野球」はどれ？", "a": "baseball", "choices": ["baseball","bag","bad","all","and","ago"]},
    {"id": 27, "q": "「美しい」はどれ？", "a": "beautiful", "choices": ["beautiful","big","blue","bad","and","ago"]},
    {"id": 28, "q": "「ベッド」はどれ？", "a": "bed", "choices": ["bed","ball","baseball","ago","all","and"]},
    {"id": 29, "q": "「一番良い」はどれ？", "a": "best", "choices": ["best","big","bad","blue","bag","all"]},
    {"id": 30, "q": "「大きい」はどれ？", "a": "big", "choices": ["big","bad","bag","all","and","ago"]},

    {"id": 31, "q": "「自転車」はどれ？", "a": "bike", "choices": ["bike","ball","bag","baseball","ago","all"]},
    {"id": 32, "q": "「鳥」はどれ？", "a": "bird", "choices": ["bird","ball","big","bad","ago","all"]},
    {"id": 33, "q": "「誕生日」はどれ？", "a": "birthday", "choices": ["birthday","bag","ball","baseball","ago","all"]},
    {"id": 34, "q": "「黒い」はどれ？", "a": "black", "choices": ["black","blue","big","bad","ago","all"]},
    {"id": 35, "q": "「青い」はどれ？", "a": "blue", "choices": ["blue","black","big","bag","ago","all"]},

    {"id": 36, "q": "「本」はどれ？", "a": "book", "choices": ["book","ball","bag","bike","ago","all"]},
    {"id": 37, "q": "「両方」はどれ？", "a": "both", "choices": ["both","ball","bag","bike","ago","all"]},
    {"id": 38, "q": "「少年」はどれ？", "a": "boy", "choices": ["boy","ball","bag","bike","ago","all"]},
    {"id": 39, "q": "「パン」はどれ？", "a": "bread", "choices": ["bread","ball","bag","bike","ago","all"]},
    {"id": 40, "q": "「朝食」はどれ？", "a": "breakfast", "choices": ["breakfast","bread","ball","bike","ago","all"]},

    {"id": 41, "q": "「兄弟」はどれ？", "a": "brother", "choices": ["brother","ball","bag","bike","ago","all"]},
    {"id": 42, "q": "「バス」はどれ？", "a": "bus", "choices": ["bus","ball","bag","bike","ago","all"]},
    {"id": 43, "q": "「忙しい」はどれ？", "a": "busy", "choices": ["busy","ball","bag","bike","ago","all"]},
    {"id": 44, "q": "「買う」はどれ？", "a": "buy", "choices": ["buy","ball","bag","bike","ago","all"]},
    {"id": 45, "q": "「ケーキ」はどれ？", "a": "cake", "choices": ["cake","ball","bag","bike","ago","all"]},

    {"id": 46, "q": "「カメラ」はどれ？", "a": "camera", "choices": ["camera","ball","bag","bike","ago","all"]},
    {"id": 47, "q": "「帽子」はどれ？", "a": "cap", "choices": ["cap","bag","ball","bike","ago","all"]},
    {"id": 48, "q": "「車」はどれ？", "a": "car", "choices": ["car","ball","bag","bike","ago","all"]},
    {"id": 49, "q": "「猫」はどれ？", "a": "cat", "choices": ["cat","ball","bag","bike","ago","all"]},
    {"id": 50, "q": "「いす」はどれ？", "a": "chair", "choices": ["chair","ball","bag","bike","ago","all"]},

    {"id": 51, "q": "「色」はどれ？", "a": "color", "choices": ["color","ball","bag","bike","ago","all"]},
    {"id": 52, "q": "「来る」はどれ？", "a": "come", "choices": ["come","ball","bag","bike","ago","all"]},
    {"id": 53, "q": "「料理する」はどれ？", "a": "cook", "choices": ["cook","ball","bag","bike","ago","all"]},
    {"id": 54, "q": "「国」はどれ？", "a": "country", "choices": ["country","city","bus","ball","ago","all"]},
    {"id": 55, "q": "「踊る」はどれ？", "a": "dance", "choices": ["dance","ball","bag","bike","ago","all"]},

    {"id": 56, "q": "「危険」はどれ？", "a": "danger", "choices": ["danger","ball","bag","bike","ago","all"]},
    {"id": 57, "q": "「日」はどれ？", "a": "day", "choices": ["day","ball","bag","bike","ago","all"]},
    {"id": 58, "q": "「昼」はどれ？", "a": "dinner", "choices": ["dinner","ball","bag","bike","ago","all"]},
    {"id": 59, "q": "「飲む」はどれ？", "a": "drink", "choices": ["drink","eat","bag","ball","ago","all"]},
    {"id": 60, "q": "「卵」はどれ？", "a": "egg", "choices": ["egg","eat","bag","ball","ago","all"]},
]

# 任意でシャッフル関数
def shuffled():
    items = QUESTIONS.copy()
    random.shuffle(items)
    return items
