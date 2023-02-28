import strawberry
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from treeflow.dict.models import Lemma


@registry.register_document
@strawberry.type
class LemmaDocument(Document):
    related_lemmas = fields.NestedField(
        properties={
            'id': fields.KeywordField(),
            'word': fields.KeywordField(),
        }
    )
    related_meanings = fields.NestedField(
        properties={
            'id': fields.KeywordField(),
            'meaning': fields.TextField(),
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


    
    @staticmethod
    def resolve_node(cls, info, id):
        node_id = relay.Node.from_global_id(id)[1]
        try:
            lemma = get_lemma_by_id(node_id)
            return dict_to_obj(LemmaDocument, lemma.to_dict())
        except Lemma.DoesNotExist:
            return None

    @classmethod
    def resolve_nodes(cls, info, ids):
        node_ids = [relay.Node.from_global_id(gid)[1] for gid in ids]
        lemmas = get_lemmas_by_ids(node_ids)
        return [
            dict_to_obj(LemmaDocument, lemma.to_dict())
            for lemma in lemmas
        ]