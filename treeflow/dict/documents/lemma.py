import strawberry
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from treeflow.dict.models import Lemma


@registry.register_document
class LemmaDocument(Document):


    related_meanings = fields.NestedField(properties={'id': fields.KeywordField(), 'meaning': fields.TextField(), 'language': fields.KeywordField()})
    related_lemmas = fields.NestedField(properties={'id': fields.KeywordField(), 'word': fields.KeywordField(), 'language': fields.KeywordField(), 'multiword_expression': fields.BooleanField()})
    class Index:
        name = 'lemmas'
    class Django:
        model = Lemma
        fields = [
            'id',
            'word',
            'language',
            'multiword_expression',
        ]
