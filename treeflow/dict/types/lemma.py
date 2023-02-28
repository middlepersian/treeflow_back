
import strawberry
from enum import Enum
from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Optional, Iterable
from treeflow.dict import models
from treeflow.dict.types.language import Language
from django.db.models import Prefetch
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, connections
from strawberry.types import Info
from typing_extensions import Self


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
    created_at: datetime
    related_lemmas: Optional[List['LemmaElastic']] = None
    related_meanings:  Optional[List[gql.LazyType['MeaningElastic', 'treeflow.dict.types.meaning']]] = None

    @classmethod
    def from_hit(cls, hit):
        # Access the source data in the hit
        source = hit['_source']

        # Build and return a new instance of LemmaElastic
        return cls(
            id=relay.to_base64('LemmaElastic', hit['_id']),
            word=source['word'],
            language=source['language'],
            multiword_expression=source['multiword_expression'],
            created_at=source['created_at'],
            related_lemmas=[],
            related_meanings=[]
        )

    @classmethod
    def resolve_id(cls, root: Self, *, info: Optional[Info] = None):
        return root.id

    @classmethod
    def resolve_nodes(
        cls,
        *,
        info: Optional[Info] = None,
        node_ids: Optional[Iterable[str]] = None,
    ):
        if node_ids is not None:
            lemmas = get_lemmas_by_ids(ids=[relay.Node.from_global_id(gid)[1] for gid in node_ids], es_conn=es_conn)
            return [LemmaElastic(id=relay.Node.to_global_id('LemmaElastic', lemma['id']), **lemma) for lemma in lemmas]

        return []

    @classmethod
    def resolve_node(
        cls,
        node_id: str,
        *,
        info: Optional[Info] = None,
        required: bool = False,
    ):
        try:
            lemma = get_lemma_by_id(id=relay.from_base64(node_id)[1], es_conn=es_conn)
            return LemmaElastic(id=node_id, **lemma)
        except Lemma.DoesNotExist:
            if required:
                raise ValueError(f"No lemma by id {node_id}")
            return None


def get_lemma_by_id(id: str) -> Lemma:
    s = Search(using=es_conn, index='lemmas').filter('ids', id=[id])
    response = s.execute()

    if len(response.hits.hits) == 0:
        raise Lemma.DoesNotExist

    return Lemma.from_hit(response.hits.hits[0])


def get_lemmas_by_ids(ids: List[str]) -> List[Lemma]:
    s = Search(using=es_conn, index='lemmas').filter('ids', id=ids)
    response = s.execute()

    lemmas = []
    for hit in response.hits.hits:
        lemma = Lemma.from_hit(hit)
        lemmas.append(lemma)

    return lemmas