
from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import TYPE_CHECKING, Annotated

from mpcd.corpus import models

if TYPE_CHECKING:
    from .bibliography import BibEntry


@gql.django.type(models.Source)
class Source(relay.Node):
    #id: gql.auto
    identifier: gql.auto
    bib_entry: gql.LazyType['BibEntry', 'mpcd.corpus.types.bibliography']
    description: gql.auto


@gql.django.input(models.Source)
class SourceInput:
    identifier: gql.auto
    bib_entry: gql.auto
    description: gql.auto


@gql.django.partial(models.Source)
class SourcePartial(gql.NodeInputPartial):
    id: gql.auto
    identifier: gql.auto
    bib_entry: gql.auto
    description: gql.auto
