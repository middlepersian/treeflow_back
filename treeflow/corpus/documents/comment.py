from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from treeflow.corpus.models import Comment

@registry.register_document
class CommentDocument(Document):

    token = fields.ObjectField(properties={
        'id': fields.KeywordField(),
        'transcription': fields.KeywordField(),
    })

    class Index:
        name = 'comments'

    class Django:
        model = Comment
        fields = [
            'id',
            'comment',
        ]


