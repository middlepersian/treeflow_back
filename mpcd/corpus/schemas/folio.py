import re
from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType, List, Float
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Folio, Facsimile

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class FolioNode(DjangoObjectType):

    class Meta:
        model = Folio
        filter_fields = {'identifier': ['exact', 'icontains', 'istartswith'],
                         'comment': ['exact', 'icontains', 'istartswith']}

        interfaces = (relay.Node, )


class FolioInput(InputObjectType):
    identifier = String()
    facsimile = ID()
    number = Float()


# Queries
class Query(ObjectType):
    folio = relay.Node.Field(FolioNode)
    all_folios = DjangoFilterConnectionField(FolioNode)

    def resolve_all_folios(self, info, **kwargs):
        return gql_optimizer.query(Folio.objects.all(), info)


# Mutations


class CreateFolio(relay.ClientIDMutation):
    class Input:
        identifier = String(required=True)
        facsimile = ID(required=True)
        number = Float(required=True)
        comment = String(required=False)
        previous = ID(required=False)

    folio = Field(FolioNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('CreateFolio.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if Facsimile.objects.filter(pk=from_global_id(input['facsimile'])[1]).exists():
            facsimile_instance = Facsimile.objects.get(pk=from_global_id(input.get('facsimile'))[1])
        else:
            return cls(success=False, errors=['Wrong facsimile ID'])

        folio_instance, folio_created = Folio.objects.get_or_create(identifier=input.get(
            'identifier'), facsimile=facsimile_instance, number=input.get('number'))

        if input.get('comment'):
            folio_instance.comment = input.get('comment')
            folio_instance.save()

        if input.get('previous'):
            if Folio.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                folio_instance.previous = Folio.objects.get(pk=from_global_id(input['previous'])[1])
                folio_instance.save()

        return cls(folio=folio_instance, success=True, errors=None)


class UpdateFolio(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        identifier = String(required=True)
        facsimile = ID(required=True)
        number = Float(required=True)
        comment = String(required=False)
        previous = ID(required=False)

    folio = Field(FolioNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        if Folio.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            folio_instance = Folio.objects.get(pk=from_global_id(input.get('id'))[1])
        else:
            return cls(success=False, errors=['folio ID does not exist'])

        folio_instance.identifier = input.get('identifier')

        if Facsimile.objects.filter(pk=from_global_id(input.get('facsimile'))[1]).exists():
            folio_instance.facsimile = Facsimile.objects.get(pk=from_global_id(input.get('facsimile'))[1])
        else:
            return cls(success=False, errors=['facsimile ID does not exist'])

        if input.get('comment'):
            folio_instance.comment = input.get('comment')

        if input.get('number'):
            folio_instance.number = input.get('number')

        if input.get('previous'):
            if Folio.objects.filter(pk=from_global_id(input['previous']['id'])[1]).exists():
                folio_instance.previous = Folio.objects.get(pk=from_global_id(input['previous']['id'])[1])
            else: return cls (success=False, errors=['previous folio ID does not exist'])    

        folio_instance.save()
        return cls(folio=folio_instance, success=True)


class DeleteFolio(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, id):
        logger.debug('DeleteFolio.mutate_and_get_payload()')
        if Folio.objects.filter(pk=from_global_id(id)[1]).exists():
            folio_instance = Folio.objects.get(pk=from_global_id(id)[1])
            folio_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_folio = CreateFolio.Field()
    update_folio = UpdateFolio.Field()
    delete_folio = DeleteFolio.Field()
