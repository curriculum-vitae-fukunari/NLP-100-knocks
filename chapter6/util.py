from typing import List


class Token:
    def __init__(self, *,
                 id_: int,
                 word: str,
                 lemma: str,
                 character_offset_begin: int,
                 character_offset_end: int,
                 pos: str,
                 ner: str,
                 speaker: str,):
        self.id_ = id_
        self.word = word
        self.lemma = lemma
        self.character_offset_begin = character_offset_begin
        self.character_offset_end = character_offset_end
        self.pos = pos
        self.ner = ner
        self.speaker = speaker


class Dep:
    def __init__(self, *,
                 type_: str,
                 governor_idx: int,
                 governor: str,
                 dependent_idx: int,
                 dependent: str):
        self.type_ = type_
        self.governor_idx = governor_idx
        self.governor = governor
        self.dependent_idx = dependent_idx
        self.dependent = dependent


class Dependencies:
    def __init__(self, *,
                 type_: str,
                 dep_list: List[Dep]):
        self.type_ = type_
        self.dep_list = list(dep_list)


class Sentence:
    def __init__(self, *,
                 id_: int,
                 token_list: List[Token],
                 dependencies_list: List[Dependencies]):
        self.id_ = id_
        self.token_list = list(token_list)
        self.dependencies_list = list(dependencies_list)


class Mention:
    def __init__(self, *,
                 representative: bool,
                 sentence: int,
                 start: int,
                 end: int,
                 head: int,
                 text: str):
        self.representative = representative
        self.sentence = sentence
        self.start = start
        self.end = end
        self.head = head
        self.text = text


class Coreference:
    def __init__(self, *,
                 mension_list: List[Mention]):
        self.mension_list = list(mension_list)