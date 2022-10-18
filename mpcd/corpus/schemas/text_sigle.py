from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from mpcd.corpus.types.text_sigle import TextSigle, TextSigleInput, TextSiglePartial


@gql.type
class Query:
    text_sigle: Optional[TextSigle] = gql.django.node()
    text_sigles:  relay.Connection[TextSigle] = gql.django.connection()


@gql.type
class Mutation:
    create_text_sigle: TextSigle = gql.django.create_mutation(TextSigleInput)
    update_text_sigle: TextSigle = gql.django.update_mutation(TextSiglePartial)
    delete_text_sigle: TextSigle = gql.django.delete_mutation(gql.NodeInput)

schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
