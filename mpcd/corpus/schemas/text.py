from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Text, Author, Resource, Source, TextSigle
from mpcd.corpus.schemas.text_sigle import TextSigleInput
from mpcd.corpus.schemas.corpus import CorpusNode
from mpcd.corpus.schemas.author import AuthorInput
from mpcd.corpus.schemas.source import SourceNode
from mpcd.corpus.schemas.resource import ResourceInput


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
    id = ID()
    corpus = CorpusNode()
    title = String()
    stage = String()
    text_sigle = TextSigleInput()
    editors = List(AuthorInput)
    collaborators = List(AuthorInput)
    resources = List(AuthorInput)
    sources = List(SourceNode)

# Query


class Query(ObjectType):
    text = relay.Node.Field(TextNode)
    all_texts = DjangoFilterConnectionField(TextNode)

# Mutations


class CreateText(relay.ClientIDMutation):
    class Input:
        id = ID()
        corpus = CorpusNode()
        title = String()
        stage = String()
        text_sigle = TextSigleInput()
        editors = List(AuthorInput)
        collaborators = List(AuthorInput)
        resources = List(ResourceInput)
        sources = List(SourceNode)

    text = Field(TextNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, corpus, title, stage, text_sigle, editors, collaborators, resources, sources):

        # check that text does not exist same title and year
        if Text.objects.filter(title=title).exists():
            return cls(success=False)

        else:
            text_instance = Text.objects.create(id=id, title=title, stage=stage)

            if TextSigle.objects.filter(sigle=text_sigle.sigle).exists():
                text_sigle_instance = TextSigle.objects.get(sigle=text_sigle.sigle)
            else:
                text_sigle_instance = TextSigle.objects.create(sigle=text_sigle.sigle, genre=text_sigle.genre)
            text_instance.text_sigle = text_sigle_instance

            for editor in editors:
                author_instance, author_created = Author.objects.get_or_create(
                    name=editor.name, last_name=editor.last_name)
                author_instance.save()
                text_instance.editors.add(author_instance)

            for collaborator in collaborators:
                author_instance, author_created = Author.objects.get_or_create(
                    name=editor.name, last_name=collaborator.last_name)
                author_instance.save()
                text_instance.collaborators.add(author_instance)

            for resource in resources:
                resource_instance, resource_created = Resource.objects.get_or_create(resource.id)
                if resource.get('authors', None) is not None:
                    for author in resource['authors']:
                        author_instance, author_created = Author.objects.get_or_create(
                            name=author.name, last_name=author.last_name)
                        author_instance.save()
                        resource_instance.authors.add(author_instance)
                text_instance.resources.add(resource_instance)

            for source in sources:
                if Source.object.filter(id=source.id).exists():
                    source_instance = Source.objects.get(pk=from_global_id(id[1]))
                    text_instance.sources.add(source_instance)
