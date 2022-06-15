from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType, List, Int
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Section, Text, Source, Token, SectionType

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class SectionNode(DjangoObjectType):
    class Meta:
        model = Section
        filter_fields = {'identifier': ['exact', 'icontains', 'istartswith']}

        interfaces = (relay.Node,)


class Query(ObjectType):
    section = relay.Node.Field(SectionNode)
    all_sections = DjangoFilterConnectionField(SectionNode)

    @login_required
    def resolve_all_sections(self, info, **kwargs):
        return gql_optimizer.query(Section.objects.all(), info)


class SectionInput(InputObjectType):
    identifier = String(required=True)
    number = Int(required=False)
    text = ID(required=True)
    section_type = ID(required=True)
    source = ID(required=False)
    tokens = List(ID, required=True)
    previous = ID(required=False)
    container = ID(required=False)


class CreateSection(relay.ClientIDMutation):

    class Input:
        identifier = String(required=True)
        number = Int(required=False)
        text = ID(required=True)
        section_type = ID(required=True)
        source = ID(required=False)
        tokens = List(ID, required=True)
        previous = ID(required=False)
        container = ID(required=False)

    section = Field(SectionNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('CreateSection.mutate_and_get_payload()')

        section_instance, section_created = Section.objects.get_or_create(identifier=input['identifier'])

        if input.get('number', None):
            section_instance.number = input['number']

        if Text.objects.filter(pk=from_global_id(input['text'])[1]).exists():
            section_instance.text = Text.objects.get(pk=from_global_id(input['text'])[1])

        else:
            return cls(errors=['Text ID not found'], success=False, section=None)

        if SectionType.objects.filter(pk=from_global_id(input['section_type'])[1]).exists():
            section_instance.section_type = SectionType.objects.get(pk=from_global_id(input['section_type'])[1])
        else:
            return cls(errors=['Section Type ID not found'], success=False, section=None)

        if input.get('source', None):
            if Source.objects.filter(pk=from_global_id(input['source'])[1]).exists():
                section_instance.source = Source.objects.get(pk=from_global_id(input['source'])[1])
            else:
                return cls(errors=['Source ID not found'], success=False, section=None)

        for token in input['tokens']:
            if Token.objects.filter(pk=from_global_id(token)[1]).exists():
                section_instance.tokens.add(Token.objects.get(pk=from_global_id(token)[1]))
            else:
                return cls(errors=['Token ID not found'], success=False, section=None)

        if input.get('previous', None):
            if Section.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                section_instance.previous = Section.objects.get(pk=from_global_id(input['previous'])[1])
            else:
                return cls(errors=['Previous Section ID not found'], success=False, section=None)

        if input.get('container', None):
            if Section.objects.filter(pk=from_global_id(input['container'])[1]).exists():
                section_instance.container = Section.objects.get(pk=from_global_id(input['container'])[1])
            else:
                return cls(errors=['Container Section ID not found'], success=False, section=None)

        section_instance.save()
        return cls(section=section_instance, success=True)


class UpdateSection(relay.ClientIDMutation):

    class Input:
        id = ID(required=True)
        identifier = String(required=True)
        number = Int(required=False)
        text = ID(required=True)
        section_type = ID(required=True)
        source = ID(required=False)
        tokens = List(ID, required=True)
        previous = ID(required=False)
        container = ID(required=False)

    section = Field(SectionNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('UpdateSection.mutate_and_get_payload()')
        if Section.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            section_instance = Section.objects.get(pk=from_global_id(input['id'])[1])

            section_instance.identifier = input['identifier']

            if input.get('number', None):
                section_instance.number = input['number']

            if Text.objects.filter(pk=from_global_id(input['text'])[1]).exists():
                section_instance.text = Text.objects.get(pk=from_global_id(input['text'])[1])

            else:
                return cls(errors=['Text ID not found'], success=False, section=None)

            if SectionType.objects.filter(pk=from_global_id(input['section_type'])[1]).exists():
                section_instance.section_type = SectionType.objects.get(pk=from_global_id(input['section_type'])[1])
            else:
                return cls(errors=['Section Type ID not found'], success=False, section=None)

            if input.get('source', None):
                if Source.objects.filter(pk=from_global_id(input['source'])[1]).exists():
                    section_instance.source = Source.objects.get(pk=from_global_id(input['source'])[1])
                else:
                    return cls(errors=['Source ID not found'], success=False, section=None)

            for token in input['tokens']:
                if Token.objects.filter(pk=from_global_id(token)[1]).exists():
                    section_instance.tokens.add(Token.objects.get(pk=from_global_id(token)[1]))
                else:
                    return cls(errors=['Token ID not found'], success=False, section=None)

            if input.get('previous', None):
                if Section.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                    section_instance.previous = Section.objects.get(pk=from_global_id(input['previous'])[1])
                else:
                    return cls(errors=['Previous Section ID not found'], success=False, section=None)

            if input.get('container', None):
                if Section.objects.filter(pk=from_global_id(input['container'])[1]).exists():
                    section_instance.container = Section.objects.get(pk=from_global_id(input['container'])[1])
                else:
                    return cls(errors=['Container Section ID not found'], success=False, section=None)

            section_instance.save()

            return cls(section=section_instance, success=True, errors=None)
        else:
            return cls(success=False, errors=['Section ID not found'], section=None)


class DeleteSection(relay.ClientIDMutation):

    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('DeleteSection.mutate_and_get_payload()')
        if Section.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            section_instance = Section.objects.get(pk=from_global_id(input['id'])[1])
            section_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class AddTokenToSection(relay.ClientIDMutation):

    class Input:
        section_id = ID(required=True)
        token_id = ID(required=True)

    success = Boolean()
    errors = List(String)
    section = Field(SectionNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('AddTokenToSection.mutate_and_get_payload()'.format(input))
        if Section.objects.filter(pk=from_global_id(input['section_id'])[1]).exists():
            section_instance = Section.objects.get(pk=from_global_id(input['section_id'])[1])
            if Token.objects.filter(pk=from_global_id(input['token_id'])[1]).exists():
                token_obj = Token.objects.get(pk=from_global_id(input['token_id'])[1])
                section_instance.tokens.add(token_obj)
                section_instance.save()
                return cls(success=True, errors=None, section=section_instance)
            else:
                return cls(success=False, errors=['Token ID not found'], section=None)
        else:
            return cls(success=False, errors=['Section ID not found'], section=None)


class Mutation(ObjectType):
    create_section = CreateSection.Field()
    update_section = UpdateSection.Field()
    delete_section = DeleteSection.Field()
    add_token_to_section = AddTokenToSection.Field()
