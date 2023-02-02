from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Annotated

from treeflow.corpus import models

if TYPE_CHECKING:
    from .token import Token

@gql.django.type(models.MorphologicalAnnotation)
class MorphologicalAnnotation(relay.Node):

    token_morphological_annotation: relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]

    id: relay.GlobalID
    feature: gql.auto
    feature_value: gql.auto


@gql.django.input(models.MorphologicalAnnotation)
class MorphologicalAnnotationInput:
    feature: gql.auto
    feature_value: gql.auto

@gql.django.partial(models.MorphologicalAnnotation)
class MorphologicalAnnotationPartial(gql.NodeInputPartial):
    id: relay.GlobalID
    feature: gql.auto
    feature_value: gql.auto