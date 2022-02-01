from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Section, Text, Source, Token, SectionType
from mpcd.corpus.schemas import TextNode, SourceNode, TokenNode


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


class SectionInput(InputObjectType):
    id = ID()
    identifier = String(required=True)
    text = TextNode()
    section_type = SectionNode()
    source = SourceNode()
    tokens = List(TokenNode)
    previous = SectionNode()


class CreateSection(relay.ClientIDMutation):

    class Input:
        identifier = String()
        text = TextNode()
        section_type = SectionNode()
        source = SourceNode()
        tokens = List(TokenNode)
        previous = SectionNode()

    section = Field(SectionNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('CreateSection.mutate_and_get_payload()')

        if Section.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            return cls(success=False)
        else:
            section_instance = Section.objects.create(identifier=input['identifier'])
            if input.get('text', None) is not None:
                text = Text.objects.get(pk=(input['text']['id'])[1])
                section_instance.text = text
            if input.get('section_type', None) is not None:
                section_type = SectionType.objects.get(pk=(input['section_type']['id'])[1])
                section_instance.section_type = section_type
            if input.get('source', None) is not None:
                source = Source.objects.get(pk=(input['source']['id'])[1])
                section_instance.source = source
            if input.get('tokens', None) is not None:
                for token in input('tokens'):
                    token_instance = Token.objects.get(pk=from_global_id(token['id'])[1])
                    section_instance.tokens.add(token_instance)
            if input.get('previous', None) is not None:
                previous = Section.objects.get(pk=(input['previous']['id'])[1])
                section_instance.previous = previous
            section_instance.save()
            return cls(section=section_instance, success=True)


class UpdateSection(relay.ClientIDMutation):

    class Input:
        id = ID()
        identifier = String()
        text = TextNode()
        section_type = SectionNode()
        source = SourceNode()
        tokens = List(TokenNode)
        previous = SectionNode()

    section = Field(SectionNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('UpdateSection.mutate_and_get_payload()')
        if Section.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            section_instance = Section.objects.get(pk=from_global_id(input['id'])[1])
            section_instance.identifier = input['identifier']
            if input.get('text', None) is not None:
                text = Text.objects.get(pk=(input['text']['id'])[1])
                section_instance.text = text
            if input.get('section_type', None) is not None:
                section_type = SectionType.objects.get(pk=(input['section_type']['id'])[1])
                section_instance.section_type = section_type
            if input.get('source', None) is not None:
                source = Source.objects.get(pk=(input['source']['id'])[1])
                section_instance.source = source
            if input.get('tokens', None) is not None:
                section_instance.tokens.clear()
                for token in input('tokens'):
                    token_instance = Token.objects.get(pk=from_global_id(token['id'])[1])
                    section_instance.tokens.add(token_instance)
            if input.get('previous', None) is not None:
                previous = Section.objects.get(pk=(input['previous']['id'])[1])
                section_instance.previous = previous
            section_instance.save()
            return cls(section=section_instance, success=True)
        else:
            return cls(success=False)


class DeleteSection(relay.ClientIDMutation):

    class Input:
        id = ID()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('DeleteSection.mutate_and_get_payload()')
        if Section.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            section_instance = Section.objects.get(pk=from_global_id(input['id'])[1])
            section_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_section = CreateSection.Field()
    update_section = UpdateSection.Field()
    delete_section = DeleteSection.Field()
