from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType

from mpcd.corpus import models


@gql.django.type(models.TextSigle)
class TextSigle(relay.Node):
    text_text_sigle: relay.Connection[LazyType['Text', 'mpcd.corpus.types.text']]

    id: gql.auto
    sigle: gql.auto
    genre: gql.auto


@gql.django.input(models.TextSigle)
class TextSigleInput:
    sigle: gql.auto
    genre: gql.auto

@gql.django.partial(models.TextSigle)
class TextSiglePartial(gql.NodeInputPartial):
    id: gql.auto
    sigle: gql.auto
    genre: gql.auto
        