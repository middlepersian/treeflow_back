from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from treeflow.corpus.types.pos import POS, POSInput, POSPartial
from typing import Optional
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry_django_plus.directives import SchemaDirectiveExtension



@gql.type
class Query:
    pos: Optional[POS] = gql.django.node()
    pos_list: relay.Connection[POS] = gql.django.connection()

@gql.type
class Mutation:
    create_pos: POS = gql.django.create_mutation(POSInput)
    update_pos: POS = gql.django.update_mutation(POSPartial)
    delete_pos: POS = gql.django.delete_mutation(gql.NodeInput)

schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
