import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Optional, Iterable
from treeflow.dict import models
from strawberry.types import Info
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Search
from asgiref.sync import sync_to_async
from treeflow.dict.types.lemma import MeaningSelection, LemmaSelection
from treeflow.dict.enums.language import Language
from treeflow.dict.enums.dict_stage import DictStage


@gql.django.filters.filter(models.Meaning, lookups=True)
class MeaningFilter:
    id: relay.GlobalID
    meaning: gql.auto
    language: Language
    lemma_related : bool
    stage : Optional[DictStage]


@gql.django.type(models.Meaning, filters=MeaningFilter)
class Meaning(relay.Node):

    token_meanings:  relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]
    sentence_meanings:  relay.Connection[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]
    comment_meaning: relay.Connection[gql.LazyType['Comment', 'treeflow.corpus.types.comment']]

    id: relay.GlobalID
    meaning: gql.auto
    language: Language
    lemma_related : Optional[bool]
    stage : Optional[DictStage]
    related_meanings: List['Meaning']
    related_lemmas: List[gql.LazyType['Lemma', 'treeflow.dict.types.lemma']]


@gql.django.input(models.Meaning)
class MeaningInput:
    meaning: gql.auto
    language: Language
    lemma_related : Optional[bool]
    stage : Optional[DictStage]
    related_meanings: gql.auto


@gql.django.partial(models.Meaning)
class MeaningPartial:
    id: relay.GlobalID
    meaning: gql.auto
    language: Language
    lemma_related : Optional[bool]
    stage : Optional[DictStage]
    related_meanings: gql.auto



@strawberry.type
class MeaningElastic(relay.Node):

    id: relay.GlobalID
    language: Language
    stage : Optional[DictStage]
    meaning: str
    lemma_related : Optional[bool]
    related_meanings: Optional[List[MeaningSelection]] = None
    related_lemmas: Optional[List[LemmaSelection]] = None

    @classmethod
    def resolve_id(self: "MeaningElastic", info: Optional[Info] = None) -> str:
        return self.id
    
    @classmethod
    def from_hit(cls, hit):
        # Access the source data in the hit
        # Build and return a new instance of MeaningElastic
        return cls(
            id=relay.to_base64(MeaningElastic, hit['id']),
            language=hit['language'],
            meaning=hit['meaning'],
            lemma_related=hit['lemma_related'],
            related_meanings=MeaningSelection.from_hit(hit, field='related_meanings'),
            related_lemmas=LemmaSelection.from_hit(hit, field='related_lemmas')

        )

    @classmethod
    def resolve_nodes(
        cls,
        *,
        info: Optional[Info] = None,
        node_ids: Optional[Iterable[str]] = None):
        if node_ids is not None:
            meanings = get_meanings_by_ids(ids=[relay.from_base64(gid)[1] for gid in node_ids], es_conn=es_conn)
            return [MeaningElastic(id=relay.to_base64('MeaningElastic', meaning['id']), **meaning) for meaning in meanings]

        return []

    @classmethod
    def resolve_node(cls, node_id: str, info: Optional[Info] = None, required: bool = False) -> Optional['MeaningElastic']:
        try:
            meaning = get_meaning_by_id(id=node_id)
            return meaning
        except (relay.GlobalIDValueError, NotFoundError):
            if required:
                raise ValueError(f"No node by id {node_id}")
            return None

    @strawberry.field
    @sync_to_async
    def meaning_object(self, info: Optional[Info]) -> Optional[Meaning]:
        if self.id is not None:
            meaning_id = relay.from_base64(self.id)[1]
            meaning = models.Meaning.objects.get(id=meaning_id)
            return meaning
        else:
            return None

def get_meaning_by_id(id: str) -> MeaningElastic:
    s = Search(index='meanings').query('ids', values=[id])
    response = s.execute()

    if len(response.hits.hits) == 0:
        raise NotFoundError(f"No meaning by id {id}")

    return MeaningElastic.from_hit(response.hits.hits[0])

def get_meanings_by_ids(ids: List[str]) -> List[MeaningElastic]:
    s = Search(index='meanings').query('ids', values=ids)
    response = s.execute()

    meanings = []
    for hit in response.hits.hits:
        meaning = MeaningElastic.from_hit(hit['_source'])
        meanings.append(meaning)

    return meanings

