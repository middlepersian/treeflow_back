from app_backend.mpcd.corpus.models import codex
from app_backend.mpcd.corpus.models.codex import Codex, Folio
from graphene import relay, ObjectType, String, Field, ID, Boolean, List, Int, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Codex, Author, Line
from mpcd.corpus.schemas.codex import CodexNode
from mpcd.corpus.schemas.folio import FolioNode


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class LineNode(DjangoObjectType):

    class Meta:
        model = codex.Line
        filter_fields = {'number': ['exact', 'icontains', 'istartswith'],
                         'folio': ['exact', 'icontains', 'istartswith'],
                         'comment': ['exact', 'icontains', 'istartswith']}

        interfaces = (relay.Node, )


class LineInput(InputObjectType):
    id = ID()
    number = String(required=True)
    folio = FolioNode(required=True)
    comment = String(required=False)


class Query(ObjectType):
    line = relay.Node.Field(LineNode)
    all_lines = DjangoFilterConnectionField(LineNode)

# Mutations


class CreateLine(relay.ClientIDMutation):
    class Input:
        number = String(required=True)
        folio = FolioNode(required=True)
        comment = String(required=False)

    line = Field(LineNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, number, folio, comment):
        logger.debug('CreateLine.mutate_and_get_payload()')
        if Line.objects.filter(number=number).exists() and Folio.objects.filter(id=folio.id).exists():
            return cls(success=False)
        else:
            line_instance = Line.objects.create()
            line_instance.number = number
            line_instance.folio = Folio.objects.get(id=folio.id)
            line_instance.comment = comment
            return cls(line=line_instance, success=True)

class UpdateLine(relay.ClientIDMutation):
    class Input:
        id = ID()
        number = String(required=True)
        folio = FolioNode(required=True)
        comment = String(required=False)

    line = Field(LineNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, number, folio, comment):
        logger.debug('UpdateLine.mutate_and_get_payload()')
        if Line.objects.filter(id=id).exists() and Folio.objects.filter(id=folio.id).exists():
            line_instance = Line.objects.get(id=id)
            line_instance.number = number
            line_instance.folio = Folio.objects.get(id=folio.id)
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
        if Line.objects.filter(id=id).exists():
            Line.objects.get(id=id).delete()
            return cls(success=True)
        else:
            return cls(success=False)            


class Mutation(ObjectType):
    create_line = CreateLine.Field()
    update_line = UpdateLine.Field()
    delete_line = DeleteLine.Field()