from django_elasticsearch_dsl import Document, fields
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

        dependency = fields.ObjectField(properties={'feature': fields.TextField(), 'value': fields.TextField()})

    class Django:
        model = Comment
        fields = ['id', 'comment', 'created_at', 'updated_at']

