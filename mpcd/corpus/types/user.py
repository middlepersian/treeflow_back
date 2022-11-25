from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from django.contrib.auth import get_user_model


@gql.django.type(get_user_model())
class User(relay.Node):
    id: relay.GlobalID
    name: gql.auto
    is_superuser: gql.auto
    is_staff: gql.auto
    email: gql.auto
