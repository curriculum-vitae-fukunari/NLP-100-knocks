'''
hightemp.txtは，日本の最高気温の記録を「都道府県」「地点」「℃」「日」のタブ区切り形式で格納したファイルである．
以下の処理を行うプログラムを作成し，hightemp.txtを入力ファイルとして実行せよ．
さらに，同様の処理をUNIXコマンドでも実行し，プログラムの実行結果を確認せよ．
https://github.com/nabehiro/Lang100/blob/master/Lang100/hightemp.txt
'''

'''
10. 行数のカウント
行数をカウントせよ．確認にはwcコマンドを用いよ．
'''
# 1行ずつリストに入る
with open("./hightemp.txt") as file:
    lines = file.readlines()
    print(len(lines))

'''
11. タブをスペースに置換
タブ1文字につきスペース1文字に置換せよ．確認にはsedコマンド，trコマンド，もしくはexpandコマンドを用いよ．
'''
with open("./hightemp.txt") as file:
    lines = file.readlines()

replaced_lines = []
for line in lines:
    replaced_line = line.replace("\t", " ")
    replaced_lines.append(replaced_line)

print(replaced_lines)

'''
12. 1列目をcol1.txtに，2列目をcol2.txtに保存
各行の1列目だけを抜き出したものをcol1.txtに，
2列目だけを抜き出したものをcol2.txtとしてファイルに保存せよ．
確認にはcutコマンドを用いよ．
'''

first_line = replaced_lines[0]
second_line = replaced_lines[1]

first_col = []
second_col = []
for line in replaced_lines:
    first_col.append(line.split()[0] + "\n")
    second_col.append(line.split()[1] + "\n")

with open("./col1.txt", "w") as file:
    file.writelines(first_col)

with open("./col2.txt", "w") as file:
    file.writelines(second_col)

'''
13. col1.txtとcol2.txtをマージ
12で作ったcol1.txtとcol2.txtを結合し，元のファイルの1列目と2列目をタブ区切りで並べたテキストファイルを作成せよ．
確認にはpasteコマンドを用いよ．
'''
# まだ解けていない
with open("./col1.txt") as file:
    col1 = file.readlines()
    print(col1)

with open("./col2.txt") as file:
    col2 = file.readlines()
    print(col2)

merged_lines = []
for row in range(len(col1)):
    merged_lines.append(col1[row].replace("\n", " ") + col2[row])

with open("./merged.txt", "w") as file:
    file.writelines(merged_lines)

'''
14. 先頭からN行を出力
自然数Nをコマンドライン引数などの手段で受け取り，
入力のうち先頭のN行だけを表示せよ．
確認にはheadコマンドを用いよ．
'''
# 入力部
count = 5

with open("./hightemp.txt", "r") as file:
    lines = file.readlines()

for index in range(count):
    print(lines[index])

'''
16. ファイルをN分割する
自然数Nをコマンドライン引数などの手段で受け取り，入力のファイルを行単位でN分割せよ．
同様の処理をsplitコマンドで実現せよ．
'''
# 元の数をN等分した値のリストを返す
def split_list(original_count, split_count):
    quo = original_count // split_count
    mod = original_count % split_count

    list = []
    for _ in range(split_count):
        list.append(quo)

    for index in range(mod):
        list[index] += 1

    return list

N = 5
with open("./hightemp.txt", "r") as file:
    lines = file.readlines()

splited = split_list(original_count=len(lines), split_count=N)

for index, value in enumerate(splited):
    list = []
    for count in range(value):
        list.append(lines.pop(0))

    filename_path = "./hightemp_" + str(index) + ".txt"
    with open(filename_path, "w") as file:
        file.writelines(list)

'''
17. １列目の文字列の異なり
1列目の文字列の種類（異なる文字列の集合）を求めよ．
確認にはsort, uniqコマンドを用いよ．
'''
with open("./hightemp.txt", "r") as file:
    lines = file.readlines()

lines_col1 = []
for line in lines:
    lines_col1.append(line.split("\t")[0])

col1_set = set(lines_col1)
print(col1_set)

'''
18. 各行を3コラム目の数値の降順にソート
各行を3コラム目の数値の逆順で整列せよ（注意: 各行の内容は変更せずに並び替えよ）．
確認にはsortコマンドを用いよ（この問題はコマンドで実行した時の結果と合わなくてもよい）．
'''
with open("./hightemp.txt", "r") as file:
    lines = file.readlines()

lines_two_dimensions = []
for line in lines:
    lines_two_dimensions.append(line.split("\t"))

# ラムダ式は要復習
lines_two_dimensions.sort(key=lambda x:x[2])
lines_two_dimensions.reverse()

print(lines_two_dimensions)

'''
19. 各行の1コラム目の文字列の出現頻度を求め，出現頻度の高い順に並べる
各行の1列目の文字列の出現頻度を求め，その高い順に並べて表示せよ．
確認にはcut, uniq, sortコマンドを用いよ．
'''
from collections import Counter

with open("./hightemp.txt", "r") as file:
    lines = file.readlines()

lines_col1 = []
for line in lines:
    lines_col1.append(line.split("\t")[0])

counter = Counter(lines_col1)
print(counter.most_common())

