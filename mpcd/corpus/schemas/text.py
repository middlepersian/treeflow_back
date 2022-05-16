
from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Text, Author, Resource, Corpus, TextSigle, Source
from django.contrib.auth.models import User
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
    corpus = ID(required=True)
    title = String(required=True)
    stage = String(required=True)
    text_sigle = ID(required=True)
    editors = List(User, required=False)
    collaborators = List(User, required=False)
    resources = List(ID, required=True)
    sources = List(ID, required=True)
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
        stage = String(required=True)
        text_sigle = ID(required=True)
        editors = List(User, required=False)
        collaborators = List(User, required=False)
        resources = List(ID, required=True)
        sources = List(ID, required=True)

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

        # set stage
        text_instance.stage = input.get('stage')

        # set text sigle
        if TextSigle.objects.filter(pk=from_global_id(input.get('text_sigle'))[1]).exists():
            text_sigle_instance = TextSigle.objects.get(pk=from_global_id(input.get('text_sigle'))[1])
        else:
            return cls(success=False, errors="Wrong text sigle ID", text=None)

        # get sources
        for source in input['sources']:
            source_instance = Source.objects.get(pk=from_global_id(source.id)[1])
            text_instance.sources.add(source_instance)

        # get editors
        if input.get('editors', None):
            for editor in input.get('editors'):
                editor_instance = User.objects.get(username=editor.get('username'))
                text_instance.editors.add(editor_instance)

        # add collaborators
        if input.get('collaborators', None):
            for collaborator in input.get('collaborators'):
                collaborator_instance = User.objects.get(username=collaborator.get('username'))
                text_instance.collaborators.add(collaborator_instance)

        if input.get('resources'):
            for resource in input.get('resources'):
                resource_instance, resource_created = Resource.objects.get_or_create(resource.id)
                if resource.get('authors'):
                    for author in resource['authors']:
                        author_instance, author_created = Author.objects.get_or_create(
                            name=author.name, last_name=author.last_name)
                        author_instance.save()
                        resource_instance.authors.add(author_instance)
                text_instance.resources.add(resource_instance)

        text_instance.save()
        return cls(text=text_instance, success=True)


class UpdateText(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        title = String(required=True)
        stage = String(required=True)
        text_sigle = ID(required=True)
        editors = List(User, required=False)
        collaborators = List(User, required=False)
        resources = List(ID, required=True)
        sources = List(ID, required=True)

    text = Field(TextNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        # check if text exists
        if Text.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            text_instance = Text.objects.get(pk=from_global_id(input.get('id'))[1])
        else:
            return cls(success=False, errors="Wrong text ID", text=None)

        # set title
        text_instance.title = input.get('title')

        # set stage
        text_instance.stage = input.get('stage')

        # set text sigle
        if TextSigle.objects.filter(pk=from_global_id(input.get('text_sigle'))[1]).exists():
            text_sigle_instance = TextSigle.objects.get(pk=from_global_id(input.get('text_sigle'))[1])
        else:
            return cls(success=False, errors="Wrong text sigle ID", text=None)

        # TODO check how to properly do this with graphql
        # add editors
        if input.get('editors', None):
            for editor in input.get('editors'):
                editor_instance = User.objects.get(username=editor.get('username'))
                text_instance.editors.add(editor_instance)

        # add collaborators
        if input.get('collaborators', None):
            for collaborator in input.get('collaborators'):
                collaborator_instance = User.objects.get(username=collaborator.get('username'))
                text_instance.collaborators.add(collaborator_instance)

        # get resources
        for resource in input.get('resources'):
            resource_instance, resource_created = Resource.objects.get_or_create(resource.id)
            if resource.get('authors'):
                for author in resource['authors']:
                    author_instance, author_created = Author.objects.get_or_create(
                        name=author.name, last_name=author.last_name)
                    author_instance.save()
                    resource_instance.authors.add(author_instance)
            text_instance.resources.add(resource_instance)

        # get sources
        for source in input['sources']:
            source_instance = Source.objects.get(pk=from_global_id(source.id)[1])
            text_instance.sources.add(source_instance)

        text_instance.save()
        return text_instance


class Mutation(ObjectType):
    create_text = CreateText.Field()
    update_text = UpdateText.Field()
