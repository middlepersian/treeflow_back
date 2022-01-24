from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Corpus
from mpcd.corpus.schemas.author import AuthorInput


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class CorpusNode(DjangoObjectType):
    class Meta:
        model = Corpus
        filter_fields = {'name': ['exact', 'icontains', 'istartswith'],
                         'slug': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class CorpusInput(InputObjectType):
    name = String()
    slug = String()


class Query(ObjectType):
    corpus = relay.Node.Field(CorpusNode)
    all_corpus = DjangoFilterConnectionField(CorpusNode)


# Mutations

class CreateCorpus(relay.ClientIDMutation):
    class Input:
        name = String(required=True)
        slug = String(required=True)

    corpus = Field(CorpusNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, name, slug):
        corpus = Corpus.objects.create(name=name, slug=slug)
        return CreateCorpus(corpus=corpus)


class UpdateCorpus(relay.ClientIDMutation):
    class Input:
        id = ID()
        name = String()
        slug = String()

    corpus = Field(CorpusNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, name, slug):
        if Corpus.objects.filter(id=id).exists():
            corpus = Corpus.objects.get(id=id)
            corpus.name = name
            corpus.slug = slug
            corpus.save()
            success = True
            return cls(corpus=corpus, success=success)
        else:
            success = False
            return cls(success=success)


class DeleteCorpus(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        if Corpus.objects.filter(id=id).exists():
            Corpus.objects.get(id=id).delete()
            success = True
            return cls(success=success)
        else:
            success = False
            return cls(success=success)


class Mutation(ObjectType):
    create_corpus = CreateCorpus.Field()
    update_corpus = UpdateCorpus.Field()
    delete_corpus = DeleteCorpus.Field()
