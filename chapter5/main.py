'''
夏目漱石の小説『吾輩は猫である』の文章（neko.txt）をCaboChaを使って係り受け解析し，
その結果をneko.txt.cabochaというファイルに保存せよ．
このファイルを用いて，以下の問に対応するプログラムを実装せよ．
'''

'''
係り受け解析
http://blog.aqutras.com/entry/2016/04/18/210000

文章を形態素に分けた後、修飾関係の解析を行うこと
語と語の繋がりを理解することができる。
人間にもわかりやすい形式で可視化することも可能
'''

'''
Cabocha
http://chasen.naist.jp/chaki/t/2005-08-29/doc/CaboCha%20Yet%20Another%20Japanese%20Dependency%20Structure%20Analyzer.htm
SVMに基づく高性能な係り受け解析器行うことができる。
'''

'''
インストール

CaboChaを動かすためには以下の3つが必要となる。
* CRF++
* MeCab
* mecab-ipadicなどの辞書ファイル

CRF++

条件付き確率場というものを用いているらしい

brew install crf++
🍺  /usr/local/Cellar/crf++/0.58: 12 files, 719.5KB

brew install cabocha
🍺  /usr/local/Cellar/cabocha/0.69: 27 files, 236MB
'''

'''
CaboChaで始める係り受け解析
https://qiita.com/nezuq/items/f481f07fc0576b38e81d

cabocha -f1
一郎は二郎を描いた絵を三郎に贈った。

* 0 5D 0/1 -0.620584
一郎  名詞,人名,*,*,一郎,いちろう,*
は 助詞,副助詞,*,*,は,は,*
* 1 2D 0/1 1.710282
二郎  名詞,人名,*,*,二郎,じろう,*
を 助詞,格助詞,*,*,を,を,*
* 2 3D 0/0 1.594028
描いた   動詞,*,子音動詞カ行,タ形,描く,えがいた,代表表記:描く
* 3 5D 0/1 -0.620584
絵 名詞,普通名詞,*,*,絵,え,漢字読み:音 代表表記:絵
を 助詞,格助詞,*,*,を,を,*
* 4 5D 0/1 -0.620584
三郎  名詞,人名,*,*,三郎,さぶろう,*
に 助詞,格助詞,*,*,に,に,*
* 5 -1D 0/0 0.000000
贈った   動詞,*,子音動詞ラ行,タ形,贈る,おくった,代表表記:贈る
。 特殊,句点,*,*,。,。,*
EOS

1行目
1. *
2. 文節番号
3. 係り先の文節番号(係り先なし:-1)
4. 主辞の形態素番号/機能語の形態素番号
5. 係り関係のスコア(大きい方が係りやすい)

2行目
1. 表層形 （Tab区切り）
2. 品詞
3. 品詞細分類1
4. 品詞細分類2
5. 品詞細分類3
6. 活用形
7. 活用型
8. 原形
9. 読み
10. 発音
'''

'''
$ cabocha -f1 neko.txt -o neko.txt.cabocha
'''

'''
40. 係り受け解析結果の読み込み（形態素）
形態素を表すクラスMorphを実装せよ．
このクラスは表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）をメンバ変数に持つこととする．
さらに，CaboChaの解析結果（neko.txt.cabocha）を読み込み，各文をMorphオブジェクトのリストとして表現し，
3文目の形態素列を表示せよ．
'''
from typing import List, Tuple
from chapter5.util import Chunk, Morph, ReceivedRelative
import re


def received_relative(item_list: List[str]) -> ReceivedRelative:

    return ReceivedRelative(chunk_number=int(item_list[1]),
                            chunk_number_modifiee=int(item_list[2].strip("D")),
                            morph_number_head=int(item_list[3].split("/")[0]),
                            morph_number_function_word=int(item_list[3].split("/")[1]),
                            score_relation=float(item_list[4]))


def morph(item_list: List[str]) -> Morph:

    # "*"で補完
    while len(split_line) < 10:
        split_line.append("*")

    return Morph(surface=item_list[0],
                 pos=item_list[1],
                 pos1=item_list[2],
                 pos2=item_list[3],
                 pos3=item_list[4],
                 inflection=item_list[5],
                 conjugation=item_list[6],
                 base=item_list[7],
                 syllabary=item_list[8],
                 pronunciation=item_list[9])


with open("./chapter5/neko.txt.cabocha", "r") as file:
    lines: List[str] = file.readlines()

sequences: List[List[str]] = []
sequence: List[str] = []
for line in lines:
    # 文の終わりを表すEOSが入っている場合
    if line == "EOS\n":
        sequences.append(sequence)
        sequence = []
    # 係り受けか、形態素を表している場合
    else:
        sequence.append(line)

sentences: List[List[Chunk]] = []
sentence: List[Chunk] = []
for sequence in sequences:
    if len(sequence) == 0:
        continue

    morph_list: List[Morph] = []
    for index, line in enumerate(sequence):
        split_line: List[str] = re.split("[\t, ]", line.strip("\n"))

        # 形態素を表す行の場合
        if split_line[0] != "*":
            morph_: Morph = morph(item_list=split_line)
            morph_list.append(morph_)
            continue

        # 係りうけを表す行の場合(文の始まりではなく、すでに形態素が読み込まれている時)
        if index != 0:
            # それまでに出現した係り受けと形態素のリストから文節インスタンスをつくり、文リストに追加
            chunk = Chunk(received_relative=received_relative_, morph_list=morph_list)
            sentence.append(chunk)
            morph_list = []

        received_relative_: ReceivedRelative = received_relative(item_list=split_line)

    chunk = Chunk(received_relative=received_relative_, morph_list=morph_list)
    sentence.append(chunk)
    sentences.append(sentence)
    morph_list = []
    sentence = []


# 8文目の中身を確認
for chunk in sentences[8]:
    print(str(chunk))

'''
42. 係り元と係り先の文節の表示
係り元の文節と係り先の文節のテキストをタブ区切り形式ですべて抽出せよ．
ただし，句読点などの記号は出力しないようにせよ．
'''
for sentence in sentences:
    print()
    for index, chunk in enumerate(sentence):
        if index == len(sentence) - 1:
            break
        modifier: str = chunk.surface_words_except_syntax()
        modifiee: str = sentence[chunk.received_relative.chunk_number_modifiee].surface_words_except_syntax()
        print(modifier + "\t" + modifiee)

'''
43. 名詞を含む文節が動詞を含む文節に係るものを抽出
名詞を含む文節が，動詞を含む文節に係るとき，これらをタブ区切り形式で抽出せよ．
ただし，句読点などの記号は出力しないようにせよ．
'''
for sentence in sentences:
    print()
    for index, chunk in enumerate(sentence):
        if index == len(sentence) - 1:
            break
        if not chunk.is_contain_noun():
            continue
        modifier: str = chunk.surface_words_except_syntax()
        if not sentence[chunk.received_relative.chunk_number_modifiee].is_contain_verb():
            continue
        modifiee: str = sentence[chunk.received_relative.chunk_number_modifiee].surface_words_except_syntax()
        print(modifier + "\t" + modifiee)

'''
44. 係り受け木の可視化
与えられた文の係り受け木を有向グラフとして可視化せよ．可視化には，係り受け木をDOT言語に変換し，Graphvizを用いるとよい．
また，Pythonから有向グラフを直接的に可視化するには，pydotを使うとよい．
'''

'''
graphvizのインストールが必要
 brew install graphviz
'''
from pydotplus import Dot, Node, Edge

dot: Dot = Dot(graph_type="digraph")
node_list: List[Tuple[Node, int]] = []
for index, chunk in enumerate(sentences[5]):
    word: str = chunk.surface_words_except_syntax()
    chunk_number_modifiee: int = chunk.received_relative.chunk_number_modifiee
    node: Node = Node(word)
    dot.add_node(node)
    node_list.append((node, chunk_number_modifiee))

for index, node in enumerate(node_list):
    if index == len(node_list) - 1:
        continue
    node_modifier: Node = node[0]
    node_modifee: Node = node_list[node[1]][0]
    dot.add_edge(Edge(node_modifier, node_modifee))

dot.write(path="test.dot.jpg", format="jpg")


'''
45. 動詞の格パターンの抽出
今回用いている文章をコーパスと見なし，日本語の述語が取りうる格を調査したい． 
動詞を述語，動詞に係っている文節の助詞を格と考え，述語と格をタブ区切り形式で出力せよ． 
ただし，出力は以下の仕様を満たすようにせよ．

動詞を含む文節において，最左の動詞の基本形を述語とする
述語に係る助詞を格とする
述語に係る助詞（文節）が複数あるときは，すべての助詞をスペース区切りで辞書順に並べる

「吾輩はここで始めて人間というものを見た」という例文（neko.txt.cabochaの8文目）を考える． 
この文は「始める」と「見る」の２つの動詞を含み，
「始める」に係る文節は「ここで」，
「見る」に係る文節は「吾輩は」と「ものを」と解析された場合は，
次のような出力になるはずである．

始める  で
見る    は を

コーパス中で頻出する述語と格パターンの組み合わせ
「する」「見る」「与える」という動詞の格パターン（コーパス中で出現頻度の高い順に並べよ）
'''

lines: List[str] = []
for sentence in sentences:
    # 動詞を含む文節中の動詞の基本形, 文節の番号を検出する
    verb_and_chunk_number: List[Tuple[str, int]] = []
    for index, chunk in enumerate(sentence):
        if chunk.is_contain_verb():
            for morph in chunk.morph_list:
                if morph.pos == "動詞":
                    verb_and_chunk_number.append((morph.base, index))

    # 助詞を含む文節中の助詞の基本形、係り先の文節番号を検出する
    particle_and_modifee_number: List[Tuple[str, int]] = []
    for index, chunk in enumerate(sentence):
        if chunk.is_contain_particle():
            modifiee_number: int = chunk.received_relative.chunk_number_modifiee
            for morph in chunk.morph_list:
                if morph.pos == "助詞":
                    particle_and_modifee_number.append((morph.base, modifiee_number))

    for verb, chunk_number in verb_and_chunk_number:
        line: str = verb + "\t"
        flag: bool = False  # 諦めた
        for particle, modifiee_number in particle_and_modifee_number:
            if chunk_number == modifiee_number:
                flag = True
                line += " " + particle
        if flag:
            lines.append(line)
            print(line)






