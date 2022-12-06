from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.bibliography import BibEntry, BibEntryInput, BibEntryPartial
from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    HasObjPerm,
    HasPerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,)


@gql.type
class Query:
    bib_entry: Optional[BibEntry] = gql.django.node(directives=[IsAuthenticated()])
    bib_entries:  relay.Connection[BibEntry] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    """All available mutations for this schema."""

    create_bib_entry: BibEntry = gql.django.create_mutation(BibEntryInput, directives=[IsAuthenticated()])
    update_bib_entry: BibEntry = gql.django.update_mutation(BibEntryPartial, directives=[IsAuthenticated()])
    delete_bib_entry: BibEntry = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
