from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Annotated

from mpcd.corpus import models

if TYPE_CHECKING:
    from .text import Text


@gql.django.type(models.Corpus)
class Corpus(relay.Node):

    text_corpus: relay.Connection[Annotated['Text', lazy('mpcd.corpus.types.text')]]

    id: gql.auto
    name: gql.auto
    slug: gql.auto
