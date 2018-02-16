from typing import List, Tuple, Optional, Iterator
from enum import Enum


class PartOfSpeech(Enum):
    """
    品詞の列挙子
    """
    NOUN = "名詞"
    VERB = "動詞"
    PARTICLE = "助詞"
    CONJUCTION = "接続詞"
    DETERMINER = "連体詞"
    ADVERB = "副詞"
    ADJECTIVE = "形容詞"
    AUXILIARY_VERB = "助動詞"
    SYNTAX = "記号"


class Morph:
    """
    形態素を表すクラス
    """
    def __init__(self,
                 surface: str,
                 pos: str,
                 pos1: str,
                 pos2: str,
                 pos3: str,
                 inflection: str,
                 conjugation: str,
                 base: str,
                 syllabary: str,
                 pronunciation: str):
        self.surface = surface              # 表層形
        self.pos = pos                      # 品詞
        self.pos1 = pos1                    # 品詞細分類1
        self.pos2 = pos2                    # 品詞細分類2
        self.pos3 = pos3                    # 品詞細分類3
        self.inflection = inflection        # 活用形
        self.conjugation = conjugation      # 活用型
        self.base = base                    # 原型
        self.syllabary = syllabary          # 読み
        self.pronunciation = pronunciation  # 発音


class ReceivedRelative:
    """
    係り受けに関する情報を保持するクラス
    """
    def __init__(self,
                 chunk_number: int,
                 chunk_number_modifiee: int,
                 morph_number_head: int,
                 morph_number_function_word: int,
                 score_relation: float):
        self.chunk_number = chunk_number                              # 文節番号
        self.chunk_number_modifiee = chunk_number_modifiee            # 係り先の文節番号(係り先なし:-1)
        self.morph_number_head = morph_number_head                    # 主辞の形態素番号
        self.morph_number_function_word = morph_number_function_word  # 機能語の形態素番号
        self.score_relation = score_relation                          # 係り関係のスコア(大きい方が係りやすい)


class Chunk:
    """
    文節を表すクラス
    一つの係り受けの情報と、複数の形態素を情報として持つ
    """
    def __init__(self,
                 received_relative: ReceivedRelative,
                 morph_list: List[Morph]):
        self.received_relative = received_relative  # 係り受けのオブジェクト
        self.morph_list = morph_list                # 形態素のリスト

    def __str__(self) -> str:
        print(vars(self.received_relative))
        for morph in self.morph_list:
            print(vars(morph))

        return ""

    def chunk_number(self) ->int:
        """
        文節番号を返す
        :return:
        """
        return self.received_relative.chunk_number

    def modifiee_number(self) -> int:
        """
        係り先の文節の番号を返す
        係り先が存在しない場合、-1を返す
        :return:
        """
        return self.received_relative.chunk_number_modifiee

    def is_contain(self, *, pos: PartOfSpeech=None) -> bool:
        """
        文節に引数で指定した品詞が含まれているかどうかを返す
        引数を指定しなかったり、Noneを指定すると常にTrueを返す
        :return:
        """
        if not pos:
            return True

        return pos.value in map(lambda x: x.pos, self.morph_list)

    def surface_words(self, *, pos: PartOfSpeech=None, need_syntax=False) -> Optional[str]:
        """
        :param pos: 指定した品詞が含まれているなら文節全体、含まれていなければNoneを返す
        :param need_syntax: Falseだと記号の除いたものを返す
        :return:
        """
        # 品詞を指定しており、かつその品詞が文節に含まれていない場合、Noneを返す
        if not self.is_contain(pos=pos):
            return None

        morph_map: Iterator = self.morph_list
        if not need_syntax:
            morph_map = filter(lambda x: x.pos != PartOfSpeech.SYNTAX.value, morph_map)
        morph_map = map(lambda x: x.surface, morph_map)

        return "".join(morph_map)

        # if need_syntax:
        #     morph_surface_map: Iterator = map(lambda x: x.surface, self.morph_list)
        #     return "".join(morph_surface_map)
        # else:
        #     morph_map_except_syntax: Iterator = filter(lambda x: x.pos != PartOfSpeech.SYNTAX.value, self.morph_list)
        #     morph_surface_map: Iterator = map(lambda x: x.surface, morph_map_except_syntax)
        #     return "".join(morph_surface_map)

    def base_word(self, *, pos: PartOfSpeech) -> Optional[str]:
        """
        文節に引数で指定した品詞が含まれているならその基本形、
        含まれていなければNoneを返す
        :return:
        """
        morph_map: Iterator = filter(lambda x: x.pos == pos.value, self.morph_list)
        morph_list: List[Morph] = list(morph_map)

        return morph_list[0].base if len(morph_list) >= 0 else None


def relative_pair(*,
                  chunk_list: List[Chunk],
                  modifier_contains_pos: PartOfSpeech=None,
                  modifiee_contains_pos: PartOfSpeech=None) -> List[Tuple[Chunk, Chunk]]:
    """
    文中の係り受け元と係り受け先の文節のペアを返す
    :param chunk_list: 文中の文節のリスト
    :param modifier_contains_pos: 係り受け元に含まれる品詞、指定した品詞にマッチしたもののみを抽出する
    :param modifiee_contains_pos: 係り受け先に含まれる品詞、指定した品詞にマッチしたもののみを抽出する
    :return:
    """
    pair_map: Iterator[Tuple[Chunk, Chunk]] = map(lambda x: (x, chunk_list[x.modifiee_number()]), chunk_list)

    pair_map = filter(lambda x: x[0].is_contain(pos=modifier_contains_pos), pair_map)
    pair_map = filter(lambda x: x[1].is_contain(pos=modifiee_contains_pos), pair_map)

    return list(pair_map)

    # pair_list: List[Tuple[Chunk, Chunk]] = []
    # for chunk in chunk_list[:-2]:
    #     modifiee_chunk: Chunk = chunk_list[chunk.modifiee_number()]
    #     if not modifier_contains_pos and not modifiee_contains_pos:
    #         pair_list.append((chunk, modifiee_chunk))
    #     elif modifier_contains_pos and not modifiee_contains_pos:
    #         if chunk.is_contain(pos=modifier_contains_pos):
    #             pair_list.append((chunk, modifiee_chunk))
    #     elif not modifier_contains_pos and modifiee_contains_pos:
    #         if modifiee_chunk.is_contain(pos=modifiee_contains_pos):
    #             pair_list.append((chunk, modifiee_chunk))
    #     else:
    #         if chunk.is_contain(pos=modifier_contains_pos) and modifiee_chunk.is_contain(pos=modifiee_contains_pos):
    #             pair_list.append((chunk, modifiee_chunk))
    #
    # return pair_list

def modifiee_modifiers(*,
                       chunk_list: List[Chunk],
                       modifier_contains_pos: PartOfSpeech = None,
                       modifiee_contains_pos: PartOfSpeech = None) -> List[Tuple[Chunk, List[Chunk]]]:

    modifiee_modifiers_list: List[Tuple[Chunk, List[Chunk]]] = []
    for chunk in chunk_list:
        # 係り受け先が指定した品詞かどうか
        if not chunk.is_contain(pos=modifiee_contains_pos):
            continue
        # 係り受け元であり、かつ係り受け元の品詞が指定した品詞と一致するものみ抽出
        modifiers_map: Iterator[Chunk] = filter(lambda x: x.modifiee_number() == chunk.chunk_number()
                                                and x.is_contain(pos=modifier_contains_pos),
                                                chunk_list)

        modifiers_list: List[Chunk] = list(modifiers_map)
        # 係り受け元が存在するかどうか
        if len(modifiers_list) == 0:
            continue

        modifiee_modifiers_: Tuple[Chunk, List[Chunk]] = (chunk, modifiers_list)
        modifiee_modifiers_list.append(modifiee_modifiers_)

    return modifiee_modifiers_list











