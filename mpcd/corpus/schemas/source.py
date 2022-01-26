from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Source


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class SourceNode(DjangoObjectType):
    class Meta:
        model = Source
        filter_fields = {'identifier': ['exact', 'icontains', 'istartswith'],
                         'slug': ['exact', 'icontains', 'istartswith'],
                         'description': ['exact', 'icontains', 'istartswith']}


class Query(ObjectType):
    source = relay.Node.Field(SourceNode)
    all_source = DjangoFilterConnectionField(SourceNode)
