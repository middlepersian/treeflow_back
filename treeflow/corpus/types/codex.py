from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Annotated, List, TYPE_CHECKING
from treeflow.corpus import models

if TYPE_CHECKING:
    from .facsimile import Facsimile
    from .comment import Comment


@gql.django.type(models.Codex)
class Codex(relay.Node):
    id: relay.GlobalID
    facsimile_codex: relay.Connection[gql.LazyType['Facsimile', 'treeflow.corpus.types.facsimile']]

    sigle: gql.auto
