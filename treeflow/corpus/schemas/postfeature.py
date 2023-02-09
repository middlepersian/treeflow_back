from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from treeflow.corpus.types.postfeature import PostFeature, PostFeatureInput, PostFeaturePartial

from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    IsAuthenticated,
)


@gql.type
class Query:
    postfeature: Optional[PostFeature] = gql.django.node(directives=[IsAuthenticated()])
    postfeatures:  relay.Connection[PostFeature] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_postfeature: PostFeature = gql.django.create_mutation(
        PostFeatureInput, directives=[IsAuthenticated()])
    update_postfeature: PostFeature = gql.django.update_mutation(
        PostFeaturePartial, directives=[IsAuthenticated()])
    delete_postfeature: PostFeature = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
