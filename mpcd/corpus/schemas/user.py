from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.user import User

from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    HasObjPerm,
    HasPerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,
)


@gql.type
class Query:
    user: Optional[User] = gql.django.node(directives=[IsSuperuser()])
    users:  relay.Connection[User] = gql.django.connection(directives=[IsSuperuser()])


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
