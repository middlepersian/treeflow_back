from elasticsearch_dsl import Document, Date, Integer, Boolean, Text, Keyword, Nested, Object


class LemmaDocument(Document):
    id = Keyword()
    word = Keyword()
    language = Keyword()
    multiword_expression = Boolean()
    related_lemmas = Nested('LemmaDocument')
    related_meanings = Nested('MeaningDocument')
    created_at = Date()


    class Meta:
        # Use `ordering` to specify the order in which the meanings should be sorted
        # when multiple meanings are associated with a lemma
        ordering = ['id']