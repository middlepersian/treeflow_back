from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING
from mpcd.corpus import models


@gql.django.type(models.Facsimile)
class Facsimile(relay.Node):
    folio_facsimile: relay.Connection[LazyType['Folio', 'mpcd.corpus.types.folio']]

    id: gql.auto
    bib_entry: LazyType['BibEntry', 'mpcd.corpus.types.bibliography']
    codex_part:  LazyType['CodexPart', 'mpcd.corpus.types.codex_part']
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
    folios: List[LazyType['Folio', 'mpcd.corpus.types.folio']]
