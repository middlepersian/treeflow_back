from graphene import relay, ObjectType, Field, ID, Boolean, List, InputObjectType, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import superuser_required

from django.contrib.auth import get_user_model
User = get_user_model()

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")
        filter_fields = {
            'username': ['icontains']
        }
        interfaces = (relay.Node, )


class Query(ObjectType):
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    @superuser_required
    def resolve_all_users(self, info, **kwargs):
        qs = User.objects.all()
        return gql_optimizer.query(qs, info)

    @superuser_required
    def resolve_user(self, info, id):
        id = from_global_id(id)[1]
        return User.objects.get(pk=id)
