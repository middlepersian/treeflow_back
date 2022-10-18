from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from mpcd.corpus.types.text import Text, TextInput, TextPartial


@gql.type
class Query:
    text: Optional[Text] = gql.django.node()
    texts:  relay.Connection[Text] = gql.django.connection()


@gql.type
class Mutation:
    create_text: Text = gql.django.create_mutation(TextInput)
    update_text: Text = gql.django.update_mutation(TextPartial)
    delete_text: Text = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation,  extensions=[DjangoOptimizerExtension])
