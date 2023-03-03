from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from treeflow.dict.models import Meaning


@registry.register_document

class MeaningDocument(Document):

    class Index:
        name = 'meanings'
    class Django:
        model = Meaning
        fields = [
            'id',
            'meaning',
            'language',
        ]
