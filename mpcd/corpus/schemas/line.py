from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType, Float, List
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
    number = Float(required=True)
    folio = FolioInput()
    comment = String(required=False)
    previous = LineNode()


class Query(ObjectType):
    line = relay.Node.Field(LineNode)
    all_lines = DjangoFilterConnectionField(LineNode)

    @login_required
    def resolve_all_lines(self, info, **kwargs):
        return gql_optimizer.query(Line.objects.all(), info)

# Mutations


class CreateLine(relay.ClientIDMutation):
    class Input:
        number = Float(required=True)
        folio = ID(required=True)
        comment = String()
        previous = ID()

    line = Field(LineNode)
    success = Boolean()
    errors = List(String)

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('CreateLine.mutate_and_get_payload()')

        if Folio.objects.filter(pk=from_global_id(input.get('folio'))[1]).exists():
            folio_instance = Folio.objects.get(pk=from_global_id(input.get('folio'))[1])
        else:
            return cls(success=False, errors=['folio does not exist'])

        line_instance, line_object = Line.objects.get_or_create(folio=folio_instance, number=input.get('number'))

       # check if previous token available
        if input.get('previous', None) is not None:
            # check if previous token with assigned id does not exist
            if Line.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                # assign previous token to line
                line_instance.previous = Line.objects.get(pk=from_global_id(input['previous'])[1])
                line_instance.save()

        if input.get('comment', None) is not None:
            line_instance.comment = input.get('comment')
            line_instance.save()

        return cls(line=line_instance, success=True, errors=None)


class UpdateLine(relay.ClientIDMutation):
    class Input:
        id = ID()
        number = Float(required=True)
        folio = FolioInput()
        comment = String()

    line = Field(LineNode)
    success = Boolean()

    @login_required
    @classmethod
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

    @login_required
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
