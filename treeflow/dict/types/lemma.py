
import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Optional, Iterable
from treeflow.dict import models
from treeflow.dict.documents.lemma import LemmaDocument
from treeflow.dict.enums.term_tech import TermTech
from treeflow.dict.enums.language import Language
from treeflow.dict.enums.dict_stage import DictStage
from elasticsearch_dsl import Search, Q, connections
from strawberry.types import Info
from elasticsearch.exceptions import NotFoundError
from asgiref.sync import sync_to_async


@strawberry.type
class TermTechList:
    term_tech: List[TermTech]

@strawberry.type
class LanguageList:
    language: List[Language]


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
    stage : Optional[DictStage]
    multiword_expression: gql.auto
    categories: Optional[List[Optional[str]]]
    related_lemmas: List['Lemma']
    related_meanings: List[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]


@gql.django.input(models.Lemma)
class LemmaInput:
    word: gql.auto
    language: Language
    stage : Optional[DictStage]
    multiword_expression: gql.auto
    categories: Optional[List[Optional[str]]]
    related_lemmas: gql.auto
    related_meanings: gql.auto


@gql.django.partial(models.Lemma)
class LemmaPartial:
    id: relay.GlobalID
    word: gql.auto
    language: Language
    stage : Optional[DictStage]
    multiword_expression: gql.auto
    categories: Optional[List[Optional[str]]]
    related_lemmas: gql.auto
    related_meanings: gql.auto


@strawberry.type
class LemmaSelection():
    word: str
    language: str
    multiword_expression: Optional[bool] = None


    @classmethod
    def from_hit(cls,hit, field="related_lemmas"):
        if field in hit:
            related_vals = hit[field]
            return[ cls(
                word=to_parse['word'],
                language=to_parse['language'],
                #category=to_parse['category'] if 'category' in to_parse else None,
                multiword_expression=to_parse['multiword_expression'] if 'category' in to_parse else None,
            ) for to_parse in related_vals]
        return None

@strawberry.type
class MeaningSelection():
    meaning: str
    language: str

    @classmethod
    def from_hit(cls, hit, field="related_meanings"):
        if field in hit:
            related_vals = hit[field]
            return[ cls(
                meaning=to_parse['meaning'],
                language=to_parse['language']
            ) for to_parse in related_vals]
        return None



@strawberry.type
class LemmaElastic(relay.Node):

    id: relay.GlobalID
    word: str
    language: Language
    stage : Optional[DictStage]
    categories: Optional[List[Optional[str]]] = None
    multiword_expression: bool
    related_lemmas: Optional[List[LemmaSelection]] = None
    related_meanings: Optional[List[MeaningSelection]] = None


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
            categories=hit['categories'] if 'categories' in hit else None,
            related_lemmas=LemmaSelection.from_hit(hit, field="related_lemmas"),
            related_meanings=MeaningSelection.from_hit(hit, field="related_meanings")
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
    s = Search(index='lemmas').query('ids', values=[id])
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


