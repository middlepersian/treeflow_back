from elasticsearch_dsl import Document, Date, Integer, Boolean, Text, Keyword, Nested, Float
from .text import TextDocument
class TokenDocument(Document):
    id = Keyword()
    number = Float()
    number_in_sentence = Float()

    root = Boolean()
    word_token = Boolean()
    visible = Boolean()

    text = Nested(TextDocument())

    language = Keyword()
    transcription = Text()
    transliteration = Text()
    lemmas = Nested(TokenLemmaDocument)
    meanings = Nested(TokenMeaningDocument)

    avestan = Text()

    previous = Nested(properties={
        'id': Keyword()
    })

    gloss = Text()

    multiword_token = Boolean()
    multiword_token_number = Nested(properties={
        'number': Float()
    })

    related_tokens = Nested(properties={
        'id': Keyword()
    })

    created_at = Date()

    class Index:
        name = 'tokens'


class TokenLemmaDocument(InnerDoc):
    lemma = Nested(properties={
        'id': Keyword(),
        'word': Keyword(),
        'language': Keyword()
    })
    order = Integer()


class TokenMeaningDocument(InnerDoc):
    meaning = Nested(properties={
        'id': Keyword(),
        'meaning': Keyword(),
        'language': Keyword()
    })
    order = Integer()