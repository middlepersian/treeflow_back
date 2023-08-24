import strawberry
import strawberry_django
from strawberry import relay
from django.contrib.auth import get_user_model


@strawberry_django.type(get_user_model())
class User(relay.Node):
    id: relay.NodeID[str]
    username: strawberry.auto 
    is_superuser: strawberry.auto 
    is_staff: strawberry.auto 
    email: strawberry.auto 
