from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay

from treeflow.corpus import models


@gql.django.type(models.PostFeature)
class PostFeature(relay.Node):

    token_morphological_annotation: relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]

    id: relay.GlobalID
    feature: gql.auto
    feature_value: gql.auto


@gql.django.input(models.PostFeature)
class PostFeatureInput:
    feature: gql.auto
    feature_value: gql.auto

@gql.django.partial(models.PostFeature)
class PostFeaturePartial(gql.NodeInputPartial):
    id: relay.GlobalID
    feature: gql.auto
    feature_value: gql.auto