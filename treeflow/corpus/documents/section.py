from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from treeflow.corpus.models import Section

@registry.register_document
class SectionDocument(Document):
    id = fields.KeywordField()
    text = fields.ObjectField(properties={id: fields.KeywordField(), title: fields.TextField()})
    tokens = Nested(properties={
        'id': fields.KeywordField(),
        'transcription': fields.KeywordField(),
    })
    previous = fields.ObjectField(properties={id: fields.KeywordField(), identifier: fields.TextField()})
    container = fields.ObjectField(properties={id: fields.KeywordField(), identifier: fields.TextField()})
    meanings = fields.NestedField(properties={
        'id': fields.KeywordField(),
        'meaning': fields.KeywordField(),
        'language': fields.KeywordField(),
    })

    created_at = Date()

    class Index:
        name = 'sections'

    class Django:
        model = Section
        fields = [
            'id',
            'number',
            'identifier',
            'type',
            'title',
            'language',
            'source',
            'created_at',
        ]    
