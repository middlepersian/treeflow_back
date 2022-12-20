from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional, cast

from mpcd.dict.types.meaning import Meaning, MeaningInput, MeaningPartial
from mpcd.dict.models.meaning import Meaning as MeaningModel

from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    HasObjPerm,
    HasPerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,
)


@gql.type
class Query:
    meaning: Optional[Meaning] = gql.django.node(directives=[IsAuthenticated()])
    meanings:  relay.Connection[Meaning] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:

    create_meaning: Meaning = gql.django.create_mutation(MeaningInput, directives=[IsAuthenticated()])
    update_meaning: Meaning = gql.django.update_mutation(MeaningPartial, directives=[IsAuthenticated()])
    delete_meaning: Meaning = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])

    @gql.django.input_mutation
    def add_related_meaning_to_meaning(self, info, meaning: relay.GlobalID, related: relay.GlobalID) -> Meaning:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")

        try:
            current_meaning = meaning.resolve_node(info)
        except:
            raise Exception("Meaning not found.")
        try:
            related_meaning = related.resolve_node(info)
        except:
            raise Exception("Related meaning not found.")
        current_meaning.related_meanings.add(related_meaning)
        current_meaning.save()
        return current_meaning


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
