import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Optional, Iterable
from treeflow.dict.types.lemma import LemmaElastic
from treeflow.dict.types.meaning import MeaningElastic
from treeflow.corpus import models
from elasticsearch_dsl import Search, connections
from strawberry.types import Info
from elasticsearch.exceptions import NotFoundError
from asgiref.sync import sync_to_async

es_conn =  connections.create_connection(hosts=['elastic:9200'], timeout=20)


@gql.django.filters.filter(models.Token, lookups=True)
class TokenFilter:
    id: relay.GlobalID
    transcription: gql.auto
    transliteration: gql.auto
    language: gql.auto
    number: gql.auto
    text: gql.LazyType['TextFilter', 'treeflow.corpus.types.text']
    section_tokens: gql.LazyType['SectionFilter', 'treeflow.corpus.types.section']


@gql.django.type(models.Token, filters=TokenFilter)
class Token(relay.Node):

    section_tokens: List[gql.LazyType['Section', 'treeflow.corpus.types.section']]
    comment_token: List[gql.LazyType['Comment', 'treeflow.corpus.types.comment']]
    feature_token : List[gql.LazyType['Feature', 'treeflow.corpus.types.feature']]
    pos_token : List[gql.LazyType['POS', 'treeflow.corpus.types.pos']]
    dependency_token : List[gql.LazyType['Dependency', 'treeflow.corpus.types.dependency']]

    id: relay.GlobalID
    number: gql.auto
    number_in_sentence: gql.auto
    root: gql.auto
    word_token: gql.auto
    visible: gql.auto
    text: gql.LazyType['Text', 'treeflow.corpus.types.text']
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: List[gql.LazyType['Lemma', 'treeflow.dict.types.lemma']]
    meanings: List[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]

    avestan: gql.auto
    previous: Optional['Token']
    next: Optional['Token']

    gloss: gql.auto

    multiword_token: gql.auto
    related_tokens: List['Token']


@gql.django.input(models.Token)
class TokenInput:
    number: gql.auto
    number_in_sentence: gql.auto
    text: gql.auto
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: gql.auto
    meanings: gql.auto
    avestan: gql.auto
    previous: gql.auto
    next: gql.auto
    gloss: gql.auto

    multiword_token: gql.auto
    related_tokens: gql.auto



@gql.django.partial(models.Token)
class TokenPartial:
    id: relay.GlobalID
    number: gql.auto
    number_in_sentence: gql.auto
    text: gql.auto
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: gql.auto
    meanings: gql.auto

    avestan: gql.auto
    previous: gql.auto
    next: gql.auto
    gloss: gql.auto

    multiword_token: gql.auto
    related_tokens: gql.auto



@strawberry.type
class POSSelection:
    id: str
    pos: str

    @classmethod
    def from_hit(cls, hit):
        if 'pos_token' in hit:
            pos_tokens = hit['pos_token']
            return [cls(
                id=pos_token['id'],
                pos=pos_token['pos'],
            ) for pos_token in pos_tokens]
        return None

@strawberry.type
class FeatureSelection:
    id: str
    feature: str
    feature_value: str

    @classmethod
    def from_hit(cls, hit):
        if 'feature_token' in hit:
            feature_tokens = hit['feature_token']
            return[ cls(
                id=feature_token['id'],
                feature=feature_token['feature'],
                feature_value=feature_token['feature_value']
            ) for feature_token in feature_tokens]
        return None
        

@strawberry.type
class TokenSelection:
    id: str
    number: float
    number_in_sentence: float
    transcription: str
    transliteration: str

    @classmethod
    def from_hit(cls, hit, field="next"):
        if field in hit:
            return cls(
                id=hit[field]['id'],
                number=hit[field]['number'],
                number_in_sentence=hit[field]['number_in_sentence'],
                transcription=hit[field]['transcription'],
                transliteration=hit[field]['transliteration']
            )
        return None



@strawberry.type
class TokenElastic(relay.Node):
    id: relay.GlobalID
    number: float
    number_in_sentence: float
    language: str
    root: str
    word_token: str
    visible: bool
    transcription: str
    transliteration: str
    avestan: str
    gloss: str
    next: Optional[TokenSelection] = None
    previous: Optional[TokenSelection] = None
    pos_token: Optional[List[POSSelection]] = None
    feature_token: Optional[List[FeatureSelection]] = None
    lemmas: Optional[List[LemmaElastic]] = None
    meanings: Optional[List[MeaningElastic]] = None

    @strawberry.field
    def resolve_id(self: "TokenElastic", info: Optional[Info] = None) -> str:
        return self.id

    @classmethod
    def from_hit(cls, hit):


        # Build and return a new instance of TokenElastic
        return cls(
            id=relay.to_base64(TokenElastic, hit['id']),
            number=hit['number'],
            number_in_sentence=hit['number_in_sentence'],
            language=hit['language'],
            root=hit['root'],
            word_token=hit['word_token'],
            visible=hit['visible'],
            transcription=hit['transcription'],
            transliteration=hit['transliteration'],
            avestan=hit['avestan'],
            gloss=hit['gloss'],
            pos_token=POSSelection.from_hit(hit),
            feature_token=FeatureSelection.from_hit(hit),
            next=TokenSelection.from_hit(hit, field='next'),
            previous=TokenSelection.from_hit(hit,field='previous'),
            lemmas = [LemmaElastic.from_hit(hit_lemma) for hit_lemma in hit['lemmas']],
            meanings = [MeaningElastic.from_hit(hit_meaning) for hit_meaning in hit['meanings']]
        )
    

    @classmethod
    def resolve_node(cls, node_id: str, info: Optional[Info] = None, required: bool = False) -> Optional['TokenElastic']:
        try:
            node = get_token_by_id(id=node_id)
            return TokenElastic.from_hit(node)
        except (relay.GlobalIDValueError, NotFoundError):
            if required:
                raise ValueError(f"No node by id {node_id}")
            return None
        
    @classmethod
    def resolve_nodes(
        cls,
        *,
        info: Optional[Info] = None,
        node_ids: Optional[Iterable[str]] = None
    ):
        if node_ids is not None:
            tokens = get_tokens_by_ids(ids=[relay.from_base64(gid)[1] for gid in node_ids], es_conn=es_conn)
            return [TokenElastic(id=relay.to_base64('TokenElastic', token['id']), **token) for token in tokens]

        return []



    @strawberry.field
    @sync_to_async
    ## TODO check return type
    def token_object(self, info: Optional[Info]) -> Optional[Token]:
        if self.id is not None:
            node_id = relay.from_base64(self.id)[1]
            token = models.Token.objects.get(id=node_id)
            return token
        else:
            return None
    


def get_token_by_id(id: str) -> TokenElastic:
    s = Search(using=es_conn, index='tokens').query('ids', values=[id])
    response = s.execute()

    if len(response.hits.hits) == 0:
        raise NotFoundError(f"No token by id {id}")

    return TokenElastic.from_hit(response.hits.hits[0]['_source'])


def get_tokens_by_ids(ids: List[str]) -> List[TokenElastic]:
    s = Search(index='tokens').query('ids', values=ids)
    response = s.execute()

    tokens = []
    for hit in response.hits.hits:
        token = TokenElastic.from_hit(hit['_source'])
        tokens.append(token)

    return tokens
