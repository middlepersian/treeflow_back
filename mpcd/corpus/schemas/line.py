from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType, Int, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Folio, Line
from .folio import FolioInput
from graphql_jwt.decorators import login_required

import graphene_django_optimizer as gql_optimizer


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class LineNode(DjangoObjectType):

    class Meta:
        model = Line
        filter_fields = {'number': ['exact', 'lt', 'lte', 'gt', 'gte'],
                         'comment': ['exact', 'icontains', 'istartswith']}

        interfaces = (relay.Node, )


class LineInput(InputObjectType):
    number = String(required=True)
    folio = FolioInput()
    comment = String(required=False)
    previous = LineNode()


class Query(ObjectType):
    line = relay.Node.Field(LineNode)
    all_lines = DjangoFilterConnectionField(LineNode)
    #all_lines = DjangoFilterConnectionField(LineNode,token=String(required=True))
    
    #@login_required
    def resolve_all_lines(self, info, **kwargs):
        return gql_optimizer.query(Line.objects.all(), info)

# Mutations


class CreateLine(relay.ClientIDMutation):
    class Input:
        number = Int(required=True)
        folio = ID()
        comment = String(required=False)
        previous = ID()

    line = Field(LineNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('CreateLine.mutate_and_get_payload()')

        if input.get('folio', None) is None:
            return cls(success=False, errors=['folio ID is required'])
        else:
            logger.error('folio ID {}'.format(input.get('folio')))
            if Folio.objects.filter(pk=from_global_id(input.get('folio'))[1]).exists():
                folio_instance = Folio.objects.get(pk=from_global_id(input.get('folio'))[1])
            else:
                return cls(success=False, errors=['folio does not exist'])

        if input.get('number', None) is not None:
            if Line.objects.filter(number=input.get('number'), folio=folio_instance).exists():
                return cls(success=False, errors=['line number {} already exists in this folio'.format(input.get('number'))])
            else:
                line = Line(folio=folio_instance, number=input.get('number'))
        else:
            return cls(success=False, errors=['number is required'])

       # check if previous token available
        if input.get('previous', None) is not None:
            # check if previous token with assigned id does not exist
            if Line.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                # assign previous token to line
                line.previous = Line.objects.get(pk=from_global_id(input['previous'])[1])

        if input.get('comment', None) is not None:
            line.comment = input.get('comment')

        line.save()

        return cls(line=line, success=True)


class UpdateLine(relay.ClientIDMutation):
    class Input:
        id = ID()
        number = String(required=True)
        folio = FolioInput()
        comment = String(required=False)

    line = Field(LineNode)
    success = Boolean()

    @ classmethod
    def mutate_and_get_payload(cls, root, info, id, number, folio, comment):
        logger.debug('UpdateLine.mutate_and_get_payload()')
        if Line.objects.filter(pk=from_global_id(id)[1]).exists() and Folio.objects.filter(pk=from_global_id(folio.id)[1]).exists():
            line_instance = Line.objects.get(pk=from_global_id(id)[1])
            line_instance.number = number
            line_instance.folio = Folio.objects.get(pk=from_global_id(folio.id)[1])
            line_instance.comment = comment
            # check if previous token available
        if input.get('previous', None) is not None:
            # check if previous token with assigned id does not exist
            if Line.objects.filter(pk=from_global_id(input['previous']['id'])[1]).exists():
                # assign previous token to line
                line_instance.previous = Line.objects.get(pk=from_global_id(input['previous']['id'])[1])

            line_instance.save()
            return cls(line=line_instance, success=True)
        else:
            return cls(success=False)


class DeleteLine(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @ classmethod
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
