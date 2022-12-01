from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.dict.types.lemma import Lemma, LemmaInput, LemmaPartial
from mpcd.dict.types.meaning import MeaningInput
import mpcd.dict.models as models

@gql.type
class Query:
    lemma: Optional[Lemma] = gql.django.node()
    lemmas:  relay.Connection[Lemma] = gql.django.connection()


@gql.type
class Mutation:
    create_lemma: Lemma = gql.django.create_mutation(LemmaInput)
    update_lemma: Lemma = gql.django.update_mutation(LemmaPartial)
    delete_lemma: Lemma = gql.django.delete_mutation(gql.NodeInput)

    @gql.django.input_mutation
    def add_related_lemma_to_lemma(self, info, lemma: relay.GlobalID, related_lemma: relay.GlobalID,) -> Lemma:
        current_lemma = lemma.resolve_node(info)
        related_lemma = related_lemma.resolve_node(info)
        current_lemma.related_lemmas.add(related_lemma)
        current_lemma.save()
        return lemma

    @gql.django.input_mutation
    def add_new_related_lemma_to_lemma(self, info, lemma: relay.GlobalID, related_lemma: LemmaInput,) -> Lemma:
        current_lemma = lemma.resolve_node(info)
        related_lemma = models.Lemma.objects.create(**related_lemma)
        current_lemma.related_lemmas.add(related_lemma)
        current_lemma.save()
        return lemma


    @gql.django.input_mutation
    def add_related_meaning_to_lemma(self, info, lemma: relay.GlobalID, related_meaning: relay.GlobalID,) -> Lemma:
        current_lemma = lemma.resolve_node(info)
        related_meaning = related_meaning.resolve_node(info)
        current_lemma.related_meanings.add(related_meaning)
        current_lemma.save()
        return lemma

    @gql.django.input_mutation
    def add_related_meaning_to_lemma(self, info, lemma: relay.GlobalID, related_meaning: MeaningInput,) -> Lemma:
        current_lemma = lemma.resolve_node(info)
        related_meaning = models.Meaning.objects.create(**related_meaning)
        current_lemma.related_meanings.add(related_meaning)
        current_lemma.save()
        return lemma

    @gql.django.input_mutation
    def remove_related_lemma_from_lemma(self, info, lemma: relay.GlobalID, related_lemma: relay.GlobalID,) -> Lemma:
        current_lemma = lemma.resolve_node(info)
        related_lemma = related_lemma.resolve_node(info)
        current_lemma.related_lemmas.remove(related_lemma)
        current_lemma.save()
        return lemma

    @gql.django.input_mutation
    def remove_related_meaning_from_lemma(self, info, lemma: relay.GlobalID, related_meaning: relay.GlobalID,) -> Lemma:
        current_lemma = lemma.resolve_node(info)
        related_meaning = related_meaning.resolve_node(info)
        current_lemma.related_meanings.remove(related_meaning)
        current_lemma.save()
        return lemma


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
