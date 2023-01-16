from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Annotated, List, TYPE_CHECKING, Optional
from mpcd.corpus import models
from mpcd.corpus.types.comment import CommentPartial, CommentInput

if TYPE_CHECKING:
    from .facsimile import Facsimile
    from .folio import Folio
    from .comment import Comment, CommentPartial, CommentInput


@gql.django.type(models.Folio)
class Folio(relay.Node):

    id: relay.GlobalID
    number: gql.auto
    facsimile: gql.LazyType['Facsimile', 'mpcd.corpus.types.facsimile']
    previous: Optional['Folio']
    next: Optional['Folio']

# TODO: compare with models how comments work


@gql.django.input(models.Folio)
class FolioInput:
    number: gql.auto
    facsimile: gql.auto
    previous: gql.auto
    next: gql.auto


@gql.django.partial(models.Folio)
class FolioPartial(gql.NodeInputPartial):
    id: relay.GlobalID
    number: gql.auto
    facsimile: gql.auto
    previous: gql.auto
    next: gql.auto
