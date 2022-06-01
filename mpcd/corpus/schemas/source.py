from graphene import relay, ObjectType, String, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Source

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class SourceNode(DjangoObjectType):
    class Meta:
        model = Source
        filter_fields = {
            'slug': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains', 'istartswith'], 'bib_entry__id': ['exact']}


class SourceInput(InputObjectType):
    id = String()
    #title = String()
    #slug = String()
    #description = String()


class Query(ObjectType):
    source = relay.Node.Field(SourceNode)
    all_source = DjangoFilterConnectionField(SourceNode)

    @login_required
    def resolve_all_sources(self, info, **kwargs):
        return gql_optimizer.query(Source.objects.all(), info)
