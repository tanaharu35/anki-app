import random

QUESTIONS = [
{"id":60000,"q":"a few ～","a":"2つ3つの","choices":["2つ3つの","たくさんの","まったくない","ほとんどの","すべての"]},
{"id":60001,"q":"2つ3つの","a":"a few ～","choices":["a few ～","a lot of ～","none of ～","most of ～","all of ～"]},
{"id":60002,"q":"a glass of ～","a":"コップ1杯の～","choices":["コップ1杯の～","1袋の～","多くの～","少しの～","～に到着する"]},
{"id":60003,"q":"コップ1杯の～","a":"a glass of ～","choices":["a glass of ～","a pair of ～","a slice of ～","be full of ～","after school"]},
{"id":60004,"q":"a little too","a":"少し～すぎる","choices":["少し～すぎる","非常に","世界中で","最初は","～がじょうず"]},
{"id":60005,"q":"少し～すぎる","a":"a little too","choices":["a little too","a lot","as usual","be born","at last"]},
{"id":60006,"q":"a lot","a":"非常に","choices":["非常に","しばらくして","1切れの","放課後に","～と違う"]},
{"id":60007,"q":"非常に","a":"a lot","choices":["a lot","a lot of ～","at first","be famous for ～","agree with ～"]},
{"id":60008,"q":"a lot of ～","a":"多くの～","choices":["多くの～","世界中で","1枚の～","最初は","～することができる"]},
{"id":60009,"q":"多くの～","a":"a lot of ～","choices":["a lot of ～","a piece of ～","be able to ～","after a while","be covered with ～"]},
{"id":60010,"q":"a pair of ～","a":"1組の～","choices":["1組の～","1枚の～","コップ1杯の～","ほかの何か","～でいっぱいである"]},
{"id":60011,"q":"1組の～","a":"a pair of ～","choices":["a pair of ～","a glass of ～","be absent from ～","at school","ask ～ for ～"]},
{"id":60012,"q":"a piece of ～","a":"1かけらの～","choices":["1かけらの～","多くの～","放課後に","いつものように","～してうれしい"]},
{"id":60013,"q":"1かけらの～","a":"a piece of ～","choices":["a piece of ～","a sheet of ～","after school","be glad to do","be born"]},
{"id":60014,"q":"a sheet of ～","a":"1枚の～","choices":["1枚の～","1組の～","世界中で","学校で","～に同意する"]},
{"id":60015,"q":"1枚の～","a":"a sheet of ～","choices":["a sheet of ～","a slice of ～","agree with ～","at school","be full of ～"]},
{"id":60016,"q":"a slice of ～","a":"（薄い）1切れの","choices":["（薄い）1切れの","1かけらの～","最初は","～と違う","～を休んでいる"]},
{"id":60017,"q":"（薄い）1切れの","a":"a slice of ～","choices":["a slice of ～","a little too","be absent from ～","at first","be different from ～"]},
{"id":60018,"q":"after a while","a":"しばらくして","choices":["しばらくして","ついに、とうとう","世界中で","～に到着する","～で有名である"]},
{"id":60019,"q":"しばらくして","a":"after a while","choices":["after a while","after school","arrive in[at,on] ～","all over the world","be famous for ～"]},
{"id":60020,"q":"after school","a":"放課後に","choices":["放課後に","学校で","最初は","ほかの何か","～がじょうず"]},
{"id":60021,"q":"放課後に","a":"after school","choices":["after school","at school","anything else","at first","be good at ～"]},
{"id":60022,"q":"agree with ～","a":"～に同意する","choices":["～に同意する","～で覆われている","～でいっぱいである","生まれる","学校で"]},
{"id":60023,"q":"～に同意する","a":"agree with ～","choices":["agree with ～","be covered with ～","be born","at school","be full of ～"]},
{"id":60024,"q":"all over the world","a":"世界中で","choices":["世界中で","放課後に","しばらくして","～に到着する","～と違う"]},
{"id":60025,"q":"世界中で","a":"all over the world","choices":["all over the world","arrive in[at,on] ～","after a while","be different from ～","after school"]},
{"id":60026,"q":"anything else","a":"ほかの何か","choices":["ほかの何か","1枚の～","ついに、とうとう","学校で","～がじょうず"]},
{"id":60027,"q":"ほかの何か","a":"anything else","choices":["anything else","at last","at school","be good at ～","a sheet of ～"]},
{"id":60028,"q":"arrive in[at,on] ～","a":"～に到着する","choices":["～に到着する","～を休んでいる","～に同意する","最初は","～と違う"]},
{"id":60029,"q":"～に到着する","a":"arrive in[at,on] ～","choices":["arrive in[at,on] ～","agree with ～","be absent from ～","at first","be different from ～"]},
{"id":60030,"q":"as ～ as A can","a":"Aができるだけ","choices":["Aができるだけ","ついに、とうとう","学校で","～することができる","生まれる"]},
{"id":60031,"q":"Aができるだけ","a":"as ～ as A can","choices":["as ～ as A can","be able to ～","at last","at school","be born"]},
{"id":60032,"q":"as usual","a":"いつものように","choices":["いつものように","最初は","世界中で","～でいっぱいである","1組の～"]},
{"id":60033,"q":"いつものように","a":"as usual","choices":["as usual","at first","all over the world","be full of ～","a pair of ～"]},
{"id":60034,"q":"ask ～ for ～","a":"～に～を求める","choices":["～に～を求める","～してうれしい","学校で","～に同意する","1枚の～"]},
{"id":60035,"q":"～に～を求める","a":"ask ～ for ～","choices":["ask ～ for ～","be glad to do","at school","agree with ～","a sheet of ～"]},
{"id":60036,"q":"ask ～ to do","a":"Aに～するように頼む","choices":["Aに～するように頼む","～で覆われている","～を休んでいる","放課後に","非常に"]},
{"id":60037,"q":"Aに～するように頼む","a":"ask ～ to do","choices":["ask ～ to do","be covered with ～","be absent from ～","after school","a lot"]},
{"id":60038,"q":"at first","a":"最初は","choices":["最初は","ついに、とうとう","世界中で","～がじょうず","1切れの"]},
{"id":60039,"q":"最初は","a":"at first","choices":["at first","at last","all over the world","be good at ～","a slice of ～"]},
{"id":60040,"q":"at last","a":"ついに、とうとう","choices":["ついに、とうとう","最初は","学校で","生まれる","多くの～"]},
{"id":60041,"q":"ついに、とうとう","a":"at last","choices":["at last","at first","at school","be born","a lot of ～"]},
{"id":60042,"q":"at school","a":"学校で","choices":["学校で","放課後に","世界中で","～を休んでいる","1組の～"]},
{"id":60043,"q":"学校で","a":"at school","choices":["at school","after school","all over the world","be absent from ～","a pair of ～"]},
{"id":60044,"q":"at the end of ～","a":"～の終わりに","choices":["～の終わりに","～で有名である","少し～すぎる","学校で","コップ1杯の～"]},
{"id":60045,"q":"～の終わりに","a":"at the end of ～","choices":["at the end of ～","be famous for ～","a little too","at school","a glass of ～"]},
{"id":60046,"q":"be able to ～","a":"～することができる","choices":["～することができる","～に到着する","1枚の～","最初は","～でいっぱいである"]},
{"id":60047,"q":"～することができる","a":"be able to ～","choices":["be able to ～","arrive in[at,on] ～","a sheet of ～","at first","be full of ～"]},
{"id":60048,"q":"be absent from ～","a":"～を休んでいる","choices":["～を休んでいる","～に同意する","学校で","1かけらの～","世界中で"]},
{"id":60049,"q":"～を休んでいる","a":"be absent from ～","choices":["be absent from ～","agree with ～","at school","a piece of ～","all over the world"]},
{"id":60050,"q":"be born","a":"生まれる","choices":["生まれる","ついに、とうとう","～に～を求める","1組の～","学校で"]},
{"id":60051,"q":"生まれる","a":"be born","choices":["be born","at last","ask ～ for ～","a pair of ～","at school"]},
{"id":60052,"q":"be covered with ～","a":"～で覆われている","choices":["～で覆われている","～でいっぱいである","世界中で","少し～すぎる","～がじょうず"]},
{"id":60053,"q":"～で覆われている","a":"be covered with ～","choices":["be covered with ～","be full of ～","all over the world","a little too","be good at ～"]},
{"id":60054,"q":"be different from ～","a":"～と違う","choices":["～と違う","～に同意する","学校で","多くの～","1切れの"]},
{"id":60055,"q":"～と違う","a":"be different from ～","choices":["be different from ～","agree with ～","at school","a lot of ～","a slice of ～"]},
{"id":60056,"q":"be famous for ～","a":"～で有名である","choices":["～で有名である","～でいっぱいである","しばらくして","最初は","1枚の～"]},
{"id":60057,"q":"～で有名である","a":"be famous for ～","choices":["be famous for ～","be full of ～","after a while","at first","a sheet of ～"]},
{"id":60058,"q":"be full of ～","a":"～でいっぱいである","choices":["～でいっぱいである","～で覆われている","学校で","非常に","1組の～"]},
{"id":60059,"q":"～でいっぱいである","a":"be full of ～","choices":["be full of ～","be covered with ～","at school","a lot","a pair of ～"]},
{"id":60060,"q":"be glad to do","a":"～してうれしい","choices":["～してうれしい","～することができる","ついに、とうとう","1かけらの～","世界中で"]},
{"id":60061,"q":"～してうれしい","a":"be glad to do","choices":["be glad to do","be able to ～","at last","a piece of ～","all over the world"]},
{"id":60062,"q":"be good at ～","a":"～がじょうず","choices":["～がじょうず","～に到着する","学校で","多くの～","最初は"]},
{"id":60063,"q":"～がじょうず","a":"be good at ～","choices":["be good at ～","arrive in[at,on] ～","at school","a lot of ～","at first"]},
]

# 任意でシャッフル関数
def shuffled():
    items = QUESTIONS.copy()
    random.shuffle(items)
    return items





