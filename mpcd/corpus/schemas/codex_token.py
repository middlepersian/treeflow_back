
from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import CodexToken


class CodexTokenNode(DjangoObjectType):
    class Meta:
        model = CodexToken
        filter_fields = {'transcription': ['exact', 'icontains', 'istartswith'],
                         'transliteration': ['exact', 'icontains', 'istartswith']
                         }
        interfaces = (relay.Node,)
# TODO CodexTokenInput and also Queries and Mutations
