from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .text import TextDocument
from treeflow.corpus.models import Token

@registry.register_document
class TokenDocument(Document):
    text = fields.ObjectField(properties={'id': fields.KeywordField(), 'title': fields.TextField()})
    lemmas = fields.NestedField(properties={'id': fields.KeywordField(), 'word': fields.KeywordField(), 'language': fields.KeywordField(),})
    meanings = fields.NestedField(properties={'id': fields.KeywordField(), 'meaning': fields.KeywordField(), 'language': fields.KeywordField(),})

    previous = fields.NestedField(properties={'id': fields.KeywordField(), 'number': fields.KeywordField(), 'number_in_sentence': fields.FloatField(),  'transcription': fields.KeywordField(), 'transliteration': fields.KeywordField(),})
    next = fields.NestedField(properties={'id': fields.KeywordField(), 'number': fields.KeywordField(), 'number_in_sentence': fields.FloatField(),  'transcription': fields.KeywordField(), 'transliteration': fields.KeywordField(),})
    # used if multiword_token is True:
    related_tokens = fields.NestedField(properties={'id': fields.KeywordField(),
                                                    'number': fields.KeywordField(),
                                                    'transcription': fields.KeywordField(),
                                                    'transliteration': fields.KeywordField(),})         



    pos_token = fields.NestedField(properties={'id': fields.KeywordField(), 'pos': fields.KeywordField(),})
    feature_token = fields.NestedField(properties={'id': fields.KeywordField(), 'feature': fields.KeywordField(), 'feature_value': fields.KeywordField(),})
    dependency_token = fields.NestedField(properties={'id': fields.KeywordField(), 'head_number': fields.FloatField(), 'rel': fields.KeywordField(),})
    dependency_head = fields.NestedField(properties={'id': fields.KeywordField(), 'head_number': fields.FloatField(), 'rel': fields.KeywordField(),})




    multiword_token_number = fields.NestedField(properties={'number': fields.KeywordField(),})                                                                                     
    class Index:
        name = 'tokens'
        
    class Django:
        model = Token
        fields = [
                'id',
                'number',
                'number_in_sentence',
                'language', 
                'root',
                'word_token',
                'visible',
                'transcription',
                'transliteration',
                'avestan',
                'gloss',
                'created_at',
                'multiword_token',
                
            ]
