from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional, cast
from asgiref.sync import sync_to_async

from mpcd.dict.types.meaning import Meaning, MeaningInput, MeaningPartial
from mpcd.dict.models.meaning import Meaning as MeaningModel


@gql.type
class Query:
    meaning: Optional[Meaning] = gql.django.node()
    meanings:  relay.Connection[Meaning] = gql.django.connection()


@gql.type
class Mutation:

    create_meaning: Meaning = gql.django.create_mutation(MeaningInput)
    update_meaning: Meaning = gql.django.update_mutation(MeaningPartial)
    delete_meaning: Meaning = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
