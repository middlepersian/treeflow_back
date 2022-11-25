from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Annotated

from mpcd.corpus import models

if TYPE_CHECKING:
    from .text import Text


@gql.django.type(models.Corpus)
class Corpus(relay.Node):

    text_corpus: relay.Connection[gql.LazyType['Text', 'mpcd.corpus.types.text']]

    id: relay.GlobalID
    name: gql.auto
    slug: gql.auto
