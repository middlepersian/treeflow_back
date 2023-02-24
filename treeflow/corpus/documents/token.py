from elasticsearch_dsl import Document, Date, Boolean, Text, Keyword, Nested, Float


class TokenDocument(Document):
    id = Keyword()
    number = Float()
    number_in_sentence = Float()

    root = Boolean()
    word_token = Boolean()
    visible = Boolean()

    text = Nested('TextDocument')

    language = Keyword()
    transcription = Text()
    transliteration = Text()
    lemmas = Nested('TokenLemmaDocument')
    meanings = Nested('TokenMeaningDocument')

    avestan = Text()

    previous = Nested('TokenDocument')

    gloss = Text()

    multiword_token = Boolean()
    multiword_token_number = Nested('TokenDocument')
    related_tokens = Nested('TokenDocument')

    created_at = Date()

    class Index:
        name = 'tokens'

