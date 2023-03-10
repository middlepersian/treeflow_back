
import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Optional, Iterable
from treeflow.dict import models
from treeflow.dict.types.language import Language
from treeflow.dict.documents.lemma import LemmaDocument
from elasticsearch_dsl import Search, Q, connections
from strawberry.types import Info
from elasticsearch.exceptions import NotFoundError
from asgiref.sync import sync_to_async


es_conn =  connections.create_connection(hosts=['elastic:9200'], timeout=20)


@gql.django.filters.filter(models.Lemma, lookups=True)
class LemmaFilter:
    id: relay.GlobalID
    word: gql.auto
    language: Language
    multiword_expression: gql.auto


@gql.django.type(models.Lemma, filters=LemmaFilter)
class Lemma(relay.Node):

    token_lemmas:  relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]
    comment_lemma: relay.Connection[gql.LazyType['Comment', 'treeflow.corpus.types.comment']]

    id: relay.GlobalID
    word: gql.auto
    language: Language
    multiword_expression: gql.auto
    related_lemmas: List['Lemma']
    related_meanings: List[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]


@gql.django.input(models.Lemma)
class LemmaInput:
    word: gql.auto
    language: Language
    multiword_expression: gql.auto
    related_lemmas: gql.auto
    related_meanings: gql.auto


@gql.django.partial(models.Lemma)
class LemmaPartial:
    id: relay.GlobalID
    word: gql.auto
    language: Language
    multiword_expression: gql.auto
    related_lemmas: gql.auto
    related_meanings: gql.auto

@gql.django.type(models.Lemma, filters=LemmaFilter)
class Lemma(relay.Node):

    token_lemmas:  relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]
    comment_lemma: relay.Connection[gql.LazyType['Comment', 'treeflow.corpus.types.comment']]

    id: relay.GlobalID
    word: gql.auto
    language: Language
    multiword_expression: gql.auto
    related_lemmas: List['Lemma']
    related_meanings: List[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]


@strawberry.type
class LemmaElastic(relay.Node):

    id: relay.GlobalID
    word: str
    language: str
    multiword_expression: bool


    @classmethod
    def resolve_id(self: "LemmaElastic", info: Optional[Info] = None) -> str:
        return self.id
    
    @classmethod
    def from_hit(cls, hit):
        # Build and return a new instance of LemmaElastic
        return cls(
            id=relay.to_base64(LemmaElastic, hit['id']),
            word=hit['word'],
            language=hit['language'],
            multiword_expression=hit['multiword_expression'],
        )
    @classmethod
    def resolve_nodes(
        cls,
        *,
        info: Optional[Info] = None,
        node_ids: Optional[Iterable[str]] = None):
        if node_ids is not None:
            lemmas = get_lemmas_by_ids(ids=[relay.from_base64(gid)[1] for gid in node_ids], es_conn=es_conn)
            return [LemmaElastic(id=relay.to_base64('LemmaElastic', lemma['id']), **lemma) for lemma in lemmas]

        return []

    @classmethod
    def resolve_node(cls, node_id: str, info: Optional[Info] = None, required: bool = False) -> Optional['LemmaElastic']:
        try:

            #global_id = relay.from_base64(node_id)
            node = get_lemma_by_id(id = node_id)
            return node
        except (relay.GlobalIDValueError, NotFoundError):
            if required:
                raise ValueError(f"No node by id {node_id}")
            return None

    @strawberry.field
    @sync_to_async
    def lemma_object(self, info: Optional[Info]) -> Optional[Lemma]:
        if self.id is not None:
            node_id = relay.from_base64(self.id)[1]
            lemma = models.Lemma.objects.get(id=node_id)
            return lemma
        else:
            return None

def get_lemma_by_id(id: str) -> LemmaElastic:
    s = Search(using=es_conn, index='lemmas').query('ids', values=[id])
    response = s.execute()

    if len(response.hits.hits) == 0:
        raise NotFoundError(f"No lemma by id {id}")

    return LemmaElastic.from_hit(response.hits.hits[0]['_source'])


def get_lemmas_by_ids(ids: List[str]) -> List[LemmaElastic]:
    s = Search(index='lemmas').query('ids', values=ids)
    response = s.execute()

    lemmas = []
    for hit in response.hits.hits:
        lemma = LemmaElastic.from_hit(hit['_source'])
        lemmas.append(lemma)

    return lemmas


