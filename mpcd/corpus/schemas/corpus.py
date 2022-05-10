from typing import List
from numpy import require
from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from mpcd.corpus.models import Corpus

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required, superuser_required


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
    slug = String(required=True)


class Query(ObjectType):
    corpus = relay.Node.Field(CorpusNode)
    all_corpus = DjangoFilterConnectionField(CorpusNode)

    def resolve_all_corpus(self, info, **kwargs):
        return gql_optimizer.query(Corpus.objects.all(), info)


# Mutations


class CreateCorpus(relay.ClientIDMutation):
    class Input:
        name = String(required=True)
        slug = String(required=True)

    corpus = Field(CorpusNode)
    success = Boolean()

    @classmethod
    @superuser_required
    def mutate_and_get_payload(cls, root, info, name, slug):
        corpus_obj, corpus_created = Corpus.objects.get_or_create(name=name, slug=slug)
        return cls(success=True, corpus=corpus_obj)


class UpdateCorpus(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        name = String(required=True)
        slug = String(required=True)

    corpus = Field(CorpusNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, id, name, slug):
        if Corpus.objects.filter(pk=from_global_id(id)[1]).exists():
            corpus = Corpus.objects.get(pk=from_global_id(id)[1])
            corpus.name = name
            corpus.slug = slug
            corpus.save()
            return cls(corpus=corpus, success=True)
        else:
            return cls(success=True, errors=['Corpus ID does not exist'], corpus=None)


class Mutation(ObjectType):
    create_corpus = CreateCorpus.Field()
    update_corpus = UpdateCorpus.Field()
