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

    token_comments: relay.Connection[Annotated['Token', lazy('mpcd.corpus.types.token')]]

    id: gql.auto
    user: Annotated['User', lazy('mpcd.corpus.types.user')]
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
    id: gql.auto
    user: gql.auto
    text: gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]
