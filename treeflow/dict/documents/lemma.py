from django_elasticsearch_dsl import Document, fields
from treeflow.dict.models import Lemma

class LemmaDocument(Document):
    related_lemmas = fields.NestedField(
        properties={
            'id': {'type': 'keyword'},
            'word': {'type': 'keyword'},
            'language': {'type': 'keyword'},
            'multiword_expression': {'type': 'boolean'},
            'related_lemmas': {'type': 'nested', 'properties': {'id': {'type': 'keyword'}}},
            'related_meanings': {'type': 'nested', 'properties': {'id': {'type': 'keyword'}}},
            'created_at': {'type': 'date'}
        }
    )
    related_meanings = fields.NestedField(
        properties={
            'id': {'type': 'keyword'},
            'meaning': {'type': 'text'},
            'language': {'type': 'keyword'},
            'related_meanings': {'type': 'nested', 'properties': {'id': {'type': 'keyword'}}},
            'created_at': {'type': 'date'}
        }
    )
    class Index:
        name = 'lemmas'
    class Django:
        model = Lemma
        fields = [
            'id',
            'word',
            'language',
            'multiword_expression',
            'created_at',
        ]