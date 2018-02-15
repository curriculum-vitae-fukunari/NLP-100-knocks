
'''
00. 文字列の逆順
文字列"stressed"の文字を逆に（末尾から先頭に向かって）並べた文字列を得よ．
'''
string = "stressed"
string_inverse = string[::-1]
print(string_inverse)

'''
02. 「パトカー」＋「タクシー」＝「パタトクカシーー」
「パトカー」＋「タクシー」の文字を先頭から交互に連結して文字列「パタトクカシーー」を得よ．
'''
patrol_car = "パトカー"
taxi = "タクシー"
patatokukashi = ""

for patrol_car_char, taxi_char in zip(patrol_car, taxi):
    patatokukashi = patatokukashi + patrol_car_char + taxi_char

print(patatokukashi)

'''
03. 円周率
"Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
という文を単語に分解し，各単語の（アルファベットの）文字数を先頭から出現順に並べたリストを作成せよ．
'''

words = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
words = words.replace(",", "")
words = words.replace(".", "")

words_list = words.split()
list = []
for word in words_list:
    list.append(len(word))

print(list)

'''
04. 元素記号
"Hi He Lied Because Boron Could Not Oxidize Fluorine. 
New Nations Might Also Sign Peace Security Clause. 
Arthur King Can."という文を単語に分解し，
1, 5, 6, 7, 8, 9, 15, 16, 19番目の単語は先頭の1文字，それ以外の単語は先頭に2文字を取り出し，
取り出した文字列から単語の位置（先頭から何番目の単語か）への連想配列（辞書型もしくはマップ型）を作成せよ．
'''

words = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
words = words.replace(".", "")
words_list = words.split()

single = [1, 5, 6, 7, 8, 9, 15, 16, 19]
single_minus1 = []
for number in single:
    single_minus1.append(number - 1)

dictionary = {}
for index, word in enumerate(words_list):
    if index in single_minus1:
        dictionary[word[:1]] = index
    else:
        dictionary[word[:2]] = index

'''
05. n-gram
与えられたシーケンス（文字列やリストなど）からn-gramを作る関数を作成せよ．
この関数を用い，"I am an NLPer"という文から単語bi-gram，文字bi-gramを得よ．
'''
def ngram(words, number):

    list = []
    if len(words) <= number:
        list.append(words)
        return list

    for index in range(len(words) - number + 1):
        list.append(words[index:index + number])
    return list

print(ngram("I am an NLPer", 2))
print(ngram("I am an NLPer".split(), 2))


'''
"paraparaparadise"と"paragraph"に含まれる文字bi-gramの集合を，
それぞれ, XとYとして求め，XとYの和集合，積集合，差集合を求めよ．
さらに，'se'というbi-gramがXおよびYに含まれるかどうかを調べよ．
'''

paraparaparadise = "paraparaparadise"
paragraph = "paragraph"

x = set(ngram(paraparaparadise, 2))
y = set(ngram(paragraph, 2))

union = x & y
intersection = x | y
difference = x - y

print(union)
print(intersection)
print(difference)

print("se" in x)
print("se" in y)
print("se" in x and "se" in y)
print("se" in x or "se" in y)

'''
07. テンプレートによる文生成
引数x, y, zを受け取り「x時のyはz」という文字列を返す関数を実装せよ．
さらに，x=12, y="気温", z=22.4として，実行結果を確認せよ．
'''

def template_(x, y, z):
    return str(x) + "時の" + str(y) + "は" + str(z)

str = template_(x=12, y="気温", z=22.4)
print(str)

'''
08. 暗号文
与えられた文字列の各文字を，以下の仕様で変換する関数cipherを実装せよ．
・英小文字ならば(219 - 文字コード)の文字に置換
・その他の文字はそのまま出力
この関数を用い，英語のメッセージを暗号化・復号化せよ．
'''

def cipher(words):
    trancelated_words = ""
    for char in words:
        if words.isalpha() and words.islower():
            trancelated_words = trancelated_words + chr(219 - ord(char))
        else:
            trancelated_words = trancelated_words + char
    return trancelated_words

str = cipher("cipher")
print(str)
print(cipher(str))

'''
09. Typoglycemia
スペースで区切られた単語列に対して，各単語の先頭と末尾の文字は残し，
それ以外の文字の順序をランダムに並び替えるプログラムを作成せよ．
ただし，長さが４以下の単語は並び替えないこととする．
適当な英語の文
（例えば"I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."）
を与え，その実行結果を確認せよ．
'''
# シャッフルのところがもうちょいきれいにならないか・・・？

words = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
words_list = words.split()

import random
answer = ""
for word in words_list:
    if len(word) <= 4:
        answer = answer + " " + word

    else:
        center_word_list = []
        for center_word_char in word[1:-1]:
            center_word_list.append(center_word_char)

        random.shuffle(center_word_list)

        first = word[0]
        last = word[-1]

        word_more_than_4 = first
        for center_word_char in center_word_list:
            word_more_than_4 = word_more_than_4 + center_word_char
        word_more_than_4 += last

        answer += " " + word_more_than_4

print(answer)



