from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from treeflow.corpus.models import Source

@registry.register_document
class SourceDocument(Document):
    id = fields.KeywordField()
    type = fields.KeywordField()
    description = fields.TextField()
    references = fields.NestedField(properties={
        'id': fields.KeywordField(),
        'key': fields.KeywordField(),})

    sources = fields.NestedField(properties={'id': fields.KeywordField(),'identifier': fields.KeywordField()})

    created_at = Date()

    class Index:
        name = 'sources'

    class Django:
        model = Source
        fields = [
            'id',
            'type',
            'identifier',
            'description',
            'created_at',
        ]
