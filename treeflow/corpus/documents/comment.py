from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Comment

@registry.register_document
class CommentDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'comment'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at', 'updated_at', 'dependency', 'image', 'section_type', 'section', 'source', 'token', 'text', 'uncertain', 'to_discuss', 'new_suggestion', 'lemma', 'meaning', 'semantic']

