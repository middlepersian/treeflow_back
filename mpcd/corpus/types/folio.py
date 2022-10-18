from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING, Optional
from mpcd.corpus import models
from mpcd.corpus.types.comment import CommentPartial, CommentInput


@gql.django.type(models.Folio)
class Folio(relay.Node):

    line_folio: relay.Connection[LazyType['Line', 'mpcd.corpus.types.line']]

    id: gql.auto
    number: gql.auto
    facsimile: LazyType['Facsimile', 'mpcd.corpus.types.facsimile']
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
    previous: Optional['Folio']


@gql.django.input(models.Folio)
class FolioInput:
    number: gql.auto
    facsimile: gql.auto
    comments: Optional[List[CommentInput]]
    previous: gql.auto


@gql.django.partial(models.Folio)
class FolioPartial(gql.NodeInputPartial):
    id: gql.auto
    number: gql.auto
    facsimile: gql.auto
    comments: Optional[gql.ListInput[CommentPartial]]
    previous: gql.auto
