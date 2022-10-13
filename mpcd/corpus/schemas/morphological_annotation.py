import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from mpcd.corpus.types.morphological_annotation import MorphologicalAnnotation


@gql.type
class Query:
    morphological_annotations:  relay.Connection[MorphologicalAnnotation] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
