from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Author


class AuthorNode(DjangoObjectType):
    class Meta:
        model = Author
        filter_fields = ['name', 'last_name']
        interfaces = (relay.Node, )


class Query(ObjectType):
    author = relay.Node.Field(AuthorNode)
    all_authors = DjangoFilterConnectionField(AuthorNode)


class Mutation(ObjectType):
    pass
