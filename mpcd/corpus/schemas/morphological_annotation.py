from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.morphological_annotation import MorphologicalAnnotation, MorphologicalAnnotationInput, MorphologicalAnnotationPartial

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
    morphological_annotation: Optional[MorphologicalAnnotation] = gql.django.node(directives=[IsAuthenticated()])
    morphological_annotations:  relay.Connection[MorphologicalAnnotation] = gql.django.connection(directives=[
                                                                                                  IsAuthenticated()])


@gql.type
class Mutation:
    create_morphological_annotation: MorphologicalAnnotation = gql.django.create_mutation(
        MorphologicalAnnotationInput, directives=[IsAuthenticated()])
    update_morphological_annotation: MorphologicalAnnotation = gql.django.update_mutation(
        MorphologicalAnnotationPartial, directives=[IsAuthenticated()])
    delete_morphological_annotation: MorphologicalAnnotation = gql.django.delete_mutation(gql.NodeInput, directives=[
                                                                                          IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
