from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Annotated, List, TYPE_CHECKING
from mpcd.corpus import models

if TYPE_CHECKING:
    from .codex_part import CodexPart
    from .comment import Comment


@gql.django.type(models.Codex)
class Codex(relay.Node):
    codex_part_codex: relay.Connection[gql.LazyType['CodexPart', 'mpcd.corpus.types.codex_part']]

    sigle: gql.auto
    comments: List[Annotated['Comment', lazy('mpcd.corpus.types.comment')]]
