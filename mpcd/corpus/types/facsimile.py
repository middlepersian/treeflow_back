from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Annotated, List, TYPE_CHECKING, Optional
from mpcd.corpus import models
from mpcd.corpus.types.comment import CommentPartial, CommentInput

if TYPE_CHECKING:
    from .bibliography import BibEntry
    from .codex import Codex
    from .comment import Comment, CommentPartial, CommentInput
    from .folio import Folio


@gql.django.type(models.Facsimile)
class Facsimile(relay.Node):
    folio_facsimile: relay.Connection[gql.LazyType['Folio', 'mpcd.corpus.types.folio']]

    id: relay.GlobalID
    bib_entry: gql.LazyType['BibEntry', 'mpcd.corpus.types.bibliography']
    codex:  gql.LazyType['Codex','mpcd.corpus.types.codex']


@gql.django.input(models.Facsimile)
class FacsimileInput:
    bib_entry: gql.auto
    codex: gql.auto


@gql.django.partial(models.Facsimile)
class FacsimilePartial(gql.NodeInputPartial):
    id: relay.GlobalID
    bib_entry: gql.auto
    codex: gql.auto
