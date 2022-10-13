from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from mpcd.corpus import models

@gql.django.type(models.TextSigle)
class TextSigle(relay.Node):
    id: gql.auto
    sigle: gql.auto
    genre: gql.auto