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
    comment_codex_part: relay.Connection[gql.LazyType['Comment', 'mpcd.corpus.types.comment']] 
    facsimile_codex_part: relay.Connection[gql.LazyType['Facsimile', 'mpcd.corpus.types.facsimile']]

    id: relay.GlobalID
    codex: gql.LazyType['Codex','mpcd.corpus.types.codex']
    slug: gql.auto


@gql.django.input(models.CodexPart)
class CodexPartInput:
    codex: gql.auto
    slug: gql.auto


@gql.django.partial(models.CodexPart)
class CodexPartPartial(gql.NodeInputPartial):
    id: relay.GlobalID
    codex: gql.auto
    slug: gql.auto
