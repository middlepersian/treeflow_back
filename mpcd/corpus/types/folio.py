from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Annotated, List, TYPE_CHECKING, Optional
from mpcd.corpus import models
from mpcd.corpus.types.comment import CommentPartial, CommentInput

if TYPE_CHECKING:
    from .facsimile import Facsimile
    from .folio import Folio
    from .line import Line
    from .comment import Comment, CommentPartial, CommentInput


@gql.django.type(models.Folio)
class Folio(relay.Node):

    line_folio: relay.Connection[Annotated['Line', lazy('mpcd.corpus.types.line')]]

    id: gql.auto
    number: gql.auto
    facsimile: Annotated['Facsimile', lazy('mpcd.corpus.types.facsimile')]
    comments: List[Annotated['Comment', lazy('mpcd.corpus.types.comment')]]
    previous: Optional['Folio']

# TODO: compare with models how comments work


@gql.django.input(models.Folio)
class FolioInput:
    number: gql.auto
    facsimile: gql.auto
    comments: gql.auto
    previous: gql.auto


@gql.django.partial(models.Folio)
class FolioPartial(gql.NodeInputPartial):
    id: gql.auto
    number: gql.auto
    facsimile: gql.auto
    comments:  gql.auto
    previous: gql.auto
