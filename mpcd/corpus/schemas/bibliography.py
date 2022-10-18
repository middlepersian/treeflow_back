from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.bibliography import BibEntry


@gql.type
class Query:
    bib_entry: Optional[BibEntry] = gql.django.node()
    bib_entries:  relay.Connection[BibEntry] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])