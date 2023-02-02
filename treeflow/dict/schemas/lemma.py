from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry_django_plus.mutations import resolvers

from typing import Optional


from treeflow.dict.types.lemma import Lemma, LemmaInput, LemmaPartial
from treeflow.dict.types.meaning import MeaningInput
import treeflow.dict.models as models


from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    HasObjPerm,
    HasPerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,)


@gql.type
class Query:
    lemma: Optional[Lemma] = gql.django.node(directives=[IsAuthenticated()])
    lemmas:  relay.Connection[Lemma] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_lemma: Lemma = gql.django.create_mutation(LemmaInput, directives=[IsAuthenticated()])
    update_lemma: Lemma = gql.django.update_mutation(LemmaPartial, directives=[IsAuthenticated()])
    delete_lemma: Lemma = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])

    @gql.django.input_mutation
    def add_related_lemma_to_lemma(self, info, lemma: relay.GlobalID, related_lemma: relay.GlobalID,) -> Lemma:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current_lemma = lemma.resolve_node(info)
        related_lemma = related_lemma.resolve_node(info)
        current_lemma.related_lemmas.add(related_lemma)
        current_lemma.save()
        return current_lemma

    @gql.django.input_mutation
    def add_new_related_lemma_to_lemma(self, info, lemma: relay.GlobalID, related_lemma: LemmaInput,) -> Lemma:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current_lemma = lemma.resolve_node(info)
        data = vars(related_lemma)
        related_lemma = resolvers.create(info, models.Lemma, resolvers.parse_input(info, data))
        current_lemma.related_lemmas.add(related_lemma)
        current_lemma.save()
        return current_lemma

    @gql.django.input_mutation
    def add_related_meaning_to_lemma(self, info, lemma: relay.GlobalID, related_meaning: relay.GlobalID,) -> Lemma:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current_lemma = lemma.resolve_node(info)
        related_meaning = related_meaning.resolve_node(info)
        current_lemma.related_meanings.add(related_meaning)
        current_lemma.save()
        return current_lemma

    @gql.django.input_mutation
    def add_new_related_meaning_to_lemma(self, info, lemma: relay.GlobalID, related_meaning: MeaningInput,) -> Lemma:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current_lemma = lemma.resolve_node(info)
        data = vars(related_meaning)
        related_meaning = resolvers.create(info, models.Meaning, resolvers.parse_input(info, data))
        current_lemma.related_meanings.add(related_meaning)
        current_lemma.save()
        return current_lemma

    @gql.django.input_mutation
    def remove_related_lemma_from_lemma(self, info, lemma: relay.GlobalID, related_lemma: relay.GlobalID,) -> Lemma:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current_lemma = lemma.resolve_node(info)
        related_lemma = related_lemma.resolve_node(info)
        current_lemma.related_lemmas.remove(related_lemma)
        current_lemma.save()
        return current_lemma

    @gql.django.input_mutation
    def remove_related_meaning_from_lemma(self, info, lemma: relay.GlobalID, related_meaning: relay.GlobalID,) -> Lemma:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current_lemma = lemma.resolve_node(info)
        related_meaning = related_meaning.resolve_node(info)
        current_lemma.related_meanings.remove(related_meaning)
        current_lemma.save()
        return current_lemma


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
