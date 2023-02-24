from elasticsearch_dsl import Document, Date, Integer, Boolean, Text, Keyword, Nested, Object


class LemmaDocument(Document):
    id = Keyword()
    word = Keyword()
    language = Keyword()
    multiword_expression = Boolean()
    related_lemmas = Nested('LemmaRelationDocument')
    related_meanings = Nested('LemmaMeaningDocument')
    created_at = Date()

    class Index:
        name = 'lemmas'

class LemmaRelationDocument(InnerDoc):
    lemma = Nested(properties={
        'id': Keyword(),
        'word': Keyword(),
        'language': Keyword()
    })
    relation_type = Keyword()

class LemmaMeaningDocument(InnerDoc):
    meaning = Nested(properties={
        'id': Keyword(),
        'language': Keyword(),
        'gloss': Text()
    })

    class Meta:
        # Use `ordering` to specify the order in which the meanings should be sorted
        # when multiple meanings are associated with a lemma
        ordering = ['id']