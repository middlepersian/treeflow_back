from elasticsearch_dsl import token_filter, analyzer
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from treeflow.corpus.models import Section


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
class SectionDocument(Document):
    text = fields.ObjectField(properties={'id': fields.KeywordField(), 'title': fields.TextField()})
    
    tokens = fields.NestedField(properties={
        'id': fields.KeywordField(),
        'number': fields.FloatField(),
        'number_in_sentence': fields.FloatField(),
        'root': fields.BooleanField(),
        'word_token': fields.BooleanField(),
        'visible': fields.BooleanField(),
        'transcription': fields.TextField(
            analyzer='standard',
            fields={
                'no_stop': fields.TextField(analyzer='stopword_analyzer')
            }
        ),
        'transliteration': fields.KeywordField(),
        'lemmas': fields.NestedField(properties={
            'id': fields.KeywordField(),
            'word': fields.KeywordField(),
        }),
        'meanings': fields.NestedField(properties={
            'id': fields.KeywordField(),
            'meaning': fields.KeywordField(),
        }),
        'language': fields.KeywordField(),
        'avestan': fields.TextField(),
        'previous': fields.ObjectField(properties={
            'id': fields.KeywordField(),
            'transcription': fields.TextField(
            analyzer='standard',
            fields={
                'no_stop': fields.TextField(analyzer='stopword_analyzer')}),
            'transliteration': fields.KeywordField(),
        }),
        'gloss': fields.TextField(),
        'multiword_token': fields.BooleanField(),
        'created_at': fields.DateField(),
    })

    previous = fields.ObjectField(properties={'id': fields.KeywordField(), 'identifier': fields.TextField()})
    container = fields.ObjectField(properties={'id': fields.KeywordField(), 'identifier': fields.TextField()})
    meanings = fields.NestedField(properties={
        'id': fields.KeywordField(),
        'meaning': fields.KeywordField(),
        'language': fields.KeywordField(),
    })
    source = fields.ObjectField(properties={'id': fields.KeywordField(), 'identifier': fields.TextField()})
    
    class Index:
        name = 'sections'
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
        model = Section
        fields = [
            'id',
            'number',
            'identifier',
            'type',
            'title',
            'language',
            'created_at',
        ]
