from elasticsearch_dsl import Document, Text, Keyword, Nested, Date


class MeaningDocument(Document):
    id = Keyword()
    meaning = Text()
    language = Keyword()
    related_meanings = Nested('MeaningDocument')
    created_at = Date()

    class Index:
        name = 'meanings'
