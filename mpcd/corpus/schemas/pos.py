from graphene import Enum


class POS(Enum):
    adjective = 'ADJ',
    adposition = 'ADP',
    adverb = "ADV",
    auxiliary = "AUX"
    coordinating_conjunction = "CCONJ"
    determiner = "DET",
    interjection = "INTJ",
    noun = "NOUN"
    numeral = "NUM"
    particle = "PART"
    pronoun = "PRON"
    proper_noun = "PROPN"
    punctuation = "PUNCT"
    subordinating_conjunction = "SCONJ"
    symbol = "SYM"
    verb = "VERB"
    other = "X"
