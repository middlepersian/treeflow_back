from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Codex, BibEntry, Comment
from mpcd.corpus.schemas.codex_enum import Codices
from graphql_relay import from_global_id


import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required, superuser_required


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class CodexNode(DjangoObjectType):
    class Meta:
        model = Codex
        filter_fields = {'sigle': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class CodexInput(InputObjectType):
    sigle = Codices(required=True)


class Query(ObjectType):
    codex = relay.Node.Field(CodexNode)
    all_codex = DjangoFilterConnectionField(CodexNode)

    @login_required
    def resolve_all_codex(self, info, **kwargs):
        return gql_optimizer.query(Codex.objects.all(), info)

# Mutations


class CreateCodex(relay.ClientIDMutation):
    class Input:
        sigle = Codices(required=True)
        bib_entry = ID(required=True)

    codex = Field(CodexNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        codex_instance, codex_created = Codex.objects.get_or_create(sigle=input.get('sigle'))
        if BibEntry.objects.filter(pk=from_global_id(input.get('bib_entry'))[1]).exists():
            bib_entry_instance = BibEntry.objects.get(pk=from_global_id(input.get('bib_entry'))[1])
            codex_instance.bib_entry = bib_entry_instance
            codex_instance.save()

        else:
            return cls(errors=['BibEntry does not exist'])

        return cls(codex=codex_instance, success=True)


class UpdateCodex(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        sigle = Codices(required=True)
        bib_entry = ID(required=True)
        comments = List(ID, required=True)

    codex = Field(CodexNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        # check that bib exists with id
        if Codex.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            codex_instance = Codex.objects.get(pk=from_global_id(input.get('id'))[1])
            # udpate sigle
            codex_instance.sigle = input.get('sigle')
            # update bib_entry
            if BibEntry.objects.filter(pk=from_global_id(input.get('bib_entry'))[1]).exists():
                bib_entry_instance = BibEntry.objects.get(pk=from_global_id(input.get('bib_entry'))[1])
                codex_instance.bib_entry = bib_entry_instance
            else:
                return cls(success=False, errors=['BibEntry ID does not exist'])

            # update comments
            codex_instance.comments.clear()
            for comment in input.get('comments'):
                if Comment.objects.filter(pk=from_global_id(comment)[1]).exists():
                    codex_instance.comments.add(Comment.objects.get(pk=from_global_id(comment)[1]))

            codex_instance.save()

        return cls(codex=codex_instance, success=True)


class DeleteCodex(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    @superuser_required
    def mutate_and_get_payload(cls, root, info, id):
        # check that codex exists with id
        if Codex.objects.filter(pk=from_global_id(id)[1]).exists():
            codex_instance = Codex.objects.get(pk=from_global_id(id)[1])
            codex_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_codex = CreateCodex.Field()
    delete_codex = DeleteCodex.Field()
    update_codex = UpdateCodex.Field()
