from graphene import Enum, ObjectType, Field


class POS(Enum):
    ADJ = 'ADJ'
    ADP = 'ADP'
    ADV = 'ADV'
    AUX = 'AUX'
    CCONJ = 'CCONJ'
    DET = 'DET'
    INTJ = 'INTJ'
    NOUN = 'NOUN'
    NUM = 'NUM'
    PART = 'PART'
    PRON = 'PRON'
    PROPN = 'PROPN'
    PUNCT = 'PUNCT'
    SCONJ = 'SCONJ'
    SYM = 'SYM'
    VERB = 'VERB'
    X = 'X'


class Query(ObjectType):
    pos = Field(POS, description='Part of speech')

    def resolve_pos(root, info, pos):
        return pos
