
from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import TYPE_CHECKING, Optional, List

from treeflow.corpus import models


@gql.django.type(models.Source)
class Source(relay.Node):
    id: relay.GlobalID
    type: gql.auto
    identifier: gql.auto
    description: gql.auto
    references: List[gql.LazyType['BibEntry', 'treeflow.corpus.types.bibliography']]
    sources: List['Source']


@gql.django.input(models.Source)
class SourceInput:
    type: gql.auto
    identifier: gql.auto
    description: gql.auto
    references: gql.auto
    sources: gql.auto


@gql.django.partial(models.Source)
class SourcePartial(gql.NodeInputPartial):
    id: relay.GlobalID
    type: gql.auto
    identifier: gql.auto
    description: gql.auto
    references: gql.auto
    sources: gql.auto
