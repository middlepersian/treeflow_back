import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from mpcd.corpus.types.folio import Folio, FolioInput, FolioPartial

from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    HasObjPerm,
    HasPerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,
)


@gql.type
class Query:
    folio: Optional[Folio] = gql.django.node(directives=[IsAuthenticated()])
    folios:  relay.Connection[Folio] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_folio: Folio = gql.django.create_mutation(FolioInput, directives=[IsAuthenticated()])
    update_folio: Folio = gql.django.update_mutation(FolioPartial, directives=[IsAuthenticated()])
    delete_folio: Folio = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
