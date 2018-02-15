from typing import List


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

    def is_contain_noun(self) -> bool:
        """
        文節に名詞が含まれているかどうかを返す
        :return:
        """
        for morph in self.morph_list:
            if morph.pos == "名詞":
                return True
        return False

    def is_contain_verb(self) -> bool:
        """
        文節に動詞が含まれているかどうかを返す
        :return:
        """
        for morph in self.morph_list:
            if morph.pos == "動詞":
                return True
        return False

    def is_contain_particle(self) -> bool:
        """
        文節に助詞が含まれているかどうかを返す
        :return:
        """
        for morph in self.morph_list:
            if morph.pos == "助詞":
                return True
        return False

    def surface_words(self) -> str:
        """
        文節(表層形)を返す
        :return:
        """
        words: str = ""
        for morph in self.morph_list:
            words += morph.surface

        return words

    def surface_words_except_syntax(self) -> str:
        """
        文節(表層形)から記号を除いたもの返す
        :return:
        """
        words: str = ""
        for morph in self.morph_list:
            if morph.pos != "記号":
                words += morph.surface

        return words



