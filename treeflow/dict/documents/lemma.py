import strawberry
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from treeflow.dict.models import Lemma


@registry.register_document
class LemmaDocument(Document):

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
