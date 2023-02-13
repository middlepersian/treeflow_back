from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay

from treeflow.corpus import models


@gql.django.type(models.Feature)
class Feature(relay.Node):

    token_morphological_annotation: relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]

    id: relay.GlobalID
    feature: gql.auto
    feature_value: gql.auto


@gql.django.input(models.Feature)
class FeatureInput:
    feature: gql.auto
    feature_value: gql.auto

@gql.django.partial(models.Feature)
class FeaturePartial(gql.NodeInputPartial):
    id: relay.GlobalID
    feature: gql.auto
    feature_value: gql.auto