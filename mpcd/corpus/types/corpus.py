from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from mpcd.corpus import models


@gql.django.type(models.Corpus)
class Corpus(relay.Node):
    id: gql.auto
    name: gql.auto
    slug: gql.auto