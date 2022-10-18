from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.morphological_annotation import MorphologicalAnnotation, MorphologicalAnnotationInput, MorphologicalAnnotationPartial


@gql.type
class Query:
    morphological_annotation: Optional[MorphologicalAnnotation] = gql.django.node()
    morphological_annotations:  relay.Connection[MorphologicalAnnotation] = gql.django.connection()


@gql.type
class Mutation:
    create_morphological_annotation: MorphologicalAnnotation = gql.django.create_mutation(MorphologicalAnnotationInput)
    update_morphological_annotation: MorphologicalAnnotation = gql.django.update_mutation(
        MorphologicalAnnotationPartial)
    delete_morphological_annotation: MorphologicalAnnotation = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
