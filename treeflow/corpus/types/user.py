from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from django.contrib.auth import get_user_model

from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    IsAuthenticated,
     IsSuperuser,
)

@gql.django.type(get_user_model())
class User(relay.Node):
    id: relay.GlobalID = gql.field()
    username: gql.auto = gql.field()
    is_superuser: gql.auto = gql.field()
    is_staff: gql.auto = gql.field()
    email: gql.auto = gql.field()
