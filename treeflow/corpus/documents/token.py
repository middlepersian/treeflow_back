from elasticsearch_dsl import token_filter, analyzer
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from treeflow.corpus.models import Token

stopword_list = [
    "ā", "abāg", "abar", "abārīg", "abāz", "abē", "ag", "agar", "amāh", "ān", "and", 
    "andar", "ānōh", "ašmā", "ašmāh", "awēšān", "awiš", "ayāb", "az", "aziš", "be", 
    "bē", "čand", "čē", "čiyōn", "did", "ēč", "ēd", "ēdōn", "ēg", "ēk", "ēn", "ēw", 
    "hād", "ham", "hamē", "harw", "ī", "im", "imān", "iš", "išān", "it", "itān", "iz", 
    "jud", "ka", "kas", "kē", "kū", "m", "man", "mān", "nē", "om", "ō", "ōh", "ōy", 
    "ōwōn", "pad", "padiš", "pas", "pēš", "rāy", "š", "šān", "t", "tā", "tān", "tis", 
    "tō", "u", "ud", "w", "was", "xwad", "xwēš", "y", "z", "_"
]
custom_stopwords = token_filter('custom_stopwords', type='stop', stopwords=stopword_list)
stopword_analyzer = analyzer('stopword_analyzer', tokenizer='standard', filter=['lowercase', custom_stopwords])


@registry.register_document
class TokenDocument(Document):
    transcription = fields.TextField(
        analyzer='standard',
        fields={
            'with_stop': fields.TextField(analyzer='stopword_analyzer')
        }
    )
    transliteration =  fields.KeywordField()
    text = fields.ObjectField(properties={'id': fields.KeywordField(), 'title': fields.TextField(), 'identifier': fields.KeywordField()})
    image = fields.ObjectField(properties={'id': fields.KeywordField(), 'identifier': fields.KeywordField()})
    lemmas = fields.NestedField(properties={'id': fields.KeywordField(), 'word': fields.KeywordField(), 'language': fields.KeywordField(), 'multiword_expression': fields.KeywordField()})
    meanings = fields.NestedField(properties={'id': fields.KeywordField(), 'meaning': fields.KeywordField(), 'language': fields.KeywordField(),})
    section_tokens = fields.NestedField(properties={'id': fields.KeywordField(), 'type': fields.KeywordField(), 'identifier': fields.KeywordField(),})

    previous = fields.NestedField(properties={
        'id': fields.KeywordField(),
        'number': fields.KeywordField(),
        'number_in_sentence': fields.FloatField(),
        'transcription': fields.TextField(
            analyzer='standard',
            fields={
                'with_stop': fields.TextField(analyzer='stopword_analyzer')
            }
        ),
        'transliteration': fields.KeywordField(),
    })    
    next = fields.NestedField(properties={
        'id': fields.KeywordField(),
        'number': fields.KeywordField(),
        'number_in_sentence': fields.FloatField(),
        'transcription': fields.TextField(
            analyzer='standard',
            fields={
                'with_stop': fields.TextField(analyzer='stopword_analyzer')
            }
        ),
        'transliteration': fields.KeywordField(),
    })
    pos_token = fields.NestedField(properties={'id': fields.KeywordField(), 'pos': fields.KeywordField(),})
    feature_token = fields.NestedField(properties={'id': fields.KeywordField(), 'feature': fields.KeywordField(), 'feature_value': fields.KeywordField(),})
    dependency_token = fields.NestedField(properties={'id': fields.KeywordField(), 'head_number': fields.FloatField(), 'rel': fields.KeywordField(),})
    dependency_head = fields.NestedField(properties={'id': fields.KeywordField(), 'head_number': fields.FloatField(), 'rel': fields.KeywordField(),})
    multiword_token_number = fields.NestedField(properties={'number': fields.KeywordField(),})           
                                                                              
    class Index:
        name = 'tokens'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'analysis': {
                'filter': {
                    'custom_stopwords': {
                        'type': 'stop',
                        'stopwords': stopword_list
                    },
                },
                'analyzer': {
                    'stopword_analyzer': {
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': ['lowercase', 'custom_stopwords']
                    },
                }
            }
        }

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
                'avestan',
                'gloss',
                'multiword_token',
            ]
