
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import BibEntry

@registry.register_document
class BibEntryDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'bibentry'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = BibEntry # The model associated with this Document
        fields = ['key']            