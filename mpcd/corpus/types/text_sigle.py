from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import TYPE_CHECKING, Annotated
from mpcd.corpus import models

if TYPE_CHECKING:
    from .text import Text


@gql.django.type(models.TextSigle)
class TextSigle(relay.Node):
    text_text_sigle: relay.Connection[gql.LazyType['Text', 'mpcd.corpus.types.text']]

    #id: gql.auto
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
        