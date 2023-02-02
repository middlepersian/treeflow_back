from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from treeflow.corpus.types.text import Text, TextInput, TextPartial

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
    text: Optional[Text] = gql.django.node(directives=[IsAuthenticated()])
    texts:  relay.Connection[Text] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_text: Text = gql.django.create_mutation(TextInput, directives=[IsAuthenticated()])
    update_text: Text = gql.django.update_mutation(TextPartial, directives=[IsAuthenticated()])
    delete_text: Text = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation,  extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
