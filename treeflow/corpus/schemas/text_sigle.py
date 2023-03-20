from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from treeflow.corpus.types.text_sigle import TextSigle, TextSigleInput, TextSiglePartial


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
    text_sigle: Optional[TextSigle] = gql.django.node()
    text_sigles:  relay.Connection[TextSigle] = gql.django.connection()


@gql.type
class Mutation:
    create_text_sigle: TextSigle = gql.django.create_mutation(TextSigleInput, directives=[IsAuthenticated()])
    update_text_sigle: TextSigle = gql.django.update_mutation(TextSiglePartial, directives=[IsAuthenticated()])
    delete_text_sigle: TextSigle = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
