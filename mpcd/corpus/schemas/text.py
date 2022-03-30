
from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Text, Author, Resource, Corpus, TextSigle, Source
from mpcd.corpus.schemas.text_sigle import TextSigleInput
from mpcd.corpus.schemas.author import AuthorInput
from mpcd.corpus.schemas.source import SourceInput
from mpcd.corpus.schemas.resource import ResourceInput

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class TextNode(DjangoObjectType):
    class Meta:
        model = Text
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'stage': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)


class TextInput(InputObjectType):
    # id = ID()
    corpus = String(required=True)
    title = String(required=True)
    stage = String()
    text_sigle = TextSigleInput()
    editors = List(AuthorInput)
    collaborators = List(AuthorInput)
    resources = List(AuthorInput)
    sources = List(SourceInput)

# Query


class Query(ObjectType):
    text = relay.Node.Field(TextNode)
    all_texts = DjangoFilterConnectionField(TextNode)

    @login_required
    def resolve_all_texts(self, info, **kwargs):
        return gql_optimizer.query(Text.objects.all(), info)


# Mutations


class CreateText(relay.ClientIDMutation):
    class Input:
        corpus = ID(required=True)
        title = String(required=True)
        stage = String()
        text_sigle = TextSigleInput()
        editors = List(AuthorInput)
        collaborators = List(AuthorInput)
        resources = List(ResourceInput)
        sources = List(SourceInput)

    text = Field(TextNode)
    success = Boolean()
    errors = String()

    @classmethod
    @login_required

    def mutate_and_get_payload(cls, root, info, **input):

        # check if corpus exists
        if Corpus.objects.filter(pk=from_global_id(input.get('corpus'))[1]).exists():
            corpus_instance = Corpus.objects.get(pk=from_global_id(input.get('corpus'))[1])
        else:
            return cls(success=False, errors="Wrong corpus ID", text=None)

          # create text with title and stage (default=untouched)
        text_instance, text_created = Text.objects.get_or_create(title=input.get('title'), corpus=corpus_instance)

        if input.get('stage', None) is not None:
            text_instance.stage = input.get('stage')

        # get source
        if input.get('sources', None) is not None:
            for source in input['sources']:
                source_instance = Source.objects.get(pk=from_global_id(source.id)[1])
                text_instance.sources.add(source_instance)

        if input.get('text_sigle', None) is not None:
            text_sigle_instance, text_sigle_created = TextSigle.objects.get_or_create(
                sigle=input.get('text_sigle').get('sigle'), genre=input.get('text_sigle').get('genre'))
            text_instance.text_sigle = text_sigle_instance
        if input.get('editors', None) is not None:
            for editor in input.get('editors'):
                author_instance, author_created = Author.objects.get_or_create(
                    name=editor.name, last_name=editor.last_name)
                author_instance.save()
                text_instance.editors.add(author_instance)
        if input.get('collaborators', None) is not None:
            for collaborator in input.get('collaborators'):
                author_instance, author_created = Author.objects.get_or_create(
                    name=editor.name, last_name=collaborator.last_name)
                author_instance.save()
                text_instance.collaborators.add(author_instance)
        if input.get('resources', None) is not None:
            for resource in input.get('resources'):
                resource_instance, resource_created = Resource.objects.get_or_create(resource.id)
                if resource.get('authors', None) is not None:
                    for author in resource['authors']:
                        author_instance, author_created = Author.objects.get_or_create(
                            name=author.name, last_name=author.last_name)
                        author_instance.save()
                        resource_instance.authors.add(author_instance)
                text_instance.resources.add(resource_instance)

        text_instance.save()
        return cls(text=text_instance, success=True)

# TODO update text


class Mutation(ObjectType):
    create_text = CreateText.Field()
