from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from treeflow.corpus.models import Text
@registry.register_document
class TextDocument(Document):
    

    editors = fields.NestedField(properties={
        'id': fields.KeywordField(),
        'username': fields.TextField()
    })
    collaborators = fields.NestedField(properties={
        'id': fields.KeywordField(),
        'username': fields.TextField()
    })

    sources = fields.NestedField(properties={'id':fields.KeywordField(), 'identifier': fields.KeywordField(),})

    language = fields.NestedField(properties={'language': fields.TextField(), })

    class Index:
        name = 'texts'

    class Django:
        model = Text
        fields = [
            'id',
            'title',
            'identifier',
            'series',
            'label',
            'stage',
            'created_at',
        ]    
