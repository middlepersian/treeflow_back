from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional, Annotated
from mpcd.corpus import models

if TYPE_CHECKING:
    from .token import Token
    from .user import User


@gql.django.type(models.TokenComment)
class TokenComment(relay.Node):

    token_comments: relay.Connection[gql.LazyType['Token', 'mpcd.corpus.types.token']]

    id: relay.GlobalID
    user: gql.LazyType['User', 'mpcd.corpus.types.user']
    text: gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]


@gql.django.input(models.TokenComment)
class TokenCommentInput:
    user: gql.auto
    text: gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]


@gql.django.partial(models.TokenComment)
class TokenCommentPartial:
    id: relay.GlobalID
    user: gql.auto
    text: gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]
