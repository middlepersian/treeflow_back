from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional, cast
from asgiref.sync import sync_to_async

from mpcd.dict.types.meaning import Meaning, MeaningInput, MeaningPartial
from mpcd.dict.models.meaning import Meaning as MeaningModel

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
    meaning: Optional[Meaning] = gql.django.node(directives=[IsAuthenticated()])
    meanings:  relay.Connection[Meaning] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:

    create_meaning: Meaning = gql.django.create_mutation(MeaningInput, directives=[IsAuthenticated()])
    update_meaning: Meaning = gql.django.update_mutation(MeaningPartial, directives=[IsAuthenticated()])
    delete_meaning: Meaning = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
