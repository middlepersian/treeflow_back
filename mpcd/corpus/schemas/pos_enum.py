from graphene import Enum, ObjectType, Field


class POS(Enum):
    adjective = 'ADJ'
    adposition = 'ADP'
    adverb = 'ADV'
    auxiliary = 'AUX'
    coordinating_conjunction = 'CCONJ'
    determiner = 'DET'
    interjection = 'INTJ'
    noun = 'NOUN'
    numeral = 'NUM'
    particle = 'PART'
    pronoun = 'PRON'
    proper_noun = 'PROPN'
    punctuation = 'PUNCT'
    subordinating_conjunction = 'SCONJ'
    symbol = 'SYM'
    verb = 'VERB'
    other = 'X'

    @property
    def description(self):
        return self.value


class Query(ObjectType):
    pos = Field(POS, description='Part of speech')

    def resolve_pos(root, info, pos):
        return pos
