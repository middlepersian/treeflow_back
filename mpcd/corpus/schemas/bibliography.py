from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.bibliography import BibEntry, BibEntryInput, BibEntryPartial


@gql.type
class Query:
    bib_entry: Optional[BibEntry] = gql.django.node()
    bib_entries:  relay.Connection[BibEntry] = gql.django.connection()


@gql.type
class Mutation:
    """All available mutations for this schema."""

    create_bib_entry: BibEntry = gql.django.create_mutation(BibEntryInput)
    update_bib_entry: BibEntry = gql.django.update_mutation(BibEntryPartial)
    delete_bib_entry: BibEntry = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
