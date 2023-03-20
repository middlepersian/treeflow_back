from asgiref.sync import sync_to_async
import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional, cast, List

from treeflow.dict.types.meaning import Meaning, MeaningInput, MeaningPartial, MeaningElastic
from treeflow.dict.models.meaning import Meaning as MeaningModel
from treeflow.dict.documents.meaning import MeaningDocument

from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    HasObjPerm,
    HasPerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,
)

from elasticsearch_dsl import Search, Q, connections
es_conn = connections.create_connection(hosts=['elastic:9200'], timeout=20)

@gql.type
class Query:
    meaning: Optional[Meaning] = gql.django.node()
    meanings:  relay.Connection[Meaning] = gql.django.connection()


    @gql.field
    @sync_to_async
    def search_meanings(pattern: str, query_type: str, size: int = 100) -> List[MeaningElastic]:
        q = Q(query_type, meaning=pattern)
        response =MeaningDocument.search().query(q).extra(size=size)
        meanings = []
        for hit in response:
            meaning = MeaningElastic.from_hit(hit)
            meanings.append(meaning)
        return meanings




@gql.type
class Mutation:

    create_meaning: Meaning = gql.django.create_mutation(MeaningInput, directives=[IsAuthenticated()])
    update_meaning: Meaning = gql.django.update_mutation(MeaningPartial, directives=[IsAuthenticated()])
    delete_meaning: Meaning = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])

    @gql.django.input_mutation
    def add_related_meaning_to_meaning(self, info, meaning: relay.GlobalID, related: relay.GlobalID) -> Meaning:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")

        try:
            current_meaning = meaning.resolve_node(info)
        except:
            raise Exception("Meaning not found.")
        try:
            related_meaning = related.resolve_node(info)
        except:
            raise Exception("Related meaning not found.")
        current_meaning.related_meanings.add(related_meaning)
        current_meaning.save()
        return current_meaning


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
