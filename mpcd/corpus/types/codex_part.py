from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Annotated

from mpcd.corpus import models

from .facsimile import Facsimile
from .codex import Codex
from .comment import Comment


@gql.django.type(models.CodexPart)
class CodexPart(relay.Node):
    facsimile_codex_part: relay.Connection[gql.LazyType['Facsimile', 'mpcd.corpus.types.facsimile']]

    id: gql.auto
    codex: gql.LazyType['Codex','mpcd.corpus.types.codex']
    slug: gql.auto
    comments: List[gql.LazyType['Comment', 'mpcd.corpus.types.comment']]


@gql.django.input(models.CodexPart)
class CodexPartInput:
    codex: gql.auto
    slug: gql.auto
    comments: gql.auto


@gql.django.partial(models.CodexPart)
class CodexPartPartial(gql.NodeInputPartial):
    id: gql.auto
    codex: gql.auto
    slug: gql.auto
    comments: gql.auto
