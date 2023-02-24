from elasticsearch_dsl import Document, Date, Integer, Boolean, Text, Keyword, Nested, Object

class TextDocument(Document):
    id = Keyword()
    title = Text()
    identifier = Text()
    language = Keyword(multi=True)
    series = Text()
    label = Text()
    stage = Text()
    editors = Nested(properties={
        'id': Keyword(),
        'username': Text()
    })
    collaborators = Nested(properties={
        'id': Keyword(),
        'username': Text()
    })
    sources = Nested(properties={
        'id': Keyword(),
        'title': Text()
    })
    created_at = Date()

    class Index:
        name = 'texts'
