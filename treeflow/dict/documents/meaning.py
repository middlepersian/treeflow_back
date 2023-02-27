from django_elasticsearch_dsl import Document, fields
from treeflow.dict.models import Meaning



class MeaningDocument(Document):
    related_meanings = fields.NestedField(
        properties={
            'id': fields.KeywordField(),
            'meaning': fields.TextField(),
            'language': fields.KeywordField(),
            'related_meanings': fields.NestedField(properties={'id': fields.KeywordField()}),
            'created_at': fields.DateField(),
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
