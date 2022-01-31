from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Folio, Line
from .folio import FolioInput


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class LineNode(DjangoObjectType):

    class Meta:
        model = Line
        filter_fields = {'number': ['exact', 'icontains', 'istartswith'],
                         'comment': ['exact', 'icontains', 'istartswith']}

        interfaces = (relay.Node, )


class LineInput(InputObjectType):
    id = ID()
    number = String(required=True)
    folio = FolioInput()
    comment = String(required=False)


class Query(ObjectType):
    line = relay.Node.Field(LineNode)
    all_lines = DjangoFilterConnectionField(LineNode)

# Mutations


class CreateLine(relay.ClientIDMutation):
    class Input:
        number = String(required=True)
        folio = FolioInput()
        comment = String(required=False)

    line = Field(LineNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, number, folio, comment):
        logger.debug('CreateLine.mutate_and_get_payload()')
        if Line.objects.filter(number=number).exists() and Folio.objects.filter(pk=from_global_id(folio.id)[1]).exists():
            return cls(success=False)
        else:
            line_instance = Line.objects.create()
            line_instance.number = number
            line_instance.folio = Folio.objects.get(pk=from_global_id(folio.id)[1])
            line_instance.comment = comment
            return cls(line=line_instance, success=True)


class UpdateLine(relay.ClientIDMutation):
    class Input:
        id = ID()
        number = String(required=True)
        folio = FolioInput()
        comment = String(required=False)

    line = Field(LineNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, number, folio, comment):
        logger.debug('UpdateLine.mutate_and_get_payload()')
        if Line.objects.filter(pk=from_global_id(id)[1]).exists() and Folio.objects.filter(pk=from_global_id(folio.id)[1]).exists():
            line_instance = Line.objects.get(pk=from_global_id(id)[1])
            line_instance.number = number
            line_instance.folio = Folio.objects.get(pk=from_global_id(folio.id)[1])
            line_instance.comment = comment
            line_instance.save()
            return cls(line=line_instance, success=True)
        else:
            return cls(success=False)


class DeleteLine(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        logger.debug('DeleteLine.mutate_and_get_payload()')
        if Line.objects.filter(pk=from_global_id(id)[1]).exists():
            Line.objects.get(pk=from_global_id(id)[1]).delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_line = CreateLine.Field()
    update_line = UpdateLine.Field()
    delete_line = DeleteLine.Field()
