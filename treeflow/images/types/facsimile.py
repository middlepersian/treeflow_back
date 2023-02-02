from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from treeflow.images import models

@gql.django.type(models.Facsimile)
class Facsimile(relay.Node):
    image_facsimile: relay.Connection[gql.LazyType['Image', 'treeflow.images.types.image']]

    id: relay.GlobalID
    bib_entry: gql.LazyType['BibEntry', 'treeflow.corpus.types.bibliography']
    codex:  gql.LazyType['Codex','treeflow.corpus.types.codex']


@gql.django.input(models.Facsimile)
class FacsimileInput:
    bib_entry: gql.auto
    codex: gql.auto


@gql.django.partial(models.Facsimile)
class FacsimilePartial(gql.NodeInputPartial):
    id: relay.GlobalID
    bib_entry: gql.auto
    codex: gql.auto
