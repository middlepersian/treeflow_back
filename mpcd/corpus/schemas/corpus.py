from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from mpcd.corpus.models import Corpus


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
    # not a relay-comform query
    corpus_slug = Field(
        CorpusNode,
        slug=String(),
    )

    def resolve_corpus_slug(root, info, slug):
        return Corpus.objects.filter(slug=slug).first()


# Mutations

class CreateCorpus(relay.ClientIDMutation):
    class Input:
        name = String(required=True)
        slug = String(required=True)

    corpus = Field(CorpusNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, name, slug):
        corpus = Corpus.objects.create(name=name, slug=slug)
        corpus.save()
        return cls(success=True, corpus=corpus)


class UpdateCorpus(relay.ClientIDMutation):
    class Input:
        id = ID()
        name = String()
        slug = String()

    corpus = Field(CorpusNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, name, slug):
        if Corpus.objects.filter(pk=from_global_id(id)[1]).exists():
            corpus = Corpus.objects.get(pk=from_global_id(id)[1])
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
        if Corpus.objects.filter(pk=from_global_id(id)[1]).exists():
            Corpus.objects.get(pk=from_global_id(id)[1]).delete()
            success = True
            return cls(success=success)
        else:
            success = False
            return cls(success=success)


class Mutation(ObjectType):
    create_corpus = CreateCorpus.Field()
    update_corpus = UpdateCorpus.Field()
    delete_corpus = DeleteCorpus.Field()
