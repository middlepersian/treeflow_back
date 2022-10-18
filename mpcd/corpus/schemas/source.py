from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.source import Source, SourceInput, SourcePartial


@gql.type
class Query:
    source: Optional[Source] = gql.django.node()
    sources:  relay.Connection[Source] = gql.django.connection()


@gql.type
class Mutation:
    create_source: Source = gql.django.create_mutation(SourceInput)
    update_source: Source = gql.django.update_mutation(SourcePartial)
    delete_source: Source = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
