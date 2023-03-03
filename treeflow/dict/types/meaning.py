
import strawberry
from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Annotated, List, TYPE_CHECKING, Optional, Iterable
from treeflow.dict import models
from treeflow.dict.types import language
from strawberry.types import Info
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Search, Q, connections
from asgiref.sync import sync_to_async

es_conn =  connections.create_connection(hosts=['elastic:9200'], timeout=20)

if TYPE_CHECKING:
    from treeflow.corpus.types.token import Token
    from treeflow.corpus.types.comment import Comment
    from treeflow.dict.types.meaning import Meaning
    from treeflow.dict.types.lemma import Lemma


@gql.django.filters.filter(models.Meaning, lookups=True)
class MeaningFilter:
    id: relay.GlobalID
    meaning: gql.auto
    language: gql.auto


@gql.django.type(models.Meaning, filters=MeaningFilter)
class Meaning(relay.Node):

    token_meanings:  relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]
    sentence_meanings:  relay.Connection[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]
    comment_meaning: relay.Connection[gql.LazyType['Comment', 'treeflow.corpus.types.comment']]

    id: relay.GlobalID
    meaning: gql.auto
    language: gql.auto
    related_meanings: List['Meaning']
    related_lemmas: List[gql.LazyType['Lemma', 'treeflow.dict.types.lemma']]


@gql.django.input(models.Meaning)
class MeaningInput:
    meaning: gql.auto
    language: gql.auto
    related_meanings: gql.auto


@gql.django.partial(models.Meaning)
class MeaningPartial:
    id: relay.GlobalID
    meaning: gql.auto
    language: gql.auto
    related_meanings: gql.auto



@strawberry.type
class MeaningElastic(relay.Node):

    id: relay.GlobalID
    language: str
    meaning: str


    @classmethod
    def resolve_id(self: "MeaningElastic", info: Optional[Info] = None) -> str:
        return self.id
    
    @classmethod
    def from_hit(cls, hit):
        # Access the source data in the hit
        source = hit['_source']

        # Build and return a new instance of MeaningElastic
        return cls(
            id=relay.to_base64(MeaningElastic, source['id']),
            language=source['language'],
            meaning=source['meaning'],
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
    def meaning_object(self, info: Optional[Info]) -> List[models.Meaning]:
        if self.id is not None:
            meaning_id = relay.from_base64(self.id)[1]
            meaning = models.Meaning.get(id=meaning_id)
            return meaning
        else:
            return []

def get_meaning_by_id(id: str) -> MeaningElastic:
    s = Search(using=es_conn, index='meanings').query('ids', values=[id])
    response = s.execute()

    if len(response.hits.hits) == 0:
        raise NotFoundError(f"No meaning by id {id}")

    return MeaningElastic.from_hit(response.hits.hits[0])

def get_meanings_by_ids(ids: List[str]) -> List[MeaningElastic]:
    s = Search(index='meanings').query('ids', values=ids)
    response = s.execute()

    meanings = []
    for hit in response.hits.hits:
        meaning = MeaningElastic.from_hit(hit)
        meanings.append(meaning)

    return meanings

