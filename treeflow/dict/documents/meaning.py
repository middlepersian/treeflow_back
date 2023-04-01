from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from treeflow.dict.models import Meaning


@registry.register_document

class MeaningDocument(Document):

    related_lemmas = fields.NestedField(properties={'id': fields.KeywordField(), 'word': fields.KeywordField(), 'language': fields.KeywordField()})
    related_meanings = fields.NestedField(properties={'id': fields.KeywordField(), 'meaning': fields.TextField(), 'language': fields.KeywordField()})

    class Index:
        name = 'meanings'
    class Django:
        model = Meaning
        fields = [
            'id',
            'meaning',
            'language',
            'lemma_related'
        ]
