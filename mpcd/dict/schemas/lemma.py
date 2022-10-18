from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.dict.types.lemma import Lemma, LemmaInput, LemmaPartial


@gql.type
class Query:
    lemma: Optional[Lemma] = gql.django.node()
    lemmas:  relay.Connection[Lemma] = gql.django.connection()


@gql.type
class Mutation:
    create_lemma: Lemma = gql.django.create_mutation(LemmaInput)
    update_lemma: Lemma = gql.django.update_mutation(LemmaPartial)
    delete_lemma: Lemma = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
