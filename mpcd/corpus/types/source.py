
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional
from strawberry.lazy_type import LazyType

from mpcd.corpus import models


@gql.django.type(models.Source)
class Source(relay.Node):
    id: gql.auto
    identifier: gql.auto
    bib_entry: LazyType['BibEntry', 'mpcd.corpus.types.bibliography']
    description: gql.auto
