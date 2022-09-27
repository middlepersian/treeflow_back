from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING
from mpcd.corpus import models

if TYPE_CHECKING:
    from mpcd.corpus.types.folio import Folio
    from mpcd.corpus.types.comment import Comment
    from mpcd.corpus.types.bibliography import BibEntry
    from mpcd.corpus.types.codex_part import CodexPart


@gql.django.type(models.Facsimile)
class Facsimile:
    id: gql.auto
    bib_entry: LazyType['BibEntry', 'mpcd.corpus.types.bibliography']
    codex_part:  LazyType['CodexPart', 'mpcd.corpus.types.codex_part']
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
    folios: List[LazyType['Folio', 'mpcd.corpus.types.folio']]
