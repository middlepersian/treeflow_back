
from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import TYPE_CHECKING, Annotated

from treeflow.corpus import models

if TYPE_CHECKING:
    from .bibliography import BibEntry


@gql.django.type(models.Source)
class Source(relay.Node):
    id: relay.GlobalID
    type: gql.auto
    identifier: gql.auto
    bib_entry: gql.LazyType['BibEntry', 'treeflow.corpus.types.bibliography']
    description: gql.auto


@gql.django.input(models.Source)
class SourceInput:
    type: gql.auto
    identifier: gql.auto
    bib_entry: gql.auto
    description: gql.auto


@gql.django.partial(models.Source)
class SourcePartial(gql.NodeInputPartial):
    id: relay.GlobalID
    type: gql.auto
    identifier: gql.auto
    bib_entry: gql.auto
    description: gql.auto
