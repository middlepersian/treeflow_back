from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List
from mpcd.corpus import models
from mpcd.corpus.types import Folio, Comment, BibEntry, CodexPart


@gql.django.type(models.Facsimile)
class Facsimile:
    id: gql.auto
    bib_entry: 'BibEntry'
    codex_part: 'CodexPart'
    comments: List['Comment']
    folios: List['Folio']
