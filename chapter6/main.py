from typing import List, Tuple, Mapping, Optional
import re

'''
50. 文区切り
(. or ; or : or ? or !) → 空白文字 → 英大文字というパターンを文の区切りと見なし，
入力された文書を1行1文の形式で出力せよ．
'''

# TODO
'''
(. or ; or : or ? or !) → 空白文字 → not 英大文字の場合記号が抜けてしまう。
正規表現で分割しても、もとのマッチした文字列が残るように
'''
with open("./nlp.txt", "r") as file:
    lines: List[str] = file.readlines()

sentences: List[str] = []
for line in lines:
    sentence_top_maybe_small_chars: List[str] = re.split("[.;:?!][\s]", line.strip("\n"))
    if sentence_top_maybe_small_chars[0] == "":
        continue

    sentence: List[str] = []
    for index in range(len(sentence_top_maybe_small_chars)):
        if index == 0:
            sentence.append(sentence_top_maybe_small_chars[index])
        elif sentence_top_maybe_small_chars[index][0].isupper():
            sentence.append(sentence_top_maybe_small_chars[index])
        else:
            sentence.append(sentence_top_maybe_small_chars[index - 1] + " " +
                            sentence_top_maybe_small_chars[index])
    sentences.extend(sentence)

print(sentences)

'''
51. 単語の切り出し
空白を単語の区切りとみなし，50の出力を入力として受け取り，1行1単語の形式で出力せよ．ただし，文の終端では空行を出力せよ．
'''
word_list: List[str] = []
for words in sentences:
    word_list.extend(words.split())
    word_list.append("")

[print(word) for word in word_list]

'''
52. ステミング
51の出力を入力として受け取り，Porterのステミングアルゴリズムを適用し，単語と語幹をタブ区切り形式で出力せよ． 
Pythonでは，Porterのステミングアルゴリズムの実装としてstemmingモジュールを利用するとよい．
'''
from nltk import stem

stemmer: stem.PorterStemmer = stem.PorterStemmer()
word_list_stemmed: List[str] = list(map(lambda x: stemmer.stem(x), word_list))
[print(word_stemmed) for word_stemmed in word_list_stemmed]

'''
53. Tokenization
Stanford Core NLPを用い，入力テキストの解析結果をXML形式で得よ．
また，このXMLファイルを読み込み，入力テキストを1行1単語の形式で出力せよ
'''
'''
Webでも試せるっぽい
http://nlp.stanford.edu:8080/corenlp/

下記より
https://stanfordnlp.github.io/CoreNLP/
$ unzip ./stanford-corenlp-full-2013-06-20.zip -d /usr/local/lib/

/usr/local/lib/ におく

以下をインストール
corenlp-python
'''

'''
以下のように書いてみたが、エラーがでて、解決していない
raise ParserError('Parse error. Could not find "[Text=" in: %s' % line)
corenlp.corenlp.ParserError: 'Parse error. Could not find "[Text=" in: '


import corenlp
import json
import pprint

corenlp_directory: str = "/usr/local/lib/stanford-corenlp-full-2018-01-31/"
parser = corenlp.StanfordCoreNLP(corenlp_path=corenlp_directory)

# パースして結果をpretty print
parsed = parser.parse("I am Alice.")
print(parsed)
'''

'''
直接動かすことにした。
http://lab.astamuse.co.jp/entry/corenlp1

$ ./usr/local.lib/stanford-corenlp-full-2018-01-31/corenlp.sh
NLP> I am Alice 

Sentence #1 (4 tokens):
I am Alice.

Tokens:
[Text=I CharacterOffsetBegin=0 CharacterOffsetEnd=1 PartOfSpeech=PRP Lemma=I NamedEntityTag=O]
[Text=am CharacterOffsetBegin=2 CharacterOffsetEnd=4 PartOfSpeech=VBP Lemma=be NamedEntityTag=O]
[Text=Alice CharacterOffsetBegin=5 CharacterOffsetEnd=10 PartOfSpeech=NNP Lemma=Alice NamedEntityTag=PERSON]
[Text=. CharacterOffsetBegin=10 CharacterOffsetEnd=11 PartOfSpeech=. Lemma=. NamedEntityTag=O]

Dependency Parse (enhanced plus plus dependencies):
root(ROOT-0, Alice-3)
nsubj(Alice-3, I-1)
cop(Alice-3, am-2)
punct(Alice-3, .-4)

テキストファイルを読み込んで、パースした文章をxmlファイルとして出力
$ /usr/local/lib/stanford-corenlp-full-2018-01-31/corenlp.sh 
-file /Users/fukunaritakeshi/PycharmProjects/NLP-100-knocks/chapter6/nlp.txt 
-outputDirectory /Users/fukunaritakeshi/PycharmProjects/NLP-100-knocks/chapter6/
'''
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from chapter6.util import Sentence, Token, Dependencies, Dep, Mention, Coreference

tree: ElementTree = ElementTree.parse("./nlp.txt.xml")
root = tree.getroot()

sentence_list: List[Sentence] = []
sentence_xml_list: List[Element] = root.findall("document/sentences/sentence")
for sentence_xml in sentence_xml_list:

    # sentence_id
    id_: int = int(sentence_xml.attrib["id"])

    # tokens
    token_list: List[Token] = []
    token_xml_list: List[Element] = sentence_xml.findall("tokens/token")
    for token_xml in token_xml_list:
        token: Token = Token(id_=int(token_xml.attrib["id"]),
                             word=token_xml.find("word").text,
                             lemma=token_xml.find("lemma").text,
                             character_offset_begin=int(token_xml.find("CharacterOffsetBegin").text),
                             character_offset_end=int(token_xml.find("CharacterOffsetEnd").text),
                             pos=token_xml.find("POS").text,
                             ner=token_xml.find("NER").text,
                             speaker=token_xml.find("Speaker").text)

        token_list.append(token)

    # dependencies
    dependencies_list: List[Dependencies] = []
    dependencies_xml_list: List[Element] = sentence_xml.findall("dependencies")
    for dependencies_xml in dependencies_xml_list:
        dependencies_type: str = dependencies_xml.attrib["type"]

        dep_list: List[Dep] = []
        dep_xml_list: List[Element] = dependencies_xml.findall("dep")
        for dep_xml in dep_xml_list:
            governor_xml: Element = dep_xml.find("governor")
            dependent_xml: Element = dep_xml.find("dependent")
            dep: Dep = Dep(type_=dep_xml.attrib["type"],
                           governor_idx=int(governor_xml.attrib["idx"]),
                           governor=governor_xml.text,
                           dependent_idx=int(dependent_xml.attrib["idx"]),
                           dependent=dependent_xml.text)

            dep_list.append(dep)

        dependencies: Dependencies = Dependencies(type_=dependencies_type,
                                                  dep_list=dep_list)
        dependencies_list.append(dependencies)

    sentence: Sentence = Sentence(id_=id_,
                                  token_list=token_list,
                                  dependencies_list=dependencies_list)

    sentence_list.append(sentence)

# 共参照表現
coreference_list: List[Coreference] = []
coreference_xml_list: List[Element] = root.findall("document/coreference/coreference")
for coreference_xml in coreference_xml_list:

    mention_list: List[Mention] = []
    mention_xml_list: List[Element] = coreference_xml.findall("mention")
    for mention_xml in mention_xml_list:
        if len(mention_xml.attrib.keys()) != 0 and mention_xml.attrib["representative"] == "true":
            representative: bool = True
        else:
            representative: bool = False
        mention: Mention = Mention(representative=representative,
                                   sentence=int(mention_xml.find("sentence").text),
                                   start=int(mention_xml.find("start").text),
                                   end=int(mention_xml.find("end").text),
                                   head=int(mention_xml.find("head").text),
                                   text=mention_xml.find("text").text)

        mention_list.append(mention)

    coreference: Coreference = Coreference(mension_list=mention_list)
    coreference_list.append(coreference)


'''
入力テキストを1行1単語の形式で出力
'''
for sentence_ in sentence_list:
    for token in sentence_.token_list:
        print(token.word)

'''
54. 品詞タグ付け
Stanford Core NLPの解析結果XMLを読み込み，単語，レンマ，品詞をタブ区切り形式で出力せよ．
'''
for sentence_ in sentence_list:
    for token in sentence_.token_list:
        print(token.word + "\t" + token.lemma + "\t" + token.pos)

'''
55. 固有表現抽出
入力文中の人名をすべて抜き出せ．
'''
for sentence_ in sentence_list:
    for token in sentence_.token_list:
        if token.pos == "NNP":
            print(token.word)

'''
56. 共参照解析
Stanford Core NLPの共参照解析の結果に基づき，文中の参照表現（mention）を代表参照表現（representative mention）に置換せよ．
ただし，置換するときは，「代表参照表現（参照表現）」のように，元の参照表現が分かるように配慮せよ．
'''

sentence_representative_list: List[List[str]] = []
for sentence_ in sentence_list:
    sentence_representative: List[str] = []
    for token_ in sentence_.token_list:
        word: str = token_.word
        # 代表参照表現で置き換えられる単語を見つける
        for coreference_ in coreference_list:
            for mention_ in coreference_.mension_list:
                if mention_.sentence != sentence_.id_:
                    continue
                # 代表参照表現そのものをさしていた時
                if mention_.representative:
                    continue

                # 代表参照表現で置き換えられる単語を見つけた場合(1語のみ)
                if mention_.start == token_.id_ and mention_.end - 1 == token_.id_:
                    representative_word: str = list(filter(lambda x: x.representative, coreference_.mension_list))[
                        0].text
                    word = representative_word + "(" + token_.word + ")"

                # 代表参照表現で置き換えられる単語を見つけた場合(始めの語句)
                elif mention_.start == token_.id_:
                    representative_word: str = list(filter(lambda x: x.representative, coreference_.mension_list))[0].text
                    word = representative_word + "(" + token_.word

                # 代表参照表現で置き換えられる単語を見つけた場合(終わりの語句)
                elif mention_.end - 1 == token_.id_:
                    word = token_.word + ")"
                # 代表参照表現で置き換えられる単語を見つけた場合(真ん中の語句)
                else:
                    pass

        sentence_representative.append(word)
    sentence_representative_list.append(sentence_representative)


# 出力
for sentence_representative_ in sentence_representative_list:
    print(" ".join(sentence_representative_))
    print()


'''
57. 係り受け解析
Stanford Core NLPの係り受け解析の結果（collapsed-dependencies）を有向グラフとして可視化せよ．
可視化には，係り受け木をDOT言語に変換し，Graphvizを用いるとよい．また，Pythonから有向グラフを直接的に可視化するには，pydotを使うとよい．
'''
# dependent -> governor
from pydotplus import Dot, Node, Edge

dot: Dot = Dot(graph_type="digraph")

# 一文目を用いる
for dependencies_ in sentence_list[0].dependencies_list:
    for dep_ in dependencies_.dep_list:
        if sentence_list[0].token_list[dep_.dependent_idx - 1].word == ",":
            continue
        if sentence_list[0].token_list[dep_.governor_idx - 1].word == ",":
            continue
        node_dependent: Node = Node(sentence_list[0].token_list[dep_.dependent_idx - 1].word)
        node_governor: Node = Node(sentence_list[0].token_list[dep_.governor_idx - 1].word)
        dot.add_edge(Edge(node_dependent, node_governor))


dot.write(path="question_57.jpg", format="jpg")


