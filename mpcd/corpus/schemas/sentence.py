from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.sentence import Sentence, SentenceInput, SentencePartial


@gql.type
class Query:
    sentence: Optional[Sentence] = gql.django.node()
    sentences:  relay.Connection[Sentence] = gql.django.connection()


@gql.type
class Mutation:
    create_sentence: Sentence = gql.django.create_mutation(SentenceInput)
    update_sentence: Sentence = gql.django.update_mutation(SentencePartial)
    delete_sentence: Sentence = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
