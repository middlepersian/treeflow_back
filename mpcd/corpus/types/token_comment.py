from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional, Annotated
from mpcd.corpus import models

if TYPE_CHECKING:
    from .token import Token
    from .comment import Comment


@gql.django.type(models.TokenComment)
class TokenComment(relay.Node):


    id: relay.GlobalID
    comment :  gql.LazyType['Comment', 'mpcd.corpus.types.comment']
    token: gql.LazyType['Token', 'mpcd.corpus.types.token']

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]





@gql.django.input(models.TokenComment)
class TokenCommentInput:
    token :  gql.auto
    comment :  gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]



@gql.django.partial(models.TokenComment)
class TokenCommentPartial:
    id: relay.GlobalID
    token :  gql.auto
    comment :  gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]
