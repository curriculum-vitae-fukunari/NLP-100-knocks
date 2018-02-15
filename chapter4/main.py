'''
夏目漱石の小説『吾輩は猫である』の文章（neko.txt）をMeCabを使って形態素解析し，
その結果をneko.txt.mecabというファイルに保存せよ．
このファイルを用いて，以下の問に対応するプログラムを実装せよ．
なお，問題37, 38, 39はmatplotlibもしくはGnuplotを用いるとよい．
'''

'''
形態素解析
http://blog.aqutras.com/entry/2016/04/18/210000

文章を文法に基づき形態素（意味をもつ最小単位に分割）に分割し、
品詞などの解析を行う。
その語がどんな品詞で元はどんな形なのかなどを知ることができる。
単語の出現頻度を調べることができる。
応用例は構文解析や単語のベクトル表現など。
'''


'''
mecabと辞書をインストール
$ brew install mecab
$ brew install mecab-ipadic

/usr/local/etc/mecabrc
/usr/local/bin/mecab
/usr/local/bin/mecab-config
'''
'''
動作確認
以下を入力

$ mecab
MeCab はフリーソフトウェアです

実行結果: 
MeCab   名詞,固有名詞,組織,*,*,*,*
は 助詞,係助詞,*,*,*,*,は,ハ,ワ
フリー   名詞,一般,*,*,*,*,フリー,フリー,フリー
ソフトウェア  名詞,一般,*,*,*,*,ソフトウェア,ソフトウェア,ソフトウェア
です  助動詞,*,*,*,特殊・デス,基本形,です,デス,デス
EOS
'''

'''
Python3バインディングのインストール
https://qiita.com/yamaAtsu/items/34e2a04408695365d586
'''

import MeCab

print(MeCab.__file__)

with open("./neko.txt", "r") as file:
    lines = file.readlines()

text = "".join(lines)
# 引数に色々なパーサを指定できる
# tagger = MeCab.Tagger("-Owakati")
tagger = MeCab.Tagger()
persed = tagger.parse(text)

with open("./neko.txt.mecab", "w") as file:
    file.writelines(persed)

'''
30. 形態素解析結果の読み込み
形態素解析結果（neko.txt.mecab）を読み込むプログラムを実装せよ．
ただし，各形態素は表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）
をキーとするマッピング型に格納し，
1文を形態素（マッピング型）のリストとして表現せよ．
第4章の残りの問題では，ここで作ったプログラムを活用せよ．
'''
import re

with open("./neko.txt.mecab") as file:
    lines = file.readlines()

# EOFの行だけ削除する
lines.pop()

dictionary_list = []
for line in lines:

    splited_list = re.split("[\t,]", line)

    surface = splited_list[0]
    base = surface
    pos = splited_list[1]
    pos1 = splited_list[2]

    dictionary = {"surface": surface,
                  "base": base,
                  "pos": pos,
                  "pos1": pos1}

    dictionary_list.append(dictionary)

'''
31. 動詞
動詞の表層形をすべて抽出せよ．
'''
verb_list = []
for dictionary in dictionary_list:
    if dictionary["pos"] == "動詞":
        verb_list.append(dictionary["surface"])

print(verb_list)

'''
33. サ変名詞
サ変接続の名詞をすべて抽出せよ
'''
verb_list = []
for dictionary in dictionary_list:
    if dictionary["pos1"] == "サ変接続":
        verb_list.append(dictionary["surface"])

print(verb_list)

'''
34. 「AのB」
2つの名詞が「の」で連結されている名詞句を抽出せよ．
'''

noun_of_noun = []
for index in range(len(dictionary_list) - 2):
    if dictionary_list[index]["pos"] != "名詞":
        continue
    if dictionary_list[index + 1]["surface"] != "の":
        continue
    if dictionary_list[index + 2]["pos"] != "名詞":
        continue

    noun_of_noun.append(dictionary_list[index]["surface"] +
                        dictionary_list[index + 1]["surface"] +
                        dictionary_list[index + 2]["surface"])

print(noun_of_noun)

'''
35. 名詞の連接
名詞の連接（連続して出現する名詞）を最長一致で抽出せよ．
'''

noun_list = []
noun = []
for dictionary in dictionary_list:
    if dictionary["pos"] == "名詞":
        noun.append(dictionary["surface"])
    else:
        if len(noun) > 0:
            noun_list.append("".join(noun))
            noun = []

print(noun_list)

'''
36. 単語の出現頻度
文章中に出現する単語とその出現頻度を求め，出現頻度の高い順に並べよ
'''
from collections import Counter

word_list = []
for dictionary in dictionary_list:
    word_list.append(dictionary["surface"])

counter = Counter(word_list)
print(counter.most_common())

'''
37. 頻度上位10語
出現頻度が高い10語とその出現頻度をグラフ（例えば棒グラフなど）で表示せよ
'''

'''
ここからttfファイルをダウンロードし、/Library/Fonts/に配置する
https://ipafont.ipa.go.jp/old/ipafont/download.html

参考
https://qiita.com/knknkn1162/items/be87cba14e38e2c0f656
'''

# Seabornが便利だそうで
import seaborn
import matplotlib.pyplot as pyplot

best_10 = counter.most_common(10)
print(best_10)

word_list = []
count_list = []
for word, count in best_10:
    word_list.append(word)
    count_list.append(count)

print(word_list)
print(count_list)

# フォントがみつからない。ふぉんとに？
#pyplot.rcParams["font.family"] = "IPAPGothic"
#pyplot.bar(word_list, count_list)
#pyplot.show()


'''
38. ヒストグラム
単語の出現頻度のヒストグラム（横軸に出現頻度，縦軸に出現頻度をとる単語の種類数を棒グラフで表したもの）を描け．
'''

count_list = []

for count in counter.most_common():
    count_list.append(count[1])

print(count_list)
# pyplot.hist(count_list, bins=10000)
# pyplot.xlim(0,30)
# pyplot.show()

'''
39. Zipfの法則
単語の出現頻度順位を横軸，その出現頻度を縦軸として，両対数グラフをプロットせよ．
'''

# pyplot.plot(range(1, len(count_list) + 1), count_list)
pyplot.loglog(range(1, len(count_list) + 1), count_list)
pyplot.show()

