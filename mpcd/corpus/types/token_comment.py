from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING, Optional
from mpcd.corpus import models


@gql.django.type(models.TokenComment)
class TokenComment(relay.Node):

    token_comments: relay.Connection[LazyType['Token', 'mpcd.corpus.types.token']]

    id: gql.auto
    user: LazyType['User', 'mpcd.corpus.types.user']
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
