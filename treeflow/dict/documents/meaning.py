from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from treeflow.dict.models import Meaning


@registry.register_document

class MeaningDocument(Document):
    related_meanings = fields.NestedField(
        properties={
            'id': fields.KeywordField(),
            'meaning': fields.TextField(),
        }
    )
    class Index:
        name = 'meanings'
    class Django:
        model = Meaning
        fields = [
            'id',
            'meaning',
            'language',
            'created_at',
        ]
