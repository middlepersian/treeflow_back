from graphene import relay, InputObjectType, String, Field, ObjectType, List, Boolean, ID
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required

from mpcd.dict.models import TermTech


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class TermTechNode(DjangoObjectType):
    class Meta:
        model = TermTech
        filter_fields = {'category': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class TermTechInput(InputObjectType):
    category = String(required=True)

# Queries


class Query(ObjectType):
    term_tech = relay.Node.Field(TermTechNode)
    all_term_tech = DjangoFilterConnectionField(TermTechNode)

    @login_required
    def resolve_all_term_tech(self, info, **kwargs):
        qs = TermTech.objects.all()
        return gql_optimizer.query(qs, info)

# Mutations


class CreateTermTech(relay.ClientIDMutation):
    class Input:
        category = String(required=True)

    term_tech = Field(TermTechNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('CreateTermTech: input: {}'.format(input))
        term_tech, term_tech_created = TermTech.objects.get_or_create(category=input['category'])
        return cls(term_tech=term_tech, success=term_tech_created, errors=None)


class UpdateTermTech(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        category = String(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        if TermTech.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            term_tech = TermTech.objects.get(pk=from_global_id(input.get('id'))[1])
            term_tech.category = input['category']
            term_tech.save()
            return cls(term_tech=term_tech, success=True, errors=None)
        else:
            return cls(term_tech=None, success=False, errors=['TermTech ID does not exist'])

class DeleteTermTech(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
    
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        if TermTech.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            TermTech.objects.get(pk=from_global_id(input.get('id'))[1]).delete()
            return cls(success=True)
        else:
            return cls(success=False)

class Mutation(ObjectType):
    create_term_tech = CreateTermTech.Field()
    update_term_tech = UpdateTermTech.Field()
    delete_term_tech = DeleteTermTech.Field()
    