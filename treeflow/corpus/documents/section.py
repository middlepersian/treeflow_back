from elasticsearch_dsl import Document, Date, Text, Keyword, Nested, Float

class Section(Document):
    id = Keyword()
    text = Nested('TextDocument')
    number = Float()
    identifier = Keyword()
    type = Keyword()
    title = Text()
    language = Keyword()
    source = Keyword()
    tokens = Nested('TokenDocument')
    previous = Nested('SectionDocument')
    container = Nested('SectionDocument')
    meanings = Nested('MeaningDocument')

    created_at = Date()

    class Index:
        name = 'sections'