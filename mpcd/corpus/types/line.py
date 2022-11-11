from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional, Annotated
from mpcd.corpus import models

if TYPE_CHECKING:
    from .folio import Folio
    from .comment import Comment, CommentPartial, CommentInput
    from .token import Token


@gql.django.type(models.Line)
class Line(relay.Node):
    token_line: relay.Connection[gql.LazyType['Token', 'mpcd.corpus.types.token']]

    #id: gql.auto
    number: gql.auto
    folio: gql.LazyType['Folio', 'mpcd.corpus.types.folio']
    comments: List[gql.LazyType['Comment', 'mpcd.corpus.types.comment']]
    previous: Optional['Line']


@gql.django.input(models.Line)
class LineInput:
    number: gql.auto
    folio: gql.auto
    comments: gql.auto
    previous: gql.auto


@gql.django.partial(models.Line)
class LinePartial(gql.NodeInputPartial):
    id: gql.auto
    number: gql.auto
    folio: gql.auto
    comments:  gql.auto
    previous: gql.auto
